"""Turn verified harvests into claim-level evidence. No model selection here."""
import json
from pathlib import Path

KEYS=['herg','lipophilicity_astrazeneca','solubility_aqsoldb','cyp3a4_veith']
SHORT=['hERG','Lipophilicity','Solubility','CYP3A4']
SPLITS=['scaffold','random']
MET=['AUROC','rho','rho','AUROC']
def read(path):
    return json.loads(Path(path).read_text())
def favorable(m,t):
    if t['p'] is None or t['p']>=.05:
        return False
    if m=='RMSE':
        return t['delta']<=-.020 and t['CI'][1]<0
    return t['delta']>=.010 and t['CI'][0]>0
def worse(m,t):
    if t['p'] is None or t['p']>=.05:
        return False
    return t['delta']>=.020 if m=='RMSE' else t['delta']<=-.010
def format_delta(r):
    return f"{r['delta']:+.4f} [{r['CI'][0]:+.4f}, {r['CI'][1]:+.4f}], p={r['p']:.5f}"
def fdelta(r):
    return f"{r['delta']:+.4f} ({r['p']:.5f})"
def collect():
    cards={k:{} for k in ('C1','C2','C3','C4','C5','C6')}
    for i,(key,label,m) in enumerate(zip(KEYS,SHORT,MET)):
        prep=read(f'audit/{key}.json')['stats']
        for split in SPLITS:
            prefix=f'audit/{key}-{split}'
            d=read(prefix+'-stats.json')
            a=read(prefix+'-audit.json')
            cell=label+' '+split
            for claim,comparison in [('C1','CP_D-A_D'),('C2','CP_C-A_C')]:
                stats=d['all']['diffs'][comparison]
                eligible=[m]+(['RMSE'] if m=='rho' else [])
                card=dict(metrics=stats,H1_pass=any(favorable(t,stats[t]) for t in eligible),
                          degradation=any(worse(t,stats[t]) for t in eligible),
                          seed_deltas=d['all']['matched_seed_deltas']['D' if claim=='C1' else 'C'])
                if claim=='C1':
                    card['CP_minus_ID']=d['all']['diffs']['CP_D-ID_D'][m]
                cards[claim][cell]=card
            cards['C3'][cell]=dict(n=d['unseen_any']['n'],metrics=d['unseen_any']['diffs']['CP_C-A_C'])
            cards['C4'][cell]=dict(teacher_rho=d['all']['points']['CP_C']['teacher_rho'],
                                   teacher_pearson=d['all']['points']['CP_C']['teacher_r'],
                                   gap=d['all']['diffs']['CP_C-teacher'],CP=d['all']['points']['CP_C'][m]['value'],
                                   FullMol=d['all']['points']['teacher'][m]['value'])
            if split=='scaffold':
                cards['C5'][label]=dict(clean=prep['clean'],decomposable=prep['decomp'],fraction=prep['decomp']/prep['clean'])
            cards['C5'][label][split]={k:a[k] for k in ('both_seen','one_seen','neither_seen','both_any','split_sizes')}
    cards['C6']=dict(coverage=cards['C5']['Solubility']['fraction'],decomposable=cards['C5']['Solubility']['decomposable'],
                     clean=cards['C5']['Solubility']['clean'],**cards['C4']['Solubility scaffold'])
    sensitivity_root=Path('audit/salt-sensitivity')
    if (sensitivity_root/'counts.json').is_file():
        counts=read(sensitivity_root/'counts.json')
        for key,l in zip(KEYS,SHORT):
            cards['C5'][l]['opposite_salt_tie']=counts[key]
    alt=sensitivity_root/'audit/solubility_aqsoldb-scaffold-stats.json'
    if alt.is_file():
        d=read(alt)['all']
        cards['C6']['opposite_salt_tie']=dict(counts=cards['C5']['Solubility']['opposite_salt_tie'],
              CP=d['points']['CP_C']['rho']['value'],FullMol=d['points']['teacher']['rho']['value'],
              gap=d['diffs']['CP_C-teacher']['rho'],teacher_rho=d['points']['CP_C']['teacher_rho']['value'])
    for cid in ('C1','C2'):
        totals={s:sum(v['H1_pass'] for k,v in cards[cid].items() if k.endswith(s)) for s in SPLITS}
        bad=[k for k,v in cards[cid].items() if v['degradation']]
        cards[cid]['H1']={**totals,'significant_degradations':bad,'overall':(totals['scaffold']>=2 or totals['random']>=3) and not bad}
    return cards
if __name__=='__main__':
    cards=collect()
    for claim,models in cards.items():
        print(claim)
        if claim=='C6':
            print(models)
            continue
        for k,v in models.items():
            if claim=='C5' or k=='H1':
                print(k,v)
            elif claim=='C4':
                m='rho' if 'rho' in v['gap'] else 'AUROC'
                print(k,round(v['teacher_rho']['value'],4),format_delta(v['gap'][m]))
            else:
                m='rho' if 'rho' in v['metrics'] else 'AUROC'
                print(k,format_delta(v['metrics'][m]),fdelta(v['metrics']['RMSE']) if 'RMSE' in v['metrics'] else '',fdelta(v['CP_minus_ID']) if claim=='C1' else '')

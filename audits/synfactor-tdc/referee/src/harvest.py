"""Verify raw artifacts, complete finite prediction array inventory and report receipt."""
from pathlib import Path
import hashlib
import json
import numpy as np
from summary import KEYS, SHORT, SPLITS, collect, read

def main():
    cards=collect()
    verdict=read('verdict.json')
    assert verdict['study']=='ref-synfactor-tdc-1125'
    assert [x['id'] for x in verdict['verdicts']]==list(cards)
    assert all(x['independent']==cards[x['id']] for x in verdict['verdicts'])
    checks={}
    for key in KEYS:
        for name in SPLITS:
            prefix=f'audit/{key}-{name}'
            stats=read(prefix+'-stats.json')
            p=np.load(prefix+'-eval.npz')
            n=len(p['truth'])
            assert all(np.isfinite(p[k]).all() and len(p[k])==n for k in p.files)
            assert stats['all']['n']==n==stats['both_seen']['n']+stats['unseen_any']['n']
            assert len(stats['all']['points'])==9 and len(stats['all']['diffs'])==5
            seeds=[]
            for mode in 'DTC':
                for kind in ('CP','A'):
                    for seed in (42,43,44):
                        path=Path(f'{prefix}-{kind}_{mode}-{seed}.npz')
                        run=np.load(path)
                        assert np.isfinite(run['pred']).all() and run['pred'].shape==(n,)
                        assert 1<=int(run['best_epoch'])<=int(run['epochs'])<=300
                        seeds.append(hashlib.sha256(path.read_bytes()).hexdigest())
            checks[key+' '+name]=dict(n=n,seed_fits=len(seeds),prediction_archive_chain_sha256=hashlib.sha256(''.join(seeds).encode()).hexdigest())
    prefix='audit/salt-sensitivity/audit/solubility_aqsoldb-scaffold'
    alt_n=len(np.load(prefix+'-eval.npz')['truth'])
    archives=[]
    for mode in 'DTC':
        for kind in ('CP','A'):
            for seed in (42,43,44):
                path=Path(f'{prefix}-{kind}_{mode}-{seed}.npz')
                run=np.load(path)
                assert run['pred'].shape==(alt_n,) and np.isfinite(run['pred']).all()
                assert 1<=int(run['best_epoch'])<=int(run['epochs'])<=300
                archives.append(hashlib.sha256(path.read_bytes()).hexdigest())
    checks['secondary solubility scaffold']=dict(n=alt_n,seed_fits=len(archives),prediction_archive_chain_sha256=hashlib.sha256(''.join(archives).encode()).hexdigest())
    for path in ('verdict.json','VERDICT.md','REPORT.md','PRIOR_ART.md'):
        assert Path(path).stat().st_size>0
    assert Path('REPORT.md').read_text().startswith('Shipped:') and len(Path('REPORT.md').read_text().splitlines())<25
    assert Path('STATUS.md').read_text().splitlines()[0].startswith('You asked:')
    assert all(k in Path('VERDICT.md').read_text() for k in ('CONTROLS:','CONTRADICTING:','LABELS:'))
    Path('audit/harvest.json').write_text(json.dumps(checks,indent=2)+'\n')
if __name__=='__main__':
    main()

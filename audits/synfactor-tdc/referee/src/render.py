"""Render the final, independently checked evidence and human referee decisions."""
from pathlib import Path
import json
import re
from summary import KEYS, SHORT, SPLITS, MET, collect, read, format_delta

def md_table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join('---' for _ in headers)+'|']+
                     ['| '+' | '.join(map(str,r))+' |' for r in rows])
def main():
    c=collect()
    decisions=read('audit/decisions.json')
    claims=dict(re.findall(r'^- \*\*(C[1-6]) (.*?)$',Path('CLAIMS_TO_CHECK.md').read_text(),re.M))
    verdicts=[dict(id=k,verdict=decisions[k][0],claimed=claims[k].replace('**',''),independent=v,reason=decisions[k][1]) for k,v in c.items()]
    Path('verdict.json').write_text(json.dumps(dict(study='ref-synfactor-tdc-1125',verdicts=verdicts),allow_nan=False,indent=2)+'\n')
    labels=read('audit/crosscheck.json')
    pair=read('audit/pair-control.json')
    cp=read('audit/cp-control.json')
    ridge=read('audit/ridge-control.json')
    leak=read('audit/leakage.json')
    lines=['# Independent referee verdict','',
           'Four raw TDC files, eight fixed test sets, 144 neural fits and 48 seed ensembles. Differences below are CP16 minus the named comparator. AUROC applies to hERG and CYP3A4, Spearman ρ to the two regression endpoints. Brackets give paired 95% bootstrap intervals. All p-values are two-sided Monte Carlo tests. Full-precision results are in verdict.json and the per-split statistics files.','',
           md_table(['Claim','Claimed result','Independent verdict and result'],[[r['id'],decisions[r['id']][2],r['verdict']+'. '+r['reason']] for r in verdicts])]
    claimed_D=['−.0065 (.863)','−.0068 (.647)','+.0032 (.832)','+.0020 (.639)']
    claimed_C={'scaffold':['+.0104 (n.s.)','+.0255 / −.0430 RMSE','+.0247 / −.0756 RMSE','+.0209 / +.0429 AP'],
               'random':['+.0094 (n.s.)','+.0352','+.0220','+.0161']}
    lines+=['','## C1. Direct experimental training','',
            'The large-endpoint scaffold ID comparisons were claimed to span +0.11 to +0.32, all p < 0.001. The claim supplies no individual random-split deltas.','']
    rows=[]
    for s in SPLITS:
        for i,l in enumerate(SHORT):
            cell=f'{l} {s}'
            v=c['C1'][cell]; m=MET[i]
            rows.append([cell,claimed_D[i] if s=='scaffold' else 'no pass',format_delta(v['metrics'][m]),
                         format_delta(v['metrics']['RMSE']) if m=='rho' else '—',
                         format_delta(v['CP_minus_ID']),'yes' if v['H1_pass'] else 'no'])
    lines.append(md_table(['Cell','Claimed matched Δ (p)','Matched Δ [CI], p','Matched ΔRMSE [CI], p','CP16 − ID Δ [CI], p','H1 pass'],rows))
    lines+=['','## C2. Distilled-Cartesian training','']
    rows=[]
    for s in SPLITS:
        for i,l in enumerate(SHORT):
            cell=f'{l} {s}'; v=c['C2'][cell]; m=MET[i]
            sec='RMSE' if m=='rho' else 'AUPRC'
            rows.append([cell,claimed_C[s][i],format_delta(v['metrics'][m]),sec+' '+format_delta(v['metrics'][sec]),
                         'yes' if v['H1_pass'] else 'no','yes' if v['degradation'] else 'no'])
    lines.append(md_table(['Cell','Claimed Δ','Independent primary Δ [CI], p','Other Δ [CI], p','H1 pass','Significant harm'],rows))
    lines+=['','## C3. Unseen synthons on the scaffold split','']
    vals=['n/a','766, +.0248, .0070','1238, +.0252, .0028','2016, +.0203, .0001']
    rows=[]
    for i,l in enumerate(SHORT):
        v=c['C3'][l+' scaffold']
        rows.append([l,vals[i],v['n'],format_delta(v['metrics'][MET[i]])])
    lines.append(md_table(['Endpoint','Claimed n, Δ, p','Independent n','Independent Δ [CI], p'],rows))
    lines+=['','## C4. Teacher fidelity and experimental accuracy','',
            'Claimed fidelity ranges were 0.822–0.903 on scaffold splits and 0.899–0.961 on random splits. The three large scaffold experimental gaps were claimed at p < 0.001.','']
    vals=['—','−.0875','−.1085','−.0262']
    rows=[]
    for s in SPLITS:
        for i,l in enumerate(SHORT):
            cell=l+' '+s; v=c['C4'][cell]; f=v['teacher_rho']
            rows.append([cell,f"{f['value']:.4f} [{f['CI'][0]:.4f}, {f['CI'][1]:.4f}]",f"{v['CP']:.4f}",f"{v['FullMol']:.4f}",
                         vals[i] if s=='scaffold' else '—',format_delta(v['gap'][MET[i]])])
    lines.append(md_table(['Cell','Teacher Spearman [CI]','CP16 experimental','Teacher experimental','Claimed gap','Independent gap [CI], p'],rows))
    lines+=['','## C5 and C6. Coverage and overlap','']
    rows=[]
    for i,l in enumerate(SHORT):
        h=c['C5'][l]; f=h['fraction']
        row=[l,['594/639','4027/4200','6400/9574','11528/12299'][i],f"{h['decomposable']}/{h['clean']} ({100*f:.3f}%)",
             ['3/119','40/806','42/1280','290/2306'][i]]
        for s in SPLITS:
            a=h[s]
            row.append(f"{a['both_seen']}/{a['split_sizes'][2]} ({100*a['both_seen']/a['split_sizes'][2]:.2f}%), {a['one_seen']}, {a['neither_seen']}, {a['both_any']}")
        rows.append(row)
    lines.append(md_table(['Endpoint','Claimed coverage','Independent coverage','Claimed scaffold both','Scaffold both, one, neither, both-any-slot','Random both, one, neither, both-any-slot'],rows))
    v=c['C6']
    alt=v['opposite_salt_tie']
    ac=alt['counts']
    lines+=['',f"With the opposite largest-fragment tie, the solubility scaffold sensitivity rerun gave {ac['decomp']}/{ac['clean']} coverage, experimental ρ={alt['CP']:.4f} for CP16 and {alt['FullMol']:.4f} for the teacher, and Δρ {format_delta(alt['gap'])}. These 18 extra fits are reported separately from the primary H1 counts.",f"C6 requires coverage >90% and a scaffold experimental Δρ >+0.020 at p <0.05. Independent coverage was {100*v['coverage']:.3f}%. The experimental Δρ was {format_delta(v['gap']['rho'])}.",'',
           '## CONTROLS:','',
           f"No. H1 decisions in src/summary.py use the matched comparator and both registered regression metrics. The ID result never supplies an H1 pass. Direct H1 passed {c['C1']['H1']['scaffold']}/4 scaffold and {c['C1']['H1']['random']}/4 random endpoints.",
           '',f"The paired comparisons use the same held-out rows, three seeds, descriptor normalization fitted on training occurrences and stopping rule for both neural heads. The 2×2 interaction check in audit/cp-control.json gives {cp['additive_interaction']:.2g} for the additive control and {cp['CP_interaction']:.3g} for CP16. The upstream masked-third-slot and product-over-four checks both give {cp['CP_formula_error']:.2g} maximum formula error and {cp['mask_invariance_error']:.2g} mask error. Parameter counts including the unused third heads are {cp['additive_parameters']:,} and {cp['CP_parameters']:,}, respectively. The matched comparison isolates the choice of head and combination as a package. Width and parameter count of the heads differ.",
           '',f"The 100-row upstream ridge control in src/verify_controls.py selected λ={ridge['lambda_selected']} with maximum prediction difference {ridge['max_absolute_error']:.2g}. The ID comparison changes both representation and architecture. Only the matched comparison decides H1. The upstream README reports >0.8 on 12/18 teacher outputs on another product set. That result supplies a reference for fidelity, not an experimental-label score.",
           '', 'Direct and distilled students use validation labels and validation teacher margins, respectively. Teacher early stopping itself uses experimental validation labels. Thus the distilled checkpoint depends indirectly on those labels. The neural worker receives no experimental test labels. The split and evaluation programs can read the raw targets. These are code-level controls within a shared filesystem.',
           '', 'The independently replayed synthetic stream checks ordered dummy identities against real training-slot membership, observed ordered type pairs, unique products, and all original canonical SMILES. The table also checks stronger forms of molecular similarity. Scaffold sharing and capped-feature collisions can make the augmented test prediction problem easier. They do not violate the sealed exact-product exclusion.','']
    rows=[]
    for key,l in zip(KEYS,SHORT):
        for s in SPLITS:
            prefix=f'audit/{key}-{s}'
            a=read(prefix+'-audit.json'); z=leak[key+' '+s]; p=pair[f'{key}-{s}-inputs']
            rows.append([l+' '+s,a['synthetic'],a['exact_overlap'],sum(z['recanonicalized_overlap_'+j] for j in ('train','val','test')),
                         a['stereo_agnostic_holdout_hits'],str(z['unique_test_scaffolds_in_synthetic'])+'/'+str(z['test_scaffolds']),p['test_cap_tuple_seen_in_synthetic']])
    lines.append(md_table(['Cell','Synthetic products','Exact overlap','Reparsed overlap','Val/test connectivity hits¹','Test scaffolds represented','Test capped pairs in synthetic²'],rows))
    lines+=['','¹ Count of synthetic products matching val/test after removing stereo and isotope distinctions in non-isomeric SMILES. ² Count of test molecules with a matching ordered capped pair. Source molecules and chemical products can differ. num_threads=4 for each numerical worker. LightGBM and Torch ran in separate processes.',
           '','## CONTRADICTING:','',
           'No. src/harvest.py checks all 144 primary fit files, including significant direct gains that contradict C1 and the solubility loss against the teacher that contradicts C6. All 8 cells, 3 strata, and 3 seeds are present in audit/*-stats.json. Ineligible strata retain their molecule counts. The following ranges show the three single-initialization CP16 minus matched-control differences. The sealed decision uses the three-seed ensemble.','']
    rows=[]
    for i,(key,l) in enumerate(zip(KEYS,SHORT)):
        for s in SPLITS:
            k=l+' '+s
            x=c['C1'][k]['seed_deltas'][MET[i]]
            y=c['C2'][k]['seed_deltas'][MET[i]]
            d=read(f'audit/{key}-{s}-stats.json')
            rows.append([k,', '.join(f'{z:+.4f}' for z in x),', '.join(f'{z:+.4f}' for z in y),
                         f"{d['both_seen']['n']} ({d['both_seen'].get('status','scored')})",
                         f"{d['all']['points']['teacher'][MET[i]]['value']:.4f} / {d['clean_teacher'][MET[i]]:.4f}"])
    lines.append(md_table(['Cell','Direct Δ, seeds 42/43/44','Cartesian Δ, seeds 42/43/44','Both seen','Decomp / all-clean teacher scores³'],rows))
    lines+=['','³ All-clean and decomposable populations were independently split. Differences mix population and split effects. See audit/*-stats.json for AP, RMSE, MAE, distilled-train controls, fidelity, intervals and seed SDs. Bootstrap intervals and permutation p-values condition on one split and fixed trained ensembles. Molecules sharing a scaffold are resampled individually under the sealed rule. The p-values are unadjusted for multiple comparisons.',
            '','## LABELS:','',
            'No. src/crosscheck.py independently re-read each Drug and numeric Y, regrouped standardized molecules, recomputed means or conflict exclusions, and verified every surviving target. Source assay annotations and physical measurements have no independent assay replicate in the allowed inputs. The check establishes agreement with the tabulated targets. Assay units and endpoint names come from the seal.','']
    rows=[]
    for key,l in zip(KEYS,SHORT):
        d=labels[key]; r=read('audit/'+key+'.json')['stats']
        rows.append([l,d['raw'],d['raw_value_counts'] or d['raw_y_range'],d['invalid'],r.get('merged',0),r.get('conflict_keys',0),
                     d['verified_clean_labels'],f"{d['max_label_abs_error']:.2g}"])
    lines.append(md_table(['Endpoint','Raw rows','Label counts or range','Invalid','Redundant valid rows merged','Conflicting keys dropped','Verified clean labels','Maximum absolute discrepancy'],rows))
    lines+=['','## Tie-breaking and reproducibility','',
            'For all equal-balance candidates, the verifier reversed atom order and reran cut enumeration. It also replaced the sealed lexicographically first equal-balance cut with the last as a sensitivity check. This changes inputs while holding the test molecules fixed. The primary fits all retain the sealed winner.','']
    rows=[]
    for key,l in zip(KEYS,SHORT):
        r=read('audit/'+key+'.json')['stats']; z=labels[key]
        rows.append([l,r['balanced_ties'],z['atom_reversal']['reordered_winner_changes'],
                     z['reverse_tie_both_seen']['scaffold'],z['reverse_tie_both_seen']['random'],
                     r['roundtrip_mismatch'],z['roundtrip'].get('same_nonisomeric',0)])
    lines.append(md_table(['Endpoint','Distinct tied cuts (molecules)','Winner changes after atom reversal','Reverse-tie both seen, scaffold','Reverse-tie both seen, random','Original cut/join string mismatches','Of which same non-isomeric graph'],rows))
    alt_rows=[]
    for key,l in zip(KEYS,SHORT):
        z=labels[key]
        alt_rows.append([l,z['literal_single_fragment_clean'],z['single_fragment_direct_smiles_changes'],
                         f"{z['decomp_lex_first_largest_tie']}/{z['clean_lex_first_largest_tie']}",
                         c['C5'][l]['opposite_salt_tie']['scaffold']['both'],
                         f"{z['random_raw_order_test_intersection']}/{c['C5'][l]['random']['split_sizes'][2]}"])
    lines+=['','Two further checks hold the raw files fixed. The first rebuilds single-component SMILES without fragment extraction and reverses the lexical tie among equal-sized salt fragments in a separate variant. The second changes only the input ordering before the seeded random split.','',
            md_table(['Endpoint','Literal single-component clean count','Single-component strings changed','Opposite salt tie, decomp/clean','Opposite salt tie, scaffold both','Random test overlap, raw vs canonical order'],alt_rows)]
    lines+=['','All 41 initial cut/join string discrepancies on lipophilicity resolved to the same isomeric canonical SMILES on reparsing. The extra canonicalization check on accepted synthetic products is reported above.','',
            'The seal fixes seeds but leaves row order, sampling enumeration order, and some implementation conventions unspecified. The rebuild sorts canonical molecules and dummy identities, applies greedy scaffold packing, uses the three stated seeds literally, and averages raw scores. Upstream train.py adds rank to its CLI seed. Its defaults, original teacher losses and connector vocabulary differ from the sealed experimental adaptations. None of these ambiguities was tuned using reference results.',
            '',f"All {labels['statistics']['metric_cases']} scalar comparisons for ties against SciPy/scikit-learn or direct arithmetic passed (maximum error {labels['statistics']['max_abs_error']:.2g}). All five metric-specific permutation p-values matched the exhaustive tiny-example swap lookup, and the paired RMSE bootstrap interval matched the scalar reference. The hash and version receipts are in audit/protocol.sha256, audit/environment.txt and audit/crosscheck.json. Sampling-related outputs are rerun evidence. They cannot establish what an inaccessible implementation actually did.",
            '','Methods and sources are in SEALED.md, DEVIATIONS.md, PRIOR_ART.md, src/, and the pinned public repository. REPORT.md gives reproduction commands.']
    Path('VERDICT.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':
    main()

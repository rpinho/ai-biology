import pathlib,hashlib,json,csv
r=pathlib.Path('/workspace/ref_manuel_M011')
def digest(p,alg='sha256'):return hashlib.new(alg,p.read_bytes()).hexdigest()
def table(p):
 with p.open() as f:
  lines=list(csv.reader(f,delimiter='\t'))
 return lines[0],{tuple(x[:4]):x[4:] for x in lines[1:]}
p=r/'pipeline_original/output/EX_clusters.tab'
assert p.exists()
assert digest(p,'md5')=='02479360ed2b8d659612fc60477ad355'
assert p.read_bytes()==(r/'rerun/original/EX_clusters.tab').read_bytes()
# The fresh pipeline graph must match the alleged pre-diagnostic graph,
# not just yield a similar final output.
graphs=[]
for g in (r/'pipeline_original/work').rglob('PART_01-cluster_input.tab'):
 graphs.append({'path':str(g.relative_to(r)),'sha256':digest(g)})
assert graphs and all(g['sha256']==digest(r/'claim/edges.tsv') for g in graphs)
assert (r/'claim/genes.tsv').read_bytes()==(r/'ExOrthist-2.0.0/test/hg38_mm10_bosTau9.tab').read_bytes()
h1,t1=table(p);h2,t2=table(r/'rerun/corrected/EX_clusters.tab')
assert h1==h2 and t1.keys()==t2.keys()
changed=[{'key':k,'old':t1[k],'new':t2[k]} for k in sorted(t1) if t1[k]!=t2[k]]
assert len(changed)==18
seal=json.loads((r/'claim/seal.json').read_text())
seal_checks={}
for key,sha in seal['files'].items():
 pairs={'exorthist_consistency/results/author_D2.R':r/'ExOrthist-2.0.0/bin/D2_cluster_EXs.R','exorthist_consistency/results/gene_input.tsv':r/'claim/genes.tsv','exorthist_consistency/results/official_EX_clusters.tab':p,'exorthist_consistency/results/baseline_graph/PART_01-cluster_input.tab':r/'claim/edges.tsv','exorthist_consistency/results/baseline_graph/EXs_PART_01-cluster_input.tab':r/'rerun/original/EXs_PART_01.tsv'}
 if key in pairs:seal_checks[key]=digest(pairs[key])==sha
result={'fresh_pipeline_golden_md5':digest(p,'md5'),'fresh_pipeline_sha256':digest(p),'fresh_graphs':graphs,'fresh_graph_matches_claim':True,'original_gene_input_byte_identical':True,'final_table_rows':len(t1),'same_final_row_keys':True,'changed_score_cells':len(changed),'corrected_table_sha256':digest(r/'rerun/corrected/EX_clusters.tab'),'claim_seal_material_checks':seal_checks,'seal_timestamp_authenticated':False,'holdout':'none; reused public release test, deterministic specification audit','changed_rows':changed}
(r/'pipeline_evidence.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='changed_rows'},indent=2))

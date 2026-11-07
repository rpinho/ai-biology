"""Referee arithmetic derived from Genome Biology 2021 Methods, not claimant code.

The clustering output supplies a partition only. Rebuild all graph counts from
ordered edges, ignoring supplied reciprocal flags except as a separate check.
Evaluate both literal paper original-gene denominator and edge-observed control.
"""
import argparse, collections, csv, hashlib, json, pathlib
from fractions import Fraction

p=argparse.ArgumentParser()
p.add_argument('--root',type=pathlib.Path,default=pathlib.Path('/workspace/ref_manuel_M011'))
p.add_argument('--edges',default='claim/edges.tsv')
p.add_argument('--original',default='claim/original_scores.tsv')
p.add_argument('--corrected',default='claim/corrected_scores.tsv')
p.add_argument('--out',default='arithmetic.json')
a=p.parse_args(); root=a.root

def rows(name):
 with (root/name).open() as f: return list(csv.reader(f,delimiter='\t'))
def ident(v):
 fields=v.split('|'); assert len(fields)==4, v
 return fields

def table(name):
 rs=rows(name); assert all(len(r)==8 for r in rs)
 d={r[0]:r[1:] for r in rs}; assert len(d)==len(rs)
 return d

edge_rows=rows(a.edges); assert all(len(r)==4 for r in edge_rows)
edges=collections.Counter((r[1],r[2]) for r in edge_rows)
vertices=set(v for pair in edges for v in pair)
genes=collections.defaultdict(set); observed=collections.defaultdict(set)
for fam,sp,gene,*_ in rows('claim/genes.tsv'): genes[fam].add((sp,gene))
for v in vertices:
 fam,gene,loc,sp=ident(v); observed[fam].add((sp,gene)); assert (sp,gene) in genes[fam]
assert all(ident(x)[0]==ident(y)[0] and ident(x)[-1]!=ident(y)[-1] for x,y in edges)
assert all(fam==ident(x)[0]==ident(y)[0] for fam,x,y,flag in edge_rows)
flag_errors=[r for r in edge_rows if (r[3]=='TRUE')!=((r[2],r[1]) in edges)]
# Best-match consistency control: each query maps to at most one exon per target gene.
query_targets=collections.defaultdict(set)
for x,y in edges: query_targets[(x,ident(y)[1])].add(y)
nonunique_best=sum(len(v)>1 for v in query_targets.values())
orig=table(a.original); fixed=table(a.corrected)
assert set(orig)==set(fixed)==vertices
clusters=collections.defaultdict(set)
for v,r in orig.items(): clusters[(ident(v)[0],r[0])].add(v)
assert all(orig[v][0]==fixed[v][0] for v in vertices)
assert all(orig[v][:-1]==fixed[v][:-1] for v in vertices)
inc=collections.defaultdict(collections.Counter); out=collections.defaultdict(collections.Counter)
for (x,y),n in edges.items(): out[x][y]=n; inc[y][x]=n
cert=[]; int_errors=[]
for v in sorted(vertices):
 fam,gene,loc,sp=ident(v); c=clusters[(fam,orig[v][0])]
 same_sp={u for u in c if ident(u)[-1]==sp}
 n_species_genes=len({ident(u)[1] for u in same_sp})
 ni=sum(n for u,n in inc[v].items() if u in c)
 no=sum(n for u,n in out[v].items() if u in c)
 nr=len(set(inc[v])&set(out[v])&c)
 integer_expected=[no,ni,len(same_sp),len(c),nr]
 if list(map(int,orig[v][1:-1]))!=integer_expected: int_errors.append(v)
 numerator=ni+no+nr
 den_paper=2*(len(c)-len(same_sp))+len(genes[fam])-n_species_genes
 den_observed=2*(len(c)-len(same_sp))+len(observed[fam])-n_species_genes
 den_trivial=2*(len(c)-len(same_sp))+len(observed[fam])-1
 assert min(den_paper,den_observed,den_trivial)>0
 scores={'paper':Fraction(numerator,den_paper),'observed':Fraction(numerator,den_observed),'trivial_one_gene':Fraction(numerator,den_trivial)}
 rec={'exon':v,'cluster':orig[v][0], 'out':no,'in':ni,'reciprocal_neighbors':nr,'exons':len(c),'same_species_exons':len(same_sp),'same_species_genes':n_species_genes,'original_genes':len(genes[fam]),'observed_genes':len(observed[fam]),'numerator':numerator,'denominator_paper':den_paper,'original_reported':orig[v][-1],'corrected_reported':fixed[v][-1]}
 for key,q in scores.items():
  rec[key+'_fraction']=str(q)
  for which,t in [('original',orig),('corrected',fixed)]: rec[which+'_matches_'+key]=abs(Fraction(t[v][-1])-q)<=Fraction(1,200)
 cert.append(rec)
summary={'edge_rows':len(edge_rows),'distinct_directed_edges':len(edges),'vertices':len(vertices),'clusters':len(clusters),'gene_families':len(genes),'bad_reciprocal_flags':len(flag_errors),'nonunique_best_query_target_gene':nonunique_best,'integer_errors':len(int_errors),'changed_scores':sum(orig[v][-1]!=fixed[v][-1] for v in vertices),'multi_same_species_gene_rows':sum(r['same_species_genes']>1 for r in cert),'same_species_one_gene_unchanged':sum(r['same_species_genes']==1 and r['original_reported']==r['corrected_reported'] for r in cert),'original_gene_vs_observed_mismatch_rows':sum(r['original_genes']!=r['observed_genes'] for r in cert)}
for which in ['original','corrected']:
 for model in ['paper','observed','trivial_one_gene']: summary[which+'_mismatch_'+model]=sum(not r[which+'_matches_'+model] for r in cert)
summary['witness']=[r for r in cert if r['exon']=='GF_002754|ENSG00000160218|chr21:44098357-44098534:+|hg38'][0]
summary['hashes']={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in [a.edges,a.original,a.corrected,'claim/genes.tsv']}
(root/a.out).write_text(json.dumps({'summary':summary,'integer_error_exons':int_errors,'rows':cert},indent=2)+'\n')
print(json.dumps(summary,indent=2))

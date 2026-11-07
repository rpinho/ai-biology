"""Independent native replays and bounded row-order controls."""
import pathlib,csv,subprocess,hashlib,json,random,concurrent.futures
r=pathlib.Path('/workspace/ref_manuel_M011'); source=r/'ExOrthist-2.0.0/bin/D2_cluster_EXs.R'; R=r/'env/bin/Rscript'
original=source.read_text()
old1='my_species = sub("\\\\|", ";", my_exon)'
new1='my_species = sub(".*\\\\|", "", my_exon)'
old2='all_exons_in_cluster[sub("\\\\|", ";", all_exons_in_cluster) == my_species]'
new2='all_exons_in_cluster[sub(".*\\\\|", "", all_exons_in_cluster) == my_species]'
assert original.count(old1)==1 and original.count(old2)==1
patched=original.replace(old1,new1).replace(old2,new2)
(r/'referee_species_patch.R').write_text(patched)
assert patched==(r/'claim/corrected_species_D2.R').read_text()

def data(path):
 with path.open() as f:return list(csv.reader(f,delimiter='\t'))
def canon(path):
 d={}
 for row in data(path):
  k=(row[0].split('|')[0],row[1]);d.setdefault(k,[]).append(row[0])
 return sorted(sorted(v) for v in d.values())

def run(folder,edges,script):
 folder.mkdir(parents=True,exist_ok=True)
 assert not (folder/'scores.tsv').exists()
 with (folder/'R.log').open('w') as f: subprocess.run([str(R),'--vanilla',str(script),str(edges),str(folder/'scores.tsv'),str(folder/'unclustered.tsv')],stdout=f,stderr=subprocess.STDOUT,check=True)
 return folder/'scores.tsv'

base=r/'adversarial';base.mkdir(exist_ok=True)
rows=data(r/'claim/edges.tsv'); partition=canon(r/'rerun/original/EXs_PART_01.tsv')
witness='GF_002754|ENSG00000160218|chr21:44098357-44098534:+|hg38'
cluster=next(c for c in partition if witness in c)
mini=[row for row in rows if row[1] in cluster and row[2] in cluster]
assert len(cluster)==4 and len(mini)==8
(base/'minimal').mkdir(exist_ok=True)
with (base/'minimal/edges.tsv').open('w') as f: csv.writer(f,delimiter='\t',lineterminator='\n').writerows(mini)
for tag,script in [('original',source),('corrected',r/'referee_species_patch.R')]:run(base/'minimal'/tag,base/'minimal/edges.tsv',script)
subprocess.run(['python3',str(r/'independent_audit.py'),'--edges','adversarial/minimal/edges.tsv','--original','adversarial/minimal/original/scores.tsv','--corrected','adversarial/minimal/corrected/scores.tsv','--out','adversarial/minimal/arithmetic.json'],check=True,stdout=subprocess.DEVNULL)

def shuffle(seed):
 folder=base/f'seed_{seed:02d}';folder.mkdir(exist_ok=True)
 shuffled=rows.copy();random.Random(seed).shuffle(shuffled)
 with (folder/'edges.tsv').open('w') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerows(shuffled)
 scores=run(folder,folder/'edges.tsv',source)
 return {'seed':seed,'same_partition':canon(scores)==partition,'unclustered_bytes':(folder/'unclustered.tsv').stat().st_size,'same_exon_scores':{x[0]:x[2:] for x in data(scores)}=={x[0]:x[2:] for x in data(r/'rerun/original/EXs_PART_01.tsv')}}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: controls=list(ex.map(shuffle,range(1,33)))
result={'referee_patch_sha256':hashlib.sha256(patched.encode()).hexdigest(),'patch_matches_claim':True,'minimal_vertices':len(cluster),'minimal_directed_edges':len(mini),'shuffle_controls':controls}
(base/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)

#!/usr/bin/env python3
"""Run supplied tiny fixtures against a caller-selected repository. Standard library only."""
import csv,datetime,json,math,os,re,shutil,subprocess,sys,tempfile
from collections import Counter,defaultdict
from pathlib import Path
BUG=sys.argv[1]; REPO=Path(sys.argv[2]).resolve(); CASE=Path(__file__).resolve().parents[1]/BUG
(CASE/'runs').mkdir(exist_ok=True)
WORK=Path(tempfile.mkdtemp(prefix='run-',dir=CASE/'runs'))
shutil.copytree(CASE/'inputs',WORK/'inputs'); I=WORK/'inputs'; B=REPO/'bin'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='1')
ENV['PATH']=str(B)+os.pathsep+ENV['PATH']
if BUG in ['B1-01','B1-02','R6-01','R6-02']: ENV['PATH']=str(Path(__file__).parent/'stubs')+os.pathsep+ENV['PATH']
count=0

def run(args,cwd=None,env=None):
    global count
    count+=1; cwd=Path(cwd or WORK); cwd.mkdir(parents=True,exist_ok=True); args=list(map(str,args))
    p=subprocess.run(args,cwd=cwd,env=dict(ENV,**(env or {})),capture_output=True,text=True,timeout=120)
    log=WORK/f'command-{count:02}'
    log.with_suffix('.json').write_text(json.dumps({'argv':args,'cwd':str(cwd),'exit':p.returncode},indent=2)+'\n')
    log.with_suffix('.stdout').write_text(p.stdout); log.with_suffix('.stderr').write_text(p.stderr)
    return p

def text(p): return p.read_text() if p.exists() else ''
def rows(p): return [l.split('\t') for l in text(p).splitlines()]
def table(p): return list(csv.DictReader(text(p).splitlines(),delimiter='\t'))
def require(p):
    if p.returncode: raise RuntimeError(p.stderr or p.stdout)
def fasta(p):
    d={}; key=None
    for line in text(p).splitlines():
        if line.startswith('>'): key=line[1:].split()[0]; d[key]=''
        elif key: d[key]+=line
    return d

def a1(v):
    d=I/v
    p=run(['perl',B/'A1_generate_annotations.pl','-GTF',d/'Tree_annot.gtf','-G',d/'Tree_gDNA.fasta','-sp','Tree','-keep_files'],d)
    require(p); return d/'Tree'
def d31(groups,pairs,label,seed=1):
    d=WORK/label; out=d/'genes.tsv'
    p=run([sys.executable,B/'D3.1_recluster_genes_by_species_pair.py','-og',groups,'-op',pairs,'-s1','A','-s2','B','-out',out],d,{'PYTHONHASHSEED':str(seed)})
    return p,rows(out)
def d32(flags=('-s1','-s2')):
    out=WORK/'out.tsv'
    p=run([sys.executable,B/'D3.2_recluster_EXs_by_species_pair.py','-ep',I/'pairs.tsv','-rg',I/'genes.tsv','-ec',I/'exons.tsv',flags[0],'A',flags[1],'B','-out',out])
    return p,rows(out)[1:]
def c2(d,ident,size):
    p=run(['perl',B/'C2_filter_and_select_best_EX_matches_by_targetgene.pl','-b',d/'scores.tsv','-sps','A,B','-int','2','-id',ident,'-max_size',size],d)
    require(p); return max(0,len(rows(d/'filtered_best_scored_EX_matches_by_targetgene.tab'))-1)
def diff_tab(name,paired=False,chunk=None,pdf=False):
    d=WORK/(name+('-paired' if paired else '-unpaired')+('-pdf' if pdf else '')); d.mkdir()
    shutil.copy2(I/(name+'.tab'),d/'input.tab')
    args=['perl',REPO/'vast-tools','diff','-o',d,'-i','input.tab','-a','A1,A2' if BUG=='VT-003' else 'A','-b','B1,B2' if BUG=='VT-003' else 'B','-d','result']
    if paired: args+=['--paired']
    if not pdf: args+=['--noPDF']
    if chunk: args+=['-n',str(chunk)]
    p=run(args,d); return p,rows(d/'result.tab')

observed={}; correct=False
if BUG.startswith('A1-'):
    variants={'A1-01':['normal','cdsonly','exonsfirst'],'A1-02':['normal'],'A1-03':['normal','attributes'],'A1-04':['normal','masked'],'A1-05':['normal','ascending'],'A1-07':['normal','shared']}[BUG]
    oak='M'+'A'*9+'E'*11+'F'*9; elm='M'+'K'*9+'D'*10+'W'*10
    for v in variants:
        d=a1(v); ex=rows(d/'Tree_protein_ids_exons_pos.txt'); seq=fasta(d/'Tree.exint')
        if BUG=='A1-01': observed[v]={'ids':sorted(text(d/'Tree_annot_exons_prot_ids.txt').splitlines()),'exon_rows':len(ex)}
        elif BUG=='A1-02': observed[v]={r[0]+':'+r[1]:r[2] for r in ex}
        elif BUG=='A1-03': observed[v]={'ids':sorted(seq),'ref_genes':sorted(r[0] for r in rows(d/'Tree_ref_proteins.txt'))}
        elif BUG=='A1-04': observed[v]=seq
        elif BUG=='A1-05': observed[v]={'sequence':seq.get('ELMP0001|elm'),'exons':[[r[1],r[4]] for r in ex if r[0]=='ELMP0001|elm']}
        else: observed[v]={'oak_sequence':seq.get('OAKP0001|oak'),'oak_exons':sum(r[0]=='OAKP0001|oak' for r in ex)}
    if BUG=='A1-01': correct=all(x['ids']==['ELMP0001|elm','OAKP0001|oak'] and x['exon_rows']==6 for x in observed.values())
    elif BUG=='A1-02':
        expected={}
        for prot,lens in [('OAKP0001|oak',[31,32,27]),('ELMP0001|elm',[30,30,30])]:
            start=0
            for n,length in enumerate(lens,1): expected[prot+':exon_'+str(n)]=f'{start//3+1}-{math.ceil((start+length)/3)}'; start+=length
        correct={k:v.split('-')[-1] for k,v in observed['normal'].items()}=={k:v.split('-')[-1] for k,v in expected.items()}
    elif BUG=='A1-03': correct=all(x['ids']==['ELMP0001|elm','OAKP0001|oak'] and x['ref_genes']==['elm','oak'] for x in observed.values())
    elif BUG=='A1-04': correct=all(x=={'OAKP0001|oak':oak,'ELMP0001|elm':elm} for x in observed.values())
    elif BUG=='A1-05': correct=all(x['sequence']==elm and x['exons']==[['exon_1','701-730'],['exon_2','601-630'],['exon_3','501-530']] for x in observed.values())
    else: correct=all(x=={'oak_sequence':oak,'oak_exons':3} for x in observed.values())
elif BUG=='A3-01':
    for v,n,total in [('default_1000',1000,1001),('family_order',1,3)]:
        d=I/v; p=run(['perl',B/'A2_split_clusters_by_species_pairs.pl','-f','clusters.tsv'],d); require(p)
        p=run(['perl',B/'A3_split_clusters_in_chunks.pl','--gene_cluster','Fern-Moss.cls.tab','--sp1','Fern','--sp2','Moss','--N_split',str(n)],d); require(p)
        locations=defaultdict(set)
        for f in (d/'Fern_Moss').glob('*part*'):
            for row in rows(f): locations[row[0]].add(f.name)
        observed[v]={'families':len(locations),'split_families':sum(len(x)>1 for x in locations.values()),'expected_families':total}
    correct=all(x['split_families']==0 and x['families']==x['expected_families'] for x in observed.values())
elif BUG in ['B1-01','B1-02']:
    for v in (['short','control'] if BUG=='B1-01' else ['reused','control']):
        d=I/v; args=['perl',B/'B1_parse_IPA_prot_aln.pl','Fern','Moss','clusters.tsv']
        for suffix in ['_annot_exons_prot_ids.txt','_protein_ids_exons_pos.txt','_protein_ids_intron_pos_CDS.txt','.exint']: args +=[f'{sp}/{sp}{suffix}' for sp in ['Fern','Moss']]
        args+=['1',REPO/'files/blosum62.txt','aligned','0.25','1']; p=run(args,d); require(p)
        if BUG=='B1-01': observed[v]={'intron_matches':len(rows(d/'aligned/INT_aln_features_Fern_Moss_part_1.txt'))-1}
        else: observed[v]={'pairs':sorted([r[0],r[2],r[3]] for r in rows(d/'aligned/PROT_aln_features_Fern_Moss_part_1.txt')[1:] if r[-2]=='Fern')}
    if BUG=='B1-01': correct=all(x['intron_matches']==4 for x in observed.values())
    else: correct=observed['reused']['pairs']==[['familyAlpha','FERNP0001|seed','MOSSP0001|spore'],['familyBeta','FERNP0002|spore','MOSSP0002|seed']] and len(observed['control']['pairs'])==2
elif BUG=='B2-01':
    for v in ['padded','control','na_word']:
        d=I/v; f=next(d.glob('*to_split*')); p=run([sys.executable,B/'B2_split_EX_pairs_to_realign.py','-i',f,'-n','1'],d); require(p)
        observed[v]=rows(next(d.glob('*to_realign*')))[1][0]
    correct=observed==dict(padded='007300',control='fam7300',na_word='null')
elif BUG=='B4-01':
    p=run(['perl',B/'B4_merge_PROT_EX_INT_aln_info.pl','merge'],I); require(p)
    observed={k:len(rows(I/'merge'/f'all_{k}_aln_features.txt'))-1 for k in ['PROT','EX','INT']}; correct=all(x==4 for x in observed.values())
elif BUG=='S1-01':
    for v,cid in [('numeric','42'),('control','fam42')]:
        d=I/v; p=run([sys.executable,B/'subset_inputs.py','-a','Fern.gtf','-o','overlap.tsv','-r','ref.tsv','-c','clusters.tsv','-g',cid,'-s','Fern'],d); require(p)
        observed[v]={f.name:len(rows(f)) for f in d.glob('Fern_subsetted*')}
    correct=all(sorted(x.values())==[1,2,2] for x in observed.values())
elif BUG=='A0-01':
    p=run(['perl','-e',r'BEGIN { *CORE::GLOBAL::localtime = sub { (0,0,12,6,10,126,5,309,0) } } my $script=shift; do $script; die $@ if $@;',B/'A0_check_input.pl','-e','evodists.txt','-g','.','-gs','_annot.gtf','-f','.','-fs','_gDNA.fasta','-c','clusters.tsv'],I); require(p)
    dates=re.findall(r'\d{4}-\d{2}-\d{2}',p.stdout); actual='2026-11-06'
    observed={'printed_date':dates[0] if dates else None,'calendar_date':actual}; correct=bool(dates and dates[0]==actual)
elif BUG in ['R6-01','R6-02']:
    for v in (['plain','dot_slash','dotted_dir'] if BUG=='R6-01' else ['plain','description']):
        d=I/v; q={'dot_slash':'./Fern.gtf','dotted_dir':'data.v1/Fern.gtf'}.get(v,'Fern.gtf')
        args=['perl',B/'get_liftovers.pl','-annot_sp1',q,'-annot_sp2','Moss.gtf','-chain_file','identity.chain','-gene_clusters','clusters.tsv']
        if BUG=='R6-02': args+=['-canonical_ss']
        p=run(args,d); observed[v]={'exit':p.returncode,'pairs':sum(len(rows(f)) for f in d.glob('Liftover*.tab'))}
    correct=all(x['exit']==0 and x['pairs']==1 for x in observed.values())
elif BUG=='R5-01':
    for v in ['collision','control']:
        d=I/v; p=run(['perl',B/'retrieve_IPA_aln.pl','-g1','seed','-g2','spore','-ex1','chr1:101-160','-ex2','chr2:201-260','-sp1','Fern','-sp2','Moss','-main_folder','main'],d); require(p)
        isolated=p.stdout.split('Isolated')[-1]
        observed[v]={sp:bool(re.search(r'(?m)^'+sp+r'\t[^\t\n]+',isolated)) for sp in ['Fern','Moss']}
    correct=all(all(x.values()) for x in observed.values())
elif BUG in ['B16','B03','B15']:
    if BUG=='B15':
        for name in ['groups.tsv','pairs.tsv']:
            f=I/name; sentinel='Unused\tC\tunusedC\tsymbol\nUnused\tD\tunusedD\tsymbol\n' if name=='groups.tsv' else 'unusedC\tunusedD\n'; f.write_text(sentinel+'\n'.join(f.read_text().splitlines()[1:])+'\n')
        for seed in [1,2,3,4,5,6]:
            p,rr=d31(I/'groups.tsv',I/'pairs.tsv',f'seed-{seed}',seed); require(p); observed[str(seed)]=sorted([r[2],r[0]] for r in rr)
        correct=len({json.dumps(x) for x in observed.values()})==1 and len(observed['1'])==4
    elif BUG=='B16':
        f=I/'pairs.tsv'; f.write_text('\n'.join(f.read_text().splitlines()[1:])+'\n')
        p,rr=d31(I/'documented.tsv',f,'documented'); observed={'exit':p.returncode,'genes':sorted(r[2] for r in rr)}; correct=p.returncode==0 and len(rr)==4
    else:
        p,rr=d31(I/'groups.tsv',I/'pairs.tsv','headerless'); require(p); observed={'genes':sorted(r[2] for r in rr),'components':len(set(r[0] for r in rr))}; correct=len(rr)==6 and observed['components']==3
elif BUG in ['B02','B04','B13']:
    if BUG=='B02':
        module=text(REPO/'modules/local/exorthist/recluster_exs.nf'); flags=re.findall(r'^\s+(-(?:sp1|sp2|s1|s2))\s',module,re.M); p,rr=d32(flags)
        observed={'flags':flags,'exit':p.returncode,'exon_rows':len(rr)}; correct=p.returncode==0 and len(rr)==2
    else:
        p,rr=d32(); require(p); observed={'rows':sorted(rr)}; correct=len(rr)==2 and all(r[0]=='Family.01.003' for r in rr)
elif BUG in ['B05','B06','B14']:
    if BUG=='B14':
        for v in ['plain','hash']:
            d=WORK/v; p=run([os.environ.get('RSCRIPT','Rscript'),B/'D2_cluster_EXs.R',I/(v+'.tsv'),'clusters.tsv','unclustered.tsv'],d)
            observed[v]={'exit':p.returncode,'exon_rows':len(rows(d/'clusters.tsv'))}
        correct=all(x['exit']==0 and x['exon_rows']==3 for x in observed.values())
    else:
        p=run(['perl',B/'D1_format_EX_clusters_input.pl',I/'groups.tsv',I/'pairs.tsv','500']); require(p)
        p=run([os.environ.get('RSCRIPT','Rscript'),B/'D2_cluster_EXs.R',WORK/'PART_01-cluster_input.tab','clusters.tsv','unclustered.tsv'])
        rr=rows(WORK/'clusters.tsv'); sizes=Counter(r[1] for r in rr)
        observed={'exit':p.returncode,'error_vector_condition':'the condition has length > 1' in p.stderr,'rows':rr}
        n=len(rows(I/'groups.tsv')); counts_ok=all(int(r[5])==sizes[r[1]] for r in rr)
        scores_ok=all(abs(float(r[7])-round((int(r[2])+int(r[3])+int(r[6]))/(2*(sizes[r[1]]-1)+(n-1)),2))<0.001 for r in rr)
        correct=p.returncode==0 and bool(rr) and (BUG=='B05' or counts_ok and scores_ok)
elif BUG=='B01':
    p=run(['perl',B/'C3_count_matches_by_EX.pl',I/'pairs.tsv','counts.tsv']); require(p)
    p=run(['perl',B/'C4_get_overlapping_EXs.pl','-i','counts.tsv','-o','overlaps.tsv']); require(p)
    p=run(['perl',B/'C5_collapse_overlapping_matches.pl','overlaps.tsv',I/'pairs.tsv','collapsed.tsv']); require(p)
    rr=rows(WORK/'collapsed.tsv'); observed={'pairs':len(rr),'coordinates':[r[1] for r in rr]}
    correct=len(rr)==2 and all(r[1]=='chrQ:980-1120:+' for r in rr)
elif BUG in ['B07','B08']:
    observed['problem_pairs']=c2(I,'0' if BUG=='B07' else '0.1','0' if BUG=='B07' else '0.8')
    if BUG=='B08':
        f=I/'scores.tsv'; f.write_text(f.read_text().replace('contig-7','contig7')); observed['control_pairs']=c2(I,'0.1','0.8')
    else: observed['control_pairs']=c2(I,'0.000001','0.000001')
    correct=all(x==1 for x in observed.values())
elif BUG in ['B09','B17']:
    for v in (['6-1','3-4','1-1'] if BUG=='B09' else ['zero-main','named-main']):
        d=I/v; p=run(['perl',B/'get_cluster_stats.pl','-main_output',d,'-gene_clusters',d/'genes.tsv'],WORK/v)
        observed[v]={'exit':p.returncode,'summary':p.stdout.split('Exon OG type')[-1].strip()}
    if BUG=='B09': correct=all(x['exit']==0 for x in observed.values()) and all(re.search(r'>=3 exons/species\s+1\b',observed[v]['summary']) and re.search(r'>=4 exons/species\s+1\b',observed[v]['summary']) and re.search(r'Other OGs\s+0\b',observed[v]['summary']) for v in ['6-1','3-4'])
    else: correct=observed['zero-main']['exit']==0 and observed['zero-main']['summary']==observed['named-main']['summary']
elif BUG=='B10':
    p=run([sys.executable,B/'generate_exint_plotter_input.py','-a',I/'annotation.gtf','-o',I/'overlap.tsv','-c',I/'groups.tsv','-e',I/'exons.tsv','-r',I/'ref.tsv','-s','A','-out','plot.tsv']); require(p)
    observed={'exons':[[r['ExonID'],r['UpPhase'],r['DownPhase'],r['FakeStart']] for r in table(WORK/'plot.tsv')]}
    correct=observed['exons']==[['chrQ:970-1029','0','1','0'],['chrQ:1120-1179','1','2','30'],['chrQ:1320-1379','2','last','60']]
elif BUG=='B11':
    for v,extra in [('requested',['-min_dPSI','40']),('default',[])]:
        p=run(['perl',B/'compare_exon_sets.pl','-sp1','A','-sp2','B','-gene_clusters',I/'groups.tsv','-exon_clusters',I/'exons.tsv','-exon_list_sp1',I/'query.tsv','-dPSI_info','dPSI','-no_plot']+extra,WORK/v); require(p)
        t=re.search(r'dPSI \((\d+)\)',p.stdout); n=re.search(r'Exons from A in exon list\s+(\d+)',p.stdout)
        observed[v]={'threshold':t[1] if t else None,'regulated':int(n[1]) if n else None}
    correct=observed=={'requested':{'threshold':'40','regulated':1},'default':{'threshold':'15','regulated':2}}
elif BUG=='VT-001':
    for v in ['input','normal']:
        d=I/v; p=run(['perl',B/'MakeTableRPKMs.pl','-sp=Hsa','-dbDir='+str(I/'db'),'-C','-TPM'],d); require(p)
        observed[v]={f.name:rows(f) for f in sorted(d.glob('*COUNTS*.tab'))}
    correct=all(any('3' in r[1:] for r in rr if r[0]=='GENE_LOW') for rr in observed['input'].values()) and len(observed['input'])==3
elif BUG=='VT-002':
    for v in ['na-first','na-last','normal']:
        d=I/v; p=run(['perl',REPO/'vast-tools','merge','-o',d,'-g',d/'groups.tab','--noIR','--sp','hg19'],d); require(p)
        observed[v]=rows(d/'to_combine/merged.micX')
    correct=observed['na-first']==observed['na-last'] and bool(observed['na-first']) and all('NA' in r for r in observed['na-first'][1:])
elif BUG=='VT-003':
    for v in ['input','normal']:
        p,rr=diff_tab(v,paired=True); require(p); observed[v]={'eligible_events':[r[1] for r in rr[1:] if r[4]!='NA']}
    correct=observed['input']==observed['normal']=={'eligible_events':['HsaEX0000001']}
elif BUG=='VT-004':
    for name in ['single','tail','normal']:
        for paired in [False,True]:
            p,rr=diff_tab(name,paired,2 if name=='tail' else None)
            observed[name+('-paired' if paired else '-unpaired')]={'exit':p.returncode,'events':max(0,len(rr)-1),'dimension_error':'incorrect number of dimensions' in p.stderr}
    p,rr=diff_tab('single',pdf=True); observed['single-pdf']={'exit':p.returncode,'events':max(0,len(rr)-1),'dimension_error':'incorrect number of dimensions' in p.stderr}
    correct=all(v['exit']==0 and v['events']==(1 if k.startswith('single') else 3 if k.startswith('tail') else 2) for k,v in observed.items())
elif BUG in ['VT-005','VT-006']:
    for v in ['input','normal']:
        d=WORK/v; d.mkdir(); shutil.copy2(I/('input.tab' if BUG=='VT-005' else v+'.tab'),d/'input.tab')
        args=['perl',REPO/'vast-tools','tidy',d/'input.tab','--min_N','1','--outFile',d/'result.tab']
        if BUG=='VT-005': args+=['--groups',I/(v+'-groups.tab')]
        p=run(args,d); observed[v]={'exit':p.returncode,'events':max(0,len(rows(d/'result.tab'))-1),'zero_division':'Illegal division by zero' in p.stderr,'missing_zero_group':'from 0 not found' in p.stderr}
    correct=all(x['exit']==0 for x in observed.values()) and observed['input']['events']==(1 if BUG=='VT-005' else 0) and observed['normal']['events']==1
else: raise ValueError(BUG)
result={'bug':BUG,'correct':bool(correct),'observed':observed}
(WORK/'summary.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
print('CORRECT' if correct else 'WRONG OUTPUT / FAILURE REPRODUCED',file=sys.stderr)
print('Run files: '+str(WORK),file=sys.stderr)

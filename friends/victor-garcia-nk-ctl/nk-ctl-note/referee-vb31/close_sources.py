import hashlib,json,pathlib,re,urllib.request
root=pathlib.Path('/workspace/ref_victor_VB31'); out=root/'public'; records=[]
for name,url in [
 ('google-deepmind_alphaevolve_repository_of_problems_README.md','https://raw.githubusercontent.com/google-deepmind/alphaevolve_repository_of_problems/main/README.md'),
 ('google-deepmind_alphaevolve_repository_of_problems_tree.json','https://api.github.com/repos/google-deepmind/alphaevolve_repository_of_problems/git/trees/main?recursive=1')]:
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-model-referee/1.0'}),timeout=30) as f:data=f.read(5_000_001)
        assert len(data)<=5_000_000
        (out/name).write_bytes(data); records.append({'file':name,'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        if name.endswith('.json'):
            tree=json.loads(data); print('tree entries',len(tree['tree']),'truncated',tree.get('truncated'))
            print('related filenames',[x['path'] for x in tree['tree'] if re.search(r'cancer|immuno|tumou?r|garcia|bonhoeffer',x['path'],re.I)])
    except Exception as ex:records.append({'url':url,'error':str(ex)})
assert (out/'primary.xml').read_bytes()==(out/'final_primary.xml').read_bytes()
assert (out/'figshare_v1.json').read_bytes()==(out/'final_figshare.json').read_bytes()
obj=json.loads((root/'independent_result.json').read_text()); obj2=json.loads((root/'bernstein_result.json').read_text())
dets={p['sha256'] for p in obj['positivity_checks'] if p['label'].endswith(': 4det')}
stats={'unique_determinants':len(dets),'coefficientwise_nonnegative_determinants':sum(min(p['coefficients'])>=0 for p in obj['polynomials'] if p['sha256'] in dets),
       'maximum_subdivision_depth':max(p['max_depth'] for p in obj2['checks']),
       'determinants_needing_subdivision':[p for p in obj2['checks'] if p['sha256'] in dets and p['max_depth']>0]}
print(stats)
(root/'close_sources.json').write_text(json.dumps({'source_recheck':'primary XML and Figshare v1 byte-identical','sources':records,'positivity_simplification':stats},indent=2))
print('SOURCE CHECKS COMPLETE')

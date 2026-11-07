import pathlib,json,hashlib,urllib.request,concurrent.futures,datetime
r=pathlib.Path('/workspace/ref_manuel_M011')
def load(n):return json.loads((r/n).read_text())
old=load('release_live.json');new=load('release_closing.json')
issues=load('issues_closing.json');repos=load('search_closing.json')
assert old['tag_name']==new['tag_name']=='v2.0.0'
assert [i['number'] for i in issues]==[i['number'] for i in load('issues_live.json')]
assert [i['full_name'] for i in repos['items']]==[i['full_name'] for i in load('public/search.json')['items']]
names=['master_D2.R','Epi.md','alphaevolve.md','alpha_problems.md','openai_math.md','erdos.md','kisonecat.md']
receipts={i['file']:i for i in load('public/receipts.json')}
(r/'closing').mkdir(exist_ok=True)
def fetch(name):
 url=receipts[name]['url'];b=urllib.request.urlopen(url,timeout=40).read();(r/'closing'/name).write_bytes(b)
 h=hashlib.sha256(b).hexdigest();return {'file':name,'url':url,'sha256':h,'unchanged':h==receipts[name]['sha256']}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(fetch,names))
assert all(x['unchanged'] for x in rows)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'latest_release':new['tag_name'],'issue_pr_records':len(issues),'repo_search_results':len(repos['items']),'all_unchanged':True,'raw_checks':rows}
(r/'closing_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

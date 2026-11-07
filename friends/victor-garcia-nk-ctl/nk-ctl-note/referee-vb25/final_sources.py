import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request
from datetime import datetime,timezone

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'MathematicsReferee/1.0'}),timeout=35) as r:
        data=r.read(2000000)
    return data
tasks={
 'primary':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7079339/fullTextXML',
 'official_catalog':'https://api.figshare.com/v2/articles/11536824',
 'exact_repo':'https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':'"Cancer-induced immunosuppression"','sort':'updated'}),
 'exact_issues':'https://api.github.com/search/issues?'+urllib.parse.urlencode({'q':'"Cancer-induced immunosuppression" in:title,body','sort':'updated'}),
 'arxiv_exact':'https://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':'all:"Cancer-induced immunosuppression" AND submittedDate:[202511020000 TO 202611022359]','max_results':30}),
 'openai_index':'https://raw.githubusercontent.com/openai/math/main/CONTENTS.md',
}
repos={'BakeLab':'BakeLab/Epi-results','alphaevolve':'google-deepmind/alphaevolve_results',
       'deepmind_correct':'google-deepmind/alphaevolve_repository_of_problems',
       'openai_math_top':'openai/math','einstein_tree':'vinid/einstein-arena',
       'plasma':'plasma-ai/erdos','kisonecat':'kisonecat/openai-math'}
for key,repo in repos.items():tasks['head_'+key]='https://api.github.com/repos/'+repo+'/git/trees/HEAD'
def fetch(item):
    key,url=item
    result={'url':url}
    try:
        data=get(url);result.update({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        if key=='primary':result['matches_frozen']=data==Path('primary_frozen.xml').read_bytes()
        if key=='official_catalog':result['matches_start']=data==Path('figshare.dat').read_bytes()
        if key in ('exact_repo','exact_issues'):
            obj=json.loads(data);result['total_count']=obj['total_count']
            result['items']=[{'url':v['html_url'],'title':v.get('title',v.get('full_name'))} for v in obj['items']]
        if key.startswith('head_'):
            obj=json.loads(data);old=json.loads(Path(key[5:]+'.dat').read_bytes())
            result['tree_sha']=obj['sha'];result['unchanged']=obj['sha']==old['sha']
        if key=='openai_index':
            result['topic_lines']=[l for l in data.decode().splitlines() if any(w in l.lower() for w in ('tumor','cancer','bonhoeffer','110185','immunosupp'))]
        if key=='arxiv_exact':result['response']=data.decode()
    except Exception as ex:result['error']=str(ex)
    return key,result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:out=dict(pool.map(fetch,tasks.items()))
out['utc']=datetime.now(timezone.utc).isoformat()
Path('final_source_receipts.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
print('FINAL SOURCE CHECK DONE')

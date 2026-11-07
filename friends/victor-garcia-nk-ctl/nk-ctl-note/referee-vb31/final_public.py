"""Final bounded public-source check and PDF reading, all on authorized pod."""
import io,json,pathlib,re,sys,urllib.parse,urllib.request,zipfile
root=pathlib.Path('/workspace/ref_victor_VB31'); out=root/'public'
receipts=[]
def get(name,url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-model-referee/1.0'}),timeout=35) as f:data=f.read(5_000_001);status=f.status
        assert len(data)<=5_000_000
        (out/name).write_bytes(data)
        rec={'file':name,'url':url,'status':status,'bytes':len(data)}
    except Exception as ex:rec={'file':name,'url':url,'error':str(ex)};data=b''
    receipts.append(rec);print(rec,flush=True)
    (root/'final_public_receipts.json').write_text(json.dumps(receipts,indent=2))
    return data
meta=get('pypdf_meta.json','https://pypi.org/pypi/pypdf/json')
if meta:
    wheel=next(x for x in json.loads(meta)['urls'] if x['filename'].endswith('py3-none-any.whl'))
    data=get('pypdf.whl',wheel['url'])
    deps=root/'pdf_reader';deps.mkdir(exist_ok=True)
    if data:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for zi in z.infolist():
                assert not zi.filename.startswith('/') and '..' not in pathlib.Path(zi.filename).parts
            z.extractall(deps)
        sys.path.insert(0,str(deps))
        from pypdf import PdfReader
        text='\n'.join(p.extract_text() for p in PdfReader(out/'related_2024.pdf').pages)
        (root/'related_2024_text.txt').write_text(text)
        print('RELATED PAPER',text[:17000],flush=True)
get('openai_math_CONTENTS.md','https://raw.githubusercontent.com/openai/math/main/CONTENTS.md')
get('repository_of_problems_search.json','https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':'repository_of_problems org:google-deepmind','sort':'updated','per_page':10}))
get('final_primary.xml','https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7079339/fullTextXML')
get('final_figshare.json','https://api.figshare.com/v2/articles/11536824/versions/1')
get('final_github.json','https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':'"cancer-induced immunosuppression"','sort':'updated','per_page':10}))
for repo in ['BakeLab/Epi-results','google-deepmind/alphaevolve_results','openai/math','togethercomputer/EinsteinArena-new-SOTA','plasma-ai/erdos','kisonecat/openai-math']:
    get('final_'+repo.replace('/','_')+'.json','https://api.github.com/repos/'+repo)
ob=json.loads((root/'independent_result.json').read_text())
dets={x['sha256'] for x in ob['positivity_checks'] if x['label'].endswith(': 4det')}
detpol=[p for p in ob['polynomials'] if p['sha256'] in dets]
print('DETERMINANT COEFFICIENT CONTROL',len(detpol),'unique determinant numerators; all coefficients positive:',all(min(p['coefficients'])>0 for p in detpol),flush=True)
print('SECOND-ROUTE SUMMARY',json.loads((root/'bernstein_result.json').read_text()),flush=True)
print('DONE',flush=True)

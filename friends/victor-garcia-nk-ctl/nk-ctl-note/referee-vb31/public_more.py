"""Further bounded, read-only public source inspection on the referee pod."""
import hashlib,io,json,pathlib,re,urllib.request,zipfile,subprocess
root=pathlib.Path('/workspace/ref_victor_VB31'); out=root/'public'
receipts=[]
def get(name,url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-model-referee/1.0'}),timeout=35) as f:
            data=f.read(12_000_001); status=f.status
        if len(data)>12_000_000:raise ValueError('bounded read exceeded')
        (out/name).write_bytes(data)
        rec={'file':name,'url':url,'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    except Exception as ex:rec={'file':name,'url':url,'error':str(ex)};data=b''
    receipts.append(rec);print(json.dumps(rec),flush=True)
    (root/'public_more_receipts.json').write_text(json.dumps(receipts,indent=2))
    return data
data=get('figshare_v1.json','https://api.figshare.com/v2/articles/11536824/versions/1')
if data:
    obj=json.loads(data)
    print('FIGSHARE',obj.get('title'),obj.get('description'),flush=True)
    for f in obj.get('files',[]):
        print('FILE',f,flush=True)
        if f.get('size',10**9)<2_000_000:
            name='figshare_'+re.sub('[^a-zA-Z0-9._-]','_',f['name'])
            blob=get(name,f['download_url'])
            if blob and zipfile.is_zipfile(io.BytesIO(blob)):
                archive=zipfile.ZipFile(io.BytesIO(blob))
                for zi in archive.infolist():
                    if zi.filename.endswith(('.R','.r','.txt','.md')) and zi.file_size<400_000:
                        text=archive.read(zi).decode(errors='replace')
                        (out/('released_'+re.sub('[^a-zA-Z0-9._-]','_',zi.filename))).write_text(text)
                        print('RELEASED',zi.filename,flush=True)
                        for line in text.splitlines():
                            if any(token in line.lower() for token in ['dn <-','dn=','dn =','nk','dndt','bn','kap']):print(line[:400],flush=True)

# Read README and tree names, not merely repository metadata.
repos=['BakeLab/Epi-results','google-deepmind/alphaevolve_results','google-deepmind/repository_of_problems','openai/math','togethercomputer/EinsteinArena-new-SOTA','plasma-ai/erdos','kisonecat/openai-math']
for repo in repos:
    meta_file=out/(repo.replace('/','_')+'.json')
    if meta_file.exists():meta=json.loads(meta_file.read_text())
    else:
        blob=get(repo.replace('/','_')+'.json','https://api.github.com/repos/'+repo)
        if not blob:continue
        meta=json.loads(blob)
    branch=meta.get('default_branch','main')
    get(repo.replace('/','_')+'_README.md',f'https://raw.githubusercontent.com/{repo}/{branch}/README.md')
    blob=get(repo.replace('/','_')+'_tree.json',f'https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1')
    if blob:
        tree=json.loads(blob)
        hits=[entry['path'] for entry in tree.get('tree',[]) if re.search(r'garcia|bonhoeffer|cancer|immuno|tumou?r',entry['path'],re.I)]
        print('AGENT_TREE',repo,'truncated',tree.get('truncated'),'paths',len(tree.get('tree',[])),'hits',hits,flush=True)
get('related_2024.pdf','https://wseas.com/journals/msa/2024/a30msa-012%282024%29.pdf')
if (out/'related_2024.pdf').exists():
    subprocess.run(['pdftotext',str(out/'related_2024.pdf'),str(out/'related_2024.txt')],check=False)
print('DONE',flush=True)

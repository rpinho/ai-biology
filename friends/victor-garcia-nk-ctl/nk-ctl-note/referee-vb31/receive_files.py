"""Copy bounded referee results back through the authorized terminal helper."""
import base64,pathlib,subprocess,sys
here=pathlib.Path(__file__).resolve().parent
files=sys.argv[1:]
assert files and all(all(c.isalnum() or c in '/._-' for c in name) and not name.startswith('/') and '..' not in name for name in files)
script=here/'pod_receive.sh'
script.write_text('set -eu\ncd /workspace/ref_victor_VB31\nprintf "REF_PAYLOAD_BEGIN\\n"\ntar -czf - '+ ' '.join(files)+' | base64 -w0\nprintf "\\nREF_PAYLOAD_END\\n"\n')
run=subprocess.run(['python3','_codex/friends_podsh.py','ref',str(script),'60'],capture_output=True,text=True,check=True)
encoded=run.stdout.split('REF_PAYLOAD_BEGIN\n',1)[1].split('\nREF_PAYLOAD_END',1)[0]
payload=base64.b64decode(encoded,validate=True)
assert len(payload)<30_000_000
(here/'referee_evidence.tar.gz').write_bytes(payload)
# The archive contains only explicitly requested paths in our pod directory.
subprocess.run(['tar','-xzf',str(here/'referee_evidence.tar.gz'),'-C',str(here)],check=True)
print('Copied',len(payload),'archive bytes')

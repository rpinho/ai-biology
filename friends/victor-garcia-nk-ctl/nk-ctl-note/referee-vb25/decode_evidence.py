"""Decode the small evidence archive transported through the authorized helper."""
import base64
import hashlib
from pathlib import Path
raw=Path('evidence_transport.txt').read_text()
payload=raw.split('BEGIN_REFEREE_EVIDENCE\n',1)[1].split('\nEND_REFEREE_EVIDENCE',1)[0]
archive=base64.b64decode(payload)
digest=hashlib.sha256(archive).hexdigest()
assert digest in raw.split('BEGIN_REFEREE_EVIDENCE',1)[0]
Path('evidence.tar.gz').write_bytes(archive)
print('Verified archive',len(archive),'bytes SHA256',digest)

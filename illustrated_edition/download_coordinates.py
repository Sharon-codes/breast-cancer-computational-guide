"""Fetch the two public coordinate records and check the recorded input hashes."""
from pathlib import Path
from urllib.request import urlopen, Request
import hashlib
import json
root=Path(__file__).resolve().parent
records=json.loads((root/'scientific_plate_sources.json').read_text())
(root/'research').mkdir(exist_ok=True)
for record in records:
    if record['chapter'] not in [5,7]:
        continue
    path=root/'research'/record['original_file']
    if not path.exists():
        request=Request(record['original_url'],headers={'User-Agent':'ScientificIllustrations/1.0'})
        with urlopen(request,timeout=60) as response:
            data=response.read()
        path.write_bytes(data)
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=record['original_sha256']:
        raise RuntimeError(f'Coordinate source changed for {path.name}; review the archive version before rendering.')
    print(path.name, digest)

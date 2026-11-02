"""Build a deterministic, skill-only ZIP using Python's standard library."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile
import io

ROOT=Path(__file__).resolve().parents[1]
FILES=['SKILL.md','agents/openai.yaml','assets/project-developer-avatar.jpg',
       'assets/project-developer.json','assets/reader.css','assets/reader.js',
       'references/data.md','references/delivery.md','references/platforms.md',
       'references/quality.md','references/selection.md','references/publishing.md',
       'scripts/check_selection.py','scripts/check_review.py','scripts/reader.py']

def package(version):
    if not re.fullmatch(r'\d+\.\d+\.\d+',version):raise ValueError('Use a semantic version, such as 0.1.0')
    skill=ROOT/'skills/markkiller';out=ROOT/'dist';out.mkdir(exist_ok=True)
    manifest={};buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(FILES):
            data=(skill/rel).read_bytes()
            manifest[rel]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
            info=zipfile.ZipInfo('markkiller/'+rel,date_time=(2026,11,2,0,0,0))
            info.create_system=3;info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,data)
    data=buf.getvalue();digest=hashlib.sha256(data).hexdigest()
    name=f'markkiller-v{version}.zip';dest=out/name
    if dest.exists() and dest.read_bytes()!=data:raise RuntimeError('Existing version differs; choose a new version')
    dest.write_bytes(data)
    (out/(name+'.sha256')).write_text(f'{digest}  {name}\n',encoding='utf-8',newline='\n')
    (out/f'manifest-v{version}.json').write_text(json.dumps({'name':'markkiller','version':version,'zip_sha256':digest,'files':manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    with zipfile.ZipFile(dest) as z:
        assert len(z.namelist())==len(FILES)
        for rel,item in manifest.items():assert hashlib.sha256(z.read('markkiller/'+rel)).hexdigest()==item['sha256']
    print(json.dumps({'archive':str(dest),'sha256':digest,'files':len(manifest)},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--version',required=True);package(p.parse_args().version)

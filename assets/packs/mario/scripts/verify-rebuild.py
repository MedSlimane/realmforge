"""Run pack checks and prove that two offline build/preview passes agree."""
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parents[1];OUT=HERE.parents[2]/'web/public/packs/mario'
log=['Remaining-compromises pass — 31 October 2026', 'Source fetch verifies the retained local cache against pinned checksums; not a claim of a fresh remote download of every historical source.', '']
def run(args):
 print('$ '+' '.join(args),flush=True)
 r=subprocess.run(args,cwd=HERE,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 print(r.stdout,flush=True);log.extend(['$ '+' '.join(args),r.stdout,f'Exit: {r.returncode}',''])
 if r.returncode:
  (HERE/'VALIDATION.txt').write_text('\n'.join(log));sys.exit(r.returncode)
def hashes():return {p.relative_to(OUT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.rglob('*')) if p.is_file()}
for args in [['npm','run','fetch'],['npm','run','build'],['npm','run','preview'],['npm','test'],['npm','run','validate'],['npm','run','validate:registry']]:run(args)
first=hashes()
run(['npm','run','build']);run(['npm','run','preview']);second=hashes()
assert first==second,'Repeated pack generation differs'
(HERE/'pack-sha256.json').write_text(json.dumps(second,indent=2)+'\n')
message=f'PASS deterministic rebuild: all {len(second)} output SHA-256 values identical across two build/preview passes.'
print(message);log.append(message);(HERE/'VALIDATION.txt').write_text('\n'.join(log)+'\n')

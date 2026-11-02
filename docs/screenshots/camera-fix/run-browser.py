"""Re-run the saved keyboard/browser probes against a running local Vite server.

Start an isolated Playwright CLI session named camera before running this script.
The CLI must be installed or available through the Codex Playwright skill wrapper.
"""
import argparse
import gzip
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--pack', choices=['mario', 'kenney'], required=True)
parser.add_argument('--mode', choices=['play', 'editor'], required=True)
parser.add_argument('--kind', choices=['trajectory', 'flat', 'slope', 'fall', 'spring', 'forms'], default='trajectory')
parser.add_argument('--label', default='rerun')
args = parser.parse_args()
cli = os.environ.get('PWCLI', str(Path.home() / '.codex/skills/playwright/scripts/playwright_cli.sh'))
code = (ROOT / ('trajectory.browser.js' if args.kind == 'trajectory' else 'fixtures.browser.js')).read_text()
code = code.replace('PACK', args.pack).replace('MODE', args.mode).replace('KIND', args.kind).replace('LABEL', args.label)
# Browser probes use this task's explicit artifact directory; adapt when using another checkout.
code = code.replace('/Users/slimane/realmforge', str(ROOT.parents[2]))
result = subprocess.run([cli, '--session', 'camera', 'run-code', code], text=True, capture_output=True)
if result.returncode:
    raise SystemExit(result.stdout + result.stderr)
if '### Result\n' not in result.stdout:
    raise SystemExit(result.stdout)
record = json.JSONDecoder().raw_decode(result.stdout.split('### Result\n', 1)[1])[0]
name = f'{args.label}-{args.pack}-{args.mode}' + ('' if args.kind == 'trajectory' else f'-{args.kind}')
with gzip.open(ROOT / f'{name}.json.gz', 'wt') as out:
    json.dump(record, out)
print(json.dumps(record['summary'], indent=2))

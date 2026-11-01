#!/usr/bin/env python3
"""Reproduce the complete source-inspection → bind-preview pipeline."""
import argparse
from pathlib import Path
import subprocess
import sys
from extract_inspect import ROOT

parser = argparse.ArgumentParser()
parser.add_argument('--downloads', type=Path, default=Path.home() / 'Downloads/realmforge-rips')
parser.add_argument('--blender', type=Path, default=Path('/Applications/Blender.app/Contents/MacOS/Blender'))
args = parser.parse_args()
(ROOT / 'evidence').mkdir(exist_ok=True)


def run(command, log):
    print('RUN', ' '.join(str(c) for c in command), flush=True)
    with (ROOT / 'evidence' / log).open('w') as output:
        result = subprocess.run([str(c) for c in command], stdout=output, stderr=subprocess.STDOUT)
    if result.returncode:
        print((ROOT / 'evidence' / log).read_text(), file=sys.stderr)
        raise SystemExit(result.returncode)
    print(f'PASS: {log}', flush=True)


# Probe FIRST, even on reruns. The bridge does not call a missing Blender operator.
run([args.blender, '--background', '--factory-startup', '--python-exit-code', '1', '--python-expr',
     "import bpy; print('BLENDER_VERSION', bpy.app.version_string); print('COLLADA_IMPORT_OPERATORS', [x for x in dir(bpy.ops.wm) if 'collada' in x.lower()])"], 'blender-probe.txt')
run([sys.executable, ROOT / 'extract_inspect.py', '--downloads', args.downloads], 'inspection.txt')
run([sys.executable, ROOT / 'prepare_previews.py'], 'preparation.txt')
run([args.blender, '--background', '--factory-startup', '--python-exit-code', '1', '--python', ROOT / 'render_previews.py'], 'render.txt')
run([sys.executable, ROOT / 'validate.py'], 'validation.txt')
run([sys.executable, ROOT / 'create_contact_sheet.py'], 'contact-sheet.txt')
print('PASS: pipeline complete; inspection-only output; no gameplay animation or manifest fragment')

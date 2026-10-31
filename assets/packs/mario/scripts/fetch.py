"""Download images and asset frame metadata only. Never reuse game code.
URLs and checksums are recorded in sources.json after the initial curation.
"""
from pathlib import Path
import concurrent.futures, hashlib, json, re, time, urllib.request
ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parents[1]
RAW = ROOT / 'assets/_downloads/mario'
BASE = 'https://raw.githubusercontent.com/Sicraftails/SMM-WE-OpenWE/main/'

def get(url, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists(): return path.read_bytes()
    last = None
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=45) as r: data = r.read()
            path.write_bytes(data)
            return data
        except Exception as exc:
            last = exc
            time.sleep(min(attempt + 1, 4))
    raise RuntimeError(f'{url}: {last}')

def parse(data): return json.loads(re.sub(r',\s*([}\]])', r'\1', data.decode('utf-8-sig')))

def main():
    lock = HERE / 'sources.json'
    if lock.exists():
        sources = json.loads(lock.read_text())
        def download(s):
            b=get(s['url'],RAW/s['file'])
            assert hashlib.sha256(b).hexdigest()==s['sha256'], s['file']
        with concurrent.futures.ThreadPoolExecutor(10) as pool: list(pool.map(download,sources))
        print(f'Fetched/verified {len(sources)} pinned source files.'); return
    names = '''spr_NSMBU_goomba spr_NSMBU_goomba_stomped spr_NSMBU_koopa spr_NSMBU_koopa_fly spr_NSMBU_shell spr_NSMBU_spiny spr_NSMBU_bullebill_base spr_NSMBU_bulletbill spr_NSMBU_pinchos spr_NSMBU_lava spr_NSMBU_donut spr_NSMBU_chain spr_NSMBU_chainchomp spr_NSMBU_spring spr_NSMBU_spring_land spr_NSMBU_spring_end spr_NSMBU_platform spr_NSMBU_platform_seesaw spr_NSMBU_coin spr_NSMBU_coin_10 spr_NSMBU_key spr_NSMBU_superacorn spr_NSMBU_star spr_NSMBU_arrow_start_hd spr_NSMBU_checkpoint spr_NSMBU_checkpoint_mario spr_NSMBU_flagpole spr_NSMBU_flag_bowser spr_NSMBU_flag_mario spr_NSMBU_flag_base spr_NSMBU_door spr_NSMBU_door_close spr_NSMBU_doorlock_anim spr_NSMBU_pswitch spr_NSMBU_onoffblock_on spr_NSMBU_onoffblock_off spr_NSMBU_qblock spr_NSMBU_qblock_empty spr_NSMBU_noteblock spr_NSMBU_block_ice spr_NSMBU_luigi_walk'''.split()
    all_names=[x['path'] for x in json.loads((RAW/'openwe-sprites-tree.json').read_text())['tree']]
    names += [x for x in all_names if 'NSMBU' in x and any(s in x.lower() for s in ['grinder','sierra','conveyor','belt','cinta','crate','box'])]
    for size in ['big','small']:
        names += [f'spr_NSMBU_mario_{size}_{a}' for a in ['idle','walk','run','skid','jump1','crouch_fall','crouch','wall_slide','dead1']]
    for theme in ['overworld','snow','desert','castle']:
        names += [x for x in all_names if re.fullmatch(f'bg_NSMBU_{theme}_[0-9]',x)]
    names=list(dict.fromkeys(names))
    sources=[]; sprites={}
    def metadata(name):
        url=BASE+f'sprites/{name}/{name}.yy'; f=f'mirror/{name}/{name}.yy'
        b=get(url,RAW/f); return name,parse(b),{'url':url,'file':f,'sha256':hashlib.sha256(b).hexdigest()}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for name,meta,source in pool.map(metadata,names): sources.append(source); sprites[name]=meta
    jobs=[]
    for name,meta in sprites.items():
        frames=meta['frames']; limit=1 if name.startswith('bg_') else (8 if 'mario_' in name else 6)
        indices=sorted(set(round(i*(len(frames)-1)/max(1,min(limit,len(frames))-1)) for i in range(min(limit,len(frames)))))
        for i in indices:
            uid=frames[i]['name'];url=BASE+f'sprites/{name}/{uid}.png'; f=f'mirror/{name}/{uid}.png'
            jobs.append((url,f,name,i))
    def download(job):
        url,f,name,i=job;b=get(url,RAW/f)
        return {'url':url,'file':f,'sha256':hashlib.sha256(b).hexdigest(),'sprite':name,'index':i}
    with concurrent.futures.ThreadPoolExecutor(10) as pool:
        for s in pool.map(download,jobs): sources.append(s)
    for i in [0,2,6,7]:
        f=f'tiles/21847-{i}.png';url=f'https://raw.githubusercontent.com/wizulus/smm2viewer/master/src/assets/img/Tile/21847-{i}.png'
        b=get(url,RAW/f);sources.append({'url':url,'file':f,'sha256':hashlib.sha256(b).hexdigest()})
    lock.write_text(json.dumps(sources,indent=2)+'\n')
    print(f'Downloaded {len(sources)} source files ({len(jobs)} sprite/layer PNGs).')
if __name__=='__main__': main()

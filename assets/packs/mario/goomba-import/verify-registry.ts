// Execute from repo root with assets/node_modules/.bin/tsx (existing dependency).
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { readManifest, elementTexture, getAnimations } from '../../../../web/src/game/assets/registry.ts';
const here = fileURLToPath(new URL('.', import.meta.url));
const manifest = JSON.parse(readFileSync(here + '../../../../web/public/packs/mario/manifest.json', 'utf8'));
const fragment = JSON.parse(readFileSync(here + 'manifest-fragment.json', 'utf8'));
const merged = structuredClone(manifest);
for (const section of ['elements', 'enemies']) Object.assign(merged[section] ??= {}, fragment[section]);
for (const section of Object.keys(manifest)) {
  if (section !== 'elements' && section !== 'enemies') assert.deepEqual(merged[section], manifest[section]);
}
for (const section of ['elements', 'enemies']) {
  for (const [key, entry] of Object.entries(manifest[section])) {
    if (!['walker', 'goomba'].includes(key)) assert.deepEqual(merged[section][key], entry);
  }
}
const files = readManifest(merged, ['walker', 'goomba'], '/packs/mario/');
const refs = ['walker', 'goomba'].map(name => elementTexture(name));
assert.deepEqual(refs[0], refs[1]);
assert.equal(refs[0].key, 'mario-walker');
assert.equal(refs[0].frame, 'goomba_walk_00');
assert.deepEqual(refs[0].displaySize, { w: 1.2, h: 1 });
assert.deepEqual(refs[0].anchor, { x: .5, y: 1 });
const atlases = files.filter(f => f.key === 'mario-walker');
assert.equal(atlases.length, 1);
assert.deepEqual(atlases[0], { kind: 'atlas', key: 'mario-walker', textureURL: '/packs/mario/enemies/goomba-import/atlas.png', atlasURL: '/packs/mario/enemies/goomba-import/atlas.json' });
const animations = getAnimations().filter(a => a.texture === 'mario-walker');
assert.equal(animations.length, 2);
for (const [name, count] of [['walk', 16], ['stomp', 14]] as const) {
  const anim = animations.find(a => a.key === `mario-walker:${name}`)!;
  assert.equal(anim.frames.length, count);
  assert.equal(new Set(anim.frames).size, count);
}
console.log('PASS actual web registry: one atlas; walker/goomba aliases; 16 walk / 14 stomp frames; anchor/scale/URLs; unrelated entries unchanged (in-memory merge only)');

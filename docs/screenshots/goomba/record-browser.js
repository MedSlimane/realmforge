async (page) => {
  await page.goto('http://127.0.0.1:8080/play/1');
  await page.waitForFunction(() => !!window.__play);
  await page.getByRole('button', { name: 'Start run', exact: true }).click();
  const folder = '/Users/slimane/realmforge/docs/screenshots/goomba';
  const fixture = await page.evaluate(async () => (await fetch('/@fs/Users/slimane/realmforge/docs/screenshots/goomba/fixture.level.v1.json')).json());
  await page.keyboard.up('ArrowRight'); await page.keyboard.up('Space');
  await page.evaluate(fixture => { window.__play.scene.restart({level: fixture, from: 'play', levelId: null}); }, fixture);
  await page.waitForFunction(() => window.__play.sequence === null && !window.__play.paused);
  await page.waitForTimeout(650);
  await page.evaluate(() => {
    const s = window.__play;
    window.__goombaEvidence = { samples: [], animations: [], inputs: [], started: performance.now(), fixture: s.file, animationDuration: s.anims.get('mario-walker:stomp').duration };
    const seen = new WeakSet();
    s.events.on('postupdate', () => {
      const e = window.__goombaEvidence;
      const sprites = s.children.list.filter(v => v.texture?.key === 'mario-walker');
      for (const v of sprites) if (!seen.has(v)) {
        seen.add(v);
        for (const event of ['animationupdate','animationcomplete','destroy']) v.on(event, (a,f) => e.animations.push({event, at:performance.now(), key:a?.key, frame:f?.textureFrame,sx:v.scaleX,sy:v.scaleY,x:v.x,y:v.y}));
      }
      e.samples.push({at:performance.now(),physicsFrame:s.frame,player:{x:s.player.body.position.x,y:s.player.body.position.y,vy:s.player.state.vy,mode:s.player.state.mode},enemyEnabled:s.runtime.elements.get(1)?.enabled,sprites:sprites.map(v=>({frame:v.frame.name,sx:v.scaleX,sy:v.scaleY,originX:v.originX,originY:v.originY,x:v.x,y:v.y}))});
    });
  });
  await page.waitForTimeout(1400);
  await page.screenshot({path:folder+'/walk.png'});
  const canvas = page.locator('canvas').first();
  const box = await canvas.boundingBox();
  let finished = false;
  const captures = [];
  const capture = async () => {
    let i=0;
    while (!finished && i<40) {
      const at=await page.evaluate(()=>performance.now());
      const name=`capture-frames/${String(i++).padStart(3,'0')}.png`;
      await page.screenshot({path:folder+'/'+name,clip:box});
      captures.push({name,at});
      await page.waitForTimeout(65);
    }
  };
  const controls = async () => {
    const key = async (name, down) => { await page.evaluate(({name,down})=>window.__goombaEvidence.inputs.push({name,down,at:performance.now()}),{name,down}); await page.keyboard[down?'down':'up'](name); };
    await key('ArrowRight',true);
    await page.waitForTimeout(170);
    await key('Space',true);
    await page.waitForTimeout(420);
    await key('Space',false); await key('ArrowRight',false);
  };
  const stompShot = async () => {
    await page.waitForFunction(()=>window.__play.children.list.some(v=>v.texture?.key==='mario-walker' && v.frame.name.startsWith('goomba_stomp_')),null,{timeout:6000,polling:'raf'});
    await page.screenshot({path:folder+'/stomp.png'});
    await page.waitForFunction(()=>window.__goombaEvidence.animations.some(e=>e.event==='animationcomplete'&&e.key==='mario-walker:stomp'),null,{timeout:3000});
    await page.waitForTimeout(160);
    finished=true;
  };
  await Promise.all([capture(),controls(),stompShot()]);
  const evidence=await page.evaluate(()=>window.__goombaEvidence);
  evidence.captures=captures; evidence.url=page.url();
  evidence.method='Real PlayScene level fixture; ArrowRight + Space keyboard input; unmodified fixed 60Hz controller and Matter enemy collision. Observation only: no activate(), stompVisuals(), finish(), or synthetic animation completion calls.';
  return evidence;
}

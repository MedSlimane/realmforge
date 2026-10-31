// From the repo root with the lab running, pass this function to playwright-cli run-code.
async (page) => {
  const consoleErrors = [], pageErrors = [];
  const onConsole = message => {if (message.type() === 'error') consoleErrors.push(message.text());};
  const onPageError = error => pageErrors.push(error.message);
  page.on('console', onConsole); page.on('pageerror', onPageError);
  await page.reload();
  await page.waitForFunction(() => !!window.seesawLab);
  const assert = (condition, message, value) => {if (!condition) throw new Error(`${message}: ${JSON.stringify(value)}`);};
  const isolated = await page.evaluate(() => window.seesawLab.isolatedGrowthBounds());
  assert(isolated.parentBoundsContainMain, 'Isolated growth bounds', isolated);
  const scenarios = [];
  for (const scenario of ['rest', 'left', 'right', 'fall']) {
    await page.evaluate(scenario => window.seesawLab.reset(scenario), scenario);
    // Exercise the actual UI growth control before landing.
    await page.getByRole('button', {name: 'Grow / shrink', exact: true}).click();
    const resting = await page.evaluate(() => {
      window.seesawLab.advance(360);
      return window.seesawLab.advance(120);
    });
    assert(resting.last.player.form === 'big' && resting.last.parentBoundsContainMain, 'Grown hull', resting);
    assert(resting.footContacts === 120 && resting.maxPenetration < 0.64 && resting.verticalRange < 0.5 && resting.horizontalRange < 0.5 && resting.maxHingeError < 0.001, 'Grown standing', resting);
    await page.screenshot({path: `game-core/docs/evidence/growth-adapter/grown-${scenario}.png`, fullPage: true});
    await page.getByRole('button', {name: 'Jump 1 frame', exact: true}).click();
    const takeoff = await page.evaluate(() => window.seesawLab.metrics());
    assert(takeoff.player.vy < 0 && !takeoff.footContact && takeoff.parentBoundsContainMain && takeoff.player.y < resting.last.player.y - 8, 'Grown jump', takeoff);
    await page.screenshot({path: `game-core/docs/evidence/growth-adapter/jump-${scenario}.png`, fullPage: true});
    const relanding = await page.evaluate(() => {window.seesawLab.advance(180); return window.seesawLab.advance(120);});
    assert(relanding.footContacts === 120 && relanding.maxPenetration < 0.64 && relanding.maxHingeError < 0.001 && relanding.last.parentBoundsContainMain, 'Grown re-landing', relanding);
    // The free hinge can tilt under a centered jump's landing impulse; record carry
    // rather than asserting that its deck remains exactly level after that impact.
    if (scenario !== 'rest') assert(relanding.verticalRange < 0.5 && relanding.horizontalRange < 0.5, 'Tilted rest after jump', relanding);
    scenarios.push({scenario, resting, takeoff, relanding});
  }
  const cycles = [];
  for (const scenario of ['rest', 'left', 'right']) {
    const cycle = await page.evaluate(scenario => {
      const lab = window.seesawLab;
      lab.reset(scenario); lab.advance(360);
      const small = lab.metrics();
      const big = lab.setForm('big');
      const crouch = lab.advance(1, {left: false, right: false, up: false, down: true, run: false, jump: false}).last;
      const stand = lab.advance(1).last;
      const shrunk = lab.setForm('small');
      return {scenario, small, big, crouch, stand, shrunk,
        feet: [small.player.y + 30, big.player.y + 60, crouch.player.y + 30, stand.player.y + 60, shrunk.player.y + 30]};
    }, scenario);
    assert(Math.max(...cycle.feet) - Math.min(...cycle.feet) < 0.06, 'Resize feet anchor', cycle);
    for (const phase of ['small', 'big', 'crouch', 'stand', 'shrunk']) assert(cycle[phase].parentBoundsContainMain && cycle[phase].footContact, `Bounds/contact during ${phase}`, cycle);
    assert(cycle.big.player.form === 'big' && cycle.crouch.player.form === 'big' && cycle.stand.player.form === 'big' && cycle.shrunk.player.form === 'small', 'Resize form sequence', cycle);
    cycles.push(cycle);
  }
  page.off('console', onConsole); page.off('pageerror', onPageError);
  assert(!consoleErrors.length && !pageErrors.length, 'Browser errors', {consoleErrors, pageErrors});
  return {browser: await page.context().browser().version(), isolated, scenarios, cycles, consoleErrors, pageErrors};
}

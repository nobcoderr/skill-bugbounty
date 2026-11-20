import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';

const [cmd, rawX, rawY] = process.argv.slice(2);

function xdotool(args) {
  const result = spawnSync('xdotool', args, { encoding: 'utf8' });
  if (result.status !== 0) {
    const detail = (result.stderr || result.stdout || 'xdotool failed').trim();
    throw new Error(detail);
  }
  return (result.stdout || '').trim();
}

function requireNumber(value, name) {
  const number = Number(value);
  if (!Number.isFinite(number) || number < 0) {
    throw new Error(`${name} must be a non-negative page pixel`);
  }
  return number;
}

const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
const context = browser.contexts()[0];
const pages = context.pages();
const page = pages[pages.length - 1];
if (!page) {
  throw new Error('no page');
}
await page.bringToFront();

const metrics = await page.evaluate(() => ({
  screenX: window.screenX,
  screenY: window.screenY,
  chromeTop: window.outerHeight - window.innerHeight,
  chromeLeft: Math.max(0, window.outerWidth - window.innerWidth),
  dpr: window.devicePixelRatio || 1,
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
}));

function toScreen(x, y) {
  if (x > metrics.innerWidth || y > metrics.innerHeight) {
    throw new Error('point is outside the page');
  }
  return {
    x: Math.round((metrics.screenX + metrics.chromeLeft + x) * metrics.dpr),
    y: Math.round((metrics.screenY + metrics.chromeTop + y) * metrics.dpr),
  };
}

function move(x, y) {
  const target = toScreen(x, y);
  // `--sync` can wait forever under XWayland/virtual desktops even after the
  // pointer has moved. A normal mousemove is synchronous at the process level
  // and remains observable through the location check below.
  xdotool(['mousemove', String(target.x), String(target.y)]);
  const location = xdotool(['getmouselocation', '--shell']);
  const found = Object.fromEntries(
    location.split('\n').map((line) => line.split('=')),
  );
  return {
    pageX: x,
    pageY: y,
    screenX: target.x,
    screenY: target.y,
    cursorX: Number(found.X),
    cursorY: Number(found.Y),
  };
}

let report;
if (cmd === 'move') {
  report = move(requireNumber(rawX, 'x'), requireNumber(rawY, 'y'));
} else if (cmd === 'click') {
  report = move(requireNumber(rawX, 'x'), requireNumber(rawY, 'y'));
  xdotool(['click', '1']);
  report.clicked = true;
} else if (cmd === 'click-text') {
  const label = rawX || '';
  if (!label) {
    throw new Error('text required');
  }
  const box = await page.getByText(label, { exact: false }).first().boundingBox();
  if (!box) {
    throw new Error('text not visible');
  }
  report = move(Math.round(box.x + box.width / 2), Math.round(box.y + box.height / 2));
  xdotool(['click', '1']);
  report.clicked = true;
  report.text = label;
} else {
  throw new Error('usage: move|click X Y | click-text TEXT');
}

console.log(JSON.stringify(report));
// Exiting disconnects this CDP client without closing the user's Chromium.
process.exit(0);

// Render src/flyer/flyer.html to img/esplendor-flyer.pdf (Letter) with Playwright.
// Usage: node tools/make_flyer.mjs [path-to-playwright-index.mjs]
import path from 'path'; import { fileURLToPath, pathToFileURL } from 'url';
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const pw = process.argv[2] || 'playwright';
const { chromium } = await import(pw.startsWith('/') ? pathToFileURL(pw).href : pw);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 816, height: 1056 } });
for (const [src, out] of [['flyer.html', 'esplendor-flyer.pdf'], ['flyer-es.html', 'esplendor-ficha-es.pdf']]) {
  await p.goto(pathToFileURL(path.join(root, 'src/flyer', src)).href, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(root, 'img', out), width: '8.5in', height: '11in', printBackground: true, pageRanges: '1' });
}
if (process.env.PREVIEW) await p.screenshot({ path: process.env.PREVIEW });
await b.close(); console.log('flyer written');

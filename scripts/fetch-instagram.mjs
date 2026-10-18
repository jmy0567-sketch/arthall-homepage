// Apify Instagram Scraper로 @shinbuldang_artcenter 최신 게시물을 받아
// assets/instagram/ 에 사진(로컬 저장)과 posts.json 을 만든다.
// 인스타그램 CDN 주소는 며칠 뒤 만료되므로 사진은 반드시 내려받아 둔다.
// 실행: APIFY_TOKEN=... node scripts/fetch-instagram.mjs
import { mkdir, writeFile, readdir, unlink } from 'node:fs/promises';
import path from 'node:path';

const USERNAME = process.env.IG_USERNAME || 'shinbuldang_artcenter';
const LIMIT = parseInt(process.env.IG_LIMIT || '12', 10);
const TOKEN = process.env.APIFY_TOKEN;
const OUT = path.resolve('assets/instagram');

if (!TOKEN) { console.error('APIFY_TOKEN 이 없습니다. GitHub 저장소 Secrets에 등록하세요.'); process.exit(1); }

const api = 'https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items';
const res = await fetch(api, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${TOKEN}` },
  body: JSON.stringify({
    directUrls: [`https://www.instagram.com/${USERNAME}/`],
    resultsType: 'posts',
    resultsLimit: LIMIT,
    addParentData: false,
  }),
});
if (!res.ok) { console.error('Apify 요청 실패', res.status, (await res.text()).slice(0, 500)); process.exit(1); }
const items = await res.json();
if (!Array.isArray(items)) { console.error('예상하지 못한 응답', JSON.stringify(items).slice(0, 500)); process.exit(1); }
if (items.some(i => i.error)) console.warn('일부 항목 오류:', items.filter(i => i.error).map(i => i.error));

await mkdir(OUT, { recursive: true });
const posts = [];
for (const it of items) {
  const code = it.shortCode;
  const src = it.displayUrl;
  if (!code || !src || !/^[\w-]+$/.test(code)) continue;
  const file = `${code}.jpg`;
  try {
    const img = await fetch(src);
    if (!img.ok) throw new Error(img.status);
    await writeFile(path.join(OUT, file), Buffer.from(await img.arrayBuffer()));
  } catch (e) { console.warn('사진 저장 실패', code, e.message); continue; }
  posts.push({
    permalink: it.url || `https://www.instagram.com/p/${code}/`,
    image: `assets/instagram/${file}`,
    type: it.type === 'Video' ? 'VIDEO' : 'IMAGE',
    caption: (it.caption || '').slice(0, 300),
    timestamp: it.timestamp || null,
  });
}
posts.sort((a, b) => String(b.timestamp).localeCompare(String(a.timestamp)));

if (!posts.length) { console.error('게시물을 하나도 받지 못해 기존 파일을 유지합니다.'); process.exit(1); }

// 목록에서 빠진 옛 사진 정리
const keep = new Set(posts.map(p => path.basename(p.image)));
for (const f of await readdir(OUT)) if (f.endsWith('.jpg') && !keep.has(f)) await unlink(path.join(OUT, f));

await writeFile(path.join(OUT, 'posts.json'),
  JSON.stringify({ username: USERNAME, updated: new Date().toISOString(), posts }, null, 2) + '\n');
console.log(`게시물 ${posts.length}개 저장 완료`);

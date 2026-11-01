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

// 키를 어디서 찾았는지 기록에 남긴다(값은 출력하지 않음). 키가 없으면 실패 대신 건너뛰어 알림 메일을 막는다.
const KEY_FROM = process.env.KEY_FROM || (TOKEN ? 'env' : 'none');
const FROM_LABEL = {
  secret: '저장소 비밀 APIFY_TOKEN',
  'secret-alt': '저장소 비밀 APIFY_API_TOKEN (이름이 달라도 사용함)',
  variable: '변수(Variables) 탭 APIFY_TOKEN',
  env: '환경 변수 APIFY_TOKEN',
  none: '찾지 못함',
}[KEY_FROM] || KEY_FROM;
console.log(`Apify 키 위치: ${FROM_LABEL}`);
if (!TOKEN) {
  console.log('::notice title=Apify 키 없음::건너뜀. 저장소 Settings → Secrets and variables → Actions → Secrets 탭 → "Repository secrets"에 이름 APIFY_TOKEN 으로 등록하세요. (Environment secrets, Dependabot·Codespaces 비밀은 읽지 못합니다)');
  process.exit(0);
}
if (KEY_FROM === 'variable') {
  console.log('::warning title=키가 변수 탭에 있음::작동은 하지만 변수는 암호화되지 않습니다. Secrets 탭의 Repository secrets로 옮기고 변수는 삭제하세요.');
}

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

# 신불당아트센터 네이버 블로그(jmy0567) 새 글 → 아트홀 홈페이지 '블로그 소식' 칸 자동 반영
# 사용: python tools/update_blog.py [사이트 폴더]   (표준 라이브러리만 씀, GitHub Actions에서 하루 2번 실행)
import html, re, sys, urllib.request
from email.utils import parsedate_to_datetime
from pathlib import Path

BLOG = 'jmy0567'
RSS = f'https://rss.blog.naver.com/{BLOG}.xml'
N = 6
root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
page = root / 'index.html'

def clean(s):
    s = re.sub(r'<!\[CDATA\[|\]\]>', '', s)
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).strip()

req = urllib.request.Request(RSS, headers={'User-Agent': 'Mozilla/5.0 (site-blog-sync)'})
xml = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
items = []
for it in re.findall(r'<item>(.*?)</item>', xml, re.S):
    g = lambda tag: (re.search(rf'<{tag}>(.*?)</{tag}>', it, re.S) or [None, ''])[1]
    title = re.sub(r'\s+', ' ', clean(g('title')))
    link = clean(g('link')).split('?')[0]
    cat = clean(g('category'))
    desc = re.sub(r'\s+', ' ', clean(g('description')))
    try:
        d = parsedate_to_datetime(clean(g('pubDate')))
        date = f'{d.month}. {d.day}.'
    except Exception:
        date = ''
    if title and link:
        items.append((title, link, cat, desc[:70], date))
items = items[:N]
if not items:
    print('블로그 글을 못 읽음 — 그대로 둠'); sys.exit(0)

E = lambda s: html.escape(s, quote=True)
cards = ''.join(
    f'<a class="blog-card" href="{E(l)}" target="_blank" rel="noopener">'
    f'<span class="blog-meta num">{E(dt)}{" · " + E(c) if c else ""}</span>'
    f'<b>{E(t)}</b><span class="blog-desc">{E(ds)}…</span></a>'
    for t, l, c, ds, dt in items)
block = f'<!--BLOG-START--><div class="blog-grid">{cards}</div><!--BLOG-END-->'
s = page.read_text(encoding='utf-8')
new = re.sub(r'<!--BLOG-START-->.*?<!--BLOG-END-->', block, s, flags=re.S)
if new != s:
    page.write_text(new, encoding='utf-8'); print('블로그 소식', len(items), '개 반영')
else:
    print('변경 없음')

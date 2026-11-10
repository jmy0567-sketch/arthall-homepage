# 신불당아트센터 M갤러리 홈페이지 만들기
# 사용: python -X utf8 mgallery/build.py  → mgallery/*.html (한국어) + en/ ja/ zh/ (영어·일본어·중국어) 다시 생성
# 구조: 갤러리현대식(메뉴 4개, 첫 화면 전시 사진, 이름 목록, 정사각 회색 칸 작품, 전시 탭)
#     + PKM식(작품 한 점씩 크게 넘겨 보기 + 작품마다 문의, 한·영 소개, 작가별 전시 목록)
# 작품 목록 = works.json (작가별 [제목, 재료, 크기, 연도]), 사진 = img/<작가>-NN.jpg 순서대로, 크기 = dims.json
# 번역 = i18n.py. 사실은 공식 홈페이지(신불당아트센터.com /310 /311 /389)와 대표님 확인값만 쓴다.
import json, os, html, sys, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n import LANGS, LANG_LABEL, HTML_LANG, OG_LOCALE, UI, ARTIST_T, CV_HEAD, CV_EN, EX_T, WHO_T, WHERE_T

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, 'works.json'), encoding='utf-8'))
DIMS = json.load(open(os.path.join(HERE, 'dims.json'), encoding='utf-8'))
BASE = 'https://jmy0567-sketch.github.io/arthall-homepage/mgallery/'
OFFICIAL = 'http://www.xn--ok1b63rk1c60br1eixzmoc.com/'
# 아트시(해외 판매) 작가 페이지. 박상국·고성희는 아트시에 올라가면 주소 추가. 가격이 달러로 보여서 외국어 페이지에만 링크
ARTSY = {'kong': 'https://www.artsy.net/artist/eunjee-kong', 'yi': 'https://www.artsy.net/artist/jeongsik-yi', 'park': 'https://www.artsy.net/artist/park-sang-kuk'}
ARTSY_GAL = 'https://www.artsy.net/partner/shinbuldang-art-center'
ARTSY_T = {'en': 'View & buy on Artsy', 'ja': 'Artsyで作品を見る・購入する', 'zh': '在 Artsy 查看与购买'}
KAKAO = 'https://pf.kakao.com/_vaDxeX'
NAVER_MAP = 'https://map.naver.com/p/search/%EC%8B%A0%EB%B6%88%EB%8B%B9%EC%95%84%ED%8A%B8%EC%84%BC%ED%84%B0'
KAKAO_MAP = 'https://map.kakao.com/?q=%EC%B2%9C%EC%95%88%20%EB%B6%88%EB%8B%B934%EA%B8%B8%203-16'
NOINDEX = False  # 11/08 대표님 OK로 검색 공개. 다시 숨기려면 True
E = html.escape
def ver(f):  # 파일이 바뀌면 주소 끝 숫자가 바뀌어 휴대폰이 옛 파일을 안 씀
    return hashlib.md5(open(os.path.join(HERE, 'assets', f), 'rb').read()).hexdigest()[:8]

ARTISTS = [
  dict(id='kong', ko='공은지', en='Eunjee Kong', field='판화 · 회화', rep=23,
       intro='홍익대학교 일반대학원 판화과를 졸업했어요. 실크스크린 판화와 아크릴 회화로 작업하고, 작품이 국립대만미술관·천안시청·호서대학교에 소장되어 있어요.',
       insta='eunjeekong',
       cv={
        '학력': ['2017 홍익대학교 일반대학원 판화과 석사 졸업', '2012 홍익대학교 시각디자인과 졸업'],
        '수상': ['2022 International Biennial Print Exhibit: 2022 R.O.C. 선정', '2022 The 8th NBC MESHTECH Tokyo International Screen Print Biennial 수상 후보', '2021 제1회 필로프린트판화가협회 신진작가공모전 최우수상', '2016 제23회 한국미술국제공모대전 입선', '2016 제36회 현대판화가협회 신인공모전 입선'],
        '개인전': ['2024 3월의 작가 – 공은지 초대전 (신불당아트센터 M스테이션, 천안)', '2023 치유의 형태 (신불당아트센터 M갤러리, 천안)', '2022 RED STARE (갤러리밈, 서울)', '2019 WHERE I STAND (갤러리밈, 서울)'],
        '그룹전': ['2025 이쪽과 저쪽 – 이정식·공은지 2인전 (M갤러리, 천안)', '2024 홍미원 창립전 (리각미술관, 천안)', '2024 청춘찬가 아트페스타 (노들섬갤러리, 서울)', '2024 유유유프로젝트 – 즐거운 미술여행 (임립미술관, 공주)', '2024 하늘 아래 어울림 – 천안작가 42인 초대전 (호서대 아산캠퍼스 갤러리)', '2024 당신의 안뇽 (M갤러리, 천안)', '2023 STAY – 삼원아트스폰서십 5기 그룹전 (삼원갤러리, 서울)', '2022 International Biennial Print Exhibit (국립대만미술관, 타이중)', '2022 The Exchange Exhibition of Korean and Thai Contemporary Prints (한국문화원, 방콕)', '2022 NBC Meshtec Tokyo Screen Print Biennial (도쿄)', '그 외 다수'],
        '작품 소장': ['국립대만미술관, 천안시청, 호서대학교'],
       }),
  dict(id='yi', ko='이정식', en='Jeongsik YI', field='회화 · 먹, 아크릴', rep=3,
       intro='단국대학교에서 동양화를 공부했어요. 먹과 아크릴로 산과 길을 그리고, 작품이 천안시립미술관·천안시청 등에 소장되어 있어요. 2013년 충남미술대전 대상을 받았어요.',
       insta='jiwoo_yijeongsik',
       cv={
        '학력': ['2018 단국대학교 대학원 회화과 동양화전공 졸업', '2016 단국대학교 예술대학 동양화과 졸업'],
        '수상': ['2018 도솔미술대전 최우수상', '2017 전국대학미술공모전 특선', '2016 문경새재휘호대회 특선', '2015 추사휘호대회 특선', '2014 남농미술대전 특선', '2013 충남미술대전 대상'],
        '개인전': ['2025 Circulation (명동갤러리, 천안)', '2024 헤테로토피아 (M갤러리, 천안)', '2023 There (M갤러리, 천안)', '2022 산수플랫폼展 (갤러리산책, 아산)', '2021 Start over (서북갤러리, 천안) · 유전-교차점 (문화상회다담, 수원)', '2019 Exodus (삼거리갤러리, 천안)', '2017 낮은음자리 (갤러리미술세계, 서울)'],
        '그룹전': ['2026 검은산 붉은몸 2인전 (홍대 아트앤디자인밸리, 서울)', '2026 五人五色, 한곳에 머물다 (헤라스아트, 서울)', '2025 이쪽과 저쪽 2인전 (M갤러리, 천안)', '2024 당신의 안뇽 (M갤러리, 천안)', '2024 Light, Color, Line (몸갤러리, 서울)', '2023 관계도시 유동하는 미래 (천안시립미술관)', '2023 천안비전23 (리각미술관, 천안)', '2018 아시아프 (동대문DDP, 서울) 외 다수'],
        '작품 소장': ['천안시립미술관, 대전검찰청 천안지검, 충청남도 홍성군청, 천안시청'],
        '현재': ['대한민국전통예술전승원 이사, 한국미술협회 청년분과 부위원장'],
       }),
  dict(id='park', ko='박상국', en='Park Sang Kuk', field='회화 · 아크릴 추상', rep=8,
       intro='한남대학교 미술교육과와 같은 대학 일반대학원 미술과를 졸업했어요. 개인전을 13회 열었고, 대한민국미술대전·단원미술대상전 심사위원을 지냈어요. 지금 연작은 「UNEXPECTEDLY MEETING A MARTIAN(뜻밖에 화성인을 만나다)」이에요.',
       insta='',
       cv={
        '학력': ['한남대학교 미술교육과 졸업', '한남대학교 일반대학원 미술과 석사'],
        '개인전': ['개인전 13회, 국내외 초대전 다수', '2026 박상국 초대전 (신불당아트센터 M갤러리, 천안)'],
        '경력': ['단원미술대상전 심사위원 역임', '대한민국미술대전 심사위원 역임', '대전직할시전 초대작가·심사위원·운영위원 역임', '충남미술대전 초대작가·심사위원·운영위원 역임', '나혜석미술공모전 심사위원 역임', '한남대 회화과·미술과 대학원, 남서울대 강사 역임'],
        '현재': ['창형전, 상형전, 한국미술협회, 한국수채화작가회', '갤러리아 백화점 문화센터 서양화 강사'],
       }),
  dict(id='ko', ko='고성희', en='', field='조각 · 유리공예', rep=None,
       intro='남서울대학교 유리공예 교수이자 조각가예요. 2025년 여름 M갤러리에서 고영환 작가와 2인전 「身體視詩」를 열었어요.',
       insta='', cv={'전시': ['2025 조각가 고성희·고영환 身體視詩 (신불당아트센터 M갤러리, 천안)']}),
]
A = {a['id']: a for a in ARTISTS}

# 전시: (상태, 작가 표시, 제목, 기간, 장소, 관련 작가 id들, 사진, 공식 페이지)
EXHIBITIONS = [
  ('now', 'M갤러리 전속 작가', '공은지 기획전시', '2026. 11. 6 – 11. 12', '2층 M갤러리 · 무료 관람 · 매일 10:00–20:00', ['kong'], 'install-wide', None),
  ('past', '그룹전', '다시 모이다: 네 번째 모임', '2026. 10. 1 – 10. 10', 'M갤러리', [], None, 'galleryPast'),
  ('past', 'park', '박상국 초대전', '2026. 9. 16 – 9. 28', 'M갤러리', ['park'], None, 'galleryPast'),
  ('past', 'park', '박상국 초대전', '2026. 6. 17 – 6. 30', 'M갤러리', ['park'], None, 'galleryPast'),
  ('past', 'yi,kong', '이쪽과 저쪽', '2025. 9. 24 – 10. 9', 'M갤러리 · 전속작가 2인전', ['yi', 'kong'], None, '337'),
  ('past', 'ko,+고영환', '身體視詩', '2025. 8. 1 – 8. 14', 'M갤러리 · 조각 2인전', ['ko'], None, '324'),
  ('past', '기획전', '여보! 우리집에도 그림 한점 걸까?', '2025. 3. 1 – 4. 15', 'M갤러리 특별 기획전', [], None, '296'),
  ('past', '그룹전', 'M갤러리 5대작가 특별전', '2024. 9. 9 – 9. 22', 'M갤러리', [], None, '256'),
  ('past', 'yi', '헤테로토피아', '2024. 8. 26 – 9. 1', 'M갤러리 · 개인전', ['yi'], None, '253'),
  ('past', 'kong', '3월의 작가 – 공은지 초대전', '2024. 3', 'M스테이션', ['kong'], None, None),
  ('past', 'kong', '치유의 형태', '2023. 7', 'M갤러리 · 개인전', ['kong'], None, None),
  ('past', 'yi', 'There', '2023', 'M갤러리 · 개인전', ['yi'], None, None),
]
STRIP = ['install-room', 'install-merge3', 'install-fists', 'install-pastel']
GUEST = {'고영환': {'ko': '고영환', 'en': 'Ko Younghwan', 'ja': 'コ・ヨンファン', 'zh': 'Ko Younghwan'}}

# ---- 언어별 도우미 (build_lang에서 L을 바꾼다) ----
L = 'ko'
def T(k): return UI[L][k]
def P(): return '' if L == 'ko' else '../'
def aname(aid): return A[aid]['ko'] if L == 'ko' else ARTIST_T[aid][L][0]
def asub(aid): return (A[aid]['en'] or A[aid]['field']) if L == 'ko' else ARTIST_T[aid][L][1]
def afield(aid): return A[aid]['field'] if L == 'ko' else ARTIST_T[aid][L][1]
def aintro(aid): return A[aid]['intro'] if L == 'ko' else ARTIST_T[aid][L][2]
def tr(d, k): return k if L == 'ko' else d.get(k, {}).get(L, k)
def who(w):
    if w in ('M갤러리 전속 작가', '그룹전', '기획전'): return tr(WHO_T, w)
    return ' · '.join(GUEST[p[1:]][L] if p.startswith('+') else aname(p) for p in w.split(','))
def ex_title(t): return tr(EX_T, t)
def ex_where(w): return tr(WHERE_T, w)
def ex_state(s): return T('now') if s == 'now' else T('past')

def work(aid, n): return W[aid][n - 1]
def label(aid, n):
    t, med, size, yr = work(aid, n)
    return f"{aname(aid)}, {t}, {yr}, {med}, {size}" if L == 'en' else f"{aname(aid)} 「{t}」 {yr}, {med}, {size}"

def tile(aid, n):
    t, med, size, yr = work(aid, n)
    key = f'{aid}-{n:02d}'; w, h = DIMS[key]; src = f'{P()}img/{key}.jpg'
    caphtml = f'<span class="t"><i>{E(t)}</i>, {yr}</span><br><span class="muted">{E(aname(aid))} · {E(med)} · {E(size)}</span>'
    return (f'<figure class="tile" style="margin:0">'
            f'<button class="sq" type="button" data-set="{aid}" data-src="{src}" data-alt="{E(aname(aid))} — {E(t)}" data-caphtml="{E(caphtml)}" data-work="{E(label(aid, n))}" aria-label="{E(t)}">'
            f'<img src="{src}" width="{w}" height="{h}" alt="{E(aname(aid))} — {E(t)}" loading="lazy"></button>'
            f'<figcaption class="cap"><i>{E(t)}</i> <span class="y">{yr}</span><br><span class="y">{E(med)} · {E(size)}</span></figcaption>'
            f'<button class="ask" type="button" data-ask="{E(label(aid, n))}">{E(T("ask_work"))}</button></figure>')

def head(title, desc, page, cur='', image='img/install-room.jpg', ld=None):
    nav = list(zip(['artists.html', 'exhibitions.html', 'buy.html', 'visit.html'], T('nav')))
    navh = ''.join(f'<a href="{h}"' + (' aria-current="page"' if cur == h else '') + f'>{E(t)}</a>' for h, t in nav)
    def url(lg): return BASE + ('' if lg == 'ko' else lg + '/') + page
    def rel(lg):
        if lg == L: return page or './'
        if L == 'ko': return f'{lg}/{page}'
        return (f'../{page}' or '../') if lg == 'ko' else f'../{lg}/{page}'
    langs = ''.join(f'<a href="{rel(lg)}" hreflang="{HTML_LANG[lg]}" lang="{HTML_LANG[lg]}"' + (' aria-current="true"' if lg == L else '') + f'>{LANG_LABEL[lg]}</a>' for lg in LANGS)
    alts = ''.join(f'<link rel="alternate" hreflang="{HTML_LANG[lg]}" href="{url(lg)}">' for lg in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{url("ko")}">'
    return f'''<!doctype html>
<html lang="{HTML_LANG[L]}"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
{'<meta name="robots" content="noindex">' if NOINDEX else ''}
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url(L)}">{alts}
<meta property="og:type" content="website"><meta property="og:site_name" content="{E(T('sub'))}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{BASE}{image}"><meta property="og:locale" content="{OG_LOCALE[L]}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="{P()}assets/style.css?v={ver('style.css')}">
{f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''}
</head><body>
<header class="top"><div class="wrap">
<a class="logo" href="./"><b><strong>M</strong><i>.</i> GALLERY</b><span>{E(T('sub'))}</span></a>
<nav class="nav" aria-label="menu">{navh}</nav>
</div><div class="langs"><div class="wrap">{langs}</div></div></header>
<main>'''

def foot():
    b = T('bar')
    return f'''</main>
<footer><div class="wrap">
<p><b>{E(T('foot1'))}</b></p>
<p>{E(T('contact'))} +82 1533-8771 · KakaoTalk <a href="{KAKAO}" target="_blank" rel="noopener">신불당M갤러리</a> · {E(T('insta_l'))} <a href="https://www.instagram.com/shinbuldang_artcenter/" target="_blank" rel="noopener">@shinbuldang_artcenter</a> · <a href="{OFFICIAL}" target="_blank" rel="noopener">{E(T('center'))}</a> · <a href="{P()}../">{E(T('arthall'))}</a></p>
<p>{E(T('foot_note'))}</p>
</div></footer>
<nav class="bar" aria-label="quick"><button class="main" type="button" data-ask="">{E(b[0])}</button><a href="tel:15338771">{E(b[1])}</a><a href="{NAVER_MAP}" target="_blank" rel="noopener">{E(b[2])}</a></nav>
<script src="{P()}assets/site.js?v={ver('site.js')}" defer></script>
</body></html>
'''

def ex_card(x):
    st, w, title, when, where, ids, img, link = x
    reps = [A[i] for i in ids if A[i]['rep']]
    if img:
        ph = f'<div class="ph"><img src="{P()}img/{img}.jpg" alt="{E(ex_title(title))}" loading="lazy"></div>'
    elif reps:
        ph = '<div class="ph art">' + ''.join(f'<img src="{P()}img/{r["id"]}-{r["rep"]:02d}.jpg" alt="{E(aname(r["id"]))}" loading="lazy">' for r in reps[:2]) + '</div>'
    else:
        ph = f'<div class="ph empty">{E(ex_title(title))}</div>'
    href = 'kong.html' if (img and 'kong' in ids) else (OFFICIAL + link if link else None)
    inner = f'{ph}<div class="ex-meta"><span class="st">{E(ex_state(st))}</span><span class="ar">{E(who(w))}</span><span class="ti">{E(ex_title(title))}</span><span class="dt">{E(when)}<br>{E(ex_where(where))}</span></div>'
    if href:
        ext = '' if href.endswith('.html') else ' target="_blank" rel="noopener"'
        return f'<a class="ex-card" href="{href}"{ext}>{inner}</a>'
    return f'<div class="ex-card">{inner}</div>'

def name_card(a):
    if a['rep']:
        ph = f'<div class="ph"><img src="{P()}img/{a["id"]}-{a["rep"]:02d}.jpg" alt="{E(aname(a["id"]))}" loading="lazy"></div>'
    else:
        ph = f'<div class="ph empty">{E(aname(a["id"])[0])}</div>'
    return f'<a class="name-card" href="{a["id"]}.html">{ph}<div><b>{E(aname(a["id"]))}</b><span>{E(asub(a["id"]))}</span></div></a>'

def collect_band():
    return f'''<div class="collect"><div class="wrap">
<div><h2>{E(T('collect_h'))}</h2><p class="muted" style="margin-top:6px">{E(T('collect_p'))}</p></div>
<div class="btns"><a class="btn" href="{KAKAO}/chat" target="_blank" rel="noopener">{E(T('kakao_btn'))}</a><a class="btn line" href="buy.html">{E(T('buy_btn'))}</a></div>
</div></div>'''

def visit_block():
    return f'''<div class="wrap"><section class="visit">
<div><h2 style="font-size:1.45rem;margin-bottom:18px">{E(T('visit'))}</h2>
<dl><dt>{E(T('place'))}</dt><dd>{T('place_v')}</dd>
<dt>{E(T('hours'))}</dt><dd>{E(T('hours_v'))}</dd>
<dt>{E(T('park'))}</dt><dd>{E(T('park_v'))}</dd>
<dt>{E(T('also'))}</dt><dd>{E(T('also_v'))}</dd>
<dt>{E(T('contact'))}</dt><dd>{E(T('contact_v'))}</dd></dl></div>
<div style="display:grid;gap:12px;align-content:end"><p class="muted">{E(T('visit_p'))}</p>
<div class="btns"><a class="btn" href="{NAVER_MAP}" target="_blank" rel="noopener">{E(T('nmap'))}</a><a class="btn line" href="{KAKAO_MAP}" target="_blank" rel="noopener">{E(T('kmap'))}</a></div></div>
</section></div>'''

OUT = HERE
def write(name, s): open(os.path.join(OUT, name), 'w', encoding='utf-8').write(s)

def index():
    now = EXHIBITIONS[0]
    ld = {"@context": "https://schema.org", "@type": "ArtGallery", "name": "신불당아트센터 M갤러리", "alternateName": "M Gallery at Shinbuldang Art Center",
          "url": BASE, "telephone": "+82-1533-8771", "isAccessibleForFree": True, "openingHours": "Mo-Su 10:00-20:00",
          "address": {"@type": "PostalAddress", "streetAddress": "불당34길 3-16 2층", "addressLocality": "천안시 서북구", "addressRegion": "충청남도", "addressCountry": "KR"},
          "sameAs": [KAKAO, "https://www.instagram.com/shinbuldang_artcenter/", ARTSY_GAL]}
    s = head(T('t_home'), T('d_home'), '', ld=ld)
    date = now[3].rstrip(' ~')
    when = date if '–' in date else (f"From {date}" if L == 'en' else f"{date}{T('from_')}")
    hero_t = '공은지 <em>기획전시</em>' if L == 'ko' else E(ex_title(now[2]))
    s += f'''<a class="hero" href="kong.html">
<picture><source media="(max-width:700px)" srcset="{P()}img/install-hands.jpg"><img src="{P()}img/install-room.jpg" alt="{E(ex_title(now[2]))}"></picture>
<div class="over"><div class="wrap"><span class="state">{E(T('now'))}</span><h1>{hero_t}</h1><span class="when">{E(when)} · {E(T('hero_where'))}</span></div></div></a>
<div class="wrap">
<section class="block"><h2>{E(T('exh'))} <a class="more" href="exhibitions.html">{E(T('more'))}</a></h2>
<div class="ex-grid">{ex_card(EXHIBITIONS[0])}{ex_card(EXHIBITIONS[4])}</div></section>
<section class="block"><h2>{E(T('artists'))} <a class="more" href="artists.html">{E(T('more'))}</a></h2>
<div class="names">{''.join(name_card(a) for a in ARTISTS)}</div></section>
<section class="block"><h2>{E(T('scene'))} <a class="more" href="https://www.instagram.com/shinbuldang_artcenter/" target="_blank" rel="noopener">{E(T('insta'))}</a></h2>
<div class="strip">{''.join(f'<a href="https://www.instagram.com/shinbuldang_artcenter/" target="_blank" rel="noopener"><img src="{P()}img/{k}.jpg" alt="{E(T("scene"))}" loading="lazy"></a>' for k in STRIP)}</div></section>
</div>
{collect_band()}
{visit_block()}'''
    write('index.html', s + foot())

def artists_page():
    s = head(f"{T('t_artists')} | {T('t_suffix')}", T('d_artists'), 'artists.html', cur='artists.html')
    s += f'<div class="wrap"><section class="block"><h2>{E(T("exclusive"))}</h2><div class="names">{"".join(name_card(a) for a in ARTISTS)}</div></section></div>'
    write('artists.html', s + collect_band() + foot())

def exhibitions_pages():
    cur = [x for x in EXHIBITIONS if x[0] != 'past']; past = [x for x in EXHIBITIONS if x[0] == 'past']
    def tabs(c):
        return (f'<nav class="tabs"><a href="exhibitions.html"' + (' aria-current="page"' if c == 1 else '') + f'>{E(T("tab_now"))}</a>'
                f'<a href="exhibitions-past.html"' + (' aria-current="page"' if c == 2 else '') + f'>{E(T("tab_past"))}</a></nav>')
    s = head(f"{T('t_exh')} | {T('t_suffix')}", T('d_exh'), 'exhibitions.html', cur='exhibitions.html')
    s += f'<div class="wrap">{tabs(1)}<div class="ex-grid">{"".join(ex_card(x) for x in cur)}</div></div>'
    write('exhibitions.html', s + foot())
    s = head(f"{T('t_past')} | {T('t_suffix')}", T('d_past'), 'exhibitions-past.html', cur='exhibitions.html')
    rows = ''.join(f'<li><time>{E(x[3])}</time><span>' + (f'<a href="{OFFICIAL}{x[7]}" target="_blank" rel="noopener">' if x[7] else '') + f'{E(who(x[1]))} · {E(ex_title(x[2]))}' + ('</a>' if x[7] else '') + f' <span class="faint">{E(ex_where(x[4]))}</span></span></li>' for x in past)
    s += f'<div class="wrap">{tabs(2)}<ul class="list">{rows}</ul><p class="faint" style="margin-top:14px"><a href="{OFFICIAL}galleryPast" target="_blank" rel="noopener">{E(T("all_past"))}</a></p></div>'
    write('exhibitions-past.html', s + foot())

def artist_page(a):
    aid = a['id']; works = W.get(aid, [])
    nm = aname(aid)
    ld = {"@context": "https://schema.org", "@type": "Person", "name": nm, "affiliation": {"@type": "ArtGallery", "name": "M Gallery, Shinbuldang Art Center"}}
    title = f"{nm} | {T('t_artist_suffix')}"
    desc = f"{T('t_artist_suffix')} {nm}. {afield(aid)}."
    img = f'img/{aid}-{a["rep"]:02d}.jpg' if a['rep'] else 'img/install-room.jpg'
    s = head(title, desc, f'{aid}.html', cur='artists.html', image=img, ld=ld)
    mine = [x for x in EXHIBITIONS if aid in x[5]]
    sub = [('#about', T('about'))] + ([('#works', f"{T('works')} {len(works)}")] if works else []) + ([('#exhibitions', T('exh'))] if mine else []) + [('#cv', T('cv'))]
    second = a['en'].upper() if L == 'ko' else A[aid]['ko']
    s += f'<div class="wrap a-head"><h1>{E(nm)}<span>{E(second)}</span></h1></div>'
    s += '<nav class="subnav"><div class="wrap">' + ''.join(f'<a href="{h}">{E(t)}</a>' for h, t in sub) + '</div></nav><div class="wrap">'
    if a['rep']:
        key = f'{aid}-{a["rep"]:02d}'; w, h = DIMS[key]
        s += f'<div class="feature"><img src="{P()}img/{key}.jpg" width="{w}" height="{h}" alt="{E(nm)} — {E(work(aid, a["rep"])[0])}"></div>'
    side = f'<p class="faint">{E(afield(aid))}</p>'
    if a['insta']: side += f'<p class="faint">{E(T("insta_l"))} <a href="https://www.instagram.com/{a["insta"]}/" target="_blank" rel="noopener">@{a["insta"]}</a></p>'
    side += f'<div class="btns" style="margin-top:6px"><button class="btn" type="button" data-ask="{E(nm)}">{E(T("ask_artist"))}</button></div>'
    if L != 'ko' and aid in ARTSY:
        side += f'<p style="margin-top:10px"><a class="btn line" href="{ARTSY[aid]}" target="_blank" rel="noopener">{E(ARTSY_T[L])} ↗</a></p>'
    second_intro = f'<p class="en">{E(ARTIST_T[aid]["en"][2])}</p>' if L == 'ko' else ''
    s += f'<section class="about" id="about" style="scroll-margin-top:140px"><div style="display:grid;gap:14px"><p>{E(aintro(aid))}</p>{second_intro}</div><div class="side">{side}</div></section>'
    if works:
        s += f'<section class="block" id="works" style="scroll-margin-top:140px"><div class="viewbar"><h2>{E(T("works"))}</h2><span class="faint">{E(T("tap"))}</span></div><div class="tiles">'
        s += ''.join(tile(aid, i + 1) for i in range(len(works))) + '</div></section>'
    else:
        s += f'<section class="block"><p class="muted">{E(T("preparing"))}</p></section>'
    if mine:
        rows = ''.join(f'<li><time>{E(x[3])}</time><span>' + (f'<a href="{OFFICIAL}{x[7]}" target="_blank" rel="noopener">' if x[7] else '') + f'{E(ex_title(x[2]))}' + ('</a>' if x[7] else '') + f' <span class="faint">{E(ex_where(x[4]))}</span></span></li>' for x in mine)
        s += f'<section class="block" id="exhibitions" style="scroll-margin-top:140px"><h2>{E(T("mg_exh"))}</h2><ul class="list">{rows}</ul></section>'
    def ul(items, cut=5):
        if len(items) > cut:
            return '<ul>' + ''.join(f'<li>{E(x)}</li>' for x in items[:cut]) + '</ul><details><summary>+</summary><ul>' + ''.join(f'<li>{E(x)}</li>' for x in items[cut:]) + '</ul></details>'
        return '<ul>' + ''.join(f'<li>{E(x)}</li>' for x in items) + '</ul>'
    cv = a['cv'] if L == 'ko' else CV_EN[aid]
    s += f'<section class="block" id="cv" style="scroll-margin-top:140px"><h2>{E(T("cv"))}</h2><div class="cv">' + ''.join(f'<div><h3>{E(k if L == "ko" else CV_HEAD[k][L])}</h3>{ul(v)}</div>' for k, v in cv.items()) + '</div></section>'
    s += f'<section class="block"><h2>{E(T("others"))}</h2><div class="names">{"".join(name_card(o) for o in ARTISTS if o["id"] != aid)}</div></section></div>'
    write(f'{aid}.html', s + collect_band() + foot())

def buy_page():
    s = head(f"{T('t_buy')} | {T('t_suffix')}", T('d_buy'), 'buy.html', cur='buy.html')
    steps = ''.join(f'<li><time>{E(a)}</time><span>{E(b)}</span></li>' for a, b in T('steps'))
    s += f'''<div class="wrap"><section class="block"><h2>{E(T('buy_h'))}</h2>
<div class="about" style="padding-top:0"><div style="display:grid;gap:16px"><p>{E(T('buy_p'))}</p><ul class="list">{steps}</ul></div>
<div class="side"><p><b>{E(T('rec_h'))}</b></p><p class="muted">{E(T('rec_p'))}</p>
<div class="btns" style="margin-top:6px"><a class="btn" href="{KAKAO}/chat" target="_blank" rel="noopener">{E(T('rec_btn'))}</a><button class="btn line" type="button" data-ask="">{E(T('other_btn'))}</button></div>
</div></div></section>
<section class="block"><h2>{E(T('by_artist'))}</h2><div class="names">{''.join(name_card(a) for a in ARTISTS)}</div></section></div>'''
    write('buy.html', s + foot())

def visit_page():
    s = head(f"{T('t_visit')} | {T('t_suffix')}", T('d_visit'), 'visit.html', cur='visit.html', image='img/install-wide.jpg')
    s += f'<div class="wrap" style="padding-top:24px"><img src="{P()}img/install-wide.jpg" alt="{E(T("sub"))}" style="width:100%"></div>'
    write('visit.html', s + visit_block() + foot())

PAGES = ['', 'artists.html', 'exhibitions.html', 'exhibitions-past.html', 'buy.html', 'visit.html'] + [f'{a["id"]}.html' for a in ARTISTS]

def sitemap():
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for lg in LANGS:
        for p in PAGES: x += f'<url><loc>{BASE}{"" if lg == "ko" else lg + "/"}{p}</loc></url>\n'
    open(os.path.join(HERE, 'sitemap.xml'), 'w', encoding='utf-8').write(x + '</urlset>\n')

def build_lang(lg):
    global L, OUT
    L = lg
    OUT = HERE if lg == 'ko' else os.path.join(HERE, lg)
    os.makedirs(OUT, exist_ok=True)
    index(); artists_page(); exhibitions_pages(); buy_page(); visit_page()
    for a in ARTISTS: artist_page(a)

if __name__ == '__main__':
    for lg in LANGS: build_lang(lg)
    sitemap()
    print('ok', {lg: len([f for f in os.listdir(HERE if lg == 'ko' else os.path.join(HERE, lg)) if f.endswith('.html')]) for lg in LANGS})

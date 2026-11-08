# 신불당아트센터 M갤러리 홈페이지 만들기
# 사용: python -X utf8 mgallery/build.py  → mgallery/*.html 다시 생성
# 구조: 갤러리현대식(메뉴 4개, 첫 화면 전시 사진, 이름 목록, 정사각 회색 칸 작품, 전시 탭)
#     + PKM식(작품 한 점씩 크게 넘겨 보기 + 작품마다 문의, 한·영 소개, 작가별 전시 목록)
# 작품 목록 = works.json (작가별 [제목, 재료, 크기, 연도]), 사진 = img/<작가>-NN.jpg 순서대로, 크기 = dims.json
# 사실은 공식 홈페이지(신불당아트센터.com /310 /311 /389)와 대표님 확인값만 쓴다.
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, 'works.json'), encoding='utf-8'))
DIMS = json.load(open(os.path.join(HERE, 'dims.json'), encoding='utf-8'))
BASE = 'https://jmy0567-sketch.github.io/arthall-homepage/mgallery/'
OFFICIAL = 'http://www.xn--ok1b63rk1c60br1eixzmoc.com/'
KAKAO = 'https://pf.kakao.com/_vaDxeX'
NAVER_MAP = 'https://map.naver.com/p/search/%EC%8B%A0%EB%B6%88%EB%8B%B9%EC%95%84%ED%8A%B8%EC%84%BC%ED%84%B0'
KAKAO_MAP = 'https://map.kakao.com/?q=%EC%B2%9C%EC%95%88%20%EB%B6%88%EB%8B%B934%EA%B8%B8%203-16'
NOINDEX = True   # 대표님 OK 받으면 False로 바꾸고 다시 만들기 (검색 공개)
E = html.escape

ARTISTS = [
  dict(id='kong', ko='공은지', en='Eunjee Kong', field='판화 · 회화', rep=23,
       intro='홍익대학교 일반대학원 판화과를 졸업했어요. 실크스크린 판화와 아크릴 회화로 작업하고, 작품이 국립대만미술관·천안시청·호서대학교에 소장되어 있어요.',
       intro_en='Printmaker and painter working in silkscreen and acrylic. MFA in Printmaking, Hongik University. Collections: National Taiwan Museum of Fine Arts, Cheonan City Hall, Hoseo University.',
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
       intro_en='Painter trained in Korean ink painting (Dankook University), working in ink and acrylic on canvas. Grand Prize, Chungnam Art Exhibition (2013). Collections include Cheonan Museum of Art and Cheonan City Hall.',
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
       intro_en='Abstract painter. MA in Fine Arts, Hannam University. 13 solo exhibitions; former juror of the Grand Art Exhibition of Korea. Current series: UNEXPECTEDLY MEETING A MARTIAN.',
       insta='',
       cv={
        '학력': ['한남대학교 미술교육과 졸업', '한남대학교 일반대학원 미술과 석사'],
        '개인전': ['개인전 13회, 국내외 초대전 다수', '2026 박상국 초대전 (신불당아트센터 M갤러리, 천안)'],
        '경력': ['단원미술대상전 심사위원 역임', '대한민국미술대전 심사위원 역임', '대전직할시전 초대작가·심사위원·운영위원 역임', '충남미술대전 초대작가·심사위원·운영위원 역임', '나혜석미술공모전 심사위원 역임', '한남대 회화과·미술과 대학원, 남서울대 강사 역임'],
        '현재': ['창형전, 상형전, 한국미술협회, 한국수채화작가회', '갤러리아 백화점 문화센터 서양화 강사'],
       }),
  dict(id='ko', ko='고성희', en='', field='조각 · 유리공예', rep=None,
       intro='남서울대학교 유리공예 교수이자 조각가예요. 2025년 여름 M갤러리에서 고영환 작가와 2인전 「身體視詩」를 열었어요.',
       intro_en='Sculptor and professor of glass craft at Namseoul University.',
       insta='', cv={'전시': ['2025 조각가 고성희·고영환 身體視詩 (신불당아트센터 M갤러리, 천안)']}),
]
A = {a['id']: a for a in ARTISTS}

# 전시: (상태, 작가 표시, 제목, 기간, 장소, 관련 작가 id들, 사진, 공식 페이지)
EXHIBITIONS = [
  ('지금 전시 중', 'M갤러리 전속 작가', '공은지 기획전시', '2026. 11. 6 ~', '2층 M갤러리 · 무료 관람 · 매일 10:00–20:00', ['kong'], 'install-wide', None),
  ('지난 전시', '그룹전', '다시 모이다: 네 번째 모임', '2026. 10. 1 – 10. 10', 'M갤러리', [], None, 'galleryPast'),
  ('지난 전시', '박상국', '박상국 초대전', '2026. 9. 16 – 9. 28', 'M갤러리', ['park'], None, 'galleryPast'),
  ('지난 전시', '박상국', '박상국 초대전', '2026. 6. 17 – 6. 30', 'M갤러리', ['park'], None, 'galleryPast'),
  ('지난 전시', '이정식 · 공은지', '이쪽과 저쪽', '2025. 9. 24 – 10. 9', 'M갤러리 · 전속작가 2인전', ['yi', 'kong'], None, '337'),
  ('지난 전시', '고성희 · 고영환', '身體視詩', '2025. 8. 1 – 8. 14', 'M갤러리 · 조각 2인전', ['ko'], None, '324'),
  ('지난 전시', '기획전', '여보! 우리집에도 그림 한점 걸까?', '2025. 3. 1 – 4. 15', 'M갤러리 특별 기획전', [], None, '296'),
  ('지난 전시', '그룹전', 'M갤러리 5대작가 특별전', '2024. 9. 9 – 9. 22', 'M갤러리', [], None, '256'),
  ('지난 전시', '이정식', '헤테로토피아', '2024. 8. 26 – 9. 1', 'M갤러리 · 개인전', ['yi'], None, '253'),
  ('지난 전시', '공은지', '3월의 작가 – 공은지 초대전', '2024. 3', 'M스테이션', ['kong'], None, None),
  ('지난 전시', '공은지', '치유의 형태', '2023. 7', 'M갤러리 · 개인전', ['kong'], None, None),
  ('지난 전시', '이정식', 'There', '2023', 'M갤러리 · 개인전', ['yi'], None, None),
]
STRIP = ['install-room', 'install-merge3', 'install-fists', 'install-pastel']

def work(aid, n): return W[aid][n - 1]
def label(aid, n):
    t, med, size, yr = work(aid, n)
    return f"{A[aid]['ko']} 「{t}」 {yr}, {med}, {size}"

def tile(aid, n):
    t, med, size, yr = work(aid, n)
    key = f'{aid}-{n:02d}'; w, h = DIMS[key]; src = f'img/{key}.jpg'
    caphtml = f'<span class="t"><i>{E(t)}</i>, {yr}</span><br><span class="muted">{E(A[aid]["ko"])} · {E(med)} · {E(size)}</span>'
    return (f'<figure class="tile" style="margin:0">'
            f'<button class="sq" type="button" data-set="{aid}" data-src="{src}" data-alt="{E(A[aid]["ko"])} 작가 작품 {E(t)}" data-caphtml="{E(caphtml)}" data-work="{E(label(aid, n))}" aria-label="{E(t)} 크게 보기">'
            f'<img src="{src}" width="{w}" height="{h}" alt="{E(A[aid]["ko"])} 작가 작품 {E(t)}" loading="lazy"></button>'
            f'<figcaption class="cap"><i>{E(t)}</i> <span class="y">{yr}</span><br><span class="y">{E(med)} · {E(size)}</span></figcaption>'
            f'<button class="ask" type="button" data-ask="{E(label(aid, n))}">이 작품 문의 →</button></figure>')

def head(title, desc, path, cur='', image='img/install-room.jpg', ld=None):
    nav = [('artists.html', '작가'), ('exhibitions.html', '전시'), ('buy.html', '작품 구입'), ('visit.html', '오시는 길')]
    navh = ''.join(f'<a href="{h}"' + (' aria-current="page"' if cur == h else '') + f'>{t}</a>' for h, t in nav)
    return f'''<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
{'<meta name="robots" content="noindex">' if NOINDEX else ''}
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="신불당아트센터 M갤러리">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{BASE}{image}"><meta property="og:locale" content="ko_KR">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="assets/style.css">
{f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''}
</head><body>
<header class="top"><div class="wrap">
<a class="logo" href="./"><b><strong>M</strong><i>.</i> GALLERY</b><span>신불당아트센터 M갤러리</span></a>
<nav class="nav" aria-label="메뉴">{navh}</nav>
</div></header>
<main>'''

FOOT = f'''</main>
<footer><div class="wrap">
<p><b>신불당아트센터 M갤러리</b> · 충남 천안시 서북구 불당34길 3-16 신불당아트센터 2층 · 무료 관람 · 매일 10:00–20:00</p>
<p>문의 1533-8771 · 카카오톡 <a href="{KAKAO}" target="_blank" rel="noopener">신불당M갤러리</a> · 인스타그램 <a href="https://www.instagram.com/shinbuldang_artcenter/" target="_blank" rel="noopener">@shinbuldang_artcenter</a> · <a href="{OFFICIAL}" target="_blank" rel="noopener">신불당아트센터</a> · <a href="../">아트홀 대관</a></p>
<p>작품 사진과 정보는 각 작가님 자료예요. 작품 가격은 문의해 주세요.</p>
</div></footer>
<nav class="bar" aria-label="빠른 문의"><button class="main" type="button" data-ask="">작품 문의</button><a href="tel:15338771">전화</a><a href="{NAVER_MAP}" target="_blank" rel="noopener">길찾기</a></nav>
<script src="assets/site.js" defer></script>
</body></html>
'''

def ex_card(x, show_img=True):
    st, who, title, when, where, _, img, link = x
    reps = [A[i] for i in x[5] if A[i]['rep']]
    if img:
        ph = f'<div class="ph"><img src="img/{img}.jpg" alt="{E(title)} 전시 현장" loading="lazy"></div>'
    elif reps:
        ph = '<div class="ph art">' + ''.join(f'<img src="img/{r["id"]}-{r["rep"]:02d}.jpg" alt="{E(r["ko"])} 작가 작품" loading="lazy">' for r in reps[:2]) + '</div>'
    else:
        ph = f'<div class="ph empty">{E(title)}</div>'
    if not show_img: ph = ''
    href = 'kong.html' if (img and 'kong' in x[5]) else (OFFICIAL + link if link else None)
    inner = f'{ph}<div class="ex-meta"><span class="st">{E(st)}</span><span class="ar">{E(who)}</span><span class="ti">{E(title)}</span><span class="dt">{E(when)}<br>{E(where)}</span></div>'
    if href:
        ext = '' if href.endswith('.html') else ' target="_blank" rel="noopener"'
        return f'<a class="ex-card" href="{href}"{ext}>{inner}</a>'
    return f'<div class="ex-card">{inner}</div>'

def name_card(a):
    if a['rep']:
        key = f"{a['id']}-{a['rep']:02d}"
        ph = f'<div class="ph"><img src="img/{key}.jpg" alt="{E(a["ko"])} 작가 대표 작품" loading="lazy"></div>'
    else:
        ph = f'<div class="ph empty">{a["ko"][0]}</div>'
    return f'<a class="name-card" href="{a["id"]}.html">{ph}<div><b>{E(a["ko"])}</b><span>{E(a["en"] or a["field"])}</span></div></a>'

def collect_band():
    return f'''<div class="collect"><div class="wrap">
<div><h2>집에, 가게에, 사무실에 그림 한 점</h2><p class="muted" style="margin-top:6px">예산과 걸 공간 사진을 보내 주시면 M갤러리가 어울리는 작품을 골라 드려요.</p></div>
<div class="btns"><a class="btn" href="{KAKAO}/chat" target="_blank" rel="noopener">카톡으로 상담</a><a class="btn line" href="buy.html">작품 구입 안내</a></div>
</div></div>'''

def write(name, s): open(os.path.join(HERE, name), 'w', encoding='utf-8').write(s)

def visit_block():
    return f'''<div class="wrap"><section class="visit">
<div><h2 style="font-size:1.45rem;margin-bottom:18px">오시는 길</h2>
<dl><dt>장소</dt><dd>신불당아트센터 2층 M갤러리<br>충남 천안시 서북구 불당34길 3-16</dd>
<dt>관람</dt><dd>무료 · 매일 10:00 – 20:00</dd>
<dt>주차</dt><dd>건물 지하주차장 무료 (만차 시 옆 건물 지문사)</dd>
<dt>함께</dt><dd>1층 멜버른커피하우스 · 1층 아트홀</dd>
<dt>문의</dt><dd>1533-8771 · 카카오톡 신불당M갤러리</dd></dl></div>
<div style="display:grid;gap:12px;align-content:end"><p class="muted">그림 보고, 1층에서 커피 한 잔 하고 가세요.</p>
<div class="btns"><a class="btn" href="{NAVER_MAP}" target="_blank" rel="noopener">네이버 지도</a><a class="btn line" href="{KAKAO_MAP}" target="_blank" rel="noopener">카카오맵</a></div></div>
</section></div>'''

def index():
    now = EXHIBITIONS[0]
    ld = {"@context": "https://schema.org", "@type": "ArtGallery", "name": "신불당아트센터 M갤러리", "alternateName": "M Gallery at Shinbuldang Art Center",
          "url": BASE, "telephone": "+82-1533-8771", "isAccessibleForFree": True, "openingHours": "Mo-Su 10:00-20:00",
          "address": {"@type": "PostalAddress", "streetAddress": "불당34길 3-16 2층", "addressLocality": "천안시 서북구", "addressRegion": "충청남도", "addressCountry": "KR"},
          "sameAs": [KAKAO, "https://www.instagram.com/shinbuldang_artcenter/"]}
    s = head('신불당아트센터 M갤러리 | 천안 불당동 무료 전시 · 작품 구입',
             '천안 불당동 신불당아트센터 2층 M갤러리. 전속 작가 공은지·이정식·박상국·고성희의 작품을 무료로 보고, 마음에 드는 작품은 바로 문의하세요.', '', ld=ld)
    s += f'''<a class="hero" href="kong.html">
<picture><source media="(max-width:700px)" srcset="img/install-hands.jpg"><img src="img/install-room.jpg" alt="공은지 기획전시 M갤러리 전시 현장"></picture>
<div class="over"><div class="wrap"><span class="state">{E(now[0])}</span><h1>공은지 <em>기획전시</em></h1><span class="when">{E(now[3].rstrip(' ~'))}부터 · 2층 M갤러리 · 무료 관람</span></div></div></a>
<div class="wrap">
<section class="block"><h2>전시 <a class="more" href="exhibitions.html">전체 보기</a></h2>
<div class="ex-grid">{ex_card(EXHIBITIONS[0])}{ex_card(EXHIBITIONS[4])}</div></section>
<section class="block"><h2>작가 <a class="more" href="artists.html">전체 보기</a></h2>
<div class="names">{''.join(name_card(a) for a in ARTISTS)}</div></section>
<section class="block"><h2>전시 현장 <a class="more" href="https://www.instagram.com/shinbuldang_artcenter/" target="_blank" rel="noopener">인스타그램 →</a></h2>
<div class="strip">{''.join(f'<a href="https://www.instagram.com/shinbuldang_artcenter/" target="_blank" rel="noopener"><img src="img/{k}.jpg" alt="M갤러리 전시 현장" loading="lazy"></a>' for k in STRIP)}</div></section>
</div>
{collect_band()}
{visit_block()}'''
    write('index.html', s + FOOT)

def artists_page():
    s = head('작가 | 신불당아트센터 M갤러리', 'M갤러리 전속 작가 공은지·이정식·박상국·고성희.', 'artists.html', cur='artists.html')
    s += f'<div class="wrap"><section class="block"><h2>전속 작가</h2><div class="names">{"".join(name_card(a) for a in ARTISTS)}</div></section></div>'
    s += collect_band()
    write('artists.html', s + FOOT)

def exhibitions_pages():
    cur = [x for x in EXHIBITIONS if x[0] != '지난 전시']
    past = [x for x in EXHIBITIONS if x[0] == '지난 전시']
    def tabs(c):
        return (f'<nav class="tabs" aria-label="전시 구분"><a href="exhibitions.html"' + (' aria-current="page"' if c == 1 else '') +
                f'>지금 · 예정</a><a href="exhibitions-past.html"' + (' aria-current="page"' if c == 2 else '') + '>지난 전시</a></nav>')
    s = head('전시 | 신불당아트센터 M갤러리', '지금 M갤러리에서 열리는 전시와 다음 전시.', 'exhibitions.html', cur='exhibitions.html')
    s += f'<div class="wrap">{tabs(1)}<div class="ex-grid">{"".join(ex_card(x) for x in cur)}</div></div>'
    write('exhibitions.html', s + FOOT)
    s = head('지난 전시 | 신불당아트센터 M갤러리', 'M갤러리 지난 전시 기록.', 'exhibitions-past.html', cur='exhibitions.html')
    rows = ''.join(f'<li><time>{E(x[3])}</time><span>' + (f'<a href="{OFFICIAL}{x[7]}" target="_blank" rel="noopener">' if x[7] else '') + f'{E(x[1])} · {E(x[2])}' + ('</a>' if x[7] else '') + f' <span class="faint">{E(x[4])}</span></span></li>' for x in past)
    s += f'<div class="wrap">{tabs(2)}<ul class="list">{rows}</ul><p class="faint" style="margin-top:14px"><a href="{OFFICIAL}galleryPast" target="_blank" rel="noopener">2021년부터 모든 지난 전시 보기 →</a></p></div>'
    write('exhibitions-past.html', s + FOOT)

def artist_page(a):
    aid = a['id']; works = W.get(aid, [])
    ld = {"@context": "https://schema.org", "@type": "Person", "name": a['ko'], "jobTitle": "미술 작가",
          "affiliation": {"@type": "ArtGallery", "name": "신불당아트센터 M갤러리"}, "url": f"{BASE}{aid}.html"}
    if a['en']: ld['alternateName'] = a['en']
    title = f'{a["ko"]} {a["en"]}'.strip() + ' | 신불당아트센터 M갤러리 전속 작가'
    desc = f'M갤러리 전속 작가 {a["ko"]}. {a["field"]}. ' + (f'작품 {len(works)}점과 약력, 작품 구입 문의.' if works else '약력과 작품 문의.')
    img = f'img/{aid}-{a["rep"]:02d}.jpg' if a['rep'] else 'img/install-room.jpg'
    s = head(title, desc, f'{aid}.html', cur='artists.html', image=img, ld=ld)
    mine = [x for x in EXHIBITIONS if aid in x[5]]
    sub = [('#about', '소개')] + ([('#works', f'작품 {len(works)}')] if works else []) + ([('#exhibitions', '전시')] if mine else []) + [('#cv', '약력')]
    s += f'<div class="wrap a-head"><h1>{E(a["ko"])}<span>{E(a["en"].upper())}</span></h1></div>'
    s += '<nav class="subnav" aria-label="작가 메뉴"><div class="wrap">' + ''.join(f'<a href="{h}">{t}</a>' for h, t in sub) + '</div></nav>'
    s += '<div class="wrap">'
    if a['rep']:
        key = f'{aid}-{a["rep"]:02d}'; w, h = DIMS[key]
        s += f'<div class="feature"><img src="img/{key}.jpg" width="{w}" height="{h}" alt="{E(a["ko"])} 작가 대표 작품 {E(work(aid, a["rep"])[0])}"></div>'
    side = f'<p class="faint">{E(a["field"])}</p>'
    if a['insta']: side += f'<p class="faint">인스타그램 <a href="https://www.instagram.com/{a["insta"]}/" target="_blank" rel="noopener">@{a["insta"]}</a></p>'
    side += f'<div class="btns" style="margin-top:6px"><button class="btn" type="button" data-ask="{E(a["ko"])} 작가 작품">이 작가 작품 문의</button></div>'
    s += f'<section class="about" id="about" style="scroll-margin-top:110px"><div style="display:grid;gap:14px"><p>{E(a["intro"])}</p><p class="en">{E(a["intro_en"])}</p></div><div class="side">{side}</div></section>'
    if works:
        s += f'<section class="block" id="works" style="scroll-margin-top:110px"><div class="viewbar"><h2>작품</h2><span class="faint">누르면 한 점씩 크게 넘겨 볼 수 있어요</span></div><div class="tiles">'
        s += ''.join(tile(aid, i + 1) for i in range(len(works))) + '</div></section>'
    else:
        s += '<section class="block"><p class="muted">작품 사진과 자세한 약력을 준비하고 있어요. 작품이 궁금하시면 먼저 문의해 주세요.</p></section>'
    if mine:
        rows = ''.join(f'<li><time>{E(x[3])}</time><span>' + (f'<a href="{OFFICIAL}{x[7]}" target="_blank" rel="noopener">' if x[7] else '') + f'{E(x[2])}' + ('</a>' if x[7] else '') + f' <span class="faint">{E(x[4])}</span></span></li>' for x in mine)
        s += f'<section class="block" id="exhibitions" style="scroll-margin-top:110px"><h2>M갤러리 전시</h2><ul class="list">{rows}</ul></section>'
    def ul(items, cut=5):
        if len(items) > cut:
            return '<ul>' + ''.join(f'<li>{E(x)}</li>' for x in items[:cut]) + '</ul><details><summary>더 보기</summary><ul>' + ''.join(f'<li>{E(x)}</li>' for x in items[cut:]) + '</ul></details>'
        return '<ul>' + ''.join(f'<li>{E(x)}</li>' for x in items) + '</ul>'
    s += '<section class="block" id="cv" style="scroll-margin-top:110px"><h2>약력</h2><div class="cv">' + ''.join(f'<div><h3>{E(k)}</h3>{ul(v)}</div>' for k, v in a['cv'].items()) + '</div></section>'
    s += f'<section class="block"><h2>다른 전속 작가</h2><div class="names">{"".join(name_card(o) for o in ARTISTS if o["id"] != aid)}</div></section></div>'
    s += collect_band()
    write(f'{aid}.html', s + FOOT)

def buy_page():
    s = head('작품 구입 | 신불당아트센터 M갤러리', 'M갤러리 전속 작가 작품 구입 상담. 예산과 공간에 맞춰 작품을 골라 드려요.', 'buy.html', cur='buy.html')
    s += f'''<div class="wrap"><section class="block"><h2>작품 구입</h2>
<div class="about" style="padding-top:0"><div style="display:grid;gap:16px">
<p>M갤러리 전속 작가의 작품은 모두 구입 상담을 받을 수 있어요. 가격은 작품마다 달라서 문의해 주시면 바로 안내해 드려요.</p>
<ul class="list"><li><time>1. 작품 고르기</time><span>작가 페이지에서 마음에 드는 작품의 <b>「이 작품 문의」</b>를 누르세요.</span></li>
<li><time>2. 상담</time><span>카톡·전화·톡톡으로 가격과 크기를 안내해 드려요.</span></li>
<li><time>3. 직접 보기</time><span>2층 M갤러리에서 실제 작품을 보고 정하실 수 있어요. (무료 관람, 매일 10:00–20:00)</span></li></ul>
</div><div class="side">
<p><b>공간에 맞는 그림 추천</b></p><p class="muted">걸 곳 사진 한 장과 예산을 보내 주시면 어울리는 작품을 골라 드려요. 집, 카페, 병원, 사무실 모두 좋아요.</p>
<div class="btns" style="margin-top:6px"><a class="btn" href="{KAKAO}/chat" target="_blank" rel="noopener">카톡으로 추천받기</a><button class="btn line" type="button" data-ask="">다른 방법으로 문의</button></div>
</div></div></section>
<section class="block"><h2>작가별로 보기</h2><div class="names">{''.join(name_card(a) for a in ARTISTS)}</div></section></div>'''
    write('buy.html', s + FOOT)

def visit_page():
    s = head('오시는 길 | 신불당아트센터 M갤러리', '천안 불당동 신불당아트센터 2층 M갤러리. 무료 관람, 매일 10:00–20:00, 지하주차장 무료.', 'visit.html', cur='visit.html', image='img/install-wide.jpg')
    s += '<div class="wrap" style="padding-top:24px"><img src="img/install-wide.jpg" alt="신불당아트센터 M갤러리 전시장" style="width:100%"></div>'
    s += visit_block()
    write('visit.html', s + FOOT)

def sitemap():
    pages = ['', 'artists.html', 'exhibitions.html', 'exhibitions-past.html', 'buy.html', 'visit.html'] + [f'{a["id"]}.html' for a in ARTISTS]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{BASE}{p}</loc></url>\n' for p in pages) + '</urlset>\n'
    write('sitemap.xml', x)

if __name__ == '__main__':
    index(); artists_page(); exhibitions_pages(); buy_page(); visit_page()
    for a in ARTISTS: artist_page(a)
    sitemap()
    print('ok', sorted(f for f in os.listdir(HERE) if f.endswith('.html')))

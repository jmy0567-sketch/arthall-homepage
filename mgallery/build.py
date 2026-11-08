# 신불당아트센터 M갤러리 홈페이지 만들기
# 사용: python -X utf8 mgallery/build.py  → mgallery/*.html 다시 생성
# 작품 목록 = works.json (작가별 [제목, 재료, 크기, 연도], 사진 = img/<작가>-NN.jpg 순서대로)
# 사실은 공식 홈페이지(신불당아트센터.com /310 /311 /389)와 대표님 확인값만 쓴다.
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, 'works.json'), encoding='utf-8'))
DIMS = json.load(open(os.path.join(HERE, 'dims.json'), encoding='utf-8'))
BASE = 'https://jmy0567-sketch.github.io/arthall-homepage/mgallery/'
E = html.escape

ARTISTS = [
  dict(id='kong', ko='공은지', en='Eunjee Kong', field='판화 · 회화',
       short='실크스크린 판화와 아크릴로 사람의 몸과 마음을 그려요.',
       intro='홍익대학교 일반대학원 판화과를 졸업했어요. 실크스크린 판화와 아크릴 회화로 작업하고, 작품이 국립대만미술관·천안시청·호서대학교에 소장되어 있어요.',
       insta='eunjeekong',
       cv={
        '학력': ['2017 홍익대학교 일반대학원 판화과 석사 졸업', '2012 홍익대학교 시각디자인과 졸업'],
        '수상': ['2022 International Biennial Print Exhibit: 2022 R.O.C. 선정', '2022 The 8th NBC MESHTECH Tokyo International Screen Print Biennial 수상 후보', '2021 제1회 필로프린트판화가협회 신진작가공모전 최우수상', '2016 제23회 한국미술국제공모대전 입선', '2016 제36회 현대판화가협회 신인공모전 입선'],
        '개인전': ['2024 3월의 작가 – 공은지 초대전 (신불당아트센터 M스테이션, 천안)', '2023 치유의 형태 (신불당아트센터 M갤러리, 천안)', '2022 RED STARE (갤러리밈, 서울)', '2019 WHERE I STAND (갤러리밈, 서울)'],
        '그룹전': ['2025 이쪽과 저쪽 – 이정식·공은지 2인전 (M갤러리, 천안)', '2024 홍미원 창립전 (리각미술관, 천안)', '2024 청춘찬가 아트페스타 (노들섬갤러리, 서울)', '2024 유유유프로젝트 – 즐거운 미술여행 (임립미술관, 공주)', '2024 하늘 아래 어울림 – 천안작가 42인 초대전 (호서대 아산캠퍼스 갤러리)', '2024 당신의 안뇽 (M갤러리, 천안)', '2023 STAY – 삼원아트스폰서십 5기 그룹전 (삼원갤러리, 서울)', '2022 International Biennial Print Exhibit (국립대만미술관, 타이중)', '2022 The Exchange Exhibition of Korean and Thai Contemporary Prints (한국문화원, 방콕)', '2022 NBC Meshtec Tokyo Screen Print Biennial (도쿄)', '그 외 다수'],
        '작품 소장': ['국립대만미술관, 천안시청, 호서대학교'],
       }),
  dict(id='yi', ko='이정식', en='Jeongsik YI', field='회화 (먹 · 아크릴)',
       short='먹과 아크릴로 산과 길을 그려요.',
       intro='단국대학교에서 동양화를 공부했어요. 먹과 아크릴로 작업하고, 작품이 천안시립미술관·천안시청 등에 소장되어 있어요. 2013년 충남미술대전 대상을 받았어요.',
       insta='jiwoo_yijeongsik',
       cv={
        '학력': ['2018 단국대학교 대학원 회화과 동양화전공 졸업', '2016 단국대학교 예술대학 동양화과 졸업'],
        '수상': ['2018 도솔미술대전 최우수상', '2017 전국대학미술공모전 특선', '2016 문경새재휘호대회 특선', '2015 추사휘호대회 특선', '2014 남농미술대전 특선', '2013 충남미술대전 대상'],
        '개인전': ['2025 Circulation (명동갤러리, 천안)', '2024 헤테로토피아 (M갤러리, 천안)', '2023 There (M갤러리, 천안)', '2022 산수플랫폼展 (갤러리산책, 아산)', '2021 Start over (서북갤러리, 천안) · 유전-교차점 (문화상회다담, 수원)', '2019 Exodus (삼거리갤러리, 천안)', '2017 낮은음자리 (갤러리미술세계, 서울)'],
        '그룹전': ['2026 검은산 붉은몸 2인전 (홍대 아트앤디자인밸리, 서울)', '2026 五人五色, 한곳에 머물다 (헤라스아트, 서울)', '2025 이쪽과 저쪽 2인전 (M갤러리, 천안)', '2024 당신의 안뇽 (M갤러리, 천안)', '2024 Light, Color, Line (몸갤러리, 서울)', '2023 관계도시 유동하는 미래 (천안시립미술관)', '2023 천안비전23 (리각미술관, 천안)', '2018 아시아프 (동대문DDP, 서울) 외 다수'],
        '작품 소장': ['천안시립미술관, 대전검찰청 천안지검, 충청남도 홍성군청, 천안시청'],
        '현재': ['대한민국전통예술전승원 이사, 한국미술협회 청년분과 부위원장'],
       }),
  dict(id='park', ko='박상국', en='Park Sang Kuk', field='회화 (아크릴 추상)',
       short='아크릴 추상 연작 「뜻밖에 화성인을 만나다」를 그려요.',
       intro='한남대학교 미술교육과와 같은 대학 일반대학원 미술과를 졸업했어요. 개인전을 13회 열었고, 대한민국미술대전·단원미술대상전 심사위원을 지냈어요. 지금 연작 제목은 「UNEXPECTEDLY MEETING A MARTIAN(뜻밖에 화성인을 만나다)」이에요.',
       insta='',
       cv={
        '학력': ['한남대학교 미술교육과 졸업', '한남대학교 일반대학원 미술과 석사'],
        '개인전': ['개인전 13회, 국내외 초대전 다수', '2026 박상국 초대전 (신불당아트센터 M갤러리, 천안)'],
        '경력': ['단원미술대상전 심사위원 역임', '대한민국미술대전 심사위원 역임', '대전직할시전 초대작가·심사위원·운영위원 역임', '충남미술대전 초대작가·심사위원·운영위원 역임', '나혜석미술공모전 심사위원 역임', '한남대 회화과·미술과 대학원, 남서울대 강사 역임'],
        '현재': ['창형전, 상형전, 한국미술협회, 한국수채화작가회', '갤러리아 백화점 문화센터 서양화 강사'],
       }),
  dict(id='ko', ko='고성희', en='', field='조각 · 유리공예',
       short='남서울대학교 유리공예 교수, 조각가예요.',
       intro='남서울대학교 유리공예 교수이자 조각가예요. 2025년 여름 M갤러리에서 고영환 작가와 2인전 「身體視詩(신체시시)」를 열었어요.',
       insta='', cv={'전시': ['2025 조각가 고성희·고영환 身體視詩 (신불당아트센터 M갤러리, 천안)']}),
]
A = {a['id']: a for a in ARTISTS}

NOW = dict(artist='kong', title='공은지 기획전시', en='KONG EUN JEE EXHIBITION', img='kong-23',
           period='2026. 11. 6 ~', place='2층 신불당아트센터 M갤러리', hours='매일 10:00 – 20:00', fee='무료 관람')

ARCHIVE = [
  ('2026. 11. 6 ~', '공은지 기획전시 (지금 전시 중)', None),
  ('2026. 10. 1 – 10. 10', '다시 모이다: 네 번째 모임', 'galleryPast'),
  ('2026. 9. 16 – 9. 28', '박상국 초대전', 'galleryPast'),
  ('2026. 6. 17 – 6. 30', '박상국 초대전', 'galleryPast'),
  ('2025. 9. 24 – 10. 9', 'M갤러리 전속작가 이정식·공은지 2인전 「이쪽과 저쪽」', '337'),
  ('2025. 8. 1 – 8. 14', '조각가 고성희·고영환 「身體視詩」', '324'),
  ('2025. 3. 1 – 4. 15', 'M갤러리 특별 기획전 「여보! 우리집에도 그림 한점 걸까?」', '296'),
  ('2024. 9. 9 – 9. 22', 'M갤러리 5대작가 특별전', '256'),
  ('2024. 8. 26 – 9. 1', '이정식 개인전 「헤테로토피아」', '253'),
  ('2024. 3', '3월의 작가 – 공은지 초대전 (M스테이션)', None),
  ('2023. 7', '공은지 개인전 「치유의 형태」', None),
  ('2023', '이정식 개인전 「There」', None),
]
OFFICIAL = 'http://www.xn--ok1b63rk1c60br1eixzmoc.com/'

# 첫 화면에 고른 작품 (사진 번호). 누드가 강한 작품은 첫 화면에서 뺐다.
PICKS = [('kong', 20), ('yi', 3), ('park', 8), ('kong', 21), ('yi', 13), ('park', 3), ('kong', 18), ('yi', 4), ('park', 9)]

def work(aid, n):
    t, med, size, yr = W[aid][n - 1]
    return t, med, size, yr

def work_label(aid, n):
    t, med, size, yr = work(aid, n)
    return f"{A[aid]['ko']} 「{t}」 {yr}, {med}, {size}"

def figure(aid, n, show_artist=False, lazy=True):
    t, med, size, yr = work(aid, n)
    key = f'{aid}-{n:02d}'
    w, h = DIMS[key]
    src = f'img/{key}.jpg'
    label = work_label(aid, n)
    by = f'<span class="by">{E(A[aid]["ko"])} · </span>' if show_artist else ''
    return (f'<figure class="work">'
            f'<button class="pic" type="button" data-view="{src}" data-cap="{E(label)}" data-work="{E(label)}" aria-label="{E(t)} 크게 보기">'
            f'<img src="{src}" width="{w}" height="{h}" alt="{E(A[aid]["ko"])} 작가 작품 {E(t)}"{" loading=lazy" if lazy else ""}></button>'
            f'<figcaption class="cap">{by}<span class="t">{E(t)}</span>, {yr}<br>{E(med)} · {E(size)}</figcaption>'
            f'<button class="ask" type="button" data-ask="{E(label)}">이 작품 문의 →</button></figure>')

def head(title, desc, path, image='img/kong-23.jpg', extra=''):
    return f'''<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="robots" content="noindex">  <!-- 대표님 OK 전까지 검색 숨김: OK 받으면 이 줄 삭제 -->
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="신불당아트센터 M갤러리">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{BASE}{image}">
<meta property="og:locale" content="ko_KR">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<link rel="stylesheet" href="assets/style.css">
{extra}</head><body>
<header class="top"><div class="wrap">
<a class="brand" href="./"><b>M<i>.</i> GALLERY</b><span>신불당아트센터 M갤러리</span></a>
<nav class="nav" aria-label="메뉴"><a href="./#artists">작가</a><a href="./#works" class="hide-s">작품</a><a href="./#archive">전시</a><a href="./#buy">작품 구입</a><a href="./#visit">오시는 길</a></nav>
</div></header>
<main>'''

FOOT = f'''</main>
<footer><div class="wrap">
<p><b>신불당아트센터 M갤러리</b> · 충남 천안시 서북구 불당34길 3-16 신불당아트센터 2층</p>
<p>문의 1533-8771 · 인스타그램 <a href="https://www.instagram.com/shinbuldang_artcenter/" target="_blank" rel="noopener">@shinbuldang_artcenter</a> · <a href="{OFFICIAL}" target="_blank" rel="noopener">신불당아트센터 홈페이지</a> · <a href="../">아트홀 대관 안내</a></p>
<p class="note">작품 사진과 정보는 각 작가님 제공 자료예요. 작품 가격은 문의해 주세요.</p>
</div></footer>
<nav class="bar" aria-label="빠른 문의"><button class="main" type="button" data-ask="">작품 문의</button><a href="tel:15338771">전화</a><a href="https://map.naver.com/p/search/%EC%8B%A0%EB%B6%88%EB%8B%B9%EC%95%84%ED%8A%B8%EC%84%BC%ED%84%B0" target="_blank" rel="noopener">길찾기</a></nav>
<script src="assets/site.js" defer></script>
</body></html>
'''

def artist_card(a):
    ph = (f'<div class="ph"><img src="img/{a["id"]}-portrait.jpg" alt="{E(a["ko"])} 작가" loading="lazy" width="800" height="800"></div>'
          if os.path.exists(os.path.join(HERE, 'img', f'{a["id"]}-portrait.jpg')) else f'<div class="ph mono" aria-hidden="true">{a["ko"][0]}</div>')
    return (f'<a class="artist-card" href="{a["id"]}.html">{ph}'
            f'<h3>{E(a["ko"])}<span>{E(a["en"]) or "Sculptor"}</span></h3><p>{E(a["field"])} · {E(a["short"])}</p></a>')

VISIT = '''<section id="visit"><div class="wrap visit">
<div><div class="sec-head"><h2>오시는 길</h2></div>
<dl>
<dt>장소</dt><dd>신불당아트센터 2층 M갤러리<br>충남 천안시 서북구 불당34길 3-16</dd>
<dt>관람</dt><dd>무료 · 매일 10:00 – 20:00</dd>
<dt>주차</dt><dd>건물 지하주차장 무료 (만차 시 옆 건물 지문사)</dd>
<dt>함께</dt><dd>1층 멜버른커피하우스 · 1층 아트홀</dd>
<dt>문의</dt><dd>1533-8771</dd>
</dl></div>
<div style="display:flex;flex-direction:column;gap:12px;justify-content:end">
<p>그림 보고, 1층에서 커피 한 잔 하고 가세요.</p>
<div class="btns"><a class="btn" href="https://map.naver.com/p/search/%EC%8B%A0%EB%B6%88%EB%8B%B9%EC%95%84%ED%8A%B8%EC%84%BC%ED%84%B0" target="_blank" rel="noopener">네이버 지도</a>
<a class="btn line" href="https://map.kakao.com/?q=%EC%B2%9C%EC%95%88%20%EB%B6%88%EB%8B%B934%EA%B8%B8%203-16" target="_blank" rel="noopener">카카오맵</a></div>
</div></div></section>'''

def index():
    now = NOW; k = now['img']; w, h = DIMS[k]
    t = W['kong'][22][0]
    ld = {"@context": "https://schema.org", "@type": "ArtGallery", "name": "신불당아트센터 M갤러리",
          "alternateName": "M Gallery at Shinbuldang Art Center", "url": BASE, "telephone": "+82-1533-8771",
          "isAccessibleForFree": True,
          "address": {"@type": "PostalAddress", "streetAddress": "불당34길 3-16 2층", "addressLocality": "천안시 서북구", "addressRegion": "충청남도", "addressCountry": "KR"},
          "openingHours": "Mo-Su 10:00-20:00"}
    s = head('신불당아트센터 M갤러리 | 천안 불당동 무료 전시 · 작품 구입',
             '천안 불당동 신불당아트센터 2층 M갤러리. 전속 작가 공은지·이정식·박상국·고성희의 작품을 무료로 보고, 마음에 드는 작품은 바로 문의하세요.',
             '', extra=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    s += f'''<div class="wrap now">
<figure><button class="pic" type="button" style="all:unset;cursor:zoom-in;display:block" data-view="img/{k}.jpg" data-cap="{E(work_label('kong',23))}" data-work="{E(work_label('kong',23))}" aria-label="크게 보기"><img src="img/{k}.jpg" width="{w}" height="{h}" alt="공은지 작가 작품 {E(t)}"></button></figure>
<div class="txt">
<p class="live">지금 전시 중</p>
<h1>{E(now['title'])}<small>{E(now['en'])}</small></h1>
<p>M갤러리 전속 작가 공은지의 판화와 회화를 만나 보세요.</p>
<dl class="facts"><dt>기간</dt><dd>{E(now['period'])}</dd><dt>장소</dt><dd>{E(now['place'])}</dd><dt>시간</dt><dd>{E(now['hours'])}</dd><dt>관람료</dt><dd>{E(now['fee'])}</dd></dl>
<div class="btns"><a class="btn" href="kong.html">작품 보러 가기</a><a class="btn line" href="#visit">오시는 길</a></div>
</div></div>
<section id="artists" style="border-top:1px solid var(--line)"><div class="wrap">
<div class="sec-head"><div><p class="label">Artists</p><h2>M갤러리 전속 작가</h2></div></div>
<div class="artists">{''.join(artist_card(a) for a in ARTISTS)}</div>
</div></section>
<section id="works" style="padding-top:8px"><div class="wrap">
<div class="sec-head"><div><p class="label">Works</p><h2>작품</h2></div><p class="note">사진을 누르면 크게 보여요.</p></div>
<div class="works">{''.join(figure(a, n, show_artist=True) for a, n in PICKS)}</div>
</div></section>
<section id="buy" class="buy"><div class="wrap">
<div style="display:grid;gap:14px"><p class="label" style="color:#9a9ca0">Collect</p>
<h2>집에, 가게에, 사무실에<br>그림 한 점 걸어 보세요</h2>
<p>예산과 걸 공간(사진 한 장이면 충분해요)을 알려 주시면 M갤러리가 어울리는 작품을 골라 드려요.</p></div>
<div style="display:grid;gap:18px"><ul><li>작품 구입 상담 (가격은 문의해 주세요)</li><li>병원·카페·사무실 공간에 맞춘 작품 추천</li><li>선물용 그림 상담</li><li>작가와의 만남·작업 의뢰 문의</li></ul>
<div class="btns"><button class="btn" type="button" data-ask="">작품 구입 상담하기</button><a class="btn line" href="tel:15338771">전화 1533-8771</a></div></div>
</div></section>
<section id="archive"><div class="wrap">
<div class="sec-head"><div><p class="label">Exhibitions</p><h2>전시 기록</h2></div><a href="{OFFICIAL}galleryPast" target="_blank" rel="noopener">지난 전시 전체 보기 →</a></div>
<ul class="archive">{''.join(f'<li><time>{E(d)}</time>' + (f'<a href="{OFFICIAL}{u}" target="_blank" rel="noopener">{E(n)}</a>' if u else f'<span>{E(n)}</span>') + '</li>' for d, n, u in ARCHIVE)}</ul>
</div></section>
{VISIT}'''
    s += FOOT
    open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(s)

def artist_page(a):
    aid = a['id']; works = W.get(aid, [])
    has_ph = os.path.exists(os.path.join(HERE, 'img', f'{aid}-portrait.jpg'))
    ph = f'<div class="ph"><img src="img/{aid}-portrait.jpg" alt="{E(a["ko"])} 작가" width="800" height="800"></div>' if has_ph else f'<div class="ph mono" aria-hidden="true">{a["ko"][0]}</div>'
    ld = {"@context": "https://schema.org", "@type": "Person", "name": a['ko'], "alternateName": a['en'] or None,
          "jobTitle": "미술 작가", "affiliation": {"@type": "ArtGallery", "name": "신불당아트센터 M갤러리"}, "url": f"{BASE}{aid}.html"}
    img = f'img/{aid}-01.jpg' if works else 'img/kong-23.jpg'
    s = head(f'{a["ko"]} {a["en"]}'.strip() + f' | 신불당아트센터 M갤러리 전속 작가',
             f'M갤러리 전속 작가 {a["ko"]}{("(" + a["en"] + ")") if a["en"] else ""}. {a["short"]} 작품 {len(works)}점과 약력, 작품 구입 문의.' if works else f'M갤러리 전속 작가 {a["ko"]}. {a["short"]}',
             f'{aid}.html', image=img, extra=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    s += f'<div class="wrap"><p class="crumb"><a href="./">M갤러리</a> › <a href="./#artists">전속 작가</a> › {E(a["ko"])}</p>'
    s += f'<div class="ahead">{ph}<div><p class="label">M Gallery Artist · {E(a["field"])}</p><h1>{E(a["ko"])}<span>{E(a["en"].upper() or "SCULPTOR")}</span></h1><p class="intro">{E(a["intro"])}</p>'
    if a.get('insta'):
        s += f'<p class="note" style="margin-top:8px">인스타그램 <a href="https://www.instagram.com/{a["insta"]}/" target="_blank" rel="noopener">@{a["insta"]}</a></p>'
    s += f'<div class="btns" style="margin-top:16px"><button class="btn" type="button" data-ask="{E(a["ko"])} 작가 작품">이 작가 작품 문의</button></div></div></div></div>'
    if works:
        s += f'<section style="padding-top:28px"><div class="wrap"><div class="sec-head"><div><p class="label">Works</p><h2>작품 {len(works)}점</h2></div><p class="note">사진을 누르면 크게 보여요.</p></div><div class="works">'
        s += ''.join(figure(aid, i + 1) for i in range(len(works)))
        s += '</div></div></section>'
    else:
        s += '<section style="padding-top:28px"><div class="wrap"><p class="note">작품 사진과 자세한 약력을 준비하고 있어요. 작품이 궁금하시면 먼저 문의해 주세요.</p></div></section>'
    def ul(items, cut=None):
        if cut and len(items) > cut:
            return '<ul>' + ''.join(f'<li>{E(x)}</li>' for x in items[:cut]) + '</ul><details><summary>더 보기</summary><ul>' + ''.join(f'<li>{E(x)}</li>' for x in items[cut:]) + '</ul></details>'
        return '<ul>' + ''.join(f'<li>{E(x)}</li>' for x in items) + '</ul>'
    s += '<section style="border-top:1px solid var(--line)"><div class="wrap"><div class="sec-head"><div><p class="label">Profile</p><h2>약력</h2></div></div><div class="cv">'
    s += ''.join(f'<div><h3>{E(k)}</h3>{ul(v, 5)}</div>' for k, v in a['cv'].items())
    s += '</div></div></section>'
    others = [o for o in ARTISTS if o['id'] != aid]
    s += f'<section style="border-top:1px solid var(--line)"><div class="wrap"><div class="sec-head"><h2>다른 전속 작가</h2></div><div class="artists">{"".join(artist_card(o) for o in others)}</div></div></section>'
    s += VISIT + FOOT
    open(os.path.join(HERE, f'{aid}.html'), 'w', encoding='utf-8').write(s)

def sitemap():
    urls = [BASE] + [f'{BASE}{a["id"]}.html' for a in ARTISTS]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(HERE, 'sitemap.xml'), 'w', encoding='utf-8').write(x)

if __name__ == '__main__':
    index()
    for a in ARTISTS: artist_page(a)
    sitemap()
    print('ok', [f for f in os.listdir(HERE) if f.endswith('.html')])

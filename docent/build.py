# QR 오디오 도슨트 페이지 + 인쇄용 QR 카드 만들기
# 실행: python docent/build.py
import json, os, html
import qrcode
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(D, "scripts.json"), encoding="utf-8"))
BASE = "https://jmy0567-sketch.github.io/arthall-homepage/docent/"
IMG = "../assets/img/"
ORDER = ["om", "jun", "kim", "park"]

CSS = """
:root{--bg:#f6f1e9;--ink:#2a241d;--sub:#7a6d5e;--line:#e2d8c8;--card:#fffdf9;--gold:#a7834a}
@media (prefers-color-scheme:dark){:root{--bg:#1a1714;--ink:#f1ebe2;--sub:#b3a593;--line:#3a332b;--card:#231f1b;--gold:#d2ad6e}}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--ink)}
body{font-family:'IBM Plex Sans KR',sans-serif;line-height:1.75;-webkit-font-smoothing:antialiased}
.wrap{max-width:560px;margin:0 auto;padding:20px 16px 48px}
.brand{font-size:12px;letter-spacing:.14em;color:var(--sub);text-transform:uppercase}
h1{font-family:'Hahmlet',serif;font-weight:500;font-size:30px;line-height:1.3;margin:10px 0 4px}
.en{font-family:'Hahmlet',serif;color:var(--sub);font-size:15px;margin:0}
.meta{font-size:14px;color:var(--sub);margin:10px 0 18px}
.gal{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px}
.gal img{height:300px;width:auto;border-radius:6px;scroll-snap-align:center;flex:none;max-width:86vw;object-fit:cover}
.player{position:sticky;top:0;z-index:2;background:var(--bg);padding:16px 0 12px;margin-top:14px;border-bottom:1px solid var(--line)}
.row{display:flex;align-items:center;gap:14px}
.play{width:64px;height:64px;border-radius:50%;border:0;background:var(--gold);color:#fff;font-size:24px;flex:none;cursor:pointer}
.play:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.bar{flex:1}.bar input{width:100%;accent-color:var(--gold)}
.time{display:flex;justify-content:space-between;font-size:12px;color:var(--sub)}
.label{font-size:15px;font-weight:600;margin-bottom:2px}
.speed{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:20px;padding:4px 10px;font-size:13px;cursor:pointer}
.script{margin-top:20px}.script p{margin:0 0 14px;font-size:17px;transition:color .3s}
.script p.on{color:var(--gold)}
h2{font-family:'Hahmlet',serif;font-weight:500;font-size:19px;margin:36px 0 12px}
.list a{display:flex;gap:12px;align-items:center;padding:10px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:inherit;text-decoration:none;margin-bottom:8px}
.list img{width:64px;height:64px;object-fit:cover;border-radius:6px;flex:none}
.list b{display:block;font-weight:600}.list span{font-size:13px;color:var(--sub)}
.info{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;font-size:14px;margin-top:24px}
.info a{color:var(--gold)}
footer{font-size:12px;color:var(--sub);margin-top:32px;text-align:center}
"""

HEAD = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@500&family=IBM+Plex+Sans+KR:wght@400;600&display=swap" rel="stylesheet">
<meta property="og:title" content="{title}"><meta property="og:image" content="{og}">
<style>{css}</style></head><body><div class="wrap">"""

TAIL = """<footer>신불당아트센터 · 천안시 서북구 불당34길 3-16 · 1533-8771<br>목소리는 AI 음성으로 만들었습니다.</footer>
</div>
<script type="text/javascript" src="//wcs.pstatic.net/wcslog.js"></script>
<script type="text/javascript">if(!wcs_add) var wcs_add = {};wcs_add["wa"] = "88f1dc14c3c978";if(window.wcs){wcs_do();}</script>
</body></html>"""

JS = """<script>
(function(){
 var a=document.getElementById('au'),b=document.getElementById('pl'),r=document.getElementById('rg'),
     c=document.getElementById('cur'),t=document.getElementById('tot'),sp=document.getElementById('sp'),
     ps=[].slice.call(document.querySelectorAll('.script p')),w=ps.map(function(p){return p.textContent.length}),
     sum=w.reduce(function(x,y){return x+y},0),speeds=[1,1.25,0.85],si=0;
 function f(s){s=Math.floor(s||0);return Math.floor(s/60)+':'+('0'+s%60).slice(-2)}
 a.addEventListener('loadedmetadata',function(){t.textContent=f(a.duration)});
 b.onclick=function(){if(a.paused){a.play()}else{a.pause()}};
 a.addEventListener('play',function(){b.textContent='❚❚';b.setAttribute('aria-label','멈춤')});
 a.addEventListener('pause',function(){b.textContent='▶';b.setAttribute('aria-label','재생')});
 a.addEventListener('timeupdate',function(){
  if(!a.duration)return; t.textContent=f(a.duration); r.value=a.currentTime/a.duration*1000; c.textContent=f(a.currentTime);
  var k=a.currentTime/a.duration*sum,acc=0;
  ps.forEach(function(p,i){var on=k>=acc&&k<acc+w[i];acc+=w[i];p.classList.toggle('on',on&&!a.paused)});
 });
 r.oninput=function(){if(a.duration)a.currentTime=r.value/1000*a.duration};
 sp.onclick=function(){si=(si+1)%speeds.length;a.playbackRate=speeds[si];sp.textContent=speeds[si]+'배속'};
})();
</script>"""


def other_list(cur):
    out = []
    for k in ORDER:
        if k == cur:
            continue
        v = S[k]
        out.append(f'<a href="{k}.html"><img src="{IMG}{v["img"][0]}" alt=""><div><b>{v["artist"]} 「{v["title"]}」</b><span>{v["place"]} · 듣기</span></div></a>')
    return '<div class="list">' + "".join(out) + "</div>"


def page(k):
    v = S[k]
    title = f'{v["artist"]} 「{v["title"]}」 오디오 도슨트 · 신불당아트센터'
    desc = v["lines"][0]
    og = "https://jmy0567-sketch.github.io/arthall-homepage/assets/img/" + v["img"][0]
    h = HEAD.format(title=html.escape(title), desc=html.escape(desc), og=og, css=CSS)
    h += '<div class="brand">신불당아트센터 · 오디오 도슨트</div>'
    h += f'<h1>{v["artist"]}<br>「{v["title"]}」</h1>'
    if v["title_en"]:
        h += f'<p class="en">{html.escape(v["title_en"])}</p>'
    meta = v["place"] + (f' · {v["period"]}' if v["period"] else "")
    h += f'<div class="meta">{meta}</div>'
    h += '<div class="gal">' + "".join(f'<img src="{IMG}{i}" alt="{v["artist"]} 작품 사진" loading="lazy">' for i in v["img"]) + "</div>"
    h += f'''<div class="player"><div class="label">▶ 눌러서 작품 설명 듣기</div><div class="row">
<button class="play" id="pl" aria-label="재생">▶</button>
<div class="bar"><input type="range" id="rg" min="0" max="1000" value="0" aria-label="재생 위치">
<div class="time"><span id="cur">0:00</span><button class="speed" id="sp">1배속</button><span id="tot">0:00</span></div></div></div>
<audio id="au" src="audio/{k}-ko.mp3" preload="metadata"></audio></div>'''
    h += '<div class="script">' + "".join(f"<p>{html.escape(l)}</p>" for l in v["lines"]) + "</div>"
    info = []
    if v["insta"]:
        info.append(f'작가 인스타그램 <a href="https://www.instagram.com/{v["insta"]}/">@{v["insta"]}</a>')
    if k == "park":
        info.append('작품 구입 문의 <a href="tel:15338771">1533-8771</a> (신불당아트센터 M갤러리)')
    else:
        info.append("관람 무료 · 11월 29일까지")
    info.append('1층 멜버른커피하우스에서 커피 한 잔 하고 가세요.')
    info.append('<a href="https://jmy0567-sketch.github.io/arthall-homepage/">신불당아트센터 홈페이지</a> · <a href="https://www.instagram.com/shinbuldang_artcenter/">@shinbuldang_artcenter</a>')
    h += '<div class="info">' + "<br>".join(info) + "</div>"
    h += "<h2>다른 전시도 들어 보세요</h2>" + other_list(k)
    h += JS + TAIL
    open(os.path.join(D, f"{k}.html"), "w", encoding="utf-8").write(h)


def index():
    h = HEAD.format(title="오디오 도슨트 · 신불당아트센터", desc="작품 설명을 목소리로 들어 보세요.",
                    og="https://jmy0567-sketch.github.io/arthall-homepage/assets/img/" + S["om"]["img"][0], css=CSS)
    h += '<div class="brand">신불당아트센터 · 오디오 도슨트</div><h1>작품 설명,<br>귀로 들어 보세요</h1>'
    h += '<div class="meta">듣고 싶은 전시를 누르세요. 한 편에 1분 안쪽이에요.</div>'
    h += '<div class="list">' + "".join(
        f'<a href="{k}.html"><img src="{IMG}{S[k]["img"][0]}" alt=""><div><b>{S[k]["artist"]} 「{S[k]["title"]}」</b><span>{S[k]["place"]}</span></div></a>'
        for k in ORDER) + "</div>"
    h += TAIL
    open(os.path.join(D, "index.html"), "w", encoding="utf-8").write(h)


def qr_card(k):
    """인쇄용 QR 카드 (A6 세로 1240x1748, 300dpi 기준)."""
    v = S[k]
    W, H = 1240, 1748
    im = Image.new("RGB", (W, H), (250, 246, 239))
    d = ImageDraw.Draw(im)
    serif = r"C:\Windows\Fonts\NotoSerifKR-VF.ttf"
    sans = r"C:\Users\USER\.claude\skills\shinbuldang-instagram\assets\fonts\Pretendard-Medium.otf"
    def ctext(y, s, f, fill=(42, 36, 29)):
        w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill)
    ctext(120, "AUDIO DOCENT", ImageFont.truetype(sans, 40), (167, 131, 74))
    ctext(200, "작품 설명 듣기", ImageFont.truetype(serif, 92))
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=2)
    q.add_data(BASE + f"{k}.html?from=qr"); q.make(fit=True)
    qi = q.make_image(fill_color=(42, 36, 29), back_color=(250, 246, 239)).convert("RGB").resize((760, 760), Image.NEAREST)
    im.paste(qi, ((W - 760) // 2, 380))
    ctext(1190, f"{v['artist']} 「{v['title']}」", ImageFont.truetype(serif, 64))
    ctext(1290, "휴대폰 카메라로 비추면 목소리 설명이 나와요", ImageFont.truetype(sans, 42), (122, 109, 94))
    ctext(1350, "이어폰을 끼거나, 작은 소리로 들어 주세요", ImageFont.truetype(sans, 42), (122, 109, 94))
    ctext(1560, "신불당아트센터", ImageFont.truetype(serif, 44), (122, 109, 94))
    os.makedirs(os.path.join(D, "print"), exist_ok=True)
    im.save(os.path.join(D, "print", f"qr-{k}.png"), dpi=(300, 300))


for k in ORDER:
    page(k); qr_card(k)
index()
print("built", ORDER)

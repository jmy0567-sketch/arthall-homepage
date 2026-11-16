"""링크 미리보기(og:image) 카드 만들기 — 사진 + 금색 '톡톡!' 버튼 (대표님 11/16: 그냥 사진인 줄 알 수 있으니 누르게)
python tools/make_og_cards.py  → assets/img/og/*.jpg, mgallery/img/og/*.jpg"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.expanduser(r"~\.claude\skills\shinbuldang-instagram\assets\fonts")
B = os.path.join(FONTS, "Pretendard-Bold.otf")
M = os.path.join(FONTS, "Pretendard-Medium.otf")
S = r"C:\Windows\Fonts\NotoSerifKR-VF.ttf"
GOLD, IVORY = (201, 169, 110), (244, 239, 228)
W, H = 1200, 630

CARDS = [
    # (출력, 원본, 세로 위치 0~1, 작은 줄, 큰 줄, 버튼)
    ("assets/img/og/og-home.jpg", "assets/img/hall-wide.jpg", 0.45, "신불당아트센터 공식 홈페이지", "공연 · 전시 · 대관 · 오시는 길", "톡톡! 홈페이지 열기"),
    ("assets/img/og/og-yearend.jpg", "assets/img/event-ceremony.jpg", 0.5, "신불당아트센터 아트홀", "올해 송년회는 무대가 있는 곳에서", "톡톡! 대관 안내 보기"),
    ("mgallery/img/og/og-index.jpg", "mgallery/img/install-wide.jpg", 0.5, "신불당아트센터 M갤러리", "전속 작가 작품 보기 · 구매 문의", "톡톡! 갤러리 열기"),
    ("mgallery/img/og/og-park.jpg", "assets/img/mgallery-parksangguk-1.jpg", 0.4, "신불당아트센터 M갤러리 전속 작가", "박상국 「뜻밖에 화성인을 만나다」", "톡톡! 작품 보기"),
    ("mgallery/img/og/og-kong.jpg", "mgallery/img/kong-show-2026-2.jpg", 0.5, "신불당아트센터 M갤러리 전속 작가", "공은지 작품 보기 · 구매 문의", "톡톡! 작품 보기"),
    ("mgallery/img/og/og-yi.jpg", "mgallery/img/yi-01.jpg", "fit", "신불당아트센터 M갤러리 전속 작가", "이정식 작품 보기 · 구매 문의", "톡톡! 작품 보기"),
    ("mgallery/img/og/og-buy.jpg", "mgallery/img/install-room.jpg", 0.5, "신불당아트센터 M갤러리", "그림 구매 · 소장 안내", "톡톡! 구매 문의하기"),
]


def card(out, src, cy, small, big, btn):
    im = Image.open(os.path.join(ROOT, src)).convert("RGB")
    if cy == "fit":  # 작품 전체를 어두운 바탕 위에 (작은 사진·흰 바탕 작품용)
        bg = Image.new("RGB", (W, H), (18, 16, 14))
        r = min((W - 80) / im.width, 350 / im.height)
        p = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
        bg.paste(p, ((W - p.width) // 2, 28))
        im = bg
    else:
        r = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * r + 0.5), int(im.height * r + 0.5)), Image.LANCZOS)
        l = (im.width - W) // 2
        t = int((im.height - H) * cy)
        im = im.crop((l, t, l + W, t + H))
    im = im.convert("RGBA")
    g = Image.new("L", (1, H))
    for y in range(H):
        g.putpixel((0, y), int(max(0, (y - H * 0.42) / (H * 0.58)) * 235))
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 255)); shade.putalpha(g.resize((W, H)))
    im = Image.alpha_composite(im, shade)
    d = ImageDraw.Draw(im)
    f1, f3 = ImageFont.truetype(M, 30), ImageFont.truetype(B, 38)
    size = 54
    while True:
        f2 = ImageFont.truetype(S, size)
        if d.textlength(big, font=f2) <= W - 120 or size <= 36:
            break
        size -= 2
    d.text((60, 412), small, font=f1, fill=GOLD)
    d.text((60, 454), big, font=f2, fill=IVORY)
    txt = btn + "  →"
    tw = d.textlength(txt, font=f3)
    bx1, by0, by1 = W - 56, 540, 606
    bx0 = bx1 - tw - 76
    d.rounded_rectangle((bx0 + 4, by0 + 6, bx1 + 4, by1 + 6), radius=33, fill=(0, 0, 0, 120))
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=33, fill=GOLD)
    d.text((bx0 + 38, by0 + 11), txt, font=f3, fill=(22, 19, 16))
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.convert("RGB").save(path, quality=88, optimize=True)
    print(out)


if __name__ == "__main__":
    for c in CARDS:
        card(*c)

# Draw the 22 November 2026 world-news image (1024x1024 PNG) with PIL.
# Facts checked against 22 November 2026 news reports (EventGraph daily
# brief, Dawn/AFP, Japan Times, Manila Times, Daily Telegraph NZ):
# Ukraine's largest attack of the year (110 missiles, 400+ drones),
# Poland airspace violation, Houthi strikes on Riyadh, Sparta II fire
# in the Baltic, UN killer-robot talks, Bitcoin two-year low, COP31.
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (247, 243, 233)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (24, 48, 84)
TEAL = (14, 110, 105)
GREY = (96, 92, 84)
GOLD = (198, 142, 24)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.text((40, 26), "THE WORLD IN ONE DAY", font=font(SERIF_B, 58), fill=INK)
d.text((984, 44), "No. 327", font=font(SANS, 22), fill=GREY, anchor="ra")
d.line([(40, 104), (W - 40, 104)], fill=INK, width=3)
d.text((40, 116), "SUNDAY  22  NOVEMBER  2026", font=font(SANS_B, 30), fill=RED)
d.text((984, 118), "WORLD MOOD: ON EDGE", font=font(SANS_B, 22), fill=GREY, anchor="ra")
d.line([(40, 160), (W - 40, 160)], fill=INK, width=2)

# ---- lead: Ukraine's largest attack of the year ----
d.text((40, 178), "WAR  ·  KYIV", font=font(SANS_B, 23), fill=RED)
lead_head = ["Ukraine's biggest", "attack of the year"]
y = 210
for line in lead_head:
    d.text((40, y), line, font=font(SERIF_B, 48), fill=INK)
    y += 56
sub = wrap(d, "110 missiles and 400 drones rain down; Zelenskyy calls Putin a \u201ckiller\u201d. Poland reports a Russian cruise missile in its airspace.", font(SANS, 25), 580)
y += 4
for line in sub:
    d.text((40, y), line, font=font(SANS, 25), fill=INK)
    y += 33
for line in wrap(d, "Trump, meanwhile, calls Putin a friend who wants to end the war.", font(SERIF, 23), 580):
    d.text((40, y + 6), line, font=font(SERIF, 23), fill=GREY)
    y += 30

# lead graphic: the attack in numbers on a navy panel
d.rectangle([(640, 178), (984, 470)], fill=NAVY)
d.text((662, 192), "THE ATTACK IN NUMBERS", font=font(SANS_B, 20), fill=(150, 175, 210))
rows = [("MISSILES", "110"), ("DRONES", "400+"), ("CIVILIANS", "DOZENS"),
        ("POLAND", "BREACH"), ("KYIV", "BLACKOUTS")]
yy = 224
for name, val in rows:
    d.text((662, yy), name, font=font(SANS_B, 24), fill=(255, 255, 255))
    d.text((962, yy), val, font=font(SANS_B, 24), fill=(255, 120, 120), anchor="ra")
    yy += 34
# rising alarm bars
bars = [(662, 452), (730, 442), (790, 448), (850, 428), (962, 408)]
d.line(bars, fill=(255, 120, 120), width=5, joint="curve")
d.polygon([(962, 408), (940, 404), (956, 424)], fill=(255, 120, 120))
d.line([(40, 492), (W - 40, 492)], fill=INK, width=2)

# ---- story grid (3 columns x 2 rows) ----
def icon_bolt(x, y, s):
    pts = [(x + s * 0.55, y), (x + s * 0.2, y + s * 0.55), (x + s * 0.45, y + s * 0.55),
           (x + s * 0.35, y + s), (x + s * 0.8, y + s * 0.45), (x + s * 0.55, y + s * 0.45)]
    d.polygon(pts, fill=GOLD)


def icon_flame(x, y, s):
    d.ellipse([(x + 6, y + s // 2), (x + s - 6, y + s - 4)], outline=RED, width=4)
    d.polygon([(x + s // 2, y + 2), (x + s - 8, y + s // 2 + 6), (x + s // 2, y + s - 8),
               (x + 8, y + s // 2 + 6)], fill=RED)


def icon_ship(x, y, s):
    d.polygon([(x + 6, y + s - 16), (x + s - 6, y + s - 16), (x + s - 14, y + s - 2),
               (x + 14, y + s - 2)], fill=NAVY)
    d.rectangle([(x + s // 2 - 2, y + 4), (x + s // 2 + 2, y + s - 18)], fill=NAVY)
    d.polygon([(x + s // 2 + 2, y + 6), (x + s - 8, y + s - 20), (x + s // 2 + 2, y + s - 20)],
              fill=RED)


def icon_robot(x, y, s):
    d.rectangle([(x + 8, y + 8), (x + s - 8, y + s - 8)], outline=NAVY, width=4)
    d.ellipse([(x + 14, y + 16), (x + 22, y + 24)], fill=NAVY)
    d.ellipse([(x + s - 22, y + 16), (x + s - 14, y + 24)], fill=NAVY)
    d.line([(x + 14, y + s - 14), (x + s - 14, y + s - 14)], fill=NAVY, width=4)


def icon_coin(x, y, s):
    d.ellipse([(x + 6, y + 6), (x + s - 6, y + s - 6)], outline=GOLD, width=4)
    d.text((x + s // 2, y + s // 2 - 14), "$", font=font(SANS_B, 26), fill=GOLD, anchor="ma")


def icon_leaf(x, y, s):
    d.ellipse([(x + 6, y + 6), (x + s - 6, y + s - 6)], outline=(46, 125, 62), width=4)
    d.line([(x + s // 2, y + s - 6), (x + s // 2, y + 10)], fill=(46, 125, 62), width=3)


stories = [
    ("RIYADH", "Houthis strike the Saudi capital",
     "Missiles rain on Riyadh; the coalition says it shot down three.", icon_bolt),
    ("BALTIC", "Russian-linked ship burns",
     "The cargo vessel Sparta II catches fire after a drone strike at sea.", icon_ship),
    ("KILLER ROBOTS", "UN talks end with no deal",
     "Geneva talks on autonomous weapons agree only to keep talking.", icon_robot),
    ("CRYPTO", "Bitcoin hits a two-year low",
     "Bitcoin crashes; FinCEN calls MEXC a money-laundering concern.", icon_coin),
    ("CLIMATE", "Fossil fuels block a deal",
     "COP31 talks stall as the fossil-fuel dispute threatens the accord.", icon_leaf),
    ("ELSEWHERE", "Peru quake, resignations",
     "A 6.7 quake hits Peru; Serbia's president quits; Mexico seizes a drug lord.", icon_flame),
]

cw, ch = 304, 196
gx, gy = 40, 508
for i, (kick, head, summ, icon) in enumerate(stories):
    x = gx + (i % 3) * (cw + 8)
    yy = gy + (i // 3) * (ch + 12)
    d.rectangle([(x, yy), (x + cw, yy + ch)], outline=(205, 197, 178), width=2)
    d.text((x + 14, yy + 10), kick, font=font(SANS_B, 18), fill=RED)
    icon(x + cw - 56, yy + 10, 40)
    lines = wrap(d, head, font(SERIF_B, 24), cw - 28)
    ty = yy + 40
    for line in lines[:2]:
        d.text((x + 14, ty), line, font=font(SERIF_B, 24), fill=INK)
        ty += 30
    slines = wrap(d, summ, font(SANS, 17), cw - 28)
    for line in slines[:3]:
        d.text((x + 14, ty + 2), line, font=font(SANS, 17), fill=GREY)
        ty += 22

# ---- footer ----
d.line([(40, 946), (W - 40, 946)], fill=INK, width=2)
d.text((W // 2, 958), "Sunday 22 November 2026  \u00b7  The world in one image",
       font=font(SANS_B, 20), fill=INK, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
print("bytes:", os.path.getsize("entry.png"))

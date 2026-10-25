"""Genera icone e immagine di anteprima (serve Pillow). Va lanciato solo se vuoi rifarle."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "assets"
PAPER, GRID, INK, TEXT, COS, SIN, MARG, MUTED = "#FBFCFE", "#E3EAF4", "#1F3C88", "#22252C", "#C8102E", "#1B7F5A", "#EBA5B0", "#5F6674"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"

def circle_mark(d, cx, cy, r, w, ang=math.radians(60)):
    px, py = cx + r*math.cos(ang), cy - r*math.sin(ang)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=TEXT, width=w)
    d.line([cx, cy, px, py], fill=INK, width=w)
    d.line([px, cy, px, py], fill=SIN, width=int(w*1.4))
    d.line([cx, cy, px, cy], fill=COS, width=int(w*1.4))
    pr = w*1.6
    d.ellipse([px-pr, py-pr, px+pr, py+pr], fill=INK)

def icon(size, name, pad=0.16):
    s = size*4
    im = Image.new("RGB", (s, s), PAPER); d = ImageDraw.Draw(im)
    r = s*(0.5-pad); circle_mark(d, s/2, s/2, r, int(s*0.035))
    im.resize((size, size), Image.LANCZOS).save(A/name)

icon(180, "apple-touch-icon.png"); icon(192, "icon-192.png", 0.2); icon(512, "icon-512.png", 0.2)

W, H, k = 1200, 630, 2
im = Image.new("RGB", (W*k, H*k), PAPER); d = ImageDraw.Draw(im)
for x in range(0, W*k, 44): d.line([x, 0, x, H*k], fill=GRID, width=2)
for y in range(0, H*k, 44): d.line([0, y, W*k, y], fill=GRID, width=2)
d.line([70*k, 0, 70*k, H*k], fill=MARG, width=4*k)
cx, cy, r = 870*k, 315*k, 230*k
d.line([cx-r-40*k, cy, cx+r+40*k, cy], fill="#CAD4E3", width=3*k)
d.line([cx, cy-r-40*k, cx, cy+r+40*k], fill="#CAD4E3", width=3*k)
ang = math.radians(120)
px, py = cx + r*math.cos(ang), cy - r*math.sin(ang)
d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=TEXT, width=4*k)
d.arc([cx-50*k, cy-50*k, cx+50*k, cy+50*k], start=-120, end=0, fill="#B7791F", width=5*k)
d.line([px, cy, px, py], fill=SIN, width=9*k)
d.line([cx, cy, px, cy], fill=COS, width=9*k)
d.line([cx, cy, px, py], fill=INK, width=5*k)
d.ellipse([px-16*k, py-16*k, px+16*k, py+16*k], fill=INK, outline=PAPER, width=5*k)
fb = ImageFont.truetype(SERIF_I, 92*k); fm = ImageFont.truetype(SERIF, 54*k); fs = ImageFont.truetype(SERIF, 40*k)
d.text((115*k, 120*k), "θ = 2π/3", font=fb, fill=INK)
d.text((115*k, 265*k), "cos θ = −1/2", font=fm, fill=COS)
d.text((115*k, 345*k), "sin θ = √3/2", font=fm, fill=SIN)
d.text((115*k, 425*k), "tan θ = −√3", font=fm, fill=TEXT)
im.resize((W, H), Image.LANCZOS).save(A/"og-image.png", optimize=True)
print("ok")

# -*- coding: utf-8 -*-
"""
Sinh asset cho intro sach lat trang:
1. Khung quyen sach mo (1180x680) -> assets/ui/book_frame.png
2. Trang moi "xe khach ve que" 2 frame (400x200) -> assets/intro_pages/03_xe_khach.png
3. Copy 4 tranh intro co san vao assets/intro_pages/ theo thu tu cot truyen
"""
import os, math, random, shutil
from PIL import Image, ImageDraw

random.seed(21)
CLIENT = r"E:\Avatar Farm\AvatarClient"
PAGES = os.path.join(CLIENT, "assets", "intro_pages")
UI = os.path.join(CLIENT, "assets", "ui")
ART = os.path.join(CLIENT, "assets", "art", "intro_game")
os.makedirs(PAGES, exist_ok=True)

# ================= 1. KHUNG QUYEN SACH =================
W, H = 1180, 680
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

LEATHER   = (94, 58, 38)
LEATHER_D = (66, 40, 26)
LEATHER_L = (122, 80, 52)
PAPER     = (243, 232, 205)
PAPER_SH  = (222, 208, 176)
PAPER_EDG = (206, 190, 158)

# Bia da (khoi ngoai cung, bo tron)
d.rounded_rectangle([0, 0, W - 1, H - 1], radius=26, fill=LEATHER_D)
d.rounded_rectangle([6, 6, W - 7, H - 7], radius=22, fill=LEATHER)
# Van da + diem nhan goc
for _ in range(700):
    x, y = random.randrange(8, W - 8), random.randrange(8, H - 8)
    if 46 < x < W - 46 and 34 < y < H - 34:
        continue
    d.point((x, y), fill=random.choice([LEATHER_D, LEATHER_L]))
for cx, cy in [(20, 20), (W - 21, 20), (20, H - 21), (W - 21, H - 21)]:
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(196, 160, 80), outline=(140, 108, 44))

# Chong trang giay (cac lop mep giay)
for i in range(5):
    off = 34 - i * 4
    col = PAPER_EDG if i % 2 == 0 else (216, 200, 168)
    d.rounded_rectangle([46 - i, off, W - 47 + i if False else W - 47, H - off], radius=8, outline=col)
# 2 trang giay chinh
d.rounded_rectangle([46, 30, W - 47, H - 31], radius=8, fill=PAPER)
for _ in range(900):  # van giay nhe
    x, y = random.randrange(50, W - 50), random.randrange(34, H - 34)
    d.point((x, y), fill=random.choice([(238, 226, 196), (248, 240, 218)]))

# Gay sach giua: bong toi + duong chi khau
cx = W // 2
for i in range(26):
    a = int(70 * (1 - i / 26))
    d.line([cx - i, 32, cx - i, H - 33], fill=(120, 100, 70, 0))  # placeholder
# ve bong bang cach chong mau dam dan ve giua
for i in range(30):
    t = 1 - i / 30.0
    col = (
        int(PAPER[0] - 60 * t),
        int(PAPER[1] - 58 * t),
        int(PAPER[2] - 55 * t),
    )
    d.line([cx - i, 34, cx - i, H - 35], fill=col)
    d.line([cx + i, 34, cx + i, H - 35], fill=col)
for y in range(60, H - 60, 42):  # chi khau
    d.line([cx - 1, y, cx + 1, y + 12], fill=(150, 128, 96))

# Bong trang giay sat mep trong
d.rounded_rectangle([46, 30, W - 47, H - 31], radius=8, outline=PAPER_SH, width=2)

# Ruy bang danh dau trang (do phai)
d.polygon([(W - 120, 30), (W - 92, 30), (W - 92, 96), (W - 106, 82), (W - 120, 96)],
          fill=(178, 62, 48), outline=(130, 42, 32))

img.save(os.path.join(UI, "book_frame.png"))
print("book_frame.png", img.size)

# ================= 2. TRANG "XE KHACH VE QUE" (2 frame 200x200) =================
def draw_bus_scene(d, ox, frame):
    # --- bau troi binh minh: gradient ---
    for y in range(0, 96):
        t = y / 96.0
        col = (
            int(120 + t * (250 - 120)),
            int(150 + t * (196 - 150)),
            int(198 + t * (150 - 198)),
        )
        d.line([ox, y, ox + 199, y], fill=col)
    # mat troi som
    sun_y = 58
    d.ellipse([ox + 138, sun_y - 16, ox + 170, sun_y + 16], fill=(255, 226, 150))
    d.ellipse([ox + 143, sun_y - 11, ox + 165, sun_y + 11], fill=(255, 244, 200))
    # may
    for mx, my, mw in [(20, 26, 40), (90, 14, 30), (150, 34, 26)]:
        m = mx + (frame * 1)  # may troi cham theo frame
        d.ellipse([ox + m, my, ox + m + mw, my + 10], fill=(255, 250, 238, 200))
        d.ellipse([ox + m + 8, my - 5, ox + m + mw - 6, my + 7], fill=(255, 252, 244, 220))
    # chim bay
    for bx, by in [(52, 30), (63, 25), (74, 32)]:
        yy = by + (1 if frame else 0)
        d.arc([ox + bx, yy, ox + bx + 6, yy + 4], 200, 340, fill=(70, 60, 70))
        d.arc([ox + bx + 5, yy, ox + bx + 11, yy + 4], 200, 340, fill=(70, 60, 70))
    # --- nui xa ---
    d.polygon([(ox, 96), (ox + 40, 62), (ox + 90, 96)], fill=(96, 118, 128))
    d.polygon([(ox + 60, 96), (ox + 130, 52), (ox + 200, 96)], fill=(80, 104, 116))
    d.polygon([(ox + 130, 96), (ox + 180, 70), (ox + 200, 82), (ox + 200, 96)], fill=(96, 118, 128))
    # --- dong lua (cac dai mau) ---
    bands = [(96, 112, (150, 176, 88)), (112, 128, (128, 160, 74)), (128, 142, (168, 188, 96))]
    for y0, y1, col in bands:
        d.rectangle([ox, y0, ox + 199, y1], fill=col)
        for _ in range(40):
            x = random.randrange(0, 200)
            y = random.randrange(y0, y1)
            d.point((ox + x, y), fill=(col[0] - 20, col[1] - 20, col[2] - 16))
    # hang cay chan troi
    for tx in range(4, 200, 22):
        d.ellipse([ox + tx, 88, ox + tx + 12, 98], fill=(58, 88, 66))
        d.rectangle([ox + tx + 5, 96, ox + tx + 7, 100], fill=(70, 52, 36))
    # --- duong nhua ---
    d.polygon([(ox, 200), (ox, 158), (ox + 200, 142), (ox + 200, 200)], fill=(96, 92, 96))
    d.polygon([(ox, 162), (ox + 200, 146), (ox + 200, 150), (ox, 167)], fill=(214, 206, 188))  # vach mep
    # vach dut giua duong (di chuyen theo frame -> cam giac xe chay)
    shift = 10 if frame else 0
    for i in range(6):
        x0 = i * 40 - shift
        d.line([ox + x0, 184 - x0 * 0.08, ox + x0 + 18, 183 - (x0 + 18) * 0.08], fill=(230, 220, 170), width=3)
    # cot dien + day
    for px_, py in [(30, 100), (110, 96), (185, 92)]:
        d.rectangle([ox + px_, py, ox + px_ + 3, py + 52], fill=(74, 60, 48))
        d.line([ox + px_ - 6, py + 6, ox + px_ + 9, py + 6], fill=(74, 60, 48), width=2)
    d.arc([ox + 33, 98, ox + 113, 116], 20, 160, fill=(60, 50, 44))
    d.arc([ox + 113, 94, ox + 188, 112], 20, 160, fill=(60, 50, 44))

    # --- XE KHACH (to, giua trai) ---
    bx, by = 26, 128 + (1 if frame else 0)   # frame 2: xe xoc nhe
    # bong xe
    d.ellipse([ox + bx - 2, by + 46, ox + bx + 126, by + 58], fill=(60, 58, 60, 120))
    # gia noc + hanh ly
    d.rectangle([ox + bx + 10, by - 10, ox + bx + 104, by - 2], fill=(120, 90, 60), outline=(70, 55, 40))
    for lx, lc in [(14, (152, 112, 72)), (36, (100, 122, 92)), (58, (160, 140, 100)), (82, (140, 96, 66))]:
        d.rectangle([ox + bx + lx, by - 9, ox + bx + lx + 18, by - 3], fill=lc, outline=(70, 55, 40))
    # than xe
    d.rounded_rectangle([ox + bx, by - 2, ox + bx + 124, by + 44], radius=7, fill=(246, 246, 242), outline=(52, 58, 74), width=2)
    d.rectangle([ox + bx + 2, by + 26, ox + bx + 122, by + 36], fill=(62, 124, 184))     # soc xanh
    d.rectangle([ox + bx + 2, by + 37, ox + bx + 122, by + 40], fill=(220, 90, 60))      # soc do mong
    # cua so + hanh khach
    for i in range(5):
        wx = bx + 8 + i * 19
        d.rectangle([ox + wx, by + 4, ox + wx + 14, by + 20], fill=(168, 215, 235), outline=(52, 58, 74))
        d.line([ox + wx + 1, by + 6, ox + wx + 10, by + 6], fill=(224, 244, 252))
        if i in (1, 3):  # bong hanh khach
            d.ellipse([ox + wx + 3, by + 9, ox + wx + 10, by + 16], fill=(80, 70, 66))
        if i == 2 and frame:  # nguoi gat gu theo nhip xe
            d.ellipse([ox + wx + 3, by + 11, ox + wx + 10, by + 18], fill=(80, 70, 66))
        elif i == 2:
            d.ellipse([ox + wx + 3, by + 9, ox + wx + 10, by + 16], fill=(80, 70, 66))
    # kinh lai (dau xe ben trai - xe chay sang trai)
    d.rectangle([ox + bx + 3, by + 3, ox + bx + 5 + 0, by + 22], fill=(168, 215, 235))
    # den pha + den hau
    d.rectangle([ox + bx - 1, by + 28, ox + bx + 2, by + 33], fill=(255, 235, 150), outline=(52, 58, 74))
    d.rectangle([ox + bx + 122, by + 28, ox + bx + 125, by + 33], fill=(210, 80, 60), outline=(52, 58, 74))
    # banh xe (hub xoay theo frame)
    for cx_ in (bx + 26, bx + 98):
        d.ellipse([ox + cx_ - 9, by + 36, ox + cx_ + 9, by + 54], fill=(30, 30, 32), outline=(12, 12, 14), width=2)
        d.ellipse([ox + cx_ - 4, by + 41, ox + cx_ + 4, by + 49], fill=(150, 150, 154))
        if frame:
            d.line([ox + cx_ - 3, by + 42, ox + cx_ + 3, by + 48], fill=(90, 90, 94))
        else:
            d.line([ox + cx_ - 3, by + 48, ox + cx_ + 3, by + 42], fill=(90, 90, 94))
    # bien "HA NOI - BAC NINH" (o day chi la bang mau)
    d.rectangle([ox + bx + 44, by - 1, ox + bx + 80, by + 3], fill=(240, 214, 120), outline=(52, 58, 74))
    # khoi po
    if frame:
        d.ellipse([ox + bx + 126, by + 38, ox + bx + 134, by + 44], fill=(200, 200, 200, 160))
        d.ellipse([ox + bx + 133, by + 33, ox + bx + 143, by + 41], fill=(220, 220, 220, 110))
    else:
        d.ellipse([ox + bx + 126, by + 39, ox + bx + 132, by + 44], fill=(210, 210, 210, 140))

img2 = Image.new("RGBA", (400, 200))
d2 = ImageDraw.Draw(img2)
draw_bus_scene(d2, 0, 0)
draw_bus_scene(d2, 200, 1)
img2.save(os.path.join(PAGES, "03_xe_khach.png"))
print("03_xe_khach.png", img2.size)

# ================= 3. COPY 4 TRANH CO SAN THEO THU TU =================
mapping = [
    ("map_1.png", "01_dem_ha_noi.png"),
    ("map_6.png", "02_tin_du.png"),
    ("map_9.png", "04_ve_lang.png"),
    ("map_3.png", "05_phong_cu.png"),
]
for src, dst in mapping:
    shutil.copy(os.path.join(ART, src), os.path.join(PAGES, dst))
    print("copied", dst)
print("DONE")

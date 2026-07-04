# -*- coding: utf-8 -*-
"""
Sinh PNG placeholder cho các asset còn thiếu của Ngày 1-2 ("Về Tới Quê").
Palette Mùa Xuân theo GDD: xanh non, vàng kem, hồng đào, trắng sương.
Chạy:  python tools/gen_placeholders_ngay1_2.py
Output: png_placeholders_ngay1-2/
"""
import os, random
from PIL import Image, ImageDraw

random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), "..", "png_placeholders_ngay1-2")
os.makedirs(OUT, exist_ok=True)

# ---------- Palette Mùa Xuân ----------
GRASS      = (124, 184, 78)
GRASS_LT   = (146, 204, 99)
GRASS_DK   = (105, 163, 66)
GRASS_OUT  = (74, 122, 46)
DIRT       = (176, 137, 104)
DIRT_LT    = (194, 155, 120)
DIRT_DK    = (156, 118, 83)
TILL_DK    = (122, 92, 67)
TILL_WET   = (100, 73, 58)
WATER      = (111, 183, 217)
WATER_LT   = (189, 227, 240)
WOOD       = (138, 106, 72)
WOOD_DK    = (95, 69, 46)
WOOD_OUT   = (58, 47, 35)
CREAM      = (245, 233, 201)
PINK       = (242, 166, 184)
WHITE      = (250, 250, 245)
BAMBOO     = (201, 161, 92)
BAMBOO_DK  = (156, 120, 62)


def new(w, h, bg=(0, 0, 0, 0)):
    img = Image.new("RGBA", (w, h), bg)
    return img, ImageDraw.Draw(img)


def speckle(d, x0, y0, w, h, colors, n):
    for _ in range(n):
        x = x0 + random.randrange(w)
        y = y0 + random.randrange(h)
        d.point((x, y), fill=random.choice(colors))


# ---------- 1. Tileset nền 32x32 (8 tile, sheet 256x32) ----------
def tile_grass(d, ox):
    d.rectangle([ox, 0, ox + 31, 31], fill=GRASS)
    speckle(d, ox, 0, 32, 32, [GRASS_LT, GRASS_DK], 60)
    for _ in range(6):  # nhánh cỏ
        x = ox + random.randrange(2, 29)
        y = random.randrange(4, 28)
        d.line([x, y, x, y - 2], fill=GRASS_DK)


def tile_grass_flower(d, ox):
    tile_grass(d, ox)
    for _ in range(3):  # hoa xuân nhỏ (hồng đào / trắng)
        x = ox + random.randrange(4, 26)
        y = random.randrange(4, 26)
        c = random.choice([PINK, WHITE])
        d.point([(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)], fill=c)
        d.point((x, y), fill=(240, 200, 90))


def tile_dirt(d, ox):
    d.rectangle([ox, 0, ox + 31, 31], fill=DIRT)
    speckle(d, ox, 0, 32, 32, [DIRT_LT, DIRT_DK], 55)


def tile_grass_dirt_edge(d, ox):  # cỏ phía trên, đất phía dưới
    tile_dirt(d, ox)
    d.rectangle([ox, 0, ox + 31, 9], fill=GRASS)
    speckle(d, ox, 0, 32, 9, [GRASS_LT, GRASS_DK], 20)
    for x in range(ox, ox + 32, 3):  # viền cỏ rủ
        d.line([x, 10, x, 10 + (x % 2)], fill=GRASS_DK)


def tile_tilled_dry(d, ox):
    tile_dirt(d, ox)
    for y in range(3, 32, 6):  # luống ngang
        d.line([ox + 1, y, ox + 30, y], fill=TILL_DK)
        d.line([ox + 1, y + 1, ox + 30, y + 1], fill=DIRT_DK)


def tile_tilled_wet(d, ox):
    d.rectangle([ox, 0, ox + 31, 31], fill=TILL_DK)
    speckle(d, ox, 0, 32, 32, [TILL_WET, DIRT_DK], 50)
    for y in range(3, 32, 6):
        d.line([ox + 1, y, ox + 30, y], fill=TILL_WET)
    speckle(d, ox, 0, 32, 32, [(130, 140, 160)], 8)  # ánh nước


def tile_water(d, ox):
    d.rectangle([ox, 0, ox + 31, 31], fill=WATER)
    for _ in range(5):  # sóng lăn tăn
        x = ox + random.randrange(2, 22)
        y = random.randrange(3, 29)
        d.line([x, y, x + random.randrange(4, 9), y], fill=WATER_LT)


def tile_path_stones(d, ox):  # đường đất có đá - lối vào sân
    tile_dirt(d, ox)
    for _ in range(4):
        x = ox + random.randrange(3, 24)
        y = random.randrange(3, 24)
        d.ellipse([x, y, x + 5, y + 3], fill=(168, 162, 150), outline=(120, 115, 105))


img, d = new(256, 32)
for i, fn in enumerate([tile_grass, tile_grass_flower, tile_dirt, tile_grass_dirt_edge,
                        tile_tilled_dry, tile_tilled_wet, tile_water, tile_path_stones]):
    fn(d, i * 32)
img.save(os.path.join(OUT, "tileset_nen_xuan_32.png"))


# ---------- 2. Ruộng 4 trạng thái (128x32) ----------
def plot_weedy(d, ox):  # ô ruộng bỏ hoang - tutorial dọn cỏ
    tile_grass(d, ox)
    for _ in range(5):
        x = ox + random.randrange(3, 26)
        y = random.randrange(6, 28)
        d.line([x, y, x - 2, y - 4], fill=(85, 130, 55))
        d.line([x, y, x, y - 5], fill=(70, 110, 45))
        d.line([x, y, x + 2, y - 4], fill=(85, 130, 55))
    for _ in range(3):
        x = ox + random.randrange(4, 26)
        y = random.randrange(4, 26)
        d.ellipse([x, y, x + 4, y + 3], fill=(150, 145, 135), outline=(110, 105, 98))


def plot_seedling(d, ox):
    tile_tilled_dry(d, ox)
    for gx, gy in [(7, 8), (21, 9), (9, 21), (23, 22)]:
        x, y = ox + gx, gy
        d.line([x, y, x, y - 3], fill=(80, 150, 60))
        d.point([(x - 1, y - 3), (x + 1, y - 3)], fill=(120, 190, 80))
        d.point((x, y - 4), fill=(120, 190, 80))


img, d = new(128, 32)
plot_weedy(d, 0)
tile_tilled_dry(d, 32)
tile_tilled_wet(d, 64)
plot_seedling(d, 96)
img.save(os.path.join(OUT, "ruong_4_trang_thai_32.png"))


# ---------- 3. Props dọn nhà (192x32, nền trong suốt) ----------
img, d = new(192, 32)
# 3.1 mạng nhện (góc trên trái)
ox = 0
web = (222, 222, 222, 200)
for end in [(18, 2), (14, 8), (8, 14), (2, 18)]:
    d.line([ox + 1, 1, ox + end[0], end[1]], fill=web)
d.line([ox + 3, 6, ox + 8, 3], fill=web)
d.line([ox + 5, 11, ox + 13, 5], fill=web)
d.line([ox + 7, 16, ox + 17, 7], fill=web)
# 3.2 đống bụi
ox = 32
d.ellipse([ox + 6, 20, ox + 26, 29], fill=(150, 138, 120), outline=(110, 100, 86))
speckle(d, ox + 8, 21, 16, 7, [(170, 158, 140), (128, 118, 102)], 14)
d.point([(ox + 10, 17), (ox + 16, 15), (ox + 22, 18)], fill=(160, 148, 130, 160))
# 3.3 bụi cỏ dại
ox = 64
for x, y in [(10, 27), (16, 28), (22, 27)]:
    d.line([ox + x, y, ox + x - 3, y - 8], fill=(85, 130, 55))
    d.line([ox + x, y, ox + x, y - 10], fill=(70, 110, 45))
    d.line([ox + x, y, ox + x + 3, y - 8], fill=(85, 130, 55))
    d.line([ox + x, y, ox + x + 1, y - 6], fill=(100, 150, 65))
# 3.4 đống lá khô
ox = 96
d.ellipse([ox + 5, 19, ox + 27, 29], fill=(180, 130, 70), outline=(130, 90, 45))
for _ in range(10):
    x = ox + random.randrange(8, 25)
    y = random.randrange(20, 28)
    d.point([(x, y), (x + 1, y)], fill=random.choice([(205, 155, 85), (150, 100, 50), (190, 120, 60)]))
# 3.5 đống rác (giấy vụn + chai)
ox = 128
d.ellipse([ox + 6, 21, ox + 22, 29], fill=(200, 196, 188), outline=(140, 136, 128))
d.polygon([(ox + 9, 23), (ox + 13, 19), (ox + 16, 24)], fill=WHITE, outline=(160, 156, 148))
d.rectangle([ox + 21, 16, ox + 25, 27], fill=(90, 140, 90), outline=(55, 95, 55))
d.rectangle([ox + 22, 13, ox + 24, 16], fill=(90, 140, 90), outline=(55, 95, 55))
# 3.6 ván gỗ gãy
ox = 160
d.polygon([(ox + 4, 24), (ox + 14, 8), (ox + 18, 10), (ox + 8, 26)], fill=WOOD, outline=WOOD_OUT)
d.polygon([(ox + 16, 14), (ox + 26, 20), (ox + 24, 24), (ox + 14, 18)], fill=WOOD_DK, outline=WOOD_OUT)
d.line([ox + 12, 14, ox + 15, 16], fill=WOOD_OUT)
img.save(os.path.join(OUT, "props_don_nha_32.png"))


# ---------- 4. Hàng rào tre (96x32: nguyên, cột, gãy) ----------
img, d = new(96, 32)
def fence_rail(d, ox, broken=False):
    for y in (10, 20):
        x1 = ox + 31 if not broken else ox + 17
        d.rectangle([ox, y, x1, y + 2], fill=BAMBOO, outline=BAMBOO_DK)
        if broken:
            d.polygon([(ox + 17, y), (ox + 21, y + 1), (ox + 17, y + 2)], fill=BAMBOO_DK)
    for px in (ox + 4, ox + 24) if not broken else (ox + 4,):
        d.rectangle([px, 4, px + 3, 30], fill=BAMBOO, outline=BAMBOO_DK)
        d.line([px + 1, 4, px + 1, 30], fill=(226, 190, 128))
fence_rail(d, 0)
d.rectangle([46, 4, 49, 30], fill=BAMBOO, outline=BAMBOO_DK)  # cột đơn
d.line([47, 4, 47, 30], fill=(226, 190, 128))
fence_rail(d, 64, broken=True)
img.save(os.path.join(OUT, "hang_rao_tre_32.png"))


# ---------- 5. UI: thanh Stamina (3 mức, 96x16 mỗi thanh) ----------
img, d = new(96, 56)
def stamina_bar(d, oy, pct, color):
    d.rounded_rectangle([0, oy, 95, oy + 15], radius=4, fill=(36, 29, 21), outline=(58, 47, 35), width=2)
    w = int(88 * pct)
    if w > 0:
        d.rounded_rectangle([4, oy + 4, 4 + w, oy + 11], radius=2, fill=color)
        d.line([5, oy + 5, 3 + w, oy + 5], fill=tuple(min(255, c + 45) for c in color))
stamina_bar(d, 0, 1.0, (111, 207, 79))
stamina_bar(d, 20, 0.5, (214, 194, 74))
stamina_bar(d, 40, 0.18, (214, 96, 74))
img.save(os.path.join(OUT, "ui_thanh_stamina.png"))

# ---------- 6. UI: hotbar 8 ô ----------
img, d = new(8 * 26 + 2, 30)
for i in range(8):
    x = 2 + i * 26
    sel = (i == 0)
    d.rounded_rectangle([x, 3, x + 23, 26], radius=3,
                        fill=(95, 69, 46), outline=CREAM if sel else WOOD_OUT, width=2)
    d.rectangle([x + 4, 7, x + 19, 22], fill=(70, 51, 34))
img.save(os.path.join(OUT, "ui_hotbar_8_o.png"))

# ---------- 7. UI: hộp thoại + bảng tên ----------
img, d = new(200, 64)
d.rounded_rectangle([0, 12, 199, 63], radius=6, fill=CREAM, outline=WOOD_OUT, width=2)
d.rounded_rectangle([2, 14, 197, 61], radius=5, outline=(214, 190, 148))
d.rounded_rectangle([8, 0, 76, 20], radius=4, fill=(184, 74, 60), outline=WOOD_OUT, width=2)  # bảng tên
d.polygon([(178, 52), (186, 52), (182, 57)], fill=WOOD_OUT)  # mũi tên "tiếp"
img.save(os.path.join(OUT, "ui_hop_thoai.png"))

# ---------- 8. UI: HUD ngày/giờ ----------
img, d = new(80, 26)
d.rounded_rectangle([0, 0, 79, 25], radius=5, fill=CREAM, outline=WOOD_OUT, width=2)
d.ellipse([6, 6, 19, 19], fill=(240, 200, 90), outline=(200, 150, 50))  # mặt trời
for a, b in [((12, 2), (12, 4)), ((12, 21), (12, 23)), ((2, 12), (4, 12)), ((21, 12), (23, 12))]:
    d.line([a, b], fill=(200, 150, 50))
d.rectangle([26, 8, 72, 17], fill=(236, 222, 186))  # chỗ hiện "Ngày 1 - 6:00"
img.save(os.path.join(OUT, "ui_hud_ngay_gio.png"))

# ---------- 9. Emote 16x16 x4 (!, ?, tim, zzz) ----------
MAPS = {
    "chamthan": [
        "......XX........",
        ".....XooX.......",
        ".....XooX.......",
        ".....XooX.......",
        ".....XooX.......",
        ".....XooX.......",
        ".....XooX.......",
        "......XX........",
        ".....XooX.......",
        "......XX........",
    ],
    "hoicham": [
        "....XXXX........",
        "...XooooX.......",
        "...Xo..oX.......",
        "......XoX.......",
        ".....XoX........",
        ".....XoX........",
        "......X.........",
        ".....XoX........",
        "......X.........",
    ],
    "tim": [
        "..XX....XX......",
        ".XppX..XppX.....",
        "XppppXXppppX....",
        "XppppppppppX....",
        ".XppppppppX.....",
        "..XppppppX......",
        "...XppppX.......",
        "....XppX........",
        ".....XX.........",
    ],
    "zzz": [
        ".XXXX...........",
        "...X............",
        "..X.............",
        ".XXXX...........",
        "......XXX.......",
        "........X.......",
        ".......X........",
        "......XXX.......",
        "..........XX....",
        "...........X....",
        "..........XX....",
    ],
}
COLORS = {"X": (58, 47, 35, 255), "o": (240, 200, 90, 255), "p": (232, 106, 130, 255)}
img, _ = new(64, 16)
for i, key in enumerate(["chamthan", "hoicham", "tim", "zzz"]):
    for y, row in enumerate(MAPS[key]):
        for x, ch in enumerate(row):
            if ch in COLORS:
                img.putpixel((i * 16 + x, y + 3), COLORS[ch])
img.save(os.path.join(OUT, "emote_16.png"))

# ---------- 10. Đồng xu VND (16x16, kiểu xu cổ lỗ vuông) ----------
img, d = new(16, 16)
d.ellipse([1, 1, 14, 14], fill=(232, 195, 74), outline=(160, 122, 32))
d.ellipse([2, 2, 13, 13], outline=(248, 226, 140))
d.rectangle([6, 6, 9, 9], fill=(160, 122, 32))
d.rectangle([7, 7, 8, 8], fill=(0, 0, 0, 0))
img.save(os.path.join(OUT, "xu_tien_16.png"))

# ---------- 11. Xe khách về quê (96x48, nhìn ngang) ----------
img, d = new(96, 48)
BODY = WHITE; STRIPE = (62, 124, 184); OUTL = (40, 45, 60)
d.rounded_rectangle([4, 10, 91, 38], radius=5, fill=BODY, outline=OUTL, width=2)
d.rectangle([4, 27, 91, 33], fill=STRIPE)  # sọc xanh
d.rectangle([10, 4, 78, 10], fill=(120, 90, 60), outline=OUTL)  # giá nóc + hành lý
for x in (14, 30, 46, 62):
    d.rectangle([x, 5, x + 12, 9], fill=random.choice([(150, 110, 70), (100, 120, 90), (160, 140, 100)]), outline=(70, 55, 40))
for i in range(5):  # cửa sổ
    x = 10 + i * 14
    d.rectangle([x, 14, x + 10, 23], fill=(168, 215, 235), outline=OUTL)
    d.line([x + 1, 15, x + 7, 15], fill=(220, 242, 250))
d.rectangle([80, 14, 88, 30], fill=(168, 215, 235), outline=OUTL)  # kính trước
d.rectangle([68, 24, 78, 37], fill=(230, 230, 225), outline=OUTL)  # cửa lên xuống
d.line([73, 24, 73, 37], fill=OUTL)
for cx in (22, 72):  # bánh xe
    d.ellipse([cx - 7, 33, cx + 7, 47], fill=(35, 35, 35), outline=(15, 15, 15))
    d.ellipse([cx - 3, 37, cx + 3, 43], fill=(150, 150, 150))
d.rectangle([89, 30, 92, 34], fill=(245, 220, 110), outline=OUTL)  # đèn pha
d.rectangle([3, 30, 6, 34], fill=(200, 80, 60), outline=OUTL)      # đèn hậu
img.save(os.path.join(OUT, "xe_khach_ve_que_96x48.png"))

print("Da sinh xong PNG placeholder vao:", os.path.abspath(OUT))
for f in sorted(os.listdir(OUT)):
    print(" -", f)

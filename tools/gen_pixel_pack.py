# -*- coding: utf-8 -*-
"""
PIXEL PACK P0 theo Production Plan v2 (Muc 4) — tat ca ve o do phan giai goc,
outline 1px, palette dong que: nau dat / xanh ma / vang nang / do gach.
Output: AvatarClient/assets/ui_pixel/  +  assets/art/characters/mc_full.png
"""
import os
from PIL import Image, ImageDraw

CLIENT = r"E:\Avatar Farm\AvatarClient"
OUT = os.path.join(CLIENT, "assets", "ui_pixel")
os.makedirs(OUT, exist_ok=True)

# ---- palette ----
OUTL   = (46, 32, 21)        # outline chung
WOOD_D = (90, 61, 38)
WOOD_M = (122, 84, 51)
WOOD_L = (154, 111, 66)
BAMBOO = (201, 161, 92)
BAM_L  = (226, 190, 128)
PAPER  = (240, 224, 184)
PAPER_S= (216, 196, 150)
DARKIN = (58, 44, 30)
GREEN  = (109, 169, 68)
GREEN_D= (74, 122, 46)
GOLD   = (232, 195, 74)
TERRA  = (181, 83, 60)
WHITE_C= (239, 236, 228)     # su trang
SKIN   = (232, 176, 136)
SKIN_S = (201, 141, 100)


def new(w, h):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def px(d, x, y, c):
    d.point((x, y), fill=c)


# ============ 1. PANEL GO 9-SLICE (24x24, margin 7) ============
def panel9(inner):
    img, d = new(24, 24)
    d.rectangle([1, 1, 22, 22], fill=inner)
    d.rectangle([1, 1, 22, 22], outline=WOOD_M)
    d.rectangle([2, 2, 21, 21], outline=WOOD_M)
    # bevel sang/tram
    d.line([2, 2, 21, 2], fill=WOOD_L)
    d.line([2, 2, 2, 21], fill=WOOD_L)
    d.line([2, 21, 21, 21], fill=WOOD_D)
    d.line([21, 3, 21, 21], fill=WOOD_D)
    d.rectangle([0, 0, 23, 23], outline=OUTL)
    # 4 got tre goc
    for cx, cy in [(3, 3), (20, 3), (3, 20), (20, 20)]:
        d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], fill=BAMBOO)
        px(d, cx, cy, BAM_L)
        d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], outline=OUTL)
    # net go trong vien
    for x in (7, 12, 17):
        px(d, x, 1, WOOD_D)
        px(d, x + 1, 22, WOOD_L)
    return img

panel9(PAPER).save(os.path.join(OUT, "panel_paper_9.png"))
panel9(DARKIN).save(os.path.join(OUT, "panel_dark_9.png"))


# ============ 2. O CHIEU / SLOT (24x24 + ban chon) ============
def slot(selected=False):
    img, d = new(24, 24)
    d.rectangle([1, 1, 22, 22], fill=DARKIN)
    d.rectangle([1, 1, 22, 22], outline=WOOD_M)
    d.rectangle([2, 2, 21, 21], outline=WOOD_D)
    d.rectangle([0, 0, 23, 23], outline=OUTL)
    d.line([2, 2, 21, 2], fill=WOOD_L)
    # day tre buoc cheo 4 goc
    for cx, cy, dx in [(2, 2, 1), (21, 2, -1), (2, 21, 1), (21, 21, -1)]:
        d.line([cx, cy + 2 * (1 if cy < 12 else -1), cx + 2 * dx, cy], fill=BAMBOO)
    if selected:
        d.rectangle([0, 0, 23, 23], outline=GOLD)
        d.rectangle([1, 1, 22, 22], outline=GOLD)
    return img

slot(False).save(os.path.join(OUT, "slot_24.png"))
slot(True).save(os.path.join(OUT, "slot_24_chon.png"))


# ============ 3. NUT TRON GO (32x32: thuong + bam) ============
def round_btn(pressed=False):
    img, d = new(32, 32)
    pxs = img.load()
    for y in range(32):
        for x in range(32):
            dx, dy = x - 15.5, y - 15.5
            r = (dx * dx + dy * dy) ** 0.5
            if r <= 15.5:
                if r > 14.2:
                    pxs[x, y] = OUTL
                elif r > 11.4:
                    base = WOOD_M
                    if dy < -abs(dx) * 0.3:
                        base = WOOD_L
                    elif dy > abs(dx) * 0.3:
                        base = WOOD_D
                    pxs[x, y] = base
                elif r > 10.4:
                    pxs[x, y] = OUTL
                else:
                    pxs[x, y] = (200, 184, 148) if pressed else PAPER
    # 4 dinh dong
    for cx, cy in [(15, 2), (15, 29), (2, 15), (29, 15)]:
        pxs[cx, cy] = GOLD
        pxs[cx + 1, cy] = GOLD
    return img

round_btn(False).save(os.path.join(OUT, "nut_tron_32.png"))
round_btn(True).save(os.path.join(OUT, "nut_tron_32_bam.png"))


# ============ 4. JOYSTICK (de 48 + num 20) ============
img, d = new(48, 48)
pxs = img.load()
for y in range(48):
    for x in range(48):
        dx, dy = x - 23.5, y - 23.5
        r = (dx * dx + dy * dy) ** 0.5
        if 22.5 >= r > 21:
            pxs[x, y] = (*OUTL, 200)
        elif 21 >= r > 18.5:
            pxs[x, y] = (*BAMBOO, 170)
        elif 18.5 >= r > 17.5:
            pxs[x, y] = (*WOOD_D, 150)
        elif r <= 17.5:
            pxs[x, y] = (40, 34, 26, 70)
# 4 vach huong
for cx, cy in [(23, 4), (23, 42), (4, 23), (42, 23)]:
    d.rectangle([cx, cy, cx + 1, cy + 1], fill=(*BAM_L, 220))
img.save(os.path.join(OUT, "joystick_de_48.png"))

img, d = new(20, 20)
pxs = img.load()
for y in range(20):
    for x in range(20):
        dx, dy = x - 9.5, y - 9.5
        r = (dx * dx + dy * dy) ** 0.5
        if r <= 9.5:
            if r > 8.3:
                pxs[x, y] = OUTL
            elif dy < -2:
                pxs[x, y] = BAM_L
            elif dy > 3:
                pxs[x, y] = WOOD_M
            else:
                pxs[x, y] = BAMBOO
img.save(os.path.join(OUT, "joystick_num_20.png"))


# ============ 5. KHUNG THANH STAMINA (64x12, long 60x8 tu (2,2)) ============
img, d = new(64, 12)
d.rectangle([0, 0, 63, 11], outline=OUTL)
d.rectangle([1, 1, 62, 10], outline=WOOD_M)
d.line([1, 1, 62, 1], fill=WOOD_L)
d.line([1, 10, 62, 10], fill=WOOD_D)
d.rectangle([2, 2, 61, 9], fill=(30, 24, 17))
img.save(os.path.join(OUT, "stamina_khung_64x12.png"))


# ============ 6. ONG TRUONG THON 64x64 x5 (idle + khoi x3 + vay tay) ============
def truong_thon(d, ox, smoke=0, wave=False):
    def R(x0, y0, x1, y1, fill, outline=None):
        d.rectangle([ox + x0, y0, ox + x1, y1], fill=fill, outline=outline)
    # bong
    d.ellipse([ox + 16, 58, ox + 46, 63], fill=(30, 24, 17, 90))
    # dep to ong vang
    R(19, 56, 28, 59, GOLD, OUTL)
    R(34, 56, 43, 59, GOLD, OUTL)
    px(d, ox + 22, 57, (170, 140, 40)); px(d, ox + 25, 57, (170, 140, 40))
    px(d, ox + 37, 57, (170, 140, 40)); px(d, ox + 40, 57, (170, 140, 40))
    # chan
    R(21, 48, 26, 56, SKIN, SKIN_S)
    R(36, 48, 41, 56, SKIN, SKIN_S)
    # quan dui nau lung
    R(17, 39, 45, 49, (109, 81, 56), OUTL)
    d.line([ox + 31, 44, ox + 31, 49], fill=(80, 58, 40))       # ong quan
    d.line([ox + 18, 41, ox + 44, 41], fill=(129, 98, 68))      # cap quan
    # bung beo + ao ba lo trang
    d.ellipse([ox + 14, 18, ox + 48, 44], fill=WHITE_C, outline=OUTL)
    d.ellipse([ox + 17, 20, ox + 45, 41], outline=(216, 212, 202))
    d.arc([ox + 18, 28, ox + 44, 46], 20, 160, fill=(206, 200, 188))  # bong bung duoi
    # vien nach ao ba lo
    d.arc([ox + 14, 16, ox + 26, 28], 200, 320, fill=(190, 186, 176))
    d.arc([ox + 36, 16, ox + 48, 28], 220, 340, fill=(190, 186, 176))
    # tay trai (cua nguoi xem: ben phai) cam dieu cay
    if wave:
        R(45, 12, 50, 24, SKIN, SKIN_S)                          # gio tay cao
        R(46, 8, 51, 13, SKIN, SKIN_S)                           # ban tay xoe
        px(d, ox + 47, 7, SKIN); px(d, ox + 49, 7, SKIN); px(d, ox + 51, 9, SKIN)
    else:
        R(44, 22, 49, 36, SKIN, SKIN_S)
        # dieu cay: ong tre cheo tu tay len mieng
        d.line([ox + 47, 34, ox + 36, 13], fill=BAMBOO, width=2)
        d.line([ox + 47, 35, ox + 37, 14], fill=(156, 120, 62))
        R(45, 33, 49, 38, (122, 84, 51), OUTL)                   # bau dieu
    # tay phai chong hong
    R(13, 22, 18, 34, SKIN, SKIN_S)
    # dau map
    d.ellipse([ox + 22, 4, ox + 40, 20], fill=SKIN, outline=OUTL)
    d.arc([ox + 22, 3, ox + 40, 13], 190, 350, fill=(120, 120, 120))  # toc hoa ram sat
    px(d, ox + 27, 11, (52, 40, 32)); px(d, ox + 35, 11, (52, 40, 32))  # mat
    d.line([ox + 29, 15, ox + 33, 15], fill=SKIN_S)              # mieng cuoi
    px(d, ox + 21, 12, SKIN); px(d, ox + 41, 12, SKIN)           # tai
    px(d, ox + 25, 13, (240, 190, 150)); px(d, ox + 37, 13, (240, 190, 150))  # ma hong phinh
    # khoi dieu cay (3 muc)
    grey = [(216, 216, 216, 220), (226, 226, 226, 170), (236, 236, 236, 110)]
    if smoke >= 1:
        d.rectangle([ox + 35, 9, ox + 37, 11], fill=grey[0])
    if smoke >= 2:
        d.rectangle([ox + 37, 4, ox + 40, 7], fill=grey[1])
        px(d, ox + 36, 5, grey[1])
    if smoke >= 3:
        d.rectangle([ox + 40, 0, ox + 44, 3], fill=grey[2])
        px(d, ox + 39, 1, grey[2]); px(d, ox + 45, 2, grey[2])

img, d = new(64 * 5, 64)
for i in range(4):
    truong_thon(d, i * 64, smoke=i)
truong_thon(d, 4 * 64, wave=True)
img.save(os.path.join(CLIENT, "assets", "art", "characters", "truong_thon_64_5f.png"))


# ============ 7. CO 3 TRANG THAI (32x32 x3: ram - goc ra - sach) ============
img, d = new(96, 32)
# f0: bui co ram
for bx, by, h in [(8, 28, 12), (13, 29, 15), (18, 28, 13), (23, 29, 11), (11, 30, 9), (21, 30, 9), (16, 30, 16)]:
    d.line([bx, by, bx, by - h], fill=GREEN_D)
    d.line([bx - 1, by, bx - 2, by - h + 3], fill=GREEN)
    d.line([bx + 1, by, bx + 2, by - h + 3], fill=(133, 189, 90))
    px(d, bx, by - h - 1, (162, 210, 110))
# f1: goc ra sau khi chem
ox = 32
for bx in (9, 14, 19, 24):
    d.line([ox + bx, 29, ox + bx, 25], fill=GREEN_D)
    d.line([ox + bx + 1, 29, ox + bx + 1, 26], fill=GREEN)
for sx, sy in [(7, 30), (16, 31), (22, 30), (27, 31), (12, 30)]:  # vun co vang roi
    d.line([ox + sx, sy, ox + sx + 2, sy], fill=(180, 190, 110))
# f2: sach (chi vai cham)
ox = 64
for sx, sy in [(12, 29), (20, 30), (16, 28)]:
    px(d, ox + sx, sy, GREEN_D)
img.save(os.path.join(OUT, "co_3_trang_thai_32.png"))


# ============ 8. MINIGAME CAU CHI SU — asset pixel roi ============
# 8.1 bang go nen 120x84 (scale 5 trong game)
img, d = new(120, 84)
d.rectangle([0, 0, 119, 83], outline=OUTL)
d.rectangle([1, 1, 118, 82], fill=(58, 44, 30))
d.rectangle([1, 1, 118, 82], outline=WOOD_M)
for y in range(12, 84, 14):  # van go ngang
    d.line([2, y, 117, y], fill=(48, 36, 24))
for x, y in [(8, 6), (110, 74), (14, 70)]:  # vet xuoc
    d.line([x, y, x + 4, y + 2], fill=(70, 54, 38))
# mang nhen goc
for i in range(4):
    d.line([2 + i * 3, 2, 2, 2 + i * 3], fill=(120, 116, 108, 140))
img.save(os.path.join(OUT, "mg_bang_go_120x84.png"))

# 8.2 truc dong + de (16x56)
img, d = new(16, 56)
d.rectangle([6, 0, 9, 47], fill=BAMBOO, outline=OUTL)
d.line([7, 1, 7, 46], fill=BAM_L)
d.rectangle([0, 48, 15, 55], fill=WOOD_M, outline=OUTL)
d.line([1, 49, 14, 49], fill=WOOD_L)
img.save(os.path.join(OUT, "mg_truc_16x56.png"))

# 8.3 ba loi su (32/24/17 x 10)
for w, band, name in [(32, TERRA, "to"), (24, (36, 90, 130), "vua"), (17, (150, 60, 60), "nho")]:
    img, d = new(w, 10)
    d.rounded_rectangle([0, 0, w - 1, 9], radius=4, fill=WHITE_C, outline=OUTL)
    d.line([2, 2, w - 3, 2], fill=(251, 250, 246))
    d.line([2, 5, w - 3, 5], fill=band)
    d.line([2, 6, w - 3, 6], fill=band)
    d.rectangle([0, 3, 1, 7], fill=BAMBOO)
    d.rectangle([w - 2, 3, w - 1, 7], fill=BAMBOO)
    img.save(os.path.join(OUT, "mg_loi_su_%s.png" % name))


# ============ 9. MC ACTIONS — ghep tu sprite walk + cong cu co san ============
ART = os.path.join(CLIENT, "assets", "art")
mc_sheet = Image.open(os.path.join(ART, "characters", "animatewalkingmaincharacter.png"))
idle = mc_sheet.crop((0, 0, 64, 64))
liem = Image.open(os.path.join(ART, "assets", "liem_32x32.png")).crop((0, 0, 32, 32))
cuoc = Image.open(os.path.join(ART, "assets", "cuoc_chim.png")).crop((0, 0, 32, 32))
binh_sheet = Image.open(os.path.join(ART, "assets", "binh_nuoc_nghieng.png"))
binh = binh_sheet.crop((5 * 32, 0, 6 * 32, 32))   # frame nghieng giua


def lean(body, dx, dy=0):
    """nghieng nguoi: dich nua than tren"""
    out = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    bottom = body.crop((0, 34, 64, 64))
    top = body.crop((0, 0, 64, 34))
    out.paste(bottom, (0, 34), bottom)
    out.paste(top, (dx, dy), top)
    return out


def with_tool(body, tool, angle, tx, ty, arc=None, specks=None):
    out = body.copy()
    t = tool.rotate(angle, resample=Image.NEAREST, expand=True)
    out.paste(t, (tx, ty), t)
    dd = ImageDraw.Draw(out)
    if arc:  # vet chem trang
        for (ax, ay) in arc:
            dd.point((ax, ay), fill=(255, 255, 255, 230))
            dd.point((ax + 1, ay + 1), fill=(255, 255, 255, 140))
    if specks:
        for (sx, sy, c) in specks:
            dd.point((sx, sy), fill=c)
    return out


frames = []
# LUU Y: cac frame ghep cong-cu-vao-tay bi troi lo lung (can ve tay / PixelLab
# de co animation cam cong cu that). Chi giu 2 frame MET (chinh sua than nguoi).
# MET 2f (gap nguoi + giot mo hoi)
tired1 = lean(idle, 0, 2)
d1 = ImageDraw.Draw(tired1)
d1.rectangle([44, 14, 45, 16], fill=(120, 190, 240))
frames.append(tired1)
tired2 = lean(idle, 0, 3)
d2 = ImageDraw.Draw(tired2)
d2.rectangle([44, 20, 45, 22], fill=(120, 190, 240))
px2 = tired2.load()
frames.append(tired2)

full = Image.new("RGBA", (64 * (10 + len(frames)), 64), (0, 0, 0, 0))
full.paste(mc_sheet, (0, 0))
for i, f in enumerate(frames):
    full.paste(f, ((10 + i) * 64, 0), f)
full.save(os.path.join(ART, "characters", "mc_full.png"))
print("mc_full.png:", full.size, "= 10 walk +", len(frames), "action frames")
print("PIXEL PACK done ->", OUT)

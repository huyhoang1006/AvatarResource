# -*- coding: utf-8 -*-
"""
Batch 2: PNG placeholder theo kich ban chi tiet Ngay 1-2 (MOBA-style mobile)
+ man chon nhan vat. Chay: python -X utf8 tools/gen_placeholders_flow.py
Output: png_placeholders_ngay1-2/
"""
import os, math, random
from PIL import Image, ImageDraw

random.seed(7)
OUT = os.path.join(os.path.dirname(__file__), "..", "png_placeholders_ngay1-2")
os.makedirs(OUT, exist_ok=True)

BRICK    = (181, 83, 60)
BRICK_LT = (201, 112, 90)
BRICK_DK = (138, 63, 46)
MORTAR   = (120, 60, 48)
MOSS     = (110, 150, 70)
CREAM    = (245, 233, 201)
WOOD_OUT = (58, 47, 35)
WOOD     = (138, 106, 72)
WOOD_DK  = (95, 69, 46)
GRASS_DK = (105, 163, 66)
SKIN     = (235, 190, 150)
UI_DARK  = (40, 34, 26, 230)


def new(w, h, bg=(0, 0, 0, 0)):
    img = Image.new("RGBA", (w, h), bg)
    return img, ImageDraw.Draw(img)


# ---------- 1. San gach do 32x32: sach / reu / nut / co moc ----------
def brick_base(d, ox):
    d.rectangle([ox, 0, ox + 31, 31], fill=MORTAR)
    for row in range(4):
        y = row * 8
        off = 0 if row % 2 == 0 else 16
        for col in range(-1, 2):
            x = ox + off + col * 32
            x0, x1 = max(ox, x + 1), min(ox + 31, x + 30)
            if x0 <= x1:
                d.rectangle([x0, y + 1, x1, y + 6], fill=BRICK)
    for _ in range(25):
        x, y = ox + random.randrange(32), random.randrange(32)
        d.point((x, y), fill=random.choice([BRICK_LT, BRICK_DK]))

img, d = new(128, 32)
brick_base(d, 0)
brick_base(d, 32)   # + reu
for _ in range(7):
    x, y = 32 + random.randrange(2, 28), random.randrange(2, 28)
    d.ellipse([x, y, x + 3, y + 2], fill=MOSS)
    d.point((x + 1, y), fill=(140, 180, 90))
brick_base(d, 64)   # + nut
d.line([70, 4, 78, 14], fill=(70, 35, 28), width=1)
d.line([78, 14, 74, 24], fill=(70, 35, 28))
d.line([74, 24, 82, 30], fill=(70, 35, 28))
brick_base(d, 96)   # + bui co dai moc len
for cx, cy in [(108, 22), (116, 18), (112, 26)]:
    d.line([cx, cy, cx - 3, cy - 7], fill=(85, 130, 55))
    d.line([cx, cy, cx, cy - 9], fill=(70, 110, 45))
    d.line([cx, cy, cx + 3, cy - 7], fill=(85, 130, 55))
img.save(os.path.join(OUT, "gach_do_san_32.png"))


# ---------- 2. Joystick ao ----------
img, d = new(100, 64)
d.ellipse([2, 2, 61, 61], fill=(60, 60, 60, 90), outline=(240, 240, 240, 150), width=2)
d.ellipse([18, 18, 45, 45], outline=(240, 240, 240, 70))
d.ellipse([68, 20, 95, 47], fill=(200, 200, 200, 180), outline=(255, 255, 255, 220), width=2)
d.ellipse([74, 25, 85, 33], fill=(235, 235, 235, 120))
img.save(os.path.join(OUT, "ui_moba_joystick.png"))


# ---------- 3. Nut trung tam 40x40 voi 6 icon trang thai ----------
def center_btn(d, ox):
    d.ellipse([ox + 1, 1, ox + 38, 38], fill=(78, 58, 38, 235), outline=CREAM, width=2)
    d.ellipse([ox + 4, 4, ox + 35, 35], outline=(160, 130, 95))

img, d = new(240, 40)
IC = (245, 233, 201)
for i in range(6):
    center_btn(d, i * 40)
# 3.1 liem (luoi cong + can)
d.arc([8, 8, 30, 26], 200, 340, fill=IC, width=3)
d.line([26, 22, 22, 31], fill=(200, 160, 110), width=3)
# 3.2 ban tay
ox = 40
d.rectangle([ox + 14, 18, ox + 26, 30], fill=IC)
for i, fx in enumerate([14, 18, 22, 26]):
    d.rectangle([ox + fx - 1, 10 + (2 if i in (0, 3) else 0), ox + fx + 1, 18], fill=IC)
d.rectangle([ox + 10, 20, ox + 13, 26], fill=IC)
# 3.3 cua mo
ox = 80
d.rectangle([ox + 12, 9, ox + 28, 31], outline=IC, width=2)
d.polygon([(ox + 14, 11), (ox + 24, 8), (ox + 24, 29), (ox + 14, 29)], fill=IC)
d.point((ox + 22, 19), fill=(78, 58, 38))
# 3.4 gau muc nuoc
ox = 120
d.line([ox + 20, 8, ox + 20, 14], fill=IC, width=2)
d.polygon([(ox + 12, 14), (ox + 28, 14), (ox + 25, 28), (ox + 15, 28)], outline=IC, fill=None)
d.line([ox + 15, 27, ox + 25, 27], fill=(140, 200, 235), width=2)
d.arc([ox + 12, 8, ox + 28, 20], 180, 360, fill=IC)
# 3.5 mat trang
ox = 160
d.ellipse([ox + 10, 9, ox + 31, 30], fill=IC)
d.ellipse([ox + 16, 7, ox + 35, 26], fill=(78, 58, 38, 255))
# 3.6 nut [>] qua thoai
ox = 200
d.polygon([(ox + 14, 11), (ox + 28, 20), (ox + 14, 29)], fill=IC)
img.save(os.path.join(OUT, "ui_moba_nut_trung_tam.png"))


# ---------- 4. O chieu (3 skill) + o hoi phuc ----------
img, d = new(4 * 40, 36)
for i in range(4):
    x = i * 40
    col = (78, 58, 38, 235) if i < 3 else (58, 78, 44, 235)
    d.ellipse([x + 2, 2, x + 33, 33], fill=col, outline=(200, 175, 135), width=2)
    if i < 3:
        d.text  # no text; ve cham so cap
        for k in range(i + 1):
            d.point((x + 14 + k * 4, 29), fill=CREAM)
# icon banh phu the trong o hoi phuc (hop vuong vang-xanh)
x = 3 * 40
d.rectangle([x + 12, 12, x + 24, 24], fill=(214, 194, 74), outline=(120, 140, 60), width=2)
d.point([(x + 17, 17), (x + 19, 19)], fill=(240, 230, 170))
img.save(os.path.join(OUT, "ui_moba_o_chieu.png"))


# ---------- 5. Quest tracker goc phai + cham than ----------
img, d = new(96, 40)
d.rounded_rectangle([0, 6, 88, 39], radius=5, fill=UI_DARK, outline=(160, 130, 95), width=2)
d.rectangle([8, 14, 60, 18], fill=(120, 108, 88))
d.rectangle([8, 24, 76, 28], fill=(96, 86, 70))
d.rectangle([8, 31, 48, 35], fill=(96, 86, 70))
d.ellipse([74, 0, 95, 21], fill=(232, 195, 74), outline=(160, 122, 32), width=2)  # badge
d.rectangle([83, 4, 86, 12], fill=(90, 60, 20))
d.rectangle([83, 15, 86, 17], fill=(90, 60, 20))
img.save(os.path.join(OUT, "ui_quest_tracker.png"))


# ---------- 6. Target indicator: o vuong xanh (2 frame) + vong auto-lock (2 frame) ----------
img, d = new(128, 32)
for f, alpha in [(0, 255), (1, 150)]:
    ox = f * 32
    c = (80, 220, 100, alpha)
    d.rectangle([ox + 1, 1, ox + 30, 30], outline=c, width=2)
    for cx, cy, dx, dy in [(1, 1, 1, 1), (30, 1, -1, 1), (1, 30, 1, -1), (30, 30, -1, -1)]:
        d.line([ox + cx, cy, ox + cx + dx * 6, cy], fill=(255, 255, 255, alpha), width=2)
        d.line([ox + cx, cy, ox + cx, cy + dy * 6], fill=(255, 255, 255, alpha), width=2)
for f, r in [(0, 13), (1, 10)]:
    ox = 64 + f * 32
    d.ellipse([ox + 16 - r, 22 - r // 2, ox + 16 + r, 22 + r // 2],
              outline=(255, 210, 80, 230), width=2)
img.save(os.path.join(OUT, "ui_target_indicator.png"))


# ---------- 7. Ong Truong Thon 48x48 x4 frame (idle + 3 frame khoi dieu cay) ----------
def truong_thon(d, ox, smoke=0):
    # dep to ong vang
    d.rectangle([ox + 14, 44, ox + 21, 46], fill=(230, 200, 80), outline=(170, 140, 40))
    d.rectangle([ox + 26, 44, ox + 33, 46], fill=(230, 200, 80), outline=(170, 140, 40))
    # chan
    d.rectangle([ox + 15, 38, ox + 20, 44], fill=SKIN)
    d.rectangle([ox + 27, 38, ox + 32, 44], fill=SKIN)
    # quan dui nau
    d.rounded_rectangle([ox + 13, 31, ox + 34, 39], radius=2, fill=(110, 82, 60), outline=(75, 55, 40))
    # bung beo - ao ba lo trang
    d.rounded_rectangle([ox + 11, 16, ox + 36, 33], radius=6, fill=(245, 245, 240), outline=(190, 190, 185))
    d.line([ox + 16, 17, ox + 14, 22], fill=(190, 190, 185))
    d.line([ox + 31, 17, ox + 33, 22], fill=(190, 190, 185))
    # vai + tay tran
    d.rectangle([ox + 8, 18, ox + 12, 28], fill=SKIN, outline=(200, 155, 120))
    d.rectangle([ox + 35, 18, ox + 39, 26], fill=SKIN, outline=(200, 155, 120))
    # dau
    d.ellipse([ox + 16, 3, ox + 31, 17], fill=SKIN, outline=(200, 155, 120))
    d.arc([ox + 16, 2, ox + 31, 12], 200, 340, fill=(90, 90, 90), width=2)  # toc hoa ram
    d.point([(ox + 20, 9), (ox + 26, 9)], fill=(50, 40, 35))                # mat
    d.line([ox + 22, 13, ox + 25, 13], fill=(160, 110, 90))                 # mieng
    # dieu cay (ong tre cheo tu mieng xuong tay phai)
    d.line([ox + 24, 13, ox + 40, 24], fill=(160, 130, 80), width=2)
    d.rectangle([ox + 38, 22, ox + 42, 27], fill=(120, 95, 55), outline=(85, 65, 38))
    # khoi thuoc (3 muc bay len)
    if smoke >= 1:
        d.ellipse([ox + 25, 7, ox + 29, 10], fill=(210, 210, 210, 190))
    if smoke >= 2:
        d.ellipse([ox + 27, 1, ox + 33, 5], fill=(220, 220, 220, 150))
    if smoke >= 3:
        d.ellipse([ox + 31, -1, ox + 39, 3], fill=(230, 230, 230, 110))

img, d = new(192, 48)
for f in range(4):
    truong_thon(d, f * 48, smoke=f)
img.save(os.path.join(OUT, "npc_truong_thon_48x48_4f.png"))


# ---------- 8. Bien go bam reu "Dat khong phu nguoi cham" ----------
img, d = new(32, 48)
d.rectangle([14, 24, 18, 46], fill=WOOD_DK, outline=WOOD_OUT)
d.rounded_rectangle([2, 6, 30, 26], radius=3, fill=WOOD, outline=WOOD_OUT, width=2)
d.line([5, 12, 27, 12], fill=WOOD_DK)
d.line([5, 17, 24, 17], fill=WOOD_DK)
d.line([5, 22, 26, 22], fill=WOOD_DK)
for x, y in [(3, 7), (26, 8), (4, 22), (24, 23), (15, 44)]:  # reu
    d.ellipse([x, y, x + 4, y + 2], fill=MOSS)
img.save(os.path.join(OUT, "bien_go_ong_ngoai_32x48.png"))


# ---------- 9. Cong rao tre xoc xech 64x48 ----------
img, d = new(64, 48)
for px in (4, 56):
    d.rectangle([px, 8, px + 4, 46], fill=(201, 161, 92), outline=(156, 120, 62))
    d.line([px + 2, 8, px + 2, 46], fill=(226, 190, 128))
# canh cong lech (2 thanh cheo + thanh ngang xieu veo)
d.line([10, 18, 54, 14], fill=(201, 161, 92), width=3)
d.line([10, 30, 54, 34], fill=(201, 161, 92), width=3)
d.line([16, 12, 22, 40], fill=(180, 140, 78), width=2)
d.line([34, 10, 40, 42], fill=(180, 140, 78), width=2)
d.line([48, 12, 50, 40], fill=(180, 140, 78), width=2)
for x, y in [(16, 17), (35, 15), (48, 32)]:  # day buoc
    d.line([x - 2, y - 2, x + 2, y + 2], fill=(120, 90, 50))
    d.line([x - 2, y + 2, x + 2, y - 2], fill=(120, 90, 50))
d.line([50, 34, 53, 44], fill=(156, 120, 62), width=2)  # thanh gay tre xuong
img.save(os.path.join(OUT, "cong_rao_tre_64x48.png"))


# ---------- 10. Minigame Thap Cau Chi Su ----------
img, d = new(160, 120)
d.rounded_rectangle([0, 0, 159, 119], radius=4, fill=(46, 36, 26), outline=(90, 72, 50), width=3)
d.rectangle([6, 6, 153, 113], outline=(30, 23, 16))
for _ in range(30):
    d.point((random.randrange(8, 152), random.randrange(8, 112)), fill=(56, 45, 33))
# 3 truc dong A B C
for i, x in enumerate((36, 80, 124)):
    d.rectangle([x - 14, 96, x + 14, 100], fill=(120, 95, 55), outline=(85, 65, 38))  # de
    d.rectangle([x - 2, 40, x + 2, 96], fill=(196, 160, 80), outline=(140, 108, 44))  # truc dong
    d.line([x - 1, 40, x - 1, 96], fill=(226, 196, 120))
# 3 loi su tren truc A (to -> nho)
for w, y, band in [(26, 86, (150, 100, 50)), (19, 76, (60, 110, 160)), (12, 66, (150, 60, 60))]:
    x = 36
    d.rounded_rectangle([x - w // 2, y - 8, x + w // 2, y], radius=4,
                        fill=(238, 235, 228), outline=(170, 165, 155), width=2)
    d.line([x - w // 2 + 3, y - 4, x + w // 2 - 3, y - 4], fill=band, width=2)
# day dut + tia lua o truc C
d.line([124, 40, 130, 30], fill=(40, 40, 40), width=2)
d.line([130, 30, 128, 20], fill=(40, 40, 40), width=2)
for ang in range(0, 360, 45):
    r = 6 if ang % 90 == 0 else 3
    ex = 128 + int(r * math.cos(math.radians(ang)))
    ey = 18 + int(r * math.sin(math.radians(ang)))
    d.line([128, 18, ex, ey], fill=(255, 230, 100))
d.point((128, 18), fill=(255, 255, 255))
img.save(os.path.join(OUT, "minigame_cau_chi_su_160x120.png"))

# tia lua rieng 2 frame (dung cho den bao / day dien net lua)
img, d = new(32, 16)
for f, r1, r2 in [(0, 6, 3), (1, 4, 2)]:
    cx = 8 + f * 16
    for ang in range(0, 360, 45):
        r = r1 if ang % 90 == 0 else r2
        d.line([cx, 8, cx + int(r * math.cos(math.radians(ang))), 8 + int(r * math.sin(math.radians(ang)))],
               fill=(255, 230, 100))
    d.point((cx, 8), fill=(255, 255, 255))
img.save(os.path.join(OUT, "fx_tia_lua_16_2f.png"))

# den bao do nhap nhay 2 frame 8x8
img, d = new(16, 8)
d.ellipse([1, 1, 6, 6], fill=(220, 60, 50), outline=(255, 140, 120))
d.point((3, 2), fill=(255, 200, 190))
d.ellipse([10, 2, 14, 6], fill=(90, 30, 25))
img.save(os.path.join(OUT, "den_bao_do_8_2f.png"))


# ---------- 11. Item icon 16x16: chia khoa cu + co dai ----------
img, d = new(32, 16)
d.ellipse([1, 3, 8, 10], outline=(196, 160, 80), width=2)          # dau khoa
d.line([8, 6, 14, 6], fill=(196, 160, 80), width=2)                # than
d.line([11, 6, 11, 9], fill=(196, 160, 80), width=2)               # rang
d.line([14, 6, 14, 10], fill=(196, 160, 80), width=2)
ox = 16
for cx, cy in [(ox + 6, 13), (ox + 10, 14)]:                       # co dai
    d.line([cx, cy, cx - 3, cy - 6], fill=(85, 130, 55))
    d.line([cx, cy, cx, cy - 8], fill=(70, 110, 45))
    d.line([cx, cy, cx + 3, cy - 6], fill=(85, 130, 55))
img.save(os.path.join(OUT, "item_chiakhoa_codai_16.png"))


# ---------- 12. Icon trang thai 16x16: chong mat / dau bung / mo hoi ----------
img, d = new(48, 16)
d.arc([2, 2, 13, 13], 0, 280, fill=(150, 120, 220), width=2)       # xoay chong mat
d.arc([5, 5, 10, 10], 90, 360, fill=(180, 160, 235), width=1)
ox = 16
d.ellipse([ox + 3, 3, ox + 12, 12], fill=(230, 180, 140), outline=(180, 120, 90))  # bung
d.line([ox + 5, 8, ox + 7, 6], fill=(150, 80, 60))
d.line([ox + 7, 6, ox + 9, 9], fill=(150, 80, 60))
d.line([ox + 9, 9, ox + 11, 7], fill=(150, 80, 60))
ox = 32
d.polygon([(ox + 8, 2), (ox + 4, 9), (ox + 8, 13), (ox + 12, 9)], fill=(120, 190, 240), outline=(70, 140, 200))  # giot mo hoi
d.point((ox + 6, 8), fill=(200, 235, 255))
img.save(os.path.join(OUT, "icon_trang_thai_16.png"))


# ---------- 13. UI loot ruong (4 slot) ----------
img, d = new(150, 110)
d.rounded_rectangle([0, 0, 149, 109], radius=6, fill=CREAM, outline=WOOD_OUT, width=3)
d.rectangle([3, 3, 146, 22], fill=(184, 74, 60))                   # thanh tieu de
d.rectangle([8, 8, 80, 16], fill=(220, 130, 115))
for i in range(4):                                                  # 4 o do
    x, y = 12 + (i % 2) * 66, 30 + (i // 2) * 38
    d.rounded_rectangle([x, y, x + 60, y + 32], radius=4, fill=(236, 222, 186), outline=(160, 130, 95), width=2)
    d.ellipse([x + 6, y + 8, x + 22, y + 24], fill=(200, 175, 135))
    d.rectangle([x + 28, y + 10, x + 54, y + 14], fill=(190, 170, 135))
    d.rectangle([x + 28, y + 19, x + 46, y + 23], fill=(205, 188, 155))
img.save(os.path.join(OUT, "ui_loot_ruong.png"))


# ---------- 14. Man chon nhan vat (mock 220x130) ----------
img, d = new(220, 130)
d.rounded_rectangle([0, 0, 219, 129], radius=8, fill=(52, 42, 32), outline=(160, 130, 95), width=3)
d.rectangle([60, 8, 160, 20], fill=(236, 222, 186))                # tieu de
for i, x in enumerate((28, 118)):                                  # 2 the nhan vat
    sel = i == 0
    d.rounded_rectangle([x, 28, x + 74, 100], radius=5,
                        fill=(78, 62, 46), outline=CREAM if sel else (110, 92, 70), width=2)
    cx = x + 37
    d.ellipse([cx - 8, 38, cx + 8, 54], fill=(120, 104, 84))       # silhouette dau
    d.rounded_rectangle([cx - 12, 56, cx + 12, 88], radius=4, fill=(120, 104, 84))
    d.rectangle([x + 14, 92, x + 60, 96], fill=(160, 140, 112))
d.rounded_rectangle([70, 106, 150, 124], radius=5, fill=(184, 74, 60), outline=CREAM, width=2)  # nut bat dau
d.polygon([(104, 111), (116, 115), (104, 119)], fill=CREAM)
img.save(os.path.join(OUT, "ui_chon_nhan_vat.png"))

# ---------- 15. Prop vuon sau: da tang + khuc go muc (32x32 x2) ----------
img, d = new(64, 32)
d.ellipse([3, 10, 28, 29], fill=(150, 145, 135), outline=(105, 100, 92), width=2)   # da tang
d.ellipse([8, 13, 18, 20], fill=(170, 165, 155))
d.line([14, 22, 24, 25], fill=(120, 115, 106))
d.ellipse([5, 24, 10, 27], fill=MOSS)
ox = 32
d.rounded_rectangle([ox + 2, 14, ox + 27, 26], radius=5, fill=(110, 82, 55), outline=(70, 52, 34), width=2)  # go muc
d.ellipse([ox + 24, 14, ox + 31, 26], fill=(150, 118, 80), outline=(70, 52, 34), width=2)                    # mat cat
d.ellipse([ox + 26, 17, ox + 29, 23], outline=(110, 82, 55))
d.line([ox + 6, 17, ox + 20, 17], fill=(85, 62, 40))
d.line([ox + 8, 22, ox + 18, 22], fill=(85, 62, 40))
d.ellipse([ox + 6, 12, ox + 12, 16], fill=MOSS)                                                              # reu muc
d.ellipse([ox + 14, 24, ox + 19, 27], fill=(140, 110, 60))                                                   # nam nho
img.save(os.path.join(OUT, "prop_vuon_da_go_32.png"))

print("Batch 2 xong.")
for f in sorted(os.listdir(OUT)):
    print(" -", f)

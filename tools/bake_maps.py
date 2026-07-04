# -*- coding: utf-8 -*-
"""Bake background maps cho AvatarClient tu tile placeholder + copy UI assets."""
import os, random, shutil
from PIL import Image

random.seed(11)
RES = r"E:\Avatar Farm\AvatarResource\png_placeholders_ngay1-2"
ART = r"E:\Avatar Farm\AvatarClient\assets"
os.makedirs(os.path.join(ART, "maps"), exist_ok=True)
os.makedirs(os.path.join(ART, "ui"), exist_ok=True)

tiles = Image.open(os.path.join(RES, "tileset_nen_xuan_32.png"))
T = {name: tiles.crop((i * 32, 0, i * 32 + 32, 32))
     for i, name in enumerate(["grass", "grass_fl", "dirt", "grass_dirt", "till_dry", "till_wet", "water", "path"])}
bricks = Image.open(os.path.join(RES, "gach_do_san_32.png"))
B = {name: bricks.crop((i * 32, 0, i * 32 + 32, 32))
     for i, name in enumerate(["brick", "brick_moss", "brick_crack", "brick_weed"])}

def base_map(cols, rows):
    img = Image.new("RGBA", (cols * 32, rows * 32))
    for r in range(rows):
        for c in range(cols):
            t = T["grass_fl"] if random.random() < 0.12 else T["grass"]
            img.paste(t, (c * 32, r * 32))
    return img

def paste_rect(img, tile_fn, c0, r0, c1, r1):
    for r in range(r0, r1):
        for c in range(c0, c1):
            img.paste(tile_fn(), (c * 32, r * 32))

# ---- San gach do (30x20 tiles = 960x640) ----
img = base_map(30, 20)
paste_rect(img, lambda: random.choice([B["brick"]] * 6 + [B["brick_moss"], B["brick_crack"]]), 8, 5, 22, 15)
# duong dat tu cong (duoi) len san
paste_rect(img, lambda: T["dirt"], 14, 15, 16, 20)
img.save(os.path.join(ART, "maps", "san_gach_bg.png"))

# ---- Vuon sau nha (30x20) ----
img = base_map(30, 20)
paste_rect(img, lambda: T["dirt"], 10, 8, 20, 14)      # khoang dat trong trot
paste_rect(img, lambda: T["dirt"], 14, 0, 16, 8)       # loi vao tu cong
img.save(os.path.join(ART, "maps", "vuon_bg.png"))

# ---- Noi that nha (20x13 = 640x416) ----
img = Image.new("RGBA", (640, 416))
from PIL import ImageDraw
d = ImageDraw.Draw(img)
d.rectangle([0, 0, 640, 416], fill=(122, 92, 67))       # nen dat/go
for y in range(0, 416, 16):                             # van go ngang
    d.line([0, y, 640, y], fill=(105, 78, 56))
    for x in range(0, 640, 96):
        d.line([x + (y // 16 % 2) * 48, y, x + (y // 16 % 2) * 48, y + 16], fill=(95, 69, 46))
d.rectangle([0, 0, 640, 96], fill=(84, 62, 44))         # tuong sau
for x in range(0, 640, 32):                             # cot go tuong
    d.line([x, 0, x, 96], fill=(70, 51, 34))
d.rectangle([0, 92, 640, 96], fill=(58, 47, 35))
img.save(os.path.join(ART, "maps", "nha_bg.png"))

# ---- Radial light gradient 256 ----
img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
px = img.load()
for y in range(256):
    for x in range(256):
        dx, dy = x - 128, y - 128
        dist = (dx * dx + dy * dy) ** 0.5 / 128
        a = max(0.0, 1.0 - dist)
        px[x, y] = (255, 255, 255, int(255 * (a ** 1.6)))
img.save(os.path.join(ART, "ui", "light_radial.png"))

# ---- Copy UI placeholders can dung ----
for f in ["ui_moba_joystick.png", "ui_moba_nut_trung_tam.png", "ui_moba_o_chieu.png",
          "ui_quest_tracker.png", "ui_target_indicator.png", "ui_hop_thoai.png",
          "ui_thanh_stamina.png", "ui_hud_ngay_gio.png", "emote_16.png",
          "item_chiakhoa_codai_16.png", "icon_trang_thai_16.png", "ui_loot_ruong.png",
          "bien_go_ong_ngoai_32x48.png", "cong_rao_tre_64x48.png", "hang_rao_tre_32.png",
          "prop_vuon_da_go_32.png", "props_don_nha_32.png", "ruong_4_trang_thai_32.png",
          "fx_tia_lua_16_2f.png", "den_bao_do_8_2f.png", "xu_tien_16.png",
          "xe_khach_ve_que_96x48.png"]:
    shutil.copy(os.path.join(RES, f), os.path.join(ART, "ui", f))
print("Baked maps + copied UI assets")

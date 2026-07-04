# -*- coding: utf-8 -*-
"""Bake nen map Ngo xom (960x640): duong dat ngang, co, loi re vao nha bo me."""
import os, random
from PIL import Image

random.seed(33)
RES = r"E:\Avatar Farm\AvatarResource\png_placeholders_ngay1-2"
OUT = r"E:\Avatar Farm\AvatarClient\assets\maps"

tiles = Image.open(os.path.join(RES, "tileset_nen_xuan_32.png"))
T = {name: tiles.crop((i * 32, 0, i * 32 + 32, 32))
     for i, name in enumerate(["grass", "grass_fl", "dirt", "grass_dirt", "till_dry", "till_wet", "water", "path"])}

img = Image.new("RGBA", (960, 640))
for r in range(20):
    for c in range(30):
        t = T["grass_fl"] if random.random() < 0.12 else T["grass"]
        img.paste(t, (c * 32, r * 32))
# duong dat ngang giua ngo (y tiles 9-12)
for r in range(9, 13):
    for c in range(30):
        img.paste(T["path"] if random.random() < 0.18 else T["dirt"], (c * 32, r * 32))
# loi re len cua nha bo me (x tiles 12-15, y 6-9)
for r in range(6, 9):
    for c in range(12, 16):
        img.paste(T["dirt"], (c * 32, r * 32))
img.save(os.path.join(OUT, "ngo_xom_bg.png"))
print("ngo_xom_bg.png OK")

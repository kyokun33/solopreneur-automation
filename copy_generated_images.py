import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"C:\Users\sude3\.gemini\antigravity-ide\brain\a666220d-4085-4ee9-b4f9-6ea8727b4996"
dst_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"

img_files = {
    "spritesheet.png": "sude_hero_paladin_v6_spritesheet_1786190391703.png",
    "portrait.png": "sude_hero_masterpiece_portrait_1786190404493.png",
    "battlescene.png": "sude_hero_battle_scene_1786190422340.png"
}

for dst_name, src_name in img_files.items():
    src_path = os.path.join(src_dir, src_name)
    dst_path = os.path.join(dst_dir, dst_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)
        print(f"✅ 복사 완료: {dst_name}")
    else:
        print(f"⚠️ 파일 없음: {src_path}")

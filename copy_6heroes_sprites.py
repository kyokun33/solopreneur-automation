import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
brain_dir = r"C:\Users\sude3\.gemini\antigravity-ide\brain\a666220d-4085-4ee9-b4f9-6ea8727b4996"
dst_sprites = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites"
dst_root = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"

os.makedirs(dst_sprites, exist_ok=True)

files = [
    "starter_v1.png",
    "opt1.png",
    "opt2.png",
    "opt3.png",
    "opt4.png",
    "opt5.png",
    "spritesheet.png",
    "portrait.png"
]

for f in files:
    sp = os.path.join(src_dir, f)
    if os.path.exists(sp):
        shutil.copy(sp, os.path.join(dst_sprites, f))
        shutil.copy(sp, os.path.join(dst_root, f))
        print(f"✅ 6대 영웅 자산 복사: {f}")

print("🎉 6대 영웅 자산 배포 완수!")

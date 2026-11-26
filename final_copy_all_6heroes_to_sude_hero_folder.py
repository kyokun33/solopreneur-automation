import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
brain_dir = r"C:\Users\sude3\.gemini\antigravity-ide\brain\a666220d-4085-4ee9-b4f9-6ea8727b4996"

dst_unity_sprites = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites"
dst_unity_root = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"

os.makedirs(dst_unity_sprites, exist_ok=True)

# 1. Copy core 6-hero sprite sheet images
core_images = [
    "starter_v1.png",
    "opt1.png",
    "opt2.png",
    "opt3.png",
    "opt4.png",
    "opt5.png",
    "spritesheet.png",
    "portrait.png",
    "battlescene.png"
]

copied_files = []

for img in core_images:
    src_path = os.path.join(src_dir, img)
    if os.path.exists(src_path):
        shutil.copy(src_path, os.path.join(dst_unity_sprites, img))
        shutil.copy(src_path, os.path.join(dst_unity_root, img))
        copied_files.append(img)
        print(f"✅ [슈드용사 에셋 복사] {img} -> Assets/Sprites/ & 슈드용사/ 루트")

# 2. Copy generated brain sprite sheets
if os.path.exists(brain_dir):
    for f in os.listdir(brain_dir):
        if f.endswith('.png'):
            src_brain = os.path.join(brain_dir, f)
            shutil.copy(src_brain, os.path.join(dst_unity_sprites, f))
            shutil.copy(src_brain, os.path.join(dst_unity_root, f))
            copied_files.append(f)
            print(f"📦 [브레인 원본 스프라이트 시트 복사] {f}")

print(f"🎉 총 {len(copied_files)}개의 6대 영웅 스프라이트 시트 & HQ 도트 이미지 자산이 '슈드용사' 폴더로 안전하게 배포되었습니다!")

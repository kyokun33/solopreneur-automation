import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
brain_dir = r"C:\Users\sude3\.gemini\antigravity-ide\brain\a666220d-4085-4ee9-b4f9-6ea8727b4996"

dst_unity_sprites = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites"
dst_unity_root = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"

os.makedirs(dst_unity_sprites, exist_ok=True)

images_to_copy = [
    "portrait.png",
    "spritesheet.png",
    "battlescene.png",
    "opt1.png",
    "opt2.png",
    "opt3.png",
    "opt4.png",
    "opt5.png"
]

print("🚀 슈드용사 폴더로 이미지 자산 복사 시작...")

copied_count = 0

for img in images_to_copy:
    src_path = os.path.join(src_dir, img)
    if os.path.exists(src_path):
        # Copy to Assets/Sprites/
        shutil.copy(src_path, os.path.join(dst_unity_sprites, img))
        # Copy to 슈드용사/ root
        shutil.copy(src_path, os.path.join(dst_unity_root, img))
        print(f"✅ [슈드용사 에셋 복사 완료] {img} -> Assets/Sprites & 루트")
        copied_count += 1

# Copy original high-res generated PNGs from brain
if os.path.exists(brain_dir):
    for f in os.listdir(brain_dir):
        if f.endswith('.png') and 'sude' in f.lower():
            src_brain = os.path.join(brain_dir, f)
            shutil.copy(src_brain, os.path.join(dst_unity_sprites, f))
            print(f"📦 [브레인 원본 복사 완료] {f}")

print(f"🎉 총 {copied_count}개 핵심 픽셀 아트 이미지가 '슈드용사' 폴더로 안전하게 배포되었습니다!")

import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"C:\Users\sude3\.gemini\antigravity-ide\brain\a666220d-4085-4ee9-b4f9-6ea8727b4996"
dst_workspace = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
dst_unity_sprites = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites"
dst_unity_root = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"

os.makedirs(dst_unity_sprites, exist_ok=True)

img_name = "sude_starter_v1_character_1786191235410.png"
src_path = os.path.join(src_dir, img_name)

if os.path.exists(src_path):
    shutil.copy(src_path, os.path.join(dst_workspace, "starter_v1.png"))
    shutil.copy(src_path, os.path.join(dst_unity_sprites, "starter_v1.png"))
    shutil.copy(src_path, os.path.join(dst_unity_root, "starter_v1.png"))
    print("✅ V1 기본 소년용사 캐릭터 복사 완료 -> starter_v1.png")
else:
    print("⚠️ 원본 이미지를 찾을 수 없습니다.")

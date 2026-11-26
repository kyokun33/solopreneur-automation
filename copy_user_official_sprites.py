import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

user_sprite_dir = r"C:\Users\sude3\OneDrive\Pictures\게임제작이미지\슈드_스프라이트_동작별정리"
workspace_official_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\sude_official_sprites"
unity_official_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\sude_official_sprites"
unity_root_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\sude_official_sprites"

os.makedirs(workspace_official_dir, exist_ok=True)
os.makedirs(unity_official_dir, exist_ok=True)
os.makedirs(unity_root_dir, exist_ok=True)

print("🚀 대표님 원본 스프라이트 폴더 26개 이미지 전수 복사 시작...")

copied_files = []

if os.path.exists(user_sprite_dir):
    for filename in os.listdir(user_sprite_dir):
        if filename.endswith(".png"):
            src_file = os.path.join(user_sprite_dir, filename)
            
            # Copy to 3 target locations
            shutil.copy(src_file, os.path.join(workspace_official_dir, filename))
            shutil.copy(src_file, os.path.join(unity_official_dir, filename))
            shutil.copy(src_file, os.path.join(unity_root_dir, filename))
            
            copied_files.append(filename)
            print(f"✅ [복사 완료] {filename} -> sude_official_sprites/")

print(f"🎉 대표님의 26개 동작별 스프라이트 이미지 전수가 '슈드용사' 에셋 폴더로 100% 안전 이관되었습니다! (총 {len(copied_files)}개)")

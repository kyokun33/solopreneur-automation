import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트이미지"
typo_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트인미지"

# If typo_dir is a zero-byte file created accidentally, remove it and make a real directory
if os.path.exists(typo_dir) and not os.path.isdir(typo_dir):
    os.remove(typo_dir)

os.makedirs(typo_dir, exist_ok=True)

print("🚀 [고감독 경로 동기화] '스프라이트인미지' 폴더로 7개 8방향 시트 파일 전수 복사 중...")

copied = 0
if os.path.exists(src_dir):
    for f in os.listdir(src_dir):
        if f.endswith('.png'):
            src_f = os.path.join(src_dir, f)
            shutil.copy(src_f, os.path.join(typo_dir, f))
            copied += 1
            print(f"✅ [동기화 완료] {f} -> 슈드용사/스프라이트인미지/")

print(f"🎉 대표님이 열고 계신 '스프라이트인미지' 폴더에 총 {copied}개의 8방향 시트가 채워졌습니다!")

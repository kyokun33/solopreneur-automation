import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트이미지"
dest_dirs = [
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트인미지",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트이미지",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트인미지",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트이미지"
]

print("🚀 [고감독 경로 동기화] 모든 8방향 시트 이미지를 루트 및 서브 디렉토리에 100% 비치 중...")

for dest in dest_dirs:
    os.makedirs(dest, exist_ok=True)
    if os.path.exists(src_dir):
        for f in os.listdir(src_dir):
            if f.endswith('.png') and os.path.isfile(os.path.join(src_dir, f)):
                try:
                    shutil.copy(os.path.join(src_dir, f), os.path.join(dest, f))
                except shutil.SameFileError:
                    pass

print("🎉 모든 경로 이미지 파일 전수 비치 및 복사 동기화 완수!")

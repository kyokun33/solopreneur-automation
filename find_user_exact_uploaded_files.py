import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("🔍 [고감독 정밀 픽셀 스캐너] 대표님이 올리신 원본 이미지 파일 경로 수색 중...")

search_roots = [
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사",
    r"C:\Users\sude3\OneDrive\Pictures",
    r"C:\Users\sude3\Downloads"
]

found_images = []

for root_path in search_roots:
    if os.path.exists(root_path):
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Exclude node_modules, .git, __pycache__
            if ".git" in dirpath or "custom_nodes" in dirpath or ".system_generated" in dirpath:
                continue
            for f in filenames:
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and not f.startswith('.'):
                    full_p = os.path.join(dirpath, f)
                    size_kb = round(os.path.getsize(full_p) / 1024, 1)
                    found_images.append((full_p, size_kb))

print(f"📍 스캔 완료! 발견된 모든 이미지 파일 목록 (총 {len(found_images)}개):")
for p, s in found_images[:25]: # Show top 25
    print(f"  - [{s} KB] {p}")

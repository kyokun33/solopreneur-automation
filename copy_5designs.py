import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"C:\Users\sude3\.gemini\antigravity-ide\brain\a666220d-4085-4ee9-b4f9-6ea8727b4996"
dst_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"

img_files = {
    "opt1.png": "sude_design_opt1_1786190613024.png",
    "opt2.png": "sude_design_opt2_1786190627577.png",
    "opt3.png": "sude_design_opt3_1786190639731.png",
    "opt4.png": "sude_design_opt4_1786190652168.png",
    "opt5.png": "sude_design_opt5_1786190666844.png"
}

for dst_name, src_name in img_files.items():
    src_path = os.path.join(src_dir, src_name)
    dst_path = os.path.join(dst_dir, dst_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)
        print(f"✅ 5디자인 복사 완료: {dst_name}")
    else:
        print(f"⚠️ 파일 없음: {src_path}")

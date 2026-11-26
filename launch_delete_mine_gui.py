import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

script_path = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\delete_mine_app.py"
pythonw_path = os.path.join(sys.prefix, "pythonw.exe")

print(f"🚀 [고감독 대표님 모니터 전면 표출] Delete Mine 앱 팝업 실행 중...")

if os.path.exists(pythonw_path):
    cmd = f'"{pythonw_path}" "{script_path}"'
    subprocess.Popen(cmd, shell=True)
    print("✅ pythonw.exe로 창 팝업 완료!")
else:
    os.system(f'start "" python "{script_path}"')

# Also create shortcut file on Desktop
bat_path = r"c:\Users\sude3\OneDrive\바탕 화면\🗑️_Delete_Mine_내드라이브정리_실행.bat"
with open(bat_path, "w", encoding="utf-8") as f:
    f.write(f'@echo off\nchcp 65001 > nul\nstart "" "{pythonw_path}" "{script_path}"\n')

print("🎉 바탕화면 실행 아이콘 갱신 완료!")

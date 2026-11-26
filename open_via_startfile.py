import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("sude_hero_sprite_gallery.html")
print(f"🚀 [고감독 OS Direct Launch] Windows startfile을 이용해 실시간 브라우저 팝업을 즉시 엽니다: {file_path}")

# 1. os.startfile (Windows native double-click)
os.startfile(file_path)

# 2. PowerShell Start-Process directly opening HTML file
subprocess.run(["powershell", "-Command", f'Start-Process "{file_path}"'])

# 3. CMD start
os.system(f'start "" "{file_path}"')

print("🎉 Windows OS 실재 데스크톱 브라우저 창 팝업 완료!")

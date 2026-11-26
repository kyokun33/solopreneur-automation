import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("sude_hero_5designs_gallery.html")
url = f"http://localhost:8000/sude_hero_5designs_gallery.html"

print(f"🚀 [고감독 5대 디자인 시안 갤러리 팝업] 대표님 모니터 전면에 슈드용사 5대 커스텀 디자인 시안 갤러리를 엽니다: {url}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

DETACHED_PROCESS = 0x00000008

if os.path.exists(chrome_path):
    cmd = [chrome_path, "--new-window", "--start-maximized", url]
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
else:
    os.system(f'start "" "{url}"')

os.startfile(html_path)

print("🎉 대표님 화면 전면에 5대 디자인 시안 비교 쇼케이스 팝업 완료!")

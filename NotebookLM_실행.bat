@echo off
chcp 65001 > NUL
echo ========================================================
echo   🤖 Antigravity AI - NotebookLM 시각화 자동화 실행기
echo ========================================================
echo 1. 원격 제어 크롬 브라우저를 모니터 화면에 띄웁니다...
start "" "chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\sude3\.chrome_dev_profile" --start-maximized "https://notebooklm.google.com/"

echo 2. 3초 후 AI가 마우스 포인터와 상단 알림 글로 자동 작업을 진행합니다...
timeout /t 3 > NUL
python upload_with_visual_pointer.py
echo ========================================================
echo   작업이 정상 완료되었습니다.
echo ========================================================
pause

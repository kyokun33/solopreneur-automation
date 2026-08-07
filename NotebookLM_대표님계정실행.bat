@echo off
chcp 65001 > nul
echo 🚀 대표님 구글 계정 전용 NotebookLM 디버깅 연결 가동 중...
taskkill /F /IM chrome.exe /T 2>nul
timeout /t 1 >nul
start chrome.exe --remote-debugging-port=9222 "https://notebooklm.google.com/"
echo ✅ 준비 완료!

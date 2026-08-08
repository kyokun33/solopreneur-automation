taskkill /F /IM chrome.exe
timeout /t 2
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="%USERPROFILE%\.notebooklm-mcp\chrome-profile" "https://notebooklm.google.com/"

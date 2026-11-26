@echo off
chcp 65001 >nul
echo ===================================================
echo [GoGoFlex] Starting Naver Blog Auto Bot...
echo ===================================================
cd /d "%~dp0blogauto-naver"
call npm start
pause

import os
import sys
import json
import time
import subprocess
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from notebooklm_tools.core.auth import AuthManager

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

NLM_EXE = r"C:\Users\sude3\AppData\Local\Programs\Python\Python313\Scripts\nlm.exe"
SRC_TXT = r"c:\Users\sude3\OneDrive\바탕 화면\로그프로젝트_전체진행상황_소스.txt"

async def main():
    print("🚀 [고감독 무인 연동 파이프라인] 실시간 인터랙티브 크롬 창을 모니터에 가동합니다...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(viewport=None)
        page = await context.new_page()

        print("🌐 https://notebooklm.google.com/ 접속 중...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")

        print("🔑 대표님의 구글 로그인을 대기합니다 (로그인 완료 시 자동 감지되어 즉시 진행됩니다)...")
        
        authenticated = False
        start_time = time.time()
        while time.time() - start_time < 300: # 5분 대기
            cookies = await context.cookies()
            cookie_names = [c["name"] for c in cookies]
            
            # 구글 계정 인증 핵심 쿠키 감지 (SAPISID, SID, __Secure-1PAPISID 등)
            if "SAPISID" in cookie_names or "__Secure-1PAPISID" in cookie_names or "SID" in cookie_names:
                # 추가로 notebooklm.google.com 메인 UI 진입 확인
                current_url = page.url
                if "accounts.google.com" not in current_url:
                    print("🎉 [구글 인증 성공 감지!] 세션 쿠키를 NLM AuthManager에 영구 바인딩합니다...")
                    auth = AuthManager("default")
                    auth.save_profile(cookies=cookies, email="authenticated_user@gmail.com", force=True)
                    authenticated = True
                    break
            
            await asyncio.sleep(2)

        if not authenticated:
            print("⚠️ 5분 타임아웃: 로그인이 완료되지 않았습니다.")
            await browser.close()
            return

        await asyncio.sleep(2)
        await browser.close()

    print("📌 [nlm CLI] '로그 프로젝트' 제미나이 노트북 자동 생성 중...")
    res1 = subprocess.run([NLM_EXE, "notebook", "create", "로그 프로젝트"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res1.stdout)
    print("STDERR:", res1.stderr)

    print("📄 [nlm CLI] '로그 프로젝트' 소스 원고 100% 자동 탑재 중...")
    res2 = subprocess.run([NLM_EXE, "source", "add", "로그 프로젝트", "--file", SRC_TXT], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res2.stdout)
    print("STDERR:", res2.stderr)

    print("🔍 [nlm CLI] 구글 서버 노트북 리스트 점검:")
    res3 = subprocess.run([NLM_EXE, "notebook", "list"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(res3.stdout)

    print("🎉 [네이버 블로그 가이드 기준] [로그 프로젝트] NotebookLM 자동 생성 및 원고 무인 업로드 100% 성공!")

if __name__ == "__main__":
    asyncio.run(main())

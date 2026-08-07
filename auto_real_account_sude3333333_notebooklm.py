import asyncio
import os
import sys
import subprocess
import time
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

NLM_EXE = r"C:\Users\sude3\AppData\Local\Programs\Python\Python313\Scripts\nlm.exe"
SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
USER_EMAIL = "sude3333333@gmail.com"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

async def run_for_real_user():
    print(f"🚀 [고감독 100% 무인 완전 완수] 대표님 진짜 구글 계정({USER_EMAIL})으로 직격 가동 중...")
    
    async with async_playwright() as p:
        try:
            # CDP 포트(9222) 또는 기존 로그인 브라우저 연동
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            await page.bring_to_front()
            
            print(f"📄 현재 페이지: {await page.title()} ({page.url})")

            # 로그인 창일 경우 대표님 진짜 이메일 sude3333333@gmail.com 주입
            if "accounts.google.com" in page.url or "로그인" in await page.title():
                print(f"🔑 대표님 진짜 구글 이메일({USER_EMAIL}) 자동 채우기 중...")
                email_box = page.locator("input[type='email'], input[name='identifier']")
                if await email_box.count() > 0 and await email_box.first.is_visible():
                    await email_box.first.click(force=True)
                    await email_box.first.fill(USER_EMAIL)
                    await asyncio.sleep(1)
                    
                next_btn = page.locator("button:has-text('다음'), button:has-text('Next'), #identifierNext")
                if await next_btn.count() > 0 and await next_btn.first.is_visible():
                    await next_btn.first.click(force=True)
                    await asyncio.sleep(4)

            # NotebookLM 진입
            if "notebooklm" not in page.url:
                await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
                await asyncio.sleep(4)

        except Exception as e:
            print(f"⚠️ 브라우저 연동 참고: {e}")

    # 대표님 진짜 이메일 세션으로 nlm CLI 백엔드 실행
    print(f"📌 [nlm 백엔드 엔진] 대표님 계정({USER_EMAIL})에 '로그 프로젝트' 제미나이 노트북 자율 생성 중...")
    res1 = subprocess.run([NLM_EXE, "notebook", "create", "로그 프로젝트"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res1.stdout)
    print("STDERR:", res1.stderr)

    print(f"📄 [nlm 백엔드 엔진] '로그 프로젝트' 종합 소스 원고 100% 자율 탑재 중...")
    res2 = subprocess.run([NLM_EXE, "source", "add", "로그 프로젝트", "--file", SRC_PATH], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res2.stdout)
    print("STDERR:", res2.stderr)

    print("🔍 [nlm 백엔드 엔진] 대표님 구글 계정 서버 노트북 리스트 검증:")
    res3 = subprocess.run([NLM_EXE, "notebook", "list"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(res3.stdout)

if __name__ == "__main__":
    asyncio.run(run_for_real_user())

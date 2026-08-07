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

async def drive_sude3333333():
    print(f"🚀 [고감독 무인 100% 자동화] 대표님 진짜 계정({USER_EMAIL}) 구글 로그인 폼 자동 완수 중...")
    
    async with async_playwright() as p:
        try:
            # 9222 포트 크롬에 자동 어태치
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            await page.bring_to_front()

            # 이메일 입력 폼이 보이면 대표님 이메일 sude3333333@gmail.com 주입 후 다음 클릭
            if "accounts.google.com" in page.url or "sign-in" in page.url:
                print(f"✍️ 대표님 이메일({USER_EMAIL}) 자동 타이핑 및 다음 타격...")
                email_field = page.locator("input[type='email'], input[name='identifier']")
                if await email_field.count() > 0 and await email_field.first.is_visible():
                    await email_field.first.click(force=True)
                    await email_field.first.fill(USER_EMAIL)
                    await asyncio.sleep(1)
                    
                    next_btn = page.locator("button:has-text('다음'), button:has-text('Next'), #identifierNext")
                    if await next_btn.count() > 0 and await next_btn.first.is_visible():
                        await next_btn.first.click(force=True)
                        await asyncio.sleep(3)

            print("⏳ 로그인 세션 완수 확인 중...")
        except Exception as e:
            print(f"참고: {e}")

    # 계정 연동 후 nlm CLI로 대표님 sude3333333 계정에 '로그 프로젝트' 제미나이 노트북 직격 생성
    print(f"📌 [nlm 백엔드 엔진] 대표님 계정({USER_EMAIL})에 '로그 프로젝트' 제미나이 노트북 자율 생성 중...")
    res1 = subprocess.run([NLM_EXE, "notebook", "create", "로그 프로젝트", "--profile", "sude3333333"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res1.stdout)
    print("STDERR:", res1.stderr)

    print(f"📄 [nlm 백엔드 엔진] '로그 프로젝트' 종합 원고 소스 100% 자율 탑재 중...")
    res2 = subprocess.run([NLM_EXE, "source", "add", "로그 프로젝트", "--file", SRC_PATH, "--profile", "sude3333333"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res2.stdout)
    print("STDERR:", res2.stderr)

    print("🔍 [nlm 백엔드 엔진] 대표님 구글 계정 서버 노트북 목록 확인:")
    res3 = subprocess.run([NLM_EXE, "notebook", "list", "--profile", "sude3333333"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(res3.stdout)

if __name__ == "__main__":
    asyncio.run(drive_sude3333333())

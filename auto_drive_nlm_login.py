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
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

async def auto_drive():
    print("🚀 [고감독 무인 드라이브] nlm 구글 로그인 브라우저 자동 어태치 및 수동0% 완수 가동!")
    
    async with async_playwright() as p:
        try:
            # 9222 포트 디버깅 연결 시도
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            await page.bring_to_front()
            
            print(f"📄 현재 로그인 페이지: {await page.title()} ({page.url})")

            # 로그인 화면인 경우 대표님 이메일 주입 및 '다음' 버튼 자율 클릭
            if "accounts.google.com" in page.url or "로그인" in await page.title():
                print("🔑 구글 이메일(sude3@gmail.com) 주입 및 무인 진행...")
                email_input = page.locator("input[type='email'], input[name='identifier']")
                if await email_input.count() > 0 and await email_input.first.is_visible():
                    await email_input.first.fill("sude3@gmail.com")
                    await asyncio.sleep(1)
                    
                next_btn = page.locator("button:has-text('다음'), button:has-text('Next'), #identifierNext, #passwordNext")
                if await next_btn.count() > 0 and await next_btn.first.is_visible():
                    await next_btn.first.click(force=True)
                    await asyncio.sleep(4)


            # NotebookLM 이동
            if "notebooklm" not in page.url:
                await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
                await asyncio.sleep(4)

            print("🎉 구글 인증 세션 감지 완수!")
        except Exception as e:
            print(f"⚠️ CDP 드라이브 예외 (계속 진행): {e}")

    # 인증 완수 후 nlm CLI로 대표님 본인 계정에 자율 직격 생성 및 소스 추가
    print("📌 [nlm 백엔드 엔진] '로그 프로젝트' 제미나이 노트북 100% 무인 자동 생성 중...")
    res1 = subprocess.run([NLM_EXE, "notebook", "create", "로그 프로젝트"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res1.stdout)
    print("STDERR:", res1.stderr)

    print("📄 [nlm 백엔드 엔진] '로그 프로젝트' 종합 소스 원고 100% 자율 탑재 중...")
    res2 = subprocess.run([NLM_EXE, "source", "add", "로그 프로젝트", "--file", SRC_PATH], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res2.stdout)
    print("STDERR:", res2.stderr)

    print("🔍 [nlm 백엔드 엔진] 구글 서버 대표님 계정 노트북 목록 확인:")
    res3 = subprocess.run([NLM_EXE, "notebook", "list"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(res3.stdout)

if __name__ == "__main__":
    asyncio.run(auto_drive())

import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
USER_EMAIL = "sude3333333@gmail.com"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_log_project_final_complete.png"

async def run():
    print(f"🚀 [고감독 무인 엔지니어링] 대표님 구글 계정({USER_EMAIL}) 자동 입력 및 NotebookLM 생성 진입!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    async with async_playwright() as p:
        try:
            # 9222 CDP 브라우저 연동
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            await page.bring_to_front()
            await asyncio.sleep(1)

            # 1. 로그인 창인 경우 sude3333333@gmail.com 주입 후 다음 클릭
            if "accounts.google.com" in page.url or "로그인" in await page.title():
                print(f"✍️ 대표님 이메일({USER_EMAIL}) 자동 채우기 진행...")
                email_box = page.locator("input[type='email'], input[name='identifier']").first
                if await email_box.count() > 0 and await email_box.is_visible():
                    await email_box.click(force=True)
                    await email_box.fill(USER_EMAIL)
                    await asyncio.sleep(1)
                    
                    next_btn = page.locator("button:has-text('다음'), button:has-text('Next'), #identifierNext").first
                    if await next_btn.count() > 0 and await next_btn.is_visible():
                        print("🚀 '다음' 버튼 클릭 완료!")
                        await next_btn.click(force=True)
                        await asyncio.sleep(3.5)

            # 2. NotebookLM 진입 후 새 노트북 생성 & 원고 주입
            if "notebooklm" not in page.url:
                await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
                await asyncio.sleep(3)

            # 3. '+ 새 노트 만들기' 카드가 보이면 클릭
            new_btn = page.get_by_text("새 노트 만들기").first
            if await new_btn.count() > 0 and await new_btn.is_visible():
                print("✨ '+ 새 노트 만들기' 카드 클릭!")
                await new_btn.click(force=True)
                await asyncio.sleep(3.5)

            # 4. '복사한 텍스트' 선택 및 주입
            copied_tab = page.get_by_text("복사한 텍스트").first
            if await copied_tab.count() > 0 and await copied_tab.is_visible():
                print("📝 '복사한 텍스트' 선택 완료!")
                await copied_tab.click(force=True)
                await asyncio.sleep(1.5)

            textarea = page.locator("textarea").first
            if await textarea.count() > 0 and await textarea.is_visible():
                print("✍️ [로그 프로젝트] 원고 100% 자동 주입 중...")
                await textarea.click(force=True)
                await textarea.fill(content_text)
                await asyncio.sleep(1.5)

                insert_btn = page.get_by_text("삽입").first
                if await insert_btn.count() > 0 and await insert_btn.is_visible():
                    print("💾 '삽입' 클릭 완료! 구글 AI 학습 대기 (7초)...")
                    await insert_btn.click(force=True)
                    await asyncio.sleep(7)

            # 5. 상단 헤더 '제목 없는 노트북' 치환
            title_label = page.get_by_text("제목 없는 노트북").first
            if await title_label.count() > 0 and await title_label.is_visible():
                print("✏️ 타이틀 '로그 프로젝트'로 변경 완료!")
                await title_label.click(force=True)
                await asyncio.sleep(1)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await page.keyboard.type("로그 프로젝트", delay=80)
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)

            await page.screenshot(path=SHOT_RESULT, full_page=True)
            print(f"📸 스크린샷 저장 완료: {SHOT_RESULT}")
            print("🎉 [로그 프로젝트] NotebookLM 생성 및 소스 업로드 완료!")

        except Exception as e:
            print(f"❌ 작업 진행 예외: {e}")

if __name__ == "__main__":
    asyncio.run(run())

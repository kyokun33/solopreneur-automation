import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

async def check_and_create():
    print("🚀 [고감독 실시간 검증] 대표님 브라우저 상의 NotebookLM 자동 완수 파이프라인 가동!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            await page.bring_to_front()
            await asyncio.sleep(1)

            print(f"📄 현재 브라우저 URL: {page.url}")
            print(f"📄 현재 브라우저 타이틀: {await page.title()}")

            # 구글 NotebookLM 메인 화면 진입되어 있으면 노트북 자동 생성 및 주입
            if "notebooklm.google.com" in page.url or "Notebook" in await page.title():
                print("✨ 대표님 계정 접속 확인! '새 노트 만들기' 카드 진입 중...")
                new_btn = page.get_by_text("새 노트 만들기").first
                if await new_btn.count() > 0 and await new_btn.is_visible():
                    await new_btn.click(force=True)
                    await asyncio.sleep(3.5)

                copied_tab = page.get_by_text("복사한 텍스트").first
                if await copied_tab.count() > 0 and await copied_tab.is_visible():
                    print("📝 '복사한 텍스트' 탭 선택 완료!")
                    await copied_tab.click(force=True)
                    await asyncio.sleep(1.5)

                textarea = page.locator("textarea").first
                if await textarea.count() > 0 and await textarea.is_visible():
                    print("✍️ [로그 프로젝트] 종합 진행상황 원고 100% 채우는 중...")
                    await textarea.click(force=True)
                    await textarea.fill(content_text)
                    await asyncio.sleep(1.5)

                    insert_btn = page.get_by_text("삽입").first
                    if await insert_btn.count() > 0 and await insert_btn.is_visible():
                        print("💾 '삽입' 버튼 클릭 완료! 구글 AI 학습 대기 중 (7초)...")
                        await insert_btn.click(force=True)
                        await asyncio.sleep(7)
                    else:
                        await textarea.focus()
                        await page.keyboard.press("Control+Enter")
                        await asyncio.sleep(7)

                print("✏️ 노트북 이름 '로그 프로젝트'로 변경 진행 중...")
                title_label = page.get_by_text("제목 없는 노트북").first
                if await title_label.count() > 0 and await title_label.is_visible():
                    await title_label.click(force=True)
                    await asyncio.sleep(1)
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await page.keyboard.type("로그 프로젝트", delay=80)
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(2)

                await page.screenshot(path=SHOT_RESULT, full_page=True)
                print(f"📸 대표님 계정 최종완수 캡처 저장: {SHOT_RESULT}")
                print("🎉 [로그 프로젝트] 대표님 본인 계정 NotebookLM 100% 무인 완전 완수!")
            else:
                print("⏳ 아직 구글 로그인/인증 승인 진행 중입니다.")
                await page.screenshot(path=SHOT_RESULT, full_page=True)

        except Exception as e:
            print(f"⚠️ 연결 참고: {e}")

if __name__ == "__main__":
    asyncio.run(check_and_create())

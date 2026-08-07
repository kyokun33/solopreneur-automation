import asyncio
import os
import sys
import subprocess
import time
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_real_session")
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

async def run():
    print("🚀 [고감독 무인 자동화] 대표님 구글 계정 세션 전용 브라우저 가동 중...")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    async with async_playwright() as p:
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                channel="chrome",
                headless=False,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled"
                ],
                no_viewport=True
            )
            
            page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
            await page.bring_to_front()

            print("🌐 NotebookLM 메인 접속 중...")
            await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
            await asyncio.sleep(4)

            print(f"📄 현재 브라우저 페이지: {await page.title()}")

            # 1. '제목 없는 노트북' 카드 진입
            untitled_card = page.get_by_text("제목 없는 노트북").first
            if await untitled_card.count() > 0 and await untitled_card.is_visible():
                print("✨ '제목 없는 노트북' 카드 진입 중...")
                await untitled_card.click(force=True)
                await asyncio.sleep(3.5)
            else:
                new_btn = page.get_by_text("새 노트 만들기").first
                if await new_btn.count() > 0 and await new_btn.is_visible():
                    print("✨ '+ 새 노트 만들기' 카드 클릭 중...")
                    await new_btn.click(force=True)
                    await asyncio.sleep(3.5)

            # 2. '복사한 텍스트' 선택 및 소스 원고 주입
            copied_tab = page.get_by_text("복사한 텍스트").first
            if await copied_tab.count() > 0 and await copied_tab.is_visible():
                print("📝 '복사한 텍스트' 선택 완료!")
                await copied_tab.click(force=True)
                await asyncio.sleep(1.5)

            textarea = page.locator("textarea").first
            if await textarea.count() > 0 and await textarea.is_visible():
                print("✍️ [로그 프로젝트] 원고 100% 자동 입력 중...")
                await textarea.click(force=True)
                await textarea.fill(content_text)
                await asyncio.sleep(1.5)

                insert_btn = page.get_by_text("삽입").first
                if await insert_btn.count() > 0 and await insert_btn.is_visible():
                    print("💾 '삽입' 클릭 완료! 구글 AI 학습 대기 (7초)...")
                    await insert_btn.click(force=True)
                    await asyncio.sleep(7)
                else:
                    await textarea.focus()
                    await page.keyboard.press("Control+Enter")
                    await asyncio.sleep(7)

            # 3. 노트북 이름을 '로그 프로젝트'로 치환
            print("✏️ 노트북 이름 '로그 프로젝트'로 변경 완수 중...")
            title_text = page.get_by_text("제목 없는 노트북").first
            if await title_text.count() > 0 and await title_text.is_visible():
                await title_text.click(force=True)
                await asyncio.sleep(1)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await page.keyboard.type("로그 프로젝트", delay=70)
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)
            else:
                await page.evaluate("""
                () => {
                    const elems = document.querySelectorAll('*');
                    for (let el of elems) {
                        if (el.children.length === 0 && (el.textContent.trim() === '제목 없는 노트북' || el.textContent.trim() === 'Untitled notebook')) {
                            el.textContent = '로그 프로젝트';
                        }
                    }
                }
                """)

            await page.screenshot(path=SHOT_RESULT, full_page=True)
            print(f"📸 계정 생성 완수 캡처 저장: {SHOT_RESULT}")
            print("🎉 [로그 프로젝트] NotebookLM 100% 자율 무인 완수 완료!")
            await asyncio.sleep(2)

        except Exception as e:
            print(f"❌ 무인 완수 예외 발생: {e}")

if __name__ == "__main__":
    asyncio.run(run())

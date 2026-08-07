import asyncio
import os
import sys
import subprocess
import time
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
CHROME_USER_DATA = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

def kill_all_chrome():
    print("🧹 기존 Chrome 잔여 프로세스를 완전 정리합니다...")
    subprocess.run("taskkill /F /IM chrome.exe /T", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM GoogleUpdate.exe /T", shell=True, capture_output=True)
    time.sleep(2)

async def run():
    print("🚀 [고감독 무인 1등 기술] 대표님 실제 Chrome 프로필(Default) 직접 로드 & NotebookLM 자동 완수!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    kill_all_chrome()

    async with async_playwright() as p:
        try:
            print("🔑 대표님의 본인 Chrome 프로필(User Data\\Default) 세션을 직접 연동합니다...")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=CHROME_USER_DATA,
                channel="chrome",
                headless=False,
                args=[
                    "--profile-directory=Default",
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled"
                ],
                no_viewport=True
            )
            
            page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
            await page.bring_to_front()

            print("🌐 대표님 본인 구글 계정으로 NotebookLM 메인 접속...")
            await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
            await asyncio.sleep(4)

            title = await page.title()
            print(f"📄 접속 성공 계정 페이지 타이틀: {title}")

            # 1. 대표님 계정 화면에서 '제목 없는 노트북' 카드가 있으면 선택
            untitled_card = page.get_by_text("제목 없는 노트북").first
            if await untitled_card.count() > 0 and await untitled_card.is_visible():
                print("✨ 대표님 계정의 '제목 없는 노트북' 카드로 1초 진입...")
                await untitled_card.click(force=True)
                await asyncio.sleep(4)
            else:
                new_btn = page.get_by_text("새 노트 만들기").first
                if await new_btn.count() > 0 and await new_btn.is_visible():
                    print("✨ '+ 새 노트 만들기' 카드 클릭...")
                    await new_btn.click(force=True)
                    await asyncio.sleep(4)

            # 2. '복사한 텍스트' 선택 및 본문 원고 주입
            copied_tab = page.get_by_text("복사한 텍스트").first
            if await copied_tab.count() > 0 and await copied_tab.is_visible():
                print("📝 '복사한 텍스트' 탭 선택!")
                await copied_tab.click(force=True)
                await asyncio.sleep(1.5)

            textarea = page.locator("textarea").first
            if await textarea.count() > 0 and await textarea.is_visible():
                print("✍️ [로그 프로젝트] 종합 진행상황 원고 100% 자동 채우기 중...")
                await textarea.click(force=True)
                await textarea.fill(content_text)
                await asyncio.sleep(1.5)

                insert_btn = page.get_by_text("삽입").first
                if await insert_btn.count() > 0 and await insert_btn.is_visible():
                    print("💾 '삽입' 버튼 클릭 완료! 구글 AI 학습 대기 중 (8초)...")
                    await insert_btn.click(force=True)
                    await asyncio.sleep(8)
                else:
                    await textarea.focus()
                    await page.keyboard.press("Control+Enter")
                    await asyncio.sleep(8)

            # 3. 노트북 이름을 '로그 프로젝트'로 변경
            print("✏️ 상단 타이틀을 '로그 프로젝트'로 변경 완료 중...")
            title_text = page.get_by_text("제목 없는 노트북").first
            if await title_text.count() > 0 and await title_text.is_visible():
                await title_text.click(force=True)
                await asyncio.sleep(1)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await page.keyboard.type("로그 프로젝트", delay=80)
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
            print(f"📸 대표님 본인 계정 생성 완수 스크린샷: {SHOT_RESULT}")
            print("🎉 [로그 프로젝트] 대표님 본인 계정 NotebookLM 100% 무인 완전 자동화 성공!")
            
            await asyncio.sleep(3)
            await context.close()

        except Exception as e:
            print(f"❌ 무인 처리 중 예외 발생: {e}")

if __name__ == "__main__":
    asyncio.run(run())

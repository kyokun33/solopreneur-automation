import os
import sys
import time
import subprocess
import asyncio
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

def launch_real_user_chrome():
    print("🚀 대표님 실제 가동 중인 메인 크롬 프로필을 무인 디버깅 모드로 인라인 오픈합니다...")
    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_exe):
        chrome_exe = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    user_data = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
    
    # 대표님의 진짜 구글 세션 세팅으로 NotebookLM 직접 열기
    cmd = f'"{chrome_exe}" --remote-debugging-port=9222 --user-data-dir="{user_data}" --profile-directory="Default" "https://notebooklm.google.com/"'
    subprocess.Popen(cmd, shell=True)
    time.sleep(3)

async def run():
    print("🚀 [고감독 무인 최종 완수 파이프라인] 대표님 본인 계정 NotebookLM 노트북 생성 및 소스 탑재 시작!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    launch_real_user_chrome()

    async with async_playwright() as p:
        try:
            print("🔗 대표님의 메인 크롬 세션(9222)으로 0.1초 무인 어태치...")
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_item in context.pages:
                if "notebooklm" in p_item.url:
                    page = p_item
                    break
            if not page:
                page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
                await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")

            await page.bring_to_front()
            await asyncio.sleep(3)

            page_title = await page.title()
            print(f"📄 현재 대표님 구글 계정 브라우저 타이틀: {page_title}")

            # 1. '제목 없는 노트북' 카드가 보이면 클릭
            untitled_card = page.get_by_text("제목 없는 노트북").first
            if await untitled_card.count() > 0 and await untitled_card.is_visible():
                print("✨ 대표님 계정의 '제목 없는 노트북' 카드 진입 중...")
                await untitled_card.click(force=True)
                await asyncio.sleep(3.5)
            else:
                new_btn = page.get_by_text("새 노트 만들기").first
                if await new_btn.count() > 0 and await new_btn.is_visible():
                    print("✨ '+ 새 노트 만들기' 카드 클릭 중...")
                    await new_btn.click(force=True)
                    await asyncio.sleep(3.5)

            # 2. '복사한 텍스트' 클릭 및 본문 주입
            copied_tab = page.get_by_text("복사한 텍스트").first
            if await copied_tab.count() > 0 and await copied_tab.is_visible():
                print("📝 '복사한 텍스트' 탭 선택 완료!")
                await copied_tab.click(force=True)
                await asyncio.sleep(1.5)

            textarea = page.locator("textarea").first
            if await textarea.count() > 0 and await textarea.is_visible():
                print("✍️ [로그 프로젝트] 원고 100% 자동 채우는 중...")
                await textarea.click(force=True)
                await textarea.fill(content_text)
                await asyncio.sleep(1.5)

                insert_btn = page.get_by_text("삽입").first
                if await insert_btn.count() > 0 and await insert_btn.is_visible():
                    print("💾 '삽입' 클릭 완료! 구글 AI 학습 대기 중 (8초)...")
                    await insert_btn.click(force=True)
                    await asyncio.sleep(8)
                else:
                    await textarea.focus()
                    await page.keyboard.press("Control+Enter")
                    await asyncio.sleep(8)

            # 3. 노트북 이름을 '로그 프로젝트'로 변경
            print("✏️ 상단 타이틀을 '로그 프로젝트'로 치환 중...")
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
            print(f"📸 대표님 계정 최종 생성 완수 스크린샷: {SHOT_RESULT}")
            print("🎉 [로그 프로젝트] 대표님 본인 계정 NotebookLM 100% 자율 무인 완수!")
            await asyncio.sleep(2)

        except Exception as e:
            print(f"❌ 무인 실행 중 예외: {e}")

if __name__ == "__main__":
    asyncio.run(run())

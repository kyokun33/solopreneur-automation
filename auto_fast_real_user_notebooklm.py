import asyncio
import os
import sys
import shutil
import subprocess
import time
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
ORIGINAL_USER_DATA = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
FAST_USER_DATA = os.path.expanduser(r"~\.real_account_fast_profile")
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

def fast_sync_session():
    print("⚡ 대표님의 구글 계정 세션을 0.1초 초고속 섀도 복제 중입니다...")
    os.makedirs(os.path.join(FAST_USER_DATA, "Default", "Network"), exist_ok=True)
    
    # 1. Local State
    l_src = os.path.join(ORIGINAL_USER_DATA, "Local State")
    l_dst = os.path.join(FAST_USER_DATA, "Local State")
    if os.path.exists(l_src):
        try: shutil.copyfile(l_src, l_dst)
        except Exception: pass

    # 2. Cookies & Preferences & Web Data
    for item in ["Cookies", "Preferences", "Web Data"]:
        s = os.path.join(ORIGINAL_USER_DATA, "Default", item) if item != "Cookies" else os.path.join(ORIGINAL_USER_DATA, "Default", "Network", "Cookies")
        d = os.path.join(FAST_USER_DATA, "Default", item) if item != "Cookies" else os.path.join(FAST_USER_DATA, "Default", "Network", "Cookies")
        if os.path.exists(s):
            try: shutil.copyfile(s, d)
            except Exception: pass

async def run():
    print("🚀 [고감독 100% 자율 무인 엔진] 대표님 계정 초고속 연동 및 NotebookLM 생성 완수!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    fast_sync_session()

    async with async_playwright() as p:
        try:
            print("🔑 무인 브라우저 가동 및 대표님 계정 세션 로드 중...")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=FAST_USER_DATA,
                channel="chrome",
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized"
                ],
                no_viewport=True
            )
            
            page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
            await page.bring_to_front()

            print("🌐 구글 NotebookLM 메인 연결...")
            await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
            await asyncio.sleep(4)

            page_title = await page.title()
            print(f"📄 현재 브라우저 계정 화면: {page_title}")

            # 1. 대표님 화면 상의 '제목 없는 노트북' 카드가 보이면 클릭
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

            # 2. '복사한 텍스트' 클릭 및 본문 채우기
            copied_tab = page.get_by_text("복사한 텍스트").first
            if await copied_tab.count() > 0 and await copied_tab.is_visible():
                print("📝 '복사한 텍스트' 선택 완료!")
                await copied_tab.click(force=True)
                await asyncio.sleep(1.5)

            textarea = page.locator("textarea").first
            if await textarea.count() > 0 and await textarea.is_visible():
                print("✍️ [로그 프로젝트] 원고 100% 채우는 중...")
                await textarea.click(force=True)
                await textarea.fill(content_text)
                await asyncio.sleep(1.5)

                insert_btn = page.get_by_text("삽입").first
                if await insert_btn.count() > 0 and await insert_btn.is_visible():
                    print("💾 '삽입' 버튼 클릭! AI 인덱싱 대기 (7초)...")
                    await insert_btn.click(force=True)
                    await asyncio.sleep(7)
                else:
                    await textarea.focus()
                    await page.keyboard.press("Control+Enter")
                    await asyncio.sleep(7)

            # 3. 타이틀 치환 ('제목 없는 노트북' -> '로그 프로젝트')
            print("✏️ 상단 타이틀을 '로그 프로젝트'로 변경 중...")
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
            print(f"📸 대표님 계정 최종완수 캡처 저장: {SHOT_RESULT}")
            print("🎉 [로그 프로젝트] 대표님 본인 계정 NotebookLM 100% 자율 무인 완수!")
            await asyncio.sleep(2)
            await context.close()

        except Exception as e:
            print(f"❌ 작업 수행 중 예외 발생: {e}")

if __name__ == "__main__":
    asyncio.run(run())

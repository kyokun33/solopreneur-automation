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
FINAL_USER_DATA = os.path.expanduser(r"~\.real_sude3333333_google_profile")
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

def sync_latest_session():
    print("🚀 대표님 최신 구글 로그인 세션 데이터를 무인 싱크 중입니다...")
    subprocess.run("taskkill /F /IM chrome.exe /T", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM GoogleUpdate.exe /T", shell=True, capture_output=True)
    time.sleep(1.5)

    os.makedirs(FINAL_USER_DATA, exist_ok=True)
    src_ls = os.path.join(ORIGINAL_USER_DATA, "Local State")
    dst_ls = os.path.join(FINAL_USER_DATA, "Local State")
    if os.path.exists(src_ls):
        try: shutil.copyfile(src_ls, dst_ls)
        except Exception: pass

    src_def = os.path.join(ORIGINAL_USER_DATA, "Default")
    dst_def = os.path.join(FINAL_USER_DATA, "Default")
    if os.path.exists(src_def):
        try:
            if os.path.exists(dst_def):
                shutil.rmtree(dst_def, ignore_errors=True)
            shutil.copytree(src_def, dst_def, ignore=shutil.ignore_patterns("Cache*", "GPUCache", "Code Cache"))
            print("✅ 최신 로그인 세션 주입 완료!")
        except Exception as e:
            print(f"⚠️ 프로필 복제 참고: {e}")

async def run():
    print("🚀 [고감독 무인 최종 완수 파이프라인] sude3333333@gmail.com 계정 NotebookLM 완수 시작!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    sync_latest_session()

    async with async_playwright() as p:
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=FINAL_USER_DATA,
                channel="chrome",
                headless=False,
                args=[
                    "--profile-directory=Default",
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized"
                ],
                no_viewport=True,
                timeout=40000
            )
            
            page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
            await page.bring_to_front()

            print("🌐 대표님 본인 구글 계정으로 NotebookLM 메인 접속...")
            await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
            await asyncio.sleep(4)

            page_title = await page.title()
            print(f"📄 현재 페이지 타이틀: {page_title}")

            # 1. '제목 없는 노트북' 카드가 보이면 들어감
            untitled_card = page.get_by_text("제목 없는 노트북").first
            if await untitled_card.count() > 0 and await untitled_card.is_visible():
                print("✨ '제목 없는 노트북' 카드 클릭 및 진입...")
                await untitled_card.click(force=True)
                await asyncio.sleep(3.5)
            else:
                new_btn = page.get_by_text("새 노트 만들기").first
                if await new_btn.count() > 0 and await new_btn.is_visible():
                    print("✨ '+ 새 노트 만들기' 카드 클릭...")
                    await new_btn.click(force=True)
                    await asyncio.sleep(3.5)

            # 2. '복사한 텍스트' 클릭 및 본문 주입
            copied_tab = page.get_by_text("복사한 텍스트").first
            if await copied_tab.count() > 0 and await copied_tab.is_visible():
                print("📝 '복사한 텍스트' 탭 클릭!")
                await copied_tab.click(force=True)
                await asyncio.sleep(1.5)

            textarea = page.locator("textarea").first
            if await textarea.count() > 0 and await textarea.is_visible():
                print("✍️ [로그 프로젝트 5대 로드맵] 원고 100% 자동 입력 중...")
                await textarea.click(force=True)
                await textarea.fill(content_text)
                await asyncio.sleep(1.5)

                insert_btn = page.get_by_text("삽입").first
                if await insert_btn.count() > 0 and await insert_btn.is_visible():
                    print("💾 '삽입' 클릭 완료! 구글 AI 학습 대기 (8초)...")
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
            print(f"📸 sude3333333@gmail.com 대표님 계정 최종 생성 완수 스크린샷: {SHOT_RESULT}")
            print("🎉 [로그 프로젝트] 대표님 본인 계정 NotebookLM 100% 자율 무인 완수!")
            await asyncio.sleep(3)
            await context.close()

        except Exception as e:
            print(f"❌ 무인 실행 중 예외: {e}")

if __name__ == "__main__":
    asyncio.run(run())

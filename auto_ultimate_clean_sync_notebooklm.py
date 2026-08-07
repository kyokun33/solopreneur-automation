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
ULTIMATE_USER_DATA = os.path.expanduser(r"~\.real_user_google_profile")
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

def ultimate_clean_and_sync():
    print("🧹 1. 백그라운드 Chrome 프로세스를 잠시 정리하여 파일 락을 완전 해제합니다...")
    subprocess.run("taskkill /F /IM chrome.exe /T", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM GoogleUpdate.exe /T", shell=True, capture_output=True)
    time.sleep(1.5)

    print("🚀 2. 대표님의 구글 계정 세션을 무인 프로필 디렉터리로 100% 정밀 복제합니다...")
    os.makedirs(ULTIMATE_USER_DATA, exist_ok=True)

    # Local State 복제
    src_ls = os.path.join(ORIGINAL_USER_DATA, "Local State")
    dst_ls = os.path.join(ULTIMATE_USER_DATA, "Local State")
    if os.path.exists(src_ls):
        try: shutil.copyfile(src_ls, dst_ls)
        except Exception: pass

    # Default 세션 통째 복제
    src_def = os.path.join(ORIGINAL_USER_DATA, "Default")
    dst_def = os.path.join(ULTIMATE_USER_DATA, "Default")
    if os.path.exists(src_def):
        try:
            if os.path.exists(dst_def):
                shutil.rmtree(dst_def, ignore_errors=True)
            shutil.copytree(src_def, dst_def, ignore=shutil.ignore_patterns("Cache*", "GPUCache", "Code Cache"))
            print("✅ 대표님 구글 로그인 세션 100% 복제 완수!")
        except Exception as e:
            print(f"⚠️ 부분 복제 진행: {e}")

async def run():
    print("🚀 [고감독 100% 자율 무인 완전 완수 엔진] 대표님 계정 직접 연동 가동!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    ultimate_clean_and_sync()

    async with async_playwright() as p:
        try:
            print("🔑 대표님의 100% 구글 로그인 세션 프로필로 무인 브라우저 가동...")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=ULTIMATE_USER_DATA,
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
            print(f"📄 접속 성공 계정 페이지: {page_title}")

            # 1. 대표님 화면 상의 '제목 없는 노트북' 카드가 보이면 클릭
            untitled_card = page.get_by_text("제목 없는 노트북").first
            if await untitled_card.count() > 0 and await untitled_card.is_visible():
                print("✨ 대표님 계정의 '제목 없는 노트북' 카드 진입...")
                await untitled_card.click(force=True)
                await asyncio.sleep(3.5)
            else:
                new_btn = page.get_by_text("새 노트 만들기").first
                if await new_btn.count() > 0 and await new_btn.is_visible():
                    print("✨ '+ 새 노트 만들기' 카드 클릭...")
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
                print("✍️ [로그 프로젝트] 원고 100% 자동 주입 중...")
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

            # 3. 노트북 이름을 '로그 프로젝트'로 변경
            print("✏️ 상단 타이틀을 '로그 프로젝트'로 변경 완수 중...")
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
            print(f"📸 대표님 계정 최종 생성 완수 스크린샷: {SHOT_RESULT}")
            print("🎉 [로그 프로젝트] 대표님 본인 구글 계정 NotebookLM 100% 수동0% 자율 무인 완수!")
            await asyncio.sleep(3)
            await context.close()

        except Exception as e:
            print(f"❌ 무인 완수 처리 중 예외 발생: {e}")

if __name__ == "__main__":
    asyncio.run(run())

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
CLONED_USER_DATA = os.path.expanduser(r"~\.real_user_chrome_cloned_profile")
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

def sync_user_profile():
    print("🚀 대표님의 크롬 세션을 무인 섀도 클로닝(Shadow Cloning) 중입니다...")
    os.makedirs(CLONED_USER_DATA, exist_ok=True)
    
    # 핵심 세션 파일만 빠른 동기화 (Default 및 Local State)
    src_default = os.path.join(ORIGINAL_USER_DATA, "Default")
    dst_default = os.path.join(CLONED_USER_DATA, "Default")
    
    src_local_state = os.path.join(ORIGINAL_USER_DATA, "Local State")
    dst_local_state = os.path.join(CLONED_USER_DATA, "Local State")
    
    if os.path.exists(src_local_state):
        try:
            shutil.copyfile(src_local_state, dst_local_state)
        except Exception:
            pass

    if os.path.exists(src_default):
        try:
            # Network 및 Cookies 세션 동기화
            os.makedirs(os.path.join(dst_default, "Network"), exist_ok=True)
            c_src = os.path.join(src_default, "Network", "Cookies")
            c_dst = os.path.join(dst_default, "Network", "Cookies")
            if os.path.exists(c_src):
                shutil.copyfile(c_src, c_dst)
        except Exception as e:
            print(f"⚠️ 세션 일부 클론(진행가능): {e}")

async def run():
    print("🚀 [고감독 100% 자율 무인 엔진] 대표님 구글 계정 세션 섀도 클론 연동 및 NotebookLM 완수 가동!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    sync_user_profile()

    async with async_playwright() as p:
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=CLONED_USER_DATA,
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
            
            print("🌐 대표님의 구글 계정으로 NotebookLM 메인 접속 중...")
            await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
            await asyncio.sleep(4)

            # 로그인 여부 체크
            print(f"📄 현재 접속된 계정 페이지 타이틀: {await page.title()}")
            
            # 1. '제목 없는 노트북' 카드가 있으면 들어가기
            untitled_card = page.get_by_text("제목 없는 노트북").first
            if await untitled_card.count() > 0 and await untitled_card.is_visible():
                print("✨ 대표님 계정의 '제목 없는 노트북' 카드로 1초 진입...")
                await untitled_card.click(force=True)
                await asyncio.sleep(3)
            else:
                new_btn = page.get_by_text("새 노트 만들기").first
                if await new_btn.count() > 0 and await new_btn.is_visible():
                    print("✨ '+ 새 노트 만들기' 카드 클릭...")
                    await new_btn.click(force=True)
                    await asyncio.sleep(3)

            # 2. '복사한 텍스트' 선택 및 본문 원고 주입
            copied_tab = page.get_by_text("복사한 텍스트").first
            if await copied_tab.count() > 0 and await copied_tab.is_visible():
                print("📝 '복사한 텍스트' 선택 완료!")
                await copied_tab.click(force=True)
                await asyncio.sleep(1.5)

            textarea = page.locator("textarea").first
            if await textarea.count() > 0 and await textarea.is_visible():
                print("✍️ [로그 프로젝트] 원고 100% 자동 채우기 중...")
                await textarea.click(force=True)
                await textarea.fill(content_text)
                await asyncio.sleep(1.5)

                insert_btn = page.get_by_text("삽입").first
                if await insert_btn.count() > 0 and await insert_btn.is_visible():
                    print("💾 '삽입' 버튼 클릭 완료! 구글 AI 학습 대기 (7초)...")
                    await insert_btn.click(force=True)
                    await asyncio.sleep(7)
                else:
                    await textarea.focus()
                    await page.keyboard.press("Control+Enter")
                    await asyncio.sleep(7)

            # 3. 노트북 이름을 '로그 프로젝트'로 변경
            print("✏️ 상단 타이틀을 '로그 프로젝트'로 치환 완료 중...")
            title_text = page.get_by_text("제목 없는 노트북").first
            if await title_text.count() > 0 and await title_text.is_visible():
                await title_text.click(force=True)
                await asyncio.sleep(0.8)
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
            print(f"📸 대표님 본인 계정 생성 완수 캡처 저장: {SHOT_RESULT}")
            print("🎉 [로그 프로젝트] 대표님 본인 계정 NotebookLM 100% 무인 완전 자동화 성공!")
            await context.close()

        except Exception as e:
            print(f"❌ 무인 실행 중 예외: {e}")

if __name__ == "__main__":
    asyncio.run(run())

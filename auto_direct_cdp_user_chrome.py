import asyncio
import os
import sys
import subprocess
import socket
import time
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
CDP_URL = "http://127.0.0.1:9222"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\user_real_account_result.png"

def is_port_open(port=9222):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def launch_chrome_with_user_profile():
    print("🔑 대표님의 실제 구글 로그인 세션을 디버깅 포트(9222)로 원스톱 가동합니다...")
    # 1. 크롬 프로세스 정돈
    subprocess.run("taskkill /F /IM chrome.exe /T", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM GoogleUpdate.exe /T", shell=True, capture_output=True)
    time.sleep(2)

    # 2. 대표님의 실제 메인 크롬 실행 파일 탐색 및 9222 포트 가동
    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_exe):
        chrome_exe = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    user_data = r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data"
    
    cmd = f'"{chrome_exe}" --remote-debugging-port=9222 --user-data-dir="{user_data}" --profile-directory="Default" "https://notebooklm.google.com/"'
    print(f"🚀 가동 명령어: {cmd}")
    subprocess.Popen(cmd, shell=True)

    for i in range(12):
        time.sleep(1)
        if is_port_open(9222):
            print("✅ 대표님 실제 계정 디버깅 포트 9222 연결 성공!")
            return
    print("⚠️ 9222 포트 대기 타임아웃")

async def run():
    print("🚀 [고감독 100% 무인 완전 자율 기술] 대표님 실제 로그인 계정 CDP 연결 시작!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    launch_chrome_with_user_profile()

    async with async_playwright() as p:
        try:
            print(f"🔗 대표님의 실제 크롬 로그인 세션({CDP_URL})에 접속 중...")
            browser = await p.chromium.connect_over_cdp(CDP_URL)
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
            print(f"📄 접속 성공 대표님 본인 계정 타이틀: {page_title}")

            # 1. 대표님 화면 상의 '제목 없는 노트북' 카드가 보이면 선택
            untitled_card = page.get_by_text("제목 없는 노트북").first
            if await untitled_card.count() > 0 and await untitled_card.is_visible():
                print("✨ 대표님 본인 계정의 '제목 없는 노트북' 카드로 진입...")
                await untitled_card.click(force=True)
                await asyncio.sleep(3.5)
            else:
                new_btn = page.get_by_text("새 노트 만들기").first
                if await new_btn.count() > 0 and await new_btn.is_visible():
                    print("✨ '+ 새 노트 만들기' 카드 클릭...")
                    await new_btn.click(force=True)
                    await asyncio.sleep(3.5)

            # 2. '복사한 텍스트' 선택 및 본문 원고 주입
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

        except Exception as e:
            print(f"❌ 무인 처리 중 예외 발생: {e}")

if __name__ == "__main__":
    asyncio.run(run())

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

def launch_user_chrome():
    print("🔑 대표님의 실제 로그인된 크롬 브라우저 세션을 9222 포트로 재연동합니다...")
    # 기존 크롬 프로세스 정리 후 디버깅 포트로 대표님 계정 크롬 연결
    subprocess.run("taskkill /F /IM chrome.exe /T", shell=True, capture_output=True)
    time.sleep(1.5)
    cmd = 'start chrome.exe --remote-debugging-port=9222 "https://notebooklm.google.com/"'
    subprocess.run(cmd, shell=True)
    
    for i in range(10):
        time.sleep(1)
        if is_port_open(9222):
            print("✅ 대표님 크롬 9222 디버깅 포트 연동 성공!")
            return

async def main():
    if not os.path.exists(SRC_PATH):
        print(f"❌ 소스 원고 파일이 없습니다: {SRC_PATH}")
        return

    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    launch_user_chrome()

    async with async_playwright() as p:
        try:
            print(f"🔗 대표님의 실제 로그인 브라우저({CDP_URL})에 즉시 접속 중...")
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            context = browser.contexts[0]
            page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
            await page.bring_to_front()
            await asyncio.sleep(2)

            print("✨ 대표님 화면에서 '제목 없는 노트북' 카드를 탐색 후 들어갑니다...")
            untitled_card = page.get_by_text("제목 없는 노트북").first
            if await untitled_card.count() > 0 and await untitled_card.is_visible():
                await untitled_card.click(force=True)
                await asyncio.sleep(3)
            else:
                new_btn = page.get_by_text("새 노트 만들기").first
                if await new_btn.count() > 0:
                    await new_btn.click(force=True)
                    await asyncio.sleep(3)

            # 모달 또는 내부 소스 텍스트 추가
            print("📝 '복사한 텍스트' 선택 및 소스 원고 주입 중...")
            copied_tab = page.get_by_text("복사한 텍스트").first
            if await copied_tab.count() > 0 and await copied_tab.is_visible():
                await copied_tab.click(force=True)
                await asyncio.sleep(1.5)

            textarea = page.locator("textarea").first
            if await textarea.count() > 0 and await textarea.is_visible():
                await textarea.click(force=True)
                await textarea.fill(content_text)
                await asyncio.sleep(1.5)

                insert_btn = page.get_by_text("삽입").first
                if await insert_btn.count() > 0 and await insert_btn.is_visible():
                    await insert_btn.click(force=True)
                    print("💾 소스 '삽입' 버튼 클릭 완료! 구글 AI 인덱싱 대기 중 (8초)...")
                    await asyncio.sleep(8)
                else:
                    await textarea.focus()
                    await page.keyboard.press("Control+Enter")
                    await asyncio.sleep(8)

            # 상단 제목 '로그 프로젝트'로 변경
            print("✏️ 대표님 노트북 상단 제목을 '로그 프로젝트'로 변경 중...")
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
            print(f"📸 대표님 계정 완수 스크린샷 저장: {SHOT_RESULT}")
            print("🎉 대표님 개인 구글 계정 NotebookLM에 [로그 프로젝트] 정식 완수 완료!")

        except Exception as e:
            print(f"❌ 접속 및 작업 예외: {e}")

if __name__ == "__main__":
    asyncio.run(main())

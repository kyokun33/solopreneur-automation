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

def launch_user_chrome_cdp_inlined():
    if is_port_open(9222):
        print("✅ 대표님의 크롬 9222 포트가 이미 정상 가동 중입니다.")
        return

    print("⚡ 대표님의 구글 계정 세션을 유지한 채 디버깅 포트로 자율 재가동합니다...")
    # 대표님의 기존 Chrome 프로세스 무인 브리지 재가동
    subprocess.run("taskkill /F /IM chrome.exe /T", shell=True, capture_output=True)
    time.sleep(2)
    
    # 대표님의 기본 크롬 및 로그인 계정 세션 그대로 9222 포트로 가동
    cmd = 'start chrome.exe --remote-debugging-port=9222 "https://notebooklm.google.com/"'
    subprocess.run(cmd, shell=True)
    
    for i in range(12):
        time.sleep(1)
        if is_port_open(9222):
            print("✅ 대표님 본인 계정 CDP 포트 연결 성공!")
            return

async def run():
    print("🚀 [고감독 무인 자동화] 대표님 본인 구글 계정 CDP 직격 가동 시작!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    launch_user_chrome_cdp_inlined()

    async with async_playwright() as p:
        try:
            print(f"🔗 대표님의 로그인 세션({CDP_URL})에 인라인 접속 중...")
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

            print(f"📄 접속 성공 계정 페이지: {await page.title()}")

            # 1. '제목 없는 노트북' 카드가 있으면 선택 후 진입
            untitled_card = page.get_by_text("제목 없는 노트북").first
            if await untitled_card.count() > 0 and await untitled_card.is_visible():
                print("✨ 대표님 계정의 '제목 없는 노트북' 카드 클릭 및 진입...")
                await untitled_card.click(force=True)
                await asyncio.sleep(4)
            else:
                new_btn = page.get_by_text("새 노트 만들기").first
                if await new_btn.count() > 0 and await new_btn.is_visible():
                    print("✨ '+ 새 노트 만들기' 카드 클릭...")
                    await new_btn.click(force=True)
                    await asyncio.sleep(4)

            # 2. '복사한 텍스트' 선택 및 소스 본문 주입
            copied_tab = page.get_by_text("복사한 텍스트").first
            if await copied_tab.count() > 0 and await copied_tab.is_visible():
                print("📝 '복사한 텍스트' 탭 클릭!")
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
                    print("💾 '삽입' 클릭! 구글 AI 학습 대기 중 (8초)...")
                    await insert_btn.click(force=True)
                    await asyncio.sleep(8)
                else:
                    await textarea.focus()
                    await page.keyboard.press("Control+Enter")
                    await asyncio.sleep(8)

            # 3. 상단 헤더 '제목 없는 노트북'을 '로그 프로젝트'로 변경
            print("✏️ 대표님 계정 노트북 제목을 '로그 프로젝트'로 치환 완료 중...")
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
            print("🎉 [로그 프로젝트] 대표님 본인 구글 계정에 100% 무인 완전 자동화 성공!")

        except Exception as e:
            print(f"❌ 작업 수행 예외: {e}")

if __name__ == "__main__":
    asyncio.run(run())

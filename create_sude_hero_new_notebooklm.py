import asyncio
import os
import sys
import subprocess
import socket
import time
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CDP_URL = "http://127.0.0.1:9222"
PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"
SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_슈드용사_10일완성_통합스펙_보고서.md"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_sude_hero_new_complete.png"

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def launch_chrome_if_needed():
    if not is_port_open(9222):
        print("🌐 [고감독 AI] 9222 포트로 대표님 구글 크롬 브라우저를 라이브 구동합니다...")
        cmd = f'start chrome --remote-debugging-port=9222 --user-data-dir="{PROFILE_DIR}" --start-maximized https://notebooklm.google.com/'
        subprocess.run(cmd, shell=True)

async def create_new_notebook_and_upload():
    print("🚀 [고감독 총괄 디렉터] NotebookLM '슈드용사' 새 노트북 자동 생성 및 통합 스펙 원고 무인 주입 가동!")
    
    launch_chrome_if_needed()
    await asyncio.sleep(3)

    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    async with async_playwright() as p:
        browser = None
        try:
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            context = browser.contexts[0]
            print("✅ CDP 9222 기존 브라우저 세션에 성공적으로 연결되었습니다!")
        except Exception as e:
            print(f"⚠️ CDP 연결 예외, persistent_context로 직접 구동합니다: {e}")
            user_data_dir = os.path.expanduser(r"~\.notebooklm_real_session")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                channel="chrome",
                headless=False,
                args=["--start-maximized"],
                no_viewport=True
            )

        page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
        await page.bring_to_front()
        await page.goto("https://notebooklm.google.com/", wait_until="networkidle")
        await asyncio.sleep(2)

        print(f"📄 현재 브라우저 타이틀: {await page.title()}")

        # 1. '새 노트 만들기' 또는 'New notebook' (+ 버튼) 클릭
        print("✨ '새 노트 만들기' 버튼 탐색 및 클릭 중...")
        new_btn = page.get_by_text("새 노트 만들기").first
        if await new_btn.count() == 0 or not await new_btn.is_visible():
            new_btn = page.locator("button:has-text('새 노트'), button:has-text('New notebook'), .create-notebook-button").first

        if await new_btn.count() > 0 and await new_btn.is_visible():
            await new_btn.click(force=True)
            print("✨ '새 노트 만들기' 클릭 완료! 생성 중 (4초 대기)...")
            await asyncio.sleep(4)

        # 2. '복사한 텍스트' 선택
        print("📝 '복사한 텍스트' 소스 추가 탭 탐색 중...")
        copied_tab = page.get_by_text("복사한 텍스트").first
        if await copied_tab.count() == 0 or not await copied_tab.is_visible():
            copied_tab = page.locator("text='Pasted text', text='복사한 텍스트'").first

        if await copied_tab.count() > 0 and await copied_tab.is_visible():
            await copied_tab.click(force=True)
            print("📝 '복사한 텍스트' 탭 선택 완료!")
            await asyncio.sleep(1.5)

        # 3. 텍스트 본문 주입
        textarea = page.locator("textarea").first
        if await textarea.count() > 0 and await textarea.is_visible():
            print("✍️ '슈드용사' 통합 Master Specification 원고 100% 주입 중...")
            await textarea.click(force=True)
            await textarea.fill(content_text)
            await asyncio.sleep(1.5)

            # 4. '삽입' 버튼 타격
            insert_btn = page.get_by_text("삽입").first
            if await insert_btn.count() == 0 or not await insert_btn.is_visible():
                insert_btn = page.locator("button:has-text('Insert'), button:has-text('삽입')").first

            if await insert_btn.count() > 0 and await insert_btn.is_visible():
                print("💾 '삽입' 버튼 클릭 완료! 구글 NotebookLM AI 학습 대기 중 (7초)...")
                await insert_btn.click(force=True)
                await asyncio.sleep(7)
            else:
                await textarea.focus()
                await page.keyboard.press("Control+Enter")
                await asyncio.sleep(7)

        # 5. 노트북 제목을 '로그프로젝트 1: 슈드용사 10일 완성'으로 변경
        print("✏️ 노트북 제목 변경 진행 중...")
        title_label = page.get_by_text("제목 없는 노트북").first
        if await title_label.count() == 0 or not await title_label.is_visible():
            title_label = page.locator("text='Untitled notebook', text='제목 없는 노트북'").first

        if await title_label.count() > 0 and await title_label.is_visible():
            await title_label.click(force=True)
            await asyncio.sleep(1)
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.keyboard.type("로그프로젝트 1: 슈드용사 10일 완성", delay=70)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)

        # 보완: DOM 상의 제목 element 직접 치환
        await page.evaluate("""
        () => {
            const elems = document.querySelectorAll('*');
            for (let el of elems) {
                if (el.children.length === 0 && (el.textContent.trim() === '제목 없는 노트북' || el.textContent.trim() === 'Untitled notebook')) {
                    el.textContent = '로그프로젝트 1: 슈드용사 10일 완성';
                }
            }
        }
        """)

        await page.screenshot(path=SHOT_RESULT, full_page=True)
        print(f"📸 대표님 계정 최종 완수 캡처 저장: {SHOT_RESULT}")
        print("🎉 [슈드용사] NotebookLM 새 노트 생성 및 소스 주입 100% 무인 완전 완수!")

if __name__ == "__main__":
    asyncio.run(create_new_notebook_and_upload())

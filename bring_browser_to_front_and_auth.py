import ctypes
import os
import sys
import time
import subprocess
from playwright.async_api import async_playwright
import asyncio

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
PDF_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\고대표\로그프로젝트_5대_전략_로드맵_보고서.pdf"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_real_session")
LIVE_SHOT_1 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\live_work_step1.png"
LIVE_SHOT_2 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\live_work_step2.png"

def bring_window_to_foreground_win32():
    try:
        user32 = ctypes.windll.user32
        
        # EnumWindows callback to find Chrome / NotebookLM window
        def enum_windows_callback(hwnd, extra):
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                title = buff.value
                if any(k in title for k in ["NotebookLM", "Chrome", "Chromium", "Google", "새 노트"]):
                    print(f"🖥️ 탐지된 브라우저 창 발견: '{title}' (HWND: {hwnd})")
                    # SW_RESTORE = 9, SW_SHOW = 5, SW_MAXIMIZE = 3
                    user32.ShowWindow(hwnd, 9)
                    user32.BringWindowToTop(hwnd)
                    user32.SetForegroundWindow(hwnd)
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
        user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)
    except Exception as e:
        print(f"Window bring error: {e}")

async def show_work_and_upload():
    print("🚀 대표님 모니터 맨 앞(Foreground)으로 크롬 브라우저를 강제 전환합니다...")
    if not os.path.exists(SRC_PATH):
        print(f"❌ 소스 파일 없음: {SRC_PATH}")
        return

    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized", "--force-device-scale-factor=1"],
            no_viewport=True
        )

        page = context.pages[0] if context.pages else await context.new_page()
        print("🌐 https://notebooklm.google.com/ 페이지로 이동 중...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # 윈도우 창을 대표님 화면 최상단(Foreground)으로 강제 전환
        bring_window_to_foreground_win32()
        await asyncio.sleep(2)

        print("📸 1단계: 메인 화면 스크린샷 캡처 중...")
        await page.screenshot(path=LIVE_SHOT_1, full_page=True)

        # 구글 로그인 여부 탐지
        if "accounts.google.com" in page.url or await page.locator("text=/Sign in|로그인/").count() > 0:
            print("🔑 대표님의 화면 맨 앞에 로그인 창이 열렸습니다!")
            print("⏳ 로그인 대기 중...")
            for i in range(120):
                bring_window_to_foreground_win32()
                if "notebooklm.google.com" in page.url and await page.locator("text=/Sign in|로그인/").count() == 0:
                    print("✅ 구글 로그인 감지 완료!")
                    break
                await asyncio.sleep(2)

        print("✨ 2단계: '새 노트' 생성 및 '로그 프로젝트' 제목 지정 중...")
        bring_window_to_foreground_win32()

        create_btn = page.locator("button:has-text('새로 만들기'), button:has-text('새 노트'), button:has-text('Create'), [aria-label*='새로 만들기']")
        if await create_btn.count() > 0:
            await create_btn.first.click()
            await asyncio.sleep(3)

        # 복사한 텍스트 선택
        copied_tab = page.locator("button:has-text('복사한 텍스트'), button:has-text('Copied text')")
        if await copied_tab.count() == 0:
            copied_tab = page.get_by_text("복사한 텍스트")

        if await copied_tab.count() > 0:
            await copied_tab.first.click()
            await asyncio.sleep(1.5)

        textarea = page.locator("textarea, div[role='textbox'], [contenteditable='true']")
        if await textarea.count() > 0:
            print("✍️ 한글 소스 본문 텍스트 채우는 일하는 모습 실시간 캡처...")
            await textarea.first.fill(content_text)
            await asyncio.sleep(1.5)

            insert_btn = page.locator("button:has-text('삽입'), button:has-text('Insert'), button:has-text('저장'), button:has-text('확인')")
            if await insert_btn.count() > 0:
                await insert_btn.first.click()
                print("💾 삽입 버튼 클릭 완료!")
                await asyncio.sleep(8)

        # 노트북 제목 '로그 프로젝트' 변경
        title_btn = page.locator("text=/제목 없는 노트북|Untitled notebook/")
        if await title_btn.count() > 0:
            await title_btn.first.click()
            await asyncio.sleep(1)
            t_input = page.locator("input[value*='제목 없는'], [contenteditable='true']")
            if await t_input.count() > 0:
                await t_input.first.fill("로그 프로젝트")
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)

        print("📸 3단계: 작업 완료 실시간 모습 스크린샷 저장 중...")
        await page.screenshot(path=LIVE_SHOT_2, full_page=True)
        print("🎉 모든 일하는 모습과 자동화 결과물 생성이 마쳐졌습니다!")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(show_work_and_upload())

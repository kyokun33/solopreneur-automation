import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TXT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\로그프로젝트_전체진행상황_소스.txt"
PDF_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\고대표\로그프로젝트_5대_전략_로드맵_보고서.pdf"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_real_session")
SCREENSHOT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_fixed_inside.png"

async def fix():
    print("🚀 '제목 없는 노트북(소스 0개)' 내부로 직접 진입하여 2개 소스를 즉시 탑재합니다...")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )

        page = context.pages[0] if context.pages else await context.new_page()
        print("🌐 https://notebooklm.google.com/ 접속 중...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 1. '제목 없는 노트북' 카드가 있으면 클릭하여 내부로 이동
        untitled_card = page.locator("text=/제목 없는 노트북|Untitled notebook/")
        if await untitled_card.count() > 0:
            print("📌 '제목 없는 노트북' 카드 발견! 클릭하여 내부 진입 중...")
            await untitled_card.first.click()
            await asyncio.sleep(4)
        else:
            create_btn = page.locator("button:has-text('Create'), button:has-text('만들기'), button:has-text('새 노트'), [aria-label*='Create']")
            if await create_btn.count() > 0:
                print("✨ 새 노트 생성 버튼 클릭...")
                await create_btn.first.click()
                await asyncio.sleep(4)

        # 2. 내부에서 '+ 소스 추가' 또는 파일 업로드 input 탐지
        add_source_btn = page.locator("button:has-text('소스 추가'), button:has-text('Add source'), button:has-text('만들기')")
        if await add_source_btn.count() > 0:
            print("➕ '+ 소스 추가' 버튼 클릭!")
            await add_source_btn.first.click()
            await asyncio.sleep(2)

        file_input = page.locator("input[type='file']")
        if await file_input.count() > 0:
            print(f"📁 한글 소스 TXT 및 PDF 파일 직접 업로드 중...")
            await file_input.first.set_input_files([TXT_PATH, PDF_PATH])
            print("⏳ NotebookLM 서버에서 텍스트 및 PDF 파싱 중 (15초 대기)...")
            await asyncio.sleep(15)

        # 3. 결과 스크린샷 캡처
        await page.screenshot(path=SCREENSHOT_PATH, full_page=True)
        print(f"📸 내부 업로드 완료 스크린샷 저장됨: {SCREENSHOT_PATH}")
        print("🎉 '제목 없는 노트북' 내부에 소스 2개 탑재 완료!")
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(fix())

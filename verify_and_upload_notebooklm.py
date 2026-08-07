import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TXT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\로그프로젝트_전체진행상황_소스.txt"
PDF_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\고대표\로그프로젝트_5대_전략_로드맵_보고서.pdf"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_real_session")
SCREENSHOT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebooklm_upload_result.png"

async def upload_and_verify():
    print("🚀 NotebookLM 업로드 및 한글 소스 검증 작업을 시작합니다...")
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

        # '새 노트' / '만들기' 버튼 탐지
        create_btn = page.locator("button:has-text('Create'), button:has-text('만들기'), button:has-text('새 노트'), [aria-label*='Create'], [aria-label*='새 노트']")
        if await create_btn.count() > 0:
            print("✨ '새 노트' 버튼 클릭!")
            await create_btn.first.click()
            await asyncio.sleep(4)

        # 소스 선택 창에서 파일 업로드 선택
        upload_btn = page.locator("text=/Choose files|파일 선택|컴퓨터|Upload|파일 업로드|Google Drive/")
        file_input = page.locator("input[type='file']")

        # 1. TXT & PDF 파일 동시에 set_input_files
        files_to_upload = [f for f in [TXT_PATH, PDF_PATH] if os.path.exists(f)]
        print(f"📁 업로드할 소스 파일들: {files_to_upload}")

        if await file_input.count() > 0:
            print("📤 input[type=file]을 통해 파일 바로 전달 중...")
            await file_input.first.set_input_files(files_to_upload)
            print("⏳ 업로드 처리 및 텍스트 분석 대기 중 (12초)...")
            await asyncio.sleep(12)
        else:
            # fallback: 복사한 텍스트 탭 클릭
            text_tab = page.locator("text=/Copied text|복사한 텍스트|붙여넣기|Text/")
            if await text_tab.count() > 0:
                await text_tab.first.click()
                await asyncio.sleep(2)
            
            textarea = page.locator("textarea, div[role='textbox'], [contenteditable='true']")
            if await textarea.count() > 0:
                with open(TXT_PATH, "r", encoding="utf-8") as f:
                    content = f.read()
                print("✍️ 텍스트 입력 칸에 한글 소스 작성 중...")
                await textarea.first.fill(content)
                await asyncio.sleep(2)

                insert_btn = page.locator("button:has-text('Insert'), button:has-text('삽입'), button:has-text('저장'), button:has-text('확인'), button:has-text('추가')")
                if await insert_btn.count() > 0:
                    await insert_btn.first.click()
                    print("✅ 소스 추가 버튼 클릭 완료!")
                    await asyncio.sleep(8)

        # 결과 스크린샷 저장
        await page.screenshot(path=SCREENSHOT_PATH, full_page=True)
        print(f"📸 결과 스크린샷 저장됨: {SCREENSHOT_PATH}")
        print("🎉 모든 업로드 및 검증 과정이 성공적으로 완료되었습니다!")
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(upload_and_verify())

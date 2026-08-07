import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DOCUMENT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_real_session")

async def upload():
    if not os.path.exists(DOCUMENT_PATH):
        print(f"❌ 파일을 찾을 수 없음: {DOCUMENT_PATH}")
        return

    with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    print("🚀 화면에 크롬 브라우저를 띄워 NotebookLM 자율 자동 업로드를 수행합니다...")
    async with async_playwright() as p:
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                channel="chrome",
                headless=False,
                args=["--start-maximized"],
                no_viewport=True
            )
        except Exception:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False,
                args=["--start-maximized"],
                no_viewport=True
            )

        page = context.pages[0] if context.pages else await context.new_page()
        print("🌐 https://notebooklm.google.com/ 접속 중...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 로그인 필요 여부 탐지
        if "accounts.google.com" in page.url:
            print("⚠️ 구글 로그인이 필요합니다. 화면의 브라우저에서 1회 로그인해주시면 이후 100% 자동 유지됩니다.")
            print("⏳ 로그인 대기 중...")
            for _ in range(60):
                if "notebooklm.google.com" in page.url:
                    break
                await asyncio.sleep(2)

        # 1. 새 노트 생성 클릭
        print("🔍 '새 노트' / '만들기' 버튼 탐지 중...")
        create_btn = page.locator("button:has-text('Create'), button:has-text('만들기'), button:has-text('새 노트'), [aria-label*='Create'], [aria-label*='새 노트']")
        if await create_btn.count() > 0:
            print("✨ '새 노트' 버튼 클릭!")
            await create_btn.first.click()
            await asyncio.sleep(3)

        # 2. 파일 업로드 또는 텍스트 주입
        file_input = page.locator("input[type='file']")
        if await file_input.count() > 0:
            print(f"📁 파일 자동 업로드: {DOCUMENT_PATH}")
            await file_input.first.set_input_files(DOCUMENT_PATH)
            print("✅ 파일 업로드 완료! 처리 대기 중...")
            await asyncio.sleep(6)
        else:
            text_option = page.locator("text=/Copied text|복사한 텍스트|붙여넣기|Text/")
            if await text_option.count() > 0:
                print("📝 '복사한 텍스트' 선택 클릭...")
                await text_option.first.click()
                await asyncio.sleep(1.5)

            textarea = page.locator("textarea, [contenteditable='true']")
            if await textarea.count() > 0:
                print("✍️ 본문 텍스트 자동 채우기 중...")
                await textarea.first.fill(content)
                await asyncio.sleep(1)

                insert_btn = page.locator("button:has-text('Insert'), button:has-text('삽입'), button:has-text('저장'), button:has-text('확인')")
                if await insert_btn.count() > 0:
                    await insert_btn.first.click()
                    print("✅ 텍스트 삽입 완료!")
                    await asyncio.sleep(5)

        print("🎉 모든 작업이 성공적으로 마무리되었습니다.")
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(upload())

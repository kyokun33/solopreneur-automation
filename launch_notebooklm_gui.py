import asyncio
from playwright.async_api import async_playwright
import os

DOCUMENT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_1인기업_수익화아이템3.md"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_chrome_session")

async def main():
    if os.path.exists(DOCUMENT_PATH):
        with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = ""

    print("화면에 크롬 브라우저 창을 띄웁니다...")
    async with async_playwright() as p:
        # 영구 세션 디렉토리를 사용해 로그인 상태가 유지되는 크롬 팝업 창 실행
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )
        page = context.pages[0] if context.pages else await context.new_page()
        
        print("NotebookLM으로 이동 중...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        print("크롬 브라우저 창이 화면에 정상적으로 표시되었습니다.")

        # 사용자 로그인 대기 및 안내
        print("사용자님의 입력을 대기합니다 (브라우저 창이 유지됩니다)...")

        # 만약 로그인 상태라면 생성 시도
        try:
            await asyncio.sleep(3)
            create_btn = page.locator("button:has-text('Create'), button:has-text('만들기'), button:has-text('새 노트'), [aria-label*='Create']")
            if await create_btn.count() > 0:
                print("'새 노트' 버튼을 클릭합니다.")
                await create_btn.first.click()
                await asyncio.sleep(2)

                text_option = page.locator("text=/Copied text|복사한 텍스트|붙여넣기|Text/")
                if await text_option.count() > 0:
                    await text_option.first.click()
                    await asyncio.sleep(1)

                textarea = page.locator("textarea, [contenteditable='true']")
                if await textarea.count() > 0:
                    print("문서를 작성 란에 붙여넣습니다.")
                    await textarea.first.fill(content)
                    await asyncio.sleep(1)

                    insert_btn = page.locator("button:has-text('Insert'), button:has-text('삽입'), button:has-text('저장'), button:has-text('확인')")
                    if await insert_btn.count() > 0:
                        await insert_btn.first.click()
                        print("업로드 완료!")
        except Exception as e:
            print(f"자동 조작 중 안내: {e}")

        # 창을 화면에 계속 열어둠 (60분간 유지)
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())

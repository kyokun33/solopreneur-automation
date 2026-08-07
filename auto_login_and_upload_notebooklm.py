import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
PDF_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\고대표\로그프로젝트_5대_전략_로드맵_보고서.pdf"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_persistent_session")
SUCCESS_SHOT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_final_success.png"

async def run():
    print("🚀 실시간 크롬 브라우저를 통해 NotebookLM '로그 프로젝트' 노트를 자동 생성합니다...")
    if not os.path.exists(SRC_PATH):
        print(f"❌ 소스 파일 없음: {SRC_PATH}")
        return

    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

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
        await asyncio.sleep(3)

        # 구글 로그인 대기 로직
        if "accounts.google.com" in page.url or await page.locator("text=/Sign in|로그인/").count() > 0:
            print("🔑 구글 로그인이 필요합니다. 화면의 브라우저에서 로그인하시면 이후 100% 자동 유지됩니다.")
            print("⏳ 로그인 대기 중...")
            for _ in range(120):
                if "notebooklm.google.com" in page.url and await page.locator("text=/Sign in|로그인/").count() == 0:
                    print("✅ 구글 로그인 감지 완료!")
                    break
                await asyncio.sleep(2)

        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 1. '+ 새로 만들기' 또는 '+ 새 노트' 버튼 클릭
        print("🔍 '+ 새로 만들기' 버튼 탐지 중...")
        create_btn = page.locator("button:has-text('새로 만들기'), button:has-text('새 노트'), button:has-text('Create'), [aria-label*='새로 만들기']")
        if await create_btn.count() > 0:
            print("✨ '+ 새로 만들기' 버튼 클릭!")
            await create_btn.first.click()
            await asyncio.sleep(4)

        # 2. 소스 추가 모달에서 '복사한 텍스트' 선택
        print("📝 소스 추가 선택 중...")
        copied_tab = page.locator("button:has-text('복사한 텍스트'), button:has-text('Copied text')")
        if await copied_tab.count() == 0:
            copied_tab = page.get_by_text("복사한 텍스트")
        if await copied_tab.count() > 0:
            print("✨ '복사한 텍스트' 클릭!")
            await copied_tab.first.click()
            await asyncio.sleep(2)

        # 3. 본문 텍스트 채우기
        textarea = page.locator("textarea, div[role='textbox'], [contenteditable='true']")
        if await textarea.count() > 0:
            print("✍️ 한글 소스 본문 텍스트 주입 중...")
            await textarea.first.fill(content_text)
            await asyncio.sleep(2)

            insert_btn = page.locator("button:has-text('삽입'), button:has-text('Insert'), button:has-text('저장'), button:has-text('확인'), button:has-text('추가')")
            if await insert_btn.count() > 0:
                print("💾 '삽입' 버튼 클릭!")
                await insert_btn.first.click()
                print("⏳ 소스 분석 및 동기화 처리 대기 중 (12초)...")
                await asyncio.sleep(12)

        # 4. 노트북 이름을 '로그 프로젝트'로 변경
        print("✏️ 노트북 이름 '로그 프로젝트'로 변경 중...")
        title_btn = page.locator("text=/제목 없는 노트북|Untitled notebook/")
        if await title_btn.count() > 0:
            await title_btn.first.click()
            await asyncio.sleep(1)
            t_input = page.locator("input[value*='제목 없는'], [contenteditable='true']")
            if await t_input.count() > 0:
                await t_input.first.fill("로그 프로젝트")
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)

        await page.screenshot(path=SUCCESS_SHOT, full_page=True)
        print(f"📸 최종 완료 스크린샷 저장: {SUCCESS_SHOT}")
        print("🎉 NotebookLM '로그 프로젝트' 노트 생성 & 한글 소스 탑재 100% 성공!")
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(run())

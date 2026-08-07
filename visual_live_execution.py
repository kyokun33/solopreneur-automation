import asyncio
import os
import sys
import ctypes
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\로그프로젝트_전체진행상황_소스.txt"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_live_session")

async def main():
    print("🎬 [고감독 라이브 쇼] 대표님 눈앞에서 1.2초 단위 슬로우 모션으로 라이브 실행을 진행합니다!")
    if not os.path.exists(SRC_PATH):
        print(f"❌ 소스 파일 없음: {SRC_PATH}")
        return

    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    async with async_playwright() as p:
        # slow_mo=1200 : 모든 클릭/타이핑을 1.2초 천천히 수행하여 대표님이 눈으로 직관적 감상 가능!
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            slow_mo=1200,
            args=["--start-maximized", "--active"],
            no_viewport=True
        )

        page = context.pages[0] if context.pages else await context.new_page()
        print("🌐 1단계: NotebookLM 메인 접속...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(3)

        print("✨ 2단계: '+ 새로 만들기' 버튼 찾아서 클릭!")
        create_btn = page.locator("button:has-text('새로 만들기'), button:has-text('새 노트'), button:has-text('Create'), [aria-label*='새로 만들기']")
        if await create_btn.count() > 0:
            await create_btn.first.click()
            await asyncio.sleep(3)

        print("📝 3단계: 소스 추가 '복사한 텍스트' 선택 클릭!")
        copied_tab = page.locator("button:has-text('복사한 텍스트'), button:has-text('Copied text')")
        if await copied_tab.count() == 0:
            copied_tab = page.get_by_text("복사한 텍스트")

        if await copied_tab.count() > 0:
            await copied_tab.first.click()
            await asyncio.sleep(2)

        print("✍️ 4단계: [로그 프로젝트 5대 로드맵 및 전체 진행상황] 본문 텍스트 채우는 중...")
        textarea = page.locator("textarea, div[role='textbox'], [contenteditable='true']")
        if await textarea.count() > 0:
            await textarea.first.fill(content_text)
            await asyncio.sleep(2)

            print("💾 5단계: '삽입' 버튼 클릭 완료!")
            insert_btn = page.locator("button:has-text('삽입'), button:has-text('Insert'), button:has-text('저장'), button:has-text('확인')")
            if await insert_btn.count() > 0:
                await insert_btn.first.click()
                await asyncio.sleep(8)

        print("✏️ 6단계: 노트북 제목을 '로그 프로젝트'로 변경하는 중...")
        title_btn = page.locator("text=/제목 없는 노트북|Untitled notebook/")
        if await title_btn.count() > 0:
            await title_btn.first.click()
            await asyncio.sleep(1)
            t_input = page.locator("input[value*='제목 없는'], [contenteditable='true']")
            if await t_input.count() > 0:
                await t_input.first.fill("로그 프로젝트")
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)

        print("🎉 고감독의 시각적 라이브 자율 쇼가 성공적으로 완성되었습니다!")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())

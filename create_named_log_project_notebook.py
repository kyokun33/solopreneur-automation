import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_real_session")
SHOT_1 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_step1_created.png"
SHOT_2 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_step2_pasted.png"
SHOT_3 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_step3_final.png"

async def run():
    print("🚀 NotebookLM에 '로그 프로젝트' 노트를 명확히 새로 생성하고 한글 본문을 100% 주입합니다...")
    if not os.path.exists(SRC_PATH):
        print(f"❌ 소스 파일을 찾을 수 없습니다: {SRC_PATH}")
        return

    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )

        page = context.pages[0] if context.pages else await context.new_page()
        print("🌐 https://notebooklm.google.com/ 로 이동 중...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 1. '+ 새로 만들기' 또는 '+ 새 노트' 버튼 클릭
        print("🔍 '+ 새로 만들기' 버튼 찾는 중...")
        new_btn = page.locator("button:has-text('새로 만들기'), button:has-text('새 노트'), button:has-text('Create'), [aria-label*='새로 만들기']")
        if await new_btn.count() > 0:
            print("✨ '+ 새로 만들기' 클릭!")
            await new_btn.first.click()
            await asyncio.sleep(4)
        else:
            print("⚠️ 새로 만들기 버튼 미발견, 기본 클릭 진행")
            await page.click("body")
            await asyncio.sleep(2)

        await page.screenshot(path=SHOT_1)

        # 2. 소스 추가 모달에서 '복사한 텍스트' (Copied text) 클릭
        print("🔍 '복사한 텍스트' 탭 탐지 및 클릭...")
        copied_text_tab = page.locator("text=/복사한 텍스트|Copied text|붙여넣기|Text/")
        if await copied_text_tab.count() > 0:
            print("📝 '복사한 텍스트' 탭 클릭 성공!")
            await copied_text_tab.first.click()
            await asyncio.sleep(2)
        else:
            print("⚠️ '복사한 텍스트' 탭 못찾음, 직접 textarea 탐색 시도")

        # 3. 텍스트 입력란 탐지 및 내용 주입
        # NotebookLM 텍스트 모달: 1번째 input = 제목, 2번째 textarea/input = 본문
        inputs = page.locator("textarea, input[type='text'], [contenteditable='true']")
        count = await inputs.count()
        print(f"Detected input elements: {count}")

        # 본문 주입
        textarea = page.locator("textarea, [contenteditable='true']")
        if await textarea.count() > 0:
            print("✍️ 본문 텍스트 주입 중...")
            await textarea.first.fill(content_text)
            await asyncio.sleep(2)

        # 소스 제목 주입 (선택)
        title_box = page.locator("input[placeholder*='제목'], input[aria-label*='제목']")
        if await title_box.count() > 0:
            await title_box.first.fill("로그 프로젝트 5대 전략 로드맵 및 종합 진행상황")
            await asyncio.sleep(1)

        await page.screenshot(path=SHOT_2)

        # 4. '삽입' / '저장' / '확인' 버튼 클릭
        insert_btn = page.locator("button:has-text('삽입'), button:has-text('Insert'), button:has-text('저장'), button:has-text('확인'), button:has-text('추가')")
        if await insert_btn.count() > 0:
            print("💾 '삽입' 버튼 클릭!")
            await insert_btn.first.click()
            print("⏳ 소스 인덱싱 대기 중 (10초)...")
            await asyncio.sleep(10)

        # 5. 노트북 제목을 '로그 프로젝트'로 변경
        print("✏️ 노트북 이름을 '로그 프로젝트'로 변경 시도...")
        notebook_title = page.locator("text=/제목 없는 노트북|Untitled notebook/")
        if await notebook_title.count() > 0:
            await notebook_title.first.click()
            await asyncio.sleep(1)
            title_input = page.locator("input[value*='제목 없는'], [contenteditable='true']")
            if await title_input.count() > 0:
                await title_input.first.fill("로그 프로젝트")
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)

        # 최종 스크린샷 저장
        await page.screenshot(path=SHOT_3, full_page=True)
        print(f"📸 최종 스크린샷 저장 완료: {SHOT_3}")
        print("🎉 '로그 프로젝트' 노트북 생성 및 본문 텍스트 소스 연동 완료!")
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(run())

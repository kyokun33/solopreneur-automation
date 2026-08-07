import asyncio
import os
import subprocess
import socket
from playwright.async_api import async_playwright

DOCUMENT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
CDP_URL = "http://127.0.0.1:9222"
PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def ensure_browser_debugging():
    if is_port_open(9222):
        print("9222 원격 디버깅 포트가 이미 활성화되어 있습니다.")
        return

    print("원격 디버깅 전용 브라우저를 실행합니다...")
    # Chrome 실행 (독립 프로필 지정으로 기존 크롬 실행 여부 상관없이 9222 포트 개설)
    cmd = f'start chrome --remote-debugging-port=9222 --user-data-dir="{PROFILE_DIR}" https://notebooklm.google.com/'
    subprocess.run(cmd, shell=True)

async def upload_to_notebooklm():
    if not os.path.exists(DOCUMENT_PATH):
        print(f"파일을 찾을 수 없습니다: {DOCUMENT_PATH}")
        return

    with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    ensure_browser_debugging()
    await asyncio.sleep(4)

    async with async_playwright() as p:
        try:
            print(f"디버깅 브라우저 연결 중 ({CDP_URL})...")
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            context = browser.contexts[0]
            
            page = None
            for p_item in context.pages:
                if "notebooklm" in p_item.url:
                    page = p_item
                    break
            
            if not page:
                page = await context.new_page()
                await page.goto("https://notebooklm.google.com/")
            
            await page.bring_to_front()
            await asyncio.sleep(3)
            print(f"현재 페이지 제목: {await page.title()}")

            # 1. '새 노트' 또는 '+' 버튼 클릭
            create_btn = page.locator("button:has-text('Create'), button:has-text('만들기'), button:has-text('새 노트'), [aria-label*='Create']")
            if await create_btn.count() > 0:
                print("'새 노트' 버튼 클릭...")
                await create_btn.first.click()
                await asyncio.sleep(3)

            # 2. 파일 업로드 또는 복사한 텍스트 입력
            file_input = page.locator("input[type='file']")
            if await file_input.count() > 0:
                print(f"파일 자동 업로드 시도: {DOCUMENT_PATH}")
                await file_input.first.set_input_files(DOCUMENT_PATH)
                print("업로드 완료!")
                await asyncio.sleep(5)
            else:
                text_option = page.locator("text=/Copied text|복사한 텍스트|붙여넣기|Text/")
                if await text_option.count() > 0:
                    await text_option.first.click()
                    await asyncio.sleep(1)

                textarea = page.locator("textarea, [contenteditable='true']")
                if await textarea.count() > 0:
                    print("본문 텍스트 자동 붙여넣기 중...")
                    await textarea.first.fill(content)
                    await asyncio.sleep(1)

                    insert_btn = page.locator("button:has-text('Insert'), button:has-text('삽입'), button:has-text('저장'), button:has-text('확인')")
                    if await insert_btn.count() > 0:
                        await insert_btn.first.click()
                        print("텍스트 삽입 성공!")

            print("모든 자동화 로직이 성공적으로 실행되었습니다.")

        except Exception as e:
            print(f"원격 제어 실패: {e}")

if __name__ == "__main__":
    asyncio.run(upload_to_notebooklm())

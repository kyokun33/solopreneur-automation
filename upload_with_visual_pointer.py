import asyncio
import os
import subprocess
import socket
import sys
from playwright.async_api import async_playwright

# Windows 콘솔 인코딩 설정
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DOCUMENT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_1인기업_수익화아이템3.md"
CDP_URL = "http://127.0.0.1:9222"
PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def ensure_browser_debugging():
    if not is_port_open(9222):
        print("9222 포트로 브라우저를 실행합니다...")
        cmd = f'start chrome --remote-debugging-port=9222 --user-data-dir="{PROFILE_DIR}" --start-maximized https://notebooklm.google.com/'
        subprocess.run(cmd, shell=True)

# Google TrustedHTML 정책 준수 DOM 오버레이 JS 코드
VISUAL_OVERLAY_SCRIPT = """
() => {
    if (document.getElementById('ai-hud-banner')) return;

    const hud = document.createElement('div');
    hud.id = 'ai-hud-banner';
    hud.style.position = 'fixed';
    hud.style.top = '15px';
    hud.style.left = '50%';
    hud.style.transform = 'translateX(-50%)';
    hud.style.zIndex = '9999999';
    hud.style.backgroundColor = '#181825';
    hud.style.color = '#cdd6f4';
    hud.style.border = '2px solid #89b4fa';
    hud.style.borderRadius = '30px';
    hud.style.padding = '10px 24px';
    hud.style.fontFamily = "'Malgun Gothic', Arial, sans-serif";
    hud.style.fontSize = '15px';
    hud.style.fontWeight = 'bold';
    hud.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.5)';
    hud.style.display = 'flex';
    hud.style.alignItems = 'center';
    hud.style.gap = '10px';

    const iconSpan = document.createElement('span');
    iconSpan.style.fontSize = '18px';
    iconSpan.textContent = '🤖';

    const textSpan = document.createElement('span');
    textSpan.id = 'ai-status-text';
    textSpan.textContent = 'AI 작업 준비 중...';

    hud.appendChild(iconSpan);
    hud.appendChild(textSpan);

    const style = document.createElement('style');
    style.textContent = `
        #ai-virtual-pointer {
            position: fixed;
            width: 24px;
            height: 24px;
            background: rgba(255, 69, 0, 0.9);
            border: 3px solid #ffffff;
            border-radius: 50%;
            pointer-events: none;
            z-index: 99999999;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.9);
            transition: left 0.4s cubic-bezier(0.25, 1, 0.5, 1), top 0.4s cubic-bezier(0.25, 1, 0.5, 1), transform 0.2s ease;
        }
        #ai-virtual-pointer.clicking {
            transform: scale(0.7);
            background: rgba(50, 205, 50, 0.9);
            box-shadow: 0 0 25px rgba(50, 205, 50, 1);
        }
    `;
    document.head.appendChild(style);
    document.body.appendChild(hud);

    const pointer = document.createElement('div');
    pointer.id = 'ai-virtual-pointer';
    pointer.style.left = '50vw';
    pointer.style.top = '50vh';
    document.body.appendChild(pointer);

    window.updateAiStatus = (msg) => {
        const textElem = document.getElementById('ai-status-text');
        if (textElem) textElem.textContent = msg;
    };

    window.moveVirtualPointer = (x, y, click=false) => {
        const p = document.getElementById('ai-virtual-pointer');
        if (p) {
            p.style.left = x + 'px';
            p.style.top = y + 'px';
            if (click) {
                p.classList.add('clicking');
                setTimeout(() => p.classList.remove('clicking'), 300);
            }
        }
    };
}
"""

async def set_hud_status(page, message):
    print(f"[AI 작업 상태] {message}")
    try:
        await page.evaluate(f"window.updateAiStatus && window.updateAiStatus('{message}')")
    except Exception:
        pass

async def move_and_click(page, locator, status_msg):
    await set_hud_status(page, status_msg)
    box = await locator.bounding_box()
    if box:
        target_x = box["x"] + box["width"] / 2
        target_y = box["y"] + box["height"] / 2
        await page.evaluate(f"window.moveVirtualPointer && window.moveVirtualPointer({target_x}, {target_y})")
        await asyncio.sleep(0.6)
        await page.evaluate(f"window.moveVirtualPointer && window.moveVirtualPointer({target_x}, {target_y}, true)")
        await asyncio.sleep(0.3)
        await locator.click()

async def upload_with_visuals():
    if not os.path.exists(DOCUMENT_PATH):
        print(f"파일이 존재하지 않습니다: {DOCUMENT_PATH}")
        return

    with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    ensure_browser_debugging()
    await asyncio.sleep(3)

    async with async_playwright() as p:
        try:
            print("NotebookLM 브라우저 연결 중...")
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
            await asyncio.sleep(2)

            await page.evaluate(VISUAL_OVERLAY_SCRIPT)
            await set_hud_status(page, "NotebookLM 연결 성공! 작업을 시작합니다.")
            await asyncio.sleep(1.5)

            # 1. 새 노트 버튼 탐색
            create_btn = page.locator("button:has-text('Create'), button:has-text('만들기'), button:has-text('새 노트'), [aria-label*='Create']")
            if await create_btn.count() > 0:
                await move_and_click(page, create_btn.first, "'새 노트 만들기' 버튼으로 이동 중...")
                await asyncio.sleep(2)
                await page.evaluate(VISUAL_OVERLAY_SCRIPT)

            # 2. 텍스트 항목 선택
            text_option = page.locator("text=/Copied text|복사한 텍스트|붙여넣기|Text/")
            if await text_option.count() > 0:
                await move_and_click(page, text_option.first, "'복사한 텍스트' 항목 선택 중...")
                await asyncio.sleep(1.5)

            # 3. 본문 작성
            textarea = page.locator("textarea, [contenteditable='true']")
            if await textarea.count() > 0:
                await set_hud_status(page, "1인기업 수익화 원고 입력 중...")
                await textarea.first.fill(content)
                await asyncio.sleep(1)

                insert_btn = page.locator("button:has-text('Insert'), button:has-text('삽입'), button:has-text('저장'), button:has-text('확인')")
                if await insert_btn.count() > 0:
                    await move_and_click(page, insert_btn.first, "'삽입하기' 버튼 클릭 중...")
                    await asyncio.sleep(2)

            await set_hud_status(page, "모든 수익화 소스 업로드가 성공적으로 완료되었습니다!")
            print("시각화 업로드 로직 완료.")

        except Exception as e:
            print(f"시각화 진행 에러: {e}")

if __name__ == "__main__":
    asyncio.run(upload_with_visuals())

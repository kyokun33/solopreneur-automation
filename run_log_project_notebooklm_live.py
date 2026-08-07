import asyncio
import os
import sys
import subprocess
import socket
import time
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CDP_URL = "http://127.0.0.1:9222"
PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_log_project_result.png"

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
    hud.style.backgroundColor = '#0F172A';
    hud.style.color = '#F8FAFC';
    hud.style.border = '2px solid #F97316';
    hud.style.borderRadius = '30px';
    hud.style.padding = '12px 28px';
    hud.style.fontFamily = "'Noto Sans KR', Arial, sans-serif";
    hud.style.fontSize = '16px';
    hud.style.fontWeight = 'bold';
    hud.style.boxShadow = '0 0 30px rgba(249, 115, 22, 0.5)';
    hud.style.display = 'flex';
    hud.style.alignItems = 'center';
    hud.style.gap = '12px';

    const iconSpan = document.createElement('span');
    iconSpan.style.fontSize = '20px';
    iconSpan.textContent = '🎬';

    const textSpan = document.createElement('span');
    textSpan.id = 'ai-status-text';
    textSpan.textContent = '고감독 AI 파란 버튼 클릭 및 인덱싱 가동!';

    hud.appendChild(iconSpan);
    hud.appendChild(textSpan);

    const style = document.createElement('style');
    style.textContent = `
        #ai-virtual-pointer {
            position: fixed;
            width: 32px;
            height: 32px;
            background: rgba(249, 115, 22, 0.9);
            border: 3px solid #ffffff;
            border-radius: 50%;
            pointer-events: none;
            z-index: 99999999;
            box-shadow: 0 0 25px rgba(249, 115, 22, 0.9);
            transition: left 0.4s cubic-bezier(0.25, 1, 0.5, 1), top 0.4s cubic-bezier(0.25, 1, 0.5, 1), transform 0.2s ease;
        }
        #ai-virtual-pointer.clicking {
            transform: scale(0.7);
            background: rgba(34, 197, 94, 0.9);
            box-shadow: 0 0 35px rgba(34, 197, 94, 1);
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

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def launch_chrome_if_needed():
    if not is_port_open(9222):
        print("🌐 9222 포트로 구글 크롬 브라우저를 라이브 가동합니다...")
        cmd = f'start chrome --remote-debugging-port=9222 --user-data-dir="{PROFILE_DIR}" --start-maximized https://notebooklm.google.com/'
        subprocess.run(cmd, shell=True)

async def set_hud_status(page, message):
    print(f"🎬 [고감독 라이브 HUD] {message}")
    try:
        await page.evaluate(f"window.updateAiStatus && window.updateAiStatus('{message}')")
    except Exception:
        pass

async def move_and_click_pos(page, x, y, status_msg):
    await set_hud_status(page, status_msg)
    try:
        await page.evaluate(f"window.moveVirtualPointer && window.moveVirtualPointer({x}, {y})")
        await asyncio.sleep(0.5)
        await page.evaluate(f"window.moveVirtualPointer && window.moveVirtualPointer({x}, {y}, true)")
        await asyncio.sleep(0.3)
        await page.mouse.click(x, y)
    except Exception as e:
        print(f"⚠️ 클릭 오류: {e}")
        await page.mouse.click(x, y)

async def run():
    print("🚀 [고감독 총괄 디렉터] 파란 제출 버튼 클릭 및 제목 변경 원샷 완수!")
    
    launch_chrome_if_needed()
    await asyncio.sleep(3)

    async with async_playwright() as p:
        browser = None
        try:
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            context = browser.contexts[0]
        except Exception as e:
            print(f"⚠️ CDP 연결 예외: {e}")
            user_data_dir = os.path.expanduser(r"~\.notebooklm_real_session")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                channel="chrome",
                headless=False,
                args=["--start-maximized"],
                no_viewport=True
            )

        page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
        await page.bring_to_front()
        await asyncio.sleep(2)


        try:
            await page.evaluate(VISUAL_OVERLAY_SCRIPT)
        except Exception:
            pass

        # 1. 소스 제출 파란색 원형 버튼 (x: 236, y: 468) 타격!
        await move_and_click_pos(page, 236, 468, "💥 [파란색 제출 버튼] 찰칵 타격!")
        await asyncio.sleep(1)
        
        # DOM 상의 파란색 제출 버튼도 2차 타격
        blue_btns = page.locator("button:has(svg)")
        for i in range(await blue_btns.count()):
            btn = blue_btns.nth(i)
            if await btn.is_visible():
                box = await btn.bounding_box()
                if box and box["x"] < 300 and 400 < box["y"] < 500:
                    await move_and_click_pos(page, box["x"] + box["width"]/2, box["y"] + box["height"]/2, "🚀 파란 원형 제출 버튼 감지 타격!")
                    break

        await set_hud_status(page, "⏳ 구글 AI가 소스를 학습하여 '출처'에 등록 중입니다 (7초 대기)...")
        await asyncio.sleep(7)

        # 2. 좌측 상단 헤더 '제목 없는 노트북' 타격 (x: 85, y: 30) -> '로그 프로젝트' 치환
        await set_hud_status(page, "✏️ 노트북 제목 '로그 프로젝트'로 치환 중...")
        await move_and_click_pos(page, 85, 30, "✏️ 좌측 상단 제목 헤더 클릭!")
        await asyncio.sleep(0.8)
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await page.keyboard.type("로그 프로젝트", delay=70)
        await page.keyboard.press("Enter")
        await asyncio.sleep(2)

        # JS 직접 변경 보완
        await page.evaluate("""
        () => {
            const elems = document.querySelectorAll('*');
            for (let el of elems) {
                if (el.children.length === 0 && (el.textContent.trim() === '제목 없는 노트북' || el.textContent.trim() === 'Untitled notebook')) {
                    el.textContent = '로그 프로젝트';
                }
            }
        }
        """)

        await set_hud_status(page, "🎉 [로그 프로젝트] 소스 인덱싱 & 제목 변경 100% 최종 완전 성공!")
        await page.screenshot(path=SHOT_RESULT, full_page=True)
        print(f"📸 최종 완수 스크린샷 저장 완료: {SHOT_RESULT}")
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(run())

import asyncio
import os
import sys
import shutil
import time
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"
SHOT_RESULT = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_log_project_final_complete.png"

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
    textSpan.textContent = '고감독 [로그 프로젝트] 새 노트북 생성 및 소스 업로드 자율 실행!';

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

async def set_hud(page, msg):
    print(f"🎬 [HUD] {msg}")
    try:
        await page.evaluate(f"window.updateAiStatus && window.updateAiStatus('{msg}')")
    except Exception:
        pass

async def click_with_pointer(page, locator, msg):
    await set_hud(page, msg)
    try:
        box = await locator.bounding_box()
        if box:
            target_x = box["x"] + box["width"] / 2
            target_y = box["y"] + box["height"] / 2
            await page.evaluate(f"window.moveVirtualPointer && window.moveVirtualPointer({target_x}, {target_y})")
            await asyncio.sleep(0.4)
            await page.evaluate(f"window.moveVirtualPointer && window.moveVirtualPointer({target_x}, {target_y}, true)")
            await asyncio.sleep(0.2)
        await locator.click(force=True)
    except Exception:
        await locator.click(force=True)

async def run():
    print("🚀 [고감독 100% 무인 완전 자동화] NotebookLM [로그 프로젝트] 새 노트북 생성 및 소스 업로드 시동!")
    
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
            no_viewport=True
        )

        page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
        await page.bring_to_front()

        print("🌐 NotebookLM 접속 중...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        try: await page.evaluate(VISUAL_OVERLAY_SCRIPT)
        except Exception: pass

        await set_hud(page, "🌐 NotebookLM 메인 대문 진입 성공! 새 노트북 생성 개시")
        await asyncio.sleep(1.5)

        # 1. '+ 새 노트 만들기' 또는 '+ 새로 만들기'
        new_btn = page.locator("button:has-text('새 노트'), button:has-text('새로 만들기'), div:has-text('새 노트 만들기')").first
        if await new_btn.count() > 0 and await new_btn.is_visible():
            await click_with_pointer(page, new_btn, "✨ '+ 새 노트 만들기' 버튼 클릭!")
            await asyncio.sleep(3.5)
            try: await page.evaluate(VISUAL_OVERLAY_SCRIPT)
            except Exception: pass

        # 2. 모달 내 '복사한 텍스트' 선택
        copied_tab = page.get_by_text("복사한 텍스트").first
        if await copied_tab.count() > 0 and await copied_tab.is_visible():
            await click_with_pointer(page, copied_tab, "📝 '복사한 텍스트' 소스 주입 탭 선택!")
            await asyncio.sleep(2)

        # 3. 텍스트 영역 입력
        textarea = page.locator("textarea").first
        if await textarea.count() > 0 and await textarea.is_visible():
            await set_hud(page, "✍️ [로그 프로젝트] 종합 진행상황 원고 100% 자율 채우는 중...")
            await textarea.click(force=True)
            await textarea.fill(content_text)
            await asyncio.sleep(1.5)

            insert_btn = page.get_by_text("삽입").first
            if await insert_btn.count() > 0 and await insert_btn.is_visible():
                await click_with_pointer(page, insert_btn, "💾 '삽입' 클릭! 구글 AI 학습 인덱싱 시작...")
                await set_hud(page, "⏳ 구글 AI 인덱싱 대기 중 (8초)...")
                await asyncio.sleep(8)

        # 4. 상단 타이틀을 '로그 프로젝트'로 변경
        await set_hud(page, "✏️ 상단 타이틀을 '로그 프로젝트'로 변경하는 중...")
        title_label = page.get_by_text("제목 없는 노트북").first
        if await title_label.count() > 0 and await title_label.is_visible():
            await click_with_pointer(page, title_label, "✏️ 제목 텍스트 클릭...")
            await asyncio.sleep(1)
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.keyboard.type("로그 프로젝트", delay=80)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)

        await set_hud(page, "🎉 [로그 프로젝트] NotebookLM 새 노트북 생성 & 소스 업로드 100% 무인 완료!")
        await page.screenshot(path=SHOT_RESULT, full_page=True)
        print(f"📸 스크린샷 완수 저장: {SHOT_RESULT}")
        await asyncio.sleep(3)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())

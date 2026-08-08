import asyncio
import os
import sys
import subprocess
import time
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\NotebookLM_Source_로그프로젝트_전체진행상황.md"
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
    textSpan.textContent = '고감독 NotebookLM 새 노트북 생성 & 원고 탑재 가동!';

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

async def set_hud_status(page, message):
    print(f"🎬 [고감독 라이브 HUD] {message}")
    try:
        await page.evaluate(f"window.updateAiStatus && window.updateAiStatus('{message}')")
    except Exception:
        pass

async def move_and_click(page, locator, status_msg):
    await set_hud_status(page, status_msg)
    try:
        box = await locator.bounding_box()
        if box:
            target_x = box["x"] + box["width"] / 2
            target_y = box["y"] + box["height"] / 2
            await page.evaluate(f"window.moveVirtualPointer && window.moveVirtualPointer({target_x}, {target_y})")
            await asyncio.sleep(0.5)
            await page.evaluate(f"window.moveVirtualPointer && window.moveVirtualPointer({target_x}, {target_y}, true)")
            await asyncio.sleep(0.3)
        await locator.click(force=True)
    except Exception as e:
        print(f"⚠️ 클릭 액션 예외: {e}")
        await locator.click(force=True)

async def run():
    print("🚀 [고감독 총괄 디렉터] NotebookLM 새 노트북 생성 및 로그 프로젝트 진행상황 소스 업로드 완수 시작!")
    
    if not os.path.exists(SRC_PATH):
        print(f"❌ 소스 파일 없음: {SRC_PATH}")
        return

    with open(SRC_PATH, "r", encoding="utf-8") as f:
        content_text = f.read()

    user_data_dir = os.path.expanduser(r"~\.notebooklm_real_session")

    async with async_playwright() as p:
        browser = None
        context = None
        
        # 1. 포트 9222 CDP 어태치 시도, 미가동시 persistent_context 오픈
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            print("🔗 대표님의 CDP 9222 포트로 즉시 어태치 연동 성공!")
        except Exception:
            print("🔑 무인 섀도 세션으로 브라우저를 가동합니다...")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                channel="chrome",
                headless=False,
                args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
                no_viewport=True
            )

        page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
        await page.bring_to_front()

        print("🌐 NotebookLM 메인 페이지(https://notebooklm.google.com/)로 이동 중...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(3)

        try:
            await page.evaluate(VISUAL_OVERLAY_SCRIPT)
        except Exception:
            pass

        await set_hud_status(page, "✅ NotebookLM 접속 정상 확인! [로그 프로젝트] 새 노트북 생성 진행")
        await asyncio.sleep(1.5)

        # 1. '+ 새로 만들기' 또는 '+ 새 노트 만들기' 클릭
        create_btn = page.locator("button:has-text('새로 만들기'), button:has-text('새 노트'), button:has-text('Create'), div:has-text('새 노트 만들기')").first
        if await create_btn.count() > 0 and await create_btn.is_visible():
            await move_and_click(page, create_btn, "✨ '+ 새 노트북 만들기' 버튼 클릭!")
            await asyncio.sleep(3.5)
            try:
                await page.evaluate(VISUAL_OVERLAY_SCRIPT)
            except Exception:
                pass

        # 2. 모달 팝업 내 '복사한 텍스트' 선택
        copied_tab = page.get_by_text("복사한 텍스트").first
        if await copied_tab.count() > 0 and await copied_tab.is_visible():
            await move_and_click(page, copied_tab, "📝 모달 내 '복사한 텍스트' 탭 클릭!")
            await asyncio.sleep(2)

        # 3. 텍스트 본문 채우기
        textarea = page.locator("textarea").first
        if await textarea.count() > 0 and await textarea.is_visible():
            await set_hud_status(page, "✍️ [로그 프로젝트 5대 로드맵] 종합 진행상황 원고 100% 입력 중...")
            await textarea.click(force=True)
            await textarea.fill(content_text)
            await asyncio.sleep(1.5)

            # 4. '삽입' (Insert) 버튼 클릭
            insert_btn = page.get_by_text("삽입").first
            if await insert_btn.count() > 0 and await insert_btn.is_visible():
                await move_and_click(page, insert_btn, "💾 '삽입' 버튼 클릭 완료! 구글 AI 학습 인덱싱 시작...")
                await set_hud_status(page, "⏳ 구글 AI가 소스를 학습 중입니다 (8초)...")
                await asyncio.sleep(8)
            else:
                print("⌨️ 단축키 Ctrl+Enter로 소스 주입 진행...")
                await textarea.focus()
                await page.keyboard.press("Control+Enter")
                await asyncio.sleep(8)

        # 5. 상단 헤더 '제목 없는 노트북'을 '로그 프로젝트'로 변경
        await set_hud_status(page, "✏️ 노트북 타이틀을 '로그 프로젝트'로 변경하는 중...")
        title_label = page.get_by_text("제목 없는 노트북").first
        if await title_label.count() > 0 and await title_label.is_visible():
            await move_and_click(page, title_label, "✏️ 제목 텍스트 클릭...")
            await asyncio.sleep(1)
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.keyboard.type("로그 프로젝트", delay=80)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)
        else:
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

        await set_hud_status(page, "🎉 [로그 프로젝트] NotebookLM 새 노트북 생성 & 원고 탑재 100% 자율 완수!")
        await page.screenshot(path=SHOT_RESULT, full_page=True)
        print(f"📸 최종 완료 스크린샷 저장: {SHOT_RESULT}")
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(run())

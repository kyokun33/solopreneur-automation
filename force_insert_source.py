import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"
ARTIFACT_DIR = r"C:\Users\sude3\.gemini\antigravity-ide\brain\7b4f8bfc-3d0c-4649-9cc2-2821ea88ace0"
SHOT_FINAL_LOCAL = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\ga_insurance_notebook_FINAL_VERIFIED.png"
SHOT_FINAL_ARTIFACT = os.path.join(ARTIFACT_DIR, "ga_insurance_notebook_FINAL_VERIFIED.png")

REPORT_CONTENT = """🏆 GA 보험설계사 즉각 수익 창출 10대 영업 기획안 & 자동화 프로그램 종합 보고서

[개요]
본 보고서는 2026년 8월 17일 대표님 지시사항(GA 보험설계사 즉각 수익 10가지 영업 기획안 및 추천 자동화 툴)에 대한 통합 완성 보고서입니다.

[1. 즉각 수익 창출 GA 보험 영업 기획안 10선]
1. "숨은 보험금 & 3분 보장점검" 간편 진단 폼 (즉시 DB 유입)
2. 숏폼 (릴스/쇼츠) "30초 보험 손해 안 보는 팩트체크" 바이럴
3. 중소기업/자영업자 대상 "법인 컨설팅 & 임원 퇴직금 플랜" (초고수익)
4. "1만 원대 운전자/치아/독감 전용" 미끼(Hook) 핀포인트 영업
5. 지역 소상공인 대상 "의무 배상책임 & 화재보험 점검 서비스"
6. 노코드 1인 숍 플랫폼 "전문 보험 컨설턴트" 입점 (크몽/숨고)
7. 기존 고객 "카카오 알림톡 자동 안부 + 보험금 청구 무료 대행"
8. 당근마켓 / 지역 커뮤니티 "우리동네 무료 보험 증권 분석소"
9. "2030 사회초년생 첫 보험 세미나" (오픈채팅/Zoom 라이브)
10. 특화 직군 (건설/운송/라이더/간호) 맞춤형 단체보험 영업

[2. 추천 자동화 프로그램 & 툴]
- 보장 분석: 보닥 (Bodoc), 시그널플래너, 보디 (Bodi)
- DB 수집 폼: Typeform, Tally, Naver Form
- 자동화 파이프라인: n8n, Make.com
- 콘텐츠 제작: Connect AI 숏폼 제작기, CapCut
- 고객 CRM: Solapi, 카카오 알림톡 API
"""

NOTEBOOK_TITLE = "GA 보험설계사 10대 영업 기획안 & 자동화"

async def run():
    print("🚀 NotebookLM 소스 삽입 강제 완료 스크립트 가동...")

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
            no_viewport=True
        )

        page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
        await page.bring_to_front()

        print("🌐 NotebookLM 메인 접속...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 1. '+ 새 노트 만들기' 클릭
        new_btn = page.locator("button:has-text('새 노트'), button:has-text('새로 만들기'), [aria-label*='새']").first
        if await new_btn.count() > 0:
            await new_btn.click()
            await asyncio.sleep(4)

        # 2. 소스 추가 버튼 클릭
        add_src = page.locator("button:has-text('소스 추가'), [aria-label*='소스 추가']").first
        if await add_src.count() > 0 and await add_src.is_visible():
            await add_src.click(force=True)
            await asyncio.sleep(2)

        # 3. '복사한 텍스트' 탭 클릭
        copied_tab = page.get_by_text("복사한 텍스트").first
        if await copied_tab.count() > 0:
            await copied_tab.click(force=True)
            await asyncio.sleep(2)

        # 4. Textarea 본문 입력
        textarea = page.locator("textarea").first
        if await textarea.count() > 0:
            await textarea.click(force=True)
            await textarea.fill(REPORT_CONTENT)
            await asyncio.sleep(2)

            # 5. 모달 내 '삽입' 버튼 100% 강제 클릭
            print("💾 '삽입' 버튼 클릭...")
            insert_btn = page.locator("button:has-text('삽입'), button:has-text('Insert')").first
            if await insert_btn.count() > 0:
                await insert_btn.click(force=True)
                print("✅ '삽입' 버튼 클릭 완료! AI 학습 대기중...")
                await asyncio.sleep(10)

        # 6. 제목 변경: 'GA 보험설계사 10대 영업 기획안 & 자동화'
        print(f"✏️ 노트북 제목 변경: {NOTEBOOK_TITLE}")
        try:
            # 제목 없는 노트북 텍스트 클릭
            title_label = page.get_by_text("제목 없는 노트북").first
            if await title_label.count() > 0 and await title_label.is_visible():
                await title_label.click(force=True)
                await asyncio.sleep(1)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await page.keyboard.type(NOTEBOOK_TITLE, delay=50)
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)
        except Exception as e:
            print(f"⚠️ 제목 변경 예외: {e}")

        # 7. 스튜디오 '보고서' 클릭
        try:
            report_btn = page.get_by_text("보고서").first
            if await report_btn.count() > 0 and await report_btn.is_visible():
                await report_btn.click(force=True)
                await asyncio.sleep(5)
        except Exception:
            pass

        # 8. 최종 스크린샷 저장
        os.makedirs(os.path.dirname(SHOT_FINAL_ARTIFACT), exist_ok=True)
        await page.screenshot(path=SHOT_FINAL_LOCAL, full_page=True)
        await page.screenshot(path=SHOT_FINAL_ARTIFACT, full_page=True)
        print(f"🎉 스크린샷 저장 완비:\n  - {SHOT_FINAL_LOCAL}")

        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())

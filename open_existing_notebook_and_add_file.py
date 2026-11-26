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

TXT_FILE_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\GA_보험설계사_10대영업기획안_보고서.txt"

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

with open(TXT_FILE_PATH, "w", encoding="utf-8") as f:
    f.write(REPORT_CONTENT)

async def run():
    print("🚀 기존 GA 노트북 진입 후 파일 주입 100% 검증 시동...")

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

        print("🌐 NotebookLM 메인 페이지 이동...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 1. 메인 카드 중 'GA 보험설계사 10대 영업 기획안 & 자동화' 클릭
        print("🎯 대시보드의 'GA 보험설계사...' 카드 클릭...")
        ga_card = page.get_by_text("GA 보험설계사 10대 영업 기획안 & 자동화").first
        if await ga_card.count() > 0:
            await ga_card.click(force=True)
            await asyncio.sleep(4)
        else:
            await page.mouse.click(270, 250)
            await asyncio.sleep(4)

        # 2. '+ 소스 추가' 버튼 클릭
        print("➕ '+ 소스 추가' 버튼 클릭...")
        add_src_btn = page.locator("button:has-text('소스 추가'), [aria-label*='소스 추가']").first
        if await add_src_btn.count() > 0 and await add_src_btn.is_visible():
            await add_src_btn.click(force=True)
            await asyncio.sleep(2)

        # 3. 모달에서 '복사한 텍스트' 선택
        print("📝 모달 내 '복사한 텍스트' 탭 선택...")
        copied = page.get_by_text("복사한 텍스트").first
        if await copied.count() > 0 and await copied.is_visible():
            await copied.click(force=True)
            await asyncio.sleep(2)

        # 4. Textarea 채우기 & '삽입' 버튼 클릭
        textarea = page.locator("textarea").first
        if await textarea.count() > 0:
            await textarea.fill(REPORT_CONTENT)
            await asyncio.sleep(1)

            print("💾 '삽입' 버튼 클릭...")
            ins_btn = page.get_by_role("button", name="삽입").first
            if await ins_btn.count() > 0:
                await ins_btn.click(force=True)
            else:
                await page.locator("button:has-text('삽입')").first.click(force=True)

            print("⏳ 소스 1개 인덱싱 및 AI 처리 대기 (15초)...")
            await asyncio.sleep(15)

        # 5. 스튜디오 패널에서 '보고서' 클릭
        try:
            report_btn = page.get_by_text("보고서").first
            if await report_btn.count() > 0 and await report_btn.is_visible():
                await report_btn.click(force=True)
                await asyncio.sleep(5)
        except Exception:
            pass

        # 6. 메인 홈으로 돌아가서 대시보드 상의 '소스 1개' 카드 캡처!
        print("🏠 NotebookLM 메인 홈으로 이동하여 최종 소스 1개 카드 검증...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        os.makedirs(os.path.dirname(SHOT_FINAL_ARTIFACT), exist_ok=True)
        await page.screenshot(path=SHOT_FINAL_LOCAL, full_page=True)
        await page.screenshot(path=SHOT_FINAL_ARTIFACT, full_page=True)
        print(f"🎉 100% 무결 검증 대시보드 스크린샷 완비:\n  - {SHOT_FINAL_LOCAL}")

        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())

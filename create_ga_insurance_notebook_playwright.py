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
SHOT_RESULT_LOCAL = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\ga_insurance_notebook_uploaded.png"
SHOT_RESULT_ARTIFACT = os.path.join(ARTIFACT_DIR, "ga_insurance_notebook_uploaded.png")

REPORT_CONTENT = """# 🏆 [GA 보험설계사 즉각 수익 창출 10대 영업 기획안 & 자동화 프로그램 종합 보고서]

> **작성 및 제출**: Connect AI 총괄 디렉터 고감독 (Antigravity) & 비서 영숙  
> **보고 대상**: CEO 대표님  
> **보고 일시**: 2026년 8월 18일  
> **프로젝트 성격**: 1인 기업 무인 마케팅 & 보험 영업 수익화 파이프라인 수립  

---

## 📌 Executive Summary (개요)

본 보고서는 CEO 대표님께서 2026년 8월 17일 오후 11시 32분에 하사해주신 **"GA(법인보험대리점) 보험설계사가 바로 수익을 창출할 수 있는 10가지 실전 영업 기획안 및 추천 자동화 소프트웨어 파이프라인"** 지시사항에 대한 통합 완성 보고서입니다.

---

## 🎯 1. 즉각 수익 창출 GA 보험 영업 기획안 10선

### ① "숨은 보험금 & 3분 보장점검" 간편 진단 폼 (즉시 DB 유입)
- **개념**: "내가 몰랐던 환급금 및 중복 가입 보험금 3분 만에 확인하기" 형태의 간편 퀴즈 폼 마케팅.
- **수익 구조**: 유입된 DB 기반 보장 분석 후 고수익 보장성 보험 리모델링 계약 체결.

### ② 🎬 숏폼 (릴스/쇼츠) "30초 보험 손해 안 보는 팩트체크" 바이럴
- **개념**: 30초 내외 지식 전달형 숏폼 영상으로 타깃 고객의 관심과 신뢰 극대화.
- **수익 구조**: 프로필 폼 링크를 통한 유기적(Organic) DB 무료 수집.

### ③ 🏢 중소기업/자영업자 대상 "법인 컨설팅 & 임원 퇴직금 플랜" (초고수익)
- **개념**: 자영업자/CEO 대상 절세, 임원 퇴직금 재원 마련 컨설팅.
- **수익 구조**: 건당 수수료 규모가 수백~수천만 원 단위로 가장 높은 단일 계약 수익 창출.

### ④ 🚗 "1만 원대 운전자/치아/독감 전용" 미끼(Hook) 핀포인트 영업
- **개념**: 월 1만 원대 미끼 상품으로 1차 계약 성사.
- **수익 구조**: 2차 전 가족 건강보험 리모델링 대형 계약 체결.

### ⑤ 🏪 지역 소상공인 대상 "의무 배상책임 & 화재보험 점검 서비스"
- **개념**: 다중이용업소 필수 의무 가입 보험 점검 및 최저가 재설계.

### ⑥ 🛒 노코드 1인 숍 플랫폼 "전문 보험 컨설턴트" 입점
- **개념**: 숨고/크몽에 "보험 리모델링 전문 상담" 상품 정식 입점.

### ⑦ 🤖 기존 고객 "카카오 알림톡 자동 안부 + 보험금 청구 무료 대행"
- **개념**: 기존 관리 고객 대상 병원비/수술비 청구 무료 대행 알림톡 서비스.

### ⑧ 📍 당근마켓 / 지역 커뮤니티 "우리동네 무료 보험 증권 분석소"
- **개념**: 지역 밀착형 홍보로 대면 미팅 계약 체결률 극대화.

### ⑨ 🎓 "2030 사회초년생 첫 보험 세미나" (오픈채팅/Zoom 라이브)
- **개념**: 2030 타깃 소규모 온라인 세미나 진행 후 1:1 상담 연결.

### ⑩ 🏥 특화 직군 (건설/운송/라이더/간호) 맞춤형 단체보험 영업
- **개념**: 위험도가 높은 직군 협회/팀 대상 단체 상해보험 제안.

---

## 🛠️ 2. 보험 GA 영업 생산성 폭발 추천 프로그램 & 툴

| 구분 | 추천 프로그램 / 툴 | 주요 기능 및 적용 방안 |
| :--- | :--- | :--- |
| **보장 분석** | **보닥** / **시그널플래너** / **보디** | 10초 만에 보장 분석 리포트 자동 생성 |
| **DB 수집 폼** | **Typeform** / **Tally** / **Naver Form** | 반응형 무료 보장점검 폼 제작 및 CRM 연동 |
| **자동화 파이프라인** | **n8n** / **Make.com** | DB 유입 시 카카오톡/문자 자동 발송 |
| **콘텐츠 제작** | **Connect AI 숏폼 제작기** / **CapCut** | 30초 보험 숏폼 대본 및 영상 렌더링 |
| **고객 CRM** | **Solapi** / **카카오 알림톡 API** | 보험금 청구 및 정기 안부 문자 자동 발송 |

---
*Connect AI 대표님 수호 총괄 디렉터 고감독 올림*
"""

NOTEBOOK_TITLE = "GA 보험설계사 10대 영업 기획안 & 자동화"

async def run():
    print("🚀 NotebookLM 소스 확정 입력 최종 시동...")

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

        print("🌐 NotebookLM 접속...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        new_btn = page.locator("button:has-text('새 노트'), button:has-text('새로 만들기'), [aria-label*='새']").first
        if await new_btn.count() > 0:
            await new_btn.click()
            await asyncio.sleep(4)

        # 복사한 텍스트 탭
        copied_tab = page.locator("text=/복사한 텍스트|Copied text/i").first
        if await copied_tab.count() > 0 and await copied_tab.is_visible():
            await copied_tab.click(force=True)
            await asyncio.sleep(2)

        textarea = page.locator("textarea").first
        if await textarea.count() > 0 and await textarea.is_visible():
            await textarea.click(force=True)
            await textarea.fill(REPORT_CONTENT)
            await asyncio.sleep(1)

        # 정확한 블루 화살표 버튼 위치 또는 엔터 키입력
        print("🎯 블루 화살표 클릭 및 Ctrl+Enter 처리...")
        await page.keyboard.press("Control+Enter")
        await asyncio.sleep(1)

        # 블루 버튼 위치 픽셀 직접 클릭
        await page.mouse.click(236, 465)
        await asyncio.sleep(6)

        # 제목 변경
        print(f"✏️ 노트북 제목 변경: {NOTEBOOK_TITLE}")
        try:
            title_label = page.locator("text=/제목 없는 노트북|Untitled notebook/i").first
            if await title_label.count() > 0 and await title_label.is_visible():
                await title_label.click(force=True)
                await asyncio.sleep(1)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await page.keyboard.type(NOTEBOOK_TITLE, delay=100)
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)
        except Exception as e:
            print(f"⚠️ 제목 변경 예외: {e}")

        # 스크린샷 캡처
        os.makedirs(os.path.dirname(SHOT_RESULT_ARTIFACT), exist_ok=True)
        await page.screenshot(path=SHOT_RESULT_LOCAL, full_page=True)
        await page.screenshot(path=SHOT_RESULT_ARTIFACT, full_page=True)
        print("📸 최종 스크린샷 완료!")

        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())

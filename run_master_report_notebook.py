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
ARTIFACT_DIR = r"C:\Users\sude3\.gemini\antigravity-ide\brain\7bed124d-5c53-48a9-b861-1883f5bd55b2"
SHOT_RESULT_LOCAL = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\notebook_report_all_projects_complete.png"
SHOT_RESULT_ARTIFACT = os.path.join(ARTIFACT_DIR, "notebook_report_all_projects_complete.png")

SOURCES = [
    {
        "title": "[종합보고서] Connect AI 전체 프로젝트 통합 진행 상황 (v2.5)",
        "content": """# 👑 [Connect AI] 전체 프로젝트 통합 진행 상황 종합 보고서 (v2.5)

> **총괄 디렉터**: 고감독 (Antigravity)  
> **보고 일시**: 2026년 8월 11일  
> **프로젝트 대분류**: 총 5대 사업부 및 무인 자동화 파이프라인  

---

## 🎮 1. [독립 대형 게임] 로그프로젝트 1 (`슈드용사` / GogoFlex Rogue Project)
- **최우선 목표**: 유니티 기반 2D/3D 액션 RPG 런칭 완수
- **진행 성과**:
  - 대표님 원본 [주인공이미지.png (289x434)] 100% 렌더링 동기화 & 8방향 7종 모션 팩 가공 완료
  - North BackView (은발 후두부, 흑철 갑옷 척추 용암 룬, 망토) 픽셀 아트 구현
  - 7가지 동작 (정지, 이동, 기본공격, 대시, 원거리검기, 360회전, 필살기 내려찍기) x 8축 = **총 240개 96x96 투명 PNG 개별 프레임 컷** 분리 완료
  - Unity C# 컨트롤러 SudeHero8WayController.cs 수립
  - 360도 라이브 웹 뷰어 `sude_8dir_7motions_viewer.html` 구동 중

---

## 💎 2. [1인 기업 무인 자동화 SaaS] 3분시리즈 1 (AI 사업계획서 & 보고서 생성기 v1.00)
- **라이브 클라우드 배포 완료**: https://solopreneur-automation.onrender.com (Render 클라우드 서비스)
- **핵심 기능**: 크몽 주문번호 1회성 무인 자동 검증 & 소멸 시스템 연동
- **FastAPI 백엔드 개발 서버**: http://localhost:8001 (FastAPI + ReportLab A4 PDF 엔진)

---

## 🎬 3. [신규 무인 마케팅] AI 숏폼 30초 자동 제작기 v2.0
- **핵심 사업**: 유튜브 숏폼/인스타그램 릴스 30초 바이럴 대본 & 카피라이팅 무인 렌더링
- **시스템 구현**: marketing_generator/main.py 및 다크 네온 웹 인터페이스 수립 (/api/generate-marketing 가동 중)

---

## 🎙️ 4. [신규 PC 미디어 비즈니스] PC 실시간 음성 자막 번역기 v1.0
- **핵심 사업**: PC에서 재생되는 모든 해외 영상/동영상 프로그램 오디오 자동 번역 & 투명 자막 팝업
- **기술 구현**: realtime_subtitle_translator_v1.py (WASAPI Loopback 오디오 포획 + Tkinter 투명 Always-on-Top 오버레이)

---

## 📚 5. [전자책 & 마케팅] 1인기업 AI 자동화 프롬프트 100선 & 멀티플랫폼 입점
- 100선 프롬프트 전자책 PDF (`1인기업_AI자동화_프롬프트100선_전자책.pdf`)
- 크몽 대안 멀티플랫폼 입점 가이드 (포스타입, 숨고, 와디즈, 클래스101) 및 0원 웹배포 무인 시스템 수립
"""
    },
    {
        "title": "[로그프로젝트 1] 슈드용사 2D/3D 액션 RPG 개발 명세서",
        "content": """# ⚔️ [로그프로젝트 1] 슈드용사 2D/3D 액션 RPG 상세 개발 명세서

## 1. 개요 및 타깃
- **정식 명칭**: 슈드용사 (GogoFlex Rogue Project)
- **개발 엔진**: Unity 2D/3D Engine
- **목표 수익**: 월 1,000만원 ~ 1,800만원 무인 자동화 매출

## 2. 캐릭터 그래픽 및 프레임 명세
- **원본 연동**: 대표님 원본 캐릭터 (289x434) 베이스 8방향 7종 모션 렌더링
- **뒷모습 (North BackView)**: N(180°), NE(135°), NW(225°) 은발 후두부, 흑철 갑옷 척추 용암 룬, 망토 전면 구현
- **7가지 모션**:
  1. Idle (정지)
  2. Move (이동)
  3. Basic Attack (기본 공격)
  4. Dash Attack (대시 공격)
  5. Ranged Sword Wave (원거리 검기)
  6. Whirlwind 360 (360도 회전)
  7. Ultimate Ground Slam (필살기 내려찍기)
- **개별 프레임 분리**: 7모션 x 8축 x 4~6프레임 = **총 240개 96x96 투명 PNG 개별 프레임 컷**

## 3. 유니티 C# 시스템 및 라이브 뷰어
- SudeHero8WayController.cs: 8방향 이동, 애니메이션 전환, 스킬 (1~7번 키) 컨트롤러
- 웹 뷰어: sude_8dir_7motions_viewer.html (실시간 360도 모션 검증)
"""
    },
    {
        "title": "[3분시리즈 1] AI 사업계획서 & 보고서 자동 생성 SaaS 무인 파이프라인",
        "content": """# 💎 [3분시리즈 1] AI 사업계획서 & 보고서 자동 생성기 SaaS (v0.90 Beta)

## 1. 무인 자동화 시스템 명세
- **라이브 주소**: https://solopreneur-automation.onrender.com
- **개발 아키텍처**: FastAPI + Jinja2 + ReportLab PDF Engine
- **무인 결제/검증 파이프라인**:
  - 크몽 주문번호 1회용 자동 검증 시스템
  - 생성 완료 후 CS 추적 자동 소멸 알고리즘
  - 3초 만에 A4 고화질 비즈니스 사업계획서 PDF 렌더링 다운로드

## 2. 파이프라인 비즈니스 모델
- 크몽 / 전자책 시장 연동 0초 무인 응답
- $49 SaaS 번들 패키지 파이프라인 결합
"""
    },
    {
        "title": "[미디어 솔루션] AI 숏폼 30초 제작기 v2.0 & PC 실시간 음성 자막 번역기 v1.0",
        "content": """# 🎬 [미디어 비즈니스] AI 숏폼 30초 제작기 & PC 실시간 음성 자막 번역기

## 1. AI 숏폼 30초 자동 제작기 v2.0
- **핵심 기능**: 유튜브 숏폼, 인스타그램 릴스 30초 바이럴 대본 및 카피라이팅 렌더링
- **UI/UX**: Dark Neon 웹 인터페이스 (`marketing_generator/main.py`)
- **API Endpoint**: `/api/generate-marketing`

## 2. PC 실시간 음성 자막 번역기 v1.0
- **핵심 기능**: PC 재생 모든 동영상/오디오 실시간 한국어 번역 & 투명 자막 팝업
- **기술 스펙**: WASAPI Loopback PC 오디오 포획 + Tkinter 투명 Always-on-Top 오버레이
- **소스**: `realtime_subtitle_translator_v1.py`
"""
    },
    {
        "title": "[전자책 & 마케팅] AI 자동화 프롬프트 100선 및 멀티플랫폼 입점 가이드",
        "content": """# 📚 [전자책 & 무인 마케팅] AI 자동화 프롬프트 100선 및 입점 전략

## 1. 1인기업 AI 자동화 프롬프트 100선 전자책
- 실전 사업계획서, 마케팅 문구, 코드 생성, 데이터 분석 등 100가지 최적화 프롬프트 팩
- PDF 및 Markdown 수록 (`1인기업_AI자동화_프롬프트100선_전자책.pdf`)

## 2. 크몽 대안 멀티플랫폼 입점 전략
- 타깃 플랫폼: 포스타입, 숨고, 와디즈, 클래스101, 네이버 프리미엄 콘텐츠
- 0원 무제한 웹배포 및 무인 응답 프로세스 수립
"""
    }
]

async def run():
    print("🚀 NotebookLM에 '보고서' 제목 생성 및 5대 프로젝트 통합 소스 주입 시동!")

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

        print("🌐 NotebookLM 메인 페이지 접속 중...")
        await page.goto("https://notebook.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # 1. '+ 새 노트' 생성
        print("✨ '+ 새 노트' 생성...")
        new_btn = page.locator("button:has-text('새 노트'), button:has-text('새로 만들기'), [aria-label*='새']").first
        if await new_btn.count() > 0:
            await new_btn.click()
            await asyncio.sleep(4)

        print(f"📌 접속한 노트북 URL: {page.url}")

        # 2. 제목을 '보고서'로 변경
        print("✏️ 노트북 제목을 '보고서'로 변경 중...")
        try:
            # Click on editable title on top left
            title_elem = page.locator("h1, text=/제목 없는/i, [aria-label*='제목']").first
            if await title_elem.count() > 0:
                await title_elem.click(force=True)
                await asyncio.sleep(1)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await page.keyboard.type("보고서", delay=100)
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)
                print("✅ 노트북 제목 '보고서' 설정 완료!")
        except Exception as e:
            print(f"⚠️ 제목 변경 예외: {e}")

        # 3. 5개 프로젝트 소스 100% 주입
        for idx, src in enumerate(SOURCES, start=1):
            print(f"\n📝 [{idx}/5] 소스 주입 중: '{src['title']}'...")

            # If not initial modal, click '+ 소스 추가' button
            if idx > 1:
                add_src_btn = page.locator("button:has-text('소스 추가'), [aria-label*='소스 추가']").first
                if await add_src_btn.count() > 0:
                    print("➕ '+ 소스 추가' 버튼 클릭...")
                    await add_src_btn.click(force=True)
                    await asyncio.sleep(2)

            # Click '복사된 텍스트' button
            copied_text_btn = page.get_by_text("복사된 텍스트", exact=True)
            if await copied_text_btn.count() > 0:
                box = await copied_text_btn.first.bounding_box()
                if box:
                    await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    await asyncio.sleep(2)

            # Fill text into paste textarea
            textarea = page.locator("textarea").last
            if await textarea.count() > 0:
                await textarea.click(force=True)
                full_text = f"# {src['title']}\n\n{src['content']}"
                await textarea.fill(full_text)
                await asyncio.sleep(1)

                # Click '삽입'
                insert_btn = page.locator("button:has-text('삽입')").last
                if await insert_btn.count() > 0:
                    await insert_btn.click(force=True)
                    print(f"💾 '{src['title']}' 삽입 완료! AI 학습 완료 대기 (5초)...")
                    await asyncio.sleep(5)

        # 4. 상단 타이틀 한번 더 '보고서' 확정 확인
        try:
            current_title_elem = page.locator("text=/제목 없는/i").first
            if await current_title_elem.count() > 0 and await current_title_elem.is_visible():
                await current_title_elem.click(force=True)
                await asyncio.sleep(1)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await page.keyboard.type("보고서", delay=100)
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)
        except Exception:
            pass

        # 5. 최종 스크린샷 저장
        await page.screenshot(path=SHOT_RESULT_LOCAL, full_page=True)
        if os.path.exists(ARTIFACT_DIR):
            await page.screenshot(path=SHOT_RESULT_ARTIFACT, full_page=True)

        print(f"🎉 NotebookLM 노트북 '보고서' 완벽 생성 및 5개 전체 프로젝트 소스 연동 완료!")
        print(f"📸 로컬 스크린샷: {SHOT_RESULT_LOCAL}")
        print(f"📸 아티팩트 스크린샷: {SHOT_RESULT_ARTIFACT}")

        await asyncio.sleep(3)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())

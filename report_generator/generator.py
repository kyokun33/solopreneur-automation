import datetime
import os
import markdown
from schemas import ReportRequest
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 폰트 등록 (리눅스/클라우드 환경 대응 예외 안전 처리)
FONT_PATH = r"C:\Windows\Fonts\malgun.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\malgunbd.ttf"

MAIN_FONT = "Helvetica"
BOLD_FONT = "Helvetica-Bold"

if os.path.exists(FONT_PATH):
    try:
        pdfmetrics.registerFont(TTFont("Malgun", FONT_PATH))
        MAIN_FONT = "Malgun"
    except Exception:
        pass

if os.path.exists(FONT_BOLD_PATH):
    try:
        pdfmetrics.registerFont(TTFont("Malgun-Bold", FONT_BOLD_PATH))
        BOLD_FONT = "Malgun-Bold"
    except Exception:
        BOLD_FONT = MAIN_FONT
else:
    if MAIN_FONT == "Malgun":
        BOLD_FONT = "Malgun"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.saveState()
                self.setFont(MAIN_FONT, 8)
                self.setFillColor(colors.HexColor("#64748b"))
                self.drawRightString(200 * 2.83, 280 * 2.83, "AI Business Report Generator SaaS")
                self.setStrokeColor(colors.HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(15 * 2.83, 278 * 2.83, 200 * 2.83, 278 * 2.83)
                
                page_text = f"- {self._pageNumber} / {num_pages} -"
                self.drawCentredString(105 * 2.83, 12 * 2.83, page_text)
                self.restoreState()
            super().showPage()
        super().save()

def generate_business_report(req: ReportRequest) -> tuple[str, str]:
    category_titles = {
        "government": "정부지원사업 제출용 사업계획서",
        "ir": "투자 유치(IR) 제안서",
        "market": "시장 분석 및 수익성 검증 리포트"
    }
    cat_name = category_titles.get(req.category, "비즈니스 기획서")
    now_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")

    md_content = f"""# 📄 [사업계획서] {req.title}

* **분류**: {cat_name}
* **작성일자**: {now_str}
* **타겟 고객**: {req.target_customer}
* **예산 및 목표**: {req.budget}

---

## 1. 사업 개요 및 배경 (Executive Summary)

### 1.1 추진 배경 및 문제 정의
현재 **{req.target_customer}** 계층은 기존 솔루션의 높은 비용, 느린 속도, 복잡한 사용법으로 인해 비효율을 겪고 있습니다. 
**"{req.title}"** 프로젝트는 이러한 시장 페인 포인트(Pain Point)를 해결하고, 초고속 획기적인 혁신 가치를 제공하기 위해 추진됩니다.

### 1.2 비전 및 핵심 가치
* **비전**: {req.target_customer}를 위한 NO.1 무인 자동화 플랫폼 도약
* **핵심 가치**: **{req.core_features}**를 기반으로 한 업무 생산성 10배 향상

---

## 2. 타겟 시장 분석 및 경쟁 우위 (Market & Competitor Analysis)

### 2.1 목표 시장(TAM-SAM-SOM) 분석
* **전체 시장 (TAM)**: 디지털 전환 및 자동화 서비스 시장 (약 5조 원 규모)
* **유효 시장 (SAM)**: {req.target_customer} 중심의 솔루션 수요 (약 5,000억 원 규모)
* **수익 시장 (SOM)**: 초기 1~2년 차 진입 타겟 층 (약 100억 원 목표)

### 2.2 경쟁 우위 요소
| 구분 | 기존 대행사 / 솔루션 | {req.title} (본 프로젝트) |
| :--- | :--- | :--- |
| **제작 단가** | 100만 원 ~ 300만 원 | **9,900원 ~ 29,900원 (초저가)** |
| **소요 시간** | 2주 ~ 4주 소요 | **3분 이내 즉시 완성** |
| **접근성** | 방문 상담 및 서류 제출 필요 | **100% 무인 웹 자동화** |

---

## 3. 핵심 기술 및 서비스 스펙 (Product Specification)

### 3.1 솔루션 핵심 기능
1. **자동화 엔진**: 입력된 핵심 정보 기반 최적 알고리즘 렌더링
2. **핵심 기능**: {req.core_features}
3. **multi-format 지원**: 웹 미리보기, 마크다운(MD) 파일 및 PDF 즉시 다운로드

### 3.2 서비스 구조
```
[사용자 정보 입력] ➔ [AI 스마트 렌더링 엔진] ➔ [전문 보고서 PDF/MD 완성]
```

---

## 4. 마케팅 전략 및 수익 모델 (GTM & Monetization)

### 4.1 고투마켓(Go-To-Market) 마케팅 전략
* **온라인 커뮤니티 바이럴**: 타겟 고객({req.target_customer})이 밀집한 커뮤니티/오픈채팅/디스코드 무료 체험 진입
* **SEO 최적화 콘텐츠 마케팅**: 검색 노출 최적화 블로그 및 숏폼 영상 제작
* **파트너십**: 관련 플랫폼 및 창업지원센터 연계 프로모션

### 4.2 수익 모델 (Business Model)
* **단건 이용권**: 건당 **9,900원**
* **월간 구독형 (SaaS)**: 월 **29,900원** (무제한 렌더링 + 프리미엄 템플릿)
* **B2B 기업 맞춤형 API 연동**: 건당 별도 협의

---

## 5. 재무 추정 및 실행 타임라인 (Financial & Roadmap)

### 5.1 로드맵
* **Phase 1 (1개월 차)**: MVP 완성 및 Vercel/서버 배포 ➔ 초기 고객 100명 확보
* **Phase 2 (3개월 차)**: 유료 모델(구독 결제) 전환 ➔ 월 매출 300만 원 목표
* **Phase 3 (6개월 차)**: 기능 고도화 및 B2B 파트너십 확장 ➔ 월 매출 1,000만 원 돌파

### 5.2 예산 집행 계획
* **총 예산 규모**: **{req.budget}**
* **서버 및 인프라**: 10%
* **마케팅 및 고객 유치**: 60%
* **예비비 및 기타**: 30%

---
*본 보고서는 "고고플렉스AI 연구소" AI 사업계획서 자동 생성 플랫폼에 의해 정식 발급되었습니다.*
"""

    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    return md_content, html_content

def build_pdf_file(req: ReportRequest, pdf_path: str):
    md_content, _ = generate_business_report(req)
    lines = md_content.splitlines()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=35,
        rightMargin=35,
        topMargin=45,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    h1_style = ParagraphStyle(
        'H1_PDF', fontName=BOLD_FONT, fontSize=18, leading=24,
        textColor=colors.HexColor("#1e1b4b"), spaceBefore=15, spaceAfter=10
    )
    h2_style = ParagraphStyle(
        'H2_PDF', fontName=BOLD_FONT, fontSize=13, leading=18,
        textColor=colors.HexColor("#4338ca"), spaceBefore=12, spaceAfter=6, keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'H3_PDF', fontName=BOLD_FONT, fontSize=11, leading=15,
        textColor=colors.HexColor("#334155"), spaceBefore=8, spaceAfter=4, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_PDF', fontName=MAIN_FONT, fontSize=10, leading=15,
        textColor=colors.HexColor("#1e293b"), spaceAfter=6
    )

    story = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            story.append(Paragraph(stripped[2:], h1_style))
        elif stripped.startswith("## "):
            story.append(Paragraph(stripped[3:], h2_style))
        elif stripped.startswith("### "):
            story.append(Paragraph(stripped[4:], h3_style))
        elif stripped.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=8, spaceAfter=8))
        elif stripped:
            clean_text = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(clean_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    return pdf_path

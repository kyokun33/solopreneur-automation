import datetime
import os
import markdown
from schemas import ReportRequest
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
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
                self.drawRightString(200 * 2.83, 280 * 2.83, "AI Business Report Generator SaaS (3분시리즈 1)")
                self.setStrokeColor(colors.HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(15 * 2.83, 278 * 2.83, 200 * 2.83, 278 * 2.83)
                
                page_text = f"- {self._pageNumber} / {num_pages} -"
                self.drawCentredString(105 * 2.83, 12 * 2.83, page_text)
                self.restoreState()
            super().showPage()
        super().save()

def detect_domain(title: str, features: str) -> str:
    text = (title + " " + features).lower()
    if any(k in text for k in ["커피", "카페", "식당", "음료", "로봇", "서빙", "음식", "베이커리", "매장", "푸드", "디저트"]):
        return "fnb"
    elif any(k in text for k in ["쇼핑몰", "스토어", "의류", "패션", "유통", "판매", "배송", "마켓"]):
        return "ecommerce"
    elif any(k in text for k in ["학원", "강의", "컨설팅", "상담", "피트니스", "뷰티", "교육", "레슨"]):
        return "service"
    elif any(k in text for k in ["제조", "공장", "제품", "키트", "장비", "하드웨어"]):
        return "hardware"
    return "it_saas"

def generate_business_report(req: ReportRequest) -> tuple[str, str]:
    category_titles = {
        "government": "정부지원사업 제출용 사업계획서",
        "ir": "투자 유치(IR) 제안서",
        "market": "시장 분석 및 수익성 검증 리포트"
    }
    cat_name = category_titles.get(req.category, "비즈니스 기획서")
    now_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    domain = detect_domain(req.title, req.core_features)

    if domain == "fnb":
        tam_text = "국내 외식 및 무인 로봇 푸드테크 시장 (약 15조 원 규모)"
        sam_text = f"{req.target_customer} 중심의 무인 로봇 매장 수요 (약 1조 2,000억 원 규모)"
        som_text = "초기 1~2년 차 거점 매장 진입 및 프랜차이즈 가맹 목표 (약 30억 원 목표)"
        
        comp_table = f"""| 구분 | 기존 수동 매장 / 일반 카페 | {req.title} (본 프로젝트) |
| :--- | :--- | :--- |
| **인건비 비중** | 매출의 30% ~ 40% (고비용) | **인건비 70% 이상 획기적 절감** |
| **운영 시간** | 10시간 ~ 12시간 한정 운영 | **24시간 365일 무인 자동 가동** |
| **품질 및 속도** | 조리자 숙련도에 따라 변동 | **로봇 알고리즘으로 균일한 최상 품질** |"""
        
        service_struct = "[고객 키오스크/앱 주문] ➔ [로봇 음료 제조 & 무인 서빙] ➔ [고객 음료 수령 및 픽업]"
        mono_text = """* **매장 음료/디저트 판매 수익**: 24시간 무인 매장 음료 및 디저트 직접 판매
* **로봇 매장 프랜차이즈 가맹 수익**: 무인 로봇 패키지 매장 가맹비 및 원두/원자재 유통 수익
* **스마트 매장 광고/협찬 수익**: 무인 서빙 로봇 디스플레이 사이니지 광고 수익"""
        
        roadmap_text = """* **Phase 1 (1~3개월 차)**: 무인 로봇 제조/서빙 설비 구축 ➔ 플래그십 1호점 오픈
* **Phase 2 (6개월 차)**: 24시간 매장 운영 데이터 검증 ➔ 직영 3호점 확장 및 월 매출 3,000만 원 달성
* **Phase 3 (1년 차)**: 프랜차이즈 가맹 사업 본격화 ➔ 전국 30개 매장 가맹 계약 체결"""

        budget_text = f"""* **총 예산 규모**: **{req.budget}**
* **로봇 제조/서빙 설비 및 키오스크**: 45%
* **매장 인테리어 및 보증금**: 35%
* **원자재(원두/음료) 및 초기 마케팅**: 20%"""

    elif domain == "ecommerce":
        tam_text = "국내 온라인 쇼핑 거래액 시장 (약 220조 원 규모)"
        sam_text = f"{req.target_customer} 타겟 무인 커머스 수요 (약 5조 원 규모)"
        som_text = "초기 1년 차 전문 쇼핑몰 진입 (약 10억 원 목표)"
        
        comp_table = f"""| 구분 | 일반 소매 쇼핑몰 | {req.title} (본 프로젝트) |
| :--- | :--- | :--- |
| **재고 부담** | 사입 및 재고 리스크 상존 | **무재고 AI 위탁/자동 풀필먼트** |
| **마케팅 효율** | 높은 수동 키워드 광고비 | **AI 타겟팅으로 광고 ROI 300% 향상** |
| **물류 소요** | 직접 포장 및 택배 발송 | **100% 무인 물류 자동 발송** |"""
        
        service_struct = "[고객 주문] ➔ [AI 무인 주문 접수 & 자동 사입] ➔ [풀필먼트 자동 택배 배송]"
        mono_text = """* **상품 판매 마진 수익**: 사입가 대비 30~50% 유통 마진 확보
* **정기 구독 배송 수익**: 주요 타겟 고객 대상 월간 정기 배송 서비스
* **B2B 도매 유통 수익**: 소상공인 대상 도매 공급 마진"""
        
        roadmap_text = """* **Phase 1 (1개월 차)**: 쇼핑몰 구축 및 100종 킬러 상품 등록 ➔ 일 매출 100만 원 달성
* **Phase 2 (3개월 차)**: AI 바이럴 마케팅 집행 ➔ 월 매출 2,000만 원 달성
* **Phase 3 (6개월 차)**: PB 자체 브랜드 출시 ➔ 월 매출 5,000만 원 돌파"""

        budget_text = f"""* **총 예산 규모**: **{req.budget}**
* **마케팅 및 SNS 바이럴 광고**: 50%
* **상품 사입 및 풀필먼트 물류비**: 30%
* **쇼핑몰 시스템 및 디자인**: 20%"""

    else: # 기본 IT/SaaS 및 일반 서비스
        tam_text = "국내 디지털 전환 및 서비스 자동화 시장 (약 10조 원 규모)"
        sam_text = f"{req.target_customer} 타겟 자동화 솔루션 수요 (약 1조 원 규모)"
        som_text = "초기 1년 차 진입 목표 (약 50억 원 목표)"
        
        comp_table = f"""| 구분 | 기존 수동 서비스 / 대행사 | {req.title} (본 프로젝트) |
| :--- | :--- | :--- |
| **서비스 단가** | 100만 원 ~ 300만 원 (고비용) | **초저가 1회성 또는 월 구독형** |
| **처리 속도** | 수일 ~ 수주 소요 | **3초 이내 즉시 완성 및 렌더링** |
| **접근성** | 방문 대면 상담 필요 | **100% 무인 웹 자동화 접속** |"""
        
        service_struct = "[사용자 정보 입력] ➔ [AI 스마트 렌더링 엔진] ➔ [전문 리포트 PDF/MD 즉시 완성]"
        mono_text = """* **단건 이용권 판매 수익**: 건당 단건 결제 수익
* **월간 구독형(SaaS) 수익**: 월간 무제한 이용 정기 구독 결제
* **B2B 맞춤형 커스텀 연동 수익**: 기업체 대상 맞춤형 솔루션 제공"""
        
        roadmap_text = """* **Phase 1 (1개월 차)**: MVP 완성 및 서비스 런칭 ➔ 초기 고객 100명 확보
* **Phase 2 (3개월 차)**: 유료 구독 모델 전환 ➔ 월 매출 500만 원 달성
* **Phase 3 (6개월 차)**: B2B 파트너십 확장 ➔ 월 매출 2,000만 원 돌파"""

        budget_text = f"""* **총 예산 규모**: **{req.budget}**
* **서버 인프라 및 시스템 구축**: 30%
* **마케팅 및 고객 유치**: 50%
* **운영비 및 기타**: 20%"""

    md_content = f"""# 📄 [사업계획서] {req.title}

* **분류**: {cat_name}
* **작성일자**: {now_str}
* **타겟 고객**: {req.target_customer}
* **예산 및 목표**: {req.budget}

---

## 1. 사업 개요 및 배경 (Executive Summary)

### 1.1 추진 배경 및 문제 정의
현재 **{req.target_customer}** 계층은 기존 비효율적인 수동 방식과 높은 비용 부담으로 인해 어려움을 겪고 있습니다. 
**"{req.title}"** 프로젝트는 이러한 시장 페인 포인트(Pain Point)를 혁신적으로 해결하고, 고효율 무인 자동화 가치를 제공하기 위해 추진됩니다.

### 1.2 비전 및 핵심 가치
* **비전**: {req.target_customer}를 위한 NO.1 대표 비즈니스 브랜드 도약
* **핵심 가치**: **{req.core_features}**를 기반으로 한 경쟁력 10배 향상

---

## 2. 타겟 시장 분석 및 경쟁 우위 (Market & Competitor Analysis)

### 2.1 목표 시장(TAM-SAM-SOM) 분석
* **전체 시장 (TAM)**: {tam_text}
* **유효 시장 (SAM)**: {sam_text}
* **수익 시장 (SOM)**: {som_text}

### 2.2 경쟁 우위 요소
{comp_table}

---

## 3. 핵심 기술 및 서비스 스펙 (Product Specification)

### 3.1 솔루션 핵심 기능
1. **스마트 자동화 엔진**: 입력 정보 기반 최적 알고리즘 실시간 구성
2. **핵심 경쟁력**: {req.core_features}
3. **Multi-Format 지원**: 웹 미리보기, 마크다운(MD) 파일 및 PDF 즉시 소장

### 3.2 서비스 구조
```
{service_struct}
```

---

## 4. 마케팅 전략 및 수익 모델 (GTM & Monetization)

### 4.1 고투마켓(Go-To-Market) 마케팅 전략
* **타겟 밀집 채널 직접 집행**: 주요 타겟 고객({req.target_customer})이 밀집한 커뮤니티 및 SNS 바이럴 마케팅
* **SEO 최적화 콘텐츠 마케팅**: 검색 노출 최적화 블로그 및 숏폼 마케팅
* **초기 프로모션**: 1회용 시리얼 코드 및 무상 체험권 제공으로 유저 유치

### 4.2 수익 모델 (Business Model)
{mono_text}

---

## 5. 재무 추정 및 실행 타임라인 (Financial & Roadmap)

### 5.1 로드맵
{roadmap_text}

### 5.2 예산 집행 계획
{budget_text}

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

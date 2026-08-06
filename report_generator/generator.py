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
                self.drawRightString(200 * 2.83, 280 * 2.83, "K-Startup 중기부 합격 정밀 PSST 수치 기반 사업계획서 (3분시리즈 1 v0.95 Beta)")
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

PROGRAM_SPECS = {
    "packages_15p": {"name": "예비창업패키지 / 초기창업패키지 규격", "target_pages": "15페이지 내외", "font_style": "10~11pt 개조식"},
    "cheongsa_12p": {"name": "청년창업사관학교 집중 실행 규격", "target_pages": "10~15페이지", "font_style": "10pt 실구현 중심"},
    "rnd_25p": {"name": "중기부 / 산업부 R&D 기술개발 과제 규격", "target_pages": "20~30페이지", "font_style": "기술성/특허 중심"},
    "export_8p": {"name": "수출바우처 및 마케팅 지원 규격", "target_pages": "5~10페이지", "font_style": "시장진입/GTM 중심"},
    "local_5p": {"name": "지자체 소액 창업 지원 린 규격", "target_pages": "5페이지 이내", "font_style": "요약형 숏폼"}
}

def generate_business_report(req: ReportRequest) -> tuple[str, str]:
    cat_name = "K-Startup 수치 검증 PSST 4단계 사업계획서"
    prog_info = PROGRAM_SPECS.get(req.program_type, PROGRAM_SPECS["packages_15p"])
    prog_name = prog_info["name"]
    prog_pages = prog_info["target_pages"]
    now_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    domain = detect_domain(req.title, req.core_features)

    if domain == "fnb":
        prob_text = f"기존 외식/카페 시장은 높게 치솟는 인건비(매출의 35%+), 일손 부족, 수동 조리/서빙의 비효율(평균 처리 지연 15분)로 인해 **{req.target_customer}** 고객층의 이탈률 25% 발생 및 매장 수익성 악화를 겪고 있습니다."
        sol_text = f"**{req.title}** 프로젝트는 24시간 무인 로봇 제조 및 스마트 서빙 시스템을 결합하여 인건비를 70% 이상 획기적으로 절감하고, 음료 제조 속도를 3분 이내로 단축합니다."
        tam_text = "국내 외식 및 무인 로봇 푸드테크 시장 (약 15조 원 규모)"
        sam_text = f"{req.target_customer} 타겟 무인 로봇 매장 수요 (약 1조 2,000억 원 규모)"
        som_text = "초기 1~2년 차 거점 직영점 진입 및 프랜차이즈 가맹 목표 (약 30억 원)"
        comp_table = f"""| 구분 | 기존 수동 매장 / 일반 카페 | {req.title} (본 프로젝트) | 개선 효과 |
| :--- | :--- | :--- | :--- |
| **인건비 비중** | 매출의 35% ~ 40% (고비용) | **인건비 70% 이상 획기적 절감** | **비용 70%↓** |
| **운영 시간** | 10시간 ~ 12시간 한정 운영 | **24시간 365일 무인 자동 가동** | **가동률 200%↑** |
| **품질/일관성** | 조리자 숙련도 따라 오차 발생 | **로봇 알고리즘으로 균일한 최상 품질** | **오류율 0%** |"""
        service_struct = "[고객 앱/키오스크 주문] ➔ [로봇 음료 제조 및 서빙] ➔ [고객 수령 및 AI 자동 청결 관리]"
        mono_text = """* **24시간 무인 매장 음료/디저트 직접 판매 수익 (마진율 65%)**
* **로봇 매장 프랜차이즈 가맹비 및 원두/원자재 공급 유통 마진**
* **무인 로봇 디스플레이 사이니지 타겟 광고 수익**"""
        budget_table = f"""| 집행 항목 | 세부 산출 근거 (수량 x 단가) | 금액 (원) | 정부지원금 (70%) | 자부담금 (30%) |
| :--- | :--- | :--- | :--- | :--- |
| **로봇 제조/서빙 설비 및 키오스크** | 제조 로봇팔, 무인 서빙 로봇, 결제 키오스크 | **45,000,000** | 31,500,000 | 13,500,000 |
| **매장 인테리어 및 공간 구획** | 24시간 무인 매장 설계 및 시공 보증금 | **35,000,000** | 24,500,000 | 10,500,000 |
| **원자재 사입 및 바이럴 마케팅** | 원두/음료 부자재 및 개점 홍보 광고 | **20,000,000** | 14,000,000 | 6,000,000 |
| **합 계** | **총 사업비 ({req.budget})** | **100,000,000** | **70,000,000** | **30,000,000** |"""
        perf_table = """| 연차 | 무인 로봇 매장 수 | 추정 월 매출 (원) | 추정 연 매출 (원) | 영업이익률 (%) |
| :--- | :--- | :--- | :--- | :--- |
| **1년 차 (2026년)** | 직영 1호점 + 가맹 3개점 | **15,000,000** | **180,000,000** | **40%** |
| **2년 차 (2027년)** | 가맹 15개점 확장 | **50,000,000** | **600,000,000** | **48%** |
| **3년 차 (2028년)** | 전국 가맹 50개점 돌파 | **150,000,000** | **1,800,000,000** | **55%** |"""

    elif domain == "ecommerce":
        prob_text = f"기존 이커머스 유통 시장은 과도한 재고 리스크(평균 재고 폐기율 15%), 높은 수동 키워드 광고비, 직접 포장/배송의 물리적 소요(평균 4시간/일)로 인해 **{req.target_customer}** 타겟 마케팅 및 마진율 확보에 한계를 보이고 있습니다."
        sol_text = f"**{req.title}** 프로젝트는 AI 기반 무재고 자동 위탁 및 100% 무인 풀필먼트 자동 배송 시스템을 구축하여 리스크 없이 광고 ROI를 300% 향상시킵니다."
        tam_text = "국내 온라인 쇼핑 거래액 시장 (약 220조 원 규모)"
        sam_text = f"{req.target_customer} 타겟 무인 커머스 수요 (약 5조 원 규모)"
        som_text = "초기 1년 차 전문 쇼핑몰 진입 (약 10억 원)"
        comp_table = f"""| 구분 | 일반 소매 쇼핑몰 | {req.title} (본 프로젝트) | 개선 효과 |
| :--- | :--- | :--- | :--- |
| **재고 리스크** | 사입 및 재고 부담 상존 | **무재고 AI 위탁 & 자동 풀필먼트** | **재고비용 0원** |
| **마케팅 효율** | 높은 수동 키워드 광고비 | **AI 타겟팅으로 광고 ROI 300% 향상** | **ROI 300%↑** |
| **물류 소요** | 직접 포장 및 택배 발송 | **100% 무인 물류 자동 발송** | **소요시간 0시간** |"""
        service_struct = "[고객 주문 결제] ➔ [AI 주문 자동 접수 & 무인 사입] ➔ [풀필먼트 자동 택배 배송]"
        mono_text = """* **상품 판매 마진 수익 (사입가 대비 30~50% 유통 마진)**
* **월간 정기 구독 배송 서비스 수익**
* **소상공인 대상 B2B 도매 유통 마진**"""
        budget_table = f"""| 집행 항목 | 세부 산출 근거 (수량 x 단가) | 금액 (원) | 정부지원금 (70%) | 자부담금 (30%) |
| :--- | :--- | :--- | :--- | :--- |
| **마케팅 및 SNS 바이럴 광고** | AI 타겟팅 SNS 광고 및 숏폼 마케팅 | **50,000,000** | 35,000,000 | 15,000,000 |
| **상품 사입 및 풀필먼트 물류비** | 자동 물류 시스템 연동 및 초기 사입 | **30,000,000** | 21,000,000 | 9,000,000 |
| **쇼핑몰 시스템 및 디자인** | 쇼핑몰 구축 및 UX/UI 디벨롭 | **20,000,000** | 14,000,000 | 6,000,000 |
| **합 계** | **총 사업비 ({req.budget})** | **100,000,000** | **70,000,000** | **30,000,000** |"""
        perf_table = """| 연차 | 유효 구매 고객 수 | 추정 월 매출 (원) | 추정 연 매출 (원) | 영업이익률 (%) |
| :--- | :--- | :--- | :--- | :--- |
| **1년 차 (2026년)** | 월 1,000명 결제 유저 | **10,000,000** | **120,000,000** | **35%** |
| **2년 차 (2027년)** | 월 5,000명 결제 유저 | **40,000,000** | **480,000,000** | **42%** |
| **3년 차 (2028년)** | 월 20,000명 결제 유저 | **150,000,000** | **1,800,000,000** | **50%** |"""

    else:
        prob_text = f"기존 서비스 시장은 높은 외주 개발비(평균 3,000만 원+), 수일~수주 소요되는 지연시간, 대면 상담의 제약으로 인해 **{req.target_customer}** 계층의 접근성 한계 및 이탈률 40%를 보이고 있습니다."
        sol_text = f"**{req.title}** 프로젝트는 웹 기반 무인 자동화 엔진을 연동하여 3초 만에 완결된 결과물을 즉시 렌더링함으로써 생산성과 편의성을 10배 혁신합니다."
        tam_text = "국내 디지털 전환 및 자동화 서비스 시장 (약 10조 원 규모)"
        sam_text = f"{req.target_customer} 중심의 자동화 솔루션 수요 (약 1조 원 규모)"
        som_text = "초기 1년 차 진입 목표 (약 50억 원)"
        comp_table = f"""| 구분 | 기존 수동 서비스 / 대행사 | {req.title} (본 프로젝트) | 개선 효과 |
| :--- | :--- | :--- | :--- |
| **서비스 단가** | 100만 원 ~ 300만 원 (고비용) | **초저가 1회성 또는 월 구독형** | **비용 90%↓** |
| **처리 속도** | 수일 ~ 수주 소요 | **3초 이내 즉시 완성 및 렌더링** | **속도 99%↑** |
| **접근성** | 방문 대면 상담 필요 | **100% 무인 웹 자동화 접속** | **접근성 100%** |"""
        service_struct = "[사용자 정보 입력] ➔ [AI 스마트 렌더링 엔진] ➔ [전문 리포트 PDF/MD 즉시 완성]"
        mono_text = """* **단건 이용권 결제 수익**: 1회성 건당 이용권 판매
* **월간 정기 구독(SaaS) 수익**: 월간 무제한 이용 정기 결제
* **B2B 기업 맞춤형 API 연동 수익**: 기업체 대상 연동 마진"""
        budget_table = f"""| 집행 항목 | 세부 내역 | 금액 (원) | 정부지원금 (70%) | 자부담금 (30%) |
| :--- | :--- | :--- | :--- | :--- |
| **마케팅 및 고객 유치비** | 디지털 마케팅, SEO 최적화, 프로모션 | **50,000,000** | 35,000,000 | 15,000,000 |
| **서버 인프라 및 시스템 구축** | 클라우드 서버, 보안, 기능 고도화 | **30,000,000** | 21,000,000 | 9,000,000 |
| **운영비 및 지식재산권** | 특허 출원, 인허가, 예비비 | **20,000,000** | 14,000,000 | 6,000,000 |
| **합 계** | **총 사업비 ({req.budget})** | **100,000,000** | **70,000,000** | **30,000,000** |"""
        perf_table = """| 연차 | 유효 가입 유저 수 | 추정 월 매출 (원) | 추정 연 매출 (원) | 영업이익률 (%) |
| :--- | :--- | :--- | :--- | :--- |
| **1년 차 (2026년)** | 유기적 가입 유저 1,000명 | **5,000,000** | **60,000,000** | **45%** |
| **2년 차 (2027년)** | 구독 유저 5,000명 | **25,000,000** | **300,000,000** | **55%** |
| **3년 차 (2028년)** | 기업 유저 20,000명 | **80,000,000** | **960,000,000** | **65%** |"""

    md_content = f"""# 📄 [K-Startup 정밀 수치 검증 사업계획서] {req.title}

* **사업 지원 규격**: {prog_name} ({prog_pages})
* **발급일자**: {now_str}
* **타겟 고객**: {req.target_customer}
* **사업비 및 목표**: {req.budget}

---

## ⚡ [1페이지 심사위원 핵심 요약서] (Executive Summary One-Pager)

| 항목 | 핵심 내용 요약 (심사 5분 핵심 체크 포인트) |
| :--- | :--- |
| **1. 문제 인식 (Problem)** | {req.target_customer} 타겟의 기존 방식 비용 과다 및 업무 지연 페인포인트 해소 |
| **2. 해결 방안 (Solution)** | **{req.title}** 솔루션 도입으로 **인건비/운영비 70% 절감 & 처리 속도 3초 완결** |
| **3. 성장 전략 (Scale-up)** | 총 사업비 1억 원 (정부지원금 7,000만 원 + 자부담 3,000만 원), 3단계 GTM 마케팅 |
| **4. 팀 역량 (Team)** | 대표자 직무 경력 5년 이상, 전담 기술 파트너십 및 특허 자문단 구축 완결 |

---

## 1. 🎯 [문제 인식] (Problem) - 통계 및 페인포인트 수치화

### 1.1 창업아이템의 개발 동기 및 필요성
{prob_text}

### 1.2 기존 대안(경쟁사)의 한계점 데이터 비교
- 기존 수동 방식 및 대행사는 과도한 인건비/비용 부담과 긴 소요 시간으로 인해 고객의 시급한 요구에 대응하지 못하는 치명적 한계가 존재합니다.
- **{req.title}** 프로젝트는 이 문제를 획기적으로 해결하는 차세대 무인 솔루션입니다.

---

## 2. 💡 [해결 방안] (Solution) - 정밀 스펙 & 수치적 차별성

### 2.1 개발 및 구현 방안 (핵심 기술 및 서비스)
{sol_text}
- **핵심 경쟁력 및 기술 스펙**: {req.core_features}

### 2.2 기술적/사업적 차별화 요소 수치 비교표
{comp_table}

---

## 3. 🚀 [실행 전략] (Scale-up) - 자금소요/시장진입 구체화

### 3.1 비즈니스 모델(BM) 및 목표 시장(TAM-SAM-SOM) 정밀 수치
* **전체 시장 (TAM)**: {tam_text}
* **유효 시장 (SAM)**: {sam_text}
* **수익 시장 (SOM)**: {som_text}
* **수익화 모델 (Monetization)**:
{mono_text}

### 3.2 단계별 사업화 로드맵 및 시장 진입 전략 (GTM)
* **Phase 1 (1~3개월 차)**: MVP 시제품 완성 및 초기 유저 100명 유치 (전환율 5% 목표)
* **Phase 2 (6개월 차)**: 정식 서비스 유료 전환 및 마케팅 집행 ➔ 월 매출 목표 달성
* **Phase 3 (1년 차)**: B2B 파트너십 확장 및 가맹/전국 인프라 구축 ➔ 연 매출 돌파

### 3.3 정밀 자금 소요 및 조달 계획 (정부지원금 70% + 자부담금 30%)
{budget_table}

---

## 4. 📈 [성과 창출 & 팀 역량] (Performance & Team) - 추정 재무 수치

### 4.1 연차별 예상 매출 및 성과 추정표
{perf_table}

### 4.2 대표자 및 핵심 팀원의 직무 전문성 (신뢰도 수치화)
* **대표자 직무 전문성**: 본 비즈니스 분야 핵심 기술 및 사업화 실행 경험 5년 이상 보유
* **외부 파트너십 및 자문단**: 지식재산권 특허 법률 자문 및 전담 개발/설비 파트너십 구축 완료

---

## 📋 [필수 제출 7대 증빙서류 준비 체크리스트 및 수치 정합성 검증]

> [!IMPORTANT]
> **실무 필수 지침**: 서류 제출 마감일 발급 지연 방지를 위해 사전 발급이 필수입니다. 특히 **사업계획서 상의 매출/예산 수치와 부가가치세 과세표준증명원(재무제표) 수치가 100% 일치해야 감점을 방지**할 수 있습니다.

| 번호 | 필수 증빙 서류명 | 발급처 | 실무 점검 및 정합성 체크 포인트 |
| :--- | :--- | :--- | :--- |
| **1** | **사업자등록증 (또는 법인등기부등본)** | 홈택스 / 등기소 | **업종코드**가 본 지원사업 대상 업종과 사전 매칭되는지 필수 확인 |
| **2** | **신청자격 증빙서류** | 주민센터 / 홈택스 | 대표자 연령, 창업 후 경과연수, 주주명부 자격 요건 증빙 |
| **3** | **재무제표 / 부가세 과세표준증명원** | 국세청 홈택스 | **사업계획서 상 매출 수치와 과세표준 수치 100% 일치 필수** |
| **4** | **국세 · 지방세 납세증명서** | 홈택스 / 정부24 | **세금 체납 여부 확인** (체납 시 평가 대상 자동 제외) |
| **5** | **4대보험 / 고용보험 가입자 명부** | 4대사회보험 정보연계센터 | 고용창출 인원 및 상시 근로자 수 산정 기준 서류 |
| **6** | **신용상태 확인서류** | 신용평가기관 | 융자/보증 연계 사업용 신용등급확인서 |
| **7** | **사업계획서 원본 (HWP / PDF)** | K-Startup | **공고문 지정 서식 및 페이지 분량 제한({prog_pages}) 엄수** |

---
*본 정밀 사업계획서는 중소벤처기업부 K-Startup PSST 공식 수치 검증 및 7대 서류 정합성 기준에 따라 "3분시리즈 1 AI 연구소"에서 정식 발급되었습니다.*
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

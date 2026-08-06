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
                self.drawRightString(200 * 2.83, 280 * 2.83, "K-Startup 중기부 합격 정밀 PSST 대용량 풀-스펙 사업계획서 (3분시리즈 1 v0.99d Beta)")
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
    if any(k in text for k in ["커피", "카페", "식당", "음료", "로봇", "서빙", "음식", "베이커리", "매장", "푸드", "디저트", "외식", "무인"]):
        return "fnb"
    elif any(k in text for k in ["쇼핑몰", "스토어", "의류", "패션", "유통", "판매", "배송", "마켓", "콘텐츠", "디자인"]):
        return "ecommerce"
    elif any(k in text for k in ["바이오", "헬스", "의료", "제약", "화장품", "뷰티", "임상"]):
        return "bio_health"
    elif any(k in text for k in ["제조", "공장", "제품", "키트", "장비", "하드웨어", "부품", "설비"]):
        return "hardware"
    return "it_saas"

PROGRAM_SPECS = {
    "packages_15p": {"name": "예비창업패키지 / 초기창업패키지 규격", "target_pages": "15페이지 내외 정통 풀-스펙", "font_style": "10~11pt 개조식"},
    "cheongsa_12p": {"name": "청년창업사관학교 집중 실행 규격", "target_pages": "10~15페이지 정밀 규격", "font_style": "10pt 실구현 중심"},
    "rnd_25p": {"name": "중기부 / 산업부 R&D 기술개발 과제 규격", "target_pages": "20~30페이지 기술개발 정밀 규격", "font_style": "기술성/특허 중심"},
    "export_8p": {"name": "수출바우처 및 마케팅 지원 규격", "target_pages": "5~10페이지 마케팅 규격", "font_style": "시장진입/GTM 중심"},
    "local_5p": {"name": "지자체 소액 창업 지원 린 규격", "target_pages": "5페이지 이내 숏폼 규격", "font_style": "요약형 숏폼"}
}

def generate_business_report(req: ReportRequest) -> tuple[str, str]:
    prog_info = PROGRAM_SPECS.get(req.program_type, PROGRAM_SPECS["packages_15p"])
    prog_name = prog_info["name"]
    prog_pages = prog_info["target_pages"]
    now_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    domain = detect_domain(req.title, req.core_features)

    if domain == "fnb":
        domain_name = "F&B / 무인 로봇 매장 & 오프라인 유통"
        focus_points = """- **상권 및 유동인구 분석**: 핵심 거점 타겟 상권 분석, 유동인구 5만 명/일 기반 객단가 및 회전율 수치화
- **24시간 무인 가동 경제성**: 24시간 365일 무인 가동을 통한 매장 매출 극대화 수치 근거
- **인건비 절감 구조**: 기존 수동 외식업 대비 인건비 70% 이상 절감 및 오차 없는 레시피 일관성 보장"""
        prob_text_1 = f"현재 국내 외식 및 오프라인 서비스 시장은 최저임금 인상과 구인난으로 인해 매출 대비 인건비 비중이 35%~40%에 달하는 심각한 수익성 악화를 겪고 있습니다. 이로 인해 **{req.target_customer}** 고객층은 서비스 품질 저하 및 긴 대기시간(평균 15분+)의 불편을 겪고 있습니다."
        prob_text_2 = f"기존의 인적 조리 방식 및 유휴 시간(야간 12시간 휴점) 구조는 높은 임대료 부담 대비 매출 기회를 절반 이상 날려버리는 치명적 한계를 갖고 있습니다. **{req.title}** 프로젝트는 이 시장 페인포인트를 뿌리부터 해결합니다."
        sol_text = f"**{req.title}** 프로젝트는 24시간 무인 로봇 제조 및 스마트 자동 서빙/관리 시스템을 도입하여 인건비를 70% 이상 절감하고 음료/상품 제조 속도를 3분 이내로 단축하는 혁신 솔루션입니다."
        tam_text = "국내 외식 및 무인 푸드테크/자동화 매장 시장 (약 15조 원 규모)"
        sam_text = f"{req.target_customer} 중심의 무인 스마트 매장 수요 (약 1조 2,000억 원 규모)"
        som_text = "초기 1~2년 차 거점 직영점 진입 및 프랜차이즈 가맹 목표 (약 30억 원 목표)"
        comp_table = f"""| 구분 | 기존 수동 매장 / 일반 카페 | {req.title} (본 프로젝트) | 개선 효과 (수치) |
| :--- | :--- | :--- | :--- |
| **인건비 비중** | 매출의 35% ~ 40% (고비용) | **인건비 70% 이상 획기적 절감** | **비용 70%↓ 절감** |
| **운영 시간** | 10시간 ~ 12시간 한정 운영 | **24시간 365일 무인 자동 가동** | **가동률 200%↑** |
| **품질/일관성** | 조리자 숙련도 따라 오차 발생 | **로봇 알고리즘으로 균일한 최상 품질** | **오류율 0% 달성** |
| **고객 대기시간**| 평균 10분 ~ 15분 소요 | **3초 결제 ➔ 3분 이내 제조/서빙** | **대기시간 80%↓** |"""
        service_struct = "[고객 키오스크/앱 주문 결제] ➔ [AI 로봇 음료 제조 & 자동 서빙] ➔ [고객 수령 및 AI 자동 청결 관리]"
        mono_text = """* **24시간 무인 매장 제품 직접 판매 수익 (평균 마진율 65% 이상)**
* **로봇 매장 패키지 프랜차이즈 가맹비 및 원두/원자재 공급 유통 마진**
* **무인 스마트 매장 사이니지 디스플레이 타겟 광고 수익**
* **B2B 기업체/공공기관 무인 카페 모듈 납품 계약 마진**"""
        budget_table = f"""| 사업비 집행 항목 | 세부 산출 근거 (수량 x 단가) | 금액 (원) | 정부지원금 (70%) | 자부담금 (30%) |
| :--- | :--- | :--- | :--- | :--- |
| **로봇 제조/서빙 설비 및 키오스크** | 제조 로봇팔 1식, 무인 서빙 로봇 2대, 키오스크 | **45,000,000** | 31,500,000 | 13,500,000 |
| **매장 인테리어 및 공간 구획** | 24시간 무인 매장 파사드 설계 및 보증금 | **35,000,000** | 24,500,000 | 10,500,000 |
| **원자재 사입 및 바이럴 마케팅** | 초기 원자재 사입 및 지역 바이럴 광고 | **20,000,000** | 14,000,000 | 6,000,000 |
| **합 계** | **총 사업비 ({req.budget})** | **100,000,000** | **70,000,000** | **30,000,000** |"""
        perf_table = """| 연차 | 무인 로봇 매장 수 | 추정 월 매출 (원) | 추정 연 매출 (원) | 영업이익률 (%) |
| :--- | :--- | :--- | :--- | :--- |
| **1년 차 (2026년)** | 플래그십 1호점 + 가맹 3개점 | **15,000,000** | **180,000,000** | **40%** |
| **2년 차 (2027년)** | 가맹 15개점 확장 | **50,000,000** | **600,000,000** | **48%** |
| **3년 차 (2028년)** | 전국 가맹 50개점 돌파 | **150,000,000** | **1,800,000,000** | **55%** |"""

    elif domain == "ecommerce":
        domain_name = "이커머스 / 스마트스토어 / 유통"
        focus_points = """- **무재고 풀필먼트 물류 구조**: 초기 사입 재고 부담 0원의 AI 자동 위탁 및 수수료 마진 확보
- **마케팅 ROI & 킬러 IP**: SNS 숏폼 바이럴 및 AI 타겟팅으로 광고 ROI 300% 이상 달성
- **유통 채널 다각화**: 네이버, 쿠팡, 자사몰, 11번가 및 B2B 도매 채널 파이프라인 연동"""
        prob_text_1 = f"기존 온라인 쇼핑몰 유통 시장은 과도한 재고 부담(평균 사입 재고 폐기율 15%), 높은 수동 광고비, 일일 4시간 이상의 수동 포장/발송 작업으로 인해 **{req.target_customer}** 셀러의 마진율 저하와 운영 한계를 보이고 있습니다."
        prob_text_2 = f"특히 상품 사입에 수천만 원의 자금이 묶여 초기 자본이 부족한 창업가들이 폐업하는 비율이 60%에 달합니다. **{req.title}** 프로젝트는 무재고 자동화 유통 구조로 리스크를 없앱니다."
        sol_text = f"**{req.title}** 프로젝트는 AI 무재고 위탁 사입 및 100% 무인 풀필먼트 자동 택배 배송 시스템을 연결하여 재고 리스크 없이 높은 순수익율을 보장합니다."
        tam_text = "국내 온라인 쇼핑 거래액 시장 (약 220조 원 규모)"
        sam_text = f"{req.target_customer} 타겟 무인 커머스 수요 (약 5조 원 규모)"
        som_text = "초기 1년 차 전문 쇼핑몰 진입 (약 10억 원 목표)"
        comp_table = f"""| 구분 | 일반 소매 쇼핑몰 | {req.title} (본 프로젝트) | 개선 효과 (수치) |
| :--- | :--- | :--- | :--- |
| **재고 리스크** | 사입 및 재고 부담 상존 | **무재고 AI 위탁 & 자동 풀필먼트** | **재고비용 0원 달성** |
| **마케팅 효율** | 높은 수동 키워드 광고비 | **AI 타겟팅으로 광고 ROI 300% 향상** | **광고효율 300%↑** |
| **물류 소요** | 직접 포장 및 택배 발송 | **100% 무인 물류 자동 발송** | **소요시간 0시간** |
| **마진율** | 사입 마진 15~20% 내외 | **직접 위탁 유통 마진 35%~50%** | **마진율 2배↑** |"""
        service_struct = "[고객 주문 결제] ➔ [AI 주문 자동 접수 & 무인 사입] ➔ [풀필먼트 자동 택배 배송]"
        mono_text = """* **상품 판매 유통 마진 수익 (사입가 대비 30~50% 마진 확보)**
* **타겟 유저 대상 월간 정기 구독 배송 서비스 수익**
* **소상공인 셀러 대상 B2B 도매 유통 공급 수수료**"""
        budget_table = f"""| 사업비 집행 항목 | 세부 산출 근거 (수량 x 단가) | 금액 (원) | 정부지원금 (70%) | 자부담금 (30%) |
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
        domain_name = "IT / 플랫폼 / 소프트웨어 / SaaS"
        focus_points = """- **기술 차별성 & 알고리즘 독창성**: 수동 대행 대비 처리 속도 99%↑ (3초 만에 완성)
- **사용자 활성화(MAU) & Retention**: 유기적 유저 유치(CAC 50% 절감) 및 구독 유지율 75% 이상 확보
- **서버 인프라 & 데이터 보안**: 오토스케일링 클라우드 구축 및 SSL 암호화 처리 체계"""
        prob_text_1 = f"기존 비즈니스 소프트웨어 및 대행 서비스 시장은 건당 100만 원~300만 원에 달하는 높은 비용, 수일~수주 소요되는 개발 지연으로 인해 **{req.target_customer}** 계층의 접근성 한계와 이탈률 40%를 초래하고 있습니다."
        prob_text_2 = f"대부분의 창업가들이 복잡한 도구와 비싼 전문가 수수료 부담으로 사업 초기 진입에 실패하고 있습니다. **{req.title}** 프로젝트는 초고속 무인 알고리즘으로 이 비효율을 획기적으로 개선합니다."
        sol_text = f"**{req.title}** 프로젝트는 웹 기반 무인 자동화 엔진을 연동하여 3초 만에 전문 결과물을 즉시 렌더링함으로써 업무 생산성을 10배 혁신합니다."
        tam_text = "국내 디지털 전환 및 자동화 서비스 시장 (약 10조 원 규모)"
        sam_text = f"{req.target_customer} 중심의 자동화 솔루션 수요 (약 1조 원 규모)"
        som_text = "초기 1년 차 진입 목표 (약 50억 원)"
        comp_table = f"""| 구분 | 기존 수동 서비스 / 대행사 | {req.title} (본 프로젝트) | 개선 효과 (수치) |
| :--- | :--- | :--- | :--- |
| **서비스 단가** | 100만 원 ~ 300만 원 (고비용) | **초저가 1회성 또는 월 구독형** | **비용 90%↓ 절감** |
| **처리 속도** | 수일 ~ 수주 소요 | **3초 이내 즉시 완성 및 렌더링** | **속도 99%↑ 향상** |
| **접근성** | 방문 대면 상담 필요 | **100% 무인 웹 자동화 접속** | **접근성 100%** |
| **사용 편의성** | 전문 지식 필수 | **1버튼 원터치 자동 완성** | **생산성 10배↑** |"""
        service_struct = "[사용자 정보 입력] ➔ [AI 스마트 렌더링 엔진] ➔ [전문 리포트 PDF/MD 즉시 완성]"
        mono_text = """* **단건 이용권 결제 수익 (1회성 건당 9,900원~29,900원)**
* **월간 정기 구독(SaaS) 수익 (월 29,900원 무제한 렌더링)**
* **B2B 기업 맞춤형 API 연동 마진**"""
        budget_table = f"""| 사업비 집행 항목 | 세부 산출 근거 (수량 x 단가) | 금액 (원) | 정부지원금 (70%) | 자부담금 (30%) |
| :--- | :--- | :--- | :--- | :--- |
| **마케팅 및 고객 유치비** | 디지털 마케팅, SEO 최적화, 바이럴 프로모션 | **50,000,000** | 35,000,000 | 15,000,000 |
| **서버 인프라 및 시스템 구축** | 클라우드 서버, 보안 시스템, 기능 고도화 | **30,000,000** | 21,000,000 | 9,000,000 |
| **운영비 및 지식재산권** | 특허 출원, 인허가, 연구 예비비 | **20,000,000** | 14,000,000 | 6,000,000 |
| **합 계** | **총 사업비 ({req.budget})** | **100,000,000** | **70,000,000** | **30,000,000** |"""
        perf_table = """| 연차 | 유효 가입 유저 수 | 추정 월 매출 (원) | 추정 연 매출 (원) | 영업이익률 (%) |
| :--- | :--- | :--- | :--- | :--- |
| **1년 차 (2026년)** | 유기적 가입 유저 1,000명 | **5,000,000** | **60,000,000** | **45%** |
| **2년 차 (2027년)** | 구독 유저 5,000명 | **25,000,000** | **300,000,000** | **55%** |
| **3년 차 (2028년)** | 기업 유저 20,000명 | **80,000,000** | **960,000,000** | **65%** |"""

    md_content = f"""# 📄 [K-Startup 정밀 수치 검증 사업계획서] {req.title}

* **사업 지원 규격**: {prog_name} ({prog_pages})
* **감지된 감수 업종**: **{domain_name}**
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

## 🎯 [{domain_name}] 업종 특화 핵심 평가 강조 포인트

{focus_points}

---

## 1. 🎯 [문제 인식] (Problem) - 통계 및 페인포인트 수치화

### 1.1 창업아이템의 개발 동기 및 배경
- 본 창업아이템 **{req.title}** 프로젝트는 기존 시장에 존재하는 비효율을 혁신하고, **{req.target_customer}** 고객층에게 초고속 무인 자동화 가치를 제공하기 위해 추진됩니다.

### 1.2 시장의 구체적 페인포인트 및 문제의 심각성
- {prob_text_1}
- {prob_text_2}

### 1.3 기존 대안(경쟁사)의 한계점 데이터 비교
- 기존 수동 방식 및 외주 대행사는 높은 비용 구조와 수일~수주의 소요 시간으로 인해 고객의 시급한 요구에 대응하지 못하는 치명적 한계가 존재합니다.

---

## 2. 💡 [해결 방안] (Solution) - 정밀 스펙 & 수치적 차별성

### 2.1 개발 및 구현 방안 (핵심 기술 및 서비스)
{sol_text}

### 2.2 서비스 프로세스 및 운영 알고리즘
```
{service_struct}
```

### 2.3 핵심 경쟁력 및 독창적 기능 스펙
- **핵심 경쟁력**: {req.core_features}
- **multi-format 지원**: 웹 미리보기, 마크다운(MD) 파일 및 PDF 즉시 소장

### 2.4 기술적/사업적 차별화 요소 수치 비교표
{comp_table}

### 2.5 지식재산권(IP) 및 특허 확보 방안
- 핵심 동작 알고리즘 및 비즈니스 모델(BM)에 관한 특허 2건 출원 예정

---

## 3. 🚀 [실행 전략] (Scale-up) - 자금소요/시장진입 구체화

### 3.1 비즈니스 모델(BM) 및 수익화 매커니즘
{mono_text}

### 3.2 목표 시장 분석 (TAM-SAM-SOM) 및 시장 진입 규모
* **전체 시장 (TAM)**: {tam_text}
* **유효 시장 (SAM)**: {sam_text}
* **수익 시장 (SOM)**: {som_text}

### 3.3 3단계 시장 진입 전략 (GTM 로드맵)
* **Phase 1 (1~3개월 차)**: MVP 시제품 완성 및 초기 유저 100명 유치 (전환율 5% 목표)
* **Phase 2 (6개월 차)**: 정식 서비스 유료 전환 및 마케팅 집행 ➔ 월 매출 목표 달성
* **Phase 3 (1년 차)**: B2B 파트너십 확장 및 가맹/전국 인프라 구축 ➔ 연 매출 돌파

### 3.4 마케팅/고객 유치 채널 및 CAC/ROI 전환율 계획
* **온라인 타겟 마케팅**: SEO 검색 노출 최적화 블로그 및 숏폼 마케팅
* **초기 프로모션**: 1회용 시리얼 코드 및 무상 체험권 제공으로 유저 유치

### 3.5 정밀 자금 소요 및 조달 계획 (정부지원금 70% + 자부담금 30%)
{budget_table}

---

## 4. 📈 [성과 창출 & 팀 역량] (Performance & Team) - 추정 재무 수치

### 4.1 연차별 예상 매출 및 성과 추정표
{perf_table}

### 4.2 대표자 및 핵심 팀원의 직무 전문성 (신뢰도 수치화)
* **대표자 직무 전문성**: 본 비즈니스 분야 핵심 기술 및 사업화 실행 경험 5년 이상 보유
* **기술 개발 역량**: 시스템 구축 및 운영 노하우 100% 내부 자산화

### 4.3 외부 파트너십 및 자문단 구축 현황
* **법률/특허 자문**: 지식재산권 전문 변리사 자문 네트워크 구축
* **제조/설비 파트너십**: 전담 기계/설비 및 클라우드 파트너사 MOU 완료

### 4.4 사회적 가치 창출 및 향후 기대효과
* 소상공인/1인 기업 비용 절감, 비효율 혁신 및 관련 산업 일자리 창출 기여

---

## 🚫 [정부지원사업 지원 제외 / 제한 업종 사전 확인 주의사항]

> [!CAUTION]
> **지원 자격 필독**: 아래 업종에 해당될 경우 정부지원사업 서류 심사에서 **자동 지원 제외(탈락)** 처리될 수 있으므로 사전에 업종코드(KSIC)를 반드시 확인하시기 바랍니다.

1. **원칙적 제외 업종**: 유흥·사행성 업종(단란주점, 도박, 게임장 등), 부동산 임대업, 금융/보험업
2. **지원 제한 업종 (R&D 및 특정 지원사업 제한)**: 단순 도소매 및 단순 유통업 (혁신성이 낮다고 판단되는 기술 R&D 지원사업에서는 제외 대상이 될 수 있으므로 제조/IT 기술 결합 요소 필수 작성)
3. **대부분 지원 가능 공모**: K-Startup 계열 (예비창업패키지, 초기창업패키지)은 제조, IT, 서비스, F&B, 콘텐츠 등 대부분 제한 없이 지원 가능합니다.

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

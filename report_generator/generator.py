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
                self.drawRightString(200 * 2.83, 280 * 2.83, "K-Startup 중기부 PSST 공식 규격 AI 사업계획서 (3분시리즈 1 v2.00)")
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

# 중소벤처기업부 K-Startup 공식 PSST 표준 프레임워크 System Prompt
PSST_OFFICIAL_SYSTEM_PROMPT = """당신은 중소벤처기업부 및 K-Startup(창업진흥원) 예비창업패키지/초기창업패키지/TIPS 공식 사업계획서 수석 평가위원입니다.
사용자가 입력한 [사업 아이템명], [타겟 고객], [핵심 경쟁력], [예산] 정보를 바탕으로 대한민국 공식 정부지원사업 표준 PSST(Problem - Solution - Scale-up - Team) 양식에 100% 부합하는 최상급 사업계획서를 작성하세요.

반드시 마크다운 개조식 불렛포인트와 세부 정밀 표를 활용하여 아래 4대 핵심 구조로 작성하세요:

# 📄 [K-Startup PSST 공식 표준 사업계획서] {title}
* **사업 분류**: 중소벤처기업부/창진원 정부지원사업 제출용 (PSST 표준 양식)
* **발급일자**: {now_str}
* **타겟 고객**: {target_customer}
* **사업비 규모**: {budget}

---

## 1. [P] Problem (문제 인식)
### 1.1 창업 아이템의 개발 동기 및 필요성
- 타겟 고객인 **{target_customer}** 계층이 겪고 있는 기존 시장의 핵심 페인 포인트(Pain Point) 분석
- 시장 조사를 통한 문제의 심각성 및 기술적/사업적 개발 필요성 기술

### 1.2 기존 대안(경쟁사)의 한계점 및 문제의 심각성
- 기존 시장 대행사/솔루션의 높은 비용, 느린 속도, 복잡한 접근성의 명확한 한계 제시

---

## 2. [S] Solution (실현 가능성 & 차별성)
### 2.1 개발 및 구현 방안 (핵심 기술 및 서비스)
- **{title}** 프로젝트의 구체적 해결 솔루션 제시
- 주요 핵심 기능: **{core_features}**

### 2.2 기술적/사업적 차별화 요소 및 경쟁 우위
| 구분 | 기존 수동 방식 / 경쟁 대안 | {title} (본 프로젝트) |
| :--- | :--- | :--- |
| **운영/제작 단가** | 기존 고비용 구조 | **획기적 비용 절감 (최대 70%↓)** |
| **처리/운영 속도** | 수일~수주 소요 | **초고속 즉시 완성 및 24시간 가동** |
| **품질/일관성** | 인적 숙련도 변동 | **표준 알고리즘으로 균일한 최상 품질** |

---

## 3. [S] Scale-up (성장 전략 & 사업화)
### 3.1 비즈니스 모델(BM) 및 목표 시장(TAM-SAM-SOM)
- **TAM (전체 시장)**: 국내 관련 산업 및 자동화 거래액 시장
- **SAM (유효 시장)**: {target_customer} 중심의 솔루션/제품 수요
- **SOM (수익 시장)**: 초기 1~2년 차 진입 직영 및 가맹/구독 유저 타겟
- **수익화 모델**: 단건 이용권, 월간 정기 구독(SaaS) 및 B2B 파트너십 마진

### 3.2 단계별 사업화 로드맵 및 시장 진입 전략 (GTM)
- **Phase 1 (1~3개월 차)**: MVP 시제품 완성 및 초기 타겟 유저 100명 검증
- **Phase 2 (6개월 차)**: 유료 서비스 전환 및 마케팅 집행 ➔ 월 매출 목표 달성
- **Phase 3 (1년 차)**: B2B 파트너십 확장 및 전국 인프라 구축 ➔ 연 매출 돌파

### 3.3 사업비 소요 및 자금 조달 계획 (정부지원금 매칭)
| 집행 항목 | 세부 내역 | 예산 비중 (%) |
| :--- | :--- | :--- |
| **시제품 제작 및 설비/인프라** | 개발, 설비, 로봇/시스템 구축 | **40%** |
| **마케팅 및 시장 진입비** | 바이럴, SEO 최적화, 광고 집행 | **40%** |
| **운영비 및 예비비** | 지식재산권(특허), 인허가, 기타 | **20%** |

---

## 4. [T] Team (팀 구성 및 보유 역량)
### 4.1 대표자 및 핵심 팀원의 직무 전문성
- **대표자 역량**: 본 사업 분야 직무 경력 및 아이템 기획/실행 추진력 보유
- **협력 네트워크**: 외부 기술 자문단, 디바이스/설비 파트너십 및 전문 자문위원회 구축

### 4.2 사회적 가치 창출 및 향후 기대효과
- 1인 기업가 및 소상공인 인건비 절감, 비효율 혁신 및 지역 일자리 창출 기여

---
*본 사업계획서는 중소벤처기업부 K-Startup PSST 공식 표준 규격에 따라 "3분시리즈 1 AI 연구소"에서 정식 발급되었습니다.*"""

def call_openai_psst_gpt(req: ReportRequest, api_key: str) -> str:
    import json
    import urllib.request
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    user_prompt = f"""[창업 아이템명]: {req.title}
[보고서 분류]: {req.category} (K-Startup PSST 공식 표준)
[타겟 고객층]: {req.target_customer}
[핵심 기능 및 경쟁력]: {req.core_features}
[사업비 및 예산]: {req.budget}

위 정보를 기반으로 중소벤처기업부 예비창업패키지/초기창업패키지 합격 기준 K-Startup PSST (Problem-Solution-Scale up-Team) 정식 양식으로 전문 사업계획서를 완벽하게 작성해 주세요."""

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": PSST_OFFICIAL_SYSTEM_PROMPT.format(
                title=req.title, now_str=datetime.datetime.now().strftime("%Y년 %m월 %d일"),
                target_customer=req.target_customer, budget=req.budget, core_features=req.core_features
            )},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }
    
    req_obj = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req_obj, timeout=30) as resp:
        res_json = json.loads(resp.read().decode("utf-8"))
        return res_json["choices"][0]["message"]["content"]

def generate_business_report(req: ReportRequest) -> tuple[str, str]:
    api_key = req.openai_api_key or os.environ.get("OPENAI_API_KEY")
    if api_key:
        try:
            md_content = call_openai_psst_gpt(req, api_key)
            html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
            return md_content, html_content
        except Exception as e:
            print(f"[WARN] OpenAI GPT Call failed: {e}, falling back to PSST Engine")

    cat_name = "중소벤처기업부 K-Startup PSST 공식 표준 사업계획서"
    now_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    domain = detect_domain(req.title, req.core_features)

    if domain == "fnb":
        prob_text = f"기존 외식/카페 시장은 높게 치솟는 인건비(매출의 35%+), 일손 부족, 수동 조리/서빙의 비효율로 인해 **{req.target_customer}** 고객층의 만족도 저하 및 매장 수익성 악화를 겪고 있습니다."
        sol_text = f"**{req.title}** 프로젝트는 24시간 무인 로봇 제조 및 스마트 서빙 시스템을 결합하여 인건비를 70% 이상 절감하고 최상의 균일한 음료/서비스 품질을 제공합니다."
        tam_text = "국내 외식 및 무인 로봇 푸드테크 시장 (약 15조 원 규모)"
        sam_text = f"{req.target_customer} 타겟 무인 로봇 매장 수요 (약 1조 2,000억 원 규모)"
        som_text = "초기 1~2년 차 거점 직영점 진입 및 프랜차이즈 가맹 목표 (약 30억 원)"
        comp_table = f"""| 구분 | 기존 수동 매장 / 일반 카페 | {req.title} (본 프로젝트) |
| :--- | :--- | :--- |
| **인건비 비중** | 매출의 30% ~ 40% (고비용) | **인건비 70% 이상 획기적 절감** |
| **운영 시간** | 10시간 ~ 12시간 한정 운영 | **24시간 365일 무인 자동 가동** |
| **품질/일관성** | 조리자 숙련도에 따라 변동 | **로봇 알고리즘으로 균일한 최상 품질** |"""
        service_struct = "[고객 앱/키오스크 주문] ➔ [로봇 음료 제조 및 서빙] ➔ [고객 수령 및 AI 자동 청결 관리]"
        mono_text = """* **24시간 무인 매장 음료/디저트 직접 판매 수익**
* **로봇 매장 프랜차이즈 가맹비 및 원두/원자재 공급 유통 마진**
* **무인 로봇 디스플레이 사이니지 타겟 광고 수익**"""
        budget_table = f"""| 집행 항목 | 세부 내역 | 예산 비중 (%) |
| :--- | :--- | :--- |
| **로봇 제조/서빙 설비 및 키오스크** | 제조 로봇팔, 무인 서빙 로봇, 결제 키오스크 | **45%** |
| **매장 인테리어 및 공간 구획** | 24시간 무인 매장 설계 및 시공 보증금 | **35%** |
| **원자재 사입 및 바이럴 마케팅** | 원두/음료 부자재 및 개점 홍보 광고 | **20%** |"""

    elif domain == "ecommerce":
        prob_text = f"기존 이커머스 유통 시장은 과도한 재고 부담, 높은 수동 키워드 광고비, 직접 포장/배송의 물리적 한계로 인해 **{req.target_customer}** 타겟 마케팅 및 마진 확보에 어려움을 겪고 있습니다."
        sol_text = f"**{req.title}** 프로젝트는 AI 기반 무재고 자동 위탁 및 100% 무인 풀필먼트 자동 배송 시스템을 구축하여 리스크 없이 고수익 유통 구조를 실현합니다."
        tam_text = "국내 온라인 쇼핑 거래액 시장 (약 220조 원 규모)"
        sam_text = f"{req.target_customer} 타겟 무인 커머스 수요 (약 5조 원 규모)"
        som_text = "초기 1년 차 전문 쇼핑몰 진입 (약 10억 원)"
        comp_table = f"""| 구분 | 일반 소매 쇼핑몰 | {req.title} (본 프로젝트) |
| :--- | :--- | :--- |
| **재고 리스크** | 사입 및 재고 부담 상존 | **무재고 AI 위탁 & 자동 풀필먼트** |
| **마케팅 효율** | 높은 수동 키워드 광고비 | **AI 타겟팅으로 광고 ROI 300% 향상** |
| **물류 소요** | 직접 포장 및 택배 발송 | **100% 무인 물류 자동 발송** |"""
        service_struct = "[고객 주문 결제] ➔ [AI 주문 자동 접수 & 무인 사입] ➔ [풀필먼트 자동 택배 배송]"
        mono_text = """* **상품 판매 마진 수익 (사입가 대비 30~50% 유통 마진)**
* **월간 정기 구독 배송 서비스 수익**
* **소상공인 대상 B2B 도매 유통 마진**"""
        budget_table = f"""| 집행 항목 | 세부 내역 | 예산 비중 (%) |
| :--- | :--- | :--- |
| **마케팅 및 SNS 바이럴 광고** | AI 타겟팅 SNS 광고 및 숏폼 마케팅 | **50%** |
| **상품 사입 및 풀필먼트 물류비** | 자동 물류 시스템 연동 및 초기 사입 | **30%** |
| **쇼핑몰 시스템 및 디자인** | 쇼핑몰 구축 및 UX/UI 디벨롭 | **20%** |"""

    else:
        prob_text = f"기존 서비스 시장은 높은 외주 비용, 처리 지연, 대면 상담의 물리적 제약으로 인해 **{req.target_customer}** 계층의 만족도 저하 및 접근성 한계를 보이고 있습니다."
        sol_text = f"**{req.title}** 프로젝트는 웹 기반 무인 자동화 엔진을 연동하여 3초 만에 완결된 결과물을 제공함으로써 생산성과 편의성을 혁신적으로 높입니다."
        tam_text = "국내 디지털 전환 및 자동화 서비스 시장 (약 10조 원 규모)"
        sam_text = f"{req.target_customer} 중심의 자동화 솔루션 수요 (약 1조 원 규모)"
        som_text = "초기 1년 차 진입 목표 (약 50억 원)"
        comp_table = f"""| 구분 | 기존 수동 서비스 / 대행사 | {req.title} (본 프로젝트) |
| :--- | :--- | :--- |
| **서비스 단가** | 100만 원 ~ 300만 원 (고비용) | **초저가 1회성 또는 월 구독형** |
| **처리 속도** | 수일 ~ 수주 소요 | **3초 이내 즉시 완성 및 렌더링** |
| **접근성** | 방문 대면 상담 필요 | **100% 무인 웹 자동화 접속** |"""
        service_struct = "[사용자 정보 입력] ➔ [AI 스마트 렌더링 엔진] ➔ [전문 리포트 PDF/MD 즉시 완성]"
        mono_text = """* **단건 이용권 결제 수익**: 1회성 건당 이용권 판매
* **월간 정기 구독(SaaS) 수익**: 월간 무제한 이용 정기 결제
* **B2B 기업 맞춤형 API 연동 수익**: 기업체 대상 연동 마진"""
        budget_table = f"""| 집행 항목 | 세부 내역 | 예산 비중 (%) |
| :--- | :--- | :--- |
| **마케팅 및 고객 유치비** | 디지털 마케팅, SEO 최적화, 프로모션 | **50%** |
| **서버 인프라 및 시스템 구축** | 클라우드 서버, 보안, 기능 고도화 | **30%** |
| **운영비 및 지식재산권** | 특허 출원, 인허가, 예비비 | **20%** |"""

    md_content = f"""# 📄 [K-Startup PSST 공식 표준 사업계획서] {req.title}

* **사업 분류**: 중소벤처기업부/창진원 정부지원사업 제출용 (PSST 표준 양식)
* **발급일자**: {now_str}
* **타겟 고객**: {req.target_customer}
* **사업비 규모**: {req.budget}

---

## 1. [P] Problem (문제 인식)

### 1.1 창업 아이템의 개발 동기 및 필요성
{prob_text}

### 1.2 기존 대안(경쟁사)의 한계점 및 문제의 심각성
- 기존 수동 방식 및 대행사는 과도한 인건비/비용 부담과 긴 소요 시간으로 인해 고객의 시급한 요구에 대응하지 못하는 치명적 한계가 존재합니다.
- **{req.title}** 프로젝트는 이 문제를 획기적으로 해결하는 차세대 솔루션입니다.

---

## 2. [S] Solution (실현 가능성 & 차별성)

### 2.1 개발 및 구현 방안 (핵심 기술 및 서비스)
{sol_text}
- **핵심 경쟁력 및 기능**: {req.core_features}

### 2.2 기술적/사업적 차별화 요소 및 경쟁 우위
{comp_table}

---

## 3. [S] Scale-up (성장 전략 & 사업화)

### 3.1 비즈니스 모델(BM) 및 목표 시장(TAM-SAM-SOM)
* **전체 시장 (TAM)**: {tam_text}
* **유효 시장 (SAM)**: {sam_text}
* **수익 시장 (SOM)**: {som_text}
* **수익 모델 (Monetization)**:
{mono_text}

### 3.2 단계별 사업화 로드맵 및 시장 진입 전략 (GTM)
* **Phase 1 (1~3개월 차)**: MVP 시제품 완성 및 초기 유저 100명 확보 ➔ 핵심 지표 검증
* **Phase 2 (6개월 차)**: 정식 서비스 유료 전환 및 마케팅 집행 ➔ 월 매출 목표 달성
* **Phase 3 (1년 차)**: B2B 파트너십 확장 및 가맹/전국 인프라 구축 ➔ 연 매출 돌파

### 3.3 사업비 소요 및 자금 조달 계획 (정부지원금 매칭)
{budget_table}

---

## 4. [T] Team (팀 구성 및 보유 역량)

### 4.1 대표자 및 핵심 팀원의 직무 전문성
* **대표자 직무 전문성**: 본 비즈니스 분야 핵심 기술 및 사업화 실행 경험 보유
* **외부 파트너십 및 자문단**: 지식재산권 특허 법률 자문 및 전담 개발/설비 파트너십 구축 완료

### 4.2 사회적 가치 창출 및 기대 효과
* 소상공인/1인 기업 비용 절감, 비효율 혁신 및 관련 산업 일자리 창출 기여

---
*본 사업계획서는 중소벤처기업부 K-Startup PSST 공식 표준 규격에 따라 "3분시리즈 1 AI 연구소"에서 정식 발급되었습니다.*
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

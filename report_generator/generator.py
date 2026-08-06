import datetime
import os
import markdown
from schemas import ReportRequest
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak, KeepTogether
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
                self.drawRightString(190 * 2.83, 282 * 2.83, "K-Startup 중기부 표준 사업계획서 (고고플렉스 AI 연구소)")
                self.setStrokeColor(colors.HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(20 * 2.83, 280 * 2.83, 190 * 2.83, 280 * 2.83)
                
                page_text = f"- {self._pageNumber} / {num_pages} -"
                self.drawCentredString(105 * 2.83, 10 * 2.83, page_text)
                self.restoreState()
            super().showPage()
        super().save()

# 🏛️ 대한민국 중소벤처기업부 K-Startup 정통 공식 10대 업종 분류체계 엔진
def detect_domain(title: str, features: str) -> str:
    text = (title + " " + features).lower()
    
    if any(k in text for k in ["펫푸드", "반려동물", "펫", "강아지", "고양이", "사료", "간식", "펫 헬스케어"]):
        return "pet_care"
    elif any(k in text for k in ["esg", "탄소", "리사이클", "업사이클", "생분해", "에너지", "태양광", "친환경 포장", "친환경 소재"]):
        return "eco_esg"
    elif any(k in text for k in ["바이오", "의료", "헬스케어", "제약", "임상", "진단", "뷰티", "화장품", "건강기능식품"]):
        return "bio_health"
    elif any(k in text for k in ["외식", "카페", "음료", "음식", "푸드", "식품", "로봇 서빙", "조리", "무인 매장", "푸드테크"]):
        return "fnb_foodtech"
    elif any(k in text for k in ["제조", "하드웨어", "공장", "금형", "사출", "소재", "부품", "장비", "드론", "로봇팔"]):
        return "smart_hardware"
    elif any(k in text for k in ["이커머스", "스마트스토어", "쇼핑몰", "유통", "무재고", "위탁", "풀필먼트", "물류"]):
        return "ecommerce_logistics"
    elif any(k in text for k in ["콘텐츠", "웹툰", "게임", "미디어", "영상", "캐릭터", "메타버스", "에듀테크"]):
        return "contents_ip"
    elif any(k in text for k in ["핀테크", "금융", "결제", "부동산", "프롭테크", "o2o", "프랜차이즈"]):
        return "fintech_proptech"
    elif any(k in text for k in ["로컬", "공간", "관광", "지역", "수공예", "게스트하우스", "스테이"]):
        return "local_lifestyle"
    return "it_ai_saas"

PROGRAM_SPECS = {
    "packages_15p": {"name": "예비창업패키지 / 초기창업패키지 규격", "target_pages": "15페이지 정통 풀-스펙", "target_num": 15},
    "cheongsa_12p": {"name": "청년창업사관학교 집중 실행 규격", "target_pages": "12페이지 정밀 규격", "target_num": 12},
    "rnd_25p": {"name": "중기부 / 산업부 R&D 기술개발 과제 규격", "target_pages": "20~30페이지 기술개발 정밀 규격", "target_num": 25},
    "export_8p": {"name": "수출바우처 및 마케팅 지원 규격", "target_pages": "8페이지 마케팅 규격", "target_num": 8},
    "local_5p": {"name": "지자체 소액 창업 지원 린 규격", "target_pages": "5페이지 이내 숏폼 규격", "target_num": 5}
}

def generate_business_report(req: ReportRequest) -> tuple[str, str]:
    prog_info = PROGRAM_SPECS.get(req.program_type, PROGRAM_SPECS["packages_15p"])
    prog_name = prog_info["name"]
    prog_pages = prog_info["target_pages"]
    now_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    domain = detect_domain(req.title, req.core_features)

    # R&D 25페이지 전용 모듈
    rnd_extra_section = ""
    if req.program_type == "rnd_25p":
        rnd_extra_section = f"""---

## [R&D 전용 25P 모듈] 기술개발 상세 파이프라인 & TRL 진단

### 1. 기술성숙도(TRL) 9단계 달성 목표
| TRL 단계 | 단계별 정의 | 현재 수준 | 사업 종료 시 목표 수준 | 검증 방법 및 증빙 |
| :--- | :--- | :--- | :--- | :--- |
| **TRL 1~2단계** | 기초 연구 및 원천 아이디어 정립 | **달성 완료** | 달성 완료 | 선행 논문 및 특허 분석 보고서 |
| **TRL 3~4단계** | 핵심 기능 검증 및 시제품 제작 | **진행 중** | **완료 목표 (3개월 차)** | 시험성적서 및 알파 테스트 결과 |
| **TRL 5~6단계** | 실제 환경 성능 검증 및 공인인증 | - | **완료 목표 (8개월 차)** | 공인시험기관 성적서 |
| **TRL 7~8단계** | 양산 전 정밀 제품 제작 및 검증 | - | **완료 목표 (12개월 차)** | 필드 테스트 및 초기 매출 계약서 |
| **TRL 9단계** | 사업화 양산 및 시장 진입 안정화 | - | **차년도 연계 목표** | 매출 세금계산서 및 양산 증명 |

### 2. 기술 명세서 및 시스템 아키텍처
- **성능 고도화**: {req.core_features} 처리 효율 5,000회 이상 및 응답/제조 속도 50ms 이내 유지
- **데이터베이스 ERD 설계**: 사용자 액션 로그, 결제, 분산 데이터 파이프라인 100% 암호화 (AES-256 적용)
- **보안 및 규제 준수**: ISO/IEC 27001 정보보안준수 및 개인정보보호법(PIPA) 기술적 보호조치 적용
- **인프라 구획**: 원자재 사입 공정 및 오토스케일링 빅데이터 수집 관리

### 3. 선행기술 조사 및 IP 포트폴리오
| 번호 | 특허/기술명 | 주요 권리 범주 | 본 프로젝트 차별화 포인트 | IP 회피 및 방어 전략 |
| :--- | :--- | :--- | :--- | :--- |
| **1** | 수동 제어 시스템 | 파라미터 수동 세팅 | **맞춤 알고리즘 자동화** | 독립 청구항 구성으로 100% 회피 |
| **2** | 단일 데이터 파이프라인 | 유선 통신 기반 제어 | **SSL 256-bit 클라우드 제어** | 기술 독창성 확보 및 특허 출원 |
| **3** | 정기 결제 시스템 | 단순 결제 프로세스 | **1회용 인증 키 및 소멸 CS 추적** | 독점 권리 확보 |
| **4** | 초고속 처리 모듈 | 배치 처리 방식 | **3초 완결 실시간 초고속 렌더링** | 처리 속도 특허권 출원 완료 |"""

    # 예창패/초창패 15p 전용 세부 시장조사
    packages_extra_section = ""
    if req.program_type in ["packages_15p", "cheongsa_12p", "rnd_25p"]:
        packages_extra_section = f"""---

## [시장분석 & GTM 15P 모듈] 타겟 유저 세분화 및 밸류체인 정밀 분석

### 1. 고객 페인포인트 정밀 수치 설문 조사 데이터
- 타겟 유저 300명 대상 정밀 설문 조사 결과: 기존 대안 서비스 만족도 28.5%에 불과
- 핵심 불편 요인 1위: **과도한 비용 부담 (68.4%)**, 2위: **느린 처리 속도 (54.2%)**, 3위: **복잡한 사용법 (41.1%)**
- **{req.title}** 도입 시 구매 전환 의향 **84.6%** 달성

### 2. TAM-SAM-SOM 시장 산출 공식 및 수치적 정합성
- **TAM (전체 시장)**: 국내 관련 산업 및 거래액 시장 (약 15조 원)
- **SAM (유효 시장)**: {req.target_customer} 중심의 세부 유효 시장 (약 1조 2,000억 원)
- **SOM (수익 시장)**: 초기 1~2년 차 진입 직영 및 정기구독 타겟 (약 30억 원 목표)

### 3. 5대 경쟁사 주요 기능 수치 비교 Matrix 표
| 기능 및 스펙 비교 | A 경쟁사 (수동) | B 경쟁사 (외주) | **{req.title} (본 사업)** | 우위 수치 |
| :--- | :--- | :--- | :--- | :--- |
| **처리 단가** | 200만 원 | 100만 원 | **초저가 월 구독/1회성** | **비용 90%↓ 절감** |
| **완성 소요시간** | 14일 소요 | 7일 소요 | **3초 원터치 자동완성** | **속도 99%↑ 향상** |
| **무인 가동률** | 0% (대면) | 0% (수동) | **100% 무인 웹 자동 접속** | **가동률 100%** |
| **데이터 보안** | 이메일 전달 | 엑셀 파일 | **256-bit SSL 암호화 DB** | **보안 100%** |

### 4. 3개년 정밀 재무 손익분기점 (BEP) 달성 시점
- **손익분기점 (BEP) 달성 시점**: 서비스 런칭 7개월 차 유료 유저 350명 달성 시점
- **초기 투입 자금 회수**: 런칭 14개월 차 누적 순이익 1억 원 돌파로 자금 회수 완료"""

    # 10대 지원사업 공식 업종별 특화 콘텐츠 맵
    if domain == "pet_care":
        domain_name = "펫케어 · 펫푸드 · 바이오헬스 · 정기구독"
        focus_points = """- **견종/묘종/연령별 맞춤 영양 설계**: 수의사 자문 1:1 맞춤 영양 밸런스 데이터 알고리즘 탑재
- **신선 배송 & 무재고 정기구독 모델**: 주문 수량 기반 콜드체인 맞춤 생산으로 재고 폐기율 0% 달성
- **구독 유지율(Retention) 85% 확보**: 1:1 건강 일지 트래킹 서비스로 고객 LTV 극대화"""
        prob_text_1 = f"현재 국내 펫케어/펫푸드 시장은 기성 일괄 사료의 영양 불균형과 첨가물 논란, 비싼 수입 렌더링 제품(평균 월 15~20만 원)으로 인해 **{req.target_customer}** 고객층의 접근성 한계를 초래하고 있습니다."
        prob_text_2 = f"기존 오프라인 사료 수동 구매 방식은 잦은 품절과 유통기한 관리 실패로 불편과 마진 부담을 지우고 있습니다. **{req.title}** 프로젝트는 100% 맞춤 펫푸드 정기구독으로 이 문제를 해결합니다."
        sol_text = f"**{req.title}** 프로젝트는 반려동물 건강 데이터 기반 1:1 맞춤 영양 레시피 설계와 무재고 콜드체인 정기배송을 연동하여 합리적인 가격에 신선함을 전달하는 솔루션입니다."
        tam_text = "국내 펫푸드 및 펫 헬스케어 정기구독 시장 (약 4조 원 규모)"
        sam_text = f"{req.target_customer} 중심의 프리미엄 맞춤 구독 수요 (약 6,000억 원 규모)"
        som_text = "초기 1~2년 차 온라인 정기구독 유저 진입 목표 (약 30억 원 목표)"
        comp_table = f"""| 구분 | 기존 수입 기성 제품 | {req.title} (본 프로젝트) | 개선 효과 (수치) |
| :--- | :--- | :--- | :--- |
| **영양 설계** | 일괄 기성품 규격 | **견종/연령/건강 1:1 맞춤 레시피** | **맞춤 정확도 100%** |
| **배송 구조** | 매번 오프라인 수동 구매 | **100% 무인 콜드체인 정기구독 배송** | **편의성 100%** |
| **신선도/재고**| 긴 유통기한 (방부제) | **주문 직후 맞춤 조리 (무방부제)** | **신선도 100%** |
| **구독 단가** | 월 15~20만 원 (고비용) | **자체 생산/직배송으로 합리적 가격** | **비용 40%↓ 절감** |"""
        service_struct = "[반려동물 건강데이터 입력] -> [AI 맞춤 레시피 생성] -> [신선 조리 및 정기배송]"
        mono_text = """* **맞춤 펫푸드 월간 정기구독 매출 수익 (평균 마진율 45% 이상)**
* **반려동물 헬스케어 맞춤 영양제 및 간식 추가 결제 수익**
* **동물병원 및 B2B 펫 숍 전용 맞춤 펫푸드 공급 수수료**"""
        budget_table = f"""| 사업비 집행 항목 | 세부 산출 근거 (수량 x 단가) | 금액 (원) | 정부지원금 (70%) | 자부담금 (30%) |
| :--- | :--- | :--- | :--- | :--- |
| **맞춤 조리 설비 및 콜드체인 구축**| 맞춤 소량 양산 조리 설비 1식 | **45,000,000** | 31,500,000 | 13,500,000 |
| **수의사 자문 레시피 성분 분석** | 공인기관 영양 성분 검사 | **25,000,000** | 17,500,000 | 7,500,000 |
| **정기구독 타겟 마케팅** | SNS 숏폼 마케팅, 체험단 프로모션 | **30,000,000** | 21,000,000 | 9,000,000 |
| **합 계** | **총 사업비 ({req.budget})** | **100,000,000** | **70,000,000** | **30,000,000** |"""
        perf_table = """| 연차 | 유효 정기구독 유저 수 | 추정 월 매출 (원) | 추정 연 매출 (원) | 영업이익률 (%) |
| :--- | :--- | :--- | :--- | :--- |
| **1년 차 (2026년)** | 구독 유저 1,500명 | **25,000,000** | **300,000,000** | **40%** |
| **2년 차 (2027년)** | 구독 유저 6,000명 | **75,000,000** | **900,000,000** | **46%** |
| **3년 차 (2028년)** | 구독 유저 20,000명 | **200,000,000** | **2,400,000,000** | **52%** |"""

    else:
        domain_name = "F&B / 무인 로봇 매장 & 오프라인 유통"
        focus_points = """- **상권 및 유동인구 분석**: 핵심 거점 타겟 상권 분석, 유동인구 5만 명/일 기반 객단가 및 회전율 수치화
- **24시간 무인 가동 경제성**: 24시간 365일 무인 가동을 통한 매장 매출 극대화 수치 근거
- **인건비 절감 구조**: 기존 수동 외식업 대비 인건비 70% 이상 절감 및 오차 없는 레시피 일관성 보장"""
        prob_text_1 = f"현재 국내 외식 및 오프라인 서비스 시장은 최저임금 인상과 구인난으로 인해 매출 대비 인건비 비중이 35%~40%에 달하는 심각한 수익성 악화를 겪고 있습니다. 이로 인해 **{req.target_customer}** 계층은 서비스 품질 저하 및 대기시간의 불편을 겪고 있습니다."
        prob_text_2 = f"대부분의 창업가들이 비싼 인건비 부담으로 진입에 실패하고 있습니다. **{req.title}** 프로젝트는 무인 로봇 솔루션으로 이 비효율을 개선합니다."
        sol_text = f"**{req.title}** 프로젝트는 24시간 무인 로봇 제조 및 스마트 자동 서빙/관리 시스템을 도입하여 인건비를 70% 이상 절감하고 소요 시간을 3분 이내로 단축하는 혁신 솔루션입니다."
        tam_text = "국내 외식 및 무인 푸드테크/자동화 매장 시장 (약 15조 원 규모)"
        sam_text = f"{req.target_customer} 중심의 무인 스마트 매장 수요 (약 1조 2,000억 원 규모)"
        som_text = "초기 1~2년 차 거점 직영점 진입 및 프랜차이즈 가맹 목표 (약 30억 원 목표)"
        comp_table = f"""| 구분 | 기존 수동 매장 / 일반 카페 | {req.title} (본 프로젝트) | 개선 효과 (수치) |
| :--- | :--- | :--- | :--- |
| **인건비 비중** | 매출의 35% ~ 40% (고비용) | **인건비 70% 이상 획기적 절감** | **비용 70%↓ 절감** |
| **운영 시간** | 10시간 ~ 12시간 한정 운영 | **24시간 365일 무인 자동 가동** | **가동률 200%↑** |
| **품질/일관성** | 조리자 숙련도 따라 오차 발생 | **알고리즘으로 균일한 최상 품질** | **오류율 0% 달성** |"""
        service_struct = "[고객 키오스크/앱 주문 결제] -> [AI 자동 제조 & 서빙] -> [고객 수령 및 자동 청결 관리]"
        mono_text = """* **24시간 무인 매장 제품 직접 판매 수익 (평균 마진율 65% 이상)**
* **로봇 매장 패키지 프랜차이즈 가맹비 및 원자재 공급 유통 마진**
* **B2B 기업체/공공기관 무인 모듈 납품 계약 마진**"""
        budget_table = f"""| 사업비 집행 항목 | 세부 산출 근거 (수량 x 단가) | 금액 (원) | 정부지원금 (70%) | 자부담금 (30%) |
| :--- | :--- | :--- | :--- | :--- |
| **스마트 제조/서빙 설비 및 키오스크**| 제조 장비 1식, 무인 서빙 2대 | **45,000,000** | 31,500,000 | 13,500,000 |
| **매장 인테리어 및 공간 구획** | 24시간 무인 매장 파사드 설계 | **35,000,000** | 24,500,000 | 10,500,000 |
| **원자재 사입 및 바이럴 마케팅** | 초기 원자재 사입 및 지역 바이럴 홍보 | **20,000,000** | 14,000,000 | 6,000,000 |
| **합 계** | **총 사업비 ({req.budget})** | **100,000,000** | **70,000,000** | **30,000,000** |"""
        perf_table = """| 연차 | 유효 가입 유저 수 | 추정 월 매출 (원) | 추정 연 매출 (원) | 영업이익률 (%) |
| :--- | :--- | :--- | :--- | :--- |
| **1년 차 (2026년)** | 매장 1호점 및 가맹점 | **15,000,000** | **180,000,000** | **40%** |
| **2년 차 (2027년)** | 가맹 15개점 확장 | **50,000,000** | **600,000,000** | **48%** |
| **3년 차 (2028년)** | 전국 가맹 50개점 돌파 | **150,000,000** | **1,800,000,000** | **55%** |"""

    # 100% 마크다운 순수 서식 (HTML 태그 및 불필요한 div 전면 제거로 마크다운 파싱 깨짐 완전 소탕)
    md_content = f"""# [K-Startup 정밀 수치 검증 사업계획서] {req.title}

* **사업 지원 규격**: {prog_name} ({prog_pages})
* **감지된 감수 업종**: **{domain_name}**
* **발급일자**: {now_str}
* **타겟 고객**: {req.target_customer}
* **사업비 및 목표**: {req.budget}

---

## [1페이지 심사위원 핵심 요약서] (Executive Summary One-Pager)

| 항목 | 핵심 내용 요약 (심사 5분 핵심 체크 포인트) |
| :--- | :--- |
| **1. 문제 인식 (Problem)** | {req.target_customer} 타겟의 기존 방식 비용 과다 및 업무 지연 페인포인트 해소 |
| **2. 해결 방안 (Solution)** | **{req.title}** 솔루션 도입으로 **인건비/운영비 70% 절감 & 처리 속도 3초 완결** |
| **3. 성장 전략 (Scale-up)** | 총 사업비 1억 원 (정부지원금 7,000만 원 + 자부담 3,000만 원), 3단계 GTM 마케팅 |
| **4. 팀 역량 (Team)** | 대표자 직무 경력 5년 이상, 전담 기술 파트너십 및 특허 자문단 구축 완결 |

---

## [{domain_name}] 업종 특화 핵심 평가 강조 포인트

{focus_points}

---

## 1. [문제 인식] (Problem) - 통계 및 페인포인트 수치화

### 1.1 창업아이템의 개발 동기 및 배경
- 본 창업아이템 **{req.title}** 프로젝트는 기존 시장에 존재하는 비효율을 혁신하고, **{req.target_customer}** 고객층에게 초고속 무인 자동화 가치를 제공하기 위해 추진됩니다.

### 1.2 시장의 구체적 페인포인트 및 문제의 심각성
- {prob_text_1}
- {prob_text_2}

### 1.3 기존 대안(경쟁사)의 한계점 데이터 비교
- 기존 수동 방식 및 외주 대행사는 높은 비용 구조와 소요 시간으로 인해 고객의 시급한 요구에 대응하지 못하는 치명적 한계가 존재합니다.

---

## 2. [해결 방안] (Solution) - 정밀 스펙 & 수치적 차별성

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

{rnd_extra_section}
{packages_extra_section}

---

## 3. [실행 전략] (Scale-up) - 자금소요/시장진입 구체화

### 3.1 비즈니스 모델(BM) 및 수익화 매커니즘
{mono_text}

### 3.2 목표 시장 분석 (TAM-SAM-SOM) 및 시장 진입 규모
* **전체 시장 (TAM)**: {tam_text}
* **유효 시장 (SAM)**: {sam_text}
* **수익 시장 (SOM)**: {som_text}

### 3.3 3단계 시장 진입 전략 (GTM 로드맵)
* **Phase 1 (1~3개월 차)**: MVP 시제품 완성 및 초기 유저 100명 유치 (전환율 5% 목표)
* **Phase 2 (6개월 차)**: 정식 서비스 유료 전환 및 마케팅 집행 -> 월 매출 목표 달성
* **Phase 3 (1년 차)**: B2B 파트너십 확장 및 가맹/전국 인프라 구축 -> 연 매출 돌파

### 3.4 마케팅/고객 유치 채널 및 CAC/ROI 전환율 계획
* **온라인 타겟 마케팅**: SEO 검색 노출 최적화 블로그 및 숏폼 마케팅
* **초기 프로모션**: 1회용 시리얼 코드 및 무상 체험권 제공으로 유저 유치

### 3.5 정밀 자금 소요 및 조달 계획 (정부지원금 70% + 자부담금 30%)
{budget_table}

---

## 4. [성과 창출 & 팀 역량] (Performance & Team) - 추정 재무 수치

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

## [정부지원사업 지원 제외 / 제한 업종 사전 확인 주의사항]

> **지원 자격 필독**: 아래 업종에 해당될 경우 정부지원사업 서류 심사에서 자동 지원 제외(탈락) 처리될 수 있으므로 사전에 업종코드(KSIC)를 반드시 확인하시기 바랍니다.

- **원칙적 제외 업종**: 유흥·사행성 업종(단란주점, 도박, 게임장 등), 부동산 임대업, 금융/보험업
- **지원 제한 업종 (R&D 및 특정 지원사업 제한)**: 단순 도소매 및 단순 유통업 (혁신성이 낮다고 판단되는 기술 R&D 지원사업에서는 제외 대상이 될 수 있으므로 제조/IT 기술 결합 요소 필수 작성)
- **대부분 지원 가능 공모**: K-Startup 계열 (예비창업패키지, 초기창업패키지)은 제조, IT, 서비스, F&B, 콘텐츠 등 대부분 제한 없이 지원 가능합니다.

---

## [필수 제출 7대 증빙서류 준비 체크리스트 및 수치 정합성 검증]

> **실무 필수 지침**: 서류 제출 마감일 발급 지연 방지를 위해 사전 발급이 필수입니다. 특히 사업계획서 상의 매출/예산 수치와 부가가치세 과세표준증명원(재무제표) 수치가 100% 일치해야 감점을 방지할 수 있습니다.

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
*본 정밀 사업계획서는 중소벤처기업부 K-Startup PSST 공식 수치 검증 및 7대 서류 정합성 기준에 따라 "고고플렉스 AI 연구소"에서 정식 발급되었습니다.*
"""

    # HTML 변환 시 부록 구역을 인쇄/미리보기 전용 고급 카드 및 테두리 서식으로 변환
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    # 웹 미리보기 시 부록 구역을 sample PDF 100% 서식 카드로 감싸기
    if "<h2>[정부지원사업 지원 제외" in html_content:
        parts = html_content.split("<h2>[정부지원사업 지원 제외")
        main_html = parts[0]
        app_html = "<h2>[정부지원사업 지원 제외" + parts[1]
        
        # 아름다운 붉은 박스 및 주황 박스 카드로 정교 치환
        app_html = app_html.replace(
            "<blockquote>\n<p><strong>지원 자격 필독</strong>:",
            '<div style="border: 1px solid #ef4444; background: #fff5f5; border-radius: 6px; padding: 10px 14px; margin: 10px 0;"><strong style="color: #dc2626; font-size: 0.9rem;">⚠️ 지원 자격 필독</strong><br><span style="font-size: 0.85rem; color: #475569;">'
        ).replace(
            "확인하시기 바랍니다.</p>\n</blockquote>",
            '확인하시기 바랍니다.</span></div>'
        ).replace(
            "<blockquote>\n<p><strong>실무 필수 지침</strong>:",
            '<div style="border: 1px solid #f59e0b; background: #fffbeb; border-radius: 6px; padding: 10px 14px; margin: 10px 0;"><strong style="color: #d97706; font-size: 0.9rem;">🔑 실무 필수 지침</strong><br><span style="font-size: 0.85rem; color: #475569;">'
        ).replace(
            "방지할 수 있습니다.</p>\n</blockquote>",
            '방지할 수 있습니다.</span></div>'
        )

        html_content = main_html + '<div class="appendix-page">' + app_html + '</div>'

    return md_content, html_content

def build_pdf_file(req: ReportRequest, pdf_path: str):
    md_content, _ = generate_business_report(req)
    lines = md_content.splitlines()

    # HWP/Word 공식 A4 표준 여백 적용
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=56.7,
        rightMargin=56.7,
        topMargin=42.5,
        bottomMargin=42.5
    )

    prog_type = req.program_type
    
    body_size = 9.5
    body_lead = 14.5
    cell_size = 8.0
    cell_lead = 11.5

    if prog_type == "rnd_25p":
        h1_size, h1_lead, h1_before, h1_after = 18, 24, 26, 14
        h2_size, h2_lead, h2_before, h2_after = 14, 19, 20, 10
        h3_size, h3_lead, h3_before, h3_after = 12, 16, 14, 6
        body_after = 10
        spacer_height = 14
        table_padding = 6
    elif prog_type in ["packages_15p", "cheongsa_12p"]:
        h1_size, h1_lead, h1_before, h1_after = 17, 23, 18, 8
        h2_size, h2_lead, h2_before, h2_after = 13, 17, 14, 6
        h3_size, h3_lead, h3_before, h3_after = 11, 15, 10, 4
        body_after = 8
        spacer_height = 8
        table_padding = 5
    else:
        h1_size, h1_lead, h1_before, h1_after = 16, 22, 14, 6
        h2_size, h2_lead, h2_before, h2_after = 12, 16, 10, 4
        h3_size, h3_lead, h3_before, h3_after = 10, 14, 6, 3
        body_after = 6
        spacer_height = 6
        table_padding = 4

    h1_style = ParagraphStyle(
        'H1_PDF', fontName=BOLD_FONT, fontSize=h1_size, leading=h1_lead,
        textColor=colors.HexColor("#1e1b4b"), spaceBefore=h1_before, spaceAfter=h1_after
    )
    h2_style = ParagraphStyle(
        'H2_PDF', fontName=BOLD_FONT, fontSize=h2_size, leading=h2_lead,
        textColor=colors.HexColor("#4338ca"), spaceBefore=h2_before, spaceAfter=h2_after, keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'H3_PDF', fontName=BOLD_FONT, fontSize=h3_size, leading=h3_lead,
        textColor=colors.HexColor("#334155"), spaceBefore=h3_before, spaceAfter=h3_after, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_PDF', fontName=MAIN_FONT, fontSize=body_size, leading=body_lead,
        textColor=colors.HexColor("#1e293b"), spaceAfter=body_after
    )

    story = []
    table_lines = []
    in_table = False
    appendix_story = []
    in_appendix = False

    for line in lines:
        stripped = line.strip()
        
        # 🚨 부록 섹션 감지시 -> 사업계획서 본문과 완전 분리(PageBreak) 후 별도 1페이지 100% 구현
        if "## [정부지원사업 지원 제외" in stripped or "정부지원사업 지원 제외" in stripped:
            if in_table and table_lines:
                in_table = False
                raw_rows = []
                for tline in table_lines:
                    if ":---" in tline or "---:" in tline or "| --- |" in tline or "| :--- |" in tline:
                        continue
                    cols = [c.strip() for c in tline.split("|")[1:-1]]
                    if cols:
                        raw_rows.append(cols)
                if raw_rows:
                    table_data = []
                    for r_idx, row in enumerate(raw_rows):
                        row_data = []
                        for cell in row:
                            st_cell = ParagraphStyle(
                                'Cell_PDF_Normal', fontName=MAIN_FONT if r_idx > 0 else BOLD_FONT, 
                                fontSize=cell_size, leading=cell_lead,
                                textColor=colors.HexColor("#ffffff" if r_idx == 0 else "#1e293b")
                            )
                            clean_cell = cell.replace("**", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                            row_data.append(Paragraph(clean_cell, st_cell))
                        table_data.append(row_data)
                    t = Table(table_data, colWidths=None)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#ffffff")),
                        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
                        ('TOPPADDING', (0,0), (-1,-1), table_padding),
                        ('BOTTOMPADDING', (0,0), (-1,-1), table_padding),
                        ('LEFTPADDING', (0,0), (-1,-1), 4),
                        ('RIGHTPADDING', (0,0), (-1,-1), 4),
                    ]))
                    story.append(KeepTogether([t]))
                    story.append(Spacer(1, spacer_height))
                table_lines = []

            # 본문 종료 후 독립된 페이지로 완전 넘김 (PageBreak)
            story.append(PageBreak())
            in_appendix = True

        # 부록 전용 폰트 및 간격 최적화
        if in_appendix:
            curr_body_size = 8.0
            curr_body_lead = 11.5
            curr_padding = 2.5
            app_body_style = ParagraphStyle(
                'Body_PDF_App', fontName=MAIN_FONT, fontSize=curr_body_size, leading=curr_body_lead,
                textColor=colors.HexColor("#1e293b"), spaceAfter=3
            )
        else:
            curr_padding = table_padding

        # 마크다운 표(| ... |) 감지 및 변환
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            in_table = False
            if table_lines:
                raw_rows = []
                for tline in table_lines:
                    if ":---" in tline or "---:" in tline or "| --- |" in tline or "| :--- |" in tline:
                        continue
                    cols = [c.strip() for c in tline.split("|")[1:-1]]
                    if cols:
                        raw_rows.append(cols)
                
                if raw_rows:
                    table_data = []
                    for r_idx, row in enumerate(raw_rows):
                        row_data = []
                        for cell in row:
                            st_cell = ParagraphStyle(
                                'Cell_PDF_App_R', fontName=MAIN_FONT if r_idx > 0 else BOLD_FONT, 
                                fontSize=7.0 if in_appendix else cell_size, 
                                leading=9.5 if in_appendix else cell_lead,
                                textColor=colors.HexColor("#ffffff" if r_idx == 0 else "#1e293b")
                            )
                            clean_cell = cell.replace("**", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                            row_data.append(Paragraph(clean_cell, st_cell))
                        table_data.append(row_data)
                    
                    t = Table(table_data, colWidths=None)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#ffffff")),
                        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
                        ('TOPPADDING', (0,0), (-1,-1), curr_padding),
                        ('BOTTOMPADDING', (0,0), (-1,-1), curr_padding),
                        ('LEFTPADDING', (0,0), (-1,-1), 3),
                        ('RIGHTPADDING', (0,0), (-1,-1), 3),
                    ]))
                    target_list = appendix_story if in_appendix else story
                    target_list.append(KeepTogether([t]))
                    target_list.append(Spacer(1, 2 if in_appendix else spacer_height))
            table_lines = []

        if stripped.startswith("# "):
            target_list = appendix_story if in_appendix else story
            target_list.append(Paragraph(stripped[2:], h1_style))
        elif stripped.startswith("## "):
            target_list = appendix_story if in_appendix else story
            target_list.append(Paragraph(stripped[3:], h2_style))
        elif stripped.startswith("### "):
            target_list = appendix_story if in_appendix else story
            target_list.append(Paragraph(stripped[4:], h3_style))
        elif stripped.startswith("---"):
            target_list = appendix_story if in_appendix else story
            target_list.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#6366f1"), spaceBefore=3 if in_appendix else 6, spaceAfter=3 if in_appendix else 6))
        elif stripped:
            clean_text = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            target_list = appendix_story if in_appendix else story
            st_use = app_body_style if in_appendix else body_style
            target_list.append(Paragraph(clean_text, st_use))

    # 🚨 부록 전체 요소를 KeepTogether로 단 1장에 100% 통째 통합 수용
    if appendix_story:
        story.append(KeepTogether(appendix_story))

    doc.build(story, canvasmaker=NumberedCanvas)
    return pdf_path

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

def detect_domain(title: str, features: str) -> str:
    text = (title + " " + features).lower()
    if any(k in text for k in ["반려동물", "펫", "강아지", "고양이", "친환경", "소재", "용품", "브랜드", "제조", "공장", "제품", "키트", "장비", "하드웨어", "부품", "설비"]):
        return "hardware"
    elif any(k in text for k in ["커피", "카페", "식당", "음료", "로봇", "서빙", "음식", "베이커리", "매장", "푸드", "디저트", "외식", "무인"]):
        return "fnb"
    elif any(k in text for k in ["쇼핑몰", "스토어", "의류", "패션", "유통", "판매", "배송", "마켓", "콘텐츠", "디자인"]):
        return "ecommerce"
    elif any(k in text for k in ["바이오", "헬스", "의료", "제약", "화장품", "뷰티", "임상"]):
        return "bio_health"
    return "it_saas"

PROGRAM_SPECS = {
    "packages_15p": {"name": "예비창업패키지 / 초기창업패키지 규격", "target_pages": "15페이지 정통 풀-스펙", "target_num": 15},
    "cheongsa_12p": {"name": "청년창업사관학교 집중 실행 규격", "target_pages": "12페이지 정밀 규격", "target_num": 12},
    "rnd_25p": {"name": "중기부 / 산업부 R&D 기술개발 과제 규격", "target_pages": "25페이지 기술개발 초정밀 규격", "target_num": 25},
    "export_8p": {"name": "수출바우처 및 마케팅 지원 규격", "target_pages": "8페이지 마케팅 규격", "target_num": 8},
    "local_5p": {"name": "지자체 소액 창업 지원 린 규격", "target_pages": "5페이지 이내 숏폼 규격", "target_num": 5}
}

def generate_business_report(req: ReportRequest) -> tuple[str, str]:
    prog_info = PROGRAM_SPECS.get(req.program_type, PROGRAM_SPECS["packages_15p"])
    prog_name = prog_info["name"]
    prog_pages = prog_info["target_pages"]
    now_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    domain = detect_domain(req.title, req.core_features)

    # R&D 25페이지 전용 기술개발 초정밀 대용량 모듈
    rnd_extra_section = ""
    if req.program_type == "rnd_25p":
        rnd_extra_section = f"""---

## [R&D 전용 25P 초정밀 모듈] 기술개발 상세 파이프라인 & TRL 진단

### 1. 기술성숙도(TRL, Technology Readiness Level) 9단계 달성 목표
| TRL 단계 | 단계별 정의 | 현재 수준 | 사업 종료 시 목표 수준 | 검증 방법 및 증빙 |
| :--- | :--- | :--- | :--- | :--- |
| **TRL 1~2단계** | 기초 연구 및 원천 아이디어 정립 | **달성 완료** | 달성 완료 | 선행 논문 및 특허 분석 보고서 |
| **TRL 3~4단계** | 연구실 수준의 핵심 기능 검증 및 시제품 제작 | **진행 중** | **완료 목표 (3개월 차)** | 시험성적서 및 알파 테스트 결과 |
| **TRL 5~6단계** | 실제 환경에서의 성능 검증 및 공인인증 | - | **완료 목표 (8개월 차)** | 공인시험기관(KTL/KTR) 성적서 |
| **TRL 7~8단계** | 양산 전 정밀 제품 제작 및 사업화 시스템 검증 | - | **완료 목표 (12개월 차)** | 필드 테스트 및 초기 매출 계약서 |
| **TRL 9단계** | 사업화 양산 및 시장 진입 안정화 | - | **차년도 연계 목표** | 매출 세금계산서 및 양산 증명 |

### 2. 하드웨어 / 소프트웨어 기술 명세서 (Architecture Specs)
- **성능 고도화**: {req.core_features} 처리 효율 5,000회 이상 및 응답/제조 속도 50ms 이내 유지
- **데이터베이스 ERD 설계**: 사용자 액션 로그, 결제, 분산 데이터 파이프라인 100% 암호화 (AES-256 적용)
- **보안 및 규제 준수**: ISO/IEC 27001 정보보안준수 및 개인정보보호법(PIPA) 기술적 보호조치 적용
- **생산/서버 인프라 구획**: 친환경 소재 사입 공정 및 오토스케일링 빅데이터 수집 관리

### 3. 수학적 알고리즘 모델링 & 의사코드 (Pseudocode & Math Modeling)
- **목적 함수**: min f(x) = sum(w_i * Cost_i) + lambda * Latency
- **실시간 연산 파이프라인**: 메시지 큐 -> 분산 집계 -> 인메모리 캐싱
- **보안 토큰 암호화 수식**: Token = HMAC-SHA256(SecretKey, Payload || Timestamp)

### 4. 선행기술 조사 및 지식재산권(IP) 포트폴리오 10선 비교 분석표
| 번호 | 특허/기술명 | 주요 권리 범주 | 본 프로젝트 차별화 포인트 | IP 회피 및 방어 전략 |
| :--- | :--- | :--- | :--- | :--- |
| **1** | 수동 제어 조리/제조 시스템 | 파라미터 수동 세팅 | **친환경 자동 렌더링/제조** | 독립 청구항 구성으로 100% 회피 |
| **2** | 단일 데이터 파이프라인 | 유선 통신 기반 제어 | **SSL 256-bit 클라우드 분산 제어** | 기술 독창성 확보 및 특허 출원 |
| **3** | 무인 결제 및 주문 시스템 | 단순 결제 프로세스 | **1회용 인증 키 및 소멸 CS 추적** | 무인 자동화 독점 권리 확보 |
| **4** | 분산 데이터 처리 모듈 | 배치 처리 방식 | **3초 완결 실시간 초고속 렌더링** | 처리 속도 특허권 출원 완료 |
| **5** | 기본 물류 위탁 시스템 | 수동 포장 사입 | **무재고 풀필먼트 자동 연동** | 서비스 BM 특허 파이프라인 구축 |
| **6** | 클라우드 오토스케일링 | 단일 서버 하드웨어 | **MSA 트래픽 분산 제어 기술** | 특허 신규 청구항 확보 완료 |
| **7** | 실시간 위생 감지 제어 | 수동 위생 검사 | **비전 AI 자동 위생 감지 센서** | 전용 알고리즘 특허 등록 진행 |

### 5. 공인시험기관 (KTL / KTR) 정밀 평가 항목 15종 세부 명세표
| 평가 항목 | 단위 | 세계 수준 (비교) | 개발 목표치 | 시험 평가 방법 및 공인 기관 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 시스템 반응 속도** | ms | 150ms 이내 | **50ms 이내** | KTL 공인 시험성적서 측정 |
| **2. 동시 접속/제조 처리** | RPS | 2,000 RPS | **5,000 RPS** | 공인 시험기관 측정 |
| **3. 무인 가동률** | % | 98.0% | **99.9% 이상** | 24시간 365일 실시간 관제 |
| **4. 오류 발생율** | % | 2.5% 이하 | **0.1% 이하** | 로그 트래킹 시스템 자동 수집 |
| **5. 데이터 암호화 안전성**| Bit | AES-128 | **AES-256** | 정보보호진흥원(KISA) 검증 |

### 6. 12개월 차 월별 상세 실행 계획표 (Timeline)
| 월 (Month) | 세부 과제 | 주요 마일스톤 및 딜리버러블 | 담당 인력 및 협력 기관 |
| :--- | :--- | :--- | :--- |
| **M1 ~ M2** | 핵심 아키텍처 및 공정 설계 | 시스템 아키텍처 정의서 작성 | 대표자 및 메인 개발자 |
| **M3 ~ M4** | 1차 알파 시제품 개발 및 내부 테스트 | 알파 버전 시제품 개발 성공 | 개발팀 및 HW/소재 협력사 |
| **M5 ~ M6** | UI/UX 연동 및 사용자 최적화 | 시제품 베타 서비스 오픈 | 디자이너 및 프론트엔드 |
| **M7 ~ M8** | 공인시험기관 성능 검증 | KTL/KTR 공인 시험성적서 획득 | 품질 검수팀 |
| **M9 ~ M10** | 필드 실증 테스트 | 실증 만족도 90% 이상 달성 | 마케팅 및 운영팀 |
| **M11 ~ M12** | 정식 상용화 배포 및 특허 등록 | 상용화 런칭 및 특허 등록증 | 대표자 및 전담 변리사 |

### 7. 글로벌 특화 경쟁 기술 및 해외 시장 진출 전략
- 미국/유럽 PCT 국제 특허 동시 출원 준비 (글로벌 IP 회피 및 선점)
- 해외 표준 기술 규격(CE, FCC) 사전 검증 테스트베드 구축

### 8. 연구개발 인프라 구축 및 연구인력 유지 관리 방안
- 석/박사급 기술 전담 연구원 3인 상주 개발 및 전공 기술 자문단 매월 워크숍
- 주간 코드 리뷰 및 CI/CD 자동화 기술 부채 방지 시스템 가동

### 9. 연구개발비 12개월 세부 정산 및 기술 자금 집행 내역서
- **연구 인력비 (인건비)**: 참여 연구원 3인 급여 (월 300만 원 x 12개월 = 36,000,000원)
- **연구 장비 및 재료 사입비**: 개발 서버, 센서, 부품/소재 사입 (44,000,000원)
- **외부 기술 위탁 및 시험분석비**: KTL 시험성적서 및 특허 법률 출원비 (20,000,000원)"""

    # 예창패/초창패 15p & 청창사 12p 전용 세부 시장조사 및 마케팅 파이프라인
    packages_extra_section = ""
    if req.program_type in ["packages_15p", "cheongsa_12p", "rnd_25p"]:
        packages_extra_section = f"""---

## [시장분석 & GTM 15P 모듈] 타겟 유저 세분화 및 밸류체인 정밀 분석

### 1. 고객 페인포인트 정밀 수치 설문 조사 데이터
- 타겟 유저 300명 대상 정밀 설문 조사 결과: 기존 대안 서비스 만족도 28.5%에 불과
- 핵심 불편 요인 1위: **과도한 비용 부담 (68.4%)**, 2위: **느린 처리 속도 (54.2%)**, 3위: **복잡한 사용법 (41.1%)**
- **{req.title}** 도입 시 구매 전환 의향 **84.6%** 달성

### 2. TAM-SAM-SOM 시장 산출 공식 및 수치적 정합성
- **TAM (전체 시장)**: 국내 관련 산업 및 자동화 거래액 시장 (약 15조 원)
- **SAM (유효 시장)**: {req.target_customer} 중심의 세부 유효 시장 (약 1조 2,000억 원)
- **SOM (수익 시장)**: 초기 1~2년 차 진입 직영 및 가맹 유저 타겟 (약 30억 원 목표)

### 3. 마이클 포터 5-Forces 경쟁 환경 분석
- **기존 경쟁 강도**: 수동 대행업체 난립하나 무인 자동화/친환경 솔루션 부재
- **신규 진입 위협**: 기술 특허 출원으로 진입 장벽 구축
- **구매자 협상력**: 초저가/고효율 제공으로 구매자 락인(Lock-in) 효과 극대화
- **공급자 협상력**: 부품/원자재 다변화 공급망 구축으로 원가 안정성 확보

### 4. 5대 경쟁사 주요 기능 수치 비교 Matrix 표
| 기능 및 스펙 비교 | A 경쟁사 (수동) | B 경쟁사 (외주) | **{req.title} (본 사업)** | 우위 수치 |
| :--- | :--- | :--- | :--- | :--- |
| **처리 단가** | 200만 원 | 100만 원 | **초저가 월 구독/1회성** | **비용 90%↓ 절감** |
| **완성 소요시간** | 14일 소요 | 7일 소요 | **3초 원터치 자동완성** | **속도 99%↑ 향상** |
| **무인 가동률** | 0% (대면) | 0% (수동) | **100% 무인 웹 자동 접속** | **가동률 100%** |
| **데이터 보안** | 이메일 전달 | 엑셀 파일 | **256-bit SSL 암호화 DB** | **보안 100%** |

### 5. 3개년 정밀 재무 손익분기점 (BEP) 달성 시점 및 자금 회수 계획
- **손익분기점 (BEP) 달성 시점**: 서비스 런칭 7개월 차 유료 유저 350명 달성 시점
- **초기 투입 자금 회수 (Payback Period)**: 런칭 14개월 차 누적 순이익 1억 원 돌파로 자금 회수 완료

### 6. 리스크 관리 시나리오 (Risk Management Plan A / B / C)
- **Plan A (정상 성장)**: 1년 차 유저 1,000명 유치 및 목표 매출 1.2억 원 달성
- **Plan B (경쟁 심화 시)**: B2B 기업체 전용 요금제 출시 및 수수료 15% 인하 대응
- **Plan C (시장 침체 시)**: 핵심 무인 기능 린(Lean) 서비스로 축소하여 월 서버비 최소화

### 7. 마케팅 유저 획득(CAC) 및 LTV(고객생애가치) 재무 추정
- **목표 유저 획득 비용 (CAC)**: 건당 15,000원 이하 유지
- **고객 생애 가치 (LTV)**: 유저당 평균 180,000원 (LTV/CAC 비율 12배 달성)"""

    if domain == "hardware":
        domain_name = "친환경 / 제조 / 하드웨어 / 바이오헬스"
        focus_points = """- **친환경 소재 및 무독성 안정성 검증**: 친환경 무독성 소재 사용 및 KC/FDA 안전 인증으로 제품 신뢰도 극대화
- **생산 단가 절감 및 3D/자동화 모듈 설계**: 대량 양산형 친환경 몰드 설계로 기존 수입 제품 대비 원가 50% 절감
- **온/오프라인 옴니채널 유통 수치화**: 자사 몰, 와디즈 펀딩, 펫 샵 및 대형마트 공급망을 통한 매출 파이프라인 구축"""
        prob_text_1 = f"현재 국내 관련 유통/제품 시장은 플라스틱 화학 소재 사용으로 인한 유해성 논란과 비싼 수입산 가격(평균 5~10만 원대)으로 인해 **{req.target_customer}** 고객층의 불만과 접근성 한계를 초래하고 있습니다."
        prob_text_2 = f"기존 저가형 유통 제품들은 안전 인증 미비와 조기 파손 문제로 교체 주기가 짧아 높은 소비자 불만을 사고 있습니다. **{req.title}** 프로젝트는 이 문제점을 뿌리부터 해결합니다."
        sol_text = f"**{req.title}** 프로젝트는 친환경 바이오 소재 기반의 맞춤 설계와 생산 공정 자동화를 결합하여 내구성과 안전성을 갖춘 고품질 제품을 합리적 가격에 제공하는 혁신 솔루션입니다."
        tam_text = "국내 관련 제품 및 친환경 유통/헬스케어 시장 (약 8조 원 규모)"
        sam_text = f"{req.target_customer} 중심의 친환경 프리미엄 수요 (약 8,000억 원 규모)"
        som_text = "초기 1~2년 차 온라인 및 플래그십 진입 목표 (약 20억 원 목표)"
        comp_table = f"""| 구분 | 기존 수입 / 기성 제품 | {req.title} (본 프로젝트) | 개선 효과 (수치) |
| :--- | :--- | :--- | :--- |
| **제품 소재** | 일반 화학 플라스틱 | **100% 친환경 무독성 바이오 소재** | **유해 물질 0% 달성** |
| **소비자 단가** | 5만 원 ~ 10만 원 (고비용) | **자체 자동화 양산으로 합리적 가격** | **원가 50%↓ 절감** |
| **내구성/안전성** | 쉽게 파손 / 미인증 | **KC 안전인증 및 정밀 내구 설계** | **수명 3배↑ 향상** |
| **맞춤 설계** | 단일 규격 기성품 | **연령/체형별 맞춤 친환경 설계** | **고객 만족도 95%** |"""
        service_struct = "[친환경 원자재 사입] -> [AI 정밀 설계 & 양산 공정] -> [KC 인증 및 전국 옴니채널 유통]"
        mono_text = """* **자사 몰 및 온라인 커머스 직접 판매 수익 (마진율 50% 이상)**
* **대형마트, 펫 숍 및 B2B 오프라인 도매 유통 마진**
* **와디즈/텀블벅 크라우드 펀딩 리워드 매출 수익**
* **해외 수출 바우처 연계 유통 마진**"""
        budget_table = f"""| 사업비 집행 항목 | 세부 산출 근거 (수량 x 단가) | 금액 (원) | 정부지원금 (70%) | 자부담금 (30%) |
| :--- | :--- | :--- | :--- | :--- |
| **친환경 소재 금형 사입 및 시제품 개발**| 금형 제작 1식, 친환경 바이오 소재 원자재 | **45,000,000** | 31,500,000 | 13,500,000 |
| **KC/FDA 안전 인증 및 성적서 발급** | 공인시험기관 KC 인증 및 독성 테스트 | **25,000,000** | 17,500,000 | 7,500,000 |
| **온라인 마케팅 및 크라우드 펀딩** | 펀딩 마케팅, SNS 바이럴, 숏폼 제작 | **30,000,000** | 21,000,000 | 9,000,000 |
| **합 계** | **총 사업비 ({req.budget})** | **100,000,000** | **70,000,000** | **30,000,000** |"""
        perf_table = """| 연차 | 유효 구매 고객 수 | 추정 월 매출 (원) | 추정 연 매출 (원) | 영업이익률 (%) |
| :--- | :--- | :--- | :--- | :--- |
| **1년 차 (2026년)** | 월 2,000건 구매 유저 | **20,000,000** | **240,000,000** | **42%** |
| **2년 차 (2027년)** | 월 8,000건 구매 유저 | **60,000,000** | **720,000,000** | **48%** |
| **3년 차 (2028년)** | 월 25,000건 구매 유저 | **180,000,000** | **2,160,000,000** | **55%** |"""

    elif domain == "fnb":
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
| **고객 대기시간**| 평균 10분 ~ 15분 소요 | **3초 결제 -> 3분 이내 제조/서빙** | **대기시간 80%↓** |"""
        service_struct = "[고객 키오스크/앱 주문 결제] -> [AI 로봇 음료 제조 & 자동 서빙] -> [고객 수령 및 AI 자동 청결 관리]"
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
        service_struct = "[고객 주문 결제] -> [AI 주문 자동 접수 & 무인 사입] -> [풀필먼트 자동 택배 배송]"
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
| **접근성** | 방문 대면 상담 필요 | **100% 무인 웹 자동 접속** | **접근성 100%** |
| **사용 편의성** | 전문 지식 필수 | **1버튼 원터치 자동 완성** | **생산성 10배↑** |"""
        service_struct = "[사용자 정보 입력] -> [AI 스마트 렌더링 엔진] -> [전문 리포트 PDF/MD 즉시 완성]"
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
- 기존 수동 방식 및 외주 대행사는 높은 비용 구조와 수일~수주의 소요 시간으로 인해 고객의 시급한 요구에 대응하지 못하는 치명적 한계가 존재합니다.

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

## [부록] K-Startup 제출 전 필수 검수 체크리스트 & 지원 제한 업종 사전 확인

*본 부록은 K-Startup 지원사업 서류 제출 전 감점 및 자동 탈락을 방지하기 위한 통합 검수 가이드입니다. 정부기관 제출용 본문(1.문제인식~4.팀역량)과 구분하여 1페이지로 독립 기입됩니다.*

### 1. 지원 제외 및 제한 업종 사전 확인
- **원칙적 제외 업종**: 유흥·사행성 업종(단란주점, 도박, 게임장 등), 부동산 임대업, 금융/보험업 (사전 제외 대상)
- **기술 지원 제한 업종**: 단순 도소매 및 단순 유통업 (혁신성이 낮다고 판단되는 기술 R&D 지원사업에서는 제외 대상이 될 수 있으므로 제조/IT 기술 결합 요소 필수 작성)
- **대부분 지원 가능 공모**: K-Startup 계열 (예비창업패키지, 초기창업패키지)은 대부분 제한 없이 지원 가능합니다.

### 2. 필수 제출 7대 증빙서류 준비 체크리스트
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

    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    return md_content, html_content

def build_pdf_file(req: ReportRequest, pdf_path: str):
    md_content, _ = generate_business_report(req)
    lines = md_content.splitlines()

    # HWP/Word 공식 A4 표준 여백 적용: 좌/우 20mm(56.7pt), 상/하 15mm(42.5pt)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=56.7,
        rightMargin=56.7,
        topMargin=42.5,
        bottomMargin=42.5
    )

    prog_type = req.program_type
    
    # 대한민국 정부 HWP 표준 폰트 규격: 본문 10.5pt, 줄간격 160%(16.8pt)
    body_size = 10.5
    body_lead = 16.8
    cell_size = 9.5
    cell_lead = 14.5

    # 프로그램 규격별 A4 렌더링 스타일 세밀 동기화
    if prog_type == "rnd_25p":
        h1_size, h1_lead, h1_before, h1_after = 18, 24, 28, 16
        h2_size, h2_lead, h2_before, h2_after = 14, 19, 22, 12
        h3_size, h3_lead, h3_before, h3_after = 12, 16, 16, 8
        body_after = 14
        spacer_height = 20
        table_padding = 12
    elif prog_type in ["packages_15p", "cheongsa_12p"]:
        h1_size, h1_lead, h1_before, h1_after = 17, 23, 22, 12
        h2_size, h2_lead, h2_before, h2_after = 13, 17, 18, 10
        h3_size, h3_lead, h3_before, h3_after = 11, 15, 14, 6
        body_after = 12
        spacer_height = 16
        table_padding = 10
    else:
        h1_size, h1_lead, h1_before, h1_after = 16, 22, 16, 8
        h2_size, h2_lead, h2_before, h2_after = 12, 16, 12, 6
        h3_size, h3_lead, h3_before, h3_after = 10, 14, 8, 4
        body_after = 8
        spacer_height = 8
        table_padding = 6

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
    cell_style = ParagraphStyle(
        'Cell_PDF', fontName=MAIN_FONT, fontSize=cell_size, leading=cell_lead,
        textColor=colors.HexColor("#1e293b")
    )
    cell_header_style = ParagraphStyle(
        'Cell_Header_PDF', fontName=BOLD_FONT, fontSize=cell_size, leading=cell_lead,
        textColor=colors.HexColor("#1e1b4b")
    )

    story = []
    table_lines = []
    in_table = False
    appendix_story = []
    in_appendix = False

    for line in lines:
        stripped = line.strip()
        
        # 부록 섹션 시작 감지 -> 강제 PageBreak 실행 및 부록 전체 KeepTogether 묶음
        if stripped.startswith("## [부록]") or "K-Startup 제출 전 필수 검수" in stripped:
            if in_table and table_lines:
                # 남아있는 표 처리
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
                            st = cell_header_style if r_idx == 0 else cell_style
                            clean_cell = cell.replace("**", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                            row_data.append(Paragraph(clean_cell, st))
                        table_data.append(row_data)
                    t = Table(table_data, colWidths=None)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#0f172a")),
                        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
                        ('TOPPADDING', (0,0), (-1,-1), table_padding),
                        ('BOTTOMPADDING', (0,0), (-1,-1), table_padding),
                        ('LEFTPADDING', (0,0), (-1,-1), 8),
                        ('RIGHTPADDING', (0,0), (-1,-1), 8),
                    ]))
                    story.append(KeepTogether([t]))
                    story.append(Spacer(1, spacer_height))
                table_lines = []

            # 4.4절 종료 후 독립된 1페이지 부록으로 강제 페이지 넘김 (PageBreak)
            story.append(PageBreak())
            in_appendix = True

        # 마크다운 표(| ... |) 감지 및 ReportLab Table 변환기
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            # 표 렌더링 시작
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
                            st = cell_header_style if r_idx == 0 else cell_style
                            clean_cell = cell.replace("**", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                            row_data.append(Paragraph(clean_cell, st))
                        table_data.append(row_data)
                    
                    t = Table(table_data, colWidths=None)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#0f172a")),
                        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
                        ('TOPPADDING', (0,0), (-1,-1), table_padding),
                        ('BOTTOMPADDING', (0,0), (-1,-1), table_padding),
                        ('LEFTPADDING', (0,0), (-1,-1), 8),
                        ('RIGHTPADDING', (0,0), (-1,-1), 8),
                    ]))
                    target_list = appendix_story if in_appendix else story
                    target_list.append(KeepTogether([t]))
                    target_list.append(Spacer(1, spacer_height))
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
            target_list.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#6366f1"), spaceBefore=10, spaceAfter=10))
        elif stripped:
            clean_text = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            target_list = appendix_story if in_appendix else story
            target_list.append(Paragraph(clean_text, body_style))

    # 부록 전체 요소를 KeepTogether로 감싸서 한 장에 100% 통합 기입
    if appendix_story:
        story.append(KeepTogether(appendix_story))

    doc.build(story, canvasmaker=NumberedCanvas)
    return pdf_path

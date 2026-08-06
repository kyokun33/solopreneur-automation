import sys
import os

BASE_DIR = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "report_generator"))

from report_generator.schemas import ReportRequest
from report_generator.generator import generate_business_report, detect_domain

test_cases = [
    ("반려동물 맞춤형 펫푸드 정기구독 서비스", "펫푸드 영양제 사료", "pet_care"),
    ("디지털 바이오 의료기기 및 줄기세포 치료제", "임상 식약처 진단", "bio_health"),
    ("24시간 무인 로봇 카페 푸드테크 솔루션", "음료 로봇 서빙 스마트 매장", "fnb_foodtech"),
    ("친환경 바이오 소재 탄소 저감 포장재", "ESG 생분해 탄소 배출 절감", "eco_esg"),
    ("스마트 공장 3D 정밀 금형 제조 로봇팔", "양산 불량률 국산화 부품", "smart_hardware"),
    ("AI 무재고 위탁 이커머스 풀필먼트 플랫폼", "스마트스토어 배송 유통", "ecommerce_logistics"),
    ("글로벌 킬러 캐릭터 IP 및 에듀테크 콘텐츠", "웹툰 게임 애니메이션 OSMU", "contents_ip"),
    ("AI 프롭테크 부동산 거래 결제 핀테크", "금융 결제 중개 수수료", "fintech_proptech"),
    ("로컬 특산물 연계 라이프스타일 팝업 공간", "로컬크리에이터 브랜딩 기획", "local_lifestyle"),
    ("AI 기반 SaaS 자동화 사업계획서 렌더링", "소프트웨어 LLM 클라우드", "it_ai_saas")
]

print("=== [대한민국 K-Startup 10대 정통 업종 감지 및 정합성 테스트] ===")
success_count = 0

for title, features, expected in test_cases:
    detected = detect_domain(title, features)
    req = ReportRequest(
        title=title,
        category="government",
        program_type="packages_15p",
        target_customer="타겟 고객층",
        core_features=features,
        budget="초기 예산 5,000만 원 / 월 목표 매출 500만 원",
        access_key="KM849201"
    )
    md_text, _ = generate_business_report(req)
    match = (detected == expected)
    if match:
        success_count += 1
    print(f"[{'SUCCESS' if match else 'FAIL'}] 아이템: {title} | 감지된 코드: {detected} | 기대 코드: {expected}")

print(f"\n최종 결과: 총 {len(test_cases)}개 중 {success_count}개 100% 감지 성공 ({success_count/len(test_cases)*100:.0f}%)")

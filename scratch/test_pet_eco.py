import sys
import os
import pypdf

BASE_DIR = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "report_generator"))

from report_generator.schemas import ReportRequest
from report_generator.generator import generate_business_report, build_pdf_file

req = ReportRequest(
    title="친환경 소재 기반 반려동물용품 브랜드",
    category="government",
    program_type="packages_15p",
    target_customer="20~40대 반려동물(강아지/고양이) 양육 1~2인 가구, 프리미엄·건강 지향 소비자",
    core_features="기존 제품 대비 친환경 소재·안전 인증을 강화하고, 반려동물 체형/연령별 맞춤 설계로 차별화",
    budget="초기 예산 5,000만 원 / 월 목표 매출 500만 원",
    access_key="KM849201"
)

md_text, html_text = generate_business_report(req)
pdf_path = os.path.join(BASE_DIR, "scratch", "pet_eco_test.pdf")
build_pdf_file(req, pdf_path)

reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)

print("=== [반려동물/친환경 용품 테스트 결과] ===")
print("PDF 총 페이지 수:", page_count, "페이지")
print("감지된 업종 관련 키워드 포함 여부 (친환경/제조/KC인증):", "친환경 소재" in md_text and "KC" in md_text)
print("부록 텍스트 통합 여부 ([부록] K-Startup 제출 전 필수 검수):", "[부록] K-Startup 제출 전 필수 검수" in md_text)

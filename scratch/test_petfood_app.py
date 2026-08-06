import sys
import os
import pypdf

BASE_DIR = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "report_generator"))

from report_generator.schemas import ReportRequest
from report_generator.generator import generate_business_report, build_pdf_file

req = ReportRequest(
    title="반려동물 맞춤형 펫푸드 정기구독 서비스",
    category="government",
    program_type="packages_15p",
    target_customer="반려견·반려묘를 양육하는 20~40대 1~2인 가구, 건강·편의성을 중시하는 초보~중급 양육자",
    core_features="반려동물의 견종/묘종·연령·건강상태 기반 맞춤 급여 설계 및 정기배송, 수의사 자문 레시피로 신뢰도 확보",
    budget="초기 예산 5,000만 원 / 월 목표 매출 500만 원",
    access_key="KM849201"
)

md_text, html_text = generate_business_report(req)
pdf_path = os.path.join(BASE_DIR, "scratch", "petfood_test.pdf")
build_pdf_file(req, pdf_path)

reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)

print("=== [펫푸드 정기구독 서비스 테스트 결과] ===")
print("PDF 총 페이지 수:", page_count, "페이지")
print("감지된 업종 명칭 검증:", "펫푸드 · 바이오헬스 · 식품제조 · 정기구독" in md_text)
print("부록 1페이지 완벽 통합 여부 ([부록] 제출 전 필수 체크리스트):", "[부록] 제출 전 필수 체크리스트" in md_text)

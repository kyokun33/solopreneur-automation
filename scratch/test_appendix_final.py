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
    target_customer="반려견·반려묘를 양육하는 20~40대 1~2인 가구",
    core_features="맞춤 급여 설계 및 정기배송, 수의사 자문 레시피",
    budget="초기 예산 5,000만 원 / 월 목표 매출 500만 원",
    access_key="KM849201"
)

md_text, html_text = generate_business_report(req)
pdf_path = os.path.join(BASE_DIR, "scratch", "appendix_final_test.pdf")
build_pdf_file(req, pdf_path)

reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)

print("=== [부록 독립 1페이지 검증 결과] ===")
print("PDF 총 페이지 수:", page_count, "페이지")

page_6_text = reader.pages[5].extract_text()
page_7_text = reader.pages[6].extract_text() if page_count >= 7 else ""

print("6페이지에 [부록] 문구 포함 여부 (포함 안 되어야 성공):", "[부록]" in page_6_text)
print("7페이지에 [부록] 문구 시작 여부 (독립 페이지 시작):", "[부록]" in page_7_text)
print("7페이지에서 7대 증빙서류 표가 완결되었는지 여부:", "사업계획서 원본" in page_7_text)

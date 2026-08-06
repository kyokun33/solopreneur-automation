import sys
import os
import pypdf

BASE_DIR = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "report_generator"))

from report_generator.schemas import ReportRequest
from report_generator.generator import generate_business_report, build_pdf_file

req = ReportRequest(
    title="24시간 AI 무인 로봇 스마트 매장",
    category="government",
    program_type="packages_15p",
    target_customer="2040 직장인, 소상공인 창업가 타겟",
    core_features="24시간 AI 무인 로봇 스마트 매장 시스템 솔루션",
    budget="초기 예산 1,000만 원 / 월 목표 매출 500만 원",
    access_key="KM849201"
)

md_text, html_text = generate_business_report(req)
pdf_path = os.path.join(BASE_DIR, "scratch", "no_backticks_test.pdf")
build_pdf_file(req, pdf_path)

reader = pypdf.PdfReader(pdf_path)
full_text = "".join([page.extract_text() for page in reader.pages])

print("=== [백틱(```) 기호 전면 제거 검증 결과] ===")
print("마크다운 텍스트에 백틱(```) 포함 여부 (포함 안 되어야 성공):", "```" in md_text)
print("PDF 전체 텍스트에 백틱(```) 포함 여부 (포함 안 되어야 성공):", "```" in full_text)

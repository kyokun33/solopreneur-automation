import sys
import os
import pypdf

BASE_DIR = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "report_generator"))

from report_generator.schemas import ReportRequest
from report_generator.generator import generate_business_report, build_pdf_file

req = ReportRequest(
    title="ai 스마트 무인 스토어",
    category="government",
    program_type="packages_15p",
    target_customer="전 연령",
    core_features="무인 AI 자동화",
    budget="초기 예산 1,000만 원 / 월 목표 매출 500만 원",
    access_key="KM849201"
)

md_text, html_text = generate_business_report(req)
pdf_path = os.path.join(BASE_DIR, "scratch", "sample_style_test.pdf")
build_pdf_file(req, pdf_path)

reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)

print("=== [샘플 PDF 100% 서식 매칭 테스트 결과] ===")
print("PDF 총 페이지 수:", page_count, "페이지")

last_page_text = reader.pages[-1].extract_text()
prev_page_text = reader.pages[-2].extract_text()

print("이전 페이지 본문 완결 여부 (이전 페이지에 부록 없어야 함):", "정부지원사업 지원 제외" not in prev_page_text)
print("마지막 페이지에 100% 샘플 PDF 내용 수용 여부:", "정부지원사업 지원 제외" in last_page_text and "사업계획서 원본" in last_page_text)

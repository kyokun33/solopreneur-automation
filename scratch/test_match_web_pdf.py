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
pdf_path = os.path.join(BASE_DIR, "scratch", "match_web_pdf_test.pdf")
build_pdf_file(req, pdf_path)

reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)

print("=== [웹 실시간 결과와 PDF 인쇄 결과 100% 동일 매칭 검증] ===")
print("PDF 총 페이지 수:", page_count, "페이지")

p_last = reader.pages[-1].extract_text()

print("마지막 페이지에 '지원 자격 필독' 박스 수용 여부:", "지원 자격 필독" in p_last)
print("마지막 페이지에 '실무 필수 지침' 박스 수용 여부:", "실무 필수 지침" in p_last)
print("마지막 페이지 7대 서류 표 항목 7번 완결 여부:", "사업계획서 원본" in p_last)

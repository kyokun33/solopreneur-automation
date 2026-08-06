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
pdf_path = os.path.join(BASE_DIR, "scratch", "clean_appendix_final.pdf")
build_pdf_file(req, pdf_path)

reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)

print("=== [지저분한 기호 제거 및 마지막장 100% 통합 검증 결과] ===")
print("PDF 총 페이지 수:", page_count, "페이지")

p_last = reader.pages[-1].extract_text()
p_prev = reader.pages[-2].extract_text()

print("마지막 페이지에 쌩 마크다운 ** 별표 기호 포함 여부 (포함 안 되어야 성공):", "**" in p_last)
print("이전 페이지 본문 완결 여부:", "정부지원사업 지원 제외" not in p_prev)
print("마지막 페이지 7대 서류 표 항목 7번 완결 여부:", "사업계획서 원본" in p_last)
print("마지막 페이지 푸터 정식 발급 문구 완결 여부:", "고고플렉스 AI 연구소" in p_last)

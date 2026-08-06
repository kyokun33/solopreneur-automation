import sys
import os

BASE_DIR = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "report_generator"))

from report_generator.schemas import ReportRequest
from report_generator.generator import generate_business_report, build_pdf_file
import pypdf

programs = [
    ("packages_15p", "예창패/초창패 (목표 15p)", 15),
    ("cheongsa_12p", "청년창업사관학교 (목표 12p)", 12),
    ("rnd_25p", "R&D 과제 (목표 20~30p)", 25),
    ("export_8p", "수출바우처 (목표 8p)", 8),
    ("local_5p", "지자체 소액 (목표 5p)", 5)
]

domains = [
    ("fnb", "ai커피숍 (F&B)", "로봇으로 서빙하고 음료 제조함"),
    ("ecommerce", "24시 무인 스토어 (이커머스)", "AI 무재고 위탁 및 오토 풀필먼트"),
    ("it_saas", "AI 자동화 플랫폼 (IT/SaaS)", "3초 만에 사업계획서 자동 렌더링"),
    ("hardware", "스마트 3D 사출 공장 (제조)", "모듈화 양산 설비 및 3D 시제품"),
    ("bio_health", "정밀 뷰티 헬스케어 (바이오)", "KFDA 식약처 인증 및 특허 알고리즘")
]

results = []

out_dir = os.path.join(BASE_DIR, "scratch", "test_pdfs")
os.makedirs(out_dir, exist_ok=True)

for prog_code, prog_label, target_pages in programs:
    for dom_code, title, features in domains:
        req = ReportRequest(
            title=title,
            category="government",
            program_type=prog_code,
            target_customer="1인 기업가, 소상공인, 일반 유저",
            core_features=features,
            budget="100,000,000원",
            access_key="KM849201"
        )
        
        md_text, html_text = generate_business_report(req)
        pdf_filename = f"{prog_code}_{dom_code}.pdf"
        pdf_path = os.path.join(out_dir, pdf_filename)
        
        build_pdf_file(req, pdf_path)
        
        reader = pypdf.PdfReader(pdf_path)
        pages_count = len(reader.pages)
                
        results.append({
            "prog_label": prog_label,
            "domain_label": title,
            "target_pages": target_pages,
            "actual_pages": pages_count,
            "char_count": len(md_text)
        })

print("=== [25가지 전 조합 사업계획서 PDF 페이지 수 테스트 결과] ===")
for idx, r in enumerate(results, 1):
    status = "OK" if r['actual_pages'] >= 4 else "NEED_MORE"
    print(f"[{idx:02d}] {r['prog_label']} | {r['domain_label']} | Target: {r['target_pages']}p | Actual: {r['actual_pages']}p | Chars: {r['char_count']:,} chars | {status}")

with open(os.path.join(BASE_DIR, "scratch", "test_matrix_report.json"), "w", encoding="utf-8") as f:
    import json
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nMatrix Test Complete!")

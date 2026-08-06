import os
import sys
import datetime
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas import ReportRequest, ReportResponse
from generator import generate_business_report

app = FastAPI(
    title="AI Business Report Generator SaaS",
    description="3분 만에 완성되는 K-Startup 대한민국 HWP/Word 공식 서식 동기화 사업계획서 자동 생성기 (3분시리즈 1 v2.70 정식버전)",
    version="2.7.0"
)

static_dir = os.path.join(BASE_DIR, "static")
template_dir = os.path.join(BASE_DIR, "templates")

os.makedirs(static_dir, exist_ok=True)
os.makedirs(template_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=template_dir)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

KEYS_FILE = os.path.join(BASE_DIR, "keys.json")

def load_keys():
    if not os.path.exists(KEYS_FILE):
        default_keys = {
            "DEMO-FREE-2026": {"used": False, "created_at": "2026-08-06"},
            "KMONG-REPORT-1001": {"used": False, "created_at": "2026-08-06"},
            "KMONG-REPORT-1002": {"used": False, "created_at": "2026-08-06"},
            "KMONG-REPORT-1003": {"used": False, "created_at": "2026-08-06"}
        }
        with open(KEYS_FILE, "w", encoding="utf-8") as f:
            import json
            json.dump(default_keys, f, ensure_ascii=False, indent=2)
        return default_keys
    try:
        import json
        with open(KEYS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_keys(keys_data):
    import json
    with open(KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(keys_data, f, ensure_ascii=False, indent=2)

async def handle_generate(req: ReportRequest):
    # 1회용 구매 인증 코드 / 크몽 주문번호 검증
    key_str = (req.access_key or "").strip().upper()
    keys_db = load_keys()

    if not key_str:
        return JSONResponse(
            status_code=403,
            content={"success": False, "detail": "🔑 크몽 주문번호 또는 1회용 인증 코드가 입력되지 않았습니다. 크몽 마이페이지에서 주문번호를 확인 후 입력해 주세요."}
        )

    # 최소 5자 이상의 크몽 주문번호 또는 사전 등록 키 패턴 체크
    if len(key_str) < 5:
        return JSONResponse(
            status_code=403,
            content={"success": False, "detail": "❌ 유효하지 않은 주문번호 형태입니다. 올바른 크몽 주문번호(예: KM849201)를 입력해 주세요."}
        )

    # 💡 무제한 데모 테스트 키 목록 (소멸하지 않고 언제나 100% 무한 사용)
    UNLIMITED_DEMO_KEYS = ["DEMO-FREE-2026", "KMONG-FREE-TEST", "FREE-DEMO-2026", "TEST-FREE-KEY"]

    # 이미 사용 완료된 주문번호/키인지 확인 (무제한 데모 키는 예외)
    if key_str not in UNLIMITED_DEMO_KEYS and key_str in keys_db and keys_db[key_str].get("used", False):
        used_time = keys_db[key_str].get("used_at", "최근")
        report_title = keys_db[key_str].get("title", "")
        return JSONResponse(
            status_code=403,
            content={"success": False, "detail": f"🚫 이미 1회 보고서 생성이 완료되어 소멸된 주문번호입니다. (사용 일시: {used_time})\n생성된 보고서: [{report_title}]"}
        )

    # 새로운 주문번호가 들어오면 동적으로 1회용 정품 등록 처리
    if key_str not in keys_db:
        keys_db[key_str] = {
            "used": False,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "Kmong Order ID Auto-Verification"
        }

    # 보고서 작성 수행
    md_content, html_content = generate_business_report(req)
    
    # 1회 사용 즉시 소멸(Used) 처리 및 CS 추적 로그 기록
    keys_db[key_str]["used"] = True
    keys_db[key_str]["used_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keys_db[key_str]["title"] = req.title
    keys_db[key_str]["category"] = req.category
    save_keys(keys_db)
    
    category_map = {
        "government": "정부지원사업용",
        "ir": "투자유치(IR)용",
        "market": "시장분석용"
    }
    
    return ReportResponse(
        success=True,
        title=req.title,
        category_name=category_map.get(req.category, "비즈니스 리포트"),
        markdown_content=md_content,
        html_content=html_content,
        generated_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.post("/api/generate", response_model=ReportResponse)
async def generate_report_api(req: ReportRequest):
    return await handle_generate(req)

@app.post("/generate-report", response_model=ReportResponse)
async def generate_report_direct(req: ReportRequest):
    return await handle_generate(req)

@app.post("/api/download-md")
async def download_markdown_api(title: str = Form(default="사업계획서"), content: str = Form(default="")):
    safe_title = urllib.parse.quote(title.replace(' ', '_'))
    # UTF-8 BOM (b'\xef\xbb\xbf') 추가로 HWP / MS Word 한글 깨짐 100% 영구 방지
    bom_content = b'\xef\xbb\xbf' + content.encode("utf-8")
    return Response(
        content=bom_content,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename=\"report.md\"; filename*=UTF-8''{safe_title}.md"}
    )

@app.post("/api/download-pdf")
async def download_pdf_api(
    title: str = Form(default="사업계획서"),
    category: str = Form(default="government"),
    program_type: str = Form(default="packages_15p"),
    target_customer: str = Form(default="전 연령"),
    core_features: str = Form(default="AI 자동화"),
    budget: str = Form(default="초기 예산 1,000만 원 / 월 목표 매출 500만 원")
):
    from generator import build_pdf_file
    import tempfile
    
    req_obj = ReportRequest(
        title=title,
        category=category,
        program_type=program_type,
        target_customer=target_customer,
        core_features=core_features,
        budget=budget,
        access_key="DEMO-FREE-2026"
    )
    
    temp_pdf = os.path.join(tempfile.gettempdir(), f"report_{int(datetime.datetime.now().timestamp())}.pdf")
    build_pdf_file(req_obj, temp_pdf)
    
    with open(temp_pdf, "rb") as f:
        pdf_bytes = f.read()
        
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=\"report.pdf\""}
    )

@app.post("/download-md")
async def download_markdown_direct(title: str = Form(default="사업계획서"), content: str = Form(default="")):
    safe_title = urllib.parse.quote(title.replace(' ', '_'))
    bom_content = b'\xef\xbb\xbf' + content.encode("utf-8")
    return Response(
        content=bom_content,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename=\"report.md\"; filename*=UTF-8''{safe_title}.md"}
    )

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Report Generator SaaS"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8090, reload=True)

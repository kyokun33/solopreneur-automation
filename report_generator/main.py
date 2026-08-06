import os
import sys
import datetime

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
    description="3분 만에 완성되는 AI 사업계획서 및 시장분석 보고서 자동 생성기",
    version="1.0.0"
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

@app.post("/api/generate", response_model=ReportResponse)
async def generate_report(req: ReportRequest):
    # 1회용 구매 인증 코드 검증
    key_str = (req.access_key or "").strip().upper()
    keys_db = load_keys()

    if not key_str:
        return JSONResponse(
            status_code=403,
            content={"success": False, "detail": "🔑 1회용 구매 인증 코드가 입력되지 않았습니다. 크몽에서 제공받은 시리얼 코드를 입력해 주세요."}
        )

    if key_str not in keys_db:
        return JSONResponse(
            status_code=403,
            content={"success": False, "detail": "❌ 유효하지 않은 인증 코드입니다. 크몽에서 발급된 정품 1회용 시리얼 코드를 확인해 주세요."}
        )

    if keys_db[key_str].get("used", False):
        return JSONResponse(
            status_code=403,
            content={"success": False, "detail": "🚫 이미 1회 사용 완료된 소멸 코드입니다. 재사용을 위해 추가 이용권을 구매해 주세요."}
        )

    # 보고서 생성
    md_content, html_content = generate_business_report(req)
    
    # 키 사용 완료(Used) 상태로 1회성 차단 소멸 처리
    keys_db[key_str]["used"] = True
    keys_db[key_str]["used_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

@app.post("/api/download-md")
async def download_markdown(title: str = Form(...), content: str = Form(...)):
    filename = f"{title.replace(' ', '_')}_사업계획서.md"
    return Response(
        content=content.encode("utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"}
    )

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Report Generator SaaS"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

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

@app.post("/api/generate", response_model=ReportResponse)
async def generate_report(req: ReportRequest):
    md_content, html_content = generate_business_report(req)
    
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

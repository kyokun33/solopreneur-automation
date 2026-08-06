import os
import datetime
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="1인기업 AI 프롬프트 100선 전자책 자동 판매 & 배포 포털")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "1인기업_AI자동화_프롬프트100선_전자책.pdf")
STATIC_PATH = os.path.join(BASE_DIR, "static")

if os.path.exists(STATIC_PATH):
    app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

@app.get("/", response_class=HTMLResponse)
async def sales_page():
    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 [특가 29,000원] 1인 기업가 AI 업무 자동화 프롬프트 100선 완장판 즉시 소장</title>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4f46e5;
            --primary-dark: #3730a3;
            --accent: #10b981;
            --bg-page: #f8fafc;
            --text-main: #0f172a;
            --text-sub: #475569;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; }
        body { background: var(--bg-page); color: var(--text-main); line-height: 1.7; padding-bottom: 80px; }

        .container { max-width: 900px; margin: 0 auto; padding: 0 20px; }

        .header-banner {
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
            color: white;
            padding: 50px 20px;
            text-align: center;
            border-bottom: 4px solid #818cf8;
        }

        .price-badge {
            background: #ef4444;
            color: white;
            font-weight: 800;
            padding: 6px 18px;
            border-radius: 30px;
            font-size: 0.95rem;
            display: inline-block;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
        }

        .main-title { font-size: 2.2rem; font-weight: 800; margin-bottom: 14px; line-height: 1.35; }
        .sub-title { font-size: 1.15rem; color: #c7d2fe; max-width: 700px; margin: 0 auto 30px auto; }

        .hero-img {
            max-width: 100%; width: 440px; border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4); border: 4px solid white; margin-bottom: 25px;
        }

        .cta-btn-group { display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; }
        .btn-buy {
            background: #10b981; color: white; border: none; padding: 18px 36px;
            font-size: 1.2rem; font-weight: 800; border-radius: 14px; cursor: pointer;
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4); text-decoration: none;
            transition: transform 0.2s; display: inline-flex; align-items: center; gap: 8px;
        }
        .btn-buy:hover { transform: translateY(-3px); background: #059669; }

        .btn-copy-platform {
            background: #6366f1; color: white; border: none; padding: 18px 28px;
            font-size: 1.05rem; font-weight: 700; border-radius: 14px; cursor: pointer;
            text-decoration: none; box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
        }

        .card-box {
            background: white; border-radius: 18px; padding: 32px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); margin-top: 35px; border: 1px solid #e2e8f0;
        }

        .card-title { font-size: 1.4rem; font-weight: 800; margin-bottom: 16px; color: var(--primary-dark); }

        .feature-list { list-style: none; }
        .feature-list li {
            padding: 12px 0; border-bottom: 1px solid #f1f5f9;
            display: flex; align-items: center; gap: 10px; font-size: 1.05rem; font-weight: 600;
        }

        .copy-box {
            background: #0f172a; color: #f1f5f9; border-radius: 12px; padding: 20px;
            font-family: monospace; font-size: 0.92rem; line-height: 1.6; white-space: pre-wrap; margin-top: 15px;
        }
    </style>
</head>
<body>

    <div class="header-banner">
        <span class="price-badge">🔥 오늘만 80% 특별 할인 (정가 150,000원 ➔ 29,000원)</span>
        <h1 class="main-title">밤샘 일하던 1인 기업가가 하루 4시간만 일하고<br/>매출 2배 만든 AI 프롬프트 100선 완장판</h1>
        <p class="sub-title">크몽/스마트스토어/리틀리 판매 검증 완료! 1초 복사+붙여넣기로 당신 곁에 24시간 일하는 10명의 에이스 직원을 무료 고용하세요.</p>
        <img src="/static/ebook_cover.png" alt="전자책 3D 커버" class="hero-cover-img">
        
        <div class="cta-btn-group">
            <a href="/download-ebook" class="btn-buy">📥 29,000원 즉시 소장 & PDF 자동 다운로드</a>
        </div>
    </div>

    <div class="container">

        <!-- 100선 포함 항목 혜택 -->
        <div class="card-box">
            <h2 class="card-title">🎁 전자책 구매 시 제공되는 5대 킬러 혜택</h2>
            <ul class="feature-list">
                <li>✅ <b>001 ~ 020</b>: 무자본 고수익 비즈니스 발굴 & 경쟁사 파고들기 프롬프트 20종</li>
                <li>✅ <b>021 ~ 040</b>: 조회수 5배 솟구치는 블로그/유튜브/카드뉴스 카피 프롬프트 20종</li>
                <li>✅ <b>041 ~ 060</b>: 거절 없는 B2B 영업 제안 이메일 & 결제 대화법 프롬프트 20종</li>
                <li>✅ <b>061 ~ 080</b>: 10페이지 보고서 1분 요약 & 파이썬 업무 자동화 프롬프트 20종</li>
                <li>✅ <b>081 ~ 100</b>: 미드저니 8k 로고/3D 커버 생성 & 무인 자동 판매 펀널 20종</li>
                <li>🎁 <b>특별 부록</b>: 1초 프롬프트 복사 버튼이 포함된 무제한 평생소장 웹 뷰어 제공</li>
            </ul>
        </div>

        <!-- 크몽/스마트스토어 등록용 상세페이지 복사 코너 -->
        <div class="card-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 class="card-title" style="margin-bottom:0;">🛒 크몽 / 스마트스토어 등록용 상세페이지 카피</h2>
                <button onclick="copyKmongCopy()" style="background:var(--primary); color:white; border:none; padding:8px 16px; border-radius:8px; font-weight:700; cursor:pointer;">📋 카피 1초 복사</button>
            </div>
            <p style="color:var(--text-sub); font-size:0.9rem; margin-top:8px;">이 텍스트를 복사해서 크몽, 네이버 스마트스토어, 리틀리에 등록하면 바로 무인 판매가 시작됩니다.</p>
            <div class="copy-box" id="kmongCopyText">[상품명] 1인 기업가를 위한 AI 업무 자동화 프롬프트 100선 완장판 (복사해서 바로 쓰는 치트키)

[추천 대상]
- 혼자서 기획, 마케팅, 영업, 고객응대까지 하느라 야근이 일상인 1인 기업가
- 마케팅 문구 작성이 막막하고 시간이 부족한 프리랜서/자영업자
- 챗GPT를 어떻게 써야 할지 감이 안 오는 입문자

[포함 내용 (100선 완장판)]
1. 무자본 고수익 아이템 발굴 & 린 사업계획서 프롬프트 20종
2. 조회수 5배 높이는 마케팅 & 숏폼 대본 프롬프트 20종
3. 거절 없는 B2B 영업 제안 & 결제 설득 대화법 20종
4. 보고서 1분 요약 & 파이썬 업무 자동화 프롬프트 20종
5. 미드저니 8k 로고 & 무인 연금 자동화 펀널 프롬프트 20종

구매 즉시 고화질 PDF 전자책과 1초 복사 웹 뷰어가 자동 제공됩니다!</div>
        </div>

    </div>

    <script>
        function copyKmongCopy() {
            const text = document.getElementById('kmongCopyText').innerText;
            navigator.clipboard.writeText(text).then(() => {
                alert("📋 크몽/스마트스토어 상세페이지 카피가 복사되었습니다! 크몽 상품 등록창에 붙여넣으세요.");
            });
        }
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)

@app.get("/download-ebook")
async def download_pdf():
    if os.path.exists(PDF_PATH):
        return FileResponse(
            PDF_PATH,
            media_type="application/pdf",
            filename="1인기업_AI자동화_프롬프트100선_전자책.pdf"
        )
    return Response(content="PDF file not found", status_code=404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8090))
    uvicorn.run("sales_portal:app", host="0.0.0.0", port=port)

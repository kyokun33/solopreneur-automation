import os
import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="AI Shorts & Marketing Copywriter Pro v2.0")

os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class MarketingRequest(BaseModel):
    product_name: str
    target_audience: str
    key_benefit: str
    tone: str = "friendly"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/generate-marketing")
async def generate_marketing(req: MarketingRequest):
    p_name = req.product_name
    target = req.target_audience
    benefit = req.key_benefit
    
    # 1. 30초 유튜브 숏츠 / 틱톡 성우 대본
    shorts_script = f"""🎬 [30초 유튜브 숏츠 / 틱톡 / 리릴스 전용 대본]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 타겟: {target}
📌 상품: {p_name}
📌 핵심 혜택: {benefit}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[00:00 - 00:05] 🔥 HOOK (후킹 화면)
- 화면: "아직도 밤새 일하시나요?" 텍스트 팝업 & 당황하는 모습
- 성우 VO: "아직도 힘들게 밤새서 업무 처리하고 계신가요? 멈추세요!"

[00:05 - 00:15] ⚡ PROBLEM & SOLUTION (문제 제기 & 솔루션)
- 화면: [{p_name}] 구동 화면 및 빠른 작업 연출 컷
- 성우 VO: "단 3초 만에 시작하는 [{p_name}] 하나면, {target}의 {benefit} 해결 끝!"

[00:15 - 00:25] 💡 PROOF & BENEFIT (실제 효과 증명)
- 화면: 하루 4시간 절약 그래프 & 사용자 후기 팝업
- 성우 VO: "실제 사용 후 하루 업무 시간이 70% 단축되었습니다. 누구나 1초 만에 마케팅 세트 완성!"

[00:25 - 00:30] 🎁 CALL TO ACTION (클릭 유도)
- 화면: 손가락이 프로필 링크를 가리키는 고화질 애니메이션
- 성우 VO: "지금 프로필 링크 누르고 선착순 할인 혜택을 챙기세요!"
"""

    # 2. Blog Copy
    blog_post = f"""# 🚀 [{p_name}] {target}를 위한 최고의 선택!

안녕하세요! 오늘은 {target} 분들이 가장 필요로 하시는 **"{p_name}"**을 소개해 드립니다.

## 💡 왜 {p_name}이 필요할까요?
많은 분들이 바쁜 일상 속에서 업무 효율에 고민을 안고 계십니다. 
**"{p_name}"**은 바로 **{benefit}**을(를) 통해 여러분의 사업 및 마케팅을 180도 바꾸어 드립니다.

### 🌟 핵심 장점 3가지
1. **압도적 효과**: {benefit}
2. **누구나 쉽게**: 3초 만에 무인 파이프라인 가동
3. **가성비 끝판왕**: 부담 없는 1인 기업 전용 구성

지금 바로 확인해 보세요!
"""

    # 3. Instagram Caption
    insta_caption = f"""✨ {target} 필수템 등장! ✨

더 이상 고민하지 마세요 🛑
[{p_name}] 하나로 {benefit} 해결 끝! 🔥

📌 이럴 때 추천해요:
✔️ 바쁜 일정 속 효율을 높이고 싶을 때
✔️ {benefit}을(를) 빠르게 경험하고 싶을 때

👉 지금 바로 프로필 링크 확인하기! (선착순 할인 진행 중 🎁)

# {p_name.replace(' ', '')} #{target.replace(' ', '')} #추천템 #자동숏츠 #1인기업 #마케팅자동화"""

    # 4. Card News Script
    card_news = [
        {"slide": 1, "title": f"😲 아직도 힘들게 작업하시나요?", "content": f"{target}를 위한 역대급 꿀팁 공개!"},
        {"slide": 2, "title": f"🔥 [{p_name}]의 등장", "content": f"더 이상 시간 낭비하지 마세요."},
        {"slide": 3, "title": f"⚡ 핵심 혜택: {benefit}", "content": f"단 3초 만에 당신의 시간을 절약해 드립니다."},
        {"slide": 4, "title": "⭐ 실제 사용자 후기", "content": f"\"[{p_name}] 쓰고 작업 시간이 절반으로 줄었어요!\""},
        {"slide": 5, "title": "🎁 프로필 링크 클릭!", "content": "지금 신청 시 특별 할인 혜택 제공!"}
    ]

    return {
        "success": True,
        "product_name": p_name,
        "shorts_script": shorts_script,
        "blog_post": blog_post,
        "insta_caption": insta_caption,
        "card_news": card_news,
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

import os
from generate_full_100_prompts import titles_100, categories, generate_prompt_text

html_head = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💡 [비밀 치트키] 1인 기업 AI 업무 자동화 프롬프트 100선 가이드북 (100% 완장판)</title>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-page: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #0f172a;
            --text-sub: #475569;
            --text-muted: #64748b;
            --primary: #4f46e5;
            --primary-light: #e0e7ff;
            --primary-dark: #3730a3;
            --accent-green: #059669;
            --accent-amber: #d97706;
            --border-subtle: #e2e8f0;
            --card-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.05), 0 8px 10px -6px rgba(15, 23, 42, 0.03);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        }

        body {
            background-color: var(--bg-page);
            color: var(--text-main);
            line-height: 1.75;
            padding-bottom: 100px;
        }

        .container {
            max-width: 980px;
            margin: 0 auto;
            padding: 0 24px;
        }

        .hero-banner {
            background: linear-gradient(135deg, #eef2ff 0%, #fae8ff 50%, #f0fdf4 100%);
            padding: 45px 24px;
            text-align: center;
            border-bottom: 1px solid var(--border-subtle);
            margin-bottom: 35px;
        }

        .hero-cover-img {
            max-width: 100%;
            width: 440px;
            height: auto;
            border-radius: 18px;
            box-shadow: 0 20px 30px -10px rgba(79, 70, 229, 0.2);
            margin-bottom: 20px;
            border: 4px solid #ffffff;
        }

        .hero-badge {
            display: inline-block;
            background: #ffffff;
            color: var(--primary);
            font-weight: 700;
            font-size: 0.88rem;
            padding: 6px 18px;
            border-radius: 30px;
            box-shadow: 0 2px 8px rgba(79, 70, 229, 0.12);
            margin-bottom: 14px;
        }

        .hero-title {
            font-size: 2.1rem;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.5px;
            margin-bottom: 12px;
            line-height: 1.35;
        }

        .hero-subtitle {
            font-size: 1.1rem;
            color: var(--text-sub);
            max-width: 700px;
            margin: 0 auto 20px auto;
            word-break: keep-all;
        }

        .curiosity-box {
            background: #ffffff;
            border-left: 5px solid var(--primary);
            border-radius: 14px;
            padding: 22px 26px;
            box-shadow: var(--card-shadow);
            margin-bottom: 35px;
        }

        .curiosity-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--primary-dark);
            margin-bottom: 8px;
        }

        .curiosity-text {
            color: var(--text-sub);
            font-size: 0.98rem;
            line-height: 1.65;
        }

        /* Vector Step Infographic Styles */
        .step-pipeline-wrapper {
            background: #ffffff;
            border-radius: 20px;
            padding: 32px 24px;
            box-shadow: var(--card-shadow);
            margin-bottom: 40px;
            border: 1px solid #f1f5f9;
        }

        .step-pipeline-header {
            text-align: center;
            margin-bottom: 24px;
        }

        .step-pipeline-tag {
            color: var(--primary);
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 1px;
        }

        .step-pipeline-title {
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--text-main);
            margin-top: 4px;
        }

        .step-pipeline-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            align-items: stretch;
            position: relative;
        }

        @media (max-width: 768px) {
            .step-pipeline-grid {
                grid-template-columns: 1fr;
            }
        }

        .step-pipeline-card {
            background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
            border: 1.5px solid #e0e7ff;
            border-radius: 16px;
            padding: 20px 16px;
            text-align: center;
            position: relative;
            transition: all 0.25s ease;
        }

        .step-pipeline-card:hover {
            transform: translateY(-4px);
            border-color: var(--primary);
            box-shadow: 0 12px 24px -6px rgba(79, 70, 229, 0.18);
        }

        .step-circle-badge {
            width: 38px;
            height: 38px;
            background: var(--primary);
            color: #ffffff;
            font-weight: 800;
            font-size: 1.1rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px auto;
            box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);
        }

        .step-card-num {
            font-size: 0.75rem;
            font-weight: 800;
            color: var(--primary-dark);
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 4px;
        }

        .step-card-heading {
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 8px;
        }

        .step-card-text {
            font-size: 0.88rem;
            color: var(--text-sub);
            line-height: 1.45;
        }

        /* 3D Icons Banner */
        .step-icons-banner {
            text-align: center;
            margin-bottom: 24px;
        }

        .step-icons-img {
            max-width: 100%;
            width: 620px;
            height: auto;
            border-radius: 12px;
        }

        /* Category Nav Tabs */
        .category-nav {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 12px;
            margin-bottom: 24px;
            border-bottom: 2px solid var(--border-subtle);
        }

        .cat-tab {
            background: #ffffff;
            border: 1px solid var(--border-subtle);
            color: var(--text-sub);
            padding: 10px 18px;
            border-radius: 30px;
            font-size: 0.9rem;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s ease;
        }

        .cat-tab.active {
            background: var(--primary);
            color: #ffffff;
            border-color: var(--primary);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
        }

        .cat-section {
            display: none;
        }

        .cat-section.active {
            display: block;
        }

        .prompt-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 24px;
            box-shadow: var(--card-shadow);
            margin-bottom: 22px;
            border: 1px solid #f1f5f9;
        }

        .prompt-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 14px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .part-badge {
            background: #e0e7ff;
            color: #3730a3;
            font-size: 0.78rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 16px;
            margin-bottom: 4px;
            display: inline-block;
        }

        .prompt-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--text-main);
        }

        .btn-copy {
            background: var(--primary);
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(79, 70, 229, 0.2);
            transition: all 0.2s ease;
        }

        .btn-copy:hover {
            background: var(--primary-dark);
        }

        .prompt-code-box {
            background: #0f172a;
            color: #f1f5f9;
            border-radius: 10px;
            padding: 16px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.92rem;
            line-height: 1.55;
            white-space: pre-wrap;
        }

        #toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: #10b981;
            color: white;
            padding: 12px 24px;
            border-radius: 30px;
            font-weight: 700;
            font-size: 0.95rem;
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            z-index: 9999;
        }

        #toast.show {
            transform: translateX(-50%) translateY(0);
        }
    </style>
</head>
<body>

    <div class="hero-banner">
        <span class="hero-badge">💡 100% 완장판 - 1인기업 필수 프롬프트 총 100선 포함</span>
        <h1 class="hero-title">밤샘 일하던 1인 기업가가 하루 4시간만 일하고<br/>매출 2배 만든 AI 프롬프트 100선</h1>
        <p class="hero-subtitle">더 이상 밤새우지 마세요! 기획부터 마케팅, B2B 영업, 문서 자동화, 이미지 숏폼까지 100가지 치트키가 들어있습니다.</p>
        <img src="./static/ebook_cover.png" alt="전자책 커버" class="hero-cover-img">
    </div>

    <div class="container">

        <div class="curiosity-box">
            <h3 class="curiosity-title">😲 "100가지 프롬프트로 24시간 불평 없이 일하는 10명의 에이스 직원을 고용하세요"</h3>
            <p class="curiosity-text">
                원하는 주제 카테고리를 선택하고, 필요한 프롬프트의 **[1초 복사]** 버튼을 눌러 ChatGPT에 바로 붙여넣으세요!
            </p>
        </div>

        <!-- Vector Step Infographic Pipeline -->
        <div class="step-pipeline-wrapper">
            <div class="step-pipeline-header">
                <div class="step-pipeline-tag">HIGH-PRECISION STEP GUIDE</div>
                <h2 class="step-pipeline-title">⚡ 10초 만에 따라하는 선명한 4단계 실행 가이드</h2>
            </div>
            
            <div class="step-icons-banner">
                <img src="./static/step_icons_3d.png" alt="3D Step Icons Graphic" class="step-icons-img">
            </div>

            <div class="step-pipeline-grid">
                <div class="step-pipeline-card">
                    <div class="step-circle-badge">1</div>
                    <div class="step-card-num">STEP 01</div>
                    <div class="step-card-heading">📋 1초 복사하기</div>
                    <div class="step-card-text">원하는 프롬프트의 <b>[1초 복사]</b> 버튼을 클릭합니다.</div>
                </div>

                <div class="step-pipeline-card">
                    <div class="step-circle-badge">2</div>
                    <div class="step-card-num">STEP 02</div>
                    <div class="step-card-heading">💬 대화창 붙여넣기</div>
                    <div class="step-card-text">ChatGPT / Claude 화면에 <b>Ctrl+V</b>로 붙여넣습니다.</div>
                </div>

                <div class="step-pipeline-card">
                    <div class="step-circle-badge">3</div>
                    <div class="step-card-num">STEP 03</div>
                    <div class="step-card-heading">📌 내 정보 입력</div>
                    <div class="step-card-text"><b>[ ]</b> 괄호 자리에 내 상품 이름만 써 넣습니다.</div>
                </div>

                <div class="step-pipeline-card">
                    <div class="step-circle-badge">4</div>
                    <div class="step-card-num">STEP 04</div>
                    <div class="step-card-heading">⚡ 3초 자동 완성</div>
                    <div class="step-card-text">엔터를 치면 10년 차 전문가 원고가 <b>3초 만에 쏟아집니다!</b></div>
                </div>
            </div>
        </div>

        <!-- Category Nav Tabs -->
        <div class="category-nav">
            <button class="cat-tab active" onclick="switchCat('cat1')">PART 1. 비즈니스 기획 (001~020)</button>
            <button class="cat-tab" onclick="switchCat('cat2')">PART 2. 마케팅 & 카피 (021~040)</button>
            <button class="cat-tab" onclick="switchCat('cat3')">PART 3. B2B 영업 & CS (041~060)</button>
            <button class="cat-tab" onclick="switchCat('cat4')">PART 4. 업무 자동화 (061~080)</button>
            <button class="cat-tab" onclick="switchCat('cat5')">PART 5. 이미지 & 숏폼 (081~100)</button>
        </div>
"""

html_sections = ""
for cat_num, (c_title, start_idx, end_idx) in enumerate(categories, 1):
    active_cls = " active" if cat_num == 1 else ""
    html_sections += f'<div id="cat{cat_num}" class="cat-section{active_cls}">\n'
    html_sections += f'<h2 style="font-size:1.4rem; font-weight:800; margin-bottom:20px; color:var(--primary);">{c_title}</h2>\n'
    
    for idx in range(start_idx, end_idx + 1):
        title = titles_100[idx - 1]
        p_text = generate_prompt_text(idx, title)
        
        html_sections += f"""
        <div class="prompt-card">
            <div class="prompt-card-header">
                <div>
                    <span class="part-badge">PROMPT {idx:03d}</span>
                    <h3 class="prompt-title">📌 [{idx:03d}] {title}</h3>
                </div>
                <button class="btn-copy" onclick="copyPrompt('p{idx}')">📋 1초 복사하기</button>
            </div>
            <div class="prompt-code-box" id="p{idx}">{p_text}</div>
        </div>
        """
    html_sections += '</div>\n'

html_footer = """
    </div>

    <div id="toast">📋 프롬프트가 복사되었습니다! ChatGPT 대화창에 Ctrl+V로 붙여넣으세요.</div>

    <script>
        function switchCat(catId) {
            document.querySelectorAll('.cat-tab').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.cat-section').forEach(s => s.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(catId).classList.add('active');
            window.scrollTo({ top: 500, behavior: 'smooth' });
        }

        function copyPrompt(id) {
            const text = document.getElementById(id).innerText;
            navigator.clipboard.writeText(text).then(() => {
                const toast = document.getElementById('toast');
                toast.classList.add('show');
                setTimeout(() => {
                    toast.classList.remove('show');
                }, 2500);
            });
        }
    </script>
</body>
</html>
"""

full_html = html_head + html_sections + html_footer
html_path = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\ebook_reader.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("ebook_reader.html updated with Vector Crisp Infographic Pipeline!")

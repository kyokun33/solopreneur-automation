import os
from PIL import Image, ImageDraw, ImageFont

# Canvas Dimension: EXACTLY 652px width x 488px height (Kmong Main Image Specs)
width = 652
height = 488

# Fonts
font_bold_path = r"C:\Windows\Fonts\malgunbd.ttf"
font_path = r"C:\Windows\Fonts\malgun.ttf"

f_badge = ImageFont.truetype(font_bold_path, 15)
f_title = ImageFont.truetype(font_bold_path, 28)
f_sub = ImageFont.truetype(font_bold_path, 17)
f_price = ImageFont.truetype(font_bold_path, 18)
f_body = ImageFont.truetype(font_path, 14)

bg_path = r"C:\Users\sude3\.gemini\antigravity-ide\brain\1de0288c-41aa-4fd5-8743-69643a6a7058\ai_report_saas_thumbnail_1to1_1786001184590.png"

# Load background and resize to fit 652x488
bg_img = Image.open(bg_path).convert("RGBA")
# Crop center square and resize to 652x488
bg_img_resized = bg_img.resize((width, height), Image.Resampling.LANCZOS)

overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Top Bar (0 ~ 130px)
draw.rectangle([(0, 0), (width, 125)], fill=(15, 23, 42, 235))
draw.rectangle([(0, 122), (width, 125)], fill=(99, 102, 241, 255))

# Red Badge
draw.rounded_rectangle([(25, 12), (230, 40)], radius=12, fill=(239, 68, 68, 255))
draw.text((38, 17), "🔥 3분 완결 AI 사업계획서", font=f_badge, fill=(255, 255, 255, 255))

# Title & Subtitle
draw.text((25, 47), "AI 사업계획서 & 보고서 자동 생성기", font=f_title, fill=(255, 255, 255, 255))
draw.text((25, 90), "정부지원사업 제출용 • IR 투자유치용 • 시장분석 100% 대응", font=f_sub, fill=(165, 180, 252, 255))

# Bottom Bar (height - 90px to height)
draw.rectangle([(0, height - 90), (width, height)], fill=(15, 23, 42, 240))
draw.rectangle([(0, height - 90), (width, height - 87)], fill=(16, 185, 129, 255))

draw.text((25, height - 78), "⚡ 9,900원 초저가 3분 완결  |  월 무제한 PRO 29,900원", font=f_price, fill=(52, 211, 153, 255))
draw.text((25, height - 44), "✓ 실시간 웹 미리보기  ✓ .MD 마크다운 다운로드  ✓ 🖨️ PDF / 인쇄 출력", font=f_body, fill=(226, 232, 240, 255))

# Composite
final_652 = Image.alpha_composite(bg_img_resized, overlay)
output_path = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\static\kmong_652x488_main_thumb.png"
desktop_path = r"C:\Users\sude3\OneDrive\바탕 화면\크몽_652x488_한글_메인이미지.png"

os.makedirs(r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\static", exist_ok=True)
final_652.convert("RGB").save(output_path, "PNG")

desktop_paths = [r'C:\Users\sude3\OneDrive\바탕 화면', r'C:\Users\sude3\Desktop']
for d in desktop_paths:
    if os.path.exists(d):
        dst = os.path.join(d, '크몽_652x488_한글_메인이미지.png')
        final_652.convert("RGB").save(dst, "PNG")
        print('Saved 652x488 image to desktop:', dst)
        break

print(f"Exact 652x488px image generated successfully! (Width: {final_652.width}px, Height: {final_652.height}px)")

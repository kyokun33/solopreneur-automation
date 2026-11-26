# -*- coding: utf-8 -*-
"""
Test refined text background boxes with professional styling:
- Dynamic auto-padding based on text bounding box
- Drop shadows for 3D depth
- Subtle 1.5px semi-transparent borders (no crude 3px solid white outline)
- Perfect horizontal & vertical centering
- Clean vertical spacing
"""

import os
from PIL import Image, ImageDraw, ImageFont

PROJ = r"f:\1인기업\google_flow_projects\empty_stomach_longform"
BRAIN = r"C:\Users\sude3\.gemini\antigravity\brain\56950890-eaa1-44d5-b934-55f3971f1d4a"
DESKTOP = r"C:\Users\sude3\Desktop"

FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"
f_badge = ImageFont.truetype(FONT_BOLD, 36)
f_h1 = ImageFont.truetype(FONT_BOLD, 92)
f_h2 = ImageFont.truetype(FONT_BOLD, 104)
f_pill = ImageFont.truetype(FONT_BOLD, 42)

def draw_pro_badge_box(canvas, text, font, x, y, fill_color, text_color=(255, 255, 255), 
                       pad_x=28, pad_y=14, radius=16, border_color=(255, 255, 255, 120), border_width=2,
                       has_shadow=True, center_x=None):
    """
    Renders a broadcast-quality text background box with precise centering,
    drop shadow, and subtle refined border.
    """
    # Create temporary overlay for alpha blending
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d_over = ImageDraw.Draw(overlay)
    
    # Calculate exact text dimensions
    bbox = d_over.textbbox((0, 0), text, font=font)
    ox, oy, x1, y1 = bbox
    text_w = x1 - ox
    text_h = y1 - oy
    
    box_w = text_w + pad_x * 2
    box_h = text_h + pad_y * 2
    
    if center_x is not None:
        box_x = center_x - box_w // 2
    else:
        box_x = x
    box_y = y
    
    # 1. Soft Drop Shadow
    if has_shadow:
        shadow_box = [box_x + 3, box_y + 5, box_x + box_w + 3, box_y + box_h + 5]
        d_over.rounded_rectangle(shadow_box, radius=radius, fill=(0, 0, 0, 130))
        
    # 2. Main Box Fill
    d_over.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], 
                            radius=radius, fill=fill_color, outline=border_color, width=border_width)
    
    # Composite overlay onto canvas
    canvas.alpha_composite(overlay)
    
    # 3. Draw perfectly centered text
    draw = ImageDraw.Draw(canvas)
    text_draw_x = box_x + pad_x - ox
    text_draw_y = box_y + pad_y - oy
    
    draw.text((text_draw_x, text_draw_y), text, font=font, fill=text_color)
    
    return box_x, box_y, box_w, box_h

def render_longform_test():
    bg_path = os.path.join(BRAIN, "longform_thumbnail_bg_png_1793678650498.jpg")
    canvas = Image.open(bg_path).convert("RGBA").resize((1920, 1080))
    doc_png = Image.open(os.path.join(PROJ, "doctor_healer_transparent.png")).convert("RGBA")
    
    # Doctor character on right
    dw = 620
    dh = int(doc_png.height * (dw / doc_png.width))
    doc_r = doc_png.resize((dw, dh), Image.Resampling.LANCZOS)
    canvas.alpha_composite(doc_r, (1920 - dw + 30, 1080 - dh + 30))
    
    # 1. Top Danger Alert Badge (Crimson Red with soft shadow & subtle highlight border)
    bx, by, bw, bh = draw_pro_badge_box(
        canvas, "● 의사 추천 공복 솔루션", f_badge,
        x=80, y=85,
        fill_color=(220, 38, 38, 245),
        text_color=(255, 255, 255),
        pad_x=32, pad_y=15, radius=18,
        border_color=(255, 255, 255, 90), border_width=2
    )
    
    draw = ImageDraw.Draw(canvas)
    
    # 2. Main Hook Line 1 (with strong 3D drop shadow)
    h1_y = by + bh + 45
    # Shadow
    draw.text((85, h1_y + 5), "아침 공복에 '이것' 먹으면", font=f_h1, fill=(0, 0, 0, 220))
    # Main text with clean stroke
    draw.text((80, h1_y), "아침 공복에 '이것' 먹으면", font=f_h1, fill=(255, 255, 255), stroke_width=6, stroke_fill=(15, 23, 42))
    
    # 3. Main Hook Line 2 (Golden Yellow with deep stroke & shadow)
    h2_y = h1_y + 115
    # Shadow
    draw.text((85, h2_y + 5), "위장이 녹아내린다?!", font=f_h2, fill=(0, 0, 0, 220))
    # Main text
    draw.text((80, h2_y), "위장이 녹아내린다?!", font=f_h2, fill=(253, 224, 71), stroke_width=7, stroke_fill=(180, 83, 9))
    
    # 4. Bottom Solution Capsule Pill (Emerald Green with perfect padding)
    tag_y = h2_y + 135
    draw_pro_badge_box(
        canvas, "최악의 음식 3 vs 의사 보약 3선", f_pill,
        x=80, y=tag_y,
        fill_color=(16, 185, 129, 245),
        text_color=(255, 255, 255),
        pad_x=34, pad_y=16, radius=20,
        border_color=(255, 255, 255, 100), border_width=2
    )
    
    rgb = canvas.convert("RGB")
    test_out = os.path.join(BRAIN, "longform_thumbnail_refined.jpg")
    rgb.save(test_out, "JPEG", quality=95)
    print("Saved test refined longform thumbnail:", test_out)

if __name__ == "__main__":
    render_longform_test()


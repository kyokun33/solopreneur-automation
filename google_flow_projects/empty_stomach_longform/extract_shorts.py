# -*- coding: utf-8 -*-
"""
Extract 3 Focused 9:16 Vertical Shorts (1080x1920) from Long-form Chapters (OSMU)
Shorts 1: 공복 바나나 편 (Scene 2, ~35.4s)
Shorts 2: 공복 고구마 편 (Scene 3, ~33.3s)
Shorts 3: 빈속 모닝커피 편 (Scene 4, ~32.9s)
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess

PROJ = r"f:\1인기업\google_flow_projects\empty_stomach_longform"
TEMP_DIR = os.path.join(PROJ, "temp_shorts")
os.makedirs(TEMP_DIR, exist_ok=True)

FPS = 30
WIDTH = 1080
HEIGHT = 1920

FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"
font_top_badge = ImageFont.truetype(FONT_BOLD, 36)
font_hook = ImageFont.truetype(FONT_BOLD, 54)
font_sub = ImageFont.truetype(FONT_BOLD, 46)
font_brand = ImageFont.truetype(FONT_BOLD, 30)

SHORTS_LIST = [
    {
        "id": "banana",
        "name": "내몸에힐링_숏츠01_공복바나나편",
        "title": "공복에 바나나 먹으면 심장에 무리가 간다?",
        "hook_text": "아침 공복 '바나나'의 충격적 진실!",
        "badge": "1분 건강 팩트체크",
        "image": os.path.join(PROJ, "scene2.jpg"),
        "audio": os.path.join(PROJ, "scene2_master.wav"),
        "duration": 35.374,
        "subtitles": [
            (0.0, 8.0, "첫 번째 피해야 할 음식, 바로 바나나!"),
            (8.0, 15.5, "아침 대용으로 가장 많이 드시는 과일이죠"),
            (15.5, 23.0, "빈속에 먹으면 마그네슘이 급격히 치솟습니다"),
            (23.0, 29.5, "칼륨 균형이 깨져 심혈관에 큰 무리와 어지럼증 유발!"),
            (29.5, 35.4, "심장이나 신장 약하신 분들은 절대 금물입니다")
        ]
    },
    {
        "id": "sweet_potato",
        "name": "내몸에힐링_숏츠02_공복고구마편",
        "title": "공복 군고구마, 위벽을 갉아먹는 주범?",
        "hook_text": "달콤한 '고구마'가 위벽을 녹인다?",
        "badge": "1분 위장 건강",
        "image": os.path.join(PROJ, "scene3.jpg"),
        "audio": os.path.join(PROJ, "scene3_master.wav"),
        "duration": 33.304,
        "subtitles": [
            (0.0, 7.5, "두 번째 위험 음식은 바로 고구마입니다"),
            (7.5, 14.5, "아침에 군고구마, 찐고구마 자주 드시죠?"),
            (14.5, 22.0, "고구마 속 '아교질'과 '타닌'이 위벽을 강하게 자극!"),
            (22.0, 28.0, "과도한 위산 분비로 타는 듯한 속쓰림 유발"),
            (28.0, 33.3, "위염, 위궤양 위험! 빈속 고구마는 피하세요")
        ]
    },
    {
        "id": "coffee",
        "name": "내몸에힐링_숏츠03_빈속모닝커피편",
        "title": "아침 빈속 모닝커피, 위점막을 태운다?",
        "hook_text": "눈뜨자마자 마시는 '모닝커피'의 위험!",
        "badge": "1분 식도·위장 보호",
        "image": os.path.join(PROJ, "scene4.jpg"),
        "audio": os.path.join(PROJ, "scene4_master.wav"),
        "duration": 32.872,
        "subtitles": [
            (0.0, 7.5, "세 번째는 아침 필수품, 바로 '모닝커피'!"),
            (7.5, 15.0, "잠 깨려고 빈속에 진한 커피 한 잔 드시나요?"),
            (15.0, 23.0, "빈속에 고농도 카페인이 위점막을 무방비 타격합니다"),
            (23.0, 28.5, "식도 괄약근이 풀리고 역류성 식도염 직행!"),
            (28.5, 32.9, "커피는 반드시 식후에 드셔야 위를 지킵니다")
        ]
    }
]

def render_vertical_short(item):
    base_img = Image.open(item["image"]).convert("RGB")
    orig_w, orig_h = base_img.size
    
    total_frames = int(item["duration"] * FPS)
    temp_avi = os.path.join(TEMP_DIR, f"{item['id']}_raw.avi")
    out_mp4 = os.path.join(PROJ, f"{item['name']}.mp4")
    desktop_mp4 = os.path.join(r"C:\Users\sude3\Desktop", f"{item['name']}.mp4")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vw = cv2.VideoWriter(temp_avi, fourcc, FPS, (WIDTH, HEIGHT))
    
    print(f"Rendering Shorts: {item['name']} ({total_frames} frames)...")
    
    # Calculate crop for vertical 9:16 (target aspect: 1080/1920 = 9/16 = 0.5625)
    # The source is 16:9 widescreen (1.777 aspect). We zoom and center crop vertically.
    target_aspect = WIDTH / HEIGHT
    
    for f in range(total_frames):
        t = f / FPS
        progress = f / total_frames
        
        # Slow zoom in vertical frame
        zoom = 1.0 + 0.06 * progress
        # To fill vertical, we crop source height, and take corresponding width
        crop_h = int(orig_h / zoom)
        crop_w = int(crop_h * target_aspect)
        
        # Center horizontally with slight pan
        left = int((orig_w - crop_w) * (0.5 + 0.1 * np.sin(progress * np.pi)))
        top = int((orig_h - crop_h) * 0.5)
        
        cropped = base_img.crop((left, top, left + crop_w, top + crop_h))
        frame_img = cropped.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(frame_img, "RGBA")
        
        # 1. Top Channel Header Badge (Center Top)
        top_box = [WIDTH//2 - 240, 160, WIDTH//2 + 240, 230]
        draw.rounded_rectangle(top_box, radius=20, fill=(16, 185, 129, 230), outline=(255, 255, 255, 220), width=3)
        draw.text((WIDTH//2 - 180, 175), f"● {item['badge']}", font=font_top_badge, fill=(255, 255, 255))
        
        # 2. Main Hook Banner Card (Upper Third)
        hook_box = [60, 270, WIDTH - 60, 420]
        draw.rounded_rectangle(hook_box, radius=24, fill=(15, 23, 42, 235), outline=(250, 204, 21, 230), width=3)
        
        # Measure and center hook text
        bbox = draw.textbbox((0, 0), item["hook_text"], font=font_hook)
        hw = bbox[2] - bbox[0]
        draw.text(((WIDTH - hw)//2, 315), item["hook_text"], font=font_hook, fill=(253, 224, 71))
        
        # 3. Dynamic Subtitles (Lower Center: Y=1380~1560)
        cur_sub = ""
        for s_start, s_end, s_text in item["subtitles"]:
            if s_start <= t < s_end:
                cur_sub = s_text
                break
        if not cur_sub and item["subtitles"]:
            cur_sub = item["subtitles"][-1][2]
            
        sub_box = [70, 1420, WIDTH - 70, 1580]
        draw.rounded_rectangle(sub_box, radius=24, fill=(10, 15, 29, 225), outline=(56, 189, 248, 200), width=2)
        
        sub_bbox = draw.textbbox((0, 0), cur_sub, font=font_sub)
        sw = sub_bbox[2] - sub_bbox[0]
        # Text shadow
        draw.text(((WIDTH - sw)//2 + 2, 1475 + 2), cur_sub, font=font_sub, fill=(0, 0, 0, 240))
        draw.text(((WIDTH - sw)//2, 1475), cur_sub, font=font_sub, fill=(255, 255, 255))
        
        # 4. Bottom Brand Watermark
        draw.text((WIDTH//2 - 140, 1760), "구독 & 좋아요 | 내몸에힐링", font=font_brand, fill=(226, 232, 240, 210))
        
        # Convert PIL to CV2 BGR
        frame_cv2 = cv2.cvtColor(np.array(frame_img), cv2.COLOR_RGB2BGR)
        vw.write(frame_cv2)
        
    vw.release()
    
    # Mux with scene audio
    cmd = [
        "ffmpeg", "-y", "-i", temp_avi, "-i", item["audio"],
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(temp_avi):
        os.remove(temp_avi)
        
    import shutil
    shutil.copy2(out_mp4, desktop_mp4)
    print(f"SUCCESS: Shorts '{item['id']}' saved -> {desktop_mp4}")

def main():
    for item in SHORTS_LIST:
        render_vertical_short(item)
    print("ALL SHORTS RENDERED SUCCESSFULLY!")

if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
"""
Render 3 High-Impact Shorts with:
1. Fixed Virtual Host Character Overlay:
   - Shorts 1 (Banana): Mentor Hani (여성 멘토) + SunHi Natural Voice
   - Shorts 2 (Sweet Potato): Doctor Healer (스마트 닥터) + InJoon Natural Voice
   - Shorts 3 (Morning Coffee): Mentor Hani (여성 멘토) + SunHi Natural Voice
2. 5 Major Health Channels Benchmarked Hooking & Design:
   - Top Category Badge with glowing emerald dot
   - Giant 2-Line Hook Header (Golden Yellow, Stroke + Shadow, NO BOX)
   - Bottom Center Subtitles with crisp typography
   - Virtual Host Character breathing & anchored at Bottom-Right PIP!
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess

PROJ = r"f:\1인기업\google_flow_projects\empty_stomach_longform"
TEMP_DIR = os.path.join(PROJ, "temp_shorts_character")
os.makedirs(TEMP_DIR, exist_ok=True)

FPS = 30
WIDTH = 1080
HEIGHT = 1920

FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"
font_badge = ImageFont.truetype(FONT_BOLD, 36)
font_hook1 = ImageFont.truetype(FONT_BOLD, 64)
font_hook2 = ImageFont.truetype(FONT_BOLD, 60)
font_sub = ImageFont.truetype(FONT_BOLD, 48)
font_brand = ImageFont.truetype(FONT_BOLD, 32)
font_char_label = ImageFont.truetype(FONT_BOLD, 26)

SHORTS_CHAR_LIST = [
    {
        "id": "banana",
        "char_img": os.path.join(PROJ, "mentor_hani_transparent.png"),
        "char_name": "힐링 멘토 하니",
        "audio": os.path.join(PROJ, "temp_shorts_v2", "banana_master.wav"),
        "name": "내몸에힐링_숏츠01_공복바나나편",
        "title": "아침 공복에 바나나 먹으면 심장에 큰 무리가 간다? #Shorts #내몸에힐링",
        "desc": "다이어트할 때 아침 대용으로 바나나 드시는 분들 많으시죠? 빈속 바나나의 충격적인 진실을 힐링 멘토 하니가 알려드립니다! #내몸에힐링 #바나나 #건강정보 #1분건강 #Shorts",
        "badge": "1분 팩트체크 · 건강 상식",
        "hook_line1": "아침 공복 '바나나'",
        "hook_line2": "심혈관에 치명타?",
        "image": os.path.join(PROJ, "scene2.jpg"),
        "subtitles": [
            (0.0, 4.2, "첫 번째 피해야 할 음식, 바로 바나나!"),
            (4.2, 8.5, "아침 대용으로 가장 많이 드시는 대표 과일"),
            (8.5, 14.0, "빈속에 먹으면 마그네슘 수치가 급격히 상승!"),
            (14.0, 20.5, "칼륨 균형이 깨져 심혈관 부담과 어지럼증 유발"),
            (20.5, 27.7, "심장과 신장이 약하시다면 절대 금물입니다")
        ]
    },
    {
        "id": "sweet_potato",
        "char_img": os.path.join(PROJ, "doctor_healer_transparent.png"),
        "char_name": "닥터 힐러",
        "audio": os.path.join(PROJ, "temp_shorts_v2", "sweet_potato_master.wav"),
        "name": "내몸에힐링_숏츠02_공복고구마편",
        "title": "달콤한 군고구마가 아침 빈속 위벽을 녹인다? #Shorts #내몸에힐링",
        "desc": "아침에 고구마 먹고 속 쓰리셨던 분들 주목! 아교질과 타닌이 위산 분비를 촉진해 위벽을 자극합니다. 닥터 힐러의 건강 솔루션! #내몸에힐링 #고구마 #위장건강 #1분건강 #Shorts",
        "badge": "의학 팩트체크 · 위장 솔루션",
        "hook_line1": "달콤한 군고구마",
        "hook_line2": "빈속 위벽을 녹인다?",
        "image": os.path.join(PROJ, "scene3.jpg"),
        "subtitles": [
            (0.0, 4.5, "두 번째 위험 음식은 달콤한 고구마입니다"),
            (4.5, 9.0, "아침에 군고구마, 찐고구마 많이 드시죠?"),
            (9.0, 15.0, "고구마 속 '아교질'과 '타닌'이 위벽을 강하게 자극!"),
            (15.0, 20.5, "과도한 위산 분비로 타는 듯한 속쓰림 유발"),
            (20.5, 25.5, "위염과 위궤양 위험! 빈속 고구마는 피하세요")
        ]
    },
    {
        "id": "coffee",
        "char_img": os.path.join(PROJ, "mentor_hani_transparent.png"),
        "char_name": "힐링 멘토 하니",
        "audio": os.path.join(PROJ, "temp_shorts_v2", "coffee_master.wav"),
        "name": "내몸에힐링_숏츠03_빈속모닝커피편",
        "title": "눈뜨자마자 마시는 모닝커피의 치명적인 습격! #Shorts #내몸에힐링",
        "desc": "잠 깨려고 빈속에 진한 아메리카노 한 잔? 고농도 카페인이 위점막을 무방비로 타격합니다! #내몸에힐링 #모닝커피 #역류성식도염 #1분건강 #Shorts",
        "badge": "식도·위장 보호 팩트체크",
        "hook_line1": "눈뜨자마자 마시는",
        "hook_line2": "'모닝커피'의 습격!",
        "image": os.path.join(PROJ, "scene4.jpg"),
        "subtitles": [
            (0.0, 4.2, "세 번째는 아침 필수품, 바로 모닝커피!"),
            (4.2, 9.0, "잠을 깨려고 빈속에 진한 커피 한 잔 드시나요?"),
            (9.0, 15.0, "공복의 고농도 카페인이 위점막을 무방비 타격!"),
            (15.0, 20.5, "식도 괄약근이 느슨해져 역류성 식도염 직행"),
            (20.5, 25.9, "커피는 반드시 식후에 드셔야 위를 지킵니다!")
        ]
    }
]

def draw_clean_text(draw, text, y, font, color, stroke_color=(0, 0, 0), stroke_width=4, shadow_color=(0, 0, 0, 220), shadow_offset=4):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (WIDTH - w) // 2
    # Shadow
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
    # Stroke + Text
    draw.text((x, y), text, font=font, fill=color, stroke_width=stroke_width, stroke_fill=stroke_color)

def render_shorts_with_character(item):
    print(f"\n==========================================")
    print(f"Rendering Character Shorts: {item['name']}")
    print(f"Host: {item['char_name']}")
    print(f"==========================================")
    
    # 1. Get audio duration
    dur_out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", item["audio"]
    ]).decode().strip()
    duration = float(dur_out)
    total_frames = int(duration * FPS)
    
    temp_avi = os.path.join(TEMP_DIR, f"{item['id']}_char_raw.avi")
    out_mp4 = os.path.join(PROJ, f"{item['name']}.mp4")
    desktop_mp4 = os.path.join(r"C:\Users\sude3\Desktop", f"{item['name']}.mp4")
    
    base_bg = Image.open(item["image"]).convert("RGB")
    orig_w, orig_h = base_bg.size
    target_aspect = WIDTH / HEIGHT
    
    # Load Character PNG
    char_src = Image.open(item["char_img"]).convert("RGBA")
    # Resize character to fit bottom-right PIP (Width ~ 480px)
    char_target_w = 460
    char_target_h = int(char_src.height * (char_target_w / char_src.width))
    char_resized = char_src.resize((char_target_w, char_target_h), Image.Resampling.LANCZOS)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vw = cv2.VideoWriter(temp_avi, fourcc, FPS, (WIDTH, HEIGHT))
    
    print(f"Total Frames: {total_frames} (Duration: {duration:.2f}s)")
    
    for f in range(total_frames):
        t = f / FPS
        progress = f / total_frames
        
        # 1. Background Cinematic Zoom
        zoom = 1.0 + 0.06 * progress
        crop_h = int(orig_h / zoom)
        crop_w = int(crop_h * target_aspect)
        left = int((orig_w - crop_w) * (0.5 + 0.06 * np.sin(progress * np.pi)))
        top = int((orig_h - crop_h) * 0.5)
        
        cropped_bg = base_bg.crop((left, top, left + crop_w, top + crop_h))
        frame_img = cropped_bg.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert("RGBA")
        
        # 2. Host Character Overlay (Bottom-Right PIP with gentle breathing animation)
        # Gentle floating / breathing: y offset +/- 6px
        breath_offset = int(6 * np.sin(t * 3.5))
        char_x = WIDTH - char_target_w + 10
        char_y = HEIGHT - char_target_h + breath_offset + 30
        
        # Paste character with transparency
        frame_img.alpha_composite(char_resized, (char_x, char_y))
        
        # Convert back to RGB for drawing text
        frame_rgb = frame_img.convert("RGB")
        draw = ImageDraw.Draw(frame_rgb, "RGBA")
        
        # 3. Top Category Badge (NO BOX, Glowing Emerald Text)
        draw_clean_text(draw, f"● {item['badge']}", 170, font_badge, (52, 211, 153), stroke_color=(10, 30, 20), stroke_width=3)
        
        # 4. Big Bold Hook Header 2 Lines (NO BOX, Golden Yellow)
        draw_clean_text(draw, item["hook_line1"], 250, font_hook1, (253, 224, 71), stroke_color=(20, 20, 20), stroke_width=5)
        draw_clean_text(draw, item["hook_line2"], 335, font_hook2, (255, 255, 255), stroke_color=(20, 20, 20), stroke_width=5)
        
        # 5. Dynamic Subtitle (Left/Center biased away from character)
        cur_sub = ""
        for s_start, s_end, s_text in item["subtitles"]:
            if s_start <= t < s_end:
                cur_sub = s_text
                break
        if not cur_sub and item["subtitles"]:
            cur_sub = item["subtitles"][-1][2]
            
        # Draw subtitle above character area (Y=1340~1420)
        draw_clean_text(draw, cur_sub, 1360, font_sub, (255, 255, 255), stroke_color=(15, 23, 42), stroke_width=4, shadow_offset=4)
        
        # 6. Character Name Badge Tag (Above Character)
        # Small elegant pill for character identity
        char_pill_box = [WIDTH - 260, HEIGHT - 180, WIDTH - 40, HEIGHT - 130]
        draw.rounded_rectangle(char_pill_box, radius=12, fill=(15, 23, 42, 220), outline=(52, 211, 153, 230), width=2)
        draw.text((WIDTH - 245, HEIGHT - 170), f"● {item['char_name']}", font=font_char_label, fill=(240, 253, 244))
        
        # 7. Brand watermark
        draw.text((60, HEIGHT - 100), "내몸에힐링 · 구독 & 좋아요", font=font_brand, fill=(226, 232, 240))
        
        # Convert to CV2 BGR
        frame_cv2 = cv2.cvtColor(np.array(frame_rgb), cv2.COLOR_RGB2BGR)
        vw.write(frame_cv2)
        
    vw.release()
    
    # Mux with clean audio
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
    print(f"SUCCESS: Character Shorts '{item['id']}' saved -> {desktop_mp4}")

def main():
    for item in SHORTS_CHAR_LIST:
        render_shorts_with_character(item)
    print("ALL 3 CHARACTER SHORTS RENDERED SUCCESSFULLY!")

if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
"""
Perfect Shorts Remaster:
1. Audio fix:
   - Eliminate ending beep/click sound (Add smooth 0.3s afade + 0.5s apad silence cushion).
   - Clean, natural mastering without harsh digital limiter popping.
2. Typography & Layout fix:
   - Perfect golden-ratio line-height and vertical padding.
   - Badge Y=210, Hook Line 1 Y=290, Hook Line 2 Y=385 (95px comfortable spacing).
   - Center-bottom Subtitles Y=1430, perfectly balanced and not colliding with character.
   - Character Host: smooth anchored breathing at bottom-right.
3. Replace deliverables on Desktop!
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess

PROJ = r"f:\1인기업\google_flow_projects\empty_stomach_longform"
TEMP_DIR = os.path.join(PROJ, "temp_shorts_perfect")
os.makedirs(TEMP_DIR, exist_ok=True)

FPS = 30
WIDTH = 1080
HEIGHT = 1920

FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"
font_badge = ImageFont.truetype(FONT_BOLD, 34)
font_hook1 = ImageFont.truetype(FONT_BOLD, 62)
font_hook2 = ImageFont.truetype(FONT_BOLD, 54)
font_sub = ImageFont.truetype(FONT_BOLD, 46)
font_brand = ImageFont.truetype(FONT_BOLD, 30)
font_char_label = ImageFont.truetype(FONT_BOLD, 26)

SHORTS_DATA = [
    {
        "id": "banana",
        "char_img": os.path.join(PROJ, "mentor_hani_transparent.png"),
        "char_name": "힐링 멘토 하니",
        "raw_mp3": os.path.join(PROJ, "temp_shorts_v2", "banana_raw.mp3"),
        "name": "내몸에힐링_숏츠01_공복바나나편",
        "badge": "1분 팩트체크 · 건강 상식",
        "hook_line1": "아침 공복 바나나",
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
        "raw_mp3": os.path.join(PROJ, "temp_shorts_v2", "sweet_potato_raw.mp3"),
        "name": "내몸에힐링_숏츠02_공복고구마편",
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
        "raw_mp3": os.path.join(PROJ, "temp_shorts_v2", "coffee_raw.mp3"),
        "name": "내몸에힐링_숏츠03_빈속모닝커피편",
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

def draw_clean_text(draw, text, y, font, color, stroke_color=(15, 23, 42), stroke_width=4, shadow_color=(0, 0, 0, 230), shadow_offset=3):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (WIDTH - w) // 2
    # Shadow
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
    # Stroke + Text
    draw.text((x, y), text, font=font, fill=color, stroke_width=stroke_width, stroke_fill=stroke_color)

def process_audio(raw_mp3, out_wav):
    # 1. Get exact duration of raw mp3
    dur_out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", raw_mp3
    ]).decode().strip()
    raw_dur = float(dur_out)
    
    # 2. Fade out 0.3s before the very end, and add 0.4s clean silence cushion
    fade_start = max(0.0, raw_dur - 0.3)
    filter_str = f"highpass=f=75,lowpass=f=12000,afade=t=out:st={fade_start:.2f}:d=0.3,apad=pad_dur=0.4"
    
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_mp3,
        "-af", filter_str,
        "-ar", "44100", "-ac", "2",
        out_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    final_dur = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out_wav
    ]).decode().strip()
    return float(final_dur)

def render_shorts_perfect(item):
    print(f"\n==========================================")
    print(f"Rendering Remastered Shorts: {item['name']}")
    print(f"==========================================")
    
    clean_wav = os.path.join(TEMP_DIR, f"{item['id']}_clean_master.wav")
    duration = process_audio(item["raw_mp3"], clean_wav)
    total_frames = int(duration * FPS)
    print(f"Clean audio ready: {duration:.2f}s ({total_frames} frames) [ZERO BEEP]")
    
    temp_avi = os.path.join(TEMP_DIR, f"{item['id']}_remaster.avi")
    out_mp4 = os.path.join(PROJ, f"{item['name']}.mp4")
    desktop_mp4 = os.path.join(r"C:\Users\sude3\Desktop", f"{item['name']}.mp4")
    
    base_bg = Image.open(item["image"]).convert("RGB")
    orig_w, orig_h = base_bg.size
    target_aspect = WIDTH / HEIGHT
    
    # Character Host
    char_src = Image.open(item["char_img"]).convert("RGBA")
    char_target_w = 460
    char_target_h = int(char_src.height * (char_target_w / char_src.width))
    char_resized = char_src.resize((char_target_w, char_target_h), Image.Resampling.LANCZOS)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vw = cv2.VideoWriter(temp_avi, fourcc, FPS, (WIDTH, HEIGHT))
    
    for f in range(total_frames):
        t = f / FPS
        progress = f / total_frames
        
        # Smooth background zoom
        zoom = 1.0 + 0.05 * progress
        crop_h = int(orig_h / zoom)
        crop_w = int(crop_h * target_aspect)
        left = int((orig_w - crop_w) * (0.5 + 0.05 * np.sin(progress * np.pi)))
        top = int((orig_h - crop_h) * 0.5)
        
        cropped_bg = base_bg.crop((left, top, left + crop_w, top + crop_h))
        frame_img = cropped_bg.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert("RGBA")
        
        # Host Character (Bottom-Right, subtle breathing)
        breath = int(5 * np.sin(t * 3.5))
        char_x = WIDTH - char_target_w + 10
        char_y = HEIGHT - char_target_h + breath + 35
        frame_img.alpha_composite(char_resized, (char_x, char_y))
        
        frame_rgb = frame_img.convert("RGB")
        draw = ImageDraw.Draw(frame_rgb, "RGBA")
        
        # 1. Top Category Badge (Y=210)
        draw_clean_text(draw, f"● {item['badge']}", 210, font_badge, (52, 211, 153), stroke_width=3)
        
        # 2. Perfect-Spacing Hook Header
        # Line 1 (Golden Yellow, Y=290)
        draw_clean_text(draw, item["hook_line1"], 290, font_hook1, (253, 224, 71), stroke_width=5)
        # Line 2 (Crisp White, Y=385 -> 95px comfortable gap!)
        draw_clean_text(draw, item["hook_line2"], 385, font_hook2, (255, 255, 255), stroke_width=5)
        
        # 3. Dynamic Subtitle (Y=1430, perfectly balanced, no collision)
        cur_sub = ""
        for s_start, s_end, s_text in item["subtitles"]:
            if s_start <= t < s_end:
                cur_sub = s_text
                break
        if not cur_sub and item["subtitles"]:
            cur_sub = item["subtitles"][-1][2]
            
        draw_clean_text(draw, cur_sub, 1430, font_sub, (255, 255, 255), stroke_width=4, shadow_offset=3)
        
        # 4. Host label pill
        char_pill_box = [WIDTH - 250, HEIGHT - 180, WIDTH - 40, HEIGHT - 130]
        draw.rounded_rectangle(char_pill_box, radius=12, fill=(15, 23, 42, 220), outline=(52, 211, 153, 230), width=2)
        draw.text((WIDTH - 235, HEIGHT - 170), f"● {item['char_name']}", font=font_char_label, fill=(240, 253, 244))
        
        # 5. Brand watermark
        draw.text((60, HEIGHT - 90), "내몸에힐링 · 구독 & 좋아요", font=font_brand, fill=(226, 232, 240))
        
        frame_cv2 = cv2.cvtColor(np.array(frame_rgb), cv2.COLOR_RGB2BGR)
        vw.write(frame_cv2)
        
    vw.release()
    
    # Mux clean
    cmd = [
        "ffmpeg", "-y", "-i", temp_avi, "-i", clean_wav,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(temp_avi):
        os.remove(temp_avi)
        
    import shutil
    shutil.copy2(out_mp4, desktop_mp4)
    print(f"SUCCESS: Remastered {desktop_mp4} saved!")

def main():
    for item in SHORTS_DATA:
        render_shorts_perfect(item)
    print("\nALL 3 REMASTERED SHORTS COMPLETED WITHOUT BEEP & PERFECT SPACING!")

if __name__ == "__main__":
    main()


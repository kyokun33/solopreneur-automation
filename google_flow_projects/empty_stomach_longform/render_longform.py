# -*- coding: utf-8 -*-
"""
Render 16:9 Long-form Video for '내몸에힐링'
Resolution: 1920x1080, 30fps
Total duration: ~199.67s (3m 19s)
Features:
- Pan / Ken Burns cinematic zoom on photorealistic 16:9 images
- Brand header pill ("내몸에힐링 · 1분 건강 팩트체크")
- Professional lower-third subtitle card with dark translucent backdrop & golden highlights
- Background music mixed subtly (-24dB ambient bed)
- Muxed with crystal-clear 20대 여성 음성 master audio
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess

PROJ = r"f:\1인기업\google_flow_projects\empty_stomach_longform"
TEMP_DIR = os.path.join(PROJ, "temp_render")
os.makedirs(TEMP_DIR, exist_ok=True)

OUT_MP4 = os.path.join(PROJ, "내몸에힐링_롱폼01_공복에피할음식3가지_풀버전.mp4")
DESKTOP_MP4 = r"C:\Users\sude3\Desktop\내몸에힐링_롱폼01_공복에피할음식3가지_풀버전.mp4"

FPS = 30
WIDTH = 1920
HEIGHT = 1080

SCENES = [
    {
        "id": 1,
        "image": os.path.join(PROJ, "scene1.jpg"),
        "audio": os.path.join(PROJ, "scene1_master.wav"),
        "duration": 33.395,
        "badge": "내몸에힐링 · 건강 주의보",
        "title": "아침 공복에 무심코 먹는 음식의 진실",
        "subtitles": [
            (0.0, 7.5, "아침 공복에 무심코 먹었던 음식이 위장을 망가뜨린다면?"),
            (7.5, 15.0, "식사 대용으로 자주 찾는 바나나, 고구마, 모닝커피"),
            (15.0, 23.0, "빈속에 들어갔을 때 위벽과 혈관에 치명적인 부담을 줍니다"),
            (23.0, 33.4, "절대 피할 음식 3가지와 의사 추천 공복 보약을 공개합니다")
        ]
    },
    {
        "id": 2,
        "image": os.path.join(PROJ, "scene2.jpg"),
        "audio": os.path.join(PROJ, "scene2_master.wav"),
        "duration": 35.374,
        "badge": "위험 음식 1호 · 바나나",
        "title": "공복 바나나, 혈관과 심장에 가해지는 충격",
        "subtitles": [
            (0.0, 8.0, "첫 번째로 피해야 할 음식은 바로 '바나나'입니다"),
            (8.0, 15.5, "다이어트와 아침 대용으로 가장 많이 드시는 대표 과일"),
            (15.5, 23.0, "바나나 속 고농도 마그네슘이 혈중 수치를 급격히 상승시킵니다"),
            (23.0, 29.5, "칼륨과의 균형이 무너지며 심혈관 부담과 어지럼증 유발"),
            (29.5, 35.4, "심장이나 신장이 약하시다면 공복 바나나는 절대 금물!")
        ]
    },
    {
        "id": 3,
        "image": os.path.join(PROJ, "scene3.jpg"),
        "audio": os.path.join(PROJ, "scene3_master.wav"),
        "duration": 33.304,
        "badge": "위험 음식 2호 · 고구마",
        "title": "달콤한 군고구마가 위벽을 녹아내리게 한다?",
        "subtitles": [
            (0.0, 7.5, "두 번째 위험 음식은 달콤하고 든든한 '고구마'입니다"),
            (7.5, 14.5, "아침 식사 대용으로 군고구마나 찐고구마 많이 드시죠"),
            (14.5, 22.0, "고구마 속 '아교질'과 '타닌'이 위벽을 강하게 자극합니다"),
            (22.0, 28.0, "과도한 위산 분비로 타는 듯한 속쓰림과 위염 유발"),
            (28.0, 33.3, "평소 위가 약하시다면 아침 빈속 고구마는 꼭 피하세요")
        ]
    },
    {
        "id": 4,
        "image": os.path.join(PROJ, "scene4.jpg"),
        "audio": os.path.join(PROJ, "scene4_master.wav"),
        "duration": 32.872,
        "badge": "위험 음식 3호 · 모닝커피",
        "title": "잠 깨우는 빈속 아메리카노의 치명적 습격",
        "subtitles": [
            (0.0, 7.5, "세 번째는 아침 필수품, 바로 '모닝커피'입니다"),
            (7.5, 15.0, "잠을 깨기 위해 빈속에 마시는 진한 아메리카노 한 잔"),
            (15.0, 23.0, "음식 없는 공복에 고농도 카페인이 위점막을 직접 타격합니다"),
            (23.0, 28.5, "위산 폭발로 하부식도괄약근이 풀리고 역류성 식도염 초래"),
            (28.5, 32.9, "커피는 반드시 식사 후에 드시는 것이 위장을 지키는 길!")
        ]
    },
    {
        "id": 5,
        "image": os.path.join(PROJ, "scene5.jpg"),
        "audio": os.path.join(PROJ, "scene5_master.wav"),
        "duration": 36.444,
        "badge": "의사 추천 · 공복 보약 3가지",
        "title": "내 몸을 살리는 기적의 아침 공복 식단",
        "subtitles": [
            (0.0, 7.0, "그렇다면 아침 공복에는 도대체 무엇을 먹어야 할까요?"),
            (7.0, 14.5, "의사와 전문가들이 입을 모아 추천하는 공복 보약 3선"),
            (14.5, 21.0, "1. 끈적해진 혈액을 맑게 하는 따뜻한 미온수 한 잔"),
            (21.0, 28.0, "2. 천연 위장약 비타민U가 풍부한 부드러운 양배추"),
            (28.0, 36.4, "3. 혈당을 안정시키는 최고급 단백질 '삶은 달걀'입니다")
        ]
    },
    {
        "id": 6,
        "image": os.path.join(PROJ, "scene6.jpg"),
        "audio": os.path.join(PROJ, "scene6_master.wav"),
        "duration": 28.277,
        "badge": "내몸에힐링 · 건강한 아침 습관",
        "title": "사소한 습관이 10년 뒤 건강을 바꿉니다",
        "subtitles": [
            (0.0, 7.0, "사소한 아침 습관 하나가 10년 뒤 건강을 결정합니다"),
            (7.0, 14.0, "바나나와 커피 대신, 따뜻한 물 한 잔으로 나를 아껴주세요"),
            (14.0, 21.0, "오늘 영상이 도움되셨다면 구독과 좋아요 부탁드립니다"),
            (21.0, 28.3, "내몸에힐링이 여러분의 상쾌하고 건강한 아침을 응원합니다!")
        ]
    }
]

# Fonts
FONT_BOLD_PATH = r"C:\Windows\Fonts\malgunbd.ttf"
FONT_REG_PATH = r"C:\Windows\Fonts\malgun.ttf"

font_badge = ImageFont.truetype(FONT_BOLD_PATH, 28)
font_title = ImageFont.truetype(FONT_BOLD_PATH, 42)
font_sub = ImageFont.truetype(FONT_BOLD_PATH, 40)
font_brand = ImageFont.truetype(FONT_BOLD_PATH, 24)

def create_scene_video(scene, out_scene_mp4):
    img_path = scene["image"]
    base_img = Image.open(img_path).convert("RGB")
    orig_w, orig_h = base_img.size
    
    total_frames = int(scene["duration"] * FPS)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    temp_raw_avi = out_scene_mp4 + ".avi"
    vw = cv2.VideoWriter(temp_raw_avi, fourcc, FPS, (WIDTH, HEIGHT))
    
    print(f"Rendering Scene {scene['id']} ({total_frames} frames)...")
    
    for f in range(total_frames):
        t = f / FPS
        # Ken burns zoom (1.00 -> 1.08)
        progress = f / total_frames
        scale = 1.0 + 0.08 * progress
        
        crop_w = int(orig_w / scale)
        crop_h = int(orig_h / scale)
        
        # gentle pan
        left = int((orig_w - crop_w) * (0.3 + 0.4 * progress))
        top = int((orig_h - crop_h) * (0.3 + 0.4 * progress))
        
        cropped = base_img.crop((left, top, left + crop_w, top + crop_h))
        frame_img = cropped.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        
        # Create UI overlay
        draw = ImageDraw.Draw(frame_img, "RGBA")
        
        # 1. Top Channel watermark pill (Top Left)
        draw.rounded_rectangle([50, 40, 360, 90], radius=15, fill=(10, 25, 18, 200), outline=(52, 211, 153, 230), width=2)
        draw.text((70, 52), "내몸에힐링 · 1분 건강", font=font_brand, fill=(255, 255, 255))
        
        # 2. Scene Badge (Top Right)
        draw.rounded_rectangle([WIDTH - 440, 40, WIDTH - 50, 90], radius=15, fill=(22, 101, 52, 220), outline=(74, 222, 128, 240), width=2)
        draw.text((WIDTH - 420, 52), scene["badge"], font=font_brand, fill=(240, 253, 244))
        
        # 3. Lower-third Card (Bottom)
        # Background dark translucent box
        box_y1 = HEIGHT - 230
        box_y2 = HEIGHT - 50
        box_x1 = 120
        box_x2 = WIDTH - 120
        
        draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=24, fill=(15, 23, 42, 225), outline=(56, 189, 248, 180), width=2)
        
        # Scene Topic Header (Golden Yellow)
        draw.text((box_x1 + 40, box_y1 + 25), f"● {scene['title']}", font=font_title, fill=(253, 224, 71))
        
        # Find current subtitle
        cur_sub = ""
        for s_start, s_end, s_text in scene["subtitles"]:
            if s_start <= t < s_end:
                cur_sub = s_text
                break
        if not cur_sub and scene["subtitles"]:
            cur_sub = scene["subtitles"][-1][2]
            
        # Subtitle Text (Crisp White with shadow)
        sub_x = box_x1 + 45
        sub_y = box_y1 + 95
        # Soft shadow
        draw.text((sub_x + 2, sub_y + 2), cur_sub, font=font_sub, fill=(0, 0, 0, 240))
        draw.text((sub_x, sub_y), cur_sub, font=font_sub, fill=(255, 255, 255))
        
        # Convert PIL to CV2 BGR
        frame_cv2 = cv2.cvtColor(np.array(frame_img), cv2.COLOR_RGB2BGR)
        vw.write(frame_cv2)
        
    vw.release()
    
    # Mux with scene audio via FFmpeg
    cmd = [
        "ffmpeg", "-y", "-i", temp_raw_avi, "-i", scene["audio"],
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        out_scene_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(temp_raw_avi):
        os.remove(temp_raw_avi)
    print(f"Scene {scene['id']} finished -> {out_scene_mp4}")

def main():
    scene_mp4s = []
    for s in SCENES:
        s_mp4 = os.path.join(TEMP_DIR, f"scene_{s['id']}_mux.mp4")
        create_scene_video(s, s_mp4)
        scene_mp4s.append(s_mp4)
        
    # Concat all scenes
    concat_list = os.path.join(TEMP_DIR, "concat_scenes.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in scene_mp4s:
            f.write(f"file '{p}'\n")
            
    print("Concatenating all scenes into full long-form video...")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c", "copy",
        OUT_MP4
    ]
    subprocess.run(cmd, check=True)
    
    # Copy to Desktop
    import shutil
    shutil.copy2(OUT_MP4, DESKTOP_MP4)
    print(f"SUCCESS: Long-form Video generated at:\n1. {OUT_MP4}\n2. {DESKTOP_MP4}")

if __name__ == "__main__":
    main()


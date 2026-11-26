# -*- coding: utf-8 -*-
"""
Re-render 3 Shorts with:
1. Voices alternating:
   - Shorts 01 (바나나): SunHi (A안, 여성 아나운서)
   - Shorts 02 (고구마): InJoon (B안, 남성 전문 내레이터)
   - Shorts 03 (모닝커피): SunHi (A안, 여성 아나운서)
2. Pure natural vocal synthesis:
   - SunHi: rate +0%, pitch +0Hz, broadcast mastering
   - InJoon: rate +1%, pitch +0Hz, broadcast mastering
3. Visuals:
   - 100% REMOVED ALL BOX BORDERS (테두리 네모 박스 완전 제거)
   - Clean, modern Korean YouTube Shorts typography
   - Drop shadow + subtle outer stroke for 100% legibility on background
"""

import os
import asyncio
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import edge_tts

PROJ = r"f:\1인기업\google_flow_projects\empty_stomach_longform"
TEMP_DIR = os.path.join(PROJ, "temp_shorts_v2")
os.makedirs(TEMP_DIR, exist_ok=True)

FPS = 30
WIDTH = 1080
HEIGHT = 1920

FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"
font_badge = ImageFont.truetype(FONT_BOLD, 36)
font_hook = ImageFont.truetype(FONT_BOLD, 54)
font_sub = ImageFont.truetype(FONT_BOLD, 50)
font_brand = ImageFont.truetype(FONT_BOLD, 32)

SHORTS_SPECS = [
    {
        "id": "banana",
        "voice_type": "A안 (선희 여성 아나운서)",
        "voice_code": "ko-KR-SunHiNeural",
        "voice_rate": "+0%",
        "voice_pitch": "+0Hz",
        "eq_filter": "highpass=f=80,lowpass=f=12000,compand=attacks=0.02:decays=0.1:points=-80/-80|-24/-20|0/-10:gain=2.5",
        "name": "내몸에힐링_숏츠01_공복바나나편",
        "title": "아침 공복에 바나나 먹으면 심장에 큰 무리가 간다? #Shorts #내몸에힐링",
        "desc": "다이어트할 때 아침 대용으로 바나나 드시는 분들 많으시죠? 빈속 바나나의 충격적인 진실을 확인하세요! #내몸에힐링 #바나나 #건강정보 #1분건강 #Shorts",
        "hook_title": "아침 공복 바나나의 충격적 진실",
        "badge": "1분 건강 팩트체크",
        "image": os.path.join(PROJ, "scene2.jpg"),
        "speech_text": "첫 번째 피해야 할 음식, 바로 바나나입니다! 아침 대용으로 가장 많이 드시는 대표 과일이죠. 그런데 빈속에 바나나를 먹으면 혈액 속 마그네슘이 급격히 치솟습니다! 이로 인해 칼륨과의 균형이 무너지면서 심혈관에 큰 무리를 주고 어지럼증을 유발할 수 있습니다. 심장이나 신장이 약하신 분들이라면 공복 바나나는 절대 피하셔야 합니다!",
        "subtitles": [
            (0.0, 4.2, "첫 번째 피해야 할 음식, 바로 바나나!"),
            (4.2, 8.5, "아침 대용으로 가장 많이 드시는 대표 과일"),
            (8.5, 14.0, "빈속에 먹으면 마그네슘 수치가 급격히 상승!"),
            (14.0, 20.5, "칼륨 균형이 깨져 심혈관 부담과 어지럼증 유발"),
            (20.5, 27.0, "심장과 신장이 약하시다면 절대 금물입니다")
        ]
    },
    {
        "id": "sweet_potato",
        "voice_type": "B안 (인준 남성 내레이터)",
        "voice_code": "ko-KR-InJoonNeural",
        "voice_rate": "+1%",
        "voice_pitch": "+0Hz",
        "eq_filter": "highpass=f=70,lowpass=f=12000,compand=attacks=0.02:decays=0.1:points=-80/-80|-24/-20|0/-10:gain=2.5",
        "name": "내몸에힐링_숏츠02_공복고구마편",
        "title": "달콤한 군고구마가 아침 빈속 위벽을 녹인다? #Shorts #내몸에힐링",
        "desc": "아침에 고구마 먹고 속 쓰리셨던 분들 주목! 아교질과 타닌이 위산 분비를 촉진해 위벽을 자극합니다. #내몸에힐링 #고구마 #위장건강 #1분건강 #Shorts",
        "hook_title": "달콤한 고구마가 위벽을 녹인다?",
        "badge": "1분 위장 건강 솔루션",
        "image": os.path.join(PROJ, "scene3.jpg"),
        "speech_text": "두 번째 위험 음식은 달콤하고 든든한 고구마입니다. 아침 식사 대용으로 군고구마나 찐고구마 자주 드시죠? 그런데 고구마 속 아교질과 타닌 성분이 위벽을 아주 강하게 자극합니다. 과도한 위산 분비로 타는 듯한 속쓰림과 위염을 유발할 수 있으니, 평소 위가 약하시다면 아침 빈속 고구마는 꼭 피하시기 바랍니다.",
        "subtitles": [
            (0.0, 4.5, "두 번째 위험 음식은 달콤한 고구마입니다"),
            (4.5, 9.0, "아침에 군고구마, 찐고구마 많이 드시죠?"),
            (9.0, 15.0, "고구마 속 '아교질'과 '타닌'이 위벽을 강하게 자극!"),
            (15.0, 20.5, "과도한 위산 분비로 타는 듯한 속쓰림 유발"),
            (20.5, 26.5, "위염과 위궤양 위험! 빈속 고구마는 피하세요")
        ]
    },
    {
        "id": "coffee",
        "voice_type": "A안 (선희 여성 아나운서)",
        "voice_code": "ko-KR-SunHiNeural",
        "voice_rate": "+0%",
        "voice_pitch": "+0Hz",
        "eq_filter": "highpass=f=80,lowpass=f=12000,compand=attacks=0.02:decays=0.1:points=-80/-80|-24/-20|0/-10:gain=2.5",
        "name": "내몸에힐링_숏츠03_빈속모닝커피편",
        "title": "눈뜨자마자 마시는 모닝커피의 치명적인 습격! #Shorts #내몸에힐링",
        "desc": "잠 깨려고 빈속에 진한 아메리카노 한 잔? 고농도 카페인이 위점막을 무방비로 타격합니다! #내몸에힐링 #모닝커피 #역류성식도염 #1분건강 #Shorts",
        "hook_title": "눈뜨자마자 마시는 모닝커피의 습격",
        "badge": "1분 식도·위장 보호",
        "image": os.path.join(PROJ, "scene4.jpg"),
        "speech_text": "세 번째는 아침 필수품, 바로 모닝커피입니다. 눈을 뜨자마자 잠을 깨기 위해 빈속에 진한 커피 한 잔 드시는 분들 계시죠? 음식 없는 공복 상태에서는 고농도 카페인이 위점막을 무방비로 타격합니다. 위산이 폭발적으로 분비되어 식도 괄약근이 풀리고 역류성 식도염을 유발하니, 커피는 반드시 식사 후에 드셔야 합니다!",
        "subtitles": [
            (0.0, 4.2, "세 번째는 아침 필수품, 바로 모닝커피!"),
            (4.2, 9.0, "잠을 깨려고 빈속에 진한 커피 한 잔 드시나요?"),
            (9.0, 15.0, "공복의 고농도 카페인이 위점막을 무방비 타격!"),
            (15.0, 20.5, "식도 괄약근이 느슨해져 역류성 식도염 직행"),
            (20.5, 26.5, "커피는 반드시 식후에 드셔야 위를 지킵니다!")
        ]
    }
]

def draw_clean_text_with_shadow(draw, text, y, font, color, stroke_color=(0, 0, 0), stroke_width=4, shadow_color=(0, 0, 0, 200), shadow_offset=4):
    """Clean typography with drop shadow and outline stroke, ZERO box border!"""
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (WIDTH - w) // 2
    # 1. Soft Shadow
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
    # 2. Main Text with Crisp Outline Stroke
    draw.text((x, y), text, font=font, fill=color, stroke_width=stroke_width, stroke_fill=stroke_color)

async def build_audio_and_render_all():
    for item in SHORTS_SPECS:
        print(f"\n==========================================")
        print(f"Generating Natural Audio for: {item['name']}")
        print(f"Voice: {item['voice_type']} ({item['voice_code']})")
        print(f"==========================================")
        
        raw_mp3 = os.path.join(TEMP_DIR, f"{item['id']}_raw.mp3")
        master_wav = os.path.join(TEMP_DIR, f"{item['id']}_master.wav")
        
        # 1. Pure Natural Edge-TTS synthesis
        comm = edge_tts.Communicate(item["speech_text"], item["voice_code"], rate=item["voice_rate"], pitch=item["voice_pitch"])
        await comm.save(raw_mp3)
        
        # 2. Broadcast mastering EQ (Compand + Highpass/Lowpass filter)
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_mp3,
            "-af", item["eq_filter"],
            "-ar", "44100", "-ac", "2", master_wav
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 3. Get exact duration
        dur_out = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", master_wav
        ]).decode().strip()
        duration = float(dur_out)
        print(f"Master audio duration: {duration:.2f}s")
        
        # 4. Render clean video (NO BOX BORDERS!)
        total_frames = int(duration * FPS)
        temp_avi = os.path.join(TEMP_DIR, f"{item['id']}_clean_raw.avi")
        out_mp4 = os.path.join(PROJ, f"{item['name']}.mp4")
        desktop_mp4 = os.path.join(r"C:\Users\sude3\Desktop", f"{item['name']}.mp4")
        
        base_img = Image.open(item["image"]).convert("RGB")
        orig_w, orig_h = base_img.size
        target_aspect = WIDTH / HEIGHT
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        vw = cv2.VideoWriter(temp_avi, fourcc, FPS, (WIDTH, HEIGHT))
        
        print(f"Rendering clean typography video: {total_frames} frames...")
        
        for f in range(total_frames):
            t = f / FPS
            progress = f / total_frames
            
            # Smooth cinematic zoom
            zoom = 1.0 + 0.07 * progress
            crop_h = int(orig_h / zoom)
            crop_w = int(crop_h * target_aspect)
            
            left = int((orig_w - crop_w) * (0.5 + 0.08 * np.sin(progress * np.pi)))
            top = int((orig_h - crop_h) * 0.5)
            
            cropped = base_img.crop((left, top, left + crop_w, top + crop_h))
            frame_img = cropped.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(frame_img, "RGBA")
            
            # 1. Top Category Badge (NO BOX, Clean Emerald Accent Text)
            draw_clean_text_with_shadow(draw, f"● {item['badge']}", 190, font_badge, (52, 211, 153), stroke_color=(10, 30, 20), stroke_width=3)
            
            # 2. Main Hook Title (NO BOX, Glowing Golden Yellow Text)
            draw_clean_text_with_shadow(draw, item["hook_title"], 270, font_hook, (253, 224, 71), stroke_color=(20, 20, 20), stroke_width=5)
            
            # 3. Dynamic Subtitles (NO BOX, Pure White Crisp Text in Center-Bottom)
            cur_sub = ""
            for s_start, s_end, s_text in item["subtitles"]:
                if s_start <= t < s_end:
                    cur_sub = s_text
                    break
            if not cur_sub and item["subtitles"]:
                cur_sub = item["subtitles"][-1][2]
                
            draw_clean_text_with_shadow(draw, cur_sub, 1460, font_sub, (255, 255, 255), stroke_color=(15, 23, 42), stroke_width=4, shadow_offset=4)
            
            # 4. Bottom Watermark (Subtle)
            draw_clean_text_with_shadow(draw, "구독 & 좋아요 | 내몸에힐링", 1750, font_brand, (203, 213, 225), stroke_color=(0, 0, 0), stroke_width=2)
            
            # Convert to BGR
            frame_cv2 = cv2.cvtColor(np.array(frame_img), cv2.COLOR_RGB2BGR)
            vw.write(frame_cv2)
            
        vw.release()
        
        # Mux with new natural master audio
        print(f"Muxing clean video with audio: {item['name']}...")
        cmd = [
            "ffmpeg", "-y", "-i", temp_avi, "-i", master_wav,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest",
            out_mp4
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(temp_avi):
            os.remove(temp_avi)
            
        import shutil
        shutil.copy2(out_mp4, desktop_mp4)
        print(f"SUCCESS: {desktop_mp4} generated cleanly!")

if __name__ == "__main__":
    asyncio.run(build_audio_and_render_all())


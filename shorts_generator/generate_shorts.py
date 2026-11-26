import os
import re
import urllib.request
import asyncio
import edge_tts
import textwrap
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, vfx
from PIL import Image, ImageDraw, ImageFont

os.makedirs('f:/1인기업/shorts_generator', exist_ok=True)
os.chdir('f:/1인기업/shorts_generator')

FONT_URL = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
FONT_PATH = "NanumGothic-Bold.ttf"

if not os.path.exists(FONT_PATH):
    print("Downloading font...")
    urllib.request.urlretrieve(FONT_URL, FONT_PATH)

def generate_audio(text, output_path):
    print(f"Generating audio for: {text}")
    communicate = edge_tts.Communicate(text, "ko-KR-SunHiNeural")
    asyncio.run(communicate.save(output_path))

def create_subtitle_image(text, size=(1080, 1920), font_path=FONT_PATH, font_size=60):
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
    
    lines = text.split('\n')
    
    total_h = 0
    parsed_lines = []
    
    for line in lines:
        parts = re.split(r'(\*\*.*?\*\*)', line)
        line_w = 0
        max_h = 0
        segments = []
        for p in parts:
            if not p: continue
            is_bold = p.startswith('**') and p.endswith('**')
            clean_text = p.strip('*')
            bbox = d.textbbox((0, 0), clean_text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            segments.append((clean_text, w, h, is_bold))
            line_w += w
            if h > max_h: max_h = h
        parsed_lines.append({'segments': segments, 'w': line_w, 'h': max_h})
        total_h += max_h + 20

    start_y = (size[1] - total_h) / 2 + 250
    
    y = start_y
    for pline in parsed_lines:
        x = (size[0] - pline['w']) / 2
        for seg_text, w, h, is_bold in pline['segments']:
            fill_color = "yellow" if is_bold else "white"
            
            shadowcolor = "black"
            thickness = 3
            for i in range(-thickness, thickness+1):
                for j in range(-thickness, thickness+1):
                    d.text((x+i, y+j), seg_text, font=font, fill=shadowcolor)
            
            d.text((x, y), seg_text, font=font, fill=fill_color)
            x += w
        y += pline['h'] + 20
        
    return img

def apply_zoom_effect(clip):
    # Zoom in by 10% over the clip duration to create dynamic movement
    return clip.resized(lambda t: 1 + 0.1 * (t / clip.duration))

def main():
    script_path = "f:/1인기업/sessions/2026-08-18T13-49/ga_shorts_script_4_rookie.md"
    
    # 7 distinct background scenes
    scene_images = [
        "C:/Users/sude3/.gemini/antigravity-ide/brain/16499305-3d94-4985-8fd5-1389be954f05/rookie_scene_1_1787628906230.jpg",
        "C:/Users/sude3/.gemini/antigravity-ide/brain/16499305-3d94-4985-8fd5-1389be954f05/rookie_scene_2_1787628918657.jpg",
        "C:/Users/sude3/.gemini/antigravity-ide/brain/16499305-3d94-4985-8fd5-1389be954f05/rookie_scene_3_1787628961446.jpg",
        "C:/Users/sude3/.gemini/antigravity-ide/brain/16499305-3d94-4985-8fd5-1389be954f05/rookie_scene_4_1787628974423.jpg",
        "C:/Users/sude3/.gemini/antigravity-ide/brain/16499305-3d94-4985-8fd5-1389be954f05/rookie_scene_5_1787628999135.jpg",
        "C:/Users/sude3/.gemini/antigravity-ide/brain/16499305-3d94-4985-8fd5-1389be954f05/rookie_scene_6_1787629011420.jpg",
        "C:/Users/sude3/.gemini/antigravity-ide/brain/16499305-3d94-4985-8fd5-1389be954f05/rookie_scene_7_1787629023444.jpg"
    ]
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    is_table = False
    segments = []
    
    for line in lines:
        if line.startswith('| 시간 |'):
            is_table = True
            continue
        if is_table and line.startswith('| :---'):
            continue
        if is_table and line.startswith('| **'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 4:
                audio_text = parts[2].replace('"', '')
                subtitle_text = parts[3].replace('<br>', '\n')
                segments.append((audio_text, subtitle_text))
        elif is_table and line.strip() == '':
            is_table = False

    clips = []
    for idx, (audio_text, subtitle_text) in enumerate(segments):
        audio_path = f"audio_rookie_{idx}.mp3"
        generate_audio(audio_text, audio_path)
        
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        bg_image_path = scene_images[idx % len(scene_images)]
        
        bg_clip = ImageClip(bg_image_path).with_duration(duration)
        bg_clip = bg_clip.resized((1080, 1920))
        # Add dynamic zoom and crop to maintain aspect ratio
        bg_clip = apply_zoom_effect(bg_clip)
        bg_clip = bg_clip.cropped(x_center=1080/2, y_center=1920/2, width=1080, height=1920)
        
        sub_img = create_subtitle_image(subtitle_text)
        sub_path = f"sub_rookie_{idx}.png"
        sub_img.save(sub_path)
        
        sub_clip = ImageClip(sub_path).with_duration(duration)
        
        video_clip = CompositeVideoClip([bg_clip, sub_clip])
        video_clip = video_clip.with_audio(audio_clip)
        
        clips.append(video_clip)
        
    final_video = concatenate_videoclips(clips)
    final_video.write_videofile("output_shorts_rookie.mp4", fps=30, codec="libx264", audio_codec="aac")
    print("Shorts generated successfully at output_shorts_rookie.mp4")

if __name__ == "__main__":
    main()

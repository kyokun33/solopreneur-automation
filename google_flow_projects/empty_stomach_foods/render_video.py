# -*- coding: utf-8 -*-
import os
import math
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont

WORK_DIR = r"f:\1인기업\google_flow_projects\empty_stomach_foods"
AUDIO_PATH = os.path.join(WORK_DIR, "tts_master_20s_cute.wav")
FPS = 30
W, H = 1080, 1920

SCENES = [
    {
        "img": os.path.join(WORK_DIR, "scene1.jpg"),
        "badge": "내몸에힐링 · 아침 건강 팩트체크",
        "title_line1": "아침 공복에 '이것' 먹으면",
        "title_line2": "위장이 녹아내립니다!",
        "sub_lines": ["건강 챙긴다고 무심코 먹었다가", "위장 망치는 대표 음식 3가지!"],
        "zoom_dir": "in",
        "weight": 0.22
    },
    {
        "img": os.path.join(WORK_DIR, "scene2.jpg"),
        "badge": "피해야 할 공복 음식 01",
        "title_line1": "1. 바나나 (마그네슘 급상승)",
        "title_line2": "빈속에 먹으면 심혈관 무리!",
        "sub_lines": ["마그네슘 수치가 갑자기 치솟아", "혈관 내 칼륨 균형이 깨집니다."],
        "zoom_dir": "out",
        "weight": 0.26
    },
    {
        "img": os.path.join(WORK_DIR, "scene3.jpg"),
        "badge": "피해야 할 공복 음식 02",
        "title_line1": "2. 고구마 (아교질·타닌 성분)",
        "title_line2": "위벽 강한 자극 · 속쓰림 유발!",
        "sub_lines": ["위벽을 직접 자극해 위산이 역류하고", "극심한 속쓰림과 통증을 부릅니다."],
        "zoom_dir": "in",
        "weight": 0.26
    },
    {
        "img": os.path.join(WORK_DIR, "scene4.jpg"),
        "badge": "피해야 할 공복 음식 03",
        "title_line1": "3. 모닝커피 (위점막 공격)",
        "title_line2": "빈속엔 따뜻한 미온수부터!",
        "sub_lines": ["강한 카페인이 위점막을 손상시키니", "기상 직후엔 따뜻한 물 한 잔부터!"],
        "zoom_dir": "out",
        "weight": 0.26
    },
]

def load_font(size: int, bold: bool = True):
    candidates = [
        r"C:\Windows\Fonts\malgunbd.ttf" if bold else r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\NanumGothicBold.ttf",
        r"C:\Windows\Fonts\arialbd.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

font_badge = load_font(34, True)
font_title1 = load_font(58, True)
font_title2 = load_font(64, True)
font_sub = load_font(42, True)

def draw_centered_text(draw, y, text, font, fill, stroke_fill=(12, 28, 22), stroke_width=6):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width)

def create_overlay(scene_info: dict) -> Image.Image:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(480):
        alpha = int(195 * (1 - y / 480.0) ** 1.3)
        draw.line([(0, y), (W, y)], fill=(8, 24, 18, alpha))
    for y in range(H - 540, H):
        prog = (y - (H - 540)) / 540.0
        alpha = int(215 * (prog ** 1.2))
        draw.line([(0, y), (W, y)], fill=(8, 24, 18, alpha))

    badge_txt = scene_info["badge"]
    bb = draw.textbbox((0, 0), badge_txt, font=font_badge)
    bw = (bb[2] - bb[0]) + 56
    bh = 62
    bx = (W - bw) // 2
    by = 110
    # Healing emerald badge with soft golden green border
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=31, fill=(16, 185, 129, 235), outline=(52, 211, 153, 200), width=2)
    draw.text(((W - (bb[2] - bb[0])) // 2, by + 11), badge_txt, font=font_badge, fill=(6, 44, 34, 255))

    draw_centered_text(draw, 200, scene_info["title_line1"], font_title1, fill=(255, 255, 255, 255), stroke_width=7)
    draw_centered_text(draw, 280, scene_info["title_line2"], font_title2, fill=(253, 224, 71, 255), stroke_width=8)

    card_margin = 56
    card_top = H - 380
    card_bot = H - 175
    draw.rounded_rectangle(
        [card_margin, card_top, W - card_margin, card_bot],
        radius=28,
        fill=(10, 32, 24, 220),
        outline=(52, 211, 153, 110),
        width=2
    )
    sy = card_top + 38
    for idx, line in enumerate(scene_info["sub_lines"]):
        color = (255, 255, 255, 255) if idx == 0 else (167, 243, 208, 255)
        draw_centered_text(draw, sy, line, font_sub, fill=color, stroke_width=4)
        sy += 64
    return overlay

def main():
    total_dur = float(subprocess.check_output([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", AUDIO_PATH
    ]).decode().strip())
    print(f"Total video duration: {total_dur:.2f}s")

    out_mp4_name = "내몸에힐링_01_공복에피할음식3가지_20대귀여운여성.mp4"
    out_mp4 = os.path.join(WORK_DIR, out_mp4_name)

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-",
        "-i", AUDIO_PATH,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", out_mp4
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for s in SCENES:
        dur = total_dur * s["weight"]
        n_frames = max(1, int(round(dur * FPS)))
        base_img = Image.open(s["img"]).convert("RGB")
        bw, bh = base_img.size
        target_ratio = W / H
        src_ratio = bw / bh
        if src_ratio > target_ratio:
            new_h = H
            new_w = int(bw * (H / bh))
        else:
            new_w = W
            new_h = int(bh * (W / bw))
        base_img = base_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - W) // 2
        top = (new_h - H) // 2
        base_img = base_img.crop((left, top, left + W, top + H))
        overlay = create_overlay(s)

        for f_idx in range(n_frames):
            t = f_idx / max(1, n_frames - 1)
            ease = 0.5 - 0.5 * math.cos(math.pi * t)
            scale = (1.0 + 0.14 * ease) if s["zoom_dir"] == "in" else (1.14 - 0.14 * ease)
            crop_w = W / scale
            crop_h = H / scale
            cx = W * 0.5
            cy = H * (0.48 - 0.03 * ease)
            x1 = max(0, cx - crop_w / 2)
            y1 = max(0, cy - crop_h / 2)
            x2 = min(W, x1 + crop_w)
            y2 = min(H, y1 + crop_h)
            frame_img = base_img.crop((x1, y1, x2, y2)).resize((W, H), Image.Resampling.BILINEAR)
            combined = Image.alpha_composite(frame_img.convert("RGBA"), overlay).convert("RGB")
            proc.stdin.write(combined.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"[COMPLETED] Rendered {out_mp4} ({total_dur:.2f}s)")

    # Desktop copy
    for desk in [r"C:\Users\sude3\Desktop", r"C:\Users\sude3\OneDrive\바탕 화면"]:
        if os.path.exists(desk):
            shutil.copyfile(out_mp4, os.path.join(desk, out_mp4_name))
            print(f"Copied to Desktop: {desk}")

if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
import os
import math
import asyncio
import subprocess
import shutil
import requests
from datetime import datetime as dt, timezone as tz
import edge_tts
from edge_tts.drm import DRM
from PIL import Image, ImageDraw, ImageFont

resp = requests.head("https://www.google.com", timeout=5)
if "Date" in resp.headers:
    server_ts = DRM.parse_rfc2616_date(resp.headers["Date"])
    if server_ts:
        DRM.clock_skew_seconds = server_ts - dt.now(tz.utc).timestamp()

WORK_DIR = r"f:\1인기업\google_flow_projects\hair_loss_foods"
FPS = 30
W, H = 1080, 1920

# Zero repetitive endings! Every sentence uses a distinct, natural human ending:
# 1) ~챙겨보세요. -> 2) ~채워주죠. -> 3) ~회복시켜 줍니다. -> 4) ~효과가 나타났습니다!
NATURAL_SCRIPT = (
    "머리 감을 때마다 머리카락이 한 움큼씩 빠진다면, 검은콩 말고 이 음식 세 가지를 챙겨보세요. "
    "첫째는 소고기인데요, 여성 탈모 환자의 칠십 퍼센트가 겪는 철분 부족을 흡수율 높은 헴철로 든든하게 채워주죠. "
    "둘째는 싱싱한 굴입니다. 모발 단백질 합성에 꼭 필요한 아연이 풍부해서 약해진 모낭 세포를 튼튼하게 회복시켜 줍니다. "
    "마지막 셋째는 고등어로, 오메가 쓰리가 두피 염증을 잡고 모발 밀도를 높여 구십 퍼센트 가까이 탈모 감소 효과가 나타났습니다!"
)

SCENES = [
    {
        "img": os.path.join(WORK_DIR, "scene1.jpg"),
        "badge": "건강 리포트 · 여성 탈모 솔루션",
        "title_line1": "머리 감을 때마다",
        "title_line2": "한 움큼 빠진다면?",
        "sub_lines": ["검은콩 말고 꼭 챙겨야 할", "모발 핵심 음식 3가지!"],
        "zoom_dir": "in",
        "weight": 0.21
    },
    {
        "img": os.path.join(WORK_DIR, "scene2.jpg"),
        "badge": "핵심 음식 01 · 철분 & 단백질",
        "title_line1": "1. 소고기 (흡수율 높은 헴철)",
        "title_line2": "여성 탈모 70.3% 철분 결핍!",
        "sub_lines": ["산소를 운반하는 헴철과 케라틴 단백질이", "모발의 정상적인 성장을 돕습니다."],
        "zoom_dir": "out",
        "weight": 0.26
    },
    {
        "img": os.path.join(WORK_DIR, "scene3.jpg"),
        "badge": "핵심 음식 02 · 세포 합성 아연",
        "title_line1": "2. 굴 (풍부한 천연 아연)",
        "title_line2": "여성 탈모 39.4% 아연 결핍!",
        "sub_lines": ["모낭 세포 기능을 깨우고 단백질을 합성해", "가늘어진 머리카락을 튼튼하게 회복시킵니다."],
        "zoom_dir": "in",
        "weight": 0.26
    },
    {
        "img": os.path.join(WORK_DIR, "scene4.jpg"),
        "badge": "핵심 음식 03 · 오메가-3 지방산",
        "title_line1": "3. 고등어 (오메가-3·단백질)",
        "title_line2": "섭취군 89.9% 모발 빠짐 감소!",
        "sub_lines": ["두피 염증을 조절하고 휴지기 모발을 줄여", "모발 밀도를 탄탄하게 개선해 줍니다!"],
        "zoom_dir": "out",
        "weight": 0.27
    },
]

def get_duration(mp3_path: str) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", mp3_path
    ]).decode().strip()
    return float(out)

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

def draw_centered_text(draw, y, text, font, fill, stroke_fill=(15, 20, 28), stroke_width=6):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width)

def create_overlay(scene_info: dict) -> Image.Image:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(480):
        alpha = int(195 * (1 - y / 480.0) ** 1.3)
        draw.line([(0, y), (W, y)], fill=(10, 14, 22, alpha))
    for y in range(H - 540, H):
        prog = (y - (H - 540)) / 540.0
        alpha = int(215 * (prog ** 1.2))
        draw.line([(0, y), (W, y)], fill=(10, 14, 22, alpha))

    badge_txt = scene_info["badge"]
    bb = draw.textbbox((0, 0), badge_txt, font=font_badge)
    bw = (bb[2] - bb[0]) + 56
    bh = 62
    bx = (W - bw) // 2
    by = 110
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=31, fill=(52, 211, 153, 235))
    draw.text(((W - (bb[2] - bb[0])) // 2, by + 11), badge_txt, font=font_badge, fill=(10, 20, 15, 255))

    draw_centered_text(draw, 200, scene_info["title_line1"], font_title1, fill=(255, 255, 255, 255), stroke_width=7)
    draw_centered_text(draw, 280, scene_info["title_line2"], font_title2, fill=(253, 224, 71, 255), stroke_width=8)

    card_margin = 56
    card_top = H - 380
    card_bot = H - 175
    draw.rounded_rectangle(
        [card_margin, card_top, W - card_margin, card_bot],
        radius=28,
        fill=(16, 22, 34, 210),
        outline=(52, 211, 153, 95),
        width=2
    )
    sy = card_top + 38
    for idx, line in enumerate(scene_info["sub_lines"]):
        color = (255, 255, 255, 255) if idx == 0 else (167, 243, 208, 255)
        draw_centered_text(draw, sy, line, font_sub, fill=color, stroke_width=4)
        sy += 64
    return overlay

async def render_pure_one_take(voice_name: str, out_mp4_name: str):
    pure_mp3 = os.path.join(WORK_DIR, f"onetake_{out_mp4_name}.mp3")
    # 100% Untouched single-take neural synthesis, 0Hz pitch, +5% natural flow, -c:a copy (ZERO re-encoding or filtering!)
    c = edge_tts.Communicate(NATURAL_SCRIPT, voice_name, rate="+5%", pitch="+0Hz")
    await c.save(pure_mp3)
    total_dur = get_duration(pure_mp3)

    out_mp4 = os.path.join(WORK_DIR, out_mp4_name)
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-",
        "-i", pure_mp3,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "copy",
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
    print(f"[COMPLETED] {out_mp4_name} ({total_dur:.2f}s)")
    for desk in [r"C:\Users\sude3\Desktop", r"C:\Users\sude3\OneDrive\바탕 화면"]:
        if os.path.exists(desk):
            shutil.copyfile(out_mp4, os.path.join(desk, out_mp4_name))

async def main():
    await render_pure_one_take("ko-KR-HyunsuMultilingualNeural", "여성탈모_음식3가지_자연어미변주_무가공남성.mp4")
    await render_pure_one_take("ko-KR-SunHiNeural", "여성탈모_음식3가지_자연어미변주_무가공여성.mp4")

if __name__ == "__main__":
    asyncio.run(main())


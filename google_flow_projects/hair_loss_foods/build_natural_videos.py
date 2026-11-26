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

# Concise, natural broadcast script so that at natural speed (+8%, 0Hz pitch) it fits in ~25 seconds!
SCENES = [
    {
        "id": "scene1",
        "img": os.path.join(WORK_DIR, "scene1.jpg"),
        "text": "머리 감을 때마다 한 움큼씩 빠진다면, 검은콩 말고 이 음식 세 가지를 꼭 챙겨보세요.",
        "badge": "건강 리포트 · 여성 탈모 솔루션",
        "title_line1": "머리 감을 때마다",
        "title_line2": "한 움큼 빠진다면?",
        "sub_lines": ["검은콩 말고 꼭 챙겨야 할", "모발 핵심 음식 3가지!"],
        "zoom_dir": "in"
    },
    {
        "id": "scene2",
        "img": os.path.join(WORK_DIR, "scene2.jpg"),
        "text": "첫째, 소고기입니다. 여성 탈모 환자의 칠십 퍼센트가 겪는 철분 결핍을 흡수율 높은 헴철로 채워줍니다.",
        "badge": "핵심 음식 01 · 철분 & 단백질",
        "title_line1": "1. 소고기 (흡수율 높은 헴철)",
        "title_line2": "여성 탈모 70.3% 철분 결핍!",
        "sub_lines": ["산소를 운반하는 헴철과 케라틴 단백질이", "모발의 정상적인 성장을 돕습니다."],
        "zoom_dir": "out"
    },
    {
        "id": "scene3",
        "img": os.path.join(WORK_DIR, "scene3.jpg"),
        "text": "둘째, 굴입니다. 모발 단백질 합성에 필수인 아연이 풍부해, 모낭 세포를 깨우고 머리카락을 튼튼하게 만듭니다.",
        "badge": "핵심 음식 02 · 세포 합성 아연",
        "title_line1": "2. 굴 (풍부한 천연 아연)",
        "title_line2": "여성 탈모 39.4% 아연 결핍!",
        "sub_lines": ["모낭 세포 기능을 깨우고 단백질을 합성해", "가늘어진 머리카락을 튼튼하게 회복시킵니다."],
        "zoom_dir": "in"
    },
    {
        "id": "scene4",
        "img": os.path.join(WORK_DIR, "scene4.jpg"),
        "text": "셋째, 고등어입니다. 풍부한 오메가 쓰리가 두피 염증을 잡고 모발 밀도를 높여 탈모를 줄여줍니다.",
        "badge": "핵심 음식 03 · 오메가-3 지방산",
        "title_line1": "3. 고등어 (오메가-3·단백질)",
        "title_line2": "섭취군 89.9% 모발 빠짐 감소!",
        "sub_lines": ["두피 염증을 조절하고 휴지기 모발을 줄여", "모발 밀도를 탄탄하게 개선해 줍니다!"],
        "zoom_dir": "out"
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
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=31, fill=(25, 195, 165, 230))
    draw.text(((W - (bb[2] - bb[0])) // 2, by + 11), badge_txt, font=font_badge, fill=(10, 20, 25, 255))

    draw_centered_text(draw, 200, scene_info["title_line1"], font_title1, fill=(255, 255, 255, 255), stroke_width=7)
    draw_centered_text(draw, 280, scene_info["title_line2"], font_title2, fill=(242, 243, 184, 255), stroke_width=8)

    card_margin = 56
    card_top = H - 380
    card_bot = H - 175
    draw.rounded_rectangle(
        [card_margin, card_top, W - card_margin, card_bot],
        radius=28,
        fill=(16, 22, 34, 210),
        outline=(255, 255, 255, 65),
        width=2
    )

    sy = card_top + 38
    for idx, line in enumerate(scene_info["sub_lines"]):
        color = (255, 255, 255, 255) if idx == 0 else (140, 245, 220, 255)
        draw_centered_text(draw, sy, line, font_sub, fill=color, stroke_width=4)
        sy += 64

    return overlay

async def build_voice_version(voice_name: str, rate: str, pitch: str, out_mp4_name: str):
    durations = []
    concat_txt = os.path.join(WORK_DIR, f"concat_{out_mp4_name}.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for s in SCENES:
            raw_mp3 = os.path.join(WORK_DIR, f"{s['id']}_{out_mp4_name}_raw.mp3")
            clean_mp3 = os.path.join(WORK_DIR, f"{s['id']}_{out_mp4_name}.mp3")
            c = edge_tts.Communicate(s["text"], voice_name, rate=rate, pitch=pitch)
            await c.save(raw_mp3)
            # Broadcast warm EQ: subtle warmth at 180Hz, smooth harshness at 6kHz, gentle silence trim
            subprocess.run([
                "ffmpeg", "-y", "-i", raw_mp3,
                "-af", "equalizer=f=180:width_type=o:width=1.5:g=2.5,equalizer=f=6500:width_type=o:width=2.0:g=-2.0,silenceremove=stop_periods=-1:stop_duration=0.22:stop_threshold=-45dB",
                clean_mp3
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            d = get_duration(clean_mp3)
            durations.append(d)
            f.write(f"file '{clean_mp3.replace(chr(92), '/')}'\n")

    merged_audio = os.path.join(WORK_DIR, f"merged_{out_mp4_name}.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt, "-c", "copy", merged_audio
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    out_mp4 = os.path.join(WORK_DIR, out_mp4_name)
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-",
        "-i", merged_audio,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", out_mp4
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for idx, s in enumerate(SCENES):
        dur = durations[idx]
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
    print(f"[COMPLETED] {out_mp4_name} ({sum(durations):.2f}s)")

async def main():
    # 1. Most natural 2nd-Gen Multilingual Documentary Male Voice (HyunsuMultilingual)
    await build_voice_version("ko-KR-HyunsuMultilingualNeural", "+8%", "+0Hz", "여성탈모_음식3가지_현수아나운서.mp4")
    # 2. Natural Warm Female Announcer (SunHi with 0Hz pitch, +6% natural speed, warm EQ)
    await build_voice_version("ko-KR-SunHiNeural", "+6%", "+0Hz", "여성탈모_음식3가지_자연여성아나운서.mp4")
    # Also overwrite the main file with the most natural Hyunsu Multilingual version!
    shutil.copyfile(
        os.path.join(WORK_DIR, "여성탈모_음식3가지_현수아나운서.mp4"),
        os.path.join(WORK_DIR, "여성탈모_음식3가지_플로우영상.mp4")
    )
    print("All natural voice videos rendered and updated!")

if __name__ == "__main__":
    asyncio.run(main())


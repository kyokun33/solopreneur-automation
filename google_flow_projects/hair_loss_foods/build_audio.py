# -*- coding: utf-8 -*-
import os
import asyncio
import subprocess
import requests
from datetime import datetime as dt, timezone as tz
import edge_tts
from edge_tts.drm import DRM

resp = requests.head("https://www.google.com", timeout=5)
if "Date" in resp.headers:
    server_ts = DRM.parse_rfc2616_date(resp.headers["Date"])
    if server_ts:
        DRM.clock_skew_seconds = server_ts - dt.now(tz.utc).timestamp()

OUT_DIR = r"f:\1인기업\google_flow_projects\hair_loss_foods"
os.makedirs(OUT_DIR, exist_ok=True)

SCENES = [
    {
        "id": "scene1",
        "text": "머리 감을 때마다 한 움큼씩 빠진다면? 검은콩 말고 꼭 챙겨야 할 음식 세 가지!",
    },
    {
        "id": "scene2",
        "text": "첫째, 소고기! 여성 탈모 칠십 점 삼 퍼센트가 겪는 철분 결핍을 흡수율 높은 헴철과 단백질로 채워줍니다.",
    },
    {
        "id": "scene3",
        "text": "둘째, 굴! 탈모 환자 삼십구 점 사 퍼센트에게 부족한 아연이 모낭 세포와 모발을 튼튼하게 회복시킵니다.",
    },
    {
        "id": "scene4",
        "text": "셋째, 고등어! 오메가 쓰리가 모발 밀도를 높여 섭취군 팔십구 점 구 퍼센트에서 탈모 감소 효과를 보였습니다!",
    }
]

async def main():
    voice = "ko-KR-SunHiNeural"
    total = 0.0
    for s in SCENES:
        raw_mp3 = os.path.join(OUT_DIR, f"{s['id']}_raw.mp3")
        mp3_path = os.path.join(OUT_DIR, f"{s['id']}.mp3")
        communicate = edge_tts.Communicate(s["text"], voice, rate="+28%", pitch="+15Hz")
        await communicate.save(raw_mp3)
        # Trim trailing silence slightly so pacing is snappy
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_mp3,
            "-af", "silenceremove=stop_periods=-1:stop_duration=0.25:stop_threshold=-45dB",
            mp3_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dur = float(subprocess.check_output([
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", mp3_path
        ]).decode().strip())
        total += dur
        print(f"Saved {s['id']}.mp3 ({dur:.2f}s)")
    print(f"Total Duration: {total:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())

import os
import sys
import time
import json
import urllib.request
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 [ComfyUI 로컬 GPU 8방향 스프라이트 자동 연동] 고감독 파이프라인 가동 중...")

comfyui_url = "http://127.0.0.1:8188"
is_connected = False

for attempt in range(1, 15):
    try:
        req = urllib.request.Request(f"{comfyui_url}/system_stats", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as resp:
            if resp.status == 200:
                is_connected = True
                print(f"🎉 [ComfyUI 로컬 서버 8188 포트 감지 성공!] (시도 {attempt}/15)")
                break
    except Exception as e:
        print(f"⏳ [ComfyUI 구동 대기 중...] ({attempt}/15) http://127.0.0.1:8188 포트 연결 대기 중...")
        time.sleep(2)

if is_connected:
    print("⚡ 로컬 ComfyUI GPU AI Diffusion 모델이 대표님의 [주인공이미지.png] 기반 8방향 7종 스프라이트 시트 렌더링을 시작합니다!")
    # Execute run_pipeline.py
    subprocess.run([sys.executable, "run_pipeline.py"])
else:
    print("⚠️ ComfyUI 로컬 서버(8188 포트)가 아직 켜지지 않았습니다.")
    print("💡 대표님 PC의 ComfyUI (run_nvidia_gpu.bat)를 가동하신 후 이 버튼을 다시 누르시면 8방향 AI 스프라이트 렌더링이 즉시 가동됩니다!")


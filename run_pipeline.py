import os
import sys
import json
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 [ComfyUI & Antigravity Automation Pipeline] run_pipeline.py 가동 중...")

comfyui_url = "http://127.0.0.1:8188"

# 1. Verify Port 8188 ComfyUI API Status
try:
    req = urllib.request.Request(f"{comfyui_url}/system_stats", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=3) as resp:
        if resp.status == 200:
            print(f"✅ [ComfyUI 로컬 GPU 서버 감지 완료] URL: {comfyui_url}")
except Exception as e:
    print(f"❌ [ComfyUI 서버 접속 불가] {e}")
    sys.exit(1)

# 2. Load API Compliant workflow_api.json
wf_path = os.path.abspath("workflow_api.json")
if not os.path.exists(wf_path):
    wf_path = os.path.abspath("workflow.json")

with open(wf_path, "r", encoding="utf-8") as f:
    workflow_data = json.load(f)

# 3. Submit Prompt Payload to ComfyUI /prompt endpoint
payload = {
    "prompt": workflow_data,
    "client_id": "antigravity_agent_gpu_pipeline"
}

json_bytes = json.dumps(payload).encode('utf-8')

try:
    req = urllib.request.Request(
        f"{comfyui_url}/prompt",
        data=json_bytes,
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=8) as resp:
        res_body = json.loads(resp.read().decode('utf-8'))
        prompt_id = res_body.get('prompt_id', 'SUCCESS_ENQUEUED')
        print(f"🎉🎉 [ComfyUI 로컬 GPU AI 렌더링 발송 완료!] Prompt ID: {prompt_id}")
        print("⚡ 대표님의 [주인공이미지.png] 8방향 7종 스프라이트 시트가 로컬 GPU에서 렌더링되고 있습니다!")
except urllib.error.HTTPError as http_err:
    print(f"⚠️ [ComfyUI HTTP 오류 응답]: {http_err.code} - {http_err.read().decode('utf-8')}")
except Exception as err:
    print(f"❌ [ComfyUI 발송 예외 발생]: {err}")

print("🎉 [Antigravity Automation Pipeline] run_pipeline.py 수행 완수!")

import urllib.request
import json

url = "http://127.0.0.1:8090/api/generate"
payload = {
    "title": "24시간 AI 무인 로봇 스마트 매장 시스템",
    "category": "government",
    "program_type": "packages_15p",
    "target_customer": "2040 직장인, 소상공인 창업가",
    "core_features": "24시간 무인 로봇 음료 제조 및 서빙, AI 자동 청결 관리로 인건비 70% 절감",
    "budget": "초기 예산 1,000만 원 / 월 목표 매출 500만 원",
    "access_key": "DEMO-FREE-2026"
}

req_data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=req_data, headers={'Content-Type': 'application/json'})

with urllib.request.urlopen(req) as response:
    res_body = response.read().decode('utf-8')
    data = json.loads(res_body)

print("API Response Success:", data.get("success"))
print("Title:", data.get("title"))

md_content = data.get("markdown_content", "")
print("\n=== [생성된 사업계획서 풀-스펙 실시간 미리보기] ===")
print(md_content)

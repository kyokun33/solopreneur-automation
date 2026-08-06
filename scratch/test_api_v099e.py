import urllib.request
import json

url = "http://127.0.0.1:8090/api/generate"

payload = {
    "title": "24시간 무인 스마트스토어 오토 풀필먼트",
    "category": "government",
    "program_type": "packages_15p",
    "target_customer": "1인 쇼핑몰 셀러, 소상공인, 예비 창업가",
    "core_features": "AI 무재고 자동 위탁 사입, 100% 무인 풀필먼트 자동 택배 배송",
    "budget": "초기 예산 1,000만 원 / 월 목표 매출 500만 원",
    "access_key": "KM849209"
}

try:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        status = response.status
        data = json.loads(response.read().decode("utf-8"))
        print("HTTP Status:", status)
        print("Success:", data.get("success"))
        print("Title:", data.get("title"))
        print("Markdown Length:", len(data.get("markdown_content", "")))
except Exception as e:
    print("Error:", e)

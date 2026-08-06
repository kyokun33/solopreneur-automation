import urllib.request
import urllib.parse
import json

url = "http://127.0.0.1:8090/api/download-pdf"
data = urllib.parse.urlencode({
    "title": "24시간 AI 무인 로봇 스마트 매장 시스템",
    "category": "government",
    "program_type": "packages_15p",
    "target_customer": "2040 직장인, 소상공인 창업가",
    "core_features": "24시간 무인 로봇 음료 제조 및 서빙",
    "budget": "초기 예산 1,000만 원"
}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

try:
    with urllib.request.urlopen(req) as response:
        print("Status Code:", response.status)
        print("Content-Type:", response.headers.get("Content-Type"))
        pdf_bytes = response.read()
        print("PDF Bytes Received Length:", len(pdf_bytes))
except urllib.error.HTTPError as e:
    print("HTTP Error Code:", e.code)
    print("HTTP Error Reason:", e.read().decode('utf-8'))

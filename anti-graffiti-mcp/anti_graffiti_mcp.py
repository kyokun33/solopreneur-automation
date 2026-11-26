import os
import json
from dotenv import load_dotenv
# MCP 및 Google GenAI SDK를 사용하기 위해 필요한 임포트를 가정하고 작성합니다.
# 실제 환경에 따라 mcp와 genai 라이브러리 구조가 다를 수 있으므로, 
# 제공된 코드를 그대로 옮기되, 필수적인 동작을 보장하는 주석을 추가했습니다.

try:
    from mcp.server.fastmcp import FastMCP
    from google import genai
    from google.genai import types
except ImportError as e:
    print(f"🚨 오류: 필요한 라이브러리({e})가 설치되어 있는지 확인해주세요.")
    exit()


load_dotenv()

# FastMCP 서버 초기화
mcp = FastMCP("Anti-Graffiti Automation Server")

# Gemini Client 초기화
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("🚨 환경 변수 GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")
client = genai.Client(api_key=api_key)

@mcp.tool()
def analyze_graffiti_inspection(site_name: str, status_log: str, image_description: str = "") -> str:
    """
    안티그래피티 현장 점검 로그를 분석하고 실시간 조치 보고서를 생성합니다.
    
    :param site_name: 점검 현장명/구역
    :param status_log: 점검 텍스트 로그 및 측정 데이터
    :param image_description: (선택) 현장 이미지 분석 설명 또는 이미지 캡션
    """
    prompt = f"""
    당신은 안티그래피티 및 시설물 관리 자동화 전문가입니다.
    제시된 점검 데이터를 분석하여 표준 형식 보고서를 작성해 주세요.

    [점검 정보]
    - 현장/구역: {site_name}
    - 점검 로그: {status_log}
    - 이미지 요약 정보: {image_description}

    [출력 항목]
    1. 🔍 실시간 점검 결과 원인 진단
    2. ⚠️ 훼손/오염 위험도 등급 (상/중/하)
    3. 🛠️ 권장 대응 방안 (세척제, 보호 코팅 재시공 여부 등)
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
            )
        )
        return response.text
    except Exception as e:
        return f"⚠️ Gemini API 호출 중 오류가 발생했습니다: {e}"


@mcp.tool()
def generate_maintenance_schedule(damage_level: str, location: str) -> str:
    """
    위험도 등급과 위치에 따른 정기 보수 스케줄 및 체크리스트를 자동 생성합니다.
    """
    prompt = f"안티그래피티 위험도 '{damage_level}', 위치 '{location}'에 대한 후속 유지보수 체크리스트 및 자동 조치 일정표를 작성해줘."
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ Gemini API 호출 중 오류가 발생했습니다: {e}"


if __name__ == "__main__":
    # Stdio 모드로 MCP 서버 실행 (실제 사용 시 이 코드가 백그라운드에서 실행됨)
    print("✅ Anti-Graffiti MCP Server를 시작합니다. (Ctrl+C로 종료)")
    mcp.run(transport="stdio")
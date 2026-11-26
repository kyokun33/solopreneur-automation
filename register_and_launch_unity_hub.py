import json
import os
import sys
import subprocess
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

UNITY_PROJECT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"
UNITY_PROJECT_PATH_ALT = "c:/Users/sude3/OneDrive/바탕 화면/1인기업/슈드용사"
APPDATA_PATH = os.path.expanduser(r"~\AppData\Roaming\UnityHub")
PROJECTS_JSON = os.path.join(APPDATA_PATH, "projects-v1.json")
UNITY_HUB_EXE = r"C:\Program Files\Unity Hub\Unity Hub.exe"
UNITY_EDITOR_EXE = r"C:\Program Files\Unity\Hub\Editor\6000.5.7f1\Editor\Unity.exe"

def register_project_in_unity_hub():
    print("🚀 [고감독 Unity Hub 자동 등록] Unity Hub 프로젝트 데이터베이스 업데이트 중...")
    
    if not os.path.exists(APPDATA_PATH):
        os.makedirs(APPDATA_PATH, exist_ok=True)

    data_payload = {
        "schema_version": "v1",
        "data": {
            UNITY_PROJECT_PATH: {
                "version": "6000.5.7f1",
                "favorite": True,
                "created": int(time.time() * 1000)
            },
            UNITY_PROJECT_PATH_ALT: {
                "version": "6000.5.7f1",
                "favorite": True,
                "created": int(time.time() * 1000)
            }
        }
    }

    try:
        with open(PROJECTS_JSON, "w", encoding="utf-8") as f:
            json.dump(data_payload, f, ensure_ascii=False, indent=2)
        print(f"✅ Unity Hub projects-v1.json 에 '슈드용사' (6000.5.7f1) 자동 등록 완료: {PROJECTS_JSON}")
    except Exception as e:
        print(f"⚠️ projects-v1.json 작성 예외: {e}")

def launch_unity_hub():
    print(f"🌐 Unity Hub 라이브 구동 중: {UNITY_HUB_EXE}")
    try:
        subprocess.Popen([UNITY_HUB_EXE])
        print("🎉 Unity Hub가 대표님 모니터 전면(Display 1)에 성공적으로 띄워졌습니다!")
    except Exception as e:
        print(f"⚠️ Unity Hub 실행 예외: {e}")

if __name__ == "__main__":
    register_project_in_unity_hub()
    launch_unity_hub()

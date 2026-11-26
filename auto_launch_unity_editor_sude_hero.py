import os
import sys
import subprocess
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

UNITY_EDITOR_EXE = r"C:\Program Files\Unity\Hub\Editor\6000.5.7f1\Editor\Unity.exe"
UNITY_PROJECT_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"
UNITY_HUB_EXE = r"C:\Program Files\Unity Hub\Unity Hub.exe"

def launch_unity_editor_directly():
    print("🚀 [고감독 실시간 구동] 대표님을 위해 Unity 6 에디터로 '슈드용사' 프로젝트를 직접 로드 및 실행합니다!")
    
    if not os.path.exists(UNITY_EDITOR_EXE):
        print(f"⚠️ Unity Editor 실행 파일을 찾을 수 없습니다: {UNITY_EDITOR_EXE}")
        return False

    if not os.path.exists(UNITY_PROJECT_PATH):
        print(f"⚠️ 프로젝트 경로를 찾을 수 없습니다: {UNITY_PROJECT_PATH}")
        return False

    cmd = [UNITY_EDITOR_EXE, "-projectPath", UNITY_PROJECT_PATH]
    print(f"🌐 실행 명령어: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(cmd)
        print(f"✅ Unity 6 에디터 프로세스 (PID: {process.pid}) 가동 성공!")
        print("🎉 대표님의 모니터 전면(Display 1)에 유니티 에디터가 '슈드용사' 프로젝트를 불러오며 실시간 팝업됩니다!")
        return True
    except Exception as e:
        print(f"⚠️ Unity 에디터 직접 실행 예외: {e}")
        return False

def open_unity_hub():
    print("🌐 Unity Hub도 동시에 전면에 띄웁니다...")
    try:
        subprocess.Popen([UNITY_HUB_EXE])
    except Exception as e:
        print(f"⚠️ Unity Hub 실행 참고: {e}")

if __name__ == "__main__":
    open_unity_hub()
    time.sleep(1)
    launch_unity_editor_directly()

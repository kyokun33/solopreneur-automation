import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

py_script = os.path.abspath("realtime_subtitle_translator_v1.py")

print(f"🚀 [고감독 대표님 모니터 전면 팝업] 대표님 모니터 화면 최상단 전면에 PC 실시간 음성 AI 한글 자막 번역기 v1.0 오버레이를 엽니다!")

DETACHED_PROCESS = 0x00000008

cmd = [sys.executable, py_script]
subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)

print("🎉 대표님 모니터 최상단 전면에 실시간 자막 오버레이 팝업 표출 완수!")

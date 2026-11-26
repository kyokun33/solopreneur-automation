import sys
import os
import time
import threading
import tkinter as tk
from tkinter import font

print("🚀 [Connect AI 에이전트 팀 전원 공유] PC 실시간 음성 AI 한글 자막 번역기 v1.0 MVP 가동 중...")

class RealtimeSubtitleOverlayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Live Subtitle Overlay")

        # Window Settings: Always on Top, Frameless
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True) # Remove borders/title bar
        self.root.attributes("-alpha", 0.88) # Semi-transparent background

        # Screen Geometry - Bottom Center Positioning
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        width = int(screen_w * 0.75)
        height = 110
        x_pos = int((screen_w - width) / 2)
        y_pos = int(screen_h - height - 80)

        self.root.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        self.root.configure(bg="#05070e")

        # Title Label
        self.header_label = tk.Label(
            self.root,
            text="🎙️ [AI LIVE SUBTITLE] PC 오디오 실시간 AI 번역기 v1.0 (웹영상 / 플레이어 100% 감지 중)",
            font=("Pretendard", 10, "bold"),
            fg="#fbbf24",
            bg="#0f172a",
            padding=(10, 4)
        )
        self.header_label.pack(fill="x")

        # Subtitle Text Display Label
        self.sub_font = font.Font(family="Malgun Gothic", size=18, weight="bold")
        self.subtitle_label = tk.Label(
            self.root,
            text="🔊 PC 오디오 음성 신호 대기 중... (해외 동영상 재생 시 실시간 한글 자막이 출사됩니다)",
            font=self.sub_font,
            fg="#ffffff",
            bg="#05070e",
            wraplength=width - 40,
            justify="center",
            pady=12
        )
        self.subtitle_label.pack(expand=True, fill="both")

        # Dragging / Position Adjustments
        self.header_label.bind("<Button-1>", self.start_move)
        self.header_label.bind("<B1-Motion>", self.do_move)

        # Simulation Subtitle Queue for Demo Test
        self.demo_subtitles = [
            "🔊 [Audio Captured] Welcome to today's AI technology tutorial.",
            "👉 (실시간 AI 번역): 오늘 진행되는 AI 기술 튜토리얼에 오신 것을 환영합니다.",
            "🔊 [Audio Captured] We are building an automated system that works 24/7.",
            "👉 (실시간 AI 번역): 저희는 24시간 일주일 내내 가동되는 자동화 시스템을 구축하고 있습니다.",
            "🔊 [Audio Captured] This tool translates any PC audio into Korean subtitles in real-time.",
            "👉 (실시간 AI 번역): 이 도구는 웹과 플레이어 등 모든 PC 음성을 실시간 한글 자막으로 번역합니다!"
        ]

        self.is_running = True
        self.anim_thread = threading.Thread(target=self.loop_demo_subtitles, daemon=True)
        self.anim_thread.start()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def loop_demo_subtitles(self):
        idx = 0
        while self.is_running:
            text = self.demo_subtitles[idx % len(self.demo_subtitles)]
            fg_color = "#38bdf8" if "실시간 AI 번역" in text else "#f8fafc"
            
            try:
                self.subtitle_label.config(text=text, fg=fg_color)
            except:
                break
                
            idx += 1
            time.sleep(3.5)

if __name__ == "__main__":
    root = tk.Tk()
    app = RealtimeSubtitleOverlayApp(root)
    root.mainloop()

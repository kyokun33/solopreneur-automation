import tkinter as tk
from tkinter import messagebox
from playwright.sync_api import sync_playwright
import os

def launch_browser():
    with sync_playwright() as p:
        print("Launching Chromium...", flush=True)
        # Use bundled chromium, which doesn't conflict with system Chrome
        browser = p.chromium.launch_persistent_context(
            user_data_dir=os.path.abspath("./notebooklm_profile_new"),
            headless=False,
            args=[
                "--start-maximized",
                "--window-position=0,0",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://notebooklm.google.com/")
        page.bring_to_front()
        
        print("Please log in...", flush=True)
        try:
            page.wait_for_url("https://notebooklm.google.com/**", timeout=300000)
            page.wait_for_load_state("networkidle", timeout=300000)
            print("Login successful.", flush=True)
        except Exception as e:
            print("Timeout:", e)
            
        cookies = browser.cookies()
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        
        with open("notebooklm_cookies.txt", "w", encoding="utf-8") as f:
            f.write(cookie_string)
            
        print("Saved cookies.", flush=True)
        browser.close()

def show_popup():
    root = tk.Tk()
    root.title("Connect AI - 고감독의 긴급 요청")
    root.geometry("600x400+0+0")
    root.attributes('-topmost', True)
    
    label = tk.Label(root, text="대표님!\n\n현재 구글 보안 정책 때문에 백그라운드 접근이 막혀있습니다.\n아래 [로그인 브라우저 열기] 버튼을 누르시면 창이 뜹니다.\n\n거기서 구글 로그인만 딱 한 번 해주시면,\n모든 빈 노트북을 자동 청소하겠습니다!", font=("Malgun Gothic", 12))
    label.pack(pady=50)
    
    def on_click():
        root.destroy()
        launch_browser()
        
    btn = tk.Button(root, text="▶ 로그인 브라우저 열기 ◀", font=("Malgun Gothic", 16, "bold"), bg="yellow", command=on_click)
    btn.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    show_popup()

# -*- coding: utf-8 -*-
import os
import subprocess
import time

def spawn_wmi():
    exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data = os.path.expandvars(r"%USERPROFILE%\.gemini\antigravity-ide\scratch\browser_profile")
    url = "https://studio.youtube.com/channel/UC1poZZSwqopCKwPz6MlGFkA/videos/upload?d=pt"
    
    ps_cmd = f'''
    $exe = "{exe}"
    $userData = "{user_data}"
    $cmd = "`"$exe`" --remote-debugging-port=9222 --user-data-dir=`"$userData`" --no-first-run --no-default-browser-check --window-size=1280,850 --window-position=150,80 `"{url}`""
    $res = ([wmiclass]"Win32_Process").Create($cmd)
    Write-Output "WMI ReturnValue: $($res.ReturnValue), ProcessId: $($res.ProcessId)"
    '''
    
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("Error:", res.stderr)
        
    time.sleep(3)
    try:
        import sys
        sys.path.append(r"C:\Users\sude3\.gemini\config\skills\interactive-browser-controller\scripts")
        import launch_browser
        launch_browser.bring_window_to_front("Chrome", 150, 80, 1280, 850)
    except Exception as e:
        print("Bring to front error:", e)

if __name__ == "__main__":
    spawn_wmi()


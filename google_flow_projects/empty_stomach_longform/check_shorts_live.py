# -*- coding: utf-8 -*-
import urllib.request
import json
import websocket

with urllib.request.urlopen("http://127.0.0.1:9222/json") as r:
    data = json.loads(r.read().decode())
    target = next(d for d in data if "studio.youtube" in d.get("url", ""))
    ws_url = target["webSocketDebuggerUrl"]

ws = websocket.create_connection(ws_url)
# navigate to shorts tab
ws.send(json.dumps({
    "id": 1,
    "method": "Page.navigate",
    "params": {"url": "https://studio.youtube.com/channel/UC1poZZSwqopCKwPz6MlGFkA/videos/short?d=ud"}
}))
ws.recv()

import time
time.sleep(3)

ws.send(json.dumps({
    "id": 2,
    "method": "Runtime.evaluate",
    "params": {
        "expression": 'Array.from(document.querySelectorAll("#video-title")).map(e => e.innerText.trim())',
        "returnByValue": True
    }
}))
res = json.loads(ws.recv())
print("LIVE SHORTS IN STUDIO:", res["result"]["result"].get("value"))
ws.close()


# -*- coding: utf-8 -*-
import urllib.request
import json
import websocket

with urllib.request.urlopen("http://127.0.0.1:9222/json") as r:
    data = json.loads(r.read().decode())
    target = next(d for d in data if d.get("id") == "ED861AC20E6B45F8960351F5044BF19B")
    ws_url = target["webSocketDebuggerUrl"]

ws = websocket.create_connection(ws_url)
cmd = json.dumps({
    "id": 1,
    "method": "Runtime.evaluate",
    "params": {
        "expression": 'Array.from(document.querySelectorAll("#video-title")).map(e => e.innerText.trim())',
        "returnByValue": True
    }
})
ws.send(cmd)
res = json.loads(ws.recv())
print("Titles in Shorts Tab:", res["result"]["result"].get("value"))
ws.close()


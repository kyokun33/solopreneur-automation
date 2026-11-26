# -*- coding: utf-8 -*-
import urllib.request
import re
import json

url = "https://www.youtube.com/watch?v=shWNRS6W9PA"
req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9"
})
html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="ignore")

title_m = re.search(r"<title>(.*?)</title>", html)
print("TITLE:", title_m.group(1) if title_m else "N/A")

desc_m = re.search(r'"shortDescription":"((?:[^"\\]|\\.)*)"', html)
if desc_m:
    desc = json.loads('"' + desc_m.group(1) + '"')
    print("\n--- DESCRIPTION ---")
    print(desc)

# Also look for captionTracks URL
cap_m = re.search(r'"captionTracks":(\[.*?\])', html)
if cap_m:
    tracks = json.loads(cap_m.group(1))
    print("\n--- CAPTION TRACKS ---")
    for t in tracks:
        print(t.get("languageCode"), t.get("name", {}).get("simpleText"), t.get("baseUrl")[:120])
    if tracks:
        cap_url = tracks[0]["baseUrl"] + "&fmt=json3"
        data = json.loads(urllib.request.urlopen(urllib.request.Request(cap_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=15).read().decode("utf-8", errors="ignore"))
        clean_lines = []
        for ev in data.get("events", []):
            segs = ev.get("segs", [])
            txt = "".join(s.get("utf8", "") for s in segs).strip()
            if txt and txt != "\n":
                clean_lines.append(txt)
        full = " ".join(clean_lines)
        print("\n--- TRANSCRIPT ---")
        print(full[:3500])
        with open(r"f:\1인기업\scratch\yt_shWNRS6W9PA_transcript.txt", "w", encoding="utf-8") as f:
            f.write(full)
        print("\nTotal transcript chars:", len(full))
else:
    print("\nNo captionTracks found in HTML.")

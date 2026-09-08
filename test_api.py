import requests

# 1. Create meeting
try:
    print("Creating meeting...")
    res = requests.post("http://localhost:8000/api/meetings", json={
        "title": "weekly",
        "meeting_date": "2026-09-08"
    })
    print(res.status_code, res.text)
    meeting_id = res.json()["id"]

    # 2. Paste transcript
    paste_text = """WEBVTT

00:00:00.000 --> 00:00:08.000
Sarah: Alright team, let me open the incident review for yesterday's database outage. David, can you give a brief timeline?

00:00:09.000 --> 00:00:22.000
David: Sure. At 14:15 UTC, our primary PostgreSQL"""
    print("Pasting transcript...")
    res2 = requests.post(f"http://localhost:8000/api/meetings/{meeting_id}/transcript/paste", json={
        "text": paste_text,
        "format": "vtt"
    })
    print(res2.status_code, res2.text)
except Exception as e:
    print("Exception:", e)

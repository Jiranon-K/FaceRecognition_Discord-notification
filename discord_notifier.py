import requests
from datetime import datetime, time
from pytz import timezone

DISCORD_WEBHOOK_URL = ""  # ใส่ URL ของ Webhook ที่ได้จากการสร้าง Webhook ใน Discord

# Global dict to track notifications sent per student per session each day
notifications_sent = {}

def send_discord_notification(name):
    # Use Thailand timezone
    tz = timezone("Asia/Bangkok")
    now = datetime.now(tz)
    current_date = now.date()
    current_time = now.time()

    session = None
    threshold = None
    session_label = ""

    # กำหนดช่วงเวลาเช็คชื่อ
    if time(8, 0) <= current_time < time(12, 0):
        session = "morning"
        threshold = time(8, 30)
        session_label = "เช็คชื่อเช้า"
    elif time(13, 0) <= current_time < time(16, 0):
        session = "afternoon"
        threshold = time(13, 30)
        session_label = "เช็คชื่อบ่าย"
    else:
        # ไม่อยู่ในช่วงเวลาที่กำหนด ไม่ส่งแจ้งเตือน
        return

    status = "ตรงเวลา" if current_time < threshold else "สาย"
    # Soft colors for Discord embed
    color = 0x88C9A1 if status == "ตรงเวลา" else 0xE8927C

    key = (name, session)
    if key in notifications_sent and notifications_sent[key] == current_date:
        return

    embed = {
        "title": f"{session_label}",
        "description": f"```\n{name}\n```",  # Monospace 
        "color": color,
        "fields": [
            {
                "name": "สถานะ",
                "value": f"`{status}`",
                "inline": True
            },
            {
                "name": "เวลา",
                "value": f"`{now.strftime('%H:%M:%S')}`",
                "inline": True
            }
        ],
        "footer": {
            "text": f"วันที่ {now.strftime('%Y-%m-%d')}"
        },
        "author": {
            "name": "ระบบเช็คชื่ออัตโนมัติ",
            "icon_url": "https://i.imgur.com/ba9f0Af.jpeg"  
        }
    }

    data = {
        "embeds": [embed]
    }

    requests.post(DISCORD_WEBHOOK_URL, json=data)
    print(f"ส่งแจ้งเตือน Discord สำหรับ {name} ใน {session_label}, สถานะ: {status}")

    notifications_sent[key] = current_date
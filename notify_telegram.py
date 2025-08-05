import requests
import json
import sys
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    return response.ok

if __name__ == "__main__":
    # Read scraped jobs from file (passed as argument or default new_jobs.json)
    filename = sys.argv[1] if len(sys.argv) > 1 else "new_jobs.json"
    try:
        with open(filename) as f:
            jobs = json.load(f)
    except Exception:
        jobs = []

    count = len(jobs)
    if count == 0:
        send_telegram_message("No new jobs found in the latest scrape.")
    else:
        # Prepare message with job titles and URLs (limit length for Telegram)
        lines = [f"<b>Found {count} new job(s):</b>\n"]
        for job in jobs[:10]:  # max 10 jobs to avoid long messages
            title = job.get("title", "No title")
            url = job.get("url", "")
            lines.append(f"• <a href='{url}'>{title}</a>")
        message = "\n".join(lines)
        send_telegram_message(message)

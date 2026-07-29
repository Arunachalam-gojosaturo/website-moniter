import os
import sys
import urllib.request
import smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText

# Configuration from Environment Variables
TARGET_URL = os.getenv("TARGET_URL", "https://google.com")
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
FORCE_EMAIL = os.getenv("FORCE_EMAIL", "false").lower() in ["true", "1", "yes"]

STATUS_FILE = "status.txt"
LAST_RUN_FILE = "last_run.txt"

def get_previous_state():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                return f.read().strip()
        except Exception:
            return "unknown"
    return "unknown"

def save_current_state(state):
    with open(STATUS_FILE, "w") as f:
        f.write(state + "\n")
    with open(LAST_RUN_FILE, "w") as f:
        f.write(datetime.now(timezone.utc).isoformat() + "\n")

def check_site(url):
    print(f"🔍 Checking target URL: {url}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SiteMonitor/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            status_code = response.getcode()
            print(f"🌐 HTTP Status Code: {status_code}")
            if 200 <= status_code < 400:
                return "online", status_code
            else:
                return "offline", status_code
    except urllib.error.HTTPError as e:
        print(f"🌐 HTTP Error Code: {e.code}")
        if 200 <= e.code < 400:
            return "online", e.code
        return "offline", e.code
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return "offline", 0

def send_email(subject, body):
    if not EMAIL_USERNAME or not EMAIL_PASSWORD or not EMAIL_TO:
        print("⚠️ Missing email credentials (EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_TO). Skipping email.")
        return False
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = f"Site Monitor <{EMAIL_USERNAME}>"
    msg["To"] = EMAIL_TO

    password = EMAIL_PASSWORD.replace(" ", "")

    try:
        print(f"📧 Sending email to {EMAIL_TO}...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USERNAME, password)
            server.sendmail(EMAIL_USERNAME, [EMAIL_TO], msg.as_string())
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def main():
    prev_state = get_previous_state()
    current_state, status_code = check_site(TARGET_URL)

    print(f"📊 Previous State: '{prev_state}' | Current State: '{current_state}'")

    should_send_email = False
    subject = ""
    body = ""

    if FORCE_EMAIL:
        print("⚡ FORCE_EMAIL is enabled. Triggering test notification email.")
        should_send_email = True
        subject = f"🔔 [Test Notification] Website Status: {current_state.upper()}"
        body = (
            f"Hello!\n\n"
            f"This is a test notification email from your Python Website Uptime Monitor.\n\n"
            f"Target URL: {TARGET_URL}\n"
            f"Current State: {current_state.upper()} (HTTP {status_code})\n"
            f"Previous State: {prev_state}\n"
            f"Time (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
    elif current_state == "offline" and prev_state == "online":
        print("🚨 ALERT: Site went DOWN!")
        should_send_email = True
        subject = f"❌ ALERT: {TARGET_URL} is DOWN!"
        body = (
            f"⚠️ ALERT: Your website is DOWN!\n\n"
            f"Target URL: {TARGET_URL}\n"
            f"HTTP Status: {status_code}\n"
            f"Time (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
    elif current_state == "online" and prev_state == "offline":
        print("🎉 RECOVERY: Site is back ONLINE!")
        should_send_email = True
        subject = f"✅ RECOVERY: {TARGET_URL} is back ONLINE"
        body = (
            f"✅ RECOVERY: Your website is back ONLINE!\n\n"
            f"Target URL: {TARGET_URL}\n"
            f"HTTP Status: {status_code}\n"
            f"Time (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
    elif prev_state == "unknown":
        print("ℹ️ First run initialization. Saving initial state without alert.")
    else:
        print("ℹ️ No state change detected. No email needed.")

    if should_send_email:
        send_email(subject, body)

    save_current_state(current_state)

if __name__ == "__main__":
    main()

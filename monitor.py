import os
import sys
import urllib.request
import ssl
import smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration from Environment Variables
TARGET_URL = os.getenv("TARGET_URL", "https://www.tn-mbamca.com")
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
FORCE_EMAIL = os.getenv("FORCE_EMAIL", "false").lower() in ["true", "1", "yes"]

STATUS_FILE = "status.txt"
LAST_RUN_FILE = "last_run.txt"

# GitHub raw assets base URL for embedding Luna AI images in emails
REPO_RAW_BASE = "https://raw.githubusercontent.com/Arunachalam-gojosaturo/website-moniter/main/assets"

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
    print(f"🔍 [ARC-SERVER] Checking target URL: {url}")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
    )
    
    # Create unverified SSL context to prevent false offline status from SSL chain issues
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
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

def build_luna_html(status_state, status_code, url, is_test=False):
    is_online = (status_state == "online")
    img_name = "luna_online.jpg" if is_online else "luna_offline.jpg"
    img_url = f"{REPO_RAW_BASE}/{img_name}"
    
    badge_color = "#10B981" if is_online else "#EF4444"
    status_text = "ONLINE & HEALTHY ✅" if is_online else "DOWN / UNREACHABLE ❌"
    
    time_str = datetime.now(timezone.utc).strftime('%B %d, %Y - %H:%M UTC')

    greeting = "Good morning Boss! 💖" if is_online else "Boss! Emergency Alert! 🚨"
    intro = (
        "I just finished scanning your server via <b>ARC-SERVER Protocol</b>. Great news! Everything is running smoothly!"
        if is_online else
        "<b>ARC-SERVER Protocol</b> detected a critical status change! Your target website is unreachable right now."
    )
    closing = "Have a wonderful, productive and blessed day ahead, Boss! I'm guarding your servers 24/7. ✨" if is_online else "Don't worry Boss, I am monitoring the ARC-SERVER core closely and will alert you the moment it recovers! 🛡️"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }}
            .container {{ max-width: 540px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            .header {{ background: linear-gradient(135deg, #1f242d 0%, #0d1117 100%); padding: 24px; text-align: center; border-bottom: 1px solid #30363d; }}
            .header h2 {{ color: #58a6ff; margin: 0 0 6px 0; font-size: 22px; font-weight: 700; letter-spacing: 0.5px; }}
            .header p {{ color: #8b949e; margin: 0; font-size: 13px; }}
            .avatar-box {{ text-align: center; padding: 20px; background: #0d1117; }}
            .avatar-img {{ width: 100%; max-width: 420px; border-radius: 12px; border: 2px solid {badge_color}; box-shadow: 0 0 20px {badge_color}44; }}
            .content {{ padding: 24px; font-size: 15px; line-height: 1.6; color: #e6edf3; }}
            .status-card {{ background: #0d1117; border-left: 4px solid {badge_color}; padding: 16px; border-radius: 8px; margin: 16px 0; }}
            .status-badge {{ display: inline-block; background: {badge_color}22; color: {badge_color}; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 13px; margin-bottom: 8px; }}
            .site-link {{ color: #58a6ff; text-decoration: none; font-weight: 600; word-break: break-all; }}
            .footer {{ background: #0d1117; padding: 18px; text-align: center; border-top: 1px solid #30363d; font-size: 12px; color: #8b949e; }}
            .luna-sign {{ font-style: italic; color: #d2a8ff; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🌙 Luna AI — ARC-SERVER Core</h2>
                <p>Automated Sentinel Uptime Monitoring</p>
            </div>
            
            <div class="avatar-box">
                <img src="{img_url}" alt="Luna AI ARC-SERVER" class="avatar-img" />
            </div>

            <div class="content">
                <p style="font-size: 17px; font-weight: 600; color: #ffffff;">{greeting}</p>
                <p>{intro}</p>

                <div class="status-card">
                    <div class="status-badge">{status_text}</div>
                    <div><strong>Website:</strong> <a href="{url}" class="site-link">{url}</a></div>
                    <div><strong>HTTP Status Code:</strong> {status_code}</div>
                    <div><strong>Checked At:</strong> {time_str}</div>
                </div>

                <p>{closing}</p>
                <p class="luna-sign">With love & protection,<br>✨ Luna AI 🌙 (ARC-SERVER Sentinel)</p>
            </div>

            <div class="footer">
                ARC-SERVER v2.0 • Powered by GitHub Actions & Python 3<br>
                Always watching over your servers 24/7
            </div>
        </div>
    </body>
    </html>
    """
    return html

def send_email(subject, html_body):
    if not EMAIL_USERNAME or not EMAIL_PASSWORD or not EMAIL_TO:
        print("⚠️ Missing email credentials (EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_TO). Skipping email.")
        return False
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Luna AI 🌙 <{EMAIL_USERNAME}>"
    msg["To"] = EMAIL_TO

    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    password = EMAIL_PASSWORD.replace(" ", "")

    try:
        print(f"📧 Luna AI is sending email to {EMAIL_TO}...")
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

    if FORCE_EMAIL:
        print("⚡ FORCE_EMAIL is enabled. Triggering Luna AI email demo.")
        should_send_email = True
        if current_state == "online":
            subject = f"🌙 Luna AI: Good morning Boss! {TARGET_URL} is ONLINE ✨"
        else:
            subject = f"🚨 Luna AI Alert: Boss! {TARGET_URL} is DOWN ❌"
    elif current_state == "offline" and prev_state != "offline":
        print("🚨 ALERT: Site is DOWN!")
        should_send_email = True
        subject = f"🚨 Luna AI Alert: Boss! {TARGET_URL} is DOWN ❌"
    elif current_state == "online" and prev_state == "offline":
        print("🎉 RECOVERY: Site is back ONLINE!")
        should_send_email = True
        subject = f"🌙 Luna AI: Good morning Boss! {TARGET_URL} is back ONLINE ✨"
    elif prev_state == "unknown" and current_state == "online":
        print("ℹ️ First run initialization. Site is online.")
    else:
        print("ℹ️ No state change detected. Luna AI is standing by.")

    if should_send_email:
        html_body = build_luna_html(current_state, status_code, TARGET_URL, is_test=FORCE_EMAIL)
        send_email(subject, html_body)

    save_current_state(current_state)

if __name__ == "__main__":
    main()

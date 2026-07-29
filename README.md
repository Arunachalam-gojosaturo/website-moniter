# 🌙 Luna AI — ARC-SERVER Website Uptime Monitor

A lightweight, 24/7 automated website uptime monitoring tool powered by **GitHub Actions**, **Python 3**, and **Gmail SMTP**. Features **Luna AI (ARC-SERVER Core)** persona with custom HTML email notifications and embedded avatars.

---

## 📸 ARC-SERVER Avatars

| Online & Healthy ✅ | Critical Alert / Down ❌ |
|:---:|:---:|
| ![Luna AI Online](assets/luna_online.jpg) | ![Luna AI Offline](assets/luna_offline.jpg) |

---

## ⚡ Features

- ⏱️ **24/7 Cloud Automated Monitoring**: Runs every 5 minutes in GitHub Cloud — **works even when your laptop is turned OFF**.
- 🌙 **Luna AI Persona**: Custom email alerts ("Good morning Boss! https://www.tn-mbamca.com is ONLINE ✨").
- 🎨 **HTML Email Templates**: Styled cyber-terminal layout with live embedded ARC-SERVER status avatars.
- 📧 **Smart State Alerts**: Only emails when your site goes **DOWN** or comes back **ONLINE** (prevents inbox spam).
- 💰 **100% Free**: Uses 0 paid services — operates entirely within free tier limits.

---

## 🛠️ How It Works

```mermaid
flowchart TD
    A[GitHub Actions 5-Min Schedule / Manual] --> B[Run Python 3 monitor.py]
    B --> C[Check Target URL HTTP Status]
    C --> D{HTTP 200-399?}
    D -- Yes --> E[State = ONLINE]
    D -- No --> F[State = OFFLINE]
    E --> G{Previous State?}
    F --> H{Previous State?}
    G -- Was Offline --> I[Luna AI sends Recovery Email ✅]
    H -- Was Online --> J[Luna AI sends Emergency Alert 🚨]
    G -- Was Online --> K[Save Status & Exit]
    H -- Was Offline --> K
    I --> K
    J --> K
```

---

## 🚀 Setup & Secrets Guide

In your GitHub repository (**Settings ➔ Secrets and variables ➔ Actions ➔ New repository secret**), configure:

| Secret Name | Value | Description |
|---|---|---|
| `EMAIL_USERNAME` | `arunachalamthehacker@gmail.com` | Sender email address |
| `EMAIL_PASSWORD` | `vwtadphcrbrcaemo` | Gmail App Password |
| `EMAIL_TO` | `cutyarunachalam1@gmail.com` | Notification recipient email |

---

## 📄 License

MIT License. Free for personal and commercial use.

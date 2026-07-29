# Site Uptime Monitor — Setup

## 1. Put the file in your repo
Copy `.github/workflows/monitor.yml` into any GitHub repo (create a new empty repo if you don't want it in an existing project).

## 2. Add secrets (repo → Settings → Secrets and variables → Actions → New repository secret)
| Secret name | Value |
|---|---|
| `EMAIL_USERNAME` | your sender Gmail address |
| `EMAIL_PASSWORD` | a Gmail **App Password** (NOT your normal Gmail password — Google blocks plain passwords for SMTP) |
| `EMAIL_TO` | the receiver email address |

### How to get a Gmail App Password
1. Enable 2-Step Verification on the sender Google account (myaccount.google.com/security).
2. Go to myaccount.google.com/apppasswords
3. Generate one for "Mail" → copy the 16-char password → paste as `EMAIL_PASSWORD`.

(Using a different provider like Outlook/Zoho? Just change `server_address`/`server_port` in the yml — ask me and I'll adjust it.)

## 3. Allow the workflow to push commits
Repo → Settings → Actions → General → "Workflow permissions" → select **Read and write permissions** → Save.
(This lets it commit `status.txt`, which is how it remembers previous state so it only emails you on a down→up change, not every 5 min.)

## 4. Test it
Repo → Actions tab → "Website Uptime Monitor" → Run workflow (manual trigger via `workflow_dispatch`). Check the logs to confirm it hits the site and the email step logic.

## Notes
- Cron is set to `*/5 * * * *` (every 5 min). GitHub's scheduler isn't exact — during high load it can be delayed up to a few extra minutes; there's no way around this on free GitHub Actions.
- It emails only on **offline → online** transition (immediate alert when it comes back up), plus a bonus down-alert on online → offline (delete that step block if you don't want it).
- First run ever has no `status.txt`, so `prev_state=unknown` — it won't false-fire an email that first run even if site is already online. From the 2nd run onward it tracks properly.

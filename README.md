# Naukri Profile Activity Automator 🚀

An automated macOS background service that keeps your **Naukri** candidate profile marked as **"Recently Active"** during prime Indian business hours (10:00 AM – 3:00 PM, Monday through Friday).

Recruiters on Naukri prioritize candidates who are actively checking the platform. This tool runs silently in the background, opens your profile and job feed in Google Chrome using your existing logged-in session, triggers activity heartbeats and smooth scrolls, and cleanly closes after 60 seconds — with zero disruptions to your normal workflow.

---

## ✨ Features

- **Native macOS LaunchAgent**: Managed by `launchd`, running quietly in the background without needing browser extensions, Docker, or external cloud servers.
- **Uses Existing Chrome Profile**: Automatically authenticated with your existing Naukri session — no storing of passwords, API keys, or cookies in plaintext.
- **Isolated Window Lifecycle**: Targets only the window it opens by its exact macOS window ID. Your existing Chrome windows, tabs, and open work are never disturbed.
- **Zero Memory Footprint**: If Chrome was closed before the run, it closes Chrome after 60 seconds.
- **Built-in Schedule Guard**: Runs strictly between 10:00 AM and 3:00 PM on weekdays (Mon–Fri). If your Mac is asleep and wakes up at night or on weekends, the script immediately exits without opening anything.
- **One-Command CLI**: Simple terminal command (`naukri-automation`) to inspect status, run tests, view logs, or pause/resume.
- **Comprehensive PDF Documentation**: Pre-rendered guide included in [`docs/Naukri_Automation_Guide.pdf`](docs/Naukri_Automation_Guide.pdf).

---

## 📅 Schedule & Frequency

Runs **once an hour on the hour** from 10:00 AM to 3:00 PM IST, Monday through Friday:

| Run # | Time (IST) | Days | Action |
| :---: | :---: | :---: | :--- |
| **1** | **10:00 AM** | Monday – Friday | Profile & Home Feed session (60s) |
| **2** | **11:00 AM** | Monday – Friday | Profile & Home Feed session (60s) |
| **3** | **12:00 PM** | Monday – Friday | Profile & Home Feed session (60s) |
| **4** | **01:00 PM** | Monday – Friday | Profile & Home Feed session (60s) |
| **5** | **02:00 PM** | Monday – Friday | Profile & Home Feed session (60s) |
| **6** | **03:00 PM** | Monday – Friday | Profile & Home Feed session (60s) |

*Total: 6 sessions per weekday / 30 sessions per week.*

---

## 🛠️ Quick Installation

Clone this repository and run the installer:

```bash
git clone https://github.com/Anuragh33/naukri-profile-automator.git
cd naukri-profile-automator
./install.sh
```

The installer will:
1. Copy the automation script and CLI wrapper to `~/.local/bin/`.
2. Configure the LaunchAgent plist with your user paths.
3. Load the background agent into macOS `launchd`.

---

## 💻 CLI Commands

Once installed, use `naukri-automation` anywhere in your terminal:

```bash
# Check current schedule status and launchd registration
naukri-automation status

# Execute an immediate 60-second test session (bypasses schedule check)
naukri-automation test

# Tail the execution logs
naukri-automation logs

# Pause the automation (e.g., during meetings or screen-sharing)
naukri-automation disable

# Resume the automation
naukri-automation enable
```

---

## ❓ FAQ: What Happens When My Mac is Closed?

- **While Closed / Asleep**: macOS enters sleep mode. System timers and background tasks pause; Chrome will **not** open.
- **Upon Waking Up**: `launchd` evaluates missed schedule intervals upon wake.
  - **Waking during active hours** (e.g. 11:30 AM on Wednesday): It runs a single catch-up browse session.
  - **Waking outside active hours** (e.g. 8:00 PM or Saturday morning): The built-in schedule validator detects that it is outside 10:00 AM – 3:00 PM Mon–Fri and exits in under 0.1 seconds. It will **never** unexpectedly open Chrome outside business hours.

---

## 📂 File Architecture

```
naukri-profile-automator/
├── bin/
│   ├── naukri_browse.py          # Core Python runner with schedule & AppleScript logic
│   └── naukri-automation         # Convenient bash CLI tool
├── launchd/
│   └── com.anuragh.naukri-automation.plist # macOS LaunchAgent definition
├── docs/
│   └── Naukri_Automation_Guide.pdf # Detailed visual PDF user guide
├── install.sh                    # One-command installer
├── uninstall.sh                  # Clean uninstaller
├── LICENSE                       # MIT License
└── README.md                     # Documentation
```

---

## 🔒 Privacy & Safety

- No personal passwords, tokens, or credentials are required or stored.
- Uses standard macOS AppleScript to interact with Google Chrome in your user session.
- Runs 100% locally on your machine.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

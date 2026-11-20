#!/opt/homebrew/bin/python3
"""
Naukri Account Activity Automator
---------------------------------
Periodically opens Naukri in Google Chrome using your existing logged-in session,
browses your profile and home feed for ~60 seconds to refresh your profile activity timestamp,
and then closes the window without disrupting any other open tabs or windows.

Schedule:
- Monday to Friday
- Once an hour from 10:00 AM to 3:00 PM (10, 11, 12, 13, 14, 15)
"""

import sys
import os
import time
import argparse
import logging
from datetime import datetime
import subprocess

LOG_DIR = os.path.expanduser("~/Library/Logs/naukri-automation")
LOG_FILE = os.path.join(LOG_DIR, "automation.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)

def run_osascript(script: str) -> tuple[int, str]:
    """Execute an AppleScript string and return (returncode, output)."""
    res = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
    )
    return res.returncode, res.stdout.strip()

def is_chrome_running() -> bool:
    """Check if Google Chrome is currently running."""
    res = subprocess.run(["pgrep", "-x", "Google Chrome"], capture_output=True)
    return res.returncode == 0

def is_within_schedule() -> tuple[bool, str]:
    """Check if current time is Monday-Friday between 10:00 AM and 3:59 PM."""
    now = datetime.now()
    # 0 = Monday, ..., 4 = Friday, 5 = Saturday, 6 = Sunday
    if now.weekday() > 4:
        return False, f"Today is {now.strftime('%A')} (weekend). Automation only runs Monday to Friday."
    if not (10 <= now.hour <= 15):
        return False, f"Current time is {now.strftime('%I:%M %p')}. Automation only runs between 10 AM and 3 PM."
    return True, f"Current time ({now.strftime('%A %I:%M %p')}) is within scheduled hours."

def browse_naukri(duration: int = 60, dry_run: bool = False):
    """Open Chrome, browse Naukri for `duration` seconds, and close."""
    logging.info("==========================================")
    logging.info("Starting Naukri browsing session...")

    if dry_run:
        logging.info("[Dry Run] Simulating browse session for %d seconds...", duration)
        time.sleep(2)
        logging.info("[Dry Run] Finished simulated session.")
        return

    was_running = is_chrome_running()
    logging.info("Google Chrome initially running: %s", was_running)

    # 1. Open a new window with Naukri Profile
    profile_url = "https://www.naukri.com/mnjuser/profile"
    home_url = "https://www.naukri.com/mnjuser/homepage"

    open_script = f'''
    tell application "Google Chrome"
        if not (it is running) then
            launch
            delay 2
        end if
        set targetWindow to make new window
        set URL of active tab of targetWindow to "{profile_url}"
        return id of targetWindow
    end tell
    '''
    ret, out = run_osascript(open_script)
    if ret != 0 or not out.isdigit():
        logging.error("Failed to open Google Chrome window: %s", out)
        return

    window_id = int(out)
    logging.info("Opened Naukri Profile in Chrome window ID %d", window_id)

    # Split duration roughly in half for profile + home feed
    half_time = max(10, (duration // 2) - 5)

    try:
        # Wait on Profile page
        logging.info("Browsing profile page for %d seconds...", half_time)
        time.sleep(half_time)

        # Attempt smooth scroll down
        scroll_script = f'''
        tell application "Google Chrome"
            try
                set targetWindow to (first window whose id is {window_id})
                execute active tab of targetWindow javascript "window.scrollBy({{top: 500, behavior: 'smooth'}});"
            end try
        end tell
        '''
        run_osascript(scroll_script)
        time.sleep(5)

        # Navigate to Homepage / Recommended Jobs feed
        logging.info("Navigating to Naukri home feed...")
        nav_script = f'''
        tell application "Google Chrome"
            try
                set targetWindow to (first window whose id is {window_id})
                set URL of active tab of targetWindow to "{home_url}"
            end try
        end tell
        '''
        run_osascript(nav_script)

        logging.info("Browsing home feed for %d seconds...", half_time)
        time.sleep(half_time)

        # Attempt smooth scroll down again
        run_osascript(scroll_script)
        time.sleep(5)

    finally:
        # Close the window we opened
        logging.info("Closing Chrome window ID %d...", window_id)
        close_script = f'''
        tell application "Google Chrome"
            try
                close (first window whose id is {window_id})
            end try
        end tell
        '''
        run_osascript(close_script)

        # If Chrome was NOT running before and has no remaining windows, quit Chrome cleanly
        if not was_running:
            cleanup_script = '''
            tell application "Google Chrome"
                try
                    if (count of windows) = 0 then
                        quit
                    end if
                end try
            end tell
            '''
            run_osascript(cleanup_script)
            logging.info("Cleaned up Chrome process since it was not running prior to automation.")

    logging.info("Naukri browsing session completed successfully.")

def main():
    parser = argparse.ArgumentParser(description="Naukri Account Activity Automator")
    parser.add_argument("--force", action="store_true", help="Force run regardless of day/time schedule (ideal for testing)")
    parser.add_argument("--duration", type=int, default=60, help="Duration to browse in seconds (default: 60)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without opening Chrome")
    parser.add_argument("--status", action="store_true", help="Show current schedule status and log location")
    args = parser.parse_args()

    if args.status:
        ok, msg = is_within_schedule()
        print("Schedule Status:", "ACTIVE" if ok else "INACTIVE")
        print("Details:", msg)
        print("Log File:", LOG_FILE)
        print("Chrome Running:", is_chrome_running())
        return

    if not args.force:
        within_schedule, msg = is_within_schedule()
        if not within_schedule:
            logging.info("Skipping run: %s", msg)
            return
        logging.info("Schedule check passed: %s", msg)
    else:
        logging.info("Force flag passed. Bypassing schedule checks.")

    browse_naukri(duration=args.duration, dry_run=args.dry_run)

if __name__ == "__main__":
    main()

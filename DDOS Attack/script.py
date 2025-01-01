import threading
import webbrowser
import time
import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import signal
import psutil

# Disclaimer: Only use this script on systems you own or have explicit permission to test.
"""
⚠️ DISCLAIMER ⚠️
This script is intended for educational and research purposes only.
Use it ONLY in a controlled environment or on systems you own or
have explicit permission to test. Misuse of this script can result
in legal consequences.
By using this script, you agree to act responsibly and ethically.
"""

# URL to open in tabs
TARGET_URL = "https://www.example.com"  # Replace with your own URL or local environment
OPEN_DELAY = 0.1  # Delay between opening tabs in seconds
BREAK_INTERVAL = 30  # Break interval in seconds
CODE_ENTRY_TIMEOUT = 30  # Time given to enter the code
DEFENSE_CODE = "leavemealone"  # Defense code to stop the attack

# Flag to stop the attack
defense_flag = threading.Event()

def open_tabs():
    """Open web browser tabs continuously with periodic breaks."""
    tab_count = 0
    while not defense_flag.is_set():
        # Open tabs continuously
        start_time = time.time()
        while time.time() - start_time < BREAK_INTERVAL:
            if defense_flag.is_set():
                print("Attack stopped by defense activation.")
                return
            webbrowser.open(TARGET_URL)
            tab_count += 1
            print(f"Tab {tab_count} opened.")
            time.sleep(OPEN_DELAY)

        # Trigger the defense mechanism during the break
        if not run_defense_mechanism():
            print("Code not entered correctly. Resuming attack...")


def run_defense_mechanism():
    """Show a popup window to accept the defense code with countdown."""
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    root.attributes('-topmost', True)  # Make the dialog always on top

    for remaining_time in range(CODE_ENTRY_TIMEOUT, 0, -1):
        user_input = simpledialog.askstring(
            "Defense Code",
            f"Enter the defense code to stop the attack (Time left: {remaining_time}s):",
            parent=root
        )
        if user_input and user_input.strip().lower() == DEFENSE_CODE:
            defense_flag.set()
            messagebox.showinfo("Success", "You are safe now! The attack has stopped.")
            close_browser_windows()
            root.destroy()
            return True
        elif user_input:
            messagebox.showerror("Error", "Incorrect code. Try again.")
        time.sleep(1)  # Countdown timer

    root.destroy()
    return False  # User failed to enter the correct code

def close_browser_windows():
    """Close all browser windows (specific to certain systems)."""
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if 'chrome' in process.info['name'].lower() or 'firefox' in process.info['name'].lower():
            os.kill(process.info['pid'], signal.SIGTERM)

# Main function to start the attack and defense mechanism
def main():
    global defense_flag

    # Start the tab-opening attack
    open_tabs()

    print("Simulation ended.")

if __name__ == "__main__":
    main()

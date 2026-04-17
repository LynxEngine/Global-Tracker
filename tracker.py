import requests
import time
from datetime import datetime

FLEET = [
    "OKFAB", "OKFAF", "OKFAH", "OKTUR", "OKFAK", "OEDFB", "OKFAA", "OKFAJ", 
    "OKPES", "OKLSD", "OKCAP", "OKEOB", "OKMHI", "OKHAD", "OKKUN", 
    "N25469", "N45FA", "N4773L", "N93434", "N99HR", "N2447B", "N2458G", 
    "N537HF", "N57FA", "N447ER", "N914SW", "N957GV", "N960GV"
]

def run_lynx_audit():
    url = "https://opensky-network.org/api/states/all"
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"--- LYNX ENGINE SCAN START: {now} ---")
    
    # Try 3 times if the server is busy
    for attempt in range(3):
        try:
            print(f"Connecting to Global Feed (Attempt {attempt + 1})...")
            response = requests.get(url, timeout=45) # Longer timeout
            if response.status_code == 200:
                data = response.json().get('states', [])
                active_targets = [s for s in data if s[1].strip() in FLEET]
                if active_targets:
                    print(f"REPORT: {len(active_targets)} TARGETS ACTIVE")
                    for s in active_targets:
                        print(f" >> {s[1].strip()}: {int(s[7]*3.28) if s[7] else 0}ft")
                else:
                    print("REPORT: NO TARGETS IN FLIGHT (Fleet Grounded)")
                return # Exit once successful
            else:
                print(f"Server Busy (Status {response.status_code})...")
        except Exception as e:
            print(f"Attempt failed: {e}")
        time.sleep(5) # Wait 5 seconds before trying again

if __name__ == "__main__":
    run_lynx_audit()

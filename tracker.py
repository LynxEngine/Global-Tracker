import requests
from datetime import datetime

# LYNX TARGET FLEET (28 AIRCRAFT)
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
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json().get('states', [])
            active_targets = [s for s in data if s[1].strip() in FLEET]
            if active_targets:
                print(f"REPORT: {len(active_targets)} TARGETS ACTIVE")
                for s in active_targets:
                    callsign = s[1].strip()
                    alt_ft = int(s[7] * 3.28084) if s[7] is not None else 0
                    spd_kt = int(s[9] * 1.94384) if s[9] is not None else 0
                    print(f" >> {callsign}: ALT {alt_ft}ft | SPD {spd_kt}kts")
            else:
                print("REPORT: NO TARGETS IN FLIGHT (Fleet Grounded)")
        else:
            print(f"BRIDGE ERROR: Status {response.status_code}")
    except Exception as e:
        print(f"SYSTEM ERROR: {str(e)}")

if __name__ == "__main__":
    run_lynx_audit()

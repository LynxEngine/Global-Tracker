import requests
import time
from datetime import datetime

# LYNX GLOBAL SAFETY WATCHLIST
# Includes Czech (OK-) and US (N-) aircraft from your 28-plane fleet.
FLEET_HEX = {
    # --- EUROPEAN GROUP ---
    "44066c": "OK-TUR", "440663": "OK-FAF", "440665": "OK-FAH", 
    "440661": "OK-FAA", "440667": "OK-FAJ", "440669": "OK-FAK",
    "440664": "OK-FAG", "440662": "OK-FAB", "440668": "OK-PES",
    "44066b": "OK-LSD", "44066a": "OK-CAP", "440666": "OK-EOB",
    
    # --- US / INTERNATIONAL GROUP ---
    "a2693b": "N25469", "a5769b": "N45FA",  "a5db22": "N4773L",
    "acf6e5": "N93434", "ad8354": "N99HR",  "a2420a": "N2447B",
    "a2472b": "N2458G", "a6cc6e": "N537HF", "a75169": "N57FA",
    "a56589": "N447ER", "acc333": "N914SW", "ad1d14": "N957GV",
    "ad278a": "N960GV"
}

def run_safety_audit():
    url = "https://opensky-network.org/api/states/all"
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"--- LYNX GLOBAL SAFETY AUDIT START: {now} ---")
    
    try:
        response = requests.get(url, timeout=45)
        if response.status_code == 200:
            states = response.json().get('states', [])
            found = 0
            for s in states:
                icao = s[0]
                if icao in FLEET_HEX:
                    found += 1
                    reg = FLEET_HEX[icao]
                    # Data Mapping: 
                    # s[6]=Lat, s[5]=Lon, s[7]=Alt(m), s[9]=Spd(m/s), s[11]=V-Rate
                    lat, lon = s[6], s[5]
                    alt = int(s[7] * 3.28) if s[7] else 0
                    spd = int(s[9] * 1.94) if s[9] else 0
                    v_rate = s[11]
                    
                    print(f"ALERT: {reg} FOUND")
                    print(f" >> LOCATION: {lat}, {lon}")
                    print(f" >> ALTITUDE: {alt} ft")
                    print(f" >> AIRSPEED: {spd} kts")
                    print(f" >> VERTICAL RATE: {v_rate} m/s")
                    
                    # SAFETY LOGIC: Detect unusual descent
                    if v_rate and v_rate < -8:
                        print(" !! WARNING: High-Speed Descent Detected !!")
                    print("-" * 30)
            
            if found == 0:
                print("REPORT: NO WATCHLIST AIRCRAFT CURRENTLY IN AIR.")
        else:
            print(f"API Error: {response.status_code}")
    except Exception as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    run_safety_audit()

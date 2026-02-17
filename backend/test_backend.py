import requests
from sgp4.api import Satrec, jday
import datetime

def test_tle():
    norad_id = 25544
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=tle"
    print(f"Fetching {url}...")
    try:
        res = requests.get(url, timeout=10)
        print(f"Status: {res.status_code}")
        print(f"Content: {res.text[:100]}...")
        if res.status_code == 200:
            lines = res.text.strip().splitlines()
            if len(lines) >= 3:
                print("TLE format looks correct (3 lines with name).")
                s = Satrec.twoline2rv(lines[1], lines[2])
                print("SGP4 Parsed successfully.")
            elif len(lines) == 2:
                print("TLE format looks correct (2 lines).")
                s = Satrec.twoline2rv(lines[0], lines[1])
                print("SGP4 Parsed successfully.")
            else:
                print("Invalid TLE line count.")
        else:
            print("Failed to fetch.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_tle()

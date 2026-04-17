#!/usr/bin/env python3

import datetime
import os
import json
import urllib.request
import urllib.parse
import time

# Window of years to bake: current year ± YEAR_WINDOW (inclusive on both sides).
YEAR_WINDOW = 10

BASE_URL = "http://localhost:8000"
DIST_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "dist"))
DIST_DIR = os.path.join(DIST_ROOT, "v1")
METADATA_OUT = os.path.join(DIST_ROOT, "metadata.json")

def fetch_json(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def generate_calendar(year, nation, diocese, locale, output_file):
    if os.path.exists(output_file):
        return output_file

    params = {'year': year, 'locale': locale}
    if nation:
        params['nation'] = nation
    if diocese:
        params['diocese'] = diocese

    url = f"{BASE_URL}/calendar?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    
    if data:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        print(f"Generated: {output_file}")
    return output_file

def main():
    print("Fetching metadata...")
    metadata_url = f"{BASE_URL}/metadata"
    data = fetch_json(metadata_url)
    if not data or 'litcal_metadata' not in data:
        print("Failed to get metadata.")
        return
    
    metadata = data['litcal_metadata']
    os.makedirs(DIST_ROOT, exist_ok=True)
    with open(METADATA_OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {METADATA_OUT}")
    current_year = datetime.date.today().year
    years = range(current_year - YEAR_WINDOW, current_year + YEAR_WINDOW + 1)
    print(f"Baking years {years.start}–{years.stop - 1} (current year {current_year} ± {YEAR_WINDOW})")
    tasks = []

    for year in years:
        # Universal Calendars
        for locale in metadata.get('locales', []):
            output_file = os.path.join(DIST_DIR, str(year), "universal", f"{locale}.json")
            tasks.append((year, None, None, locale, output_file))

        # National Calendars
        for calendar in metadata.get('national_calendars', []):
            nation = calendar['calendar_id']
            for locale_full in calendar['locales']:
                locale = locale_full.split('_')[0]
                output_file = os.path.join(DIST_DIR, str(year), "nations", nation, f"{locale}.json")
                tasks.append((year, nation, None, locale, output_file))

        # Diocesan Calendars
        for calendar in metadata.get('diocesan_calendars', []):
            diocese = calendar['calendar_id']
            for locale_full in calendar['locales']:
                locale = locale_full.split('_')[0]
                output_file = os.path.join(DIST_DIR, str(year), "dioceses", diocese, f"{locale}.json")
                tasks.append((year, None, diocese, locale, output_file))
                
    print(f"Executing {len(tasks)} generation tasks sequentially to avoid server race conditions...")
    
    for task in tasks:
        generate_calendar(*task)
        # Small delay to let the server breathe
        time.sleep(0.05)
            
    print("Done!")

if __name__ == '__main__':
    main()

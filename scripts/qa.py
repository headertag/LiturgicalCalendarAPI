#!/usr/bin/env python3

import os
import json
import sys
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8000"
DIST_ROOT = os.path.join(os.path.dirname(__file__), "..", "dist", "v1")

def fetch_json(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return None

def verify_file(args):
    file_path, year_dir = args
    year = int(os.path.basename(year_dir))
    relative_path = os.path.relpath(file_path, year_dir)
    parts = relative_path.split(os.sep)

    # Structure is: universal/{locale}.json OR nations/{nation}/{locale}.json OR dioceses/{diocese}/{locale}.json
    params = {'year': year}
    
    if parts[0] == 'universal':
        locale = parts[1].replace('.json', '')
        params['locale'] = locale
    elif parts[0] == 'nations':
        params['national_calendar'] = parts[1]
        params['locale'] = parts[2].replace('.json', '')
    elif parts[0] == 'dioceses':
        params['diocesan_calendar'] = parts[1]
        params['locale'] = parts[2].replace('.json', '')
    else:
        return True, None # Not a calendar file we care about

    url = f"{BASE_URL}/calendar?" + urllib.parse.urlencode(params)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        static_data = json.load(f)

    api_data = fetch_json(url)
    if api_data is None:
        return False, f"Could not fetch from API: {url}"

    # Strip volatile metadata
    for data in (static_data, api_data):
        if 'metadata' in data:
            for k in ('generation_time', 'request_id', 'timestamp', 'date_time'):
                data['metadata'].pop(k, None)

    if static_data == api_data:
        return True, None
    else:
        # Find the mismatch for reporting
        mismatches = []
        if static_data.keys() != api_data.keys():
            mismatches.append(f"Root keys mismatch: Static={list(static_data.keys())}, API={list(api_data.keys())}")
        else:
            for key in api_data.keys():
                if api_data[key] != static_data[key]:
                    mismatches.append(f"Field '{key}' mismatch")
        return False, f"Mismatch in {relative_path}: {'; '.join(mismatches)}"

def main():
    if not os.path.exists(DIST_ROOT):
        print(f"Error: {DIST_ROOT} does not exist. Run pipeline.py first.")
        sys.exit(1)

    year_dirs = sorted(
        os.path.join(DIST_ROOT, name) for name in os.listdir(DIST_ROOT)
        if name.isdigit() and os.path.isdir(os.path.join(DIST_ROOT, name))
    )
    if not year_dirs:
        print(f"Error: no year directories found under {DIST_ROOT}.")
        sys.exit(1)

    years_span = f"{os.path.basename(year_dirs[0])}–{os.path.basename(year_dirs[-1])}"
    print(f"Scanning {DIST_ROOT} for files across {len(year_dirs)} years ({years_span})...")
    files_to_verify = []
    for year_dir in year_dirs:
        for root, dirs, files in os.walk(year_dir):
            for file in files:
                if file.endswith('.json'):
                    files_to_verify.append((os.path.join(root, file), year_dir))

    total = len(files_to_verify)
    print(f"Verifying {total} files against live API...")
    
    failures = []
    completed = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(verify_file, files_to_verify))
        for success, error in results:
            completed += 1
            if not success:
                failures.append(error)
                print(f"FAILED: {error}")
            if completed % 50 == 0:
                print(f"Progress: {completed}/{total} verified...")

    print("\n" + "="*30)
    print(f"Verification Complete!")
    print(f"Total Files: {total}")
    print(f"Passed: {total - len(failures)}")
    print(f"Failed: {len(failures)}")
    print("="*30)

    if failures:
        sys.exit(1)
    else:
        print("All static files match the API output exactly! (Zero 'boogs' found)")
        sys.exit(0)

if __name__ == '__main__':
    main()

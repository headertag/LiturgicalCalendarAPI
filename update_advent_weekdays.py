import json

file_path = 'jsondata/sourcedata/lectionary/feriale_tempus_adventus/en.json'

with open(file_path, 'r') as f:
    data = json.load(f)

advent_acclamations = {
    "AdventWeekday1Tuesday": "Psalm 85:8",
    "AdventWeekday1Wednesday": "Isaiah 40:9-10",
    "AdventWeekday1Friday": "Isaiah 40:9-10",
    "AdventWeekday2Monday": "Luke 3:4, 6",
    "AdventWeekday2Tuesday": "Luke 3:4, 6",
    "AdventWeekday2Wednesday": "Isaiah 45:8",
    "AdventWeekday2Friday": "Isaiah 45:8",
    "AdventWeekday3Tuesday": "Psalm 85:8",
    "AdventWeekday3Friday": "Isaiah 61:1",
    "AdventWeekdayDec17": "O Wisdom",
    "AdventWeekdayDec18": "O Sacred Lord",
    "AdventWeekdayDec19": "O Flower of Jesse's stem",
    "AdventWeekdayDec20": "O Key of David",
    "AdventWeekdayDec21": "O Radiant Dawn",
    "AdventWeekdayDec22": "O King of all nations",
    "AdventWeekdayDec23": "O Emmanuel",
    "AdventWeekdayDec24": "O Radiant Dawn"
}

for key, value in advent_acclamations.items():
    if key in data:
        data[key]["gospel_acclamation"] = value

with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Updated {file_path}")

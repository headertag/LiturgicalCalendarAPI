import json

file_path = 'jsondata/sourcedata/lectionary/feriale_tempus_nativitatis/en.json'

with open(file_path, 'r') as f:
    data = json.load(f)

christmas_weekdays = {
    "ChristmasWeekdayDec30": {
        "first_reading": "1 John 2:12-17",
        "responsorial_psalm": "Psalm 96:7-8a, 8b-9, 10",
        "gospel_acclamation": "Matthew 4:16",
        "gospel": "Luke 2:36-40"
    },
    "ChristmasWeekdayDec31": {
        "first_reading": "1 John 2:18-21",
        "responsorial_psalm": "Psalm 96:1-2, 11-12, 13",
        "gospel_acclamation": "John 1:14a, 12a",
        "gospel": "John 1:1-18"
    },
    "ChristmasWeekdayJan2": {
        "first_reading": "1 John 2:22-28",
        "responsorial_psalm": "Psalm 98:1, 2-3ab, 3cd-4",
        "gospel_acclamation": "Hebrews 1:1-2",
        "gospel": "John 1:19-28"
    },
    "ChristmasWeekdayJan4": {
        "first_reading": "1 John 3:7-10",
        "responsorial_psalm": "Psalm 98:1, 7-8, 9",
        "gospel_acclamation": "Hebrews 1:1-2",
        "gospel": "John 1:35-42"
    }
}

for key, value in christmas_weekdays.items():
    if key in data:
        data[key].update(value)

with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Updated {file_path}")

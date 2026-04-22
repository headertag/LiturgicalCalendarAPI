import json

file_path = 'jsondata/sourcedata/lectionary/dominicale_et_festivum_B/en.json'

with open(file_path, 'r') as f:
    data = json.load(f)

year_b_data = {
    "Advent1": {
        "first_reading": "Isaiah 63:16b-17, 19b; 64:2-7",
        "responsorial_psalm": "Psalm 80:2-3, 15-16, 18-19",
        "second_reading": "1 Corinthians 1:3-9",
        "gospel_acclamation": "Psalm 85:8",
        "gospel": "Mark 13:33-37"
    },
    "Advent2": {
        "first_reading": "Isaiah 40:1-5, 9-11",
        "responsorial_psalm": "Psalm 85:9-10, 11-12, 13-14",
        "second_reading": "2 Peter 3:8-14",
        "gospel_acclamation": "Luke 3:4, 6",
        "gospel": "Mark 1:1-8"
    },
    "Advent3": {
        "first_reading": "Isaiah 61:1-2a, 10-11",
        "responsorial_psalm": "Luke 1:46-48, 49-50, 53-54",
        "second_reading": "1 Thessalonians 5:16-24",
        "gospel_acclamation": "Isaiah 61:1",
        "gospel": "John 1:6-8, 19-28"
    },
    "Advent4": {
        "first_reading": "2 Samuel 7:1-5, 8b-12, 14a, 16",
        "responsorial_psalm": "Psalm 89:2-3, 4-5, 27, 29",
        "second_reading": "Romans 16:25-27",
        "gospel_acclamation": "Luke 1:38",
        "gospel": "Luke 1:26-38"
    },
    "Christmas": {
        "vigil": {
            "first_reading": "Isaiah 62:1-5",
            "responsorial_psalm": "Psalm 89:4-5, 16-17, 27, 29",
            "second_reading": "Acts 13:16-17, 22-25",
            "gospel_acclamation": "",
            "gospel": "Matthew 1:1-25"
        },
        "night": {
            "first_reading": "Isaiah 9:1-6",
            "responsorial_psalm": "Psalm 96:1-2, 2-3, 11-12, 13",
            "second_reading": "Titus 2:11-14",
            "gospel_acclamation": "Luke 2:10-11",
            "gospel": "Luke 2:1-14"
        },
        "dawn": {
            "first_reading": "Isaiah 62:11-12",
            "responsorial_psalm": "Psalm 97:1, 6, 11-12",
            "second_reading": "Titus 3:4-7",
            "gospel_acclamation": "Luke 2:14",
            "gospel": "Luke 2:15-20"
        },
        "day": {
            "first_reading": "Isaiah 52:7-10",
            "responsorial_psalm": "Psalm 98:1, 2-3, 3-4, 5-6",
            "second_reading": "Hebrews 1:1-6",
            "gospel_acclamation": "",
            "gospel": "John 1:1-18"
        }
    },
    "HolyFamily": {
        "first_reading": "Genesis 15:1-6; 21:1-3",
        "responsorial_psalm": "Psalm 105:1-2, 3-4, 5-6, 8-9",
        "second_reading": "Hebrews 11:8, 11-12, 17-19",
        "gospel_acclamation": "Hebrews 1:1-2",
        "gospel": "Luke 2:22-40"
    },
    "OrdSunday2": {
        "first_reading": "1 Samuel 3:3b-10, 19",
        "responsorial_psalm": "Psalm 40:2, 4, 7-8, 8-9, 10",
        "second_reading": "1 Corinthians 6:13c-15a, 17-20",
        "gospel_acclamation": "John 1:41, 17",
        "gospel": "John 1:35-42"
    },
    "OrdSunday3": {
        "first_reading": "Jonah 3:1-5, 10",
        "responsorial_psalm": "Psalm 25:4-5, 6-7, 8-9",
        "second_reading": "1 Corinthians 7:29-31",
        "gospel_acclamation": "Mark 1:15",
        "gospel": "Mark 1:14-20"
    },
    "OrdSunday4": {
        "first_reading": "Deuteronomy 18:15-20",
        "responsorial_psalm": "Psalm 95:1-2, 6-7, 8-9",
        "second_reading": "1 Corinthians 7:32-35",
        "gospel_acclamation": "Matthew 4:16",
        "gospel": "Mark 1:21-28"
    },
    "OrdSunday5": {
        "first_reading": "Job 7:1-4, 6-7",
        "responsorial_psalm": "Psalm 147:1-2, 3-4, 5-6",
        "second_reading": "1 Corinthians 9:16-19, 22-23",
        "gospel_acclamation": "Matthew 8:17",
        "gospel": "Mark 1:29-39"
    },
    "OrdSunday6": {
        "first_reading": "Leviticus 13:1-2, 44-46",
        "responsorial_psalm": "Psalm 32:1-2, 5, 11",
        "second_reading": "1 Corinthians 10:31—11:1",
        "gospel_acclamation": "Luke 7:16",
        "gospel": "Mark 1:40-45"
    },
    "OrdSunday7": {
        "first_reading": "Isaiah 43:18-19, 21-22, 24b-25",
        "responsorial_psalm": "Psalm 41:2-3, 4-5, 13-14",
        "second_reading": "2 Corinthians 1:18-22",
        "gospel_acclamation": "Luke 4:18",
        "gospel": "Mark 2:1-12"
    },
    "OrdSunday8": {
        "first_reading": "Hosea 2:16b, 17b, 21-22",
        "responsorial_psalm": "Psalm 103:1-2, 3-4, 8, 10, 12-13",
        "second_reading": "2 Corinthians 3:1b-6",
        "gospel_acclamation": "James 1:18",
        "gospel": "Mark 2:18-22"
    },
    "OrdSunday9": {
        "first_reading": "Deuteronomy 5:12-15",
        "responsorial_psalm": "Psalm 81:3-4, 5-6, 10-11, 14, 17",
        "second_reading": "2 Corinthians 4:6-11",
        "gospel_acclamation": "John 17:17b, 17a",
        "gospel": "Mark 2:23—3:6"
    },
    "OrdSunday10": {
        "first_reading": "Genesis 3:9-15",
        "responsorial_psalm": "Psalm 130:1-2, 3-4, 5-6, 7-8",
        "second_reading": "2 Corinthians 4:13—5:1",
        "gospel_acclamation": "John 12:31b, 32",
        "gospel": "Mark 3:20-35"
    },
    "OrdSunday11": {
        "first_reading": "Ezekiel 17:22-24",
        "responsorial_psalm": "Psalm 92:2-3, 13-14, 15-16",
        "second_reading": "2 Corinthians 5:6-10",
        "gospel_acclamation": "",
        "gospel": "Mark 4:26-34"
    },
    "OrdSunday12": {
        "first_reading": "Job 38:1, 8-11",
        "responsorial_psalm": "Psalm 107:23-24, 25-26, 28-29, 30-31",
        "second_reading": "2 Corinthians 5:14-17",
        "gospel_acclamation": "Luke 7:16",
        "gospel": "Mark 4:35-41"
    },
    "OrdSunday13": {
        "first_reading": "Wisdom 1:13-15; 2:23-24",
        "responsorial_psalm": "Psalm 30:2, 4, 5-6, 11, 12, 13",
        "second_reading": "2 Corinthians 8:7, 9, 13-15",
        "gospel_acclamation": "2 Timothy 1:10",
        "gospel": "Mark 5:21-43"
    },
    "OrdSunday14": {
        "first_reading": "Ezekiel 2:2-5",
        "responsorial_psalm": "Psalm 123:1-2, 2, 3-4",
        "second_reading": "2 Corinthians 12:7-10",
        "gospel_acclamation": "Luke 4:18",
        "gospel": "Mark 6:1-6a"
    },
    "OrdSunday15": {
        "first_reading": "Amos 7:12-15",
        "responsorial_psalm": "Psalm 85:9-10, 11-12, 13-14",
        "second_reading": "Ephesians 1:3-14",
        "gospel_acclamation": "Ephesians 1:17-18",
        "gospel": "Mark 6:7-13"
    },
    "OrdSunday16": {
        "first_reading": "Jeremiah 23:1-6",
        "responsorial_psalm": "Psalm 23:1-3, 3-4, 5, 6",
        "second_reading": "Ephesians 2:13-18",
        "gospel_acclamation": "John 10:27",
        "gospel": "Mark 6:30-34"
    },
    "OrdSunday17": {
        "first_reading": "2 Kings 4:42-44",
        "responsorial_psalm": "Psalm 145:10-11, 15-16, 17-18",
        "second_reading": "Ephesians 4:1-6",
        "gospel_acclamation": "Luke 7:16",
        "gospel": "John 6:1-15"
    },
    "OrdSunday18": {
        "first_reading": "Exodus 16:2-4, 12-15",
        "responsorial_psalm": "Psalm 78:3-4, 23-24, 25, 54",
        "second_reading": "Ephesians 4:17, 20-24",
        "gospel_acclamation": "Matthew 4:4b",
        "gospel": "John 6:24-35"
    },
    "OrdSunday19": {
        "first_reading": "1 Kings 19:4-8",
        "responsorial_psalm": "Psalm 34:2-3, 4-5, 6-7, 8-9",
        "second_reading": "Ephesians 4:30—5:2",
        "gospel_acclamation": "John 6:51",
        "gospel": "John 6:41-51"
    },
    "OrdSunday20": {
        "first_reading": "Proverbs 9:1-6",
        "responsorial_psalm": "Psalm 34:2-3, 10-11, 12-13, 14-15",
        "second_reading": "Ephesians 5:15-20",
        "gospel_acclamation": "John 6:56",
        "gospel": "John 6:51-58"
    },
    "OrdSunday21": {
        "first_reading": "Joshua 24:1-2a, 15-17, 18b",
        "responsorial_psalm": "Psalm 34:2-3, 16-17, 18-19, 20-21, 22-23",
        "second_reading": "Ephesians 5:21-32",
        "gospel_acclamation": "John 6:63c, 68c",
        "gospel": "John 6:60-69"
    },
    "OrdSunday22": {
        "first_reading": "Deuteronomy 4:1-2, 6-8",
        "responsorial_psalm": "Psalm 15:2-3, 3-4, 4-5",
        "second_reading": "James 1:17-18, 21b-22, 27",
        "gospel_acclamation": "James 1:18",
        "gospel": "Mark 7:1-8, 14-15, 21-23"
    },
    "OrdSunday23": {
        "first_reading": "Isaiah 35:4-7a",
        "responsorial_psalm": "Psalm 146:7, 8-9, 9-10",
        "second_reading": "James 2:1-5",
        "gospel_acclamation": "Matthew 4:23",
        "gospel": "Mark 7:31-37"
    },
    "OrdSunday24": {
        "first_reading": "Isaiah 50:5-9a",
        "responsorial_psalm": "Psalm 116:1-2, 3-4, 5-6, 8-9",
        "second_reading": "James 2:14-18",
        "gospel_acclamation": "Galatians 6:14",
        "gospel": "Mark 8:27-35"
    },
    "OrdSunday25": {
        "first_reading": "Wisdom 2:12, 17-20",
        "responsorial_psalm": "Psalm 54:3-4, 5, 6, 8",
        "second_reading": "James 3:16—4:3",
        "gospel_acclamation": "2 Thessalonians 2:14",
        "gospel": "Mark 9:30-37"
    },
    "OrdSunday26": {
        "first_reading": "Numbers 11:25-29",
        "responsorial_psalm": "Psalm 19:8, 10, 12-13, 14",
        "second_reading": "James 5:1-6",
        "gospel_acclamation": "John 17:17b, 17a",
        "gospel": "Mark 9:38-43, 45, 47-48"
    },
    "OrdSunday27": {
        "first_reading": "Genesis 2:18-24",
        "responsorial_psalm": "Psalm 128:1-2, 3, 4-5, 6",
        "second_reading": "Hebrews 2:9-11",
        "gospel_acclamation": "1 John 4:12",
        "gospel": "Mark 10:2-16"
    },
    "OrdSunday28": {
        "first_reading": "Wisdom 7:7-11",
        "responsorial_psalm": "Psalm 90:12-13, 14-15, 16-17",
        "second_reading": "Hebrews 4:12-13",
        "gospel_acclamation": "Matthew 5:3",
        "gospel": "Mark 10:17-30"
    },
    "OrdSunday29": {
        "first_reading": "Isaiah 53:10-11",
        "responsorial_psalm": "Psalm 33:4-5, 18-19, 20, 22",
        "second_reading": "Hebrews 4:14-16",
        "gospel_acclamation": "Mark 10:45",
        "gospel": "Mark 10:35-45"
    },
    "OrdSunday30": {
        "first_reading": "Jeremiah 31:7-9",
        "responsorial_psalm": "Psalm 126:1-2, 2-3, 4-5, 6",
        "second_reading": "Hebrews 5:1-6",
        "gospel_acclamation": "2 Timothy 1:10",
        "gospel": "Mark 10:46-52"
    },
    "OrdSunday31": {
        "first_reading": "Deuteronomy 6:2-6",
        "responsorial_psalm": "Psalm 18:2-3, 3-4, 47, 51",
        "second_reading": "Hebrews 7:23-28",
        "gospel_acclamation": "John 14:23",
        "gospel": "Mark 12:28b-34"
    },
    "OrdSunday32": {
        "first_reading": "1 Kings 17:10-16",
        "responsorial_psalm": "Psalm 146:7, 8-9, 9-10",
        "second_reading": "Hebrews 9:24-28",
        "gospel_acclamation": "Matthew 5:3",
        "gospel": "Mark 12:38-44"
    },
    "OrdSunday33": {
        "first_reading": "Daniel 12:1-3",
        "responsorial_psalm": "Psalm 16:5, 8, 9-10, 11",
        "second_reading": "Hebrews 10:11-14, 18",
        "gospel_acclamation": "Luke 21:36",
        "gospel": "Mark 13:24-32"
    },
    "Lent1": {
        "first_reading": "Genesis 9:8-15",
        "responsorial_psalm": "Psalm 25:4-5, 6-7, 8-9",
        "second_reading": "1 Peter 3:18-22",
        "gospel_acclamation": "Matthew 4:4b",
        "gospel": "Mark 1:12-15"
    },
    "Lent2": {
        "first_reading": "Genesis 22:1-2, 9a, 10-13, 15-18",
        "responsorial_psalm": "Psalm 116:10, 15, 16-17, 18-19",
        "second_reading": "Romans 8:31b-34",
        "gospel_acclamation": "",
        "gospel": "Mark 9:2-10"
    },
    "Lent3": {
        "first_reading": "Exodus 20:1-17",
        "responsorial_psalm": "Psalm 19:8, 9, 10, 11",
        "second_reading": "1 Corinthians 1:22-25",
        "gospel_acclamation": "John 3:16",
        "gospel": "John 2:13-25"
    },
    "Lent4": {
        "first_reading": "2 Chronicles 36:14-16, 19-23",
        "responsorial_psalm": "Psalm 137:1-2, 3, 4-5, 6",
        "second_reading": "Ephesians 2:4-10",
        "gospel_acclamation": "John 3:16",
        "gospel": "John 3:14-21"
    },
    "Lent5": {
        "first_reading": "Jeremiah 31:31-34",
        "responsorial_psalm": "Psalm 51:3-4, 12-13, 14-15",
        "second_reading": "Hebrews 5:7-9",
        "gospel_acclamation": "John 12:26",
        "gospel": "John 12:20-33"
    },
    "PalmSun": {
        "procession": "Mark 11:1-10",
        "first_reading": "Isaiah 50:4-7",
        "responsorial_psalm": "Psalm 22:8-9, 17-18, 19-20, 23-24",
        "second_reading": "Philippians 2:6-11",
        "gospel_acclamation": "Philippians 2:8-9",
        "gospel": "Mark 14:1—15:47"
    },
    "Easter": {
        "first_reading": "Acts 10:34a, 37-43",
        "responsorial_psalm": "Psalm 118:1-2, 16-17, 22-23",
        "second_reading": "Colossians 3:1-4",
        "gospel_acclamation": "1 Corinthians 5:7b-8a",
        "gospel": "John 20:1-9"
    },
    "Easter2": {
        "first_reading": "Acts 4:32-35",
        "responsorial_psalm": "Psalm 118:2-4, 13-15, 22-24",
        "second_reading": "1 John 5:1-6",
        "gospel_acclamation": "John 20:29",
        "gospel": "John 20:19-31"
    },
    "Easter3": {
        "first_reading": "Acts 3:13-15, 17-19",
        "responsorial_psalm": "Psalm 4:2, 4, 7-8, 9",
        "second_reading": "1 John 2:1-5a",
        "gospel_acclamation": "Luke 24:32",
        "gospel": "Luke 24:35-48"
    },
    "Easter4": {
        "first_reading": "Acts 4:8-12",
        "responsorial_psalm": "Psalm 118:1, 8-9, 21-23, 26, 28, 29",
        "second_reading": "1 John 3:1-2",
        "gospel_acclamation": "John 10:14",
        "gospel": "John 10:11-18"
    },
    "Easter5": {
        "first_reading": "Acts 9:26-31",
        "responsorial_psalm": "Psalm 22:26-27, 28, 30, 31-32",
        "second_reading": "1 John 3:18-24",
        "gospel_acclamation": "John 15:4a, 5b",
        "gospel": "John 15:1-8"
    },
    "Easter6": {
        "first_reading": "Acts 10:25-26, 34-35, 44-48",
        "responsorial_psalm": "Psalm 98:1, 2-3, 3-4",
        "second_reading": "1 John 4:7-10",
        "gospel_acclamation": "John 14:23",
        "gospel": "John 15:9-17"
    },
    "Easter7": {
        "first_reading": "Acts 1:15-17, 20a, 20c-26",
        "responsorial_psalm": "Psalm 103:1-2, 11-12, 19-20",
        "second_reading": "1 John 4:11-16",
        "gospel_acclamation": "John 14:18",
        "gospel": "John 17:11b-19"
    },
    "Ascension": {
        "first_reading": "Acts 1:1-11",
        "responsorial_psalm": "Psalm 47:2-3, 6-7, 8-9",
        "second_reading": "Ephesians 1:17-23",
        "gospel_acclamation": "Matthew 28:19a, 20b",
        "gospel": "Mark 16:15-20"
    },
    "Trinity": {
        "first_reading": "Deuteronomy 4:32-34, 39-40",
        "responsorial_psalm": "Psalm 33:4-5, 6, 9, 18-19, 20, 22",
        "second_reading": "Romans 8:14-17",
        "gospel_acclamation": "Revelation 1:8",
        "gospel": "Matthew 28:16-20"
    },
    "CorpusChristi": {
        "first_reading": "Exodus 24:3-8",
        "responsorial_psalm": "Psalm 116:12-13, 15, 16, 17-18",
        "second_reading": "Hebrews 9:11-15",
        "gospel_acclamation": "John 6:51",
        "gospel": "Mark 14:12-16, 22-26"
    },
    "SacredHeart": {
        "first_reading": "Hosea 11:1, 3-4, 8c-9",
        "responsorial_psalm": "Isaiah 12:2-3, 4, 5-6",
        "second_reading": "Ephesians 3:8-12, 14-19",
        "gospel_acclamation": "1 John 4:10b",
        "gospel": "John 19:31-37"
    },
    "ChristKing": {
        "first_reading": "Daniel 7:13-14",
        "responsorial_psalm": "Psalm 93:1, 1-2, 5",
        "second_reading": "Revelation 1:5-8",
        "gospel_acclamation": "Mark 11:9, 10",
        "gospel": "John 18:33b-37"
    }
}

for key, value in year_b_data.items():
    if key in data:
        if isinstance(value, dict) and 'vigil' in value:
             for subkey, subvalue in value.items():
                 if subkey in data[key]:
                     data[key][subkey].update(subvalue)
                 else:
                     data[key][subkey] = subvalue
        else:
            data[key].update(value)

with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Updated {file_path}")

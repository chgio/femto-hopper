# Pixels femto-IN
# updated to FEMTO:
version = 0.1


import os, json, time
from datetime import datetime as dt


# repeatedly prompt the user for the file path until it's valid
# then read the backup file, decode it and load it as a dictionary

while True:
    input_path = input("Input .json backup file to open: ")
    file_path = input_path.strip()

    if os.path.exists(file_path):
        with open(file_path) as stream:
            pixels = json.load(stream)
        break

    else:
        print("File not found. Please retry.")


# port the loaded data to the FEMTO format
# and make sure it's sorted chronologically

femto = []

for entry in pixels:
    date = entry["date"]
    print(date)
    unix_ts = int(time.mktime(dt.strptime(date, "%Y-%m-%d").timetuple()))   # convert pixels' date format to UNIX timestamp
    mood = entry["mood"]
    note = entry["notes"]

    femto.append({
        "time": unix_ts,
        "mood": mood,
        "note": note
    })

femto.sort(key=lambda x: x["time"])


# finally, export the ported data
# to the femto-{version}.json file

with open("femto-v{v}.json".format(v=version), "w") as stream:
    json.dump(femto, stream, indent=4)
# Pixels femto-OUT
# updated to FEMTO:
version = 0.1


import os, json, time
from datetime import datetime as dt


# repeatedly prompt the user for the file path until it's valid
# then read the femto file load it as a dictionary

while True:
    input_path = input("Input .json femto file to open: ")
    file_path = input_path.strip()

    if os.path.exists(file_path):
        with open(file_path) as stream:
            femto = json.load(stream)
        break

    else:
        print("File not found. Please retry.")


# port the loaded data to the pixels format
# while merging same-day entries

entries = []
same_day = []                                                       # a list to keep track of all entries made during the same day
next_date = 0

for i, entry in enumerate(femto):
    unix_ts = entry["time"]
    mood = entry["mood"]
    note = entry["note"]

    if next_date:                                                   # if the next date is already initialised
        date = next_date                                            # take that for the current date
    else:                                                           # otherwise -- if it isn't initialised yet
        date = dt.utcfromtimestamp(unix_ts)                         # convert the UNIX timestamp
    year = date.year
    month = date.month
    day = date.day

    same_day.append(entry)

    next_entry = femto[(i+1)%len(femto)]                            # the modulo is inserted to prevent over-indexing the list; instead, it'll wrap around...
    next_date = dt.utcfromtimestamp(next_entry["time"])
    next_year = next_date.year
    next_month = next_date.month
    next_day = next_date.day

    if next_day != day or next_month != month or next_year != year: # ...because of that -- to account for both very long and very gapped usage -- all three date elements are checked
        moods = [e["mood"] for e in same_day]                       # the moods are extracted out of the same day list
        mood = round(sum(moods) / len(moods))                       # and averaged together to represent the overall daily mood

        notes = [e["note"] for e in same_day]                       # the notes are extracted out of the same day list
        note = "\n\n".join(notes).strip()                           # concatenated together and tidied up to represent the daily overview

        entries.append({
        "date":     "{y}-{m}-{d}".format(y=year, m=month, d=day),   # format the date accordingly to pixels' format
        "mood":     mood,
        "emotions": [],
        "notes":    note
        })

        same_day = []

pixels = entries


# finally, export the ported data
# to the mt-hopper_pixels-backup.json file

with open("mt-hopper_pixels-backup.json", "w") as stream:
    json.dump(pixels, stream, indent=4)
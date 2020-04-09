# Daylio femto-IN
# updated to FEMTO:
version = 0.1

# Copyright (C) 2020 Giorgio Ciacchella, Darren Fielding, Zoltán Kiss

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# See the GNU General Public License at `COPYING`
# or https://www.gnu.org/licenses/#GPL for more details.


import os, json, base64


# repeatedly prompt the user for the file path until it's valid
# then read the backup file, decode it and load it as a dictionary

while True:
    input_path = input("Input .daylio backup file to open: ")
    file_path = input_path.strip()

    if os.path.exists(file_path):
        with open(file_path) as stream:         # as mentioned in templates.md
            encoded = stream.read()             # daylio backups via a base64 file
            decoded = base64.b64decode(encoded) # which has to be decoded
            daylio = json.loads(decoded)        # before being loaded as a json
        break

    else:
        print("File not found. Please retry.")


# extract the meaningful data from the loaded dictionary
# and prepare it for easier manipulation

entries = daylio["dayEntries"]
moods = daylio["customMoods"]
tags = daylio["tags"]
tag_groups = daylio["tag_groups"]

moods_dict = {}                                 # lookup table to map mood id's to mood scores

for mood in moods:
    mood_id = mood["id"]
    mood_score = 6 - mood["mood_group_id"]      # normalise daylio's inverted mood scale
    moods_dict.update({mood_id: mood_score})

moods = moods_dict


# port the extracted data to the femto format
# and sort it chronologically

femto = []

for entry in entries:
    unix_ts = entry["datetime"] // 1000         # normalise daylio's millisecond UNIX timestamp
    mood_id = entry["mood"]
    mood = moods[mood_id]                       # look up the mood score from the mood id
    note = entry["note"]

    femto.append({
        "time": unix_ts,
        "mood": mood,
        "note": note
    })

femto.sort(key=lambda x: x["time"])             # normalise chronological sorting


# finally, export the ported data
# to the femto-{version}.json file

with open("femto-v{v}.json".format(v=version), "w") as stream:
    json.dump(femto, stream, indent=4)
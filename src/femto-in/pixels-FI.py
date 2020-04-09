# Pixels femto-IN
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
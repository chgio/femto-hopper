# Daylio femto-OUT
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


import os, json, base64, time
from datetime import datetime as dt


# repeatedly prompt the user for the file path until it's valid
# then read the femto file and load it as a dictionary

while True:
    input_path = input("Input .json femto file to open: ")
    file_path = input_path.strip()

    if os.path.exists(file_path):
        with open(file_path) as stream:
            femto = json.load(stream)
        break

    else:
        print("File not found. Please retry.")


# port the loaded data
# to the daylio format

entries = []
entry_id = 0

for entry in femto:
    entry_id += 1                               # linearly increase the entry id, even though it's not yet entirely clear how exactly daylio manages it
    unix_ts = entry["time"]
    mood = entry["mood"]
    note = entry["note"]

    date = dt.utcfromtimestamp(unix_ts)         # convert and "unpack" the UNIX timestamp
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute

    entries.append({
        "id":               entry_id,
        "minute":           minute,             # spread out the date accordingly to daylio's format
        "hour":             hour,
        "day":              day,
        "month":            month - 1,          # correct to daylio's 0-starting month numbering
        "year":             year,
        "datetime":         unix_ts * 1000,     # correct to daylio's millisecond UNIX timestamp
        "timeZoneOffset":   0,
        "mood":             6 - mood,           # correct to daylio's inverted mood scale
        "note":             note,
        "tags":             []
        })
    
    entries.sort(key=lambda x: -x["datetime"])  # correct to daylio's inverted chronological sorting

daylio = {
    "dayEntries": entries
}


# finally, encode the ported data and export it
# to the mt-hopper_daylio-backup.daylio file

with open("mt-hopper_daylio-backup.daylio", "w") as stream: # as mentioned in templates.md
    decoded = json.dumps(daylio)                            # daylio exports via a base64 file
    encoded = base64.b64encode(decoded.encode("utf-8"))     # so the json has to be encoded
    stream.write(encoded.decode("utf-8"))                   # before being written
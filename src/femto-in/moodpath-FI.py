version = 0.1

import os, json
from datetime import datetime as dt


# Moodpath has several .csv files, so we will prompt the user for a folder
# that contains them.
# Only using `happiness_scores.csv` and `notes.csv` as they contain the data
# we are most concerned with.
while True:
    path = input("Enter filepath containing Moodpath `.csv` files: ")
    path = path.strip()
    
    if not os.path.isdir(path):
        print("Path not found.  Please try again.")
        continue
    
    if not os.path.exists(path + "\happiness_scores.csv"):
        print("Cannot find necessary moodpath files.  Please try again.")
        continue
    
    break
    

times = []
moods = []
notes = []


# Fortunately, I think you need to submit a happiness score in order to
# submit other data, so the times in this file should be complete
with open(path + "/happiness_scores.csv") as f:
    for line in f.readlines()[1:]:
        line = line.strip().split(',')
        times.append(line[1]) 
        moods.append(int(line[0]) + 1)
        
        
# A note may or may not be included for a given entry, so we check for
# notes with a time shared with a happiness score entry
with open(path + "/notes.csv") as f:
    lines = [ x.strip().rsplit(',', 1) for x in f.readlines()[1:] ]
    i = 0
    for t in times:
        if t == lines[i][1]:
            if lines[i][0][0] == '"':           # Tidy up string if needed
                lines[i][0] = lines[i][0][1:-1]
            notes.append(lines[i][0])
            i += 1
        else:
            notes.append('')


# Custom UNIX time parser, so this would need thorough testing
# Alternatively could use third-party package `dateutil`
for i in range(len(times)):
    if times[i].count(' ') > 1:
        dts = times[i].rsplit(' ', 1)
        dts[1] = dts[1][:3] + ':' + dts[1][3:]
        dts = ''.join(dts)
        times[i] = int(dt.fromisoformat(dts).timestamp())


# Export the ported data to the femto-{version}.json file
femto = []
for i in range(len(times)):
    femto.append( {"time" : times[i], "mood": moods[i], "note" : notes[i]} )
    
femto.sort(key=lambda x: x["time"])
    
with open("femto-v{v}.json".format(v=version), "w") as stream:
    json.dump(femto, stream, indent=4)

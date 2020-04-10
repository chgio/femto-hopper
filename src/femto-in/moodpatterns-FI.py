# MoodPatterns femto-IN
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


import os, json, sqlite3


# repeatedly prompt the user for the file path until it's valid
# then connect to it as a database

while True:
    input_path = input("Input MoodPatterns .db backup file to open: ")
    file_path = input_path.strip()

    if os.path.exists(file_path):
        moodpatterns_db = sqlite3.connect(file_path) #moodpaths uses an SQLite database
        db_cursor = moodpatterns_db.cursor()
        break

    else:
        print("File not found. Please retry.")


# extract the meaningful data from the connected database
# and prepare it for easier manipulation

survey_list = db_cursor.execute("SELECT * FROM survey WHERE missing = 'FALSE'").fetchall() # Get list of finished entries
survey_headings = []
for heading in db_cursor.description: # Get key names
    survey_headings.append(heading[0])
event_list = db_cursor.execute("""SELECT et.event_unixtime, e.event_label 
                                    FROM event as e, event_time as et 
                                    WHERE e.event_id = et.event_id""").fetchall() # Get event times and labels
event_dict = {}
for event in event_list:
    event_dict[event[0]] = event[1] # {event_time: event_label}, makes looking up events using time easier

moods = db_cursor.execute("SELECT id, start, end FROM scales").fetchall() # find all the different mood scale ids used

# make the script slightly more resilient to database format changes
# by dynamically making sure we find the right indices
time_ix = survey_headings.index("alarm_unixtime")
mood_start_ix = survey_headings.index("sad_happy")
mood_end_ix = survey_headings.index(moods[-1][0]) # assuming that moods will at least be in adjacent columns
                                                     # and last mood in the scales table will also be the last column

# port the extracted data to the femto format
# and sort it chronologically

femto = []

for survey in survey_list:
    survey_time = survey[time_ix] # when the survey happened, used multiple times

    # calculate average mood using sad_happy, discontent_content and stressed_relax scores if existent
    mood = 0
    scales_exist = 0 # number of scales that were found to be not None
    for score in survey[mood_start_ix:mood_start_ix+3]:
        if score != None:
            mood = mood + int(score)
            scales_exist += 1
    
    if scales_exist == 0:
        mood = 3 # placeholder mood score if normal calculation didn't work out
    else:
        mood = int(round(mood / scales_exist,0)) # take average of scores and round to an integer
        if mood in range(21): # if mood is between 0 and 20, inclusive
            mood = 1
        elif mood in range(21,41): # if mood is between 21 and 40, inclusive
            mood = 2
        elif mood in range(41,61): # if mood is between 41 and 60, inclusive
            mood = 3
        elif mood in range(61,81): # if mood is between 61 and 80, inclusive
            mood = 4
        elif mood in range(81,101): # if mood is between 81 and 100, inclusive
            mood = 5

    # construct a string from all the other scales 
    note_list = [] # for efficiency, create a list of sentences to add first, then join
    if survey_time in event_dict:
        note_list.append(f"I made this entry due to the following happening: {event_dict[survey_time]}.")
    for i in range(len(moods)):
        # reminder that moods will be of the form (mood_id, mood_low_score_name, mood_high_score_name)

        mood_ix = mood_start_ix + i # find column of the mood scale
        mood_score = survey[mood_ix] # get the score on the scale

        if mood_score != None: # if this scale has a score
            mood_score = int(mood_score)
            mood_lower = moods[i][1] # the adjective for a low score
            mood_higher = moods[i][2] # the adjective for a high score

            # handle 'special' scales
            # external and internal focus
            if mood_lower == "external focus":
                mood_lower = "externally focussed"
                mood_higher = "internally focussed"
            # craving
            elif mood_lower == "craving":
                mood_score = 100 - mood_score # convert so 100 is maximal craving, not minimal
                if mood_score == 0:
                    note_list.append(f"I felt no craving ({mood_score}/100).")
                elif mood_score in range(1,11):
                    note_list.append(f"I felt a slight craving ({mood_score}/100).")
                elif mood_score in range(11,31):
                    note_list.append(f"I felt a bit of a craving ({mood_score}/100).")
                elif mood_score in range(31,51):
                    note_list.append(f"I felt a mild craving ({mood_score}/100).")
                elif mood_score in range(51,71):
                    note_list.append(f"I felt a moderate craving ({mood_score}/100).")
                elif mood_score in range(71,91):
                    note_list.append(f"I felt a heavy craving ({mood_score}/100).")
                elif mood_score in range(91,101):
                    note_list.append(f"I felt a very heavy craving ({mood_score}/100).")
                continue # move to next scale
            # all other scales
            # lower mood
            if mood_score in range(0,11): # if mood is between 0 and 10, inclusive
                note_list.append(f"I felt very {mood_lower}.")
            elif mood_score in range(11,21): # if mood is between 11 and 20, inclusive
                note_list.append(f"I felt quite {mood_lower}.")
            elif mood_score in range(21,31): # if mood is between 21 and 30, inclusive
                note_list.append(f"I felt moderately {mood_lower}.")
            elif mood_score in range(31,41): # if mood is between 31 and 40, inclusive
                note_list.append(f"I felt kind of {mood_lower}.")
            elif mood_score in range(41,46): # if mood is between 41 and 45, inclusive
                note_list.append(f"I felt slightly {mood_lower}.")
            # neither mood
            elif mood_score in range(46,55): # if mood is between 46 and 54, inclusive
                note_list.append(f"I felt neither {mood_lower} nor {mood_higher}.")
            # higher mood
            elif mood_score in range(55,60): # if mood is between 55 and 59, inclusive
                note_list.append(f"I felt slightly {mood_higher}.")
            elif mood_score in range(60,70): # if mood is between 60 and 69, inclusive
                note_list.append(f"I felt kind of {mood_higher}.")
            elif mood_score in range(70,80): # if mood is between 70 and 79, inclusive
                note_list.append(f"I felt moderately {mood_higher}.")
            elif mood_score in range(80,90): # if mood is between 80 and 89, inclusive
                note_list.append(f"I felt quite {mood_higher}.")
            elif mood_score in range(90,101): # if mood is between 90 and 100, inclusive
                note_list.append(f"I felt very {mood_higher}.")

    note = " ".join(note_list)

    femto.append({
        "time": survey_time,
        "mood": mood,
        "note": note
    })

femto.sort(key=lambda x: x["time"])             # normalise chronological sorting


# finally, export the ported data
# to the femto-{version}.json file

with open("femto-v{v}.json".format(v=version), "w") as stream:
    json.dump(femto, stream, indent=4)
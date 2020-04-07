# mt-hopper Templates



# Backup Files

The following apps support *backing up and restoring* via one or more **user-owned** files.

The sections in their respective files which are meaningful towards the purpose of `mt-hopper` are exemplified and explained in the following.


## Daylio

Daylio's backup comes as a single `.json` file, `base64`-ed and aliased as `backup_{yyyy}_{mm}_{dd}.daylio:`
```python
"dayEntries": 
[
    {
        "id": <int, entry ID>,  // this ID is obviously unique, but not numbered chronologically or even starting from 0 or 1...
        "minute": <int>,
        "hour": <int>,
        "day": <int>,
        "month": <int>,
        "year": <int>,
        "datetime": <int, UNIX-epoch timestamp>,
        "timeZoneOffset": <int, time zone offset from GMT>,
        "mood": <int, mood ID as specified in "customMoods">,
        "note": <str>,
        "tags": [
            <int, tag ID as specified in "tags">,
            ...]
    },
    ...]

"customMoods":
[
    {
        "id": <int, mood ID as mentioned in "dayEntries">,
        "custom_name": <str>,
        "mood_group_id": <int, sets the mood group [x/5] the custom mood details: 1=best ... 5=worst>,
        "mood_group_order": <int>,
        "icon_id": <int>,
        "predefined_name_id": <int>,
        "is_active": <bool>,
        "createdAt": <int, UNIX-epoch timestamp>
    },
...]

"tags":
[
    {
        "id": <int, tag ID as mentioned in "dayEntries">,
        "name": <str>,
        "createdAt": <int, UNIX-epoch timestamp>,
        "icon": <int>,
        "order": <int>,
        "state": <int>,
        "id_tag_group": <int>
    },
]
```

In this file, the core mood data is represented by:
-   `customMoods["mood_group_id"]`, as the core **mood / 5** data for the entry
-   `dayEntries["note"]`, as the core **note** string for the entry

Other meaningful data is represented by:
-   `tags["name"]`, as the event tags for the entry


## Journey


## MoodPatterns


## Pixels


## eMoods



# Export Files

Unlike the ones mentioned above, the following apps support *only exporting* to one or more **user-owned** files.       
However, they were still considered, in order to allow users to migrate to a more data-conscious app without having to give up all their past data.

The sections in their respective files which are meaningful towards the purpose of `mt-hopper` are exemplified and explained in the following.


## MoodPath

MoodPath's export file comes as a `.zip` archive storing 3 `.csv` files:
-   `answers.csv`
-   `happiness_scores.csv`
-   `notes.csv`

`happiness_scores.csv`:
```
happiness_score, entry_time

<int: 1=worst, 5=best>,
<yyyy-mm-dd hh:mm:ss +tmzn>
```

`notes.csv`:
```
content, entry_time

<str>, <yyyy-mm-dd hh:mm:ss +tmzn>
```

`answers.csv`:
```
answered_at, question, answer, intensity

<yyyy-mm-dd hh:mm:ss +tmzn>,
<str>,
<yes/no>,
<int: 0=lightest ... 5=heaviest>
```
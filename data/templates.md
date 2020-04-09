# mt-hopper Templates


---

# Backup Files

The following apps support *backing up and restoring* via one or more **user-owned** files.

The sections in their respective files which are meaningful towards the purpose of `mt-hopper` are exemplified and explained in the following.


## Daylio

Daylio's backup comes as a single `.json` file, `base64`-ed and aliased as `backup_{yyyy}_{mm}_{dd}.daylio`:
```python
{
  "dayEntries":
  [
    {
      "id":                 <int, entry ID>,   # this ID is obviously unique, but not numbered chronologically or even starting from 0 or 1...
      "minute":             <int>,
      "hour":               <int>,
      "day":                <int>,
      "month":              <int>,
      "year":               <int>,
      "datetime":           <int, UNIX-epoch timestamp in milliseconds>,
      "timeZoneOffset":     <int, time zone offset from GMT>,
      "mood":               <int, mood ID as specified in "customMoods">,
      "note":               <str>,
      "tags": [
                            <int, tag ID as specified in "tags">,
          ...]
    },
  ...],
  "customMoods":
  [
    {
      "id":                 <int, mood ID as mentioned in "dayEntries">,
      "custom_name":        <str>,
      "mood_group_id":      <int, sets the mood group [x/5] the custom mood details: 1=best ... 5=worst>,
      "mood_group_order":   <int>,
      "icon_id":            <int>,
      "predefined_name_id": <int>,
      "is_active":          <bool>,
      "createdAt":          <int, UNIX-epoch timestamp>
    },
  ...],
  "tags":
  [
    {
      "id":                 <int, tag ID as mentioned in "dayEntries">,
      "name":               <str>,
      "createdAt":          <int, UNIX-epoch timestamp>,
      "icon":               <int>,
      "order":              <int>,
      "state":              <int>,
      "id_tag_group":       <int>
    },
  ...],
...}
```

In this file, the core mood data is represented by:
- `customMoods["mood_group_id"]`, as the core **mood / 5** data for the entry
- `dayEntries["note"]`, as the core **note** string for the entry

Other meaningful data is represented by:
- `tags["name"]`, as the event tags for the entry


## Journey


## MoodPatterns


## Pixels

Pixels' backup comes as a single, clear `.json` file:
```python
[
  {
    "date":   <str: yyyy-mm-dd>
    "mood":   <int: 1=worst ... 5=best>
    "emotions": [
              <str>,
    ...]
    "notes":  <str>
  },
...]
```

In this file, the core mood data is represented by:
- `mood`, as the core **mood / 5** data for the day
- `notes`, as the core **note** string for the day

Other meaningful data is represented by:
- `emotions`, as the emotion tags for the day


## eMoods



---

# Export Files

Unlike the ones mentioned above, the following apps support *only exporting* to one or more **user-owned** files.       
However, they were still considered, in order to allow users to migrate to a more data-conscious app without having to give up all their past data.

The sections in their respective files which are meaningful towards the purpose of `mt-hopper` are exemplified and explained in the following.


## MoodPath

MoodPath's export file comes as a `.zip` archive storing 5 `.csv` files:
- `answers.csv`
- `emotions.csv`
- `happiness_scores.csv`
- `notes.csv`
- `situations.csv`

`happiness_scores.csv`:
```
happiness_score, entry_time

<int: 0=worst ... 4=best>,
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

`emotions.csv`:
```

```

`situations.csv`:
```

```

In these files, the core mood data is represented by:
- `happiness_scores.csv: happiness_score`, as the core **mood / 5** data for the entry
- `notes.csv: content`, as the core **note** string for the entry

Other meaningful data is represented by:
- `answers.csv: question, answer, intensity`, as relevant feeling data for each prompted entry



---

# Approach

Generally, the **core mood data** includes any form of basic emotional data which is implemented by fairly all considered apps, and which is therefore expected to be retained across all formats in a uniform and machine-readable way -- as per the current version of the FEMTO specifications stored in `femto-spec.md`.

On the other hand, the **other meaningful data** represents all other information which is more unique to individual implementations, yet still relevant to an accurate and thorough description of the mood.
While this data is not ported via any of the fundamental FEMTO fields, it is still humanely meaningful: therefore, this is usually included in the `"note"` field as a simple, human-readable snippet of information extracted out of whatever value it used to represent.
# MFemto-hopper:

### A tool for improving data portability between mood tracking apps.

![coral](img/coral/coral.png)

###### ICON BY [MADE X MADE](https://thenounproject.com/christian933) ON [THE NOUN PROJECT](https://thenounproject.com); &copy; 2020 [CC BY 3.0](https://creativecommons.org/licenses/by/3.0)


# Introduction

There are so many mood tracker apps around, and for a reason: they're all different in character, features and purpose, and each of them is appealing in its own unique and stylish way.        
Among all the different designs, however, we recognise a handful of essential features they all have in common:
-   some kind of **"mood out of x"** rating
-   the option to **write down** your thoughts and feelings as a **note**

Despite their fundamental similarities, transferring this extremely basic data between the various apps is often way too rough: they all export it in different formats and with different internal structures, and not all of them even support a *truly* user-owned backup in the first place.      
Using different formats is okay -- given the natural massive differences between them, it's obvious that the optimal ways of storing the data they record will be multiple and diverse.

However, this makes switching from a mood tracker to another, or "hopping" (like *distro-hopping,* hence the name), much rougher than it should be: too often, it means giving up all your progress because of the incompatible formats.
Plus, everyone is different and in continuous growth, and nobody expects any app to appeal to *all* the users *all* the time: people should be free to "hop" between mood trackers at their own discretion, all while still being able to retain at least some of their data.

That's why **Femto-hopper** exists: to enable users to translate that basic mood data so that they can keep it during their explorations of the mood tracker scene.     


# Composition

The project is functionally made up of two main elements:
-   **FEMTO,** the common stanadard that specifies what data fields are retained throughout the conversion and how
-   the **scripts** themselves, which operate the conversions to and from the FEMTO standard

This "central" design (all formats to FEMTO, from FEMTO to all formats) was preferred over the "mesh" alternative (each format to each other format) for its **uniformity and scalability,** at the cost of thoroughness.       
Otherwise, the number of individual scripts needed would increase quadratically, which would make scaling this project beyond a handful of apps a nightmare; instead, the two architectures even out at just 3 apps, and past that point the needed scripts only grow linearly, 2 more per each new app.

Plus, this allows for a common standard with a clear set of rules (specified in `femto-spec.md`) and avoids the chaos that would result from having to come up with *10* new conversion strategies just to include the 6th app -- and, at any rate, some data loss is expected and unavoidable, given the innate differences between the apps.

---

The repository is composed of:
-   `data`, a folder for the user to store file backups at their discretion
    -   `sample`, which hosts all the sample exports we have collected for documenting the different formats
        -   `in`, for the files exported by the apps and to feed the program
        -   `out`, for the files spit out by the program and to import to the apps
    -   `templates.md` is where we keep a detailed record of all the formats we've included
-   `src`, divided in:
    -   `femto-in`, storing the scripts that convert *from* the various export formats *to* the FEMTO standard
    -   `femto-out`, storing the scripts that convert *from* the FEMTO standard *to* the various import formats
    -   `femto-spec.md` for the current FEMTO specifications
-   `img`, with the images for this readme


# Interface

This project is currently just a collection of scripts, and barely represents anything more than a simple proof of concept -- however, the first versions of the UI will be represented by a bare-bones command-line interface: feed the file to the program, then specify its origin and destination apps.     
In this design, all the data-file handling would have to be operated by the user.

In the indefinite future, if the project gains enough track, it could be ported to Android and iOS apps for a more intuitive, natural and seamless in-place usage: simply export the data from the old app, convert it in a pinch, and import it to the new one.


# Contribute

Whether you're a user or a developer of a mood tracker, we look forward to including your app into our tool!

## As a user
If you use a mood tracker app and you want it to be included in Femto-hopper, let us know by taking this [Typeform Survey](https://ciakkig.typeform.com/to/FgAHqZ) so that we can steer our efforts towards involving it.

The survey takes about 3 minutes to complete, and never asks you about any emotional data -- only about the *apps* themselves.

## As a dev
If you're developing or maintaining a mood tracker app, we're looking forward to welcoming it in our network.

As a general guideline, it will need a backup & restore feature relying on a clear file that's owned, accessible and handleable by the user.    
We recommend making such a feature free, but we recognise it may require funding.       
You can use whatever format you're most comfortable with, but we strongly suggest **`JSON`** for its popularity, transparency and flexibility.

At any rate, make sure to [get in touch](mailto:ciakki.g@gmail.com) with us so we can get you and your app involved!


# License

**Copyright (C) 2020 Giorgio Ciacchella, Darren Fielding, Zoltán Kiss**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License at `COPYING` or https://www.gnu.org/licenses/#GPL for more details.
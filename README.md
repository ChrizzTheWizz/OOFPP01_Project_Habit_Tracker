# Project: HabitTracker

## Table of Contents
1. [About the project](#About-the-project)
2. [Requirements](#Requirements)
3. [Installation](#Installation)
4. [Usage / How to](#Usage-/-How-to)
5. [Contributing](#Contributing)


## About the project
This Habit Tracker App is designed to help you keep track of your self-set goals. Activities that are to become regular daily or weekly habits can be created and evaluated.

Depending on whether you want to establish daily or weekly habits, once you have completed the activity with conviction and motivation, you can check it off in the app as 'successfully completed'. With the app you can always keep track of the daily/weekly goals you have set yourself, analyse them individually or display an overview. If you don't miss a day (for daily habits) or a week (for weekly habits) and tick off the task accordingly, you generate so-called streaks, which are also evaluated.

To get a first impression, you can also create randomly generated habits. These cannot be edited, but they give you an insight into how the programme works.

Have fun and success. 

IMPORTANT:
This app was developed as part of a portfolio assignment for my Data Science degree and contains the basic requirements according to the assignment. Further development is not planned.

## Requirements

**General:** 
This app was written in Python. Make sure you have Python 3.7+ installed on your device. 
You can download the latest version of Python [here](https://www.python.org/downloads/). 

**Packages:**
* [questionary](https://github.com/tmbo/questionary) (install via "pip install questionary")
* [tabulate](https://github.com/astanin/python-tabulate) (install via "pip install tabulate)


## Installation

**How To:**<br>
The easiest way to use this app is to download the following files:
/bin/config.txt
/habittracker/__init__.py
/habittracker/analyze.py
/habittracker/display.py
/habittracker/habits.py
/habittracker/main.py
/habittracker/rand_habits.py
/habittracker.py
/readme.md

Make sure to keep the folder structure in place.


## Usage / How to

In the following, you will get an overview of the main functionalities and how to access them.

### 0. Start

* Run this app within your terminal using "python habittracker.py"
* You need to be in the directory where you downloaded this app
* As soon as the application is started, it checks whether the folder structure according to the config.txt already exists. If not the basics are created.
* Depending on existing entries, the possible functions are displayed

---
### 1. Create a habit
* A new habit consists of a unique name, consisting of a maximum of two words, a specification, i.e. a more detailed description of the habit for your own use, and a periodicity in which the habit must be fulfilled.
* Tracking starts on the day the habit is put on. An individual setting for when a habit starts is not available in the current version. Furthermore, no end date can be set. If a habit is no longer of interest, it can be deleted.
* If a habit is created, it is automatically added to the overview.
* Each time the application is started, the last entry of all habits are checked. If there is an n-multiple of the periodicity between the last entry and the current date, the missing entries are evaluated as "breaking the habit".
* For each habit there is a separate file in which it is recorded when the habit was fulfilled or broken according to the periodicity.

---
### 2. Check-off habits
* Only in the case that a habit (see 1.) has been created, it can also be checked off. A list of all habits is displayed for this purpose.
* A habit can only be checked-off once per defined period. If a habit is selected twice, a corresponding feedback is given. With the current version, there is no filtering of the displayed habits beforehand.
* Example Demo Data cannot be checked-off.

---
### 3. Analyzing habits
* Several predefined analysis views are available.
* For detailed analysis you need to choose a habit from the displayed list. The content of the tracking file stored for this habit is then displayed.

---
### 3. Deleting habits
* Several predefined analysis views are available.
* For detailed analysis you need to choose a habit from the displayed list. The content of the tracking file stored for this habit is then displayed.

---
### 4. Options
* Random habits (daily/weekly) can be generated here for testing purposes of the analysis module.
* Further setting options are not possible with the current version

---
### 5. Instructions
* Opens the readme-file

---
### 6. Quit
* Terminates the app
  

## Contributing 
With reference to the fact that this app was created in the course of my studies and I am therefore in a constant learning process, I am happy to receive any feedback.
So please feel free to contribute pull requests or create issues for bugs and feature requests.

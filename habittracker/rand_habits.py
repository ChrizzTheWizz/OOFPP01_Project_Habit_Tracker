from datetime import date, timedelta
import random
import pandas as pd
import numpy as np

from habittracker import habits

list_random_doings = [
    "Python Coding",
    "Studying DataScience",
    "Implement Testing",
    "Fight Trojan",
    "Ask tutor",
    "Solve datetime-issues",
    "Be grateful",
    "Learn Klingon",
    "Having clown-breakfast",
    "Use docstrings",
    "Stop non-smoking",
    "Crack code",
    "Automate stuff",
    "Feed Godzilla",
    "Fight sexism",
    "Fight racism",
    "Dream interstellar",
    "Follow Pippi-Longstocking"
]


def create_random_habit(period, path_habit_overview, absolute_directory_habit_files):
    """

    :param period: Periodicity of the random habit ('daily' or 'weekly')
    :param path_habit_overview: Path where .json-habit-overview-file should be saved according to config.txt
    :param absolute_directory_habit_files: (Absolute) Path to habit file with datetime-relating data
    :return:
    """
    global list_random_doings

    name = ""
    # creating empty list for existing habit names
    names_existing_habits = []
    # filling list with existing habit names
    for habit in habits.list_habit_instances:
        names_existing_habits.append(habit.name)
    # random habit name from list

    name = list_random_doings[random.randint(0, len(list_random_doings)-1)]
    # if name has already be chosen (by user or random creation): choose new name
    while name in names_existing_habits:
        name = list_random_doings[random.randint(0, len(list_random_doings) - 1)]
    # file path to habit file
    file = f"{absolute_directory_habit_files}\\{name.replace(' ', '_').lower()}.json"
    # default specification for demo data
    spec = "! DEMO ! DATA !"

    # random data starts 2021/01/01 at the earliest
    start = date(2021, 1, 1)
    # random data ends 2021/06/30 at the latest
    end = date(2021, 6, 30)

    # random calculation of start and end date
    factor_start = random.uniform(0, 0.5)
    factor_end = random.uniform(0.51, 1)
    start_habit = start + (end-start) * factor_start
    end_habit = start + (end-start) * factor_end

    # creating instance
    new_instance = habits.Habit(name, spec, period, file, start_habit)
    # adding habit to habit overview
    new_instance.add_to_overview(path_habit_overview)

    # empty list for dataframe values
    values_for_dataframe = []
    # date index for dataframe based on random start and end as well as the periodicity
    index_for_dataframe = pd.date_range(start_habit, end_habit, freq=period)

    # for every possible value on basis of the number of index entries: random true or false
    for n in range(0, len(index_for_dataframe)):
        random_check_off = "Yes" if random.getrandbits(1) == 1 else "No"
        if random_check_off == "Yes":
            # if randomly 'Yes': generating random time for check-off-date timestamp
            check_off_hours = random.randint(0, 23)
            check_off_minutes = random.randint(0, 59)
            check_off_seconds = random.randint(0, 59)
            check_off_date = index_for_dataframe[n] + timedelta(hours=check_off_hours,
                                                                minutes=check_off_minutes,
                                                                seconds=check_off_seconds)

        else:
            # if randomly false: set check-off-date timestamp np.nan (none)
            check_off_date = np.nan

        # adding either random true + check-off-date or false + np.nan to dataframe
        values_for_dataframe.append([random_check_off, check_off_date])

    # creating dataframe on basis of randomly created index and randomly created values
    df_habit = pd.DataFrame(values_for_dataframe, columns=["Checked-off", "Check-off date"], index=index_for_dataframe)
    # saving dataframe to .json file
    df_habit.to_json(new_instance.file, date_format='iso')

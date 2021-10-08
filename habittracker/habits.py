import os
from datetime import datetime, timedelta, timezone
import pandas as pd
from os.path import exists
import pytz


global list_habit_instances


def create_habit_overview(path_habit_overview):
    """
    Creating a .json-habit-overview-file containing
    - Name (string)
    - Specification (string)
    - Periodicity (string)
    - Created on (datetime)
    - File Directory (string)
    for every existing / created habit.
    This file serves as a basis for re-instantiating the habits

    :param path_habit_overview: Path where .json-habit-overview-file should be saved according to config.txt
    :return: Boolean --> False if file can not be created - true if file has been successfully created
    """
    df_habit_overview = pd.DataFrame(
        columns=["Name", "Specification", "Periodicity", "Created on", "File Directory"])

    if not isinstance(path_habit_overview, str):
        raise TypeError("Path to habit overview needs to be a string!")
    elif path_habit_overview[-5:] != ".json":
        raise ValueError("File ist not a .json-file")
    else:
        invalid_characters = ["#", "%", "&", "<", ">", "%", "'", '"', "=", "@", "?", "*", "€"]
        for character in path_habit_overview:
            if character in invalid_characters:
                raise ValueError("Non-valid characters found in path / filename!")

    try:
        df_habit_overview.to_json(path_habit_overview, date_format='iso')
    except OSError:
        print(f"Problems with your operating system! Make sure this app can write to '{path_habit_overview}!")
        return False
    else:
        return True


def read_habit_overview(path_habit_overview):
    """
    Reads .json-habit-overview-file and creates a pandas dataframe

    :param path_habit_overview: Path where .json-habit-overview-file should be saved according to config.txt
    :return: pandas dataframe
    """
    if not os.path.exists(path_habit_overview):
        raise FileNotFoundError("File cannot be found!")
    elif path_habit_overview[-5:] != ".json":
        raise ValueError("File is not a .json file!")
    else:
        try:
            df_habit_overview = pd.read_json(path_habit_overview)
        except ValueError:
            raise ValueError("Unexpected character found in file. Could not load habit overview!")
        else:
            return df_habit_overview


def create_habit(habit_attributes, path_habit_overview, absolute_directory_habit_files):
    """
    Creating new instance of the class habit

    :param habit_attributes: user generated input for name, specification and periodicity
    :param path_habit_overview: Path where .json-habit-overview-file should be saved according to config.txt
    :param absolute_directory_habit_files: (Absolute) Path to habit file with datetime-relating data
    :return: Status of creating new habit (string)
    """

    if not isinstance(habit_attributes, tuple):
        raise AttributeError("Attributes must be delivered in a tuple!")
    elif len(habit_attributes) != 3:
        raise AttributeError("Exactly three parameters must be delivered within list!")

    # converting list input into separate variables
    name = habit_attributes[0]
    spec = habit_attributes[1]
    period = habit_attributes[2]
    file = f"{absolute_directory_habit_files}\\{name.replace(' ', '_').lower()}.json"

    # instantiate habit
    habit = Habit(name, spec, period, file)
    # adding habit to habit overview
    status_called_function = habit.add_to_overview(path_habit_overview)
    if status_called_function.split(" ")[0] == "ERROR:":
        # if an error occurred while adding to overview: Remove habit
        habit.remove_habit(path_habit_overview)
        status = "ERROR: Could not create new habit!"
        return status
    else:
        status = "Successfully created a new habit. Good luck!"
        return status


def re_instantiate_habits(df_habit_overview):
    """
    Re-instantiating the habits according to pandas dataframe based on the .json-habit-overview-file

    :param df_habit_overview: pandas dataframe with all existing / created habits
    :return:
    """

    # converting date-values from pandas default type to datetime
    df_habit_overview["Created on"] = pd.to_datetime(df_habit_overview["Created on"])
    # creating list of habits for looping
    habit_list = df_habit_overview.values.tolist()

    current_num_habit = 1
    for habit in habit_list:
        name = habit[0]
        spec = habit[1]
        period = habit[2]
        created = habit[3]
        file = habit[4]
        # loop variable for instantiating
        globals()[f"habit_{current_num_habit}"] = Habit(name, spec, period, file, created)
        current_num_habit += 1

    for habit in list_habit_instances:
        # updates missed check-off dates in habit file
        status_called_function = habit.auto_update_file()
        print(status_called_function)

    status = f"Re-instantiated {len(habit_list)} habits."

    return status

class Habit:
    """
    Provides
    - adding to overview
    ...
    """

    def __init__(self, name, spec, period, file, created=datetime.now(pytz.utc)):
        # attributes
        self.name = name
        self.spec = spec
        self.period = period
        self.file = file
        self.created = created

        if not exists(self.file):
            empty_df_habit = self.create_dataframe()
            empty_df_habit.to_json(self.file, date_format='iso')

        # updating running habit list
        list_habit_instances.append(self)

    def add_to_overview(self, path_habit_overview):
        """

        :param path_habit_overview: Path where .json-habit-overview-file should be saved according to config.txt
        :return: Status (string)
        """
        # create dictionary for new entry
        new_habit = {"Name": self.name, "Specification": self.spec, "Periodicity": self.period,
                     "Created on": self.created, "File Directory": f"{self.file}"}

        try:
            # load existing habit overview file
            df_overview = pd.read_json(path_habit_overview)
            # add dictionary to habit overview
            df_overview = df_overview.append(new_habit, ignore_index=True)
            # save habit overview
            df_overview.to_json(path_habit_overview, date_format='iso')
            # return status
            status = "Added habit to overview"
            return status
        except ValueError:
            # Create and return error message
            status = "ERROR: Couldn't add habit to overview!"
            return status

    def create_dataframe(self, start="init", end="init"):
        """

        :param start:
        :param end:
        :return:
        """

        if type(start) != type(end):
            raise ValueError("Both start and end must be of same type")
        if end < start:
            raise ValueError("End date is before start date!")

        """EMPTY LIST FOR FALSE VALUES"""
        df_values = []
        if start == "init" and end == "init":
            df_index = []
        else:
            df_index = pd.date_range(start, end, freq=self.period)
            for i in df_index:
                df_values.append(["No", pd.np.nan])

        df_habit = pd.DataFrame(df_values, columns=["Checked-off", "Check-off date"], index=df_index)

        return df_habit

    def auto_update_file(self):
        """
        Auto-updating the habit:
        Reading the habit file (.json) and comparing the last date (if available) with the current day
        and calculate possible missed period(-s):
        If period(-s) have been missed: Register failures ("No" in column) and save data to habit file
        If habit belongs to demo data: Don't auto-update habit and return error message (--> demo data)
        If no periods have been missed: Don't auto-update habit and return message (--> period still running)

        :return: Status (ERROR-Message or Success)
        """
        # save current day for the need for auto-updating
        current_day = datetime.now(pytz.utc)

        # read existing habit data
        df_habit = pd.read_json(self.file)
        if df_habit.empty:
            # if no data is in file set the last date to:
            # for daily habits: one day before start date
            # for weekly habits: seven days (1 week) before start date
            df_last_date = self.created.date() - timedelta(1) if self.period == "D" else \
                self.created.date() - timedelta(7)
        else:
            # else read last date from dataframe
            df_last_date = df_habit.index[-1].date()

        # if habit belongs to demo data
        if self.spec == "! DEMO ! DATA !":
            # return appropriate status
            status = f"Habit {self.name}: No auto-update for demo data"
            return status

        # if check-off for the period still possible!
        # for daily habits: last date entry is more than two days ago
        # for weekly habits: last date entry is more than two weeks (14 days) ago
        elif (current_day.date() - df_last_date <= timedelta(2) and self.period == "D") or \
                (current_day.date() - df_last_date <= timedelta(14) and self.period == "7d"):
            # return appropriate status
            status = f"Habit {self.name}: No auto-update needed - already checked-off or " \
                     f"check-off for only running period still possible!"
            return status
        else:
            # start auto update preparation
            # set start date of missed periods
            # for daily habits: one day after the last date
            # for weekly habits: seven days after the last date
            start_date = df_last_date + timedelta(1) \
                if self.period == "D" else df_last_date + timedelta(7)

            # set end date of missed periods
            # for daily habits: one day before today
            # for weekly habits: seven days before today
            end_date = current_day.date() - timedelta(1) \
                if self.period == "D" else current_day.date() - timedelta(7)

            # create dataframe which will be added to the existing one
            add_df_habit = self.create_dataframe(start_date, end_date)
            # append existing dataframe
            df_habit = df_habit.append(add_df_habit)
            # save new dataframe
            df_habit.to_json(self.file, date_format='iso')

            # return appropriate status
            status = f"Habit {self.name}: Auto-Update for {start_date} - {end_date} successfully completed."
            return status

    def check_off_habit(self):
        """
        Checking-off the habit:
        Reading the habit file (.json) and comparing the last date (if available) with the current day:
        If period is running and check-off is possible: Check-off habit ("Yes" in column) and save data to habit file
        If habit belongs to demo data: Don't check-off habit and return error message (--> demo data)
        If period already checked-off: Don't check-off habit and return error message (--> already checked-off)

        :return: Status (ERROR-Message or Success)
        """

        current_day = datetime.now(pytz.utc)

        # read existing habit data
        df_habit = pd.read_json(self.file)

        if df_habit.empty:
            # if no data is in file set the last date to:
            # for daily habits: one day before start date
            # for weekly habits: seven days (1 week) before start date
            df_last_date = current_day.date() - timedelta(1) \
                if self.period == "D" else current_day.date() - timedelta(7)
        else:
            # else read last date from dataframe
            # df_habit.index = pd.to_datetime(df_habit.index)
            df_last_date = df_habit.index[-1].date()
            # df_last_date = df_last_date.to_pydatetime()

        # if habit belongs to demo data
        if self.spec == "! DEMO ! DATA !":
            # create error message
            status = "ERROR: Can't check-off demo data! For further information read the instructions."
            return status
        # if habit already has been checked-off in running period
        # for daily habits: the same day
        # for weekly habits: within the last six
        elif (df_last_date == current_day.date() and self.period == "D") or \
                (current_day.date() - df_last_date <= timedelta(6) and self.period == "7d"):
            # create error message
            status = "ERROR: Can't check-off twice a habit!"
            return status

        else:
            # create dictionary with check-off data for dataframe
            check_off = {"Checked-off": "Yes", "Check-off date": current_day}
            # create new date-index-list depending on periodicity and last date in dataframe
            # for daily habits: the next day
            # for weekly habits: the next week (+7 days)
            df_new_date = [df_last_date + timedelta(1) if self.period == "D" else
                           df_last_date + timedelta(7)]
            # create new dataframe with calculated data
            df_check = pd.DataFrame(check_off, index=df_new_date)
            # append new dataframe to existing dataframe
            df_habit = df_habit.append(df_check)
            df_habit.to_json(self.file, date_format='iso')

            # return appropriate status
            status = "Successfully checked-off your habit!"
            return status

    def analyze_habit(self):
        """
        Defines a default <list / dictionary> for analyze-module as well as counts longest streak

        :return:
        """

        # initialize main variables for analysis
        start_streak = "-"
        end_streak = "-"
        period_longest_streak = "-"
        streak, max_streak = 0, 0

        # transform datetime to string in user-friendly format
        created_on = self.created.strftime("%Y-%m-%d")

        # read existing habit data
        df_habit = pd.read_json(self.file)

        # if habit file is empty
        if df_habit.empty:
            count_checked_off_true = 0
            percentage_checked_off_periods = "0%"
            number_of_periods = 0

        # if habit data is available
        else:
            # count the number of checked-off (column 'checked-off' = 'Yes') entries
            count_checked_off_true = df_habit[df_habit["Checked-off"] == "Yes"]["Checked-off"].count()

            # if no recent period has been checked-off
            if count_checked_off_true == 0:
                pass
            # if period(-s) have been successfully checked-off
            else:
                # start analysis (--> longest streak)
                for n in range(0, len(df_habit)):
                    # for every entry check if the period has been successfully checked-off
                    if df_habit.iloc[n]["Checked-off"] == "Yes":
                        # if period has been checked-off increase temporary variable 'streak' by one
                        streak += 1
                        if streak == 1:
                            # if it's the beginning of a streak remember the start-date of that streak
                            start_streak = df_habit.index[n].date()
                        if n == len(df_habit) - 1:
                            # if the entry belongs to a streak and it's the last entry: Remember the date as end-date
                            end_streak = df_habit.index[n].date()
                            if streak > max_streak:
                                # if the current streak is longer: Transfer streak-data to final variables
                                max_streak = streak
                                period_longest_streak = f"{start_streak} - " \
                                                        f"{end_streak if self.period == 'D' else end_streak + timedelta(6)}"
                    elif df_habit.iloc[n]["Checked-off"] == "No" and streak >= 1:
                        # if streak has been broken save the last date entry as end-date
                        end_streak = df_habit.index[n - 1].date()
                        if streak > max_streak:
                            # if the current streak is longer: Transfer streak-data to final variables
                            max_streak = streak
                            period_longest_streak = f"{start_streak} - " \
                                                    f"{end_streak if self.period == 'D' else end_streak + timedelta(6)}"
                        # reset temporary variable 'streak' to zero
                        streak = 0
                    else:
                        # if there's no running streak continue with next entry
                        pass

            percentage_checked_off_periods = f"{((count_checked_off_true / len(df_habit)) * 100).round(2)}%"
            number_of_periods = len(df_habit)

        habit_analysis = {"Name": self.name,
                          "Specification": self.spec,
                          "Periodicity": "daily" if self.period == "D" else "weekly",
                          "Created on": created_on,
                          "Number of periods": number_of_periods,
                          "Checked-off periods": count_checked_off_true,
                          "Percentage checked-off periods": percentage_checked_off_periods,
                          "Longest Streak": max_streak,
                          "Period Longest Streak": period_longest_streak}

        return habit_analysis

    def remove_habit(self, path_habit_overview):
        """
        Removes existing habit according to user input

        :param path_habit_overview: Path where .json-habit-overview-file should be saved according to config.txt
        :return: Status (ERROR-Message or Success)
        """

        # ERROR-Handling habit file
        try:
            os.remove(self.file)
        except OSError:
            status = "Habit file could not be removed! Habit not deleted!"
            return status

        # load existing habit overview file
        df_overview = pd.read_json(path_habit_overview)
        # remove habit from overview
        df_overview = df_overview.drop(df_overview[df_overview.Name == self.name].index)
        # save updated habit overview file
        df_overview.to_json(path_habit_overview, date_format='iso')

        # remove instance from current and global habit list
        list_habit_instances.remove(self)

        del self
        status = "Habit successfully deleted"
        return status

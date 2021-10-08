import sys
import os
import unittest
import pandas as pd
import numpy as np
from datetime import date, datetime
from habittracker import habits

# insertion to sys.path to be able to import the modules to be tested
path = os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + "habittracker")
sys.path.insert(0, path)


class TestHabitsFunctions(unittest.TestCase):
    def setUp(self) -> None:
        habits.list_habit_instances = []
        list_of_test_files = ["test_habits_overview_testcase00.json",
                              "test_habits_overview_testcase01.json",
                              "test_habits_overview_testcase02.json",
                              "test_habits_overview_testcase03.json",
                              "test_habits_overview_testcase04.json",
                              "test_habits_overview_testcase05.json",
                              "testcase04.json",
                              "test_habits_habit_testcase01.json",
                              "test_habits_habit_testcase04.json",
                              "test_habits_habit_testcase05-1.json",
                              "test_habits_habit_testcase05-2.json",
                              "test_habits_habit_testcase05-3.json",
                              ]
        for file in list_of_test_files:
            if os.path.exists(file):
                os.remove(file)

    def test_create_habit_overview(self):
        # test: create overview with valid filename
        status = habits.create_habit_overview("test_habits_overview_testcase00.json")
        self.assertTrue(status)

        # test: create overview with invalid filename
        with self.assertRaises(TypeError):
            habits.create_habit_overview(2)
        with self.assertRaises(ValueError):
            habits.create_habit_overview("test_habits_overview_no_ending")
            habits.create_habit_overview("habits@overview")
            habits.create_habit_overview("habits$overview")
            habits.create_habit_overview("<habitsoverview>")

        # test: write into a directory that doesn't exist
        status = habits.create_habit_overview("test_habits_dir\\habits_overview.json")
        self.assertFalse(status)

    def test_read_habit_overview(self):
        # create non-empty overview
        habits.create_habit_overview("test_habits_overview_testcase01.json")
        habit01 = habits.Habit("Testcase01", "Habits Testcase 01", "D", "test_habits_habit_testcase01.json")
        habit01.add_to_overview("test_habits_overview_testcase01.json")

        # create empty overview
        habits.create_habit_overview("test_habits_overview_testcase02.json")

        # create empty overview and manipulate to non-json-conforming format
        habits.create_habit_overview("test_habits_overview_testcase03.json")
        with open("test_habits_overview_testcase03.json", "w") as file_overview:
            file_overview.write("This is non { conforming } text for a .json-file!")

        # test: load non-empty overview
        df_habit_overview = habits.read_habit_overview("test_habits_overview_testcase01.json")
        self.assertFalse(df_habit_overview.empty)

        # test: load empty overview
        df_habit_overview01 = habits.read_habit_overview("test_habits_overview_testcase02.json")
        self.assertTrue(df_habit_overview01.empty)

        # test: load created overviews with false file ending --> rename existing files
        os.rename("test_habits_overview_testcase01.json", "test_habits_overview_testcase01.jpeg")
        os.rename("test_habits_overview_testcase02.json", "test_habits_overview_testcase02.xls")
        os.rename("test_habits_overview_testcase03.json", "test_habits_overview_testcase03")
        with self.assertRaises(ValueError):
            habits.read_habit_overview("test_habits_overview_testcase01.jpeg")
            habits.read_habit_overview("test_habits_overview_testcase02.xls")
            habits.read_habit_overview("test_habits_overview_testcase03")
        # undo renaming
        os.rename("test_habits_overview_testcase01.jpeg", "test_habits_overview_testcase01.json")
        os.rename("test_habits_overview_testcase02.xls", "test_habits_overview_testcase02.json")
        os.rename("test_habits_overview_testcase03", "test_habits_overview_testcase03.json")

        # test: load manipulated overview
        with self.assertRaises(ValueError):
            habits.read_habit_overview("test_habits_overview_testcase03.json")

        # test: file does not exist
        with self.assertRaises(FileNotFoundError):
            habits.read_habit_overview("test_habits_overview_non_existing.json")

    def test_create_habit(self):
        # create new habit overview
        habits.create_habit_overview("test_habits_overview_testcase04.json")

        # test: create unique habit with valid habit attributes
        habit_attributes = ("Testcase04", "Habits Testcase 04", "weekly")
        habits.create_habit(habit_attributes, "test_habits_overview_testcase04.json", os.getcwd())

        # test: create habit with invalid habit attributes
        with self.assertRaises(AttributeError):
            # invalid: no list
            habit_attributes = f"Name: Testcase04, Specification: Habits Testcase 04, Periodicity: weekly"
            habits.create_habit(habit_attributes, "test_habits_overview_testcase04.json", os.getcwd())
            # invalid: not enough parameters
            habit_attributes = ("Testcase04", "Habits Testcase 04")
            habits.create_habit(habit_attributes, "test_habits_overview_testcase04.json", os.getcwd())

    def test_re_instantiate_habits(self):
        # create an overview containing three habits
        habits.create_habit_overview("test_habits_overview_testcase05.json")
        habit05_1 = habits.Habit("Testcase05-1", "Habits Testcase 05-1", "D", "test_habits_habit_testcase05-1.json")
        habit05_1.add_to_overview("test_habits_overview_testcase05.json")
        habit05_2 = habits.Habit("Testcase05-2", "Habits Testcase 05-2", "D", "test_habits_habit_testcase05-2.json")
        habit05_2.add_to_overview("test_habits_overview_testcase05.json")
        habit05_3 = habits.Habit("Testcase05-3", "! DEMO ! DATA !", "D", "test_habits_habit_testcase05-3.json")
        habit05_3.add_to_overview("test_habits_overview_testcase05.json")

        # create an overview containing no habits
        habits.create_habit_overview("test_habits_overview_testcase06.json")

        # test: re-instantiate habits according to habit overview data
        df_overview = habits.read_habit_overview("test_habits_overview_testcase05.json")
        status = habits.re_instantiate_habits(df_overview)
        self.assertEqual(status, "Re-instantiated 3 habits.")

        # test: re-instantiate habits according to empty habit overview data
        df_overview = habits.read_habit_overview("test_habits_overview_testcase06.json")
        status = habits.re_instantiate_habits(df_overview)
        self.assertEqual(status, "Re-instantiated 0 habits.")

    def tearDown(self) -> None:
        list_of_test_files = ["test_habits_overview_testcase00.json",
                              "test_habits_overview_testcase01.json",
                              "test_habits_overview_testcase02.json",
                              "test_habits_overview_testcase03.json",
                              "test_habits_overview_testcase04.json",
                              "test_habits_overview_testcase05.json",
                              "test_habits_overview_testcase06.json",
                              "test_habits_habit_testcase01.json",
                              "test_habits_habit_testcase04.json",
                              "testcase04.json",
                              "test_habits_habit_testcase05-1.json",
                              "test_habits_habit_testcase05-2.json",
                              "test_habits_habit_testcase05-3.json",
                              ]
        for file in list_of_test_files:
            if os.path.exists(file):
                os.remove(file)


class TestHabitsClass(unittest.TestCase):
    def setUp(self) -> None:
        habits.list_habit_instances = []
        list_of_test_files = ["test_habits_overview_testcase10.json",
                              "test_habits_overview_testcase11.json",
                              "test_habits_habit_testcase10.json",
                              "test_habits_habit_testcase11.json",
                              "test_habits_habit_testcase12.json",
                              "test_habits_habit_testcase13.json",
                              "test_habits_habit_testcase14.json",
                              "test_habits_habit_testcase15.json",
                              "test_habits_habit_testcase16.json",
                              "test_habits_habit_testcase17.json",
                              "test_habits_habit_testcase18.json",
                              "test_habits_habit_testcase19.json",
                              "test_habits_habit_testcase20.json"
                              ]
        for file in list_of_test_files:
            if os.path.exists(file):
                os.remove(file)

    def test_add_to_overview(self):
        # create empty overview
        habits.create_habit_overview("test_habits_overview_testcase10.json")
        # create new habit
        habit10 = habits.Habit("Testcase10", "Habits Testcase 10", "D", "test_habits_habit_testcase10.json")

        # test: add habit to empty overview
        status = habit10.add_to_overview("test_habits_overview_testcase10.json")
        self.assertEqual(status, "Added habit to overview")

    def test_create_dataframe(self):
        # create new habit with created on date 2021-09-01
        habit11 = habits.Habit("Testcase11", "Habits Testcase 11", "D",
                               "test_habits_habit_testcase11.json", datetime(2021, 9, 1))
        # set valid date parameters for dataframe
        start = datetime(2021, 9, 1)
        end = datetime(2021, 9, 10)

        # test with valid date parameters
        dataframe = habit11.create_dataframe(start, end)
        self.assertTrue(isinstance(dataframe, pd.DataFrame))

        # set invalid date parameters for dataframe (end < start)
        start = datetime(2021, 9, 1)
        end = datetime(2021, 8, 1)
        with self.assertRaises(ValueError):
            habit11.create_dataframe(start, end)

        # set invalid date parameters for dataframe (date + default value: 'init' --> string)
        start = datetime(2021, 9, 1)
        with self.assertRaises(ValueError):
            habit11.create_dataframe(start)

    def test_auto_update_file(self):
        # create new habit with created on date 2021-09-01
        habit12 = habits.Habit("Testcase12", "Habits Testcase 12", "D",
                               "test_habits_habit_testcase12.json", datetime(2021, 9, 1))

        # create new habit with created on date = today
        habit13 = habits.Habit("Testcase13", "Habits Testcase 12", "D", "test_habits_habit_testcase13.json")

        # create new habit with specification like demo data
        habit14 = habits.Habit("Testcase14", "! DEMO ! DATA !", "D", "test_habits_habit_testcase14.json")

        # test: Habit with no data and created on 2021-09-01 needs auto-update from created on date on
        status = habit12.auto_update_file()
        self.assertEqual(status[:47], "Habit Testcase12: Auto-Update for 2021-09-01 - ")

        # test: Habit with same date for created on and current date for auto-update
        status = habit13.auto_update_file()
        self.assertEqual(status,
                         "Habit Testcase13: No auto-update needed - "
                         "already checked-off or check-off for only running period still possible!")

        # test: Habit as demo data
        status = habit14.auto_update_file()
        self.assertEqual(status, "Habit Testcase14: No auto-update for demo data")

    def test_check_off_habit(self):
        # create new habit with created on date 2021-09-01
        habit15 = habits.Habit("Testcase15", "Habits Testcase 15", "D",
                               "test_habits_habit_testcase15.json", datetime(2021, 9, 1))
        # create new habit with created on date 2021-09-01
        habit16 = habits.Habit("Testcase12", "Habits Testcase 16", "D",
                               "test_habits_habit_testcase16.json", datetime(2021, 9, 1))
        # create new habit with specification like demo data
        habit17 = habits.Habit("Testcase17", "! DEMO ! DATA !", "D", "test_habits_habit_testcase17.json")

        # test: check-off auto-updated habit (period still running)
        habit15.auto_update_file()
        status = habit15.check_off_habit()
        self.assertEqual(status, "Successfully checked-off your habit!")

        # test: check-off twice auto-update habit
        habit16.auto_update_file()
        habit16.check_off_habit()
        status = habit16.check_off_habit()
        self.assertEqual(status, "ERROR: Can't check-off twice a habit!")

        # test: check off demo data
        status = habit17.check_off_habit()
        self.assertEqual(status, "ERROR: Can't check-off demo data! For further information read the instructions.")

    def test_analyze_habit(self):
        # create new daily habit with created on date 2021-09-01
        habit18 = habits.Habit("Testcase18", "Habits Testcase 18", "D",
                               "test_habits_habit_testcase18.json", datetime(2021, 9, 1))
        # set-up habit: create data for Testcase18
        start = date(2021, 9, 1)
        end = date(2021, 9, 10)
        list_index = pd.date_range(start, end, freq="D")
        list_values = [["Yes", datetime(2021, 9, 1, 12, 0, 0)],
                       ["No", np.nan],
                       ["No", np.nan],
                       ["Yes", datetime(2021, 9, 4, 12, 0, 0)],
                       ["Yes", datetime(2021, 9, 5, 12, 0, 0)],
                       ["Yes", datetime(2021, 9, 6, 12, 0, 0)],
                       ["No", np.nan],
                       ["No", np.nan],
                       ["No", np.nan],
                       ["Yes", datetime(2021, 9, 10, 12, 0, 0)]]
        df_habit18 = pd.DataFrame(list_values, columns=["Checked-off", "Check-off date"], index=list_index)
        # saving dataframe to .json file
        df_habit18.to_json(habit18.file, date_format='iso')

        # test: check for identical dictionaries
        analysis = habit18.analyze_habit()
        analysis_test = {"Name": "Testcase18",
                         "Specification": "Habits Testcase 18",
                         "Periodicity": "daily",
                         "Created on": "2021-09-01",
                         "Number of periods": 10,
                         "Checked-off periods": 5,
                         "Percentage checked-off periods": "50.0%",
                         "Longest Streak": 3,
                         "Period Longest Streak": "2021-09-04 - 2021-09-06"}
        self.assertDictEqual(analysis, analysis_test)

        # create new weekly habit with created on date 2021-09-01
        habit19 = habits.Habit("Testcase19", "Habits Testcase 19", "7d",
                               "test_habits_habit_testcase19.json", datetime(2021, 9, 1))
        # set-up habit: create data for Testcase19
        start = date(2021, 9, 1)
        end = date(2021, 9, 15)
        list_index = pd.date_range(start, end, freq="7d")
        list_values = [["Yes", datetime(2021, 9, 1, 12, 0, 0)],
                       ["No", np.nan],
                       ["Yes", datetime(2021, 9, 15, 12, 0, 0)]]
        df_habit19 = pd.DataFrame(list_values, columns=["Checked-off", "Check-off date"], index=list_index)
        # saving dataframe to .json file
        df_habit19.to_json(habit19.file, date_format='iso')
        analysis = habit19.analyze_habit()
        analysis_test = {"Name": "Testcase19",
                         "Specification": "Habits Testcase 19",
                         "Periodicity": "weekly",
                         "Created on": "2021-09-01",
                         "Number of periods": 3,
                         "Checked-off periods": 2,
                         "Percentage checked-off periods": "66.67%",
                         "Longest Streak": 1,
                         "Period Longest Streak": "2021-09-01 - 2021-09-07"}
        self.assertDictEqual(analysis, analysis_test)

    def test_remove_habit(self):
        # create empty overview
        habits.create_habit_overview("test_habits_overview_testcase11.json")
        # create new habit to be removed and add it to the overview
        habit20 = habits.Habit("Testcase20", "Habits Testcase 20", "D", "test_habits_habit_testcase16.json")
        habit20.add_to_overview("test_habits_overview_testcase06.json")

        # test: remove habit
        status = habit20.remove_habit("test_habits_overview_testcase11.json")
        self.assertNotIn(habit20, habits.list_habit_instances)
        self.assertEqual(status, "Habit successfully deleted")

    def tearDown(self) -> None:
        list_of_test_files = ["test_habits_overview_testcase10.json",
                              "test_habits_overview_testcase11.json",
                              "test_habits_habit_testcase10.json",
                              "test_habits_habit_testcase11.json",
                              "test_habits_habit_testcase12.json",
                              "test_habits_habit_testcase13.json",
                              "test_habits_habit_testcase14.json",
                              "test_habits_habit_testcase15.json",
                              "test_habits_habit_testcase16.json",
                              "test_habits_habit_testcase17.json",
                              "test_habits_habit_testcase18.json",
                              "test_habits_habit_testcase19.json",
                              "test_habits_habit_testcase20.json"
                              ]
        for file in list_of_test_files:
            if os.path.exists(file):
                os.remove(file)

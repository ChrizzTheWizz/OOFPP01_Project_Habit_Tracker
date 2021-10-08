import sys
import os
import unittest
import pandas as pd
import numpy as np
from datetime import date, datetime
from habittracker import analyze
from habittracker import habits

# insertion to sys.path to be able to import the modules to be tested
path = os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + "habittracker")
sys.path.insert(0, path)


class TestAnalyze(unittest.TestCase):

    def setUp(self) -> None:
        habits.list_habit_instances = []
        list_of_test_files = ["test_analyze_habit_testcase1.json",
                              "test_analyze_habit_testcase2.json",
                              "test_analyze_habit_testcase3.json",
                              "test_analyze_habit_testcase4.json",
                              "test_analyze_habit_testcase5.json"
                              ]
        for file in list_of_test_files:
            if os.path.exists(file):
                os.remove(file)

        # set-up habits: instantiating
        habit1 = habits.Habit("Testcase1", "DT1", "D", "test_analyze_habit_testcase1.json")
        habit2 = habits.Habit("Testcase2", "DT2", "D", "test_analyze_habit_testcase2.json")
        habit3 = habits.Habit("Testcase3", "WT1", "7d", "test_analyze_habit_testcase3.json")
        habit4 = habits.Habit("Testcase4", "WT2", "7d", "test_analyze_habit_testcase4.json")
        habit5 = habits.Habit("Testcase5", "WT3", "7d", "test_analyze_habit_testcase5.json")

        # set-up habits: create data Testcase1
        start = date(2021, 9, 1)
        end = date(2021, 9, 7)
        list_index = pd.date_range(start, end, freq="D")
        list_values = [["Yes", datetime(2021, 9, 1, 12, 0, 0)],
                       ["Yes", datetime(2021, 9, 2, 12, 0, 0)],
                       ["Yes", datetime(2021, 9, 3, 12, 0, 0)],
                       ["Yes", datetime(2021, 9, 4, 12, 0, 0)],
                       ["No", np.nan],
                       ["No", np.nan],
                       ["Yes", datetime(2021, 9, 7, 12, 0, 0)]]
        df_habit1 = pd.DataFrame(list_values, columns=["Checked-off", "Check-off date"], index=list_index)
        # saving dataframe to .json file
        df_habit1.to_json(habit1.file, date_format='iso')

        # set-up habits: create data Testcase2
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
        df_habit2 = pd.DataFrame(list_values, columns=["Checked-off", "Check-off date"], index=list_index)
        # saving dataframe to .json file
        df_habit2.to_json(habit2.file, date_format='iso')

        # set-up habits: create data Testcase3
        start = date(2021, 9, 1)
        end = date(2021, 9, 15)
        list_index = pd.date_range(start, end, freq="7d")
        list_values = [["Yes", datetime(2021, 9, 1, 12, 0, 0)],
                       ["No", np.nan],
                       ["Yes", datetime(2021, 9, 15, 12, 0, 0)]]
        df_habit3 = pd.DataFrame(list_values, columns=["Checked-off", "Check-off date"], index=list_index)
        # saving dataframe to .json file
        df_habit3.to_json(habit3.file, date_format='iso')

        # set-up habits: create data Testcase4
        start = date(2021, 9, 1)
        end = date(2021, 9, 30)
        list_index = pd.date_range(start, end, freq="7d")
        list_values = [["Yes", datetime(2021, 9, 1, 12, 0, 0)],
                       ["Yes", datetime(2021, 9, 8, 12, 0, 0)],
                       ["Yes", datetime(2021, 9, 15, 12, 0, 0)],
                       ["No", np.nan],
                       ["Yes", datetime(2021, 9, 29, 12, 0, 0)]]
        df_habit4 = pd.DataFrame(list_values, columns=["Checked-off", "Check-off date"], index=list_index)
        # saving dataframe to .json file
        df_habit4.to_json(habit4.file, date_format='iso')

        # set-up habits: create data Testcase5
        # Testcase 5 is empty (no checked-off periods)

    def test_create_num_list_habits(self):
        list_numbered_habits = analyze.create_num_list_habits(habits.list_habit_instances)
        self.assertIn("1 Testcase1", list_numbered_habits)
        self.assertIn("2 Testcase2", list_numbered_habits)
        self.assertIn("3 Testcase3", list_numbered_habits)
        self.assertIn("4 Testcase4", list_numbered_habits)
        self.assertIn("5 Testcase5", list_numbered_habits)

        # check with empty list simulating no existing habits
        empty_list = []
        list_numbered_habits = analyze.create_num_list_habits(empty_list)
        self.assertFalse(list_numbered_habits)

    def test_request_analysis(self):
        df_analysis = analyze.request_analysis(habits.list_habit_instances)
        # Check Testcase1
        self.assertEqual(df_analysis.iloc[0]["Name"], "Testcase1")
        self.assertEqual(df_analysis.iloc[0]["Specification"], "DT1")
        self.assertEqual(df_analysis.iloc[0]["Periodicity"], "daily")
        self.assertEqual(df_analysis.iloc[0]["Created on"], datetime.now().strftime("%Y-%m-%d"))
        self.assertEqual(df_analysis.iloc[0]["Number of periods"], 7)
        self.assertEqual(df_analysis.iloc[0]["Checked-off periods"], 5)
        self.assertEqual(df_analysis.iloc[0]["Percentage checked-off periods"], "71.43%")
        self.assertEqual(df_analysis.iloc[0]["Longest Streak"], 4)
        self.assertEqual(df_analysis.iloc[0]["Period Longest Streak"], "2021-09-01 - 2021-09-04")
        # Check Testcase2
        self.assertEqual(df_analysis.iloc[1]["Name"], "Testcase2")
        self.assertEqual(df_analysis.iloc[1]["Specification"], "DT2")
        self.assertEqual(df_analysis.iloc[1]["Periodicity"], "daily")
        self.assertEqual(df_analysis.iloc[1]["Created on"], datetime.now().strftime("%Y-%m-%d"))
        self.assertEqual(df_analysis.iloc[1]["Number of periods"], 10)
        self.assertEqual(df_analysis.iloc[1]["Checked-off periods"], 5)
        self.assertEqual(df_analysis.iloc[1]["Percentage checked-off periods"], "50.0%")
        self.assertEqual(df_analysis.iloc[1]["Longest Streak"], 3)
        self.assertEqual(df_analysis.iloc[1]["Period Longest Streak"], "2021-09-04 - 2021-09-06")
        # Check Testcase3
        self.assertEqual(df_analysis.iloc[2]["Name"], "Testcase3")
        self.assertEqual(df_analysis.iloc[2]["Specification"], "WT1")
        self.assertEqual(df_analysis.iloc[2]["Periodicity"], "weekly")
        self.assertEqual(df_analysis.iloc[2]["Created on"], datetime.now().strftime("%Y-%m-%d"))
        self.assertEqual(df_analysis.iloc[2]["Number of periods"], 3)
        self.assertEqual(df_analysis.iloc[2]["Checked-off periods"], 2)
        self.assertEqual(df_analysis.iloc[2]["Percentage checked-off periods"], "66.67%")
        self.assertEqual(df_analysis.iloc[2]["Longest Streak"], 1)
        self.assertEqual(df_analysis.iloc[2]["Period Longest Streak"], "2021-09-01 - 2021-09-07")
        # Check Testcase4
        self.assertEqual(df_analysis.iloc[3]["Name"], "Testcase4")
        self.assertEqual(df_analysis.iloc[3]["Specification"], "WT2")
        self.assertEqual(df_analysis.iloc[3]["Periodicity"], "weekly")
        self.assertEqual(df_analysis.iloc[3]["Created on"], datetime.now().strftime("%Y-%m-%d"))
        self.assertEqual(df_analysis.iloc[3]["Number of periods"], 5)
        self.assertEqual(df_analysis.iloc[3]["Checked-off periods"], 4)
        self.assertEqual(df_analysis.iloc[3]["Percentage checked-off periods"], "80.0%")
        self.assertEqual(df_analysis.iloc[3]["Longest Streak"], 3)
        self.assertEqual(df_analysis.iloc[3]["Period Longest Streak"], "2021-09-01 - 2021-09-21")
        # Check Testcase5
        self.assertEqual(df_analysis.iloc[4]["Name"], "Testcase5")
        self.assertEqual(df_analysis.iloc[4]["Specification"], "WT3")
        self.assertEqual(df_analysis.iloc[4]["Periodicity"], "weekly")
        self.assertEqual(df_analysis.iloc[4]["Created on"], datetime.now().strftime("%Y-%m-%d"))
        self.assertEqual(df_analysis.iloc[4]["Number of periods"], 0)
        self.assertEqual(df_analysis.iloc[4]["Checked-off periods"], 0)
        self.assertEqual(df_analysis.iloc[4]["Percentage checked-off periods"], "0%")
        self.assertEqual(df_analysis.iloc[4]["Longest Streak"], 0)
        self.assertEqual(df_analysis.iloc[4]["Period Longest Streak"], "-")

        # check with empty list simulating no existing habits
        empty_list = []
        df_analysis = analyze.request_analysis(empty_list)
        self.assertTrue(df_analysis.empty)

    def test_create_analysis(self):
        df_analysis = analyze.request_analysis(habits.list_habit_instances)
        result_analysis = analyze.create_analysis(df_analysis, "Test:", "Name", ["daily"])
        # test if intro is correct
        self.assertEqual(result_analysis[:5], "Test:")
        # test if counting habits according to filtering ('daily') is correct
        # from -2:-1 due to /n at the end of line in code
        self.assertEqual(result_analysis[-2:-1], "2")
        # test if counting habits according to filtering ('weekly') is correct
        # from -2:-1 due to /n at the end of line in code
        result_analysis = analyze.create_analysis(df_analysis, "Test:", "Name", ["weekly"])
        self.assertEqual(result_analysis[-2:-1], "3")
        # test if counting habits according to filtering ('daily' + 'weekly') is correct
        # from -2:-1 due to /n at the end of line in code
        result_analysis = analyze.create_analysis(df_analysis, "Test:", "Name", ["daily", "weekly"])
        self.assertEqual(result_analysis[-2:-1], "5")

        # non-available periodicity simulating that there's no output
        result_analysis = analyze.create_analysis(df_analysis, "Test:", "Name", ["monthly"])
        self.assertEqual(result_analysis[-35:], "There are no habits to be analyzed!")

        # raising errors
        # unknown column for sorting dataframe
        with self.assertRaises(TypeError):
            analyze.create_analysis("df_analysis", "Test:", "Name", ["daily", "weekly"])
        with self.assertRaises(ValueError):
            analyze.create_analysis(df_analysis, "This is an test analysis:", "Something", ["daily"])
        # false type for periodicity
        with self.assertRaises(TypeError):
            analyze.create_analysis(df_analysis, "This is an test analysis", "Name", "daily")

    def test_details_habit(self):
        result_analysis = analyze.details_habit(habits.list_habit_instances[0])
        self.assertEqual(result_analysis[:21], "Detailed analysis for")
        self.assertIn("Name: Testcase1", result_analysis)
        self.assertIn("Specification: DT1", result_analysis)
        self.assertIn("Periodicity: daily", result_analysis)
        self.assertIn("Number of periods: 7", result_analysis)
        self.assertIn("Checked-off periods: 5", result_analysis)
        self.assertIn("Percentage checked-off periods: 71.43%", result_analysis)
        self.assertIn("Longest Streak: 4", result_analysis)
        self.assertIn("Period Longest Streak: 2021-09-01 - 2021-09-04", result_analysis)

        result_analysis = analyze.details_habit(habits.list_habit_instances[2])
        self.assertEqual(result_analysis[:21], "Detailed analysis for")
        self.assertIn("Name: Testcase3", result_analysis)
        self.assertIn("Specification: WT1", result_analysis)
        self.assertIn("Periodicity: weekly", result_analysis)
        self.assertIn("Number of periods: 3", result_analysis)
        self.assertIn("Checked-off periods: 2", result_analysis)
        self.assertIn("Percentage checked-off periods: 66.67%", result_analysis)
        self.assertIn("Longest Streak: 1", result_analysis)
        self.assertIn("Period Longest Streak: 2021-09-01 - 2021-09-07", result_analysis)

        result_analysis = analyze.details_habit(habits.list_habit_instances[4])
        self.assertEqual(result_analysis, "No detailed analysis for 'Testcase5'!")

        with self.assertRaises(TypeError):
            analyze.details_habit("Habit")

    def tearDown(self) -> None:
        list_of_test_files = ["test_analyze_habit_testcase1.json",
                              "test_analyze_habit_testcase2.json",
                              "test_analyze_habit_testcase3.json",
                              "test_analyze_habit_testcase4.json",
                              "test_analyze_habit_testcase5.json"
                              ]
        for file in list_of_test_files:
            if os.path.exists(file):
                os.remove(file)

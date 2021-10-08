import pandas as pd
from datetime import timedelta, datetime

import habittracker.habits


def create_num_list_habits(habit_instances):
    """
    Creates a numbered list of existing habits based on the global list of habit instances

    :param habit_instances: List of existing habit instances
    :return: List of numbered habits
    """

    # empty list of numbered habits
    list_habits = []

    # enumerating through existing habit instances and adding number, name and specification of existing habits
    for i, habit in enumerate(habit_instances):
        list_habits.append(f"{i + 1} {habit.name}")

    return list_habits


def request_analysis(habit_instances):
    """
    Creating a pandas dataframe for analysis on basis of existing habits

    :param habit_instances: List of existing habit instances
    :return: pandas dataframe for analyzing existing habits
    """

    # creating an empty pandas dataframe with defined columns (ATTENTION: MUST FIT DICTIONARY RETURN FROM HABIT METHOD)
    df_analysis = pd.DataFrame(
        columns=["Name",
                 "Specification",
                 "Periodicity",
                 "Created on",
                 "Number of periods",
                 "Checked-off periods",
                 "Percentage checked-off periods",
                 "Longest Streak",
                 "Period Longest Streak"])

    # for every existing habit instance
    for habit in habit_instances:
        # generating dataframe with analyze_habit() (class method)
        results_habit = habit.analyze_habit()
        # insert results from class method into new dataframe scheme for analysis
        df_analysis = df_analysis.append(results_habit, ignore_index=True)

    return df_analysis


def create_analysis(df_analysis, intro_analysis, analysis_sort_by, analysis_periodicity):
    """
    Creating analysis output for all existing habits

    :param analysis_periodicity: periodicity of the habits to be analyzed ('daily' and/or 'weekly')
    :param analysis_sort_by: parameter according to the habits are to be sorted ('name', 'created on' or 'streaks')
    :param intro_analysis: name of the analysis that is displayed at the top of the analysis
    :param df_analysis: pandas dataframe for analyzing existing habits
    :return: string with intro, main analysis and outro
    """
    # to use 'isin'-functionality, 'analysis_periodicity' needs to be a list
    if not isinstance(df_analysis, pd.DataFrame):
        raise TypeError("Analysis subject must be a pandas dataframe!")
    if not isinstance(analysis_periodicity, list):
        raise TypeError("Periodicity to be filtered must be in a list!")
    if analysis_sort_by not in df_analysis.columns:
        raise ValueError("Analysis can only be sort by known columns in the dataframe!")

    # for not changing the original analysis a copy is generated
    df_analysis_output = df_analysis.copy()

    # dataframe is filtered according to input
    if analysis_periodicity != "none":
        df_analysis_output = df_analysis_output[df_analysis_output["Periodicity"].isin(analysis_periodicity)]
        # df_analysis_output = df_analysis_output.loc[df_analysis_output.Periodicity == analysis_periodicity]

    # text at the end of the displayed analysis (number of analyzed habits) according to (non-) empty dataframe
    if df_analysis_output.empty:
        outro_analysis = f"There are no habits to be analyzed!"
        return f"{intro_analysis}\n{outro_analysis}"
    else:
        outro_analysis = f"\nNumber of analyzed habits: {len(df_analysis_output)}\n"
        # if dataframe isn't empty
        # dataframe is sorted by column (ascending only for 'Longest Streak' analysis)
        if analysis_sort_by == "Longest Streak":
            df_analysis_output = df_analysis_output.sort_values(by=[analysis_sort_by], ascending=False)
        else:
            df_analysis_output = df_analysis_output.sort_values(by=[analysis_sort_by])

        # definition of columns that are displayed
        output_analysis_all_habits = df_analysis_output.loc[:, ["Name",
                                                                "Specification",
                                                                "Periodicity",
                                                                "Number of periods",
                                                                "Checked-off periods",
                                                                "Percentage checked-off periods",
                                                                "Longest Streak",
                                                                "Period Longest Streak",
                                                                "Created on"]]

        return f"{intro_analysis}\n{output_analysis_all_habits.to_markdown(index=False)}\n{outro_analysis}"


def details_habit(habit):
    """
    Creating a detailed analysis output for specific (according to user input) existing habit.

    :param habit: Chosen habit instance for detailed analysis
    :return: string with intro, habit overview data and detailed analysis
    """

    if not isinstance(habit, habittracker.habits.Habit):
        raise TypeError("Parameter is not of class Habit!")

    # reading stored habit data
    df_habit_details = pd.read_json(habit.file)
    if df_habit_details.empty:
        intro_analysis = f"No detailed analysis for '{habit.name}'!"
        return intro_analysis
    else:
        df_habit_overview_data = habit.analyze_habit()
        intro_analysis = f"Detailed analysis for '{habit.name}':"
        output_habit_overview_data = f"Name: {df_habit_overview_data['Name']}\n" \
                                     f"Specification: {df_habit_overview_data['Specification']}\n" \
                                     f"Periodicity: {df_habit_overview_data['Periodicity']}\n" \
                                     f"Number of periods: {df_habit_overview_data['Number of periods']}\n" \
                                     f"Checked-off periods: {df_habit_overview_data['Checked-off periods']}\n" \
                                     f"Percentage checked-off periods: " \
                                     f"{df_habit_overview_data['Percentage checked-off periods']}\n" \
                                     f"Longest Streak: {df_habit_overview_data['Longest Streak']}\n" \
                                     f"Period Longest Streak: {df_habit_overview_data['Period Longest Streak']}\n" \
                                     f"Created on: {df_habit_overview_data['Created on']}\n"

        # converting date-values from pandas default type to datetime
        df_habit_details["Check-off date"] = pd.to_datetime(df_habit_details["Check-off date"])
        # replace not checked-off entries with '-'
        df_habit_details["Check-off date"] = df_habit_details["Check-off date"].fillna("-")
        # converting datetime data to '%Y-%m-%d %H:%M:%S' format (if checked-off) or '-' (if not) for better readability
        df_habit_details["Check-off date"] = \
            df_habit_details["Check-off date"].apply(lambda x: datetime.strftime(x, "%Y-%m-%d %H:%M:%S") if x != "-" else x)
        # creating new column 'period' on basis of the index for better readability
        df_habit_details["Period"] = df_habit_details.index
        # depending on periodicity (daily / weekly) the column 'period' is calculated
        df_habit_details["Period"] = df_habit_details["Period"].apply(
            lambda x: f"{x.date()}" if habit.period == "D" else f"{x.date()} - {x.date() + timedelta(6)}")

        # defining the columns for output
        df_habit_details = df_habit_details[["Period", "Checked-off", "Check-off date"]].sort_index(ascending=False)

        return f"{intro_analysis}\n{output_habit_overview_data}\n{df_habit_details.to_markdown(index=False)}"

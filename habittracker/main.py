import os
import sys
from habittracker import *


def read_config_data():
    """
    Reads configuration content from ...\bin\config.txt (default path)
    WARNING: At the current state the config.txt should not be changed!

    Default configuration parameters:
    Directory Documents, Directory Habits, Path File Habits Overview

    :return: dictionary with config data from config.txt
    """

    # empty dictionary is created
    dict_config_data = {}
    # default path to config file
    path_config_file = f"{os.path.normpath(os.getcwd())}\\bin\\config.txt"

    try:
        # reading raw data from config file
        with open(path_config_file, "r") as config:
            raw_config_data = config.readlines()
    except(FileNotFoundError):
        # create error message for user
        status = "ERROR: Config-File not found! " \
                 "'bin' directory available? " \
                 "'config.txt' available?\n" \
                 "Application terminates ..."

        # create 'FileNotFound' entry to dictionary for program termination
        dict_config_data["Status config-file"] = status
    else:
        # writing data to dictionary
        dict_config_data["Status config-file"] = "File successfully read"
        for config_entry in range(0, len(raw_config_data)):
            dict_config_data[raw_config_data[config_entry].split(":")[0]] = \
                raw_config_data[config_entry].split(":")[-1].rstrip().lstrip()
    finally:
        return dict_config_data


def starting_routine(absolute_path_habit_overview, relative_path_habit_files):
    """
    Starting routine needs to be executed every time the app gets started.
    Checks for existing habits to re-instantiating.
    If app is executed for the first time the structure (directories) and habit overview (.json) will be created.

    :param absolute_path_habit_overview: Absolute path to habit overview (.json-file)
    :param relative_path_habit_files: Relative path to habit files (directory)
    :return: Status of starting routine
    """

    # creating empty global list for habit instances
    habits.list_habit_instances = []
    # if path read from config file to habit overview exists ...
    if os.path.exists(absolute_path_habit_overview):
        # ... checking habit overview for existing habits
        df_habit_overview = habits.read_habit_overview(absolute_path_habit_overview)
        if not df_habit_overview.empty:
            # if habit overview isn't empty: habits need to be re-instantiated
            status_called_function = habits.re_instantiate_habits(df_habit_overview)
            return status_called_function
        else:
            # if habit overview is empty there's nothing else to do
            return "No current habits for re-instantiating"

    else:
        # if there's no structure according to the config.txt the structure and habit overview need to be created
        create_structure(relative_path_habit_files)
        habits.create_habit_overview(absolute_path_habit_overview)
        return "Structure created"


def create_structure(relative_path_habit_files):
    """
    Creating the directories (default values)
    - ...\docs\ (for habit overview)
    - ...\docs\habits\ (for habit files data)

    :param relative_path_habit_files:
    :return:
    """
    current_path = os.getcwd()

    for subfolder in relative_path_habit_files.split("\\"):
        current_path = f"{current_path}\\{subfolder}"

        try:
            os.mkdir(current_path)
        except OSError:
            print("Problems with your operating system!")
        except FileExistsError(OSError):
            print("Directory already exists!")


def main():
    """

    :return:
    """

    # reading configuration data from ...\bin\config.txt
    config_data = read_config_data()
    # if config-data could not be read: Exit program
    if config_data["Status config-file"].split(" ")[0] == "ERROR:":
        display.dummy_output(config_data["Status config-file"])
        sys.exit()

    # assignment of relevant directory parameters from configuration data to run starting routine
    absolute_path_habit_overview = f"{os.path.normpath(os.getcwd())}\\{config_data['Path File Habits Overview']}"
    relative_path_habit_files = config_data['Directory Habits']
    absolute_directory_habit_files = f"{os.path.normpath(os.getcwd())}\\{config_data['Directory Habits']}"
    app_version = config_data['Version']

    # running starting routine for
    # (1) re-instantiating habits (if existing) or
    # (2) creating structure (if app is started for the first time)
    starting_routine(absolute_path_habit_overview, relative_path_habit_files)

    # variable for navigation through main menu - "Start main" = default value
    step_main = "Start main"

    while step_main != "Quit":
        # layout prompts via module display functions
        prompt_main = display.header("START", app_version)
        print(prompt_main)

        # checking for possible steps
        possible_steps_main = display.check_available_functions(habits.list_habit_instances)
        # asking user for input (action)
        step_main = display.user_input_step_main(possible_steps_main)

        if step_main == "Create new habit":
            # if user wants to create a new habit: asking for attributes, initialize habit and return confirmation
            # habit attributes contain: name, specification and periodicity
            habit_attributes = display.user_input_habit_attr(habits.list_habit_instances)
            # ask for confirmation
            answer_confirmation = display.confirmation("Do you want to create this new habit?\n"
                                                       f"Name:            {habit_attributes[0]}\n"
                                                       f"Specification:   {habit_attributes[1]}\n"
                                                       f"Periodicity:     "
                                                       f"{'daily' if habit_attributes[2] == 'D' else 'weekly'}")

            if answer_confirmation == "Yes":
                # instantiating habit and adding it to the habit overview
                status_called_function = habits.create_habit(habit_attributes, absolute_path_habit_overview,
                                                             absolute_directory_habit_files)
                # display
                display.dummy_output(status_called_function)

        elif step_main == "Check-off habit":
            # if user wants to check-off a new habit: asking for habit to check-off and return confirmation
            # numbered list of existing habits is created
            numbered_list_of_habits = analyze.create_num_list_habits(habits.list_habit_instances)
            # asking for number of habit to check-off
            num_chosen_habit = display.user_input_habit_choice(numbered_list_of_habits)
            # convert numbered input (integer) into habit (instance)
            chosen_habit = habits.list_habit_instances[int(num_chosen_habit) - 1]
            # ask for confirmation
            answer_confirmation = display.confirmation("Do you want to check-off this habit?\n"
                                                       f"Name:            {chosen_habit.name}\n"
                                                       f"Specification:   {chosen_habit.spec}\n"
                                                       f"Periodicity:     "
                                                       f"{'daily' if chosen_habit.period == 'D' else 'weekly'}")

            if answer_confirmation == "Yes":
                # check-off habit
                status_called_function = chosen_habit.check_off_habit()
                # confirmation for checked-off habit (!!! HIER GGF NOCH ERROR HANDLING EINBAUEN !!!)
                display.dummy_output(status_called_function)

        elif step_main == "Delete a habit":
            # if user wants to delete a habit
            # numbered list of existing habits is created
            numbered_list_of_habits = analyze.create_num_list_habits(habits.list_habit_instances)
            # asking for number of habit to delete
            num_chosen_habit = display.user_input_habit_choice(numbered_list_of_habits)
            # convert numbered input (integer) into habit (instance)
            chosen_habit = habits.list_habit_instances[int(num_chosen_habit) - 1]
            # ask for confirmation
            answer_confirmation = display.confirmation("Do you really want to delete this habit?\n"
                                                       f"Name:            {chosen_habit.name}\n"
                                                       f"Specification:   {chosen_habit.spec}\n"
                                                       f"Periodicity:     "
                                                       f"{'daily' if chosen_habit.period == 'D' else 'weekly'}")

            if answer_confirmation == "Yes":
                status_called_function = chosen_habit.remove_habit(absolute_path_habit_overview)
                # confirmation for deleted habit
                display.dummy_output(status_called_function)

        elif step_main == "Instructions":
            # if user wants to read the instructions (readme.txt)
            with open(f"{os.path.normpath(os.getcwd() + os.sep)}/readme.md", "r") as file:
                readme = file.read()
            display.clear()
            print(readme)
            display.dummy_output("End of file")

        elif step_main == "Analyze my habits":
            """ --- FROM THIS POINT ON ANALYSIS MENU --- """
            # if user wants to analyze existing habits: analyzing-module starts and analysis menu is displayed
            # dataframe (pandas) is created
            df_analyzed_habits = analyze.request_analysis(habits.list_habit_instances)

            if df_analyzed_habits.empty:
                display.dummy_output("ERROR: No habits existing for analysis!")
                step_analysis = "Return to main"
            else:
                # variable for navigation through analysis menu - "Start analysis" = default value
                step_analysis = "Start analysis"

            while step_analysis != "Return to main":
                # layout prompts via module display functions
                prompt_analysis = display.header("Analysis", app_version)
                print(prompt_analysis)

                # asking user for input (action)
                step_analysis = display.user_input_step_analysis()

                if step_analysis == "Detailed analysis of a habit (choice in next step)":
                    # if user wants to see an detailed analysis of a specific habit
                    # numbered list of existing habits is created
                    numbered_list_of_habits = analyze.create_num_list_habits(habits.list_habit_instances)
                    # asking for number of habit to analyze
                    num_chosen_habit = display.user_input_habit_choice(numbered_list_of_habits)
                    # convert numbered input (integer) into habit (instance)
                    chosen_habit = habits.list_habit_instances[int(num_chosen_habit) - 1]
                    # if detailed analysis is possible (existing habit file)
                    result_analysis = analyze.details_habit(chosen_habit)

                    # print the results
                    print(result_analysis)
                    display.dummy_output("Analysis successful")

                elif step_analysis == "Return to main":
                    # if no (further) analysis is wanted
                    pass
                else:
                    # set parameters for overview analysis
                    if step_analysis == "Overview all habits (sorted by name)":
                        analysis_sorted_by = "Name"
                        analysis_periodicity = ["daily", "weekly"]
                    elif step_analysis == "Overview all habits (sorted by date of creation)":
                        analysis_sorted_by = "Created on"
                        analysis_periodicity = ["daily", "weekly"]
                    elif step_analysis == "Overview all habits (sorted by streak)":
                        analysis_sorted_by = "Longest Streak"
                        analysis_periodicity = ["daily", "weekly"]
                    elif step_analysis == "Overview daily habits (sorted by name)":
                        analysis_sorted_by = "Name"
                        analysis_periodicity = ["daily"]
                    elif step_analysis == "Overview daily habits (sorted by date of creation)":
                        analysis_sorted_by = "Created on"
                        analysis_periodicity = ["daily"]
                    elif step_analysis == "Overview daily habits (sorted by streak)":
                        analysis_sorted_by = "Longest Streak"
                        analysis_periodicity = ["daily"]
                    elif step_analysis == "Overview weekly habits (sorted by name)":
                        analysis_sorted_by = "Name"
                        analysis_periodicity = ["weekly"]
                    elif step_analysis == "Overview weekly habits (sorted by date of creation)":
                        analysis_sorted_by = "Created on"
                        analysis_periodicity = ["weekly"]
                    elif step_analysis == "Overview weekly habits (sorted by streak)":
                        analysis_sorted_by = "Longest Streak"
                        analysis_periodicity = ["weekly"]

                    result_analysis = analyze.create_analysis(df_analyzed_habits,
                                                              step_analysis,
                                                              analysis_sorted_by,
                                                              analysis_periodicity)
                    # print the results
                    print(result_analysis)
                    display.dummy_output("Analysis successful")

        elif step_main == "Options":
            """ --- FROM THIS POINT ON OPTIONS MENU --- """
            # if user wants to set options
            # variable for navigation through options menu - "Start options" = default value
            step_options = "Start options"

            while step_options != "Return to main":
                # layout prompts via module display functions
                prompt_analysis = display.header("Options", app_version)
                print(prompt_analysis)

                # asking user for input (action)
                step_options = display.user_input_step_options()

                if step_options == "Create random example data (daily habit)":
                    # if user wants to create a random daily habit
                    rand_habits.create_random_habit("D", absolute_path_habit_overview, absolute_directory_habit_files)
                    # confirmation for analyzed habit (!!! HIER GGF NOCH ERROR HANDLING EINBAUEN !!!)
                    display.dummy_output(f"Random habit successfully created!")
                    # habit_attributes = display_functions.user_input_random_habit(habits.list_habit_instances)
                    # habits.create_habit(habit_attributes, absolute_path_habit_overview)

                elif step_options == "Create random example data (weekly habit)":
                    # if user wants to create a random weekly habit
                    rand_habits.create_random_habit("7d", absolute_path_habit_overview, absolute_directory_habit_files)
                    # confirmation for analyzed habit (!!! HIER GGF NOCH ERROR HANDLING EINBAUEN !!!)
                    display.dummy_output(f"Random habit successfully created!")
                    # habit_attributes = display_functions.user_input_random_habit(habits.list_habit_instances)
                    # habits.create_habit(habit_attributes, absolute_path_habit_overview)

                elif step_options == "Return to main":
                    # if no (further) options are wanted
                    pass

        elif step_main == "Quit":
            # if user wants to quit
            pass

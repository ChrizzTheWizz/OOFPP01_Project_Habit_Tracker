import os
import questionary


def clear():
    """
    Clear screen function for proper display output

    :return:
    """
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def header(title, app_version):
    """
    Using clear() function and standardized string output for header.

    :param app_version: App-Version read from config.txt
    :param title: Title for header prompt
    :return: String for printing the header
    """
    clear()

    # standard string for header and placeholder for title
    """ HIER KÖNNTE NOCH DIE Versionsnummer aus der config.txt gelesen werden """
    display = ("\t\t\t#########################################\n"
               "\t\t\t## WELCOME TO CHRIZZ HABIT TRACKER APP ##\n"
               "\t\t\t#########################################\n"
               f"\t\t\t\t\t\tVersion: {app_version}\n"
               "\n"
               f"+++ {title} +++")

    return display


def user_input_habit_attr(list_habit_instances):
    """
    Asking for user input ('name', 'specification' and 'periodicity') for new habit with questionary.
    Name (string): may not already exist.
    Specification (string): no further conventions
    Periodicity (string): daily or weekly

    :param list_habit_instances: Current list (instances of class habit) of habits
    :return: User input for 'name', 'specification' and 'periodicity' of the new habit
    """

    # creating empty list for existing habit names
    names_existing_habits = []
    # filling list with existing habit names
    for habit in list_habit_instances:
        names_existing_habits.append(habit.name)

    # using questionary.text for user input. Name needs to be unique, larger than 'nothing' and less than three words
    name = questionary.text(
        "Enter the title (at least one letter and less than three words) of the habit: ",
        validate=lambda text: True if len(text) > 0 and len(
            text.split(" ")) <= 2 and text not in names_existing_habits else
        "Please enter a unique name with at least one letter and less than three words!"
    ).ask().strip()

    # using questionary.text for user input. Specification for detailed information to the user and may not be empty
    spec = questionary.text(
        "Enter a specification of the habit: ",
        validate=lambda text: True if len(text) > 0 else "Please enter a specification"
    ).ask().strip()

    """ASKING FOR THE SUPPORTED PERIODICITY"""
    # using questionary.select for user input. Periodicity can only be 'daily' or 'weekly'
    period = questionary.select(
        "Please choose a periodicity for your new habit:",
        choices=[
            "daily",
            "weekly"
        ]
    ).ask()

    # converting periodicity input to pandas conventional format for datetime.range
    if period == "daily":
        period = "D"
    elif period == "weekly":
        period = "7d"

    return name, spec, period


def check_available_functions(list_of_habits):
    """
    Default options:
    - Create new habit
    - Options
    - Instructions
    - Quit

    :param list_of_habits: According to existing habits further functions are available
    :return: List of available functions (as string), that are used for questionary-input.
    """

    """ Prüfung einbauen, wenn keine / falsche Liste mitgegeben wird """
    if not list_of_habits:
        # if habit overview list is empty only default options are available
        return [
            "Create new habit",
            "Options",
            "Instructions",
            "Quit"
        ]

    elif not os.listdir(f"{os.path.normpath(os.getcwd() + os.sep)}\docs\habits"):
        # if habits exist but no detailed habit data is available existing habits can be checked-off
        return [
            "Create new habit",
            "Check-off habit",
            "Delete a habit",
            "Options",
            "Instructions",
            "Quit"
        ]

    else:
        # every option is available
        return [
            "Create new habit",
            "Check-off habit",
            "Analyze my habits",
            "Delete a habit",
            "Options",
            "Instructions",
            "Quit"
        ]


def user_input_step_main(possible_actions):
    """
    Using questionary.select for user input which action the user wants to make (main menu)

    :param possible_actions: Possible actions according to check_available_functions() beforehand in main.py
    :return: Action (string) based on available functions / actions that can be done by the user
    """
    action = questionary.select(
        "What do you like to do?",
        choices=possible_actions
    ).ask()

    return action


def user_input_habit_choice(numbered_list_of_habits):
    """
    Using questionary.select for user input which habit has to be chosen

    :param numbered_list_of_habits:
    :return: Returns number (integer) of chosen habit
    """
    chosen_habit = questionary.select(
        "Which habit do you want to choose?",
        choices=numbered_list_of_habits
    ).ask().split(" ")[0]

    return chosen_habit


def user_input_step_analysis():
    """
    Using questionary.select for user input which action the user wants to make (analysis menu)

    :return: Action (string) based on available analysis that can be done by the user
    """
    step_analysis = questionary.select(
        "Which analysis do want to see?",
        choices=["Overview all habits (sorted by name)",
                 "Overview all habits (sorted by date of creation)",
                 "Overview all habits (sorted by streak)",
                 "Overview daily habits (sorted by name)",
                 "Overview daily habits (sorted by date of creation)",
                 "Overview daily habits (sorted by streak)",
                 "Overview weekly habits (sorted by name)",
                 "Overview weekly habits (sorted by date of creation)",
                 "Overview weekly habits (sorted by streak)",
                 "Detailed analysis of a habit (choice in next step)",
                 "Return to main"]).ask()

    return step_analysis


def user_input_step_options():
    """
    Using questionary.select for user input which action the user wants to make (options menu)

    :return: Action (string) based on available options that can be done by the user
    """
    step_options = questionary.select(
        "What do you want to do?",
        choices=["Create random example data (daily habit)",
                 "Create random example data (weekly habit)",
                 "Return to main"]).ask()

    return step_options


def confirmation(prompt):
    """
    Dummy questionary.select ouput for better user experience while using functionalities.
    Replaces any time-controlled continuation of the menu navigation

    :param prompt: Tiny text what has recently be done.
    :return: none
    """

    answer = questionary.select(
        prompt,
        choices=["Yes", "No"]).ask()

    return answer


def dummy_output(prompt):
    """
    Dummy questionary.select ouput for better user experience while using functionalities.
    Replaces any time-controlled continuation of the menu navigation

    :param prompt: Tiny text what has recently be done.
    :return: none
    """

    dummy = questionary.select(prompt, choices=["return"]).ask()

Binary_Choice_List = [
    [False, 'No'],
    [True, 'Yes'],
]

Likert_Familiarity_List = [
    [1, 'Not at all familiar'],
    [2, 'Slightly familiar'],
    [3, 'Somewhat familiar'],
    [4, 'Moderately familiar'],
    [5, 'Extremely familiar']
]


def read_csv(filename):
    """Reads a CSV in random order"""
    import csv

    f = open(filename, encoding='cp1252')
    rows = list(csv.DictReader(f))

    # random.shuffle(rows)  # Randomisation is just a hindrance
    return rows


def value_function(task, player):
    """Returns a player's stated valuation for a task."""
    if task == 'Fancy Pizza':
        return player.Fancy_Pizza_Value
    elif task == 'Cheap Pizza':
        return player.Cheap_Pizza_Value
    elif task == 'Fancy Taco':
        return player.Fancy_Taco_Value
    elif task == 'Cheap Taco':
        return player.Cheap_Taco_Value
    else:
        raise ValueError('Input must be first (capital) letter of a task name')


def list_subtract(first_list, second_list):
    """Set-difference, but for lists"""
    return list(set(first_list) - set(second_list))


def find_min_diff(arr, n):
    """Finds the minimum difference (and inducing indices) in a list"""
    # Initialize difference as infinite, indexes to stop pycharm yelling
    diff = 10 ** 20
    index1 = 0
    index2 = 0
    # Find the min diff by comparing difference
    # of all possible pairs in given array
    for i in range(n - 1):
        for j in range(i + 1, n):
            if abs(arr[i] - arr[j]) < diff:
                diff = abs(arr[i] - arr[j])
                if arr[i] >= arr[j]:
                    index1 = i
                    index2 = j
                else:
                    index1 = j
                    index2 = i
                # Return min diff
    return diff, index1, index2


def task_name_decoder(string):
    """Returns task app from task name"""
    if string == 'Tabulation':
        return 'task_tabulation'
    elif string == 'Concealment':
        return 'task_encoding'
    elif string == "Interpretation":
        return 'task_transcribing'
    elif string == "Replication":
        return 'task_replication'
    elif string == "Organisation":
        return "task_organising"


def task_name(string):
    """Returns task name from task initial"""
    if string == 'T':
        return 'Tabulation'
    elif string == 'C':
        return "Concealment"
    elif string == 'I':
        return "Interpretation"
    elif string == 'R':
        return "Replication"
    elif string == 'O':
        return "Organisation"
    else:
        raise ValueError('Input must be first (capital) letter of a task name')


def option_index(option):
    """Numeric value of option"""
    if option == "Option 1":
        return 1
    elif option == "Option 2":
        return 2


global_cases_dict = {'Introduction': ['all_correct'],
                     'BDM': ['success'],
                     'Task_WTP': ['random'],
                     'Exp_Prob': [[0.3, 0.5, 0.1, 0.1]],  # [(O1,O1), (O1,O2), (O2, O1), (O2,O2)]
                     'tremble_prob': [0.05]}


# global_cases_dict = {'detect_mobile': ['non_mobile', 'mobile'],  # Full version
#                      'Ethics_Consent': ['Consent', 'No_Consent'],
#                      'Introduction': ['all_correct', 'incorrect'],
#                      'BDM': ['success'],
#                      'Task_WTP': ['random'],
#                      'Exp_Prob': [[0.3, 0.5, 0.1, 0.1]],  # [(O1,O1), (O1,O2), (O2, O1), (O2,O2)]
#                      'tremble_prob': [0.05]}


def dict_product(dicts):
    """
    >>> list(dict_product(dict(number=[1,2], character='ab')))
    [{'character': 'a', 'number': 1},
     {'character': 'a', 'number': 2},
     {'character': 'b', 'number': 1},
     {'character': 'b', 'number': 2}]
    """
    import itertools
    return (dict(zip(dicts, x)) for x in itertools.product(*dicts.values()))


global_cases = list(dict_product(global_cases_dict))


def bot_control_choice(bot_type):
    if bot_type == 'Never_Experiment' or bot_type == 'Switch_to_Experiment':
        return 1
    if bot_type == 'Switch_from_Experiment' or bot_type == 'Always_Experiment':
        return 2


def bot_treatment_choice(bot_type):
    if bot_type == 'Never_Experiment' or bot_type == 'Switch_from_Experiment':
        return 1
    if bot_type == 'Switch_to_Experiment' or bot_type == 'Always_Experiment':
        return 2


def bot_should_play_app(self, app):
    """Determines whether bot should play app
    parameter app should correspond to Constants.name_in_url
    """
    if app == 'Introduction':  # User must consent to continue
        return True
    if app == 'BDM':  # User must get introduction questions correct to continue.
        return bot_should_play_app(self, 'Introduction') and self.case['Introduction'] == 'all_correct'
    if app == 'Task_WTP':  # No additional requirements
        return bot_should_play_app(self, 'BDM')
    if 'task' in app:
        return bot_should_play_app(self, 'BDM')
    if 'RET' in app:
        if 'path' not in self.player.participant.vars:  # Depends if we want to test Choice alone or not
            return bot_should_play_app(self, 'BDM')
        else:
            return bot_should_play_app(self, 'BDM') and \
                   (self.player.participant.path == 'Worst' or self.player.participant.path == 'Regular')
    if 'Menu' in app or app == 'Interim':
        return bot_should_play_app(self, 'RET')
    if app == 'Demog_Survey' or app == 'payment_info':
        if 'path' not in self.player.participant.vars:  # Depends if we want to test survey alone
            return bot_should_play_app(self, 'BDM')
        else:
            return bot_should_play_app(self, 'BDM')

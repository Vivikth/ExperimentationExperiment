def read_csv(filename):
    """Reads a CSV in random order"""
    import csv

    f = open(filename, encoding='cp1252')
    rows = list(csv.DictReader(f))

    # random.shuffle(rows)  # Randomisation is just a hindrance
    return rows


def value_function(task, player):
    """Returns a player's stated valuation for a task."""
    if task == 'T':
        return player.Tabulation_Value
    elif task == 'C':
        return player.Concealment_Value
    elif task == 'I':
        return player.Interpretation_Value
    elif task == 'R':
        return player.Replication_Value
    elif task == 'O':
        return player.Organisation_Value
    else:
        raise ValueError('Input must be first (capital) letter of a task name')


def list_subtract(first_list, second_list):
    """Set-difference, but for lists"""
    return list(set(first_list) - set(second_list))


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


def app_after_task(player, _upcoming_apps):
    """Returns next app after player has completed task"""
    import time
    if 'stage' not in player.participant.vars:
        player.participant.end_time = time.time()
        player.participant.time_taken = player.participant.end_time - player.participant.start_time
        return 'Demog_Survey'
    elif player.participant.stage == '1a':
        player.participant.stage = '1b'
        return 'Menu_Select'
    elif player.participant.stage == '1b':
        player.participant.stage = '2a'
        player.participant.pair = player.participant.pair2
        return 'Interim'
    elif player.participant.stage == '2a':
        player.participant.stage = '2b'
        return 'Menu_Select2'
    elif player.participant.stage == '2b':
        player.participant.stage = '3'
        player.participant.end_time = time.time()
        player.participant.time_taken = player.participant.end_time - player.participant.start_time
        return 'Demog_Survey'


def option_index(option):
    """Numeric value of option"""
    if option == "Option 1":
        return 1
    elif option == "Option 2":
        return 2


global_cases_dict = {'detect_mobile': ['non_mobile'],
                     'Ethics_Consent': ['Consent'],
                     'Introduction': ['all_correct'],
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
    if app == 'detect_mobile':
        return True
    if app == 'Ethics_Consent':  # Only non-mobile users can continue.
        return self.case['detect_mobile'] == 'non_mobile'
    if app == 'Introduction':  # User must consent to continue
        return bot_should_play_app(self, 'Ethics_Consent') and self.case['Ethics_Consent'] == 'Consent'
    if app == 'BDM':  # User must get introduction questions correct to continue.
        return bot_should_play_app(self, 'Introduction') and self.case['Introduction'] == 'all_correct'
    if app == 'Task_WTP':  # No additional requirements
        return bot_should_play_app(self, 'BDM')
    if 'task' in app:
        return bot_should_play_app(self, 'BDM')
    if 'RET' in app:
        if 'path' not in self.player.participant.vars:  # Depends if we want to test RET_Choice alone or not
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

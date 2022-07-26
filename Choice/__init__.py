import random
from otree.api import *

# from . import models
from Global_Functions import list_subtract

# Treatment, Pair1, pair2 are inputted before.

author = 'Vivikth'
doc = """Choosing a real effort task"""


class Constants(BaseConstants):
    name_in_url = 'RET_Choice1'
    players_per_group = None
    num_rounds = 1
    task_list = ["Option 1", "Option 2"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Control_Task_Choice = models.CharField(
        doc="Control_Task_Choice", choices=Constants.task_list, widget=widgets.RadioSelect,
    )
    Treatment_Caused_Switch = models.BooleanField(
        doc="Treatment_Caused_Switch"
    )
    Blunder_Task_Choice = models.CharField(
        doc="Blunder_Task_Choice", choices=Constants.task_list, widget=widgets.RadioSelect,
    )


# Need to add calculations determining whether player switched.


# FUNCTIONS
def creating_session(subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            if 'pair1' in player.session.config:
                player.participant.pair1 = player.session.config['pair1']
            if 'pair2' in player.session.config:
                player.participant.pair2 = player.session.config['pair2']
            if 'treatment_used1' in player.session.config:
                player.participant.treatment_used1 = player.session.config['treatment_used1']
            else:
                player.participant.treatment_used1 = random.choice(["Control", "Blunder"])
            # print(player.participant.treatment_used1)
        for tried in ['next_meal_day', 'next_meal_time', 'next_meal_date']:
            if tried in player.session.config:
                player.participant.vars[tried] = player.session.config[tried]
            else:
                pass


# PAGES
class RetChoiceIntroduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return 'stage' not in player.participant.vars


class BlunderTaskSelection(Page):
    form_model = 'player'
    form_fields = ['Blunder_Task_Choice']

    @staticmethod
    def vars_for_template(player: Player):
        all_tasks = ["Fancy Pizza", "Cheap Pizza", "Fancy Taco", "Cheap Taco"]
        stage_for_template = "1st"
        version_for_template = "A"
        good_task = player.participant.pair1[0]
        bad_task = player.participant.pair1[1]
        remaining_tasks = list_subtract(all_tasks, [good_task, bad_task])
        return {
            'Good_Task': good_task,
            'Bad_Task': bad_task,
            'stage_for_template': stage_for_template,
            'version_for_template': version_for_template,
            'remaining_tasks': remaining_tasks
        }


class ControlTaskSelection(Page):
    form_model = 'player'
    form_fields = ['Control_Task_Choice']

    @staticmethod
    def vars_for_template(player: Player):
        stage_for_template = "1st"
        version_for_template = "A"
        good_task = player.participant.pair1[0]
        bad_task = player.participant.pair1[1]
        task_info = player.participant.pair1[0]
        other_task = player.participant.pair2[0]
        return {
            'Good_Task': good_task,
            'Bad_Task': bad_task,
            'stage_for_template': stage_for_template,
            'Task_Info': task_info,
            'version_for_template': version_for_template,
            'Other_Task': other_task
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.blunder_choice = player.Blunder_Task_Choice
        player.participant.control_choice = player.Control_Task_Choice


class RandomPick(Page):
    @staticmethod
    def vars_for_template(player: Player):
        all_tasks = ["Fancy Pizza", "Cheap Pizza", "Fancy Taco", "Cheap Taco"]
        good_task = player.participant.pair1[0]
        bad_task = player.participant.pair1[1]
        task_info = player.participant.pair1[0]
        remaining_tasks = list_subtract(all_tasks, [good_task, bad_task])
        other_task = player.participant.pair2[0]
        BDM_Payout = player.participant.BDM_Num / 100 - 0.01
        return {
            'Good_Task': good_task,
            'Bad_Task': bad_task,
            'Other_Task': other_task,
            'Task_Info': task_info,
            'remaining_tasks': remaining_tasks,
            'BDM_Payout': BDM_Payout
        }

    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     if player.Task_Choice == player.Control_Task_Choice:
    #         player.Treatment_Caused_Switch = False
    #     else:
    #         player.Treatment_Caused_Switch = True
    #     if 'opt_choice2' not in player.participant.vars:
    #         player.participant.switched1 = player.Treatment_Caused_Switch
    #     else:
    #         player.participant.switched2 = player.Treatment_Caused_Switch

    # @staticmethod
    # def app_after_this_page(player: Player, upcoming_apps):
    #     opt_choice1 = player.participant.opt_choice1
    #     # print(Constants.name_in_url)
    #     # print('opt_choice2' in player.participant.vars)
    #     if 'opt_choice2' in player.participant.vars:
    #         player.participant.time_before_tasks = time.time()
    #         player.participant.task_to_complete = task_name_decoder(task_name(player.participant.pair[opt_choice1])) \
    #                                               + player.participant.stage
    #         return task_name_decoder(task_name(player.participant.pair[opt_choice1])) + player.participant.stage


page_sequence = [RetChoiceIntroduction, BlunderTaskSelection, ControlTaskSelection, RandomPick]


# def custom_export(players):
#     yield ['participant_code', 'participant_label', 'session_label',
#            'treatment_used1', 'treatment_used2',
#            'blunder_choice1', 'blunder_choice2',
#            'treatment_choice1', 'treatment_choice2',
#            'control_choice1', 'control_choice2',
#            'switched1', 'switched2']
#
#     for player in players:
#         participant = player.participant
#         for field in settings.PARTICIPANT_FIELDS:  # Custom Export doesn't like empty fields
#             if field not in participant.vars:
#                 if field not in ['lc1a', 'pair', 'stage', 'task_to_complete', 'opt_choice1', 'opt_choice2']:
#                     setattr(participant, field, None)
#         yield [participant.code, participant.label, participant.session.label,
#                participant.treatment_used1, participant.treatment_used2,
#                participant.blunder_choice1, participant.blunder_choice2,
#                participant.treatment_choice1, participant.treatment_choice2,
#                participant.control_choice1, participant.control_choice2,
#                participant.switched1, participant.switched2]

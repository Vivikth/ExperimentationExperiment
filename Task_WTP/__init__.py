from otree.api import *
import random
import time
import settings
from Global_Functions import value_function, list_subtract, find_min_diff, meal_name_from_task
from more_itertools import sort_together

# Make blunder menu options and control menu options.
# Need to check HTML (Task_WTP & BDM). DO THIS, then move onto next app.
author = "Vivikth"
doc = """ Determines subject's valuations for level-1 tasks """


class Constants(BaseConstants):
    name_in_url = 'Task_WTP'
    players_per_group = None
    num_rounds = 1
    Stage_Title = "Part 1 (continued): Applying the Switch-Point Procedure"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Elicitation Variables
    Fancy_Pizza_Value = models.FloatField(doc="Fancy_Pizza_Value", min=0, max=20,
                                          label="Your switch point for meal 1 is:")
    Cheap_Pizza_Value = models.FloatField(doc="Cheap_Pizza_Value", min=0, max=20,
                                          label="Your switch point for meal 2 is:")
    Fancy_Taco_Value = models.FloatField(doc="Fancy_Taco_Value", min=0, max=20,
                                         label="Your switch point for meal 3 is:")
    Cheap_Taco_Value = models.FloatField(doc="Cheap_Taco_Value", min=0, max=20,
                                         label="Your switch point for meal 4 is:")

    Rand_T = models.StringField(choices=["Fancy Pizza", "Cheap Pizza", "Fancy Taco", "Cheap Taco"])  # Foods
    Rand_Outcome = models.StringField(choices=["BW", "C"])  # Best, Worst Continue
    BDM_Num = models.IntegerField(min=1, max=2001)


class Trial(ExtraModel):
    player = models.Link(Player)
    question = models.StringField()
    optionA = models.StringField()
    optionB = models.StringField()
    optionC = models.StringField()
    optionD = models.StringField()
    solution = models.StringField()
    choice = models.StringField()
    is_correct = models.BooleanField()


# FUNCTIONS
def pair_generator(player: Player):
    all_tasks = ["Fancy Pizza", "Cheap Pizza", "Fancy Taco", "Cheap Taco"]

    participant = player.participant
    task_info_status = [participant.tried_fancy_pizza, participant.tried_cheap_pizza, participant.tried_fancy_taco,
                        participant.tried_cheap_taco]
    not_tried_tasks = [(task, _) for _, task in sorted(zip(task_info_status, all_tasks))]
    least_familiar_tasks = [thingo for thingo in not_tried_tasks if thingo[1] <= sorted(not_tried_tasks,
                                                                                        key=lambda x: x[1])[1][1]]

    def reorder_pair(pair):
        if value_function(pair[0], player) >= value_function(pair[1], player):
            return pair
        else:
            return pair[::-1]

    values = [value_function(thingo[0], player) for thingo in least_familiar_tasks]

    diff, index1, index2 = find_min_diff(values, len(values))
    pair1 = reorder_pair([least_familiar_tasks[index1][0], least_familiar_tasks[index2][0]])
    new_list = list_subtract(all_tasks, pair1)
    pair2 = reorder_pair(random.sample(new_list, 2))


    # pair (a,b) is the pair with least Likert rankings (i.e. subject is least familiar); a preferred to b.
    # pair1 = reorder_pair(not_tried_tasks[0:2])
    # new_list = list_subtract(all_tasks, pair1)
    # pair2 = reorder_pair(random.sample(new_list, 2))
    #
    # if len(not_tried_tasks) == 2:
    #     participant.tried_ge_3 = 0
    #     values = [value_function(task, player) for task in not_tried_tasks]
    #     pair1 = [task for _, task in sorted(zip(values, all_tasks), reverse=True)]  # Untried (x,y) with v(x) >= v(y)
    #     new_list = list_subtract(all_tasks, pair1)
    #     pair2 = reorder_pair(random.sample(new_list, 2))
    # elif len(not_tried_tasks) > 2:
    #     participant.tried_ge_3 = 0
    #     values = [value_function(task, player) for task in not_tried_tasks]
    #     diff, index1, index2 = find_min_diff(values, len(values))
    #     pair1 = reorder_pair([all_tasks[index1], all_tasks[index2]])  # Untried (x,y) with v(x) >= v(y)
    #     new_list = list_subtract(all_tasks, pair1)
    #     pair2 = reorder_pair(random.sample(new_list, 2))
    # else:
    #     participant.tried_ge_3 = 1
    #     pair1 = reorder_pair(random.sample(all_tasks, 2))
    #     new_list = list_subtract(all_tasks, pair1)
    #     pair2 = reorder_pair(random.sample(new_list, 2))

    return pair1, pair2


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        # Randomisation
        if 'Rand_T' in p.session.config:  # Random Task to complete
            p.Rand_T = p.session.config['Rand_T']
        else:
            p.Rand_T = random.choice(["Fancy Pizza", "Cheap Pizza", "Fancy Taco", "Cheap Taco"])
        p.participant.rand_task = meal_name_from_task(p.Rand_T)

        # Generate continuation_rv to determine whether program should continue or do best / worst task
        if 'continuation_rv' in p.session.config:
            continuation_rv = p.session.config['continuation_rv']
        else:
            continuation_rv = random.random()

        if continuation_rv <= 0.2:  # If BDM is to be implemented (20% probability)
            p.Rand_Outcome = "Yes_BDM"
            p.BDM_Num = random.randint(1, 2001)  # BDM Question Number to select
        else:
            p.Rand_Outcome = "No_BDM"  # If best / worst task is not selected.
            p.BDM_Num = 0  # These are placeholder values - they will never be accessed.
        p.participant.rand_outcome = p.Rand_Outcome
        p.participant.BDM_Num = p.BDM_Num
        for tried in ['tried_fancy_pizza', 'tried_cheap_pizza', 'tried_fancy_taco', 'tried_cheap_taco', 'next_meal_day',
                      'next_meal_time', 'next_meal_date', 'sample_meal_day', 'sample_meal_time', 'sample_meal_date']:
            if tried in p.session.config:
                p.participant.vars[tried] = p.session.config[tried]
            else:
                pass


def get_nullable(obj, field_name):
    try:
        return getattr(obj, field_name)
    except TypeError:
        return None


# PAGES
class WtpIntro(Page):
    pass


class InstructionPage(Page):
    form_model = 'player'
    form_fields = ['Fancy_Pizza_Value', 'Cheap_Pizza_Value', 'Fancy_Taco_Value',
                   'Cheap_Taco_Value']

    @staticmethod
    def live_method(player, data):
        if 'Fancy_Pizza_Value' in data:
            player.Fancy_Pizza_Value = data['Fancy_Pizza_Value']
        if 'Cheap_Pizza_Value' in data:
            player.Cheap_Pizza_Value = data['Cheap_Pizza_Value']
        if 'Fancy_Taco_Value' in data:
            player.Fancy_Taco_Value = data['Fancy_Taco_Value']
        if 'Cheap_Taco_Value' in data:
            player.Cheap_Taco_Value = data['Cheap_Taco_Value']

        if all(get_nullable(player, value) is not None for value in ['Fancy_Pizza_Value', 'Cheap_Pizza_Value',
                                                                     'Fancy_Taco_Value',
                                                                     'Cheap_Taco_Value']):
            names = ['Meal 1: Sandwiches, Wraps and Uncrustables', 'Meal 2: Hot Assorted Tarts',
                     'Meal 3: Individual Salads/Rice Paper Rolls', 'Meal 4: Hot Fork Dish']
            values = [player.Fancy_Pizza_Value, player.Cheap_Pizza_Value, player.Fancy_Taco_Value,
                      player.Cheap_Taco_Value]
            return {player.id_in_group: sort_together([values, names])[1][::-1]}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.Fancy_Pizza_Value = player.Fancy_Pizza_Value
        player.participant.Cheap_Pizza_Value = player.Cheap_Pizza_Value
        player.participant.Fancy_Taco_Value = player.Fancy_Taco_Value
        player.participant.Cheap_Taco_Value = player.Cheap_Taco_Value
        player.participant.switch_point = value_function(player.Rand_T, player)


class WtpConc(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.pair1, player.participant.pair2 = pair_generator(player)
        # print(player.participant.pair1, player.participant.pair2)
    # @staticmethod
    # def app_after_this_page(player: Player, upcoming_apps):
    #     if player.Rand_Outcome == "C":  # Continue with experiment without best or worst task.
    #         player.participant.path = "Regular"
    #         return 'Choice'
    #     elif player.Rand_Outcome == "BW":
    #         # print("value is ", value_function(player.Rand_T, player), )
    #         # print("BDM Num is ", player.BDM_Num)
    #         # print("lot outcome is ", player.lot_outcome)
    #         if value_function(player.Rand_T, player) > player.BDM_Num:  # Player values task more than lottery
    #             player.participant.task_to_complete = task_name_decoder(task_name(player.Rand_T)) + '0'
    #             player.participant.lc1a = 1  # Set task level to 1.
    #             player.participant.time_before_tasks = time.time()
    #             player.participant.path = "Single_Task"
    #             return task_name_decoder(task_name(player.Rand_T)) + '0'
    #         else:
    #             if player.lot_outcome < player.BDM_Num:  # Player gets best task as lottery outcome
    #                 player.participant.path = "Best"
    #                 player.participant.end_time = time.time()
    #                 player.participant.time_taken = player.participant.end_time - player.participant.start_time
    #                 return "Demog_Survey"
    #             else:  # Player gets worst task as lottery outcome
    #                 player.participant.path = "Worst"

    @staticmethod
    def vars_for_template(player: Player):
        switch_point = value_function(player.Rand_T, player)
        return {
            'switch_point': switch_point,
            'selected_task': player.Rand_T
        }



page_sequence = [WtpIntro, InstructionPage, WtpConc]

# def custom_export(players):
#     yield ['participant_code', 'participant_label', 'session_label',
#            'Concealment_Value', 'Fancy_Pizza_Value', 'Interpretation_Value',
#            'Replication_Value', 'Organisation_Value',
#            'pair1', 'pair2', 'sub_menu1', 'sub_menu2',
#            'path', 'rand_task']
#
#     for player in players:
#         participant = player.participant
#         for field in settings.PARTICIPANT_FIELDS:  # Custom Export doesn't like empty fields
#             if field not in participant.vars:
#                 if field not in ['lc1a', 'pair', 'stage', 'task_to_complete', 'opt_choice1', 'opt_choice2']:
#                     setattr(participant, field, None)
#         yield [participant.code, participant.label, participant.session.label,
#                participant.Concealment_Value, participant.Fancy_Pizza_Value, participant.Interpretation_Value,
#                participant.Replication_Value, participant.Organisation_Value,
#                participant.pair1, participant.pair2, participant.sub_menu1, participant.sub_menu2,
#                participant.path, participant.rand_task]

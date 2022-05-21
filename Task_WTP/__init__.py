from otree.api import *
import random
import time
import settings
from Global_Functions import read_csv, value_function, list_subtract, task_name_decoder, task_name
from more_itertools import sort_together

author = "Vivikth"
doc = """ Determines subject's valuations for level-1 tasks """


class Constants(BaseConstants):
    name_in_url = 'Task_WTP'
    players_per_group = None
    num_rounds = 1
    Stage_Title = "Applying the Switch-Point Procedure"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Elicitation Variables
    Tabulation_Value = models.FloatField(doc="Tabulation_Value", min=0, max=100,
                                         label="Your switch point for the tabulation task is:")
    Concealment_Value = models.FloatField(doc="Concealment_Value", min=0, max=100,
                                          label="Your switch point for the concealment task is:")
    Interpretation_Value = models.FloatField(doc="Interpretation_Value", min=0, max=100,
                                             label="Your switch point for the interpretation task is:")
    Replication_Value = models.FloatField(doc="Replication_Value", min=0, max=100,
                                          label="Your switch point for the replication task is:")
    Organisation_Value = models.FloatField(doc="Organisation_Value", min=0, max=100,
                                           label="Your switch point for the organisation task is:")
    # Randomisation Variables
    BDM_Num = models.IntegerField(min=0, max=100)
    Rand_Outcome = models.StringField(choices=["BW", "C"])  # Best, Worst Continue
    Rand_T = models.StringField(choices=["T", "C", "I", "R", "O"])  # Tasks
    lot_outcome = models.IntegerField(min=0, max=100)

    # Boring Task Variables
    num_correct = models.IntegerField(initial=0)
    raw_responses = models.LongStringField()
    num_trials = models.IntegerField()


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


def to_dict(trial: Trial):
    return dict(
        question=trial.question,
        optionA=trial.optionA,
        optionB=trial.optionB,
        optionC=trial.optionC,
        optionD=trial.optionD,
        id=trial.id,
        solution=trial.solution
    )


# FUNCTIONS
def pair_generator(player: Player, exclude):
    all_tasks = ['T', 'C', 'I', 'R', 'O']
    ex_task = [exclude]
    la = list_subtract(all_tasks, ex_task)

    def reorder_pair(pair):
        if value_function(pair[0], player) >= value_function(pair[1], player):
            return pair
        else:
            return pair[::-1]

    pair1 = reorder_pair(random.sample(la, 2))
    new_list = list_subtract(la, pair1)
    pair2 = reorder_pair(random.sample(new_list, 2))

    return pair1, pair2


def sub_control_menu_generator(input_task):
    def all_levels(task):
        return [(task_name(task), i) for i in range(2, 5)]

    tuples_to_remove = all_levels(input_task)
    all_tasks = all_levels('T') + all_levels('C') + all_levels('I') + all_levels('R') + all_levels('O')
    tasks_to_choose = list_subtract(all_tasks, tuples_to_remove)
    menu_options = random.sample(tasks_to_choose, 3)
    return menu_options


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        # Boring Task Question Setup
        stimuli = read_csv('Task_WTP/BoringQs.csv')
        p.num_trials = len(stimuli)
        p.num_correct = 0
        for stim in stimuli:
            Trial.create(player=p, **stim)

        # Randomisation
        if 'Rand_T' in p.session.config:  # Random Task to complete
            p.Rand_T = p.session.config['Rand_T']
        else:
            p.Rand_T = random.choice(["T", "C", "I", "R", "O"])
        p.participant.rand_task = p.Rand_T

        # Generate continuation_rv to determine whether program should continue or do best / worst task
        if 'continuation_rv' in p.session.config:
            continuation_rv = p.session.config['continuation_rv']
        else:
            continuation_rv = random.random()

        if continuation_rv <= 0.05:  # If best / worst task is selected
            p.Rand_Outcome = "BW"
            p.BDM_Num = random.randint(0, 100)  # BDM Question Number to select
            if 'lot_outcome' in p.session.config:  # Result of Lottery between best and worst task.
                p.lot_outcome = p.session.config['lot_outcome']
            else:
                p.lot_outcome = random.randint(0, 100)
        else:
            p.Rand_Outcome = "C"  # If best / worst task is not selected.
            p.BDM_Num = 0         # These are placeholder values - they will never be accessed.
            p.lot_outcome = 0


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
    form_fields = ['Tabulation_Value', 'Concealment_Value', 'Replication_Value',
                   'Interpretation_Value', 'Organisation_Value']

    @staticmethod
    def live_method(player, data):
        if 'Tabulation_Value' in data:
            player.Tabulation_Value = data['Tabulation_Value']
        if 'Concealment_Value' in data:
            player.Concealment_Value = data['Concealment_Value']
        if 'Interpretation_Value' in data:
            player.Interpretation_Value = data['Interpretation_Value']
        if 'Replication_Value' in data:
            player.Replication_Value = data['Replication_Value']
        if 'Organisation_Value' in data:
            player.Organisation_Value = data['Organisation_Value']

        if all(get_nullable(player, value) is not None for value in ['Tabulation_Value', 'Concealment_Value',
                                                                     'Replication_Value',
                                                                     'Interpretation_Value', 'Organisation_Value']):
            names = ['Tabulation', 'Concealment', 'Replication', 'Interpretation', 'Organisation']
            values = [player.Tabulation_Value, player.Concealment_Value, player.Replication_Value,
                      player.Interpretation_Value, player.Organisation_Value]
            return {player.id_in_group: sort_together([values, names])[1][::-1]}


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.Tabulation_Value = player.Tabulation_Value
        player.participant.Concealment_Value = player.Concealment_Value
        player.participant.Interpretation_Value = player.Interpretation_Value
        player.participant.Replication_Value = player.Replication_Value
        player.participant.Organisation_Value = player.Organisation_Value



class WtpConc(Page):

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.pair1, player.participant.pair2 = pair_generator(player, player.Rand_T)
        player.participant.pair = player.participant.pair1
        player.participant.sub_menu1 = sub_control_menu_generator(player.participant.pair1[1])
        player.participant.sub_menu2 = sub_control_menu_generator(player.participant.pair2[1])

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.Rand_Outcome == "C":  # Continue with experiment without best or worst task.
            player.participant.path = "Regular"
            return 'RET_Choice'
        elif player.Rand_Outcome == "BW":
            # print("value is ", value_function(player.Rand_T, player), )
            # print("BDM Num is ", player.BDM_Num)
            # print("lot outcome is ", player.lot_outcome)
            if value_function(player.Rand_T, player) > player.BDM_Num:  # Player values task more than lottery
                player.participant.task_to_complete = task_name_decoder(task_name(player.Rand_T)) + '0'
                player.participant.lc1a = 1  # Set task level to 1.
                player.participant.time_before_tasks = time.time()
                player.participant.path = "Single_Task"
                return task_name_decoder(task_name(player.Rand_T)) + '0'
            else:
                if player.lot_outcome < player.BDM_Num:  # Player gets best task as lottery outcome
                    player.participant.path = "Best"
                    player.participant.end_time = time.time()
                    player.participant.time_taken = player.participant.end_time - player.participant.start_time
                    return "Demog_Survey"
                else:  # Player gets worst task as lottery outcome
                    player.participant.path = "Worst"

    @staticmethod
    def vars_for_template(player: Player):
        switch_point = value_function(player.Rand_T, player)
        return {
            'switch_point': switch_point,
            'selected_task': task_name(player.Rand_T)
        }


class Boring(Page):
    form_model = 'player'
    form_fields = ['raw_responses']

    @staticmethod
    def is_displayed(player: Player):
        return not player.participant._is_bot


    @staticmethod
    def js_vars(player: Player):
        stimuli = [to_dict(trial) for trial in Trial.filter(player=player)]
        return dict(trials=stimuli)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import json
        responses = json.loads(player.raw_responses)
        for trial in Trial.filter(player=player):
            # have to use str() because Javascript implicitly converts keys to strings
            trial.choice = responses[str(trial.id)]
            trial.is_correct = trial.choice == trial.solution
            player.num_correct += int(trial.is_correct)


class BoringConc(Page):
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return "RET_Choice"


page_sequence = [WtpIntro, InstructionPage, WtpConc, Boring, BoringConc]


def custom_export(players):
    yield ['participant_code', 'participant_label', 'session_label',
           'Concealment_Value', 'Tabulation_Value', 'Interpretation_Value',
           'Replication_Value', 'Organisation_Value',
           'pair1', 'pair2', 'sub_menu1', 'sub_menu2',
           'path', 'rand_task']

    for player in players:
        participant = player.participant
        for field in settings.PARTICIPANT_FIELDS:  # Custom Export doesn't like empty fields
            if field not in participant.vars:
                if field not in ['lc1a', 'pair', 'stage', 'task_to_complete', 'opt_choice1', 'opt_choice2']:
                    setattr(participant, field, None)
        yield [participant.code, participant.label, participant.session.label,
               participant.Concealment_Value, participant.Tabulation_Value, participant.Interpretation_Value,
               participant.Replication_Value, participant.Organisation_Value,
               participant.pair1, participant.pair2, participant.sub_menu1, participant.sub_menu2,
               participant.path, participant.rand_task]

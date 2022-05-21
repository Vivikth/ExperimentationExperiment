from otree.api import *
#  Need to transfer old app in.
import settings
from Global_Functions import read_csv
from more_itertools import sort_together

author = 'Vivikth'  # This app was based off questions_from_csv in Otree Snippets
doc = """Introduces and tests subjects on BDM Procedure"""


class C(BaseConstants):
    NAME_IN_URL = 'BDM'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    # print("BDM creating_session running!")
    for p in subsession.get_players():
        stimuli = read_csv('BDM/BDMQs.csv')
        p.num_trials = len(stimuli)
        p.participant.BDM_Score = 0
        for stim in stimuli:
            Trial.create(player=p, **stim)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    raw_responses = models.LongStringField(blank=True)
    num_trials = models.IntegerField()
    Q1_Correct = models.BooleanField()
    Q2_Correct = models.BooleanField()
    Q3_Correct = models.BooleanField()
    Q4_Correct = models.BooleanField()
    Q5_Correct = models.BooleanField()
    # Fancy_Pizza_Value = models.FloatField(doc="Fancy_Pizza_Value", min=0, max=100,
    #                                       label="Your switch point for the fancy pizza is:")
    # Cheap_Pizza_Value = models.FloatField(doc="Cheap_Pizza_Value", min=0, max=100,
    #                                       label="Your switch point for the cheap pizza task is:")
    # Fancy_Taco_Value = models.FloatField(doc="Fancy_Taco_Value", min=0, max=100,
    #                                      label="Your switch point for the fancy taco task is:")
    # Cheap_Taco_Value = models.FloatField(doc="Cheap_Taco_Value", min=0, max=100,
    #                                      label="Your switch point for the cheap taco task is:")
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

class Trial(ExtraModel):
    player = models.Link(Player)
    question = models.StringField()
    optionA = models.StringField()
    optionB = models.StringField()
    optionC = models.StringField()
    optionD = models.StringField()
    solution = models.StringField()
    Qnum = models.StringField()
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
        Qnum=trial.Qnum,
        solution=trial.solution
    )


# Functions
def get_nullable(obj, field_name):
    try:
        return getattr(obj, field_name)
    except TypeError:
        return None

# PAGES
class BDMIntro(Page):
    pass


class Stimuli(Page):
    form_model = 'player'
    form_fields = ['raw_responses']

    @staticmethod
    def js_vars(player: Player):
        stimuli = [to_dict(trial) for trial in Trial.filter(player=player)]
        return dict(trials=stimuli)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import json
        # print(player.raw_responses, Trial.filter(player=player)[0].id)
        # print(type(player.raw_responses))
        # print(Trial.filter(player=player)[0].solution)
        responses = json.loads(player.raw_responses)
        for trial in Trial.filter(player=player):
            # have to use str() because Javascript implicitly converts keys to strings
            trial.choice = responses[str(trial.id)]
            trial.is_correct = trial.choice == trial.solution
            player.participant.BDM_Score += int(trial.is_correct)
            # print(trial.Qnum)
            # For getting question correct in horizontal data
            if trial.Qnum == str(1.0):
                player.Q1_Correct = trial.is_correct
                player.participant.Q1_Correct = player.Q1_Correct
            elif trial.Qnum == str(2.0):
                player.Q2_Correct = trial.is_correct
                player.participant.Q2_Correct = player.Q2_Correct
            elif trial.Qnum == str(3.0):
                player.Q3_Correct = trial.is_correct
                player.participant.Q3_Correct = player.Q3_Correct
            elif trial.Qnum == str(4.0):
                player.Q4_Correct = trial.is_correct
                player.participant.Q4_Correct = player.Q4_Correct
            elif trial.Qnum == str(5.0):
                player.Q5_Correct = trial.is_correct
                player.participant.Q5_Correct = player.Q5_Correct


class ElicitIntro(Page):
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


page_sequence = [BDMIntro, Stimuli, ElicitIntro]

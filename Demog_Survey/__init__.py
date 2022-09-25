from otree.api import *
import time
import settings

author = 'Vivikth'
doc = """Demographic Survey to be completed at the end of experiment"""


class Constants(BaseConstants):
    name_in_url = 'Demog_Survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(doc="Age", min=0, max=100,
                              label="What is your age?")
    gender = models.StringField(doc="Gender",
                                choices=["Male", "Female", "Self-Report", "Prefer not to answer"],
                                label="What is your gender? Enter in the field below if you'd prefer to Self-Report.")
    gender_self_select = models.StringField(doc="Gender_self_select",
                                            blank=True)
    study = models.StringField(doc="study", label="Which of the following best describes your field of study?")
    econ_classes = models.IntegerField(doc="econ_classes",
                                       label="How many economics classes have you taken so far?")
    years = models.IntegerField(doc="years")
    GPA = models.FloatField(doc="GPA", label="What is your university GPA?", min=0, max=7)


# FUNCTIONS
def study_choices(_player):
    return ['Business and Economics', 'Engineering and Computer Science', 'Science',
            'Arts and Social Sciences', 'Law', 'Other']


# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'gender_self_select', 'study', 'econ_classes',
                   'years', 'GPA']

    @staticmethod
    def error_message(player, values):
        if values['gender'] == "Self-Report" and values['gender_self_select'] == '':
            return 'You must type in a gender if you selected Self-report'
        if values['gender'] != "Self-Report" and values['gender_self_select'] != '':
            return 'You can only type your gender if you selected Self-report'


    @staticmethod
    def vars_for_template(player: Player):
        return {
            'gender_self_select_label': 'Please enter your gender if you would prefer to self-report'
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.end_time = time.time()
        player.participant.time_taken = player.participant.end_time - player.participant.start_time
        player.participant.payoff += 10


class FinalPage(Page):
    pass


def custom_export(players):
    yield ['participant_code', 'participant_label', 'session_label', '_is_bot', # Global Variables
           'participant_payoff',
           'start_time', 'end_time', 'time_taken',  # Time Variables
           'BDM_Score', 'Q1_Correct', 'Q2_Correct',  # BDM
           'Q3_Correct', 'Q4_Correct', 'Q5_Correct',
           'Fancy_Pizza_Value', 'Cheap_Pizza_Value', 'Fancy_Taco_Value', 'Cheap_Taco_Value',  # Task_WTP
           'pair1', 'pair2', 'rand_task', 'rand_outcome', 'BDM_Num', 'BDM_Payout',
           'treatment_used1', 'blunder_choice', 'control_choice',  # RET_Choice
           'bret_payoff', 'r1_boxes', 'r2_boxes', 'r1_bomb',  # Risk Task
           'r2_bomb',
           'b5q1', 'b5q2', 'b5q3', 'b5q4', 'b5q5', 'b5q6', 'b5q7', 'b5q8', 'b5q9', 'b5q10',  # bigfive
           'extraversion', 'agreeableness', 'conscientiousness', 'emotionally_stable', 'openness',
           'age', 'gender', 'gender_self_select',  # Demographic
           'study', 'econ_classes', 'years', 'GPA']

    for player in players:
        participant = player.participant

        for field in settings.PARTICIPANT_FIELDS:  # Custom Export doesn't like empty fields
            if field not in participant.vars:
                if field not in ['lc1a', 'pair', 'stage', 'task_to_complete', 'opt_choice1', 'opt_choice2']:
                    setattr(participant, field, None)

        yield [participant.code, participant.label, participant.session.label, participant._is_bot, # Global Vars
               participant.payoff,
               participant.start_time, participant.end_time, participant.time_taken,  # Time Variables
               participant.BDM_Score, participant.Q1_Correct, participant.Q2_Correct,  # BDM
               participant.Q3_Correct, participant.Q4_Correct, participant.Q5_Correct,
               participant.Fancy_Pizza_Value, participant.Cheap_Pizza_Value,  # Task_WTP
               participant.Fancy_Taco_Value, participant.Cheap_Taco_Value,
               participant.pair1, participant.pair2,
               participant.rand_task, participant.rand_outcome, participant.BDM_Num, participant.BDM_Payout,
               participant.treatment_used1,  # RET_Choice
               participant.blunder_choice, participant.control_choice,
               participant.bret_payoff, participant.r1_boxes, participant.r2_boxes, participant.r1_bomb,  # bret
               participant.r2_bomb,
               participant.b5q1, participant.b5q2, participant.b5q3, participant.b5q4, participant.b5q5,
               participant.b5q6, participant.b5q7, participant.b5q8, participant.b5q9, participant.b5q10,
               participant.extraversion, participant.agreeableness, participant.conscientiousness,
               participant.emotionally_stable, participant.openness,
               player.age, player.gender, player.gender_self_select,  # Demographic
               player.study, player.econ_classes, player.years, player.GPA]


page_sequence = [Survey, FinalPage]

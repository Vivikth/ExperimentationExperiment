from otree.api import *

import settings

author = 'Vivikth'
doc = """Demographic Survey to be completed at the end of experiment"""


class Constants(BaseConstants):
    name_in_url = 'Demog_Survey'
    players_per_group = None
    num_rounds = 1
    identify_tasks = ['identify_tabulation', 'identify_organisation',
                      'identify_replication', 'identify_concealment', 'identify_interpretation']


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
    GPA = models.FloatField(doc="GPA", label="What is your university GPA?")

    identify = models.StringField(doc="identify",
                                  choices=["Yes", "No"],
                                  label="Did you correctly identify any of the tasks before completing them?")
    identify_tabulation = models.BooleanField(blank=True, label="Tabulation", widget=widgets.CheckboxInput)
    identify_organisation = models.BooleanField(blank=True, label="Organisation", widget=widgets.CheckboxInput)
    identify_replication = models.BooleanField(blank=True, label="Replication", widget=widgets.CheckboxInput)
    identify_concealment = models.BooleanField(blank=True, label="Concealment", widget=widgets.CheckboxInput)
    identify_interpretation = models.BooleanField(blank=True, label="Interpretation", widget=widgets.CheckboxInput)


# FUNCTIONS
def study_choices(_player):
    return ['Business and Economics', 'Engineering and Computer Science', 'Science',
            'Arts and Social Sciences', 'Law', 'Other']


def creating_session(subsession):
    for player in subsession.get_players():
        participant = player.participant


# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'gender_self_select', 'study', 'econ_classes',
                   'years', 'GPA', 'identify'] + Constants.identify_tasks

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


def custom_export(players):
    yield ['participant_code', 'participant_label', 'session_label', '_is_bot',  # Global Variables
           'treatment', 'start_time', 'end_time',  # Introduction
           'time_before_tasks', 'time_taken',
           'BDM_Score', 'Q1_Correct', 'Q2_Correct',  # BDM
           'Q3_Correct', 'Q4_Correct', 'Q5_Correct',
           'Concealment_Value', 'Tabulation_Value',  # Task_WTP
           'Interpretation_Value', 'Replication_Value', 'Organisation_Value',
           'pair1', 'pair2', 'sub_menu1', 'sub_menu2',
           'path', 'rand_task',
           'treatment_used1', 'treatment_used2',  # RET_Choice
           'blunder_choice1', 'blunder_choice2',
           'treatment_choice1', 'treatment_choice2',
           'control_choice1', 'control_choice2',
           'switched1', 'switched2',
           'menu_choice1', 'menu_choice2',  # Menu_Select
           'age', 'gender', 'gender_self_select',  # Demographic
           'study', 'econ_classes', 'years', 'GPA',
           'identify', 'identify_tabulation', 'identify_organisation',
           'identify_replication', 'identify_concealment', 'identify_interpretation']

    for player in players:
        participant = player.participant

        for field in settings.PARTICIPANT_FIELDS:  # Custom Export doesn't like empty fields
            if field not in participant.vars:
                if field not in ['lc1a', 'pair', 'stage', 'task_to_complete', 'opt_choice1', 'opt_choice2']:
                    setattr(participant, field, None)

        yield [participant.code, participant.label, participant.session.label, participant._is_bot,  # Global Vars
               participant.treatment, participant.start_time, participant.end_time,  # Introduction
               participant.time_before_tasks, participant.time_taken,
               participant.BDM_Score, participant.Q1_Correct, participant.Q2_Correct,  # BDM
               participant.Q3_Correct, participant.Q4_Correct, participant.Q5_Correct,
               participant.Concealment_Value, participant.Tabulation_Value,  # Task_WTP
               participant.Interpretation_Value, participant.Replication_Value, participant.Organisation_Value,
               participant.pair1, participant.pair2, participant.sub_menu1, participant.sub_menu2,
               participant.path, participant.rand_task,
               participant.treatment_used1, participant.treatment_used2,  # RET_Choice
               participant.blunder_choice1, participant.blunder_choice2,
               participant.treatment_choice1, participant.treatment_choice2,
               participant.control_choice1, participant.control_choice2,
               participant.switched1, participant.switched2,
               participant.menu_choice1, participant.menu_choice2,  # Menu_Select
               player.age, player.gender, player.gender_self_select,  # Demographic
               player.study, player.econ_classes, player.years, player.GPA,
               player.identify, player.identify_tabulation, player.identify_organisation,
               player.identify_replication, player.identify_concealment, player.identify_interpretation]


page_sequence = [Survey]

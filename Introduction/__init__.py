from otree.api import *
from Global_Functions import Binary_Choice_List, Likert_Familiarity_List
import time

doc = """
The app that introduces subjects to the experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PAYMENT_AMOUNT = 10  # May need to be updated later on


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sona_id = models.IntegerField(min=1000, max=9999)  # Inclusive, but unlikely endpoint IDs will be triggered
    agreement = models.BooleanField(
        label='I agree to participate in the project',
        choices=[
            [False, 'No'],
            [True, 'Yes'],
        ],
        widget=widgets.RadioSelectHorizontal,
    )
    name = models.StringField()
    date = models.StringField()


    Tried_Fancy_Pizza = models.IntegerField(label='How familiar are you with the items in meal 1?',
                                            choices=Likert_Familiarity_List,
                                            widget=widgets.RadioSelectHorizontal,
                                            )
    Tried_Cheap_Pizza = models.IntegerField(label='How familiar are you with the items in meal 2?',
                                            choices=Likert_Familiarity_List,
                                            widget=widgets.RadioSelectHorizontal,
                                            )
    Tried_Fancy_Taco = models.IntegerField(label='How familiar are you with the items in meal 3?',
                                           choices=Likert_Familiarity_List,
                                           widget=widgets.RadioSelectHorizontal,
                                           )
    Tried_Cheap_Taco = models.IntegerField(label='How familiar are you with the items in meal 4?',
                                           choices=Likert_Familiarity_List,
                                           widget=widgets.RadioSelectHorizontal,
                                           )
    payment_question = models.FloatField(doc="payment_question")


# FUNCTIONS
def agreement_error_message(_player: Player, value):
    if value is False:
        return 'You must agree to participate in this experiment to continue.'  # May need to fix error message


def payment_question_error_message(_player, value):
    if value != C.PAYMENT_AMOUNT:
        return "Your answer was incorrect. Please try again."


def creating_session(subsession):
    for player in subsession.get_players():
        player.participant.next_meal_day = player.session.config["next_meal_day"]
        player.participant.next_meal_time = player.session.config["next_meal_time"]
        player.participant.next_meal_date = player.session.config["next_meal_date"]
        player.participant.sample_meal_day = player.session.config["sample_meal_day"]
        player.participant.sample_meal_time = player.session.config["sample_meal_time"]
        player.participant.sample_meal_date = player.session.config["sample_meal_date"]


# PAGES
class SonaID(Page):
    form_model = 'player'
    form_fields = ['sona_id']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.label = str(player.sona_id)  # oTree requires label to be a string (?)


class Introduction(Page):
    form_model = 'player'
    form_fields = ['payment_question', 'Tried_Fancy_Pizza', 'Tried_Cheap_Pizza', 'Tried_Fancy_Taco', 'Tried_Cheap_Taco']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.tried_fancy_pizza = player.Tried_Fancy_Pizza # Meal 1: Sandwiches, Wraps and Uncrustables
        player.participant.tried_cheap_pizza = player.Tried_Cheap_Pizza  # Meal 2: Hot Assorted Tarts
        player.participant.tried_fancy_taco = player.Tried_Fancy_Taco # Meal 3: Individual Salads / Rice Paper Rolls
        player.participant.tried_cheap_taco = player.Tried_Cheap_Taco # Meal 4: Hot fork dishes
        player.participant.start_time = time.time()


class InformationSheet(Page):
    form_model = 'player'
    form_fields = [
        'agreement',
        'name',
    ]



page_sequence = [SonaID, InformationSheet, Introduction]

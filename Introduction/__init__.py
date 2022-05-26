from otree.api import *
from Global_Functions import Binary_Choice_List

doc = """
The app that introduces subjects to the experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PAYMENT_AMOUNT = 20  # May need to be updated later on


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
    Tried_Fancy_Pizza = models.BooleanField(label='I have tried the fancy pizza before',
                                            choices=Binary_Choice_List,
                                            widget=widgets.RadioSelectHorizontal,
                                            )
    Tried_Cheap_Pizza = models.BooleanField(label='I have tried the cheap pizza before',
                                            choices=Binary_Choice_List,
                                            widget=widgets.RadioSelectHorizontal,
                                            )
    Tried_Fancy_Taco = models.BooleanField(label='I have tried the fancy taco before',
                                           choices=Binary_Choice_List,
                                           widget=widgets.RadioSelectHorizontal,
                                           )
    Tried_Cheap_Taco = models.BooleanField(label='I have tried the cheap taco before',
                                           choices=Binary_Choice_List,
                                           widget=widgets.RadioSelectHorizontal,
                                           )


# FUNCTIONS
def agreement_error_message(_player: Player, value):
    if value is False:
        return 'You must agree to participate in this experiment to continue.'  # May need to fix error message


# PAGES
class SonaID(Page):
    form_model = 'player'
    form_fields = ['sona_id']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.label = str(player.sona_id)  # oTree requires label to be a string (?)


class Introduction(Page):
    pass


class InformationSheet(Page):
    form_model = 'player'
    form_fields = [
        'agreement',
        'name',
    ]


class TriedBefore(Page):
    form_model = 'player'
    form_fields = [
        'Tried_Fancy_Pizza',
        'Tried_Cheap_Pizza',
        'Tried_Fancy_Taco',
        'Tried_Cheap_Taco'
    ]


page_sequence = [SonaID, InformationSheet, Introduction, TriedBefore]

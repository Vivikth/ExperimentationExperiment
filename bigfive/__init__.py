from otree.api import *

doc = """Big 5 personality test"""


class C(BaseConstants):
    NAME_IN_URL = 'bigfive'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_q(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4, 5, 6, 7], widget=widgets.RadioSelect)


class Player(BasePlayer):
    q1 = make_q('... Extraverted, enthusiastic')
    q2 = make_q('... Critical, quarrelsome')
    q3 = make_q('... Dependable, self-disciplined')
    q4 = make_q('... Anxious, easily upset')
    q5 = make_q('... Open to new experiences, complex')
    q6 = make_q('... Reserved, quiet')
    q7 = make_q('... Sympathetic, warm')
    q8 = make_q('... Disorganized, careless')
    q9 = make_q('... Calm, emotionally stable')
    q10 = make_q('... Conventional, uncreative')

    extraversion = models.FloatField()
    agreeableness = models.FloatField()
    conscientiousness = models.FloatField()
    emotionally_stable = models.FloatField()
    openness = models.FloatField()


def combine_score(positive, negative):
    return 4 + (positive - negative) / 2


class Survey(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.extraversion = combine_score(player.q1, player.q6)
        player.agreeableness = combine_score(player.q7, player.q2)
        player.conscientiousness = combine_score(player.q3, player.q8)
        player.emotionally_stable = combine_score(player.q9, player.q4)
        player.openness = combine_score(player.q5, player.q10)


class Results(Page):
    pass


# page_sequence = [Survey, Results]
page_sequence = [Survey]

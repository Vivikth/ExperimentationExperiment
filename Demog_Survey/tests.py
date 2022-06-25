import random

from . import *
from otree.api import Bot
from Global_Functions import global_cases, bot_should_play_app


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            age = random.choice([18, 19, 20, 21, 22, 23, 24, 25, 26])
            gender = random.choice(["Male", "Female", "Prefer not to answer"])
            study = random.choice(['Business and Economics', 'Engineering and Computer Science', 'Science',
                                   'Arts and Social Sciences', 'Law', 'Other'])
            econ_classes = random.choice([0, 1, 2, 3, 4, 5])
            years = random.choice([0, 1, 2, 3, 4, 5])
            gpa = random.choice([3, 4, 5, 6, 7])
            yield Survey, dict(age=age, gender=gender, study=study, econ_classes=econ_classes,
                               years=years, GPA=gpa, identify="No")

from . import *
from otree.api import Bot, Submission
from Global_Functions import global_cases, bot_should_play_app
import random


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            yield WtpIntro
            yield Submission(InstructionPage, dict(
                Fancy_Pizza_Value=random.randint(0, 100),
                Cheap_Pizza_Value=random.randint(0, 100),
                Fancy_Taco_Value=random.randint(0, 100),
                Cheap_Taco_Value=random.randint(0, 100)))
            yield WtpConc

from . import *
from otree.api import Bot
from Global_Functions import global_cases, bot_should_play_app
import random


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, C.NAME_IN_URL):
            random_list = []
            for i in range(10):
                n = random.randint(1, 7)
                random_list.append(n)
            yield_dict = {}
            for j, q_num in enumerate(['q' + str(i) for i in range(1, 11)]):
                yield_dict[q_num] = random_list[j]
            yield Survey, yield_dict

from . import *
from otree.api import Bot
from Global_Functions import global_cases, bot_control_choice, bot_treatment_choice, bot_should_play_app
import random


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            yield RetChoiceIntroduction
            type_draw = random.random()
            if type_draw < self.case['Exp_Prob'][0]:
                bot_type = 'Never_Experiment'
            elif type_draw < self.case['Exp_Prob'][0] + self.case['Exp_Prob'][1]:
                bot_type = 'Switch_to_Experiment'
            elif type_draw < self.case['Exp_Prob'][0] + self.case['Exp_Prob'][1] + self.case['Exp_Prob'][2]:
                bot_type = 'Switch_from_Experiment'
            else:
                bot_type = 'Always_Experiment'

            control_choice = bot_control_choice(bot_type)
            blunder_choice = 1
            control_tremble_draw = random.random()
            blunder_tremble_draw = random.random()
            if control_tremble_draw < self.case['tremble_prob']:
                control_choice = 3 - control_choice
            if blunder_tremble_draw < self.case['tremble_prob']:
                blunder_choice = 3 - blunder_choice

            yield FirstChoice, dict(Blunder_Task_Choice="Option %i" % blunder_choice)
            yield SecondChoice, dict(Control_Task_Choice="Option %i" % control_choice)
            yield RandomPick

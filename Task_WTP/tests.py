from . import *
from otree.api import Bot, Submission
from Global_Functions import global_cases, bot_should_play_app
import random


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            yield WtpIntro
            # yield Submission(InstructionPage, dict(
            #     Tabulation_Value=0,
            #     Concealment_Value=0,
            #     Interpretation_Value=0,
            #     Replication_Value=0,
            #     Organisation_Value=0), check_html=False)
            yield Submission(InstructionPage, dict(
                Tabulation_Value=random.randint(0, 100),
                Concealment_Value=random.randint(0, 100),
                Interpretation_Value=random.randint(0, 100),
                Replication_Value=random.randint(0, 100),
                Organisation_Value=random.randint(0, 100)), check_html=False)
            yield WtpConc
            if self.player.participant.path != 'Regular' and self.player.participant.path != 'Single_Task':
                if self.player.participant.path == 'Worst':
                    yield BoringConc

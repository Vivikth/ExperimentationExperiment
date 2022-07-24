import json

from . import *
from otree.api import Bot, Submission
from Global_Functions import global_cases, bot_should_play_app




class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, C.NAME_IN_URL):
            if self.case['Introduction'] == 'all_correct':
                yield BDMIntro  # Could Check HTML later on.

                # print(Trial.filter(player=self.player))
                test_dict = {Trial.filter(player=self.player)[0].id: "D",
                             Trial.filter(player=self.player)[1].id: "D",
                             Trial.filter(player=self.player)[2].id: "A",
                             Trial.filter(player=self.player)[3].id: "C",
                             Trial.filter(player=self.player)[4].id: "A"}

                yield Submission(Stimuli, dict(raw_responses=json.dumps(test_dict)), check_html=False)

                # I have no clue how to make bot test JS of stimuli page
                # Solution - skip page if bot. Will revisit issue if I get time.

                yield BdmConc

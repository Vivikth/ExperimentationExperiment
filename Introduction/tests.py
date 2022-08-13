from . import *
from otree.api import Bot, SubmissionMustFail
from Global_Functions import global_cases, bot_should_play_app
import random
from datetime import date




class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, C.NAME_IN_URL):
            if self.case['Introduction'] == 'all_correct':
                yield SonaID, dict(sona_id=1000)
                yield InformationSheet, dict(agreement=True,
                                             name="Beep_Boop")
                yield Introduction, dict(Tried_Fancy_Pizza=1,
                                         Tried_Cheap_Pizza=1,
                                         Tried_Fancy_Taco=1,
                                         Tried_Cheap_Taco=1,
                                         payment_question=C.PAYMENT_AMOUNT)
            #
            # yield Introduction,  if self.case['Introduction'] == 'incorrect':
            #     random_payment = random.choice(list(range(0, 20)) + list(range(21, 40)))
            #     random_task = random.choice(["Tabulation", "Concealment",
            #                                  "Replication", "Organisation"])
            #     random_level = random.choice(list(range(0, 4)) + list(range(5, 40)))
            #     random_category = random.choice(list(range(0, 5)) + list(range(6, 40)))
            #     yield SubmissionMustFail(Introduction, dict(payment_question=random_payment,
            #                              visual_abilities=random_task,
            #                              num_levels=random_level,
            #                              num_categories=random_category))

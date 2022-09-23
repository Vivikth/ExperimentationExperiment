from . import *
from Global_Functions import global_cases, bot_should_play_app


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, C.NAME_IN_URL):
            if C.INSTRUCTIONS and self.player.round_number == 1:
                yield Instructions
            boxes_collected = 2
            yield (
                Game,
                dict(
                    bomb_row=1,
                    bomb_col=1,
                    boxes_collected=boxes_collected,
                    bomb=1 if self.case['bomb'] == 'always_bomb' else 0,
                ),
            )
            expected_round_result = (
                0 if self.case['bomb'] == 'always_bomb' else C.BOX_VALUE * boxes_collected
            )
            expect(self.player.round_result, expected_round_result)
            if C.RESULTS and self.player.round_number == C.NUM_ROUNDS:
                # 1 round is chosen randomly
                expect(self.participant.bret_payoff, expected_round_result)
                yield Results

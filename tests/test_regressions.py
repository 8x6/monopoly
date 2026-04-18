import unittest
import contextlib
import io
import random

import monopoly


class RegressionTests(unittest.TestCase):
    def test_take_turn_applies_rules_once(self):
        game = monopoly.Game()
        game.roll = lambda: 7  # GO -> Chance

        player = monopoly.Player()
        player.position = 0
        player.tell = lambda _roll: None

        draw_calls = 0
        original_draw = monopoly.CHANCE_DECK.draw

        def draw_tracker(_player):
            nonlocal draw_calls
            draw_calls += 1

        monopoly.CHANCE_DECK.draw = draw_tracker
        try:
            game.take_turn(player)
        finally:
            monopoly.CHANCE_DECK.draw = original_draw

        self.assertEqual(draw_calls, 1)

    def test_go_to_jail_does_not_pass_go(self):
        class PlayerSpy(monopoly.Player):
            def __init__(self):
                self.position = 30
                self.passed_go = False

            def pass_go(self):
                self.passed_go = True

        player = PlayerSpy()
        player.go_to_jail()

        self.assertEqual(player.position, 10)
        self.assertFalse(player.passed_go)

    def test_landing_on_go_to_jail_does_not_pass_go(self):
        class PlayerSpy(monopoly.Player):
            def __init__(self):
                self.position = 28
                self.passed_go = False

            def pass_go(self):
                self.passed_go = True

        player = PlayerSpy()
        player.advance(2)  # Lands on "Go To Jail" square at position 30.

        self.assertEqual(player.position, 10)
        self.assertFalse(player.passed_go)

    def test_chance_landing_frequency_regression_band(self):
        # Fixed-seed Monte Carlo guardrail. This catches major distribution
        # regressions (for example, accidentally applying rules twice per turn).
        original_state = random.getstate()
        original_chance_deck = monopoly.CHANCE_DECK
        original_community_deck = monopoly.COMMUNITY_CHEST_DECK
        try:
            random.seed(12345)
            monopoly.CHANCE_DECK = monopoly.ChanceDeck()
            monopoly.COMMUNITY_CHEST_DECK = monopoly.CommunityChestDeck()

            game = monopoly.Game()
            player = monopoly.Player()
            player.position = 0
            player.tell = lambda _roll: None

            turns = 100000
            counts = [0] * 40

            # Deck draws print card text; keep test output clean.
            with contextlib.redirect_stdout(io.StringIO()):
                for _ in range(turns):
                    game.take_turn(player)
                    counts[player.position] += 1

            chance_total = counts[7] + counts[22] + counts[36]
            chance_rate = chance_total / float(turns)

            # Tuned to be tolerant of normal simulation variance while still
            # catching large behavioral shifts.
            self.assertGreater(chance_rate, 0.022)
            self.assertLess(chance_rate, 0.033)
        finally:
            random.setstate(original_state)
            monopoly.CHANCE_DECK = original_chance_deck
            monopoly.COMMUNITY_CHEST_DECK = original_community_deck


if __name__ == "__main__":
    unittest.main()

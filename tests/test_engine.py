import unittest
from app.games.mooncake.engine import MooncakeEngine


class TestMooncakeEngine(unittest.TestCase):
    def setUp(self):
        self.game = MooncakeEngine()

    def test_initial_values(self):
        """Initial score is 0, cpc is 1, and cps is 0."""
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.total_produced, 0)
        self.assertEqual(self.game.cpc, 1)
        self.assertEqual(self.game.cps, 0)

    def test_click(self):
        """Click increments score and total_produced by cpc."""
        gain = self.game.click()
        self.assertEqual(gain, 1)
        self.assertEqual(self.game.score, 1)
        self.assertEqual(self.game.total_produced, 1)

    def test_buy_upgrade_failure_insufficient_score(self):
        """Cannot purchase upgrade without sufficient score."""
        mortar = self.game.upgrades["mortar"]
        self.game.score = mortar.cost - 1
        success, msg = self.game.buy_upgrade("mortar")
        self.assertFalse(success)
        self.assertEqual(mortar.count, 0)

    def test_buy_upgrade_success_and_scaling(self):
        """Purchasing deducts score, increments count, adjusts cpc, and scales cost."""
        mortar = self.game.upgrades["mortar"]
        initial_cost = mortar.cost
        self.game.score = initial_cost + 20

        success, msg = self.game.buy_upgrade("mortar")
        self.assertTrue(success)
        self.assertEqual(mortar.count, 1)
        self.assertEqual(self.game.score, 20)
        self.assertEqual(self.game.cpc, 2)
        self.assertGreater(mortar.cost, initial_cost)
        self.assertIsInstance(mortar.cost, int)

    def test_passive_tick(self):
        """Passive production generates mooncakes every second."""
        oven = self.game.upgrades["oven"]
        initial_cost = oven.cost
        self.game.score = initial_cost
        self.game.total_produced = initial_cost
        self.game.buy_upgrade("oven")
        self.assertEqual(self.game.cps, 1)

        earned = self.game.tick(2.0)
        self.assertEqual(earned, 2)
        self.assertEqual(self.game.score, 2)
        self.assertEqual(self.game.total_produced, initial_cost + 2)

    def test_achievements_unlock(self):
        """Achievements unlock when cumulative production reaches threshold."""
        for _ in range(10):
            self.game.click()
        self.assertTrue(self.game.achievements["first_batch"]["unlocked"])
        self.assertFalse(self.game.achievements["feast"]["unlocked"])

    def test_reset(self):
        """Reset clears score, total, counts, and achievements."""
        self.game.click()
        self.game.reset()
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.total_produced, 0)
        self.assertEqual(self.game.cpc, 1)
        self.assertEqual(self.game.cps, 0)


if __name__ == "__main__":
    unittest.main()

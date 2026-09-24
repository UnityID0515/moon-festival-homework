import unittest
from app.games.bbq.engine import BBQEngine, Skewer


class TestBBQEngine(unittest.TestCase):
    def setUp(self):
        self.engine = BBQEngine()

    def test_initial_state(self):
        """Grill starts with 3 empty slots and 0 score."""
        self.assertEqual(len(self.engine.slots), 3)
        self.assertTrue(all(slot is None for slot in self.engine.slots))
        self.assertEqual(self.engine.score, 0)
        self.assertEqual(self.engine.served_count, 0)

    def test_place_food(self):
        """Placing food fills slot with initial 0% progress."""
        success, msg = self.engine.place_food(slot_idx=0, food_id="beef")
        self.assertTrue(success)
        slot = self.engine.slots[0]
        self.assertIsNotNone(slot)
        self.assertEqual(slot.food_id, "beef")
        self.assertEqual(slot.side_a, 0.0)
        self.assertEqual(slot.side_b, 0.0)
        self.assertFalse(slot.is_flipped)
        self.assertFalse(slot.sauce_brushed)

    def test_tick_advances_doneness(self):
        """Tick should only advance the side currently facing the fire."""
        self.engine.place_food(slot_idx=0, food_id="beef")  # speed = 10% / s
        self.engine.tick(2.0)  # 2 seconds -> +20%

        slot = self.engine.slots[0]
        self.assertAlmostEqual(slot.side_a, 20.0, places=1)
        self.assertEqual(slot.side_b, 0.0)

    def test_flip_skewer(self):
        """Flipping switches the active cooking side."""
        self.engine.place_food(slot_idx=0, food_id="beef")
        self.engine.tick(2.0)  # side_a = 20%
        
        success, msg = self.engine.flip(slot_idx=0)
        self.assertTrue(success)
        self.assertTrue(self.engine.slots[0].is_flipped)

        self.engine.tick(3.0)  # side_b = 30%
        slot = self.engine.slots[0]
        self.assertAlmostEqual(slot.side_a, 20.0, places=1)
        self.assertAlmostEqual(slot.side_b, 30.0, places=1)

    def test_brush_sauce(self):
        """Brushing sauce sets flag and only applies once."""
        self.engine.place_food(slot_idx=0, food_id="beef")
        success, msg = self.engine.brush_sauce(slot_idx=0)
        self.assertTrue(success)
        self.assertTrue(self.engine.slots[0].sauce_brushed)

        # Second attempt
        success2, msg2 = self.engine.brush_sauce(slot_idx=0)
        self.assertFalse(success2)

    def test_serve_raw(self):
        """Serving undercooked food awards 0 points."""
        self.engine.place_food(slot_idx=0, food_id="beef")
        self.engine.slots[0].side_a = 40.0
        self.engine.slots[0].side_b = 20.0

        result = self.engine.serve(slot_idx=0)
        self.assertEqual(result["status"], "raw")
        self.assertEqual(result["points"], 0)
        self.assertEqual(self.engine.score, 0)
        self.assertIsNone(self.engine.slots[0])

    def test_serve_perfect(self):
        """Serving evenly cooked food with sauce awards 1.5x base score."""
        self.engine.place_food(slot_idx=0, food_id="beef")  # base = 100
        self.engine.slots[0].side_a = 80.0
        self.engine.slots[0].side_b = 85.0
        self.engine.slots[0].sauce_brushed = True

        result = self.engine.serve(slot_idx=0)
        self.assertEqual(result["status"], "perfect")
        self.assertEqual(result["points"], 150)  # 100 * 1.5
        self.assertEqual(self.engine.score, 150)
        self.assertEqual(self.engine.served_count, 1)
        self.assertIsNone(self.engine.slots[0])

    def test_serve_burnt(self):
        """Serving burnt food awards only 10 consolation points."""
        self.engine.place_food(slot_idx=0, food_id="beef")
        self.engine.slots[0].side_a = 105.0
        self.engine.slots[0].side_b = 70.0

        result = self.engine.serve(slot_idx=0)
        self.assertEqual(result["status"], "burnt")
        self.assertEqual(result["points"], 10)
        self.assertEqual(self.engine.score, 10)

    def test_reset(self):
        """Reset clears all slots and scores."""
        self.engine.place_food(0, "beef")
        self.engine.score = 500
        self.engine.served_count = 5
        self.engine.reset()

        self.assertEqual(self.engine.score, 0)
        self.assertEqual(self.engine.served_count, 0)
        self.assertTrue(all(slot is None for slot in self.engine.slots))


if __name__ == "__main__":
    unittest.main()

import unittest
from fastapi.testclient import TestClient
from main import app


class TestBBQAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_bbq_page(self):
        """GET /games/bbq should return 200 OK and render BBQ grill."""
        response = self.client.get("/games/bbq")
        self.assertEqual(response.status_code, 200)
        self.assertIn("露天烤肉模擬器", response.text)
        self.assertIn("烤網工位", response.text)

    def test_place_and_tick(self):
        """Placing food and ticking should update grill state."""
        init_res = self.client.get("/games/bbq")
        cookies = init_res.cookies

        # Place beef on slot 0
        place_res = self.client.post("/games/bbq/place/0/beef", cookies=cookies)
        self.assertEqual(place_res.status_code, 200)
        self.assertIn("鮮嫩牛肉串", place_res.text)

        # Tick 1 second
        tick_res = self.client.post("/games/bbq/tick", cookies=cookies)
        self.assertEqual(tick_res.status_code, 200)

    def test_flip_and_sauce(self):
        """Flip and sauce endpoints should update the skewer."""
        init_res = self.client.get("/games/bbq")
        cookies = init_res.cookies

        self.client.post("/games/bbq/place/1/tempura", cookies=cookies)
        flip_res = self.client.post("/games/bbq/flip/1", cookies=cookies)
        self.assertEqual(flip_res.status_code, 200)

        sauce_res = self.client.post("/games/bbq/sauce/1", cookies=cookies)
        self.assertEqual(sauce_res.status_code, 200)
        self.assertIn("已刷醬", sauce_res.text)

    def test_serve(self):
        """Serve endpoint removes food and outputs message."""
        init_res = self.client.get("/games/bbq")
        cookies = init_res.cookies

        self.client.post("/games/bbq/place/2/sausage", cookies=cookies)
        serve_res = self.client.post("/games/bbq/serve/2", cookies=cookies)
        self.assertEqual(serve_res.status_code, 200)
        self.assertIn("空置", serve_res.text)


if __name__ == "__main__":
    unittest.main()

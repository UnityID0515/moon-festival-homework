import unittest
from fastapi.testclient import TestClient
from main import app


class TestMooncakeAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_hub_homepage(self):
        """GET / should render the game hub with 200 OK."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("中秋小遊戲樂園", response.text)
        self.assertIn("月餅點點樂", response.text)

    def test_mooncake_game_page(self):
        """GET /games/mooncake should render the game SPA."""
        response = self.client.get("/games/mooncake")
        self.assertEqual(response.status_code, 200)
        self.assertIn("月餅點點樂", response.text)
        self.assertIn("玉兔搗藥杵", response.text)

    def test_click_endpoint(self):
        """POST /games/mooncake/click should increment score."""
        # First visit to get cookie
        init_res = self.client.get("/games/mooncake")
        cookie = init_res.cookies.get("session_id")

        click_res = self.client.post("/games/mooncake/click", cookies={"session_id": cookie} if cookie else {})
        self.assertEqual(click_res.status_code, 200)
        # Check that response contains updated score (1)
        self.assertIn("1", click_res.text)

    def test_buy_upgrade_endpoint(self):
        """POST /games/mooncake/buy/{item_id} should deduct score and increase item count."""
        init_res = self.client.get("/games/mooncake")
        cookies = init_res.cookies

        # Click 15 times to afford mortar
        for _ in range(15):
            self.client.post("/games/mooncake/click", cookies=cookies)

        buy_res = self.client.post("/games/mooncake/buy/mortar", cookies=cookies)
        self.assertEqual(buy_res.status_code, 200)
        self.assertIn("已擁有: 1", buy_res.text)

    def test_reset_endpoint(self):
        """POST /games/mooncake/reset should reset game."""
        init_res = self.client.get("/games/mooncake")
        cookies = init_res.cookies

        self.client.post("/games/mooncake/click", cookies=cookies)
        reset_res = self.client.post("/games/mooncake/reset", cookies=cookies)
        self.assertEqual(reset_res.status_code, 200)
        self.assertIn("累計總產量", reset_res.text)
        self.assertIn(">0</span>", reset_res.text)


if __name__ == "__main__":
    unittest.main()

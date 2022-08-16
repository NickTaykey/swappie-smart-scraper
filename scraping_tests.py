from scrapers import fetch_swappie_iPhones_data, fetch_latest_iPhone_price
import unittest


class ScrapingTests(unittest.TestCase):
    def test_swappie_scraper(self):
        self.assertIsInstance(
            fetch_swappie_iPhones_data("12-pro-max", testing=True), tuple
        )
        self.assertIsInstance(
            fetch_swappie_iPhones_data("se-2020", testing=True), tuple
        )
        self.assertIsInstance(
            fetch_swappie_iPhones_data("x", testing=True), tuple
        )
        self.assertIsNone(
            fetch_swappie_iPhones_data("invalid model name", testing=True)
        )

    def test_apple_scraper(self):
        self.assertIsInstance(
            fetch_latest_iPhone_price("13-pro-max", testing=True), int
        )
        self.assertIsInstance(
            fetch_latest_iPhone_price("12", testing=True), int
        )
        self.assertIsInstance(
            fetch_latest_iPhone_price("13-mini", testing=True), int
        )
        self.assertIsInstance(
            fetch_latest_iPhone_price("se", testing=True), int
        )
        self.assertIsNone(fetch_latest_iPhone_price("6s", testing=True))


if __name__ == "__main__":
    unittest.main()

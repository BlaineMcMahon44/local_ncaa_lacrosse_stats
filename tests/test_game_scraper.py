import unittest
from src.ncaa_lacrosse_statistics.drivers import GameScraper, global_games

class TestGameScraper(unittest.TestCase):

    def test_all_years(self):
        for year in ['2018', '2019', '2020', '2021', '2022', '2023', '2024']:
            game_scraper = GameScraper(year, False)
            game_scraper.run(3)
            self.assertEqual(game_scraper.scraped_data, global_games)
            self.assertIn('harvard', game_scraper.scraped_data)
            self.assertIn(year, game_scraper.scraped_data)

    def test_one_year(self, year):
            game_scraper = GameScraper(year, False)
            game_scraper.run(3)
            self.assertEqual(game_scraper.scraped_data, global_games)
            self.assertIn('harvard', game_scraper.scraped_data)
            self.assertIn(year, game_scraper.scraped_data)       

if __name__ ==  "__main__":
    unittest.main()
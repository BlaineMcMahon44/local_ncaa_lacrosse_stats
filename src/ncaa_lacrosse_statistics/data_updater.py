from .data_operations import ProcessGameData, ProcessScheduleData
from .drivers import GameScraper, global_games
import datetime
import pandas as pd
import shutil
import os 
from .logger import MyLogger  # Assuming logger.py contains the Logger class

logger = MyLogger(__name__)

class GamesUpdater(object):
    games_location  = 'data/csv/Updated_Games' 
    teams_location = "data/csv/Teams"
    schedule_location = "data/csv/Schedule"
    year = datetime.datetime.now().strftime("%Y")
    
    def __init__(self):
        self.scraper = GameScraper(self.year, False)
        self.current_game_data = pd.read_csv(self.games_location, index_col = 0)
        self.game_headers = []

    def get_games(self):
        """
        Run the game scraper for the current thread
        """
        self.scraper.run(4)
        self.game_headers.append(self.scraper.headers)

    def process_data(self):
        """
        Process the data returned from the game scraper for the current year 
        """
        self.data_processor = ProcessGameData(global_games, self.game_headers, "game_data_2024")
        self.data_processor.process_data()

        self.schedule = ProcessScheduleData(global_games, self.game_headers, "schedule")
        self.schedule.process_data()
        
    def combine_data(self):
        """
        Combine the data returned from the game scraper for the current year with the current games data frame and rewrite the files 
        """
        try:
            output_file_path = self.data_processor.combine_game_data(self.current_game_data, self.data_processor.df)
        except Exception as e:
            logger.error(f"Error in combining game data {e}")
            shutil.copy("data/csv/Updated_Games_backup", self.games_location)
            raise e

        update_game_path = os.path.join(os.getcwd(), "data/csv/Updated_Games")        
        shutil.copy(output_file_path, update_game_path)
        shutil.copy(update_game_path, "data/csv/Updated_Games_backup")
    
    def update_schedule(self):
        logger.info(self.schedule.output_file_path)
        shutil.copy(self.schedule.output_file_path, self.schedule_location)

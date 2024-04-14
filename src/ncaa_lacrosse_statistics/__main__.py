from .data_operations import ProcessGameData, ProcessTeamData
from .drivers import TeamScraper, GameScraper, global_games
from .data_updater import GamesUpdater
from .data_base import DataBase
import shutil 
import pandas as pd 
import json
import time
import datetime
import os
def get_all_data():
    years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    start = time.time()

    teams = []
    teams_headers = []
    game_headers = []

    for year in years:
        team_scraper = TeamScraper(year, False)
        team_scraper.run()
        
        teams.append(team_scraper.scraped_data)
        if not teams_headers:
            teams_headers.append(team_scraper.headers)
        
    team_data = ProcessTeamData(teams, teams_headers, "team_data_2018-2024")
    team_data.process_data()

    for year in years:
        game_scraper = GameScraper(year, False)
        game_scraper.run(3)
        
        if not game_headers:
            game_headers.append(game_scraper.headers)       

    game_data = ProcessGameData(global_games, game_headers, "game_data_2018-2024")
    
    game_data.process_data()
    end = time.time()
    print(end - start)

def main():
    # Find most recent games and update the games table 

    updater = GamesUpdater()
    updater.get_games()
    updater.process_data()
    updater.combine_data()
    updater.update_schedule()
    # Save results to database
    db = DataBase("Games", "Teams")
    db.convert_df_sql()

    '''    
    years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    start = time.time()

    teams = []
    teams_headers = []

    for year in years:
        team_scraper = TeamScraper(year, False)
        team_scraper.run()
        
        teams.append(team_scraper.scraped_data)
        if not teams_headers:
            teams_headers.append(team_scraper.headers)
        
    team_data = ProcessTeamData(teams, teams_headers, "team_data_2018-2024")
    team_data.process_data()
    '''
if __name__ == "__main__":
    main()

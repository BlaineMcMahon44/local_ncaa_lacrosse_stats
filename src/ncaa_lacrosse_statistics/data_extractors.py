from .drivers import TeamScraper
from .drivers import GameScraper, global_games
import multiprocessing
from .logger import MyLogger  # Assuming logger.py contains the Logger class

logger = MyLogger(__name__)

class Scraper:
    def __init__(self, year:str, is_game:bool = False)-> None:
        self.year = year
        self.is_game = is_game
        self.scraper = GameScraper(self.year, False) if is_game else TeamScraper(self.year, False)       

    def scrape_data(self)-> list:
        """
        Calls the corresponding methdods to scrape data for a teams or games depending on is_game

        Returns:
            scraper.scraped_data: List of scrape data (rows for dataframe)
            scraper.headers: List of headers (columns for dataframe)
        """
        try:
            if self.is_game:
                self.scraper.run(self.year, 2)
            else:
                self.scraper.pull_up_rankings(self.year)
                self.scraper.extract_teams() 

            return self.scraper.scraped_data, self.scraper.headers
        
        except Exception as e:
            logger.error(f"Error occurred while scraping data from {self.year}: {e}")
            return None, None

        finally:
            self.scraper.close()        

class Extractor(object):
    def __init__(self, years:list)-> None:
        self.years = years 
        self.teams = multiprocessing.Manager().list()
        self.team_headers = multiprocessing.Manager().list()
        self.games = multiprocessing.Manager().list()
        self.game_headers = multiprocessing.Manager().list()

    def _update_data_lists(self, teams: list, headers: list, games: bool = None)-> None:
        """
        Depending on is_game, append the corresponding teams and headers to the appropriate lists.

        Args:
            teams (list): list of teams data
            headers (list): list of headers corresponding to teams data
            games (bool, optional): Boolean value to indicate which list to append. Defaults to None.
        """
        if not games:
            if not self.team_headers:
                self.team_headers.append(headers)
            self.teams.append(teams)
        elif games:
            if not self.game_headers:
                self.game_headers.append(headers)
            self.games.append(teams)

    def _scrape_data(self, year: str, is_game:bool = False)-> None:
        """
        Creates a Scraper object and calls the _scrape_data method for each year using multiprocessing.Process

        Args:
            year (str): string of the year to be scraped.
            is_game (bool, optional): Boolean used to check whether grames or teams are being scraped. Defaults to False.
        """
        scraper = Scraper(year, is_game)
        data, headers = scraper.scrape_data()
        if data and headers:
            self._update_data_lists(data, headers, games=is_game)

    def _create_extractors(self, years, games=False)-> None:
        """
        For a list of years, calls the _scrape_data method for each year using multiprocessing.Process
        and launches each process to run in parallel.
        It then waits for each process to finish and then returns the results.

        Args:
            years (_type_): The list of years to be extracted.
            games (bool, optional): Games are set to True if they are to be extracted. Defaults to False.
        """
        processes = []
        try:
            for year in years:
                process = multiprocessing.Process(target=self._scrape_data, args=(year, games))
                processes.append(process)
                process.start()

            for process in processes:
                process.join()
        
        except Exception as e:
            logger.error(f"Exception occured in multiprocessing {e}")
            
    # Cannot launch all processes at once due to being blocked by router so need to break proccesses up into groups of 2
    def break_up_extractors(self, chunk_size:int, games:bool = False)-> None:
        """
        Breaks up years into chunks depending on chunk_size.
        Calls the _create_extractors method on each chunk 

        Args:
            chunk_size (int): number of years to be extracted in each chunk.
            games (bool, optional): If games are to be extracted instead of Teams. Defaults to False.
        """
        for i in range(0, len(self.years), chunk_size):
            if i + chunk_size <= len(self.years):
                # Print or process the current chunk
                self._create_extractors(self.years[i:i + chunk_size], games=games)
            else:
                # Handle the last chunk with fewer elements
                self._create_extractors(self.years[i:], games=games)

if __name__ == "__main__":
    years = ['2018', '2019', '2020', '2021','2022', '2023']
    #games_extractor = Extractor(years)
    #games_extractor.break_up_extractors(2, games=True)


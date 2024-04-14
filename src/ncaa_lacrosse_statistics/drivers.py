from weakref import proxy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
import datetime
import time
import multiprocessing
import random
from .logger import MyLogger  # Assuming logger.py contains the Logger class
import pandas as pd
import concurrent.futures
import threading

# Create a logger instance
logger = MyLogger(__name__)

global_games = []

class ChromeDriver(object):
    def __init__(self, headless: bool = False, exec_path: str = "/usr/local/bin/chromedriver", proxy:bool = False)-> None:
        self.chrome_options = ChromeOptions()
        self.exec_path = exec_path

        if proxy:
            proxy = "http://b8f164b26e3317bb0b214c26f6ce8abe7867c81c:premium_proxy=true&device=desktop&session_id=12345@proxy.zenrows.com:8001"
            proxies = {"http": proxy, "https": proxy}
            self.proxy = proxies["https"]
            self.chrome_options.add_argument(f'--proxy-server={self.proxy}')

        if headless:
            self.chrome_options.add_argument("--headless")

        self.user_agent_lists = [ 
            'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) GSA/7.0.55539 Mobile/11D257 Safari/9537.53'
            'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F69'
            #'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
            #'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4',
            #'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
            #'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
            #'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4',
            #'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53'
            ]
        service = ChromeService(executable_path=self.exec_path)
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        self.driver.implicitly_wait(10)
        self.user_agent = random.choice(self.user_agent_lists)
        self.chrome_options.add_argument(f'user-agent={self.user_agent}')
        
        self.lacrosse_url = "https://stats.ncaa.org/rankings/institution_trends"

    def load_page(self, url:str, max_retries:int = 3)-> None:
        """
        Loads the given url into the browser and blocks until the page is loaded.
        If the page is not loaded within the given number of retries, an exception is raised.
        """
        retry_count = 0
        while retry_count < max_retries:
            try:
                logger.info(f"Loading page: {url}")
                self.driver.get(url)     
                time.sleep(3)
                logger.info("Page loaded successfully")
                return
            except TimeoutException as e:
                logger.error(f"TimeoutException: {e}")
                time.sleep(120)
                retry_count += 1
            except WebDriverException as e:
                logger.error(f"TimeoutException: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected Exception: {e}")
                raise 

    def close(self)-> None:
        """
        Closes the browser.
        """
        try:
            self.driver.quit()
        except Exception as e:
            logger.error(f"Error while closing WebDriver: {e}")
    
    def pull_up_rankings(self, year:str)-> None:
        """Pulls up the rankings for the given year.

        Args:
            year (str): Given the year to pull up the rankings for.

        Raises:
            f: NoSuchElementException: If the element is not found.
            f: WebDriverException: If another WebDriver-related exceptions occur.
        """ 
        
        self.load_page(self.lacrosse_url)       
        # Block to deal with first screen dropdown menus that filter by sport and division
        try:
            self.driver.find_element(By.ID, "sport").click()
            dropdown = self.driver.find_element(By.ID, "sport")
            dropdown.find_element(By.XPATH, ".//option[@value='MLA']").click()
            time.sleep(4)
            self.driver.find_element(By.ID, "u_div").click()
            dropdown = self.driver.find_element(By.ID, "u_div")
            dropdown.find_element(By.XPATH, "//option[. = 'I']").click()
            time.sleep(4)
            dropdown = self.driver.find_element(By.ID, "acadyr")
            dropdown.find_element(By.XPATH, f"//option[@value={year}.0]").click()
            time.sleep(4)
            self.driver.find_element(By.ID, "trends").click()
            time.sleep(4)
            self.driver.find_element(By.LINK_TEXT, "Institution").click()

        except NoSuchElementException as e:
            raise f"Element not found {e}"
        except WebDriverException as e:
            # Exception handling for other WebDriver-related exceptions
            raise f"Other exception has occured {e}"

class TeamScraper(ChromeDriver):
    def __init__(self, year:str, headless:bool = False)-> None:
        super().__init__(headless=headless, proxy=True) # Call the constructor of the parent class
        self.year = year
        self.header_check = ['Institution', 'Conference', 'G', 'Goals', 'Assists', 'Points', 'Shots', 'SOG', 'Man-Up G', 'Man-Down G', 'GB', 'TO', 'CT', 'FO Won', 'FOs Taken', 'Pen', 'Pen Time', 'G Min', 'Goals Allowed', 'Saves', 'RC', 'YC', 'Clears', 'Att', 'Clear Pct', 'OTG', 'Year'] 
        self.headers = []
        self.scraped_data = []

    def extract_teams(self)-> None:
        """
        Extracts the teams from the given year
        
        Args:
            None

        Raises:
            f: NoSuchElementException: If the element is not found.
            f: Exception: If another exceptions occur.
        """ 
        # Find the html table that contains all teams
        try:
            table = self.driver.find_element(By.XPATH, "//*[@id='stat_grid']/thead")
        except NoSuchElementException as e:
            logger.error(f"Error in finding teams table {e}")
            table = self.driver.find_element(By.ID, "stat_grid")
        try:
            logger.info(table)
            # Find find all of the heading element which is <tr> tag of table
            rows = table.find_elements(By.XPATH, ".//tr")
            # Find Iterate through the first row to retrieve headers which is <th> tag of rows
            heading_names = rows[0].find_elements(By.XPATH, ".//th")
        except NoSuchElementException as e:
            raise f"Error in finding headers of teams table {e}"
        self.check_headers(heading_names)
        try:
            rows = self.driver.find_elements(By.XPATH,"//*[@id='stat_grid']/tbody/tr")
            teams_table = []
            for row in rows:
                cells = row.find_elements(By.XPATH, ".//td") # Once cells are found loop through each cell and retrieve the text
                text_in_cells = [cell.text for cell in cells]
                text_in_cells.append(self.year)
                teams_table.append(text_in_cells)
            self.scraped_data = teams_table       
        except NoSuchElementException as e:
            raise f"Error finding text in teams table cells {e}"
        except Exception as e:
            raise f"Error in trying to extract teams data {e}"

    # Need to verify that the headers retrieved are as expected
    def check_headers(self, heading_names: list)-> None:
            """
            Verifies that the headers are as expected

            Args:
                heading_names (list): list of expected headers to check against
            """
            headers = [heading.text for heading in heading_names]
            headers.append('Year')           
            assert headers == self.header_check, f"headers do not match {headers} and {self.header_check}"     
            logger.info(f"Headers are: {headers}")   
            self.headers = headers     
    
    def run(self):
        self.pull_up_rankings(self.year)
        self.extract_teams()


class GameScraper(ChromeDriver):
    def __init__(self, year:str, headless:bool = False)-> None:
        super().__init__(headless=headless, proxy=True) # Call the constructor of the parent class
        self.year = year
        self.header_url = "http://stats.ncaa.org/player/game_by_game?game_sport_year_ctl_id=16320&org_id=518&stats_player_seq=-100"
        self.main_url = "http://stats.ncaa.org/rankings/institution_trends"
        self.header_check = ['Date', 'Institution', 'Opponent', 'Result', 'G', 'Goals', 'Assists', 'Points', 'Shots', 'SOG', 'Man-Up G', 'Man-Down G', 'GB', 'TO', 'CT', 'FO Won', 'FOs Taken', 'Pen', 'Pen Time', 'G Min', 'Goals Allowed', 'Saves', 'W', 'L', 'T', 'RC', 'YC', 'Clears', 'Att', 'Clear Pct', 'OTG', 'Opp_G', 'Opp_Goals', 'Opp_Assists', 'Opp_Points', 'Opp_Shots', 'Opp_SOG', 'Opp_Man-Up G', 'Opp_Man-Down G', 'Opp_GB', 'Opp_TO', 'Opp_CT', 'Opp_FO Won', 'Opp_FOs Taken', 'Opp_Pen', 'Opp_Pen Time', 'Opp_G Min', 'Opp_Goals Allowed', 'Opp_Saves', 'Opp_W', 'Opp_L', 'Opp_T', 'Opp_RC', 'Opp_YC', 'Opp_Clears', 'Opp_Att', 'Opp_Clear Pct', 'Opp_OTG', 'Year'] 
        self.headers = []
        self.link_tuples = []
        self.stats = []

    def get_headers(self)-> None:
        """
        Pulls up a sample team page to load the headers from the header url

        Raises:
            NoSuchElementException: If the element is not found.
        """
        self.load_page(self.header_url)
        try:
            # Since there is 31 headers loop through each header element to get the text
            for i in range(1,31):
                header = self.driver.find_element(By.XPATH, f"/html/body/div[2]/div[3]/table/tbody/tr/td/table/tbody/tr[2]/th[{i}]") # This is the exact xpath
                self.headers.append(header.text)
        except NoSuchElementException as e:
            logger.error(f"Error no element found for /html/body/div[2]/div[3]/table/tbody/tr/td/table/tbody/tr[2]/th[{i}]")
            raise e

        for header in self.headers[3:]: # Adding opponent headers section for defensive stats which start after result header (3)
            self.headers.append(f"Opp_{header}")

        # Want to include the Team Name as well as Year to each entry to we can map this to our teams table eventually
        self.headers.insert(1, 'Institution') 
        self.headers.append('Year')
        
        # Ensure the headers have not changed from static check values
        self.check_headers()

    def check_headers(self)-> None:
        """
        Checks that the headers have not changed from static check values
        """
        assert self.header_check == self.headers, f"Headers do not match {self.headers} and {self.header_check}"

    def find_team_links(self)-> None:
        """
        Find all of the links to the teams on the main page and store them in a list

        Raises:
            NoSuchElementException: If the element is not found.
            Exception: If another exceptions occur.
        """
        try:
            all_link_tags = self.driver.find_elements(By.TAG_NAME, "a") # Find all link tags on page
            target_links = [link for link in all_link_tags if link.get_attribute("target") == "TEAM_WIN" and "/team/" in link.get_attribute("href")] # Filter link tags for only the institution links
        except NoSuchElementException as e:
            logger.error(f"Error cannot find link tags {e}")
            raise e
        try:
            for link in target_links:
                href = link.get_attribute("href") # Need the link to the specific institution page
                text = link.text # Need the text for the teams name 
                tup = tuple([href,text]) # Create a tuple with link and team name 
                self.link_tuples.append(tup)
        except Exception as e:
            logger.error(f"Error in getting text or href from link {e}")
            raise e
    def get_teams_stats(self, links: list)-> None:
        """
        Load each teams games results page and
        Retrieve the games table for each team and call get game_by_game_data for each team

        Raises:
            Exception: If another exceptions occur.
        """
        chrome_driver = ChromeDriver(proxy = True)
        if links:    
            for link in links: # Link to teams pages are [0] and team name is [1]
                team = (link[1])                
                try: 
                    chrome_driver.load_page(link[0]) # Load specific teams page
                except Exception as e:
                    logger.error(f"Error in loading team page {e}")
                
                try:
                    game_by_game_link = chrome_driver.driver.find_element(By.XPATH, "//a[contains(text(),'Game By Game')]")
                except NoSuchElementException as e:
                    # Since the game by game link is hidden in html find all links on the page 
                    game_by_game_link = chrome_driver.driver.find_element(By.XPATH, "//a[contains(.,'Game By Game')]")
                
                chrome_driver.load_page(game_by_game_link.get_attribute("href"))

                try:
                    self.get_game_by_game_data(team, chrome_driver)
                except Exception as e:
                    logger.error(f"Error in getting game by game data for team {team}")
                    raise e
            
    def get_game_by_game_data(self, team: str, chrome_driver: ChromeDriver)-> None:
        """
        Retrieve the offensive and defensive stats from each game and add raw data to scraped_data

        Args:
            team (str): The current team name

        Raises:
            NoSuchElementException: If the element is not found.
            Exception: If another exceptions occur.
        """
        stats = []
        max_retries = 3
        retry_delay = 2
        for _ in range(max_retries):        
            try:
                games_table = chrome_driver.driver.find_element(By.XPATH,"//*[@id='game_breakdown_div']/table/tbody/tr/td/table")
                #games_table = self.driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/table/tbody/tr/td/table/tbody")
                break
            except NoSuchElementException as e:
                chrome_driver.driver.refresh()
                logger.info(f"Error in finding games table {e} for team {team}")
                time.sleep(retry_delay)
        else:
            logger.error("Element not found after multiple attempts")
            raise NoSuchElementException("Element not found after multiple attempts")

        try:
            stats = self.get_offensive_stats(games_table)
        except Exception as e:
            logger.error(f"Exception in getting offensive stats {e}")
            raise e
        try:
            stats = self.get_defensive_stats(stats)
        except Exception as e:
            logger.error(f"Exception in getting defensive stats {e}")
            raise e

        for row in stats: # Add team name and year data for each game 
            row.insert(1, team)
            row.append(self.year)

        global_games.append(stats)
 
    def get_offensive_stats(self, games_table)-> list:
        """
        Retrieve the offensive stats from the games table

        Args:
            games_table (str): The games table which contains the offensive stats

        Raises:
            NoSuchElementException: If the element is not found.
            Exception: If another exceptions occur.

        Returns:
            list: Returns a list of offensive stats
        """
        tmp_table = []
        
        try:
            rows = games_table.find_elements(By.XPATH, ".//tr") # Retrieve the rows of table
        except NoSuchElementException as e:
            logger.error(f"Error in finding the rows of games table {games_table}")
            raise e
        
        for row in rows[2:]: # Skip the first two rows of data
            row_x = []
            try:
                cells = row.find_elements(By.XPATH,".//td") # Find the cell elements in the row
            except NoSuchElementException as e:
                logger.error(f"Error in finding the rows of games table {games_table}")
                raise e
            
            try:
                for cell in cells:
                    if cell.text != "":
                        row_x.append(cell.text.strip()) 
                    else:
                        if cell.get_attribute('textContent') != "\n":
                            row_x.append(cell.get_attribute('textContent').strip())
            except Exception as e:
                logger.error(f"Error in getting cell text attributes {e}")
            tmp_table.append(row_x)  
        
        return tmp_table

    def get_defensive_stats(self, stats: list)-> None:
        """
        Retrieve the defensive stats from the games table and adds the offensive and defensive stats to scraped_data

        Raises:
            NoSuchElementException: If the element is not found.
            Exception: If another exceptions occur.

        Returns:
            list: Returns a list of defensive stats
        """
        try:
            new_data = stats
            
            for i, row in enumerate(new_data):
                if 'Defensive Totals' in row:
                    new_data[i-1].extend(row[3:])
                    new_data.pop(i)

            stats = new_data

            first_row_len = len(stats[0][1])

            # loop over each row
            for row in stats:
                # check if length of row is less than first row length
                if len(row) < first_row_len:
                    # append blank values to make it match first row length
                    row.extend([''] * (first_row_len - len(row)))
            return stats
        except Exception as e:
            logger.error(f"Error in retrieving defensive stats for {stats}")

    def run(self, num_threads:int)->None:
        """
        Run the scraper for the given year, will launch threads for extracting team data 

        Args:
            year (str): The given year to extract team data for
            num_threads (int): The number of threads to launch for the given year 
        """
        self.get_headers()
        self.pull_up_rankings(self.year)
        self.find_team_links()

        chunk_size = int(len(self.link_tuples) / num_threads)
        start = 0 
        threads = []

        while start < len(self.link_tuples):
            end = min(start + chunk_size, len(self.link_tuples))  # Calculate the end index of the sublist
            thread = threading.Thread(target=self.get_teams_stats, args=(self.link_tuples[start:end],))
            threads.append(thread)
            thread.start()
            start = end  # Update the start index for the next iteration

        for thread in threads:
            thread.join()              

def test_proxy(i):
    print(f"Launching Target {i}")
    driver = ChromeDriver(proxy=True)
    driver.load_page("https://stats.ncaa.org/rankings/conference_trends")
    driver.close()
    print(f"Closing Target {i}")

def test_games():
    # GAMES TEST
    years = ['2019']
    
    dfs= []

    for year in years:
        scraper = GameScraper(year, headless=False)
        scraper.run(year, 6)
        logger.info(global_games)
        for team in global_games:
            dfs.append(pd.DataFrame(team, columns=scraper.headers))

    #dfs = [pd.DataFrame(team, columns=scraper.headers) for team in scraper.scraped_data ]
    result = pd.concat(dfs,ignore_index=True)

    result.to_csv('game_data_2019.csv')
    scraper.close()

def test_teams():
    # TEAM TEST
    year = 2019
    scraper = TeamScraper(year, False)
    try:
        scraper.pull_up_rankings(year)
        scraper.extract_teams()
    finally:
        scraper.close()
        
    logger.info(scraper.scraped_data)


if __name__ == "__main__":
    test_games()
    '''
    driver = ChromeDriver(proxy=True)
    time.sleep(10)
    driver.load_page("https://stats.ncaa.org/rankings/conference_trends")
    time.sleep(10)
    driver.close()
    processes = []

    for i in range(0,5):
        process = multiprocessing.Process(target=test_proxy, args=(int(i),))
        processes.append(process)
        process.start()
        
    # Wait for all processes to finish
    for process in processes:
        process.join()
    '''



from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from jose import jwt
from pydantic import BaseModel
from typing import Annotated
from typing import Optional
import pandas as pd
import io
import re
from datetime import datetime
from typing import Optional

current_year = datetime.now()
current_year = current_year.year

games_location  = "data/csv/Updated_Games"
teams_location = "data/csv/Teams"
schedule_location = "data/csv/Schedule"

games = pd.read_csv(games_location, index_col=0)
teams = pd.read_csv(teams_location, index_col=0)
schedule = pd.read_csv(schedule_location, index_col=0)
results = games.loc[games['Year'] == 2024]

games = games.reset_index(drop = True)
teams = teams.reset_index(drop = True)
schedule = schedule.reset_index(drop = True)
results = results.reset_index(drop = True)

games_dict = games.to_dict(orient='records')
teams_dict = teams.to_dict(orient='records')
schedule_dict = schedule.to_dict(orient='records')

app = FastAPI()

# Allow requests from your React app
origins = [
    "http://localhost",
    "http://localhost:3001",  # Assuming your React app runs on port 3000 during development
]

# Allow requests from all origins with the appropriate methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class Team(BaseModel):
    Id: int
    Team_Name: str
    Conference: str
    Games: int
    Goals: int
    Assists: int
    Points: int
    Shots: int
    SOG: int
    Man_Up_G: int
    GB: int
    TO: int
    CT: int
    FO_Pct: float
    Pen: int
    Goals_Allowed: int
    Saves: int
    Clear_Pct: float
    Year: int

class Game(BaseModel):
    Date: int
    Team_Name: str
    Opponent: str
    Result: str
    Goals: int
    Assists: int
    Points: int
    Shots: int
    SOG: int
    Man_Up_G: Optional[int]
    GB: int
    TO: int
    CT: int
    FO_Won: int
    FOs_Taken: int
    Pen: int
    Goals_Allowed: int
    Saves: int
    W: int
    L: int
    Clear_Pct: float
    Opp_Goals: int
    Opp_Assists: int
    Opp_Points: int
    Opp_Shots: int
    Opp_SOG: int
    Opp_Man_Up_G: Optional[int]
    Opp_GB: int
    Opp_TO: int
    Opp_CT: int
    Opp_FO_Won: int
    Opp_FOs_Taken: int
    Opp_Pen: int
    Opp_Saves: int
    Opp_Clear_Pct: float
    Year: int
    Home: int
    Away: int
    Location: str
    OT: int
    Distance_Traveled: float
    Team_Id: int
    Opponent_Id: int

class cleanGameDict(object):
    def __init__(self, games_list):
        self.games_list = games_list
        self.remove_spaces()
        self.remove_hyphens()

    def remove_spaces(self):
        for index, game in enumerate(self.games_list):
            for key in list(game.keys()):
                if ' ' in key:
                    new_key = key.replace(' ', '_')
                    self.games_list[index][new_key] = self.games_list[index].pop(key)

    def remove_hyphens(self):
        for index, game in enumerate(self.games_list):
            for key in list(game.keys()):
                if '-' in key:
                    new_key = key.replace('-', '_')
                    self.games_list[index][new_key] = self.games_list[index].pop(key)


def check_year(year, df):
    if year:
        pattern = re.compile(r'^(2018|2019|2020|2021|2022|2023|2024)(,(2018|2019|2020|2021|2022|2023|2024))*$')
        
        if pattern.match(year):   
            years = set(map(int, year.split(',')))

            # Filter dataframe for correct years
            df_filtered = df[df["Year"].isin(years)]
            
            return df_filtered
        else:
            raise HTTPException(status_code=404, detail="Team not found")
    return df

def check_team(team, df):
    # If user specified a team
    if team:
        # Check team is a valid team or if all teams are specified 
        if team in df['Team Name'].values:
            df = df[df['Team Name'] == team]
            return df 
        else:
            raise HTTPException(status_code=404, detail=f"Team {team} not found")
    else: 
        return df

def get_csv(df, year, team):
    stream = io.StringIO()

    df_year_filtered = check_year(year, df)
    df_team_filtered = check_team(team, df_year_filtered)
    
    df_team_filtered.to_csv(stream, index = False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response

@app.get("/games")
async def get_games(year: Optional[str] = None, team: Optional[str] = None):
    """
    End point to retrieve the general game by game information 

    Args:
        year (Optional[str], optional): _description_. Defaults to None.
        team (Optional[str], optional): _description_. Defaults to None.
        Examples:
             http://localhost:8000/games?year=2024,2021&team=michigan - will retrieve all of the games for 2021 & 2024 for Michigan
             http://localhost:8000/games?team=harvard - will retrieve all the games for every year for Harvard
             http://localhost:8000/games - will retrieve all of the game information from every year for every team
        
    Returns:
        json: json representation of the game
    """
    df_year_filtered = check_year(year, games)
    df_team_filtered = check_team(team, df_year_filtered)

    print(df_team_filtered[df_team_filtered['Team Name'] == 'yale' ])  


    # Validate the game data were returning     
    data = df_team_filtered.to_dict(orient='records')
    cleaned_game_data = cleanGameDict(data)
    for game in cleaned_game_data.games_list:
        validate_game = Game(**game)

    return cleaned_game_data.games_list

@app.get("/teams")
async def get_teams(year: Optional[str] = None, team: Optional[str] = None):
    """
    End point to retrieve the general team info 

    Args:
        year (Optional[str], optional): _description_. Defaults to None. 
        team (Optional[str], optional): _description_. Defaults to None.
        Examples:
             http://localhost:8000/teams?year=2024,2021&team=michigan - will retrieve all of the team for 2021 & 2024 for Michigan
             http://localhost:8000/teams?team=harvard - will retrieve all the team for every year for Harvard
             http://localhost:8000/teams - will retrieve all of the team information from every year for every team

    Returns:
        json: json representation of the team 
    """
    df_year_filtered = check_year(year, teams)
    df_team_filtered = check_team(team, df_year_filtered)

    print(df_team_filtered['Team Name'])  

    # Validate the game data were returning     
    data = df_team_filtered.to_dict(orient='records')
    cleaned_team_data = cleanGameDict(data)
    for game in cleaned_team_data.games_list:
        validate_game = Team(**game)

    return data
@app.get("/teams/names")
async def get_teams_names(year: Optional[str] = None):
    """
    End point to retrieve the general team info 

    Args:
        year (Optional[str], optional): _description_. Defaults to None. 
        team (Optional[str], optional): _description_. Defaults to None.
        Examples:
             http://localhost:8000/teams?year=2024,2021&team=michigan - will retrieve all of the team for 2021 & 2024 for Michigan
             http://localhost:8000/teams?team=harvard - will retrieve all the team for every year for Harvard
             http://localhost:8000/teams - will retrieve all of the team information from every year for every team

    Returns:
        json: json representation of the team 
    """
    df_year_filtered = check_year(year, teams)
    df_year_filtered = list(df_year_filtered['Team Name'])
    return df_year_filtered

@app.get("/games/csv")
async def get_games_csv(
    year: Optional[str] = Query(None, min_length=4, max_length=50, regex='^(2018|2019|2020|2021|2022|2023|2024)(,(2018|2019|2020|2021|2022|2023|2024))*$'),
    team: Optional[str] = Query(None, min_length=2, max_length=50)
):
    return get_csv(games, year, team)

@app.get("/teams/csv")
async def get_games_csv(
    year: Optional[str] = Query(None, min_length=4, max_length=50, regex='^(2018|2019|2020|2021|2022|2023|2024)(,(2018|2019|2020|2021|2022|2023|2024))*$'),
    team: Optional[str] = Query(None, min_length=2, max_length=50)
):
    return get_csv(teams, year, team)

@app.get("/")
async def home():
    """
    End point to retrieve the schedule of games left to play 

    Returns:
        json: json representation of the schedule 
    """
    return schedule_dict

@app.get("/results")
async def get_results():
    """
    End point to retrieve the schedule of games left to play 

    Returns:
        json: json representation of the schedule 
    """
    # Function to sort and concatenate team names
    def sort_teams(row):
        teams = [row['Team Name'], row['Opponent']]
        return tuple(sorted(teams))

    # Create a new column with sorted team names
    results['Sorted_Teams'] = results.apply(sort_teams, axis=1)
       
    df_no_duplicates = results.drop_duplicates(subset=['Date', 'Sorted_Teams'])

    # Drop the 'Sorted_Teams' column if you don't need it anymore
    df_no_duplicates.drop(columns=['Sorted_Teams'], inplace=True)

    data = df_no_duplicates.to_dict(orient='records')
    cleaned_game_data = cleanGameDict(data)
    for game in cleaned_game_data.games_list:
        validate_game = Game(**game)

    return cleaned_game_data.games_list

@app.get("/{path:path}")
async def catch_all(path: str):
    raise HTTPException(status_code=400, detail="Endpoint not found")


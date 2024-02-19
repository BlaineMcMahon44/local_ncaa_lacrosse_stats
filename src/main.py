from .data_operations import ProcessGameData
from .data_operations import ProcessTeamData
from .data_extractors import Extractor

def main():
    
    years = ["2019"]
    '''
    extractor = Extractor(years)
    extractor.break_up_extractors(2, games=False)
    #Post Process Block for Team Data
    data = ProcessTeamData(extractor.teams, extractor.team_headers, "Team_Data_all_years.csv")
    data.process_data()
    '''

    extractor = Extractor(years) 
    extractor.break_up_extractors(2, games=True)
    game_data = ProcessGameData(extractor.games, extractor.game_headers,"game_data_2018_2019.csv")
    game_data.create_dataframe()
    game_data.rename_column('Institution', 'Team Name')
    game_data.process_data()
    game_data.save_data_csv()
    
if __name__ == "__main__":
    main()
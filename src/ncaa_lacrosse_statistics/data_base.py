from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd
class DataBase(object):
    # Location of database
    db_file = 'sqlite:///lacrosse_statistics.db'
    
    # Create Engine
    engine = create_engine(db_file)
    games_data_csv = os.path.join(os.getcwd(), 'data','csv', 'Updated_Games')
    team_data_csv = os.path.join(os.getcwd(), 'data', 'csv', 'Teams')
    
    # Reflect the database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)

    def __init__(self, games_table_name, team_table_name):
        self.games_data = games_table_name
        self.team_data = team_table_name   
        
        # Create a database session 
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def convert_df_sql(self):
        # Convert games table to table in database
        df = pd.read_csv(self.games_data_csv, index_col=0)
        print(df[df['Team Name'] == 'harvard'])
        df.to_sql(self.games_data, con=self.engine, if_exists='replace', index=False)

        # Convert teams table to table in database
        df = pd.read_csv(self.team_data_csv, index_col=0)
        df.to_sql(self.team_data, con=self.engine, if_exists='replace', index=False)
        
if __name__ == '__main__':
    db = DataBase('Games_Data','Team_Data')
    db.convert_df_sql()

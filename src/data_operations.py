import hashlib
import pandas as pd
import numpy as np
import re
from .logger import MyLogger
import os 
from datetime import datetime
from geopy.geocoders import Nominatim
import geopy.distance
from .geo_data import geo_locations


# Create a logger instance
logger = MyLogger(__name__)

class ProcessData(object):
    """
    Base class for data processing.

    Parameters
    ----------
    data : list
        A list of dataframes for each year.
    output_file_name : str, optional
        The name of the output CSV file, by default "sample_data.csv".

    Attributes
    ----------
    df : pandas.DataFrame
        The combined dataframe.
    output_file_name : str
        The name of the output CSV file.

    Methods
    -------
    save_data_csv(self, raw=False)
        Saves the processed data to a CSV file.
    rename_column(self, column_name, new_column_name)
        Renames a column in the dataframe.
    reset_column_order(self, desired_column_order)
        Resets the column order of the dataframe.
    reset_index(self)
        Resets the index of the dataframe.
    compute_percentage(self, float_columns)
        Computes a percentage of a float column.
    convert_memory_types(self)
        Converts integer and float columns to more memory-efficient types.
    drop_columns(self, column_names)
        Drops one or more columns from the dataframe.
    create_ids_for_teams(self)
        Creates an ID for each team based on their name.
    """

    def __init__(self, data, output_file_name='sample_data.csv'):
        self.data = data
        self.df = None
        self.output_file_name = output_file_name

    def save_data_csv(self, raw=False):
        """
        Saves the processed data to a CSV file.

        Parameters
        ----------
        raw : bool, optional
            If True, saves the raw data without cleaning, by default False.

        Returns
        -------
        None
            Saves the processed data to a CSV file.
        """
        # Get the current date and time
        current_datetime = datetime.now()

        # Format and print the current date and time with a custom format
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H:%M:%S")

        # Construct the full path without changing the working directory
        output_directory = os.path.join(os.getcwd(), "data", formatted_datetime)
        os.makedirs(output_directory, exist_ok=True)

        # Save the DataFrame to CSV in the specified directory
        output_file_path = os.path.join(output_directory, self.output_file_name)
        if raw:
            self.df.to_csv(output_file_path, index=False)
        else:
            self.df.to_csv(output_file_path)

    def rename_column(self, column_name, new_column_name):
        """
        Renames a column in the dataframe.

        Parameters
        ----------
        column_name : str
            The name of the column to rename.
        new_column_name : str
            The new name for the column.
        """
        if column_name in self.df.columns:
            self.df.rename(columns={column_name: new_column_name}, inplace=True)

    def reset_column_order(self, desired_column_order):
        """
        Resets the column order of the dataframe.

        Parameters
        ----------
        desired_column_order : list
            A list of the desired column order.
        """
        for column in desired_column_order:
            if column not in self.df.columns:
                raise ValueError(f"Column '{column}' not found in the DataFrame.")
        self.df = self.df[desired_column_order]
    
    def reset_index(self):
        """
        Resets the index of the dataframe.
        """
        try:
            self.df = self.df.reset_index(drop=True)
        except Exception as e:
            logger.error(f"Error resetting dataframe index {e}")

    def compute_percentage(self, float_columns: list)-> None:
        """
        Computes a percentage of a float column.

        Parameters
        ----------
        float_columns : list
            A list of float columns to compute the percentage of.
        """
        for column in float_columns:
            if column in self.df.columns:
                is_float_column = np.issubdtype(self.df[column].dtype, np.floating)
                if is_float_column: 
                    self.df[column] = np.ceil(self.df[column] * 100) / 100
                    self.df[column] = self.df[column].round(1)

    def convert_memory_types(self):
        """
        Converts integer and float columns to more memory-efficient types.
        """
        try:
            for column in self.numeric_cols:
                if column in self.df.columns:
                    if self.df[column].dtype == 'int64':
                        if self.df[column].max() < 20000:
                            self.df[column] = self.df[column].astype('int16')
        
        except Exception as e:
                logger.error(f"Error in changing integer or float type/value {e}") 

    def convert_to_numeric(self, numeric_cols: list)->None:
        """
        Converts integer and float columns to more memory-efficient types.
        """
        try:
            for column in numeric_cols:
                if column == 'Clear Pct' or column == 'Opp_Clear Pct': # Want to preserve the decimal values in this column 
                    self.df[column] = self.df[column].apply(lambda x: float(x) if str(x).strip() else 0)
                else:
                    self.df[column] = self.df[column].apply(lambda x: int(x) if str(x).strip() else 0)
        except ValueError as ve:
            logger.error(f"Error in converting a value in {column} to an integer/float {ve}")
            raise ve

    def drop_columns(self, column_names):
        """
        Drops one or more columns from the dataframe.

        Parameters
        ----------
        column_names : list
            A list of the column names to drop.
        """
        try:
            if column_names:
                self.df.drop(column_names, axis='columns', inplace=True)
        except KeyError as ke:
            logger.error(f"Error one or more columns names {column_names} are not present in dataframe {self.df.columns}")

    def create_ids_for_teams(self):
        """
        Creates an ID for each team based on their name.
        """
        if 'Institution' in self.df.columns:
            try:
                self.df['Id'] = self.df['Institution'].apply(lambda x: int(hashlib.sha256(x.encode()).hexdigest(),16 )% 1000 ) 
            except Exception as e:
                logger.error(f"Error in converting Institution into an ID ")

    def clean_data_values(self)-> None: # Some institutions have values with: (NY) or unwanted periods
        """
        Cleans the data values in the dataframe.

        Parameters:
        self (object): The instance of the class.

        Returns:
        None

        Raises:
        ValueError: If there is an error in cleaning the data values.
        """
        try:
            for column in self.df.columns:
                if column == 'Institution' or column == 'Team Name' or column == 'Opponent':
                    self.df[column] = self.df[column].apply(lambda x: x.lower())
                if column == 'Clear Pct' or column == 'Opp_Clear Pct':
                    self.df[column] = self.df[column].astype(str).apply(lambda x: re.sub('/', '', x))
                    self.df[column] = self.df[column].astype(str).apply(lambda x: re.sub('\,','',x))
                if self.df[column].dtype == 'object' and column != 'Clear Pct' and column != 'Opp_Clear Pct':
                    self.df[column] = self.df[column].astype(str).apply(lambda x: re.sub('\.[0-9]*','',x))
                    self.df[column] = self.df[column].astype(str).apply(lambda x: re.sub('\(.*\)','',x))
                    self.df[column] = self.df[column].astype(str).apply(lambda x: re.sub('\'','',x))
                    self.df[column] = self.df[column].astype(str).apply(lambda x: re.sub('\,','',x))
                    self.df[column] = self.df[column].astype(str).apply(lambda x: re.sub('/','', x))

        except ValueError as ve:
            logger.error(f"ValueError in cleaning data values: {ve} in column {column} which has type {self.df[column].dtype}")
            # Use pd.to_numeric with errors='coerce' to safely convert to numeric
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
            # Now handle NaN values if needed, for example, replace them with 0
            self.df[column].fillna(0, inplace=True)

        except Exception as e:
            logger.error(f"Error in cleaning data values {e}")
            raise e

class ProcessGameData(ProcessData):
    """
    Class for processing game data.

    Parameters
    ----------
    team_data : list
        A list of dataframes for each year.
    headers : list
        A list of the headers for each dataframe.
    output_file_name : str, optional
        The name of the output CSV file, by default "sample_data.csv".

    Attributes
    ----------
    data : list
        A list of dataframes for each year.
    headers : list
        A list of the headers for each dataframe.
    df : pandas.DataFrame
        The combined dataframe.
    output_file_name : str
        The name of the output CSV file.

    Methods
    -------
    clean_data_values(self)
        Cleans the data values in the dataframe.
    compute_win_loss(self)
        Computes the win/loss for each game.
    compute_home_away_teams(self)
        Computes the home/away status for each team.
    convert_to_numeric(self)
        Converts the data values to numeric types.
    handle_null_values(self)
        Handles null values in the dataframe.
    compute_faceoff_pct(self)
        Computes the faceoff percentage for each game.
    """

    def __init__(self, team_data, headers, output_file_name = "sample_data.csv"):
        super().__init__(team_data, output_file_name)
        self.data = team_data
        self.headers = headers[0]
        self.unwanted_cols = ['OTG', 'YC', 'G Min', 'Pen Time', 'Man-Down G', 'Man-Down G', 'RC', 'Clears', 'Att', 'T', 'Opp_G Min', 'Opp_L', 'Opp_W','Opp_T', 'Opp_RC', 'Opp_YC', 'Opp_Clears', 'Opp_Clears', 'Opp_Att', 'Opp_OTG', 'Opp_Goals Allowed', 'Opp_Pen Time','Opp_Man-Down G','Opp_G']        
        
        self.numeric_cols =  ['G', 'Goals', 'Opp_Goals', 'Assists', 'Opp_Assists', 'Points', 'Opp_Points', 'Shots',  
       'SOG', 'Man-Up G', 'Opp_Man-Up G', 'GB', 'TO', 'CT', 'Opp_CT', 'FO Won', 'FOs Taken','Opp_FO Won', 'Opp_FOs Taken', 'Pen', 'Opp_Shots', 'Opp_Pen',
       'Goals Allowed', 'Saves', 'Clear Pct', 'Year', ]
        
        self.string_cols = ['Institution', 'Opponent', 'Location']

    def create_dataframe(self):
        """
        Creates a dataframe from the input data.

        Parameters:
        data (list): A list of dataframes for each year.
        headers (list): A list of the headers for each dataframe.

        Returns:
        pandas.DataFrame: The combined dataframe.

        Raises:
        Exception: If there is an error in creating the dataframe.
        """
        dfs = []
        try:
            for year in self.data:  # Create a dataframe for each year
                flat_arr = [item for sublist in year for item in sublist]
                dfs.append(pd.DataFrame(flat_arr, columns=self.headers))
        except Exception as e:
            logger.error(f"Error adding dataframe for year {year} {e}... appending a blank dataframe inplace")
            dfs.append(pd.DataFrame())
        
        try:
            if not self.df:
                self.df = pd.concat(dfs)  # Combine all dataframes into a single dataframe
        except Exception as e:
            logger.error(f"Error in combining all dataframes into one dataframe {e}")
            raise e    

    def remove_null_games(self)-> None:
        """
        Remove games that were not played, but data row is still populated

        Returns:
        None
        """
        # Find the index of rows that satisfy the condition
        rows_to_drop = self.df[(self.df['Result'] == '-') | (self.df['Result'].isna()) & (self.df['Goals'].isna()) & (self.df['Opp_Goals'].isna())].index

        # Drop the rows based on the index
        self.df.drop(rows_to_drop, inplace=True)
    
    def clean_opponent_names(self)-> None:
        """
        If Location is in the Opponent value, remove it from the Opponent column.

        Returns:
        None 
        """
        for index, value in self.df['Opponent'].items():
            if '\n' in value:
                split_value = value.split('\n')
                self.df.at[index, 'Opponent'] = split_value[0]

    def compute_win_loss(self)-> None: # Some institutions have values with: (NY) or unwanted periods
        """
        Computes the win/loss for each game.

        Parameters:
        self (object): The instance of the class.

        Returns:
        None

        """
        for index, value in self.df['Result'].items():
            cleaned_value = re.sub('\([0-9]\)', '', value)

            # Update if game went overtime
            if '(' in value:
                self.df.at[index, 'OT'] = 1
                cleaned_value = cleaned_value.replace('(', '').replace(')', '')  # Remove parentheses
                self.df.at[index, 'Result'] = cleaned_value
            else:
                self.df.at[index, 'OT'] = 0
            
            # Handle case for null result
            if value == '-':
                continue 

            # Update if game went overtime
            if '*' in value:
                cleaned_value = cleaned_value.replace('*', '')
                self.df.at[index, 'Result'] = cleaned_value

            split_value = cleaned_value.split('-')
                
            # Compute win / loss 
            if int(split_value[0]) > int(split_value[1]):
                self.df.at[index, 'W'] = 1
                self.df.at[index, 'L'] = 0
            else:
                self.df.at[index, 'W'] = 0
                self.df.at[index, 'L'] = 1        


    def compute_home_away_teams(self):
        """
        Compute the home/away status for each team. Removes @ from the opponent team name.
        
        Returns:
        None 
        """
        for index, value in self.df['Opponent'].items():
            if '@' in value:
                self.df.at[index, 'Home'] = 0
                self.df.at[index, 'Away'] = 1
                self.df.at[index, 'Location'] = value.split('@')[1].strip()
                self.df.at[index, 'Opponent'] = value.replace('@','')
            else:
                self.df.at[index, 'Home'] = 1
                self.df.at[index, 'Away'] = 0
                self.df.at[index, 'Location'] = self.df.at[index, 'Team Name']

    def handle_null_values(self):
        """
        Fills null numeric columns with a default value of 0.  Will drop any columns that have NaN values in Institution or Conference.

        Raises:
            e: if there is any exception in handling the null values.
        """
        try:
            for column in self.numeric_cols:
                # Replace NaN values with a default value or use another strategy
                self.df[column].fillna(0, inplace=True)  # Replace NaN with 0 as an example, adjust as needed
            self.df.dropna(subset=self.string_cols, how='any', inplace=True) # Drop rows that have strings with NaN in Institution or Conference
        except Exception as e:
            logger.error(f"Error in handling null values {e}")
            raise e

    def compute_faceoff_pct(self):
            """
            Computes the faceoff percentage for each game. Removes FO won and FOs Taken from the dataframe. Adds FO Pct to the dataframe.

            Parameters:
            self (object): The instance of the class.

            Returns:
            None 
            """
            if 'FO Won' in self.df.columns and 'FOs Taken' in self.df.columns:
                
                # Compute faceoff percentage using FO Won and FOs Taken
                self.df['FO Pct'] = self.df['FO Won'] / self.df['FOs Taken']
                self.df['FO Pct'] = np.ceil(self.df['FO Pct'] * 1000) / 1000
                self.df['FO Pct'] = np.ceil(self.df['FO Pct'].apply(lambda x: x * 100)).round(1)
                
                # Drop unnecessary columns
                self.drop_columns(['FO Won','FOs Taken'])

                # Fill NaN values in 'FO Pct' with zero
                self.df['FO Pct'].fillna(0, inplace=True)

                # Update Numeric Cols to match
                self.numeric_cols.remove('FO Won')
                self.numeric_cols.remove('FOs Taken')
            
            else:
                logger.warning(f"Trying to compute Face Percentage with correct columns in dataframe {self.df.columns}")
    
    def compute_geo_location(self):
        """
        Compute the geolocation for each game. 
        If a team is played an away game use the location and team name to calculate distance traveled for the game.

        Adds a new column to the dataframe called: Distance Traveled.

        Returns:
        None
        """
        for index, value in self.df['Home'].items():

            logger.info(f"Home Team {self.df.at[index, 'Team Name']} university")
            logger.info(f"Away Team {self.df.at[index, 'Opponent']} university")
            logger.info(f"Location {self.df.at[index, 'Location']} ")
            
            if value == 1:
                self.df.at[index, 'Distance Traveled'] = 0
            else:
                try:
                    loc = Nominatim(user_agent="GetLoc")
                
                    home_location = loc.geocode(f"{self.df.at[index, 'Team Name']} university")
                    
                    if home_location == None:
                        home_coordinates = geo_locations[self.df.at[index, 'Team Name']] 
                    else:
                        home_coordinates = (home_location.latitude, home_location.longitude)

                    away_location = loc.geocode(f"{self.df.at[index, 'Location']} university")
                    
                    if away_location == None:
                        away_coordinates = geo_locations[self.df.at[index, 'Opponent']]
                    else:
                        away_coordinates = (away_location.latitude, away_location.longitude)

                    if home_coordinates and away_coordinates:
                        self.df.at[index, 'Distance Traveled'] = geopy.distance.geodesic(home_coordinates, away_coordinates).miles
                    else:
                        self.df.at[index, 'Distance Traveled'] = None

                except Exception as e:
                    logger.error(f"{e}")                
            
            logger.info(self.df.at[index, 'Distance Traveled'])

    def process_data(self):
        self.remove_null_games()
        self.drop_columns(self.unwanted_cols)
        self.compute_home_away_teams()
        self.clean_opponent_names()
        self.compute_win_loss()
        self.clean_data_values()
        self.reset_index()
        self.convert_to_numeric(self.numeric_cols)
        self.create_ids_for_teams()
        self.compute_geo_location()


class ProcessTeamData(ProcessData):
    def __init__(self, team_data, headers, output_file_name="team_data.csv"):
        super().__init__(team_data, output_file_name)
        self.data = team_data
        self.headers = headers[0]
        self.unwanted_cols = ['G Min', 'Man-Down G', 'RC', 'YC', 'Clears','Att', 'OTG', 'Pen Time']
        self.numeric_cols =  ['G', 'Goals', 'Assists', 'Points', 'Shots',
       'SOG', 'Man-Up G', 'GB', 'TO', 'CT', 'FO Won', 'FOs Taken', 'Pen',
       'Goals Allowed', 'Saves', 'Clear Pct', 'Year']
        self.string_cols = ['Institution','Conference']

    def create_dataframe(self):
        """
        Creates a dataframe from the input data.

        Parameters:
        data (list): A list of dataframes for each year.
        headers (list): A list of the headers for each dataframe.

        Returns:
        pandas.DataFrame: The combined dataframe.

        Raises:
        Exception: If there is an error in creating the dataframe.
        """
        try:
            logger.info(self.headers)
            flat_data = [item for sublist in self.data for item in sublist]
            self.df = pd.DataFrame(flat_data, columns=self.headers) # Create a dataframe from the list of dataframes
        except Exception as e:
            logger.error(f"Error adding dataframe for year {e}... appending a blank dataframe inplace")        
        logger.info(self.df.head())

    def handle_null_values(self):
        try:
            for column in self.numeric_cols:
                # Replace NaN values with a default value or use another strategy
                self.df[column].fillna(0, inplace=True)  # Replace NaN with 0 as an example, adjust as needed
            self.df.dropna(subset=self.string_cols, how='any', inplace=True) # Drop rows that have strings with NaN in Institution or Conference
        except Exception as e:
            logger.error(f"Error in handling null values {e}")
            raise e

    def compute_faceoff_pct(self):
            if 'FO Won' in self.df.columns and 'FOs Taken' in self.df.columns:
                
                # Compute faceoff percentage using FO Won and FOs Taken
                self.df['FO Pct'] = self.df['FO Won'] / self.df['FOs Taken']
                self.df['FO Pct'] = np.ceil(self.df['FO Pct'] * 1000) / 1000
                self.df['FO Pct'] = np.ceil(self.df['FO Pct'].apply(lambda x: x * 100)).round(1)
                
                # Drop unnecessary columns
                self.drop_columns(['FO Won','FOs Taken'])

                # Fill NaN values in 'FO Pct' with zero
                self.df['FO Pct'].fillna(0, inplace=True)

                # Update Numeric Cols to match
                self.numeric_cols.remove('FO Won')
                self.numeric_cols.remove('FOs Taken')
            
            else:
                logger.warning(f"Trying to compute Face Percentage with correct columns in dataframe {self.df.columns}")

    def process_data(self):
        self.create_dataframe()
        self.drop_columns(self.unwanted_cols)
        self.handle_null_values()
        self.clean_data_values()
        self.convert_to_numeric(self.numeric_cols)
        self.compute_faceoff_pct()
        self.reset_index()
        self.create_ids_for_teams()
        self.reset_column_order(['Id', 'Institution', 'Conference', 'G', 'Goals', 'Assists', 'Points', 'Shots',
            'SOG', 'Man-Up G', 'GB', 'TO', 'CT', 'FO Pct', 'Pen', 'Goals Allowed', 'Saves',
            'Clear Pct', 'Year'])
        self.rename_column('G','Games')
        self.rename_column('Institution','Team Name')
        self.save_data_csv()
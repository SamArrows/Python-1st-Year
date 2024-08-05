import csv
import datetime as dt
import os
import pandas as pd
from utils import *

def get_days(data : pd.DataFrame, pollutant : str, mapping) -> list:
    """
    -Finds the data for each day based on the readings from each of the 24 hours in each day
    -read every 24 rows, get the specific data for pollutant specified
    :params:
        =data - a pandas dataframe which indicates which station to read data from, corresponding to a specific csv file; it is read using a filepath relative to the python script.
            In the function specified in the main file named reporting_menu(), only three options will be given for users to choose from, to avoid invalid inputs:
            (M)arylebone Road, (N)orth Kensington and (H)arlington. The functions daily_average and daily_median pass the relevant filepath to get_days based on
            the value from reporting_menu. The data frame is obtained from a dictionary of user-inputs as keys and the csv files as values.
        =pollutant - a string which specifies which pollutant to read data from, corresponding to a different column in the csv files; when
            requesting the user for input in the main file, only valid inputs will be given as options: no, pm10, pm25
        =mapping - a function that you pass in to perform on each day's data, i.e. performing meannvalue on the list of 24 values that represents each day, and then returning the values
            of these mappings. The reason for having a function in the input is due to both daily_median and daily_average using the same data but performing different operations on the data.
            As a list of the daily data can't be returned due to being too big, it makes sense to use the same function get_days for reading it into lists from the dataframes and applying the specified
            function to the data
    :return: a list containing the data for a specified pollutant per day of size 365 as it spans a year
    """
    line_count = 0
    day = []
    mappings = []
    for i in range(0, len(data)):
        try:
            day.append(float(data.loc[i].at[pollutant]))
        except:
            '''exception will occur if the data cannot be converted to a float - i.e. it is "No data". This won't be added to the list.
            I have made the design choice to not replace any "No data" cells with alternate data as if you have too many consecutive cells
            of No data, then taking averages over a day where 23/24 cells are just filled in with some abstract value like 0 has no real meaning
            for monitoring anything. Instead, it is simply more logical to try and take averages of the data available.
            '''
            a = 1   #nothing needs to happen if data isn't being added; a = 1 is just filler code
        if(line_count != 0 and line_count % 23 == 0):   #first line is 0 so each 24 lines are offset by 1
            mappings.append(mapping(day))
            day = []
        line_count += 1
    return mappings

def daily_average(data : dict, monitoring_station : str, pollutant : str):
    """
    -Finds the average pollution for each day based on the readings from each of the 24 hours in each day
    -read every 24 rows, get the specific data for pollutant specified
    -it does this by passing a function (in this case, meannvalue) to map onto each day to the get_days function;
    -get_days finds each of the 24 values for each day and then applies a function to them, either median or mean value
    :params:
        =data - a dictionary of filepaths corresponding to the csv files that contain pollution data. Depending on the pollutant and monitoring station,
            a specific filepath will be selected from the dictionary to read data from and create a pandas dataframe with.
            It will be passed to this function from the main.py file during the calling of reporting_menu
        =monitoring_station - a string which indicates which station to read data from, corresponding to a specific csv file; in the function
            specified in the main file named reporting_menu(), only three options will be given for users to choose from, to avoid invalid inputs:
            (M)arylebone Road, (N)orth Kensington and (H)arlington
        =pollutant - a string which specifies which pollutant to read data from, corresponding to a different column in the csv files; when
            requesting the user for input in the main file, only valid inputs will be given as options: no, pm10, pm25
    :return: a list containing the daily averages of size 365 as it spans a year
    """
    return get_days(data[monitoring_station], pollutant, meannvalue)

def daily_median(data : dict,  monitoring_station : str, pollutant : str):
    """
    -Finds the median pollution for each day based on the readings from each of the 24 hours in each day
    -read every 24 rows, get the specific data for pollutant specified
    -Like the daily_average function, daily_median passes a function to get_days to map onto each day's 24 values; in this case, medianvalue is the function to be mapped
    :params:
        =data - a dictionary of filepaths corresponding to the csv files that contain pollution data. Depending on the pollutant and monitoring station,
            a specific filepath will be selected from the dictionary to read and create a pandas dataframe from. It will be passed to this function from the main.py file during the
            calling of reporting_menu
        =monitoring_station - a string which indicates which station to read data from, corresponding to a specific csv file; in the function
            specified in the main file named reporting_menu(), only three options will be given for users to choose from, to avoid invalid inputs:
            (M)arylebone Road, (N)orth Kensington and (H)arlington
        =pollutant - a string which specifies which pollutant to read data from, corresponding to a different column in the csv files; when
            requesting the user for input in the main file, only valid inputs will be given as options: no, pm10, pm25
    :return: a list containing the daily medians of size 365 as it spans a year
    """
    return get_days(data[monitoring_station], pollutant, medianvalue)

def hourly_average(data, monitoring_station, pollutant):
    """
    -Gets the average pollution level for each hour of a day over the course of a year - i.e. gets the average pollution for 13:00 every day for 365 days; returns 24 values in a list
    :params:
        =data - a dictionary of filepaths corresponding to the csv files that contain pollution data. Depending on the pollutant and monitoring station,
            a specific filepath will be selected from the dictionary to read data from and create a pandas dataframe with.
            It will be passed to this function from the main.py file during the calling of reporting_menu
        =monitoring_station - a string which indicates which station to read data from, corresponding to a specific csv file; in the function
            specified in the main file named reporting_menu(), only three options will be given for users to choose from, to avoid invalid inputs:
            (M)arylebone Road, (N)orth Kensington and (H)arlington
        =pollutant - a string which specifies which pollutant to read data from, corresponding to a different column in the csv files; when
            requesting the user for input in the main file, only valid inputs will be given as options: no, pm10, pm25
    :return: a dictionary with 24 key-value pairs corresponding to each hour of a day and its average pollution for the specified pollution over the course of the monitoring period (a year),
    i.e. 01:00:00 is a key whose value is the mean average of every pollution measurement taken at 01:00:00 each day across the year
    """
    df = data[monitoring_station]
    original_cols = set(df.columns) # getting all the columns
    new_cols = set()
    for col in original_cols:
        if col not in ["pm10", "pm25", "no", "date"] or col == pollutant:   #keeps the date and time columns along with the desired pollutant column
            new_cols.add(col)
    df = df[new_cols]   #the dataframe is resized so that it is a subset of itself, with the unwanted pollutant columns omitted
    hours = { }
    for i in range(1, 25):
        if i < 10:
            hour = "0" + str(i) + ":00:00"
        else:
            hour = str(i) + ":00:00"
        hourlyData = df.loc[df["time"] == hour]
        hours[hour] = meannvalue(hourlyData[pollutant].values)
    return hours
    
def monthly_average(data, monitoring_station, pollutant):
    """-Finds the average pollution over each month in the space of a year, i.e. average pm10 recordings in January, February ... December
        :params:  
            =data - the dictionary with key-value pairs corresponding to (monitoring station) : (csv_file to read from and create a pandas dataframe with)
            =monitoring_station - a string which indicates which station to read data from, corresponding to a specific csv file; in the function
                specified in the main file named reporting_menu(), only three options will be given for users to choose from, to avoid invalid inputs:
                (M)arylebone Road, (N)orth Kensington and (H)arlington
            =pollutant - a string which specifies which pollutant to read data from, corresponding to a different column in the csv files; when
                requesting the user for input in the main file, only valid inputs will be given as options: no, pm10, pm25
        :return: a dictionary whereby the key is the month as a number (Jan = 01, Feb = 02 ... Dec = 12) and the value is the 
            average recordings for the specified pollutant for each month
    """
    months = { }
    for i in range(1, 13):
        months[i] = 0
    df = data[monitoring_station]
    original_cols = set(df.columns) # getting all the columns
    new_cols = set()
    for col in original_cols:
        if col not in ["pm10", "pm25", "no"] or col == pollutant:   #keeps the date and time columns along with the desired pollutant column
            new_cols.add(col)
    df = df[new_cols]   #the dataframe is resized so that it is a subset of itself, with the unwanted pollutant columns omitted
    monthly_values = []
    current_month = 1
    for ind in df.index:
        month = int(str(df['date'][ind])[5:7])
        if month != current_month:
            months[current_month] = meannvalue(monthly_values)
            current_month += 1
            monthly_values = []
        else:
            monthly_values.append(df[pollutant][ind])
    months[12] = meannvalue(monthly_values)     #the month does't change on the final line of the csv file so to ensure the data for December is read and the average calculated, we must find the average outside the for loop
    return months
    
def peak_hour_date(data, date, monitoring_station,pollutant):
    """-For a given date (e.g. 2021-01-01), returns the hour of the day with the highest pollution level and its corresponding value (e.g. (12:00, 14.8))
        :params: 
            =data - a dictionary of filepaths corresponding to the csv files that contain pollution data. Depending on the pollutant and monitoring station,
                a specific filepath will be selected from the dictionary to read data from. It will be passed to this function from the main.py file during the
                calling of reporting_menu
            =date - a specific date to find the peak pollution for, entered in the form YYYY-MM-DD. This will be done in the main.py file, with error-checking
                to ensure that the user doesn't enter a date outside the range of those in the csv_file (2021-01-01 to 2021-12-31) or one that doesn't exist (e.g. 2021-02-31)
            =monitoring_station - a string which indicates which station to read data from, corresponding to a specific csv file; in the function
                specified in the main file named reporting_menu(), only three options will be given for users to choose from, to avoid invalid inputs:
                (M)arylebone Road, (N)orth Kensington and (H)arlington
            =pollutant - a string which specifies which pollutant to read data from, corresponding to a different column in the csv files; when
                requesting the user for input in the main file, only valid inputs will be given as options: no, pm10, pm25
        :return: a tuple with the time and the corresponding pollution value
    """
    df = data[monitoring_station]
    df = df.loc[df['date'] == date]
    df = df.reset_index()
    valPos = maxvalue(list(df[pollutant]))
    try:    #try will run if all data checked was numerical as the return value from maxvalue should be a single integer for the index of the biggest number
        time = df['time'][valPos]
        value = df[pollutant][valPos]
    except: #if invalid data is found, a list is returned, with the first part being the index of the biggest number found and the second part simply being a string specifying that invalid data was present in the list
        time = df['time'][valPos[0]]
        value = df[pollutant][valPos[0]]
    return value, time

def count_missing_data(data : dict,  monitoring_station : str, pollutant : str) -> int:
    """For a given monitoring station and pollutant, returns the number of "No data" entries found in the data
    :params:
        =data - a dictionary of filepaths corresponding to the csv files that contain pollution data. Depending on the pollutant and monitoring station,
            a specific filepath will be selected from the dictionary to read data from. It will be passed to this function from the main.py file during the
            calling of reporting_menu
        =monitoring_station - a string which indicates which station to read data from, corresponding to a specific csv file; in the function
            specified in the main file named reporting_menu(), only three options will be given for users to choose from, to avoid invalid inputs:
            (M)arylebone Road, (N)orth Kensington and (H)arlington
        =pollutant - a string which specifies which pollutant to read data from, corresponding to a different column in the csv files; when
            requesting the user for input in the main file, only valid inputs will be given as options: no, pm10, pm25
    :return: the total number of 'No data' entries found in the data, as an integer
    """
    df = data[monitoring_station]
    return df[pollutant].value_counts()["No data"]  #counts the occurrences of the values specified inside [] after value_counts for a given column, (pollutant) in this case

def fill_missing_data(data : dict, new_value,  monitoring_station : str, pollutant : str):
    """For a given monitoring station and pollutant, returns a copy of the data with the missing values 'No data' replaced by the value in the parameter new value
        :params:
            =new_value - the value to replace 'No data' with
            =data - a dictionary of filepaths from which to read the data from and and establish a pandas dataframe with
            =monitoring_station - a string which indicates which station to read data from, corresponding to a specific csv file; in the function
                specified in the main file named reporting_menu(), only three options will be given for users to choose from, to avoid invalid inputs:
                (M)arylebone Road, (N)orth Kensington and (H)arlington
            =pollutant - a string which specifies which pollutant to read data from, corresponding to a different column in the csv files; when
                requesting the user for input in the main file, only valid inputs will be given as options: no, pm10, pm25 
        :return: a pandas dataframe with the No data replaced with the new_value  """
    df = data[monitoring_station]
    original_cols = set(df.columns) # getting all the columns
    new_cols = set()
    for col in original_cols:
        if col not in ["pm10", "pm25", "no"] or col == pollutant:   #keeps the date and time columns along with the desired pollutant column
            new_cols.add(col)
    df = df[new_cols]   #the dataframe is resized so that it is a subset of itself, with the unwanted pollutant columns omitted
    df = df.replace("No data", new_value)
    return df
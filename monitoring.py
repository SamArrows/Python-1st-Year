import json
from utils import *
import requests
import datetime as dt
from matplotlib import pyplot as mpl
import math

def get_live_data_from_api(site_code='MY1',species_code='NO',start_date : dt.date =None,end_date : dt.date =None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    start_date = dt.date.today() if start_date is None else start_date
    end_date = start_date + dt.timedelta(days=1) if end_date is None else end_date

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    valid_data = False
    for measurement in res.json()['RawAQData']['Data']: #this code block checks through the requested data to check if there is any data or if all the actual values are empty (''); if they are, then the site or species code must be incorrect, so the json is not returned
        if measurement['@Value'] != '':
            valid_data = True   #as long as one piece of data isn't empty, the data is valid
    if valid_data:
        return res.json()
    else:
        return None

def get_hourly_data(site_code='MY1',species_code='NO',start_date=None,end_date=None):
    '''
    -Gets the hourly data in the form of a dictionary with the key being the date and hour and value being the data at that point in time. If the date range to collect data for is only the space of a day,
    then no date is given in the key and simply the hour is used, i.e:
        {'00:00': '7', 
        '01:00': '6.5',
        '02:00': '4.7',
        '03:00': '5',
        '04:00': '6',
        '05:00': '7.4',
        '06:00': '16',
        '07:00': '34.3',
        '08:00': '101.1',
        '09:00': '100.3'}
    :params: identical to those of get_live_data_from_api() as it passes them straight to it to get the data before effectively just formatting it for ease of use in other parts of the program
        =site_code - the site code to gather data from
        =species_code - type of pollution to monitor
        =start_date - the date from which to start getting data from - defaults to the current day if an invalid date is entered or none is given
        =end_date - the date at which to stop getting data - defaults to tomorrow if an invalid date is entered or none is given, which means the data collected will be up to the latest data collected for today
    :return: a dictionary of data whereby each hour is a key with its value being the pollution monitored at that time; if more than one day is to be monitored then the key will have the date and the hour in the format 2022-12-13 07:00:00
    '''
    try:
        list_of_data = get_live_data_from_api(site_code,species_code,start_date,end_date)['RawAQData']['Data']
    except: #no data exists on the given date so no data is returned from get_live_data_from_api, thus it cannot be subscripted
        return f"No hourly data could be found in the range {start_date} : {end_date}"    #returns None as no hourly data can be fetched
    start_date = dt.date.today() if start_date is None else start_date  #added the date validation to ensure the code runs if the user inputs a false date, i.e. 30th of February which doesn't exist
    end_date = start_date + dt.timedelta(days=1) if end_date is None else end_date

    dictionary = {}
    if end_date.day - start_date.day == 1:  #only one day is having its hourly values collected - no need for the dictionary's keys to have the date, just the hour is enough
        only_day_required = True
    else:
        only_day_required = False
    for i in range(0, len(list_of_data)):
        if only_day_required:
            if i < 10:
                index = "0" + str(i) + ":00"
            else:
                index = str(i) + ":00"                
        else:
            index = list_of_data[i]['@MeasurementDateGMT']
        data = list_of_data[i]['@Value']
        if data != '':
            dictionary[index] = data
    return dictionary

def plot_dictionary(data):
    """
    -Creates a pyplot of the data fed to it when the data is a valid dictionary. The data is in the form of a function such as get_hourly_data(), which when run successfully, returns a dictionary
        of data to parse and process but if there is no data for an entire day for example, then no hourly data can be put into a dictionary so the function returns an error message string which,
        if plot_dictionary receives, will output instead of creating a pyplot for a dictionary. get_daily_means can also be used as an input.
    """
    x,y = [],[]
    if isinstance(data, dict):    #some dates have no data recorded for them so hourly values cannot be fetched
        for key in data:
            x.append(key)
            y.append(float(data[key]))
        mpl.plot(x, y)
        mpl.axis([0, len(x), 0, math.floor(y[maxvalue(y)] + 10)])
        mpl.xticks(rotation=90, fontsize='8', horizontalalignment='right')
        mpl.show()
    else:
        print(data)

def get_daily_means(site_code='MY1',species_code='NO',start_date=dt.date.today() + dt.timedelta(days=-31),end_date=dt.date.today() + dt.timedelta(days=1)):
    """
    -Takes the mean average of each day from start_date to end_date and draws a pyplot graph of them
    :params:
        =site_code - the site code to gather data from
        =species_code - type of pollution to monitor
        =start_date - the date from which to start getting data from - defaults to a month before the current day if an invalid date is entered or none is given
        =end_date - the date at which to stop getting data - defaults to tomorrow if an invalid date is entered or none is given, which means the data collected will be up to the latest data collected for today
        (effectively, the default values for the start and end dates makes it get the daily averages for roughly the past month up to today if no values are given; this contrasts the other functions' default values which
        collect data for the current day as you would end up with just a graph of one value - today's mean average - which isn't particularly useful).
    :return: the function itself doesn't return a value but does create a pyplot showing the daily mean averages for the given time frame, which the user can choose to save from pyplot as an image file  
    """
    averages = {}
    templist = []
    day = start_date
    while day != end_date + dt.timedelta(days=1):
        for i in range(0, 23):
            if i < 10:
                index = "0" + str(i) + ":00"
            else:
                index = str(i) + ":00"   
            hours = get_hourly_data(site_code, species_code, day, day + dt.timedelta(days=1))
            try:   #will always run if hours has read all the 24 pieces of data for the day's hours correctly. If one is missing then that will not be appended to the list 
                templist.append(hours[index])
            except: #if no data was read for hours then it can't be indexed so the except block will run. If data was read but for one of the hours in the day, there was a missing value, this key won't exist in hours so will also throw an exception
                a = 1   #filler code - we don't want to add 0 or some other filler value to temp list if only one hour in the day had a value missing as this skews the average
        if meannvalue(templist) is not None:
            averages[str(day)] = meannvalue(templist)
        templist = []
        day = day + dt.timedelta(days=1)
    return averages

def get_daily_peaks(site_code='MY1',species_code='NO',start_date=dt.date.today() + dt.timedelta(days=-31),end_date=dt.date.today() + dt.timedelta(days=1)):
    """
    -Finds the peak readings each day in the range (start_date) to (end_date) for a given pollutant (species_code) at a (given site_code)
    :params: ^^^ explained here 
    :return: a dictionary with each day's peak values
    """
    peaks = {}
    day = start_date
    while day != end_date + dt.timedelta(days=1):
        for i in range(0, 23):
            if i < 10:
                index = "0" + str(i) + ":00"
            else:
                index = str(i) + ":00"   
            hours = get_hourly_data(site_code, species_code, day, day + dt.timedelta(days=1))
            if isinstance(hours,dict):
                collection = list(zip(hours.keys(), hours.values()))  #zips up the dictionary's key-value pairs in a list
                sorted_by_size = bubble_sort(collection, True, 1, False)   #applies bubble sort on the zipped up list of key-value pairs from the dictionary, using each pair's values to make the comparisons; the fourth parameter is false as we know the list only contains numbers so we don't need to waste time searching for non-numerical values and removing them
                peaks[str(day)] = sorted_by_size[-1][1] #for the second indexer, 0 refers to the key and 1 refers to the value - the key would be the date but we are only interested in the daily peak, not when the daily peak occurred
            #if it wasn't a dictionary, it means it didn't contain any valid hourly readings so no peak could be found
        day = day + dt.timedelta(days=1)
    return peaks
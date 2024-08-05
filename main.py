from reporting import *
import pandas as pd
import datetime as dt
from utils import *
from monitoring import *
from intelligence import *
from matplotlib import pyplot as mpl

csv_files = { 
                "M" : pd.read_csv(os.path.join(os.path.dirname(__file__), "./data/Pollution-London Marylebone Road.csv")) ,   #the os.path stuff is to ensure the file path is located correctly as I found that using simply the filename doesn't work on every device whereas the os path code does
                "N" : pd.read_csv(os.path.join(os.path.dirname(__file__), "./data/Pollution-London N Kensington.csv")),
                "H" : pd.read_csv(os.path.join(os.path.dirname(__file__),"./data/Pollution-London Harlington.csv"))
            }

def main_menu():
    """
    A function that will be executed upon the initialisation of the program, showing the
    main menu of the program allowing the user to navigate through the different options
    Doesn't take any parameters, nor returns any values, but does require the user to enter
    a single-character code in order to call the right function to open the desired menu.
    """
    option = ""
    while True:     #Having a while loop means once a user has exited a submenu, they will by default be brought back to the main menu and given the option to open another menu, or quit
        option = input("Welcome to the ACQUA data monitoring system. Listed below are the options:\n-(R)eporting menu\n-(I)ntelligence menu\n-(M)onitoring menu\n-(A)bout\n-(Q)uit \n>>> ")
        if option == "R":
            reporting_menu()
            #once the user exits a sub-menu, they will automatically be brought back to the main menu to choose another option
        elif option == "I":
            intelligence_menu()
        elif option == "M":
            monitoring_menu()
        elif option == "A":
            about()
        elif option == "Q":
            quit()
        else:
            print("Invalid option selected")


def reporting_menu():
    """
    A function that will be executed when the user chooses the 'R' option in the
    main menu. It should allow the user to choose the necessary options to perform the analyses
    described in Section 4.1 regarding reporting, allowing the user to navigate through the different options and return
    to the main menu - this is done by default when the user quits from the reporting menu, as the reporting menu is
    only called via the main menu in a while loop.
    There are no inputs for the function itself and no outputs, however it requires text-based user input to determine which
    functions it should call and what to parameterise those functions with.
    """
    validOptions = ["1", "2", "3", "4", "5"]
    option = ""
    while option != "Q":
        option = input("Select an analysis to perform from the menu or (Q)uit and return to the main menu:\n-(1) - daily average - returns the daily averages (i.e., 365 values) for a particular pollutant and monitoring station\n-(2) - daily median - returns the daily median values (i.e., 365 values) for a particular pollutant and monitoring station\n-(3) - hourly average - returns the hourly averages (i.e., 24 values) for a particular pollutant and monitoring station\n-(4) - monthly average - returns the monthly averages (i.e., 12 values) for a particular pollutant and monitoring station\n-(5) - peak hour date - for a given date (e.g. 2021-01-01) returns the hour of the day with the highest pollution level and its corresponding value (e.g. (12:00, 14.8))\n >>> ")
        if(option != "Q" and option in validOptions):
            #next we need to get the monitoring station
            validStations = ["N", "M", "H"]
            station = ""
            while station not in validStations:
                station = input("Select a monitoring station out of (M)arylebone Road, (N)orth Kensington and (H)arlington\n >>> ")
            validPollutants = ["no", "pm10", "pm25"]
            pollutant = ""
            while pollutant not in validPollutants:
                pollutant = input("Select a valid pollutant out of (no), (pm10), (pm25)\n >>> ")
            #now all the relevant inputs have been gathered from the user, we just need to call the correct function
            if option == "1":   #daily average
                print(daily_average(csv_files, station, pollutant))
            elif option == "2":     #daily median
                print(daily_median(csv_files, station, pollutant))
            elif option == "3":     #hourly average
                print(hourly_average(csv_files, station, pollutant))
            elif option == "4":     #monthly average
                print(monthly_average(csv_files, station, pollutant))
            else:   #due to our check earlier, we know option is in validOptions so by process of elimination, it must be 5; this corresponds to peak hour date
                date = ""
                while date == "":   #peak_hour_date requires a fourth parameter as a date so we need to validate the user's input and pass it to the function
                    date = input("Enter the date you'd like to find the peak pollution for, in the format YYYY-MM-DD in the range of 2021-01-01 to 2021-12-31 >>> ")
                    valid_date = validate_date(date)
                    if valid_date != False:
                        if valid_date.year != 2021:
                            date = ""
                            print("That wasn't a valid date according to the criteria set!")
                    else:
                        date = ""
                        print("That wasn't a valid date according to the criteria set!")
                print(peak_hour_date(csv_files, str(date), station, pollutant))
    #if the option Q was chosen, then the loop won't run and the function call will come to an end, thus returning us to the main menu

def monitoring_menu():
    """
    A function that will be executed when the user chooses the 'M' option in the
    main menu. It should allow the user to choose the necessary options to perform the tasks
    you implemented for the RM module described in Section 4.3, allowing the user to navigate
    through the different options and return to the main menu.
    There are no inputs for the function itself and no outputs, however it requires text-based user input to determine which
    functions it should call and what to parameterise those functions with.
    """
    site_code, species_code, start_date, end_date = "", "", "", ""
    while site_code == "":
        site_code = input("All options require you to enter a monitoring site code, a species code and a start date.\nBe aware that in the monitoring section, many dates lack data for some hours so some plots or dictionaries created from the data may seem bare due to the lack of readings available\nPlease enter the monitoring station code for validation >>> ")
        if get_live_data_from_api(site_code, 'NO') is None:
            site_code = ""
            print("That was an invalid site code, try again.")
    while species_code == "":
        species_code = input("All options require you to enter a monitoring site code and a species code \nPlease enter the species code for validation >>> ")
        if get_live_data_from_api('MY1', species_code) is None:
            species_code = ""
            print("That was an invalid species code, try again.")
    while start_date == "":
        start_date = input("Please enter the start date in the format YYYY-MM-DD >>> ")
        start_date = validate_date(start_date)
        if start_date == False:
            start_date = ""
            print("That wasn't a valid date. Try again.")
    while end_date == "":
        end_date = input("Most of the options require an end date so please also input one in the format YYYY-MM-DD >>> ")
        end_date = validate_date(end_date)
        if end_date == False:
            end_date = ""
            print("That wasn't a valid date. Try again.")
    validOptions = ["1", "2", "3", "4", "5", "6"]
    option = ""
    while option != "Q":
        option = input("Select an analysis to perform from the menu or (Q)uit and return to the main menu:\n-(1) - get hourly data - returns the hourly values for a particular pollutant and monitoring site over a given time frame as a dictionary\n-(2) - plot hourly data for a given day - attempts to create a pyplot of (1) ^^^\n-(3) - get daily mean averages - returns the mean average values in a day based on hourly readings for a particular pollutant and monitoring station for a given date range. Can take time to process the data and create a plot\n-(4) - plot daily mean averages - attempts to create a pyplot of (3) ^^^\n-(5) - get daily peaks - finds the peak reading for a given pollutant at a given site code each day in the range given and prints a dictionary of it\n-(6) - plot daily peaks - attempts to create a pyplot of (5) ^^^\n-(Q) - Return to the main menu; to change your inputs for monitoring, you need to return to the main menu and re-open the monitoring menu\n >>> ")
        if(option != "Q" and option in validOptions):
            if option == '1':
                print(f"Finding hourly data for site {site_code} on pollutant {species_code} from {start_date} to {end_date}")
                print(get_hourly_data(site_code, species_code, start_date, end_date))
            elif option == '2':
                print(f"Generating plot for hourly data for site {site_code} on pollutant {species_code} for {start_date}")
                plot_dictionary(get_hourly_data(site_code, species_code, start_date))
            elif option == '3':
                print(f"Finding mean average readings for each day based on their hourly readings for {site_code} on pollutant {species_code} from {start_date} to {end_date}")
                print(get_daily_means(site_code, species_code, start_date, end_date))
            elif option == '4':
                print(f"Generating plot for daily means data for site {site_code} on pollutant {species_code} from {start_date} to {end_date}")
                plot_dictionary(get_daily_means(site_code, species_code, start_date, end_date))
            elif option == '5':
                print(f"Finding daily peak readings for pollutant {species_code} at site {site_code} from {start_date} to {end_date}")
                print(get_daily_peaks(site_code, species_code, start_date, end_date))
            else:   #only remaining option is 6
                print(f"Generating plot for daily peaks for site {site_code} on pollutant {species_code} from {start_date} to {end_date}")
                plot_dictionary(get_daily_peaks(site_code, species_code, start_date, end_date))
        #if the option Q was chosen, then the loop won't run and the function call will come to an end, thus returning us to the main menu


def intelligence_menu():
    """
    A function that will be executed when the user chooses the 'I' option in
    the main menu. It should allow the user to choose the necessary options to perform the
    tasks described in Section 4.2 regarding intelligence, allowing the user to navigate through the different options and
    return to the main menu.
    There are no inputs for the function itself and no outputs, however it requires text-based user input to determine which
    functions it should call and what to parameterise those functions with.
    """
    validOptions = ["1", "2", "3", "4"]
    option = ""
    while option != "Q":
        filepath = ""
        while filepath == "":
            filepath = input("All the analyses for the mobility intelligence module require a map to read; please enter a valid image file to read, from the data folder (just the filename with its extension is sufficient) >>> ")
            try:
                i = mpl.imread(f"./data/{filepath}")
            except:
                filepath = ""
                print("File could not be located")
        filepath = "./data/" + filepath
        option = input("Select an analysis to perform from the menu or (Q)uit and return to the main menu:\n-(1) - find red pixels - finds the red pixels in an image specified by the user and outputs a new image file map-red-pixels.jpg in the data folder which is binary and has white for the red pixels and black for everything else\n-(2) - find cyan pixels - finds the cyan pixels in an image specified by the user and outputs a new image file map-cyan-pixels.jpg in the data folder which is binary and has white for the cyan pixels and black for everything else\n-(3) - detect connected components - reads a binary image file, finds the number of connected components and their pixels before writing these to a file cc-output-2a.txt\n-(4) - detect connected components sorted - reads a binary image file and outputs a textfile (cc-output-2b.txt) with the connected components in decreasing order based on their number of pixels, as well as an image file (cc-top-2.jpg) which displays the 2 biggest connected components\n >>> ")
        if(option != "Q" and option in validOptions):
            if option == "1":
                print(f"Finding red pixels for image file {filepath}")
                find_red_pixels(filepath)   #the thresholds are taken at their default values, i.e. upper = 100, lower = 50
            elif option == "2":
                print(f"Finding cyan pixels for image file {filepath}")
                find_cyan_pixels(filepath)   #the thresholds are taken at their default values, i.e. upper = 100, lower = 50
            else:
                colour = ""
                validColours = "R", "C"
                while colour == "":
                    colour = input("To find connected components, the image must be a binary image, i.e. black and white. To get in this format, you must specify whether you want it to find (R)ed connected components or (C)yan connected components >>> ")
                    if colour in validColours:
                        if colour == "R":
                            colour = "red"
                        else:
                            colour = "cyan"
                        if option == "3":
                            print(f"Outputting {colour} connected components and their corresponding numbers of pixels to textfile cc-output-2a.txt for image {filepath}")
                            if colour == "red":
                                detect_connected_components(find_red_pixels(filepath))
                            else:
                                detect_connected_components(find_cyan_pixels(filepath))
                        else: #last possibility is that option == 4
                            print(f"Sorting {colour} connected components by number of pixels and outputting to cc-output-2b.txt; creating image cc-top-2.jpg to represent the largest components; file being used for input = {filepath}")
                            if colour == "red":
                                detect_connected_components_sorted(find_red_pixels(filepath))
                            else:
                                detect_connected_components_sorted(find_cyan_pixels(filepath))
                    else:
                        colour = ""
                        print("Invalid colour entered")
        #if the option Q was chosen, then the loop won't run and the function call will come to an end, thus returning us to the main menu

def about():
    """Prints the module code (ECM1400) and the candidate number (233954)"""
    print("ECM1400\n")
    print("233954")

def quit():
    """Terminates the program when the user chooses the Q option in the main menu.
    No parameters are required and nothing is returned."""
    exit()

if __name__ == '__main__':
    main_menu()
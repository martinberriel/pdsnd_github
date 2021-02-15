import time
import calendar
import pandas as pd
import numpy as np 

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = [month.lower() for month in calendar.month_name[1:]]

DAYS = [day.lower() for day in calendar.day_name[:]]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("First let us know which city do you want to explore first? : ").lower()
        if city not in CITY_DATA:
            print("Unfortunately we have no data for that particular city. Try for example 'chicago'")
        else:
            break
    
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month should we analize?: ").lower()
        if month not in MONTHS and month != 'all':
            print("Please enter a valid month. Try for example 'january' or enter 'all'")
        else:
            break
 
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day of the week should we look into?: ").lower()
        if day not in DAYS and day != 'all':
            print("Please enter a valid day of the week. Try for example 'friday' or enter 'all'")
        else:
            break
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour
        
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]    
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
        common_month = df['month'].mode()[0]
        print("The most common month for the selected filters is: {}".format(MONTHS[common_month - 1].title()))
    except IndexError:
        print("No values are available for the selected month, try a different selection")

    # display the most common day of week
    try:
        common_day_of_week = df['day_of_week'].mode()[0]
        print("The most common day of the week for the selected filters is: {}".format(common_day_of_week))
    except IndexError:
        print("No values are available for the selected day of the week, try a different selection")
        
    # display the most common start hour
    try:
        common_start_hour = df['start_hour'].mode()[0]
        print("The most common start hour for the selected filters is: {}".format(common_start_hour))
    except IndexError:
        print("No values are available for the filters, try a different selection")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        common_start_station = df['Start Station'].mode()[0]
        print("The most common start station for the selected filters is: {}".format(common_start_station))
    except IndexError:
        print("No values are available for the filters, try a different selection")

    # display most commonly used end station
    try:
        common_end_station = df['End Station'].mode()[0]
        print("The most common end station for the selected filters is: {}".format(common_end_station))
    except IndexError:
        print("No values are available for the filters, try a different selection")

    # display most frequent combination of start station and end station trip
    try:
        common_combination_stations = df[["Start Station", "End Station"]].groupby(["Start Station", "End Station"]).size().nlargest()
        common_combination_station_comp = common_combination_stations.iloc[:1].to_string(header=False).split("  ")
        print("The most common station combination is from {} to {} and it has being used {} times".format(common_combination_station_comp[0],common_combination_station_comp[1],common_combination_station_comp[3]))
    except IndexError:
        print("No top station combination could be determined, try a different selection")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def dateStringFromSeconds(secs):
    """Return days, hours , minutes and seconds as a string for a given number of seconds."""
    if secs > 0:
        days = secs//86400
        hours = (secs - days*86400)//3600
        minutes = (secs - days*86400 - hours*3600)//60
        seconds = secs - days*86400 - hours*3600 - minutes*60
        result = ("{0} day{1}, ".format(int(days), "s" if days!=1 else "") if days else "") + \
        ("{0} hour{1}, ".format(int(hours), "s" if hours!=1 else "") if hours else "") + \
        ("{0} minute{1}, ".format(int(minutes), "s" if minutes!=1 else "") if minutes else "") + \
        ("{0} second{1} ".format(int(seconds), "s" if seconds!=1 else "") if seconds else "")
        return result

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_seconds = df['Trip Duration'].sum()
    print("Total travel time was: {}".format(dateStringFromSeconds(total_travel_time_seconds)))
    
    # display mean travel time
    mean_travel_time_seconds = df['Trip Duration'].mean()
    print("Mean travel time was: {}".format(dateStringFromSeconds(mean_travel_time_seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if not df['User Type'].value_counts().empty:
        print("The types of users using the service are:")
        print(df['User Type'].value_counts().to_string(header=False))
    else: 
        print("There is no information about user types on the selection, try with different filters")
    print("\n")

    # Display counts of gender
    if not df['User Type'].value_counts().empty:
        try:
            print("The genders of the users using the service are:")
            print(df['Gender'].value_counts().to_string(header=False))
        except KeyError: 
            print("There is no information about users gender")
    else:
        print("There is no information about user genders on the selection, try with different filters")
    print("\n")

    # Display earliest, most recent, and most common year of birth
    try:
        print("Earliest year of birth is: {}".format(int(df['Birth Year'].min())))
        print("Most recent year of birth is: {}".format(int(df['Birth Year'].max())))
        print("Most common year of birth is: {}".format(int(df['Birth Year'].mode()[0])))
    except KeyError: 
        print("There is no information about users birth year")
    except ValueError:
        print("There is no information about users birth year")
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    """ Selects the raw data of the dataframe and displays it 5 lines at a time"""
    i = 0
    raw = input("Would you like to see the first 5 lines of the raw data? (yes/no)").lower()
    pd.set_option('display.max_columns',200)
    while True:   
        if raw in ["no","yes"]:
           if raw == 'no':
              break
           while True:            
            if raw == 'no':
              break
            raw = input('Would you like to see 5 additional lines of the raw data? (yes/no)').lower()
            if raw in ["no","yes"]:
                try:
                    print(df.iloc[i:i+5])
                    i += 5
                except IndexError:
                    print("There is no more information to be shown")
              else:
                print("Please enter yes or no")        
        else:
             print("Please enter yes or no")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

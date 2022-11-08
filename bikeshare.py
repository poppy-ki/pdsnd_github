import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': r'C:\Users\pkennon\OneDrive - Brit Group Services\Documents\python test\chicago.csv',
              'new york': r'C:\Users\pkennon\OneDrive - Brit Group Services\Documents\python test\new_york_city.csv',
              'washington': r'C:\Users\pkennon\OneDrive - Brit Group Services\Documents\python test\washington.csv' }
    """This dictionary links the name of each city to the data for that city"""

city_options = ('new york', 'chicago', 'washington')
month_options = ('january', 'february', 'march', 'april', 'may', 'june', 'all')
day_options = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')

def get_filters():
    """ This function prompts the user to select a city, and filter on the month and day of their choice."""

    print('Hello! Let\'s explore some US bikeshare data!')

    city = input('\nWhat city would you like to look at? Chicago, New York, or Washington?\n')
    while city.lower() not in city_options:
        city = input('\nError: Please type either New York, Chicago, or Washington.\n')
    else:
        print('Great! The data will be filtered to only include'+' '+ city + ' ' + 'data.')

    month = input('\nWhat month would you like to look at? January, February, March, April, May, or June? If all months, type "all".\n')
    while month.lower() not in month_options:
        month = input('\nError: Please type either january, february, march, april, may, june, or all.\n')
    else:
        if month != 'all':
            print('Great! The data will be filtered to only include'+' '+ month + ' ' + 'data.')
        else:
            print('Okay! The data will not be filtered by month.')

    day = input('\nWhat day of the week would you like to look at? If all days, type "all". \n')   
    while day.lower() not in day_options:
        day = input('\nError: Please type either monday, tuesday, wednesday, thursday, friday, saturday, sunday, or all.\n')
    else:
        if day != 'all':
            print('Great! The data will be filtered to only include'+' '+ day + ' ' + 'data.')    
        else:
            print('Okay! The data will not be filtered by day.')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """ This function creates a dataframe based on the city, month, and day selected. """    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
        month_no = month_options.index(month) + 1 
        df = df[df['month'] == month_no]
   
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
 
    return df

def time_stats(df):
    """ This function gives statistics relating to start time. """   
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month:
    popular_month = df['month'].mode()[0]
    month_options_dic = {1 : 'January',
                            2: 'February',
                            3 : 'March',
                            4 : 'April',
                            5 : 'May',
                            6 : 'June'}

    print('The most popular start month is ' + month_options_dic[popular_month])
    
    # Display the most common day of week:
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular start day is ' + str(popular_day))
    
    # Display the most common start hour:
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour is ' + str(popular_hour) + ':00')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """ This function gives statistics relating to the start and end stations. """ 

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station:
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is ' + str(popular_start_station))
    
    # Display most commonly used end station:
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station is ' + str(popular_end_station))
    
    # Display most frequent combination of start station and end station trip:
    df['start_end'] = df['Start Station'] + ' and ' + df['End Station']
    popular_start_end = df['start_end'].mode()[0]
    print('The most popular combination of start and end station is ' + str(popular_start_end))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """ This function gives statistics relating to the trip duration. """   

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time:
    total_time = df['Trip Duration'].sum()
    print('The total travel time is ' + str(total_time) + ' seconds.')
    
    # Display mean travel time:
    mean_time = df['Trip Duration'].mean()
    print('The average travel time is ' + str(mean_time) + ' seconds.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """ This function gives statistics relating to the users of the bikes. """   

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types:
    user_types = df['User Type'].value_counts()
    print('\nUser types:\n')
    print(user_types)

    # Display counts of gender:
    try: 
        genders = df['Gender'].value_counts()
        print('\nGenders:\n')
        print(genders)
    except:
        print('Gender statistics cannot be displayed for this city.')

    # Display earliest, most recent, and most common year of birth:
    try:
        earliest_yob = df['Birth Year'].min()
        print('\nThe earliest birth year is ' + str(earliest_yob))
        latest_yob = df['Birth Year'].max()
        print('The latest birth year is ' + str(latest_yob))
        popular_yob = df['Birth Year'].mode()
        print('The most common birth year is ' + str(popular_yob))
    except:
        print('Birth year statistics cannot be displayed for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    """ This last function calls on the previous functions and brings them together, 
    prompting the user to choose city, month, and day, and then producing the relevant statistics """

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        rawdata = pd.read_csv(CITY_DATA[city])
        n = 5
        raw = input('\nWould you like to see some raw data?\n')
        if raw.lower() == 'yes':
            print('\nHere are the first 5 rows of raw data\n')
            print(rawdata[0:n])
        else:
            print('Ok!')

        raw2 = input('\nWould you like to see some more raw data?\n')

        while raw2.lower() == 'yes':
            n=n+5
            print('\nHere are the next 5 rows of raw data\n')
            print(rawdata[n-5:n])
            raw2 = input('\nWould you like to see some more raw data?\n')  
        else:
            print('Ok!')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

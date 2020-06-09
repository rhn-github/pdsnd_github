"""
This is the Python code for Richard's Bikeshare Project.
Please Note that the CSV files listed in CITY DATA were not pushed to the Remote Repository
"""

import time
import pandas as pd
import numpy as np
import calendar as ca

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #get user input for city (chicago, new york city, washington)
    citylist =("chicago", "new york city", "washington")
    citychoice = input("Would you like to see data for Chicago, New York City, or Washington?\n")
    if format(citychoice.lower()) in citylist:
        city = (format(citychoice.lower()))
    else:
        while format(citychoice.lower()) not in citylist:
            citychoice = input("Sorry, there is no data for {}, please choose from Chicago, New York City, or Washington.\n".format(citychoice.title()))
        city = (format(citychoice.lower()))

    # get user input for month (all, january, february, ... , june)
    monthlist =("all", "january", "february", "march", "april", "may", "june")
    monthchoice = input("For which month would you like to see data?\n Please enter the name of the month,\n or if you don't wish to see a particular month, please enter 'all':\n")
    if format(monthchoice.lower()) in monthlist:
        month = (format(monthchoice.lower()))
    else:
        while format(monthchoice.lower()) not in monthlist:
            monthchoice = input("Sorry, there is no data for the month {},\n please enter the name of another month,\n or if you don't wish to see a particular month, please enter 'all':\n".format(monthchoice.title()))
        month = (format(monthchoice.lower()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    daylist = ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    daychoice = input("For which day of the week would you like to see data?\n Please enter the name of the day you would like to see,\n or if you don't wish to see a particular day, please enter 'all':\n")
    if format(daychoice.lower()) in daylist:
        day = (format(daychoice.lower()))
    else:
        while format(daychoice.lower()) not in daylist:
            daychoice = input("Sorry, {} is not a valid entry,\n Please enter the name of the day you would like to see,\n or if you don't wish to see a particular day, please enter 'all':\n".format(daychoice))
        day = (format(daychoice.lower()))

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
    
    df = pd.read_csv(CITY_DATA[city])
         
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time']) 
         
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    start_time = time.time()

    # display the most common month
    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month
    # find the most popular month
    popular_month = df['month'].mode()[0]
    # determine if one month selected or all
    monnun = df['month'].nunique()
   
    # display the most common day of week
    # extract day from the Start Time column to create a day column
    df['day'] = df['Start Time'].dt.weekday
    # find the most popular day
    popular_day = df['day'].mode()[0]
    # determine if one day selected or all
    daynun = df['day'].nunique()
    
    # based on day and month determination select output text
    if monnun + daynun == 2:
        print('\nCalculating The Most Frequent Times of Travel\nfor ' + ca.day_name[popular_day] + 's in the month of ' + ca.month_name[popular_month] + '...\n')    
    elif monnun + daynun == 8:  
        print('\nCalculating The Most Frequent Times of Travel\nin the month of ' + ca.month_name[popular_month] + '...\n')
        print('Most Popular Day:', ca.day_name[popular_day])
    elif monnun + daynun == 7:  
        print('\nCalculating The Most Frequent Times of Travel for ' + ca.day_name[popular_day] + 's...\n')
        print('Most Popular Month:', ca.month_name[popular_month])
    else:   
        print('\nCalculating The Most Frequent Times of Travel...\n')
        print('Most Popular Month:', ca.month_name[popular_month])
        print('Most Popular Day:', ca.day_name[popular_day])   
     
    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', str(popular_hour) + '00 to ' + str(popular_hour) +'59.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start)
    
    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = (df['trip']).mode()[0]
    print('Most Popular Trip:', popular_trip)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total travel time in selected period:', int(total_duration//3600), 'hours', int(int(total_duration%3600)//60), 'minutes', int(total_duration%60), 'seconds')
    
    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('Average travel time in selected period:', int(mean_duration//60), 'minutes ', int(mean_duration%60), 'seconds')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Summary of user types:')
    print(user_types)
    
    # Display counts of gender
    print('\nSummary of user gender:')
    try:
        gender = df['Gender'].value_counts()
        print(gender)
    except KeyError:
        print('No Gendar Data available for this City')

    #Display earliest, most recent, and most common year of birth
    print('\nSummary of Birth Years:')
    try:
        earliest = df['Birth Year'].min()
        print('Earliest Year of Birth:', int(earliest))
        latest = df['Birth Year'].max()
        print('Most Recent Year of Birth:', int(latest))
        common = df['Birth Year'].mode()[0]
        print('Most Common Year of Birth:', int(common))
    except KeyError:
        print('No Birth Year Data available for this City')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw(df):
    """Displays the raw data for the selection city / month / day."""
    
    seeraw = input("Would you like to see the raw data for this selection?\nEnter yes to see the Raw data, or no (or any other key) to skip this:\n")
    
    if seeraw == "yes":
        print('Here are the first 5 entries:')
        a = 0
        b = 5
        while True:
            start_time = time.time()
            print(df[a:b])
            a += 5
            b += 5
            print("\nThis took %s seconds.\n" % (time.time() - start_time))
            seenext = input('Would you like to see the next 5 entries?\nEnter yes to continue with the next 5 entries, or no (or any other key) to stop:\n')
            if seenext.lower() != 'yes':
                break
            else:
                print('Here are the next 5 entries:')
    print('-'*40)  

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw(df)

        restart = input('\nWould you like to restart?\nEnter yes to restart, or no (or any other key) to quit:\n')
        if restart.lower() != 'yes':
            break
        else:
            print('-'*40 + '\n')  


if __name__ == "__main__":
	main()

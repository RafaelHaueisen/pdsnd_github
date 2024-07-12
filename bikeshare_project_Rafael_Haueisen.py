#!/usr/bin/env python
# coding: utf-8

# In[8]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_input(prompt, options):
    """
    Handles user input and validates it against a set of options.

    Args:
        prompt (str): The input prompt for the user.
        options (tuple): The valid input options.

    Returns:
        (str): Validated user input.
    """
    user_input = input(prompt).lower()
    while user_input not in options:
        user_input = input(f"Invalid input. Please choose from {', '.join(options)}: ").lower()
    return user_input

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ('chicago', 'new york city', 'washington')
    months = ('january', 'february', 'march', 'april', 'may', 'june', 'all')
    days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all')
    
    city = get_input(f"Which city do you require data from? Please choose from {', '.join(cities)}: ", cities)
    month = get_input(f"Which month do you require data from? Please choose from {', '.join(months)}: ", months)
    day = get_input(f"Which day of week do you require data from? Please choose from {', '.join(days)}: ", days)

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
    global CITY_DATA
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # capitalize the first letter to match the format of .dt.day_name()
        day = day.title()
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = {1: 'January', 2: 'Febuary', 3: 'March',
              4: 'April', 5: 'May', 6: 'June'}
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # if the user didn't filter by month it will print
    if len(df['month'].unique()) != 1:
        print(f'The most common month is {months[df["month"].mode()[0]]}')
    else:
        print(f'You chose the month {months[df["month"].mode()[0]]}')

    # display the most common day of week
    # if the user didn't filter by dow it will print
    if len(df['day_of_week'].unique()) != 1:
        print(f'The most common day of week is {df["day_of_week"].mode()[0]}')
    else:
        print(f'You chose the day {df["day_of_week"].mode()[0]}')
        
    # display the most common start hour
    print(f'The most common start hour is {df["Start Time"].dt.hour.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f'The most commonly used start station is {df["Start Station"].mode()[0]}')

    # display most commonly used end station
    print(f'The most commonly used end station is {df["End Station"].mode()[0]}')

    # display most frequent combination of start station and end station trip
    station_combination = df['Start Station'] + '//' + df['End Station']
    print(f"The most common trip is: {station_combination.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f'The total travel time is: {df["Trip Duration"].sum()} seconds')

    # display mean travel time
    print(f'The mean travel time is: {df["Trip Duration"].mean()} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The quantity and types of user are: \n')
    print(df["User Type"].value_counts())

    # Check if I have acces to gender and birth dates
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The quantity and types of user are: \n')
    print(df["User Type"].value_counts())

    # Check if I have acces to gender and birth dates
    if city != 'washington':
        # Display counts of gender
        print('The gender types an count is: \n')
        print(df["Gender"].value_counts())
        
        # Display earliest, most recent, and most common year of birth
        print(f'The earliest year of birth is: {df["Birth Year"].min()}')
        print(f'The most recent year of birth is: {df["Birth Year"].max()}')
        print(f'The most common year of birth is: {df["Birth Year"].mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data_display(df):
    """Checks to see if the user wnats to view some raw data"""
    
    raw_data = str(input('\nWould you like to see the first 5 rows of raw data? ' \
                             'Enter yes or no.\n')).lower()
    # User input
    while raw_data != 'no' and raw_data != 'yes':
        raw_data = str(input('Please enter yes or no only! '))
    
    # Printing raw data
    i = 0
    while raw_data == 'yes':
        print(df.iloc[5*i:5*i+5])
        i += 1
        raw_data = str(input('\nWould you like to see 5 more? Enter yes or no.\n')).lower()
        while raw_data != 'no' and raw_data != 'yes':
            raw_data = str(input('Please enter yes or no only! '))
    
    print('-'*40)
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data_display(df)
            

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


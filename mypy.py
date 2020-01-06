import time
import pandas as pd
import numpy as np
import calendar
import datetime

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
    
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    while True:
        city = input("\nWould you like to see data for Chicago, New York City or Washington?").lower()
        if city in CITY_DATA.keys(): 
                print("\nLooks like you want to hear about {}!".format(city)) 
                break
        else:
                print("\nThat is not a valid city! Please try again.")
                
    
    while True:
        month = input("\nWhich month would you like to filter by? All, January, February, March, April, May, June?").lower()
        if month in months:
            print("\nFiltering by {} month.".format(month).title())
            break
        if month == 'all':
            print('\nFiltering by {} months.'.format(month))
            break
        else:
            print("\nThat is not a valid month! Please try again.")

    
    while True:
        day = input("\nWhich day would you like to filter by? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?").lower()
        if day in days:
            print("Filtering by {}.".format(day).title())
            break
        if day == 'all':
            print('Filtering by {} days.'.format(day))
            break
        else:
            print("\nInvalid day input! Please try again.")


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
    df=pd.read_csv(CITY_DATA[city])
      
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


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
    """Displays statistics on the most frequent times of travel including the month, day of the week and starting hour."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    
    
    most_common_month = df['month'].mode()[0]
   
    print('Most common month:',calendar.month_name[most_common_month]) 
    
    
    
    most_common_dow = df['day_of_week'].mode()[0]
    print('Most common day of week:', most_common_dow)

    
    most_common_start_hour = df['hour'].mode()[0]
    print('Most common start hour:', datetime.time(most_common_start_hour))


    
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular start and stop stations and the most common route."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
   
    
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', start_station)
    
    end_station = df['End Station'].mode()[0]
    print('\nMost commonly used end station:', end_station)

    
    combination_station = (df['Start Station'] + " AND " + df['End Station']).mode()[0]
    print('\nMost frequent combination of start and stop stations:', combination_station)

    
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is {} days.'.format(round(total_travel_time/60/60/24),2))

    
    mean_travel_time = df['Trip Duration'].mean()
    print ('\nAverage travel time is {} minutes.'.format(round(mean_travel_time/60),2))

    
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users including gender and date of birth statistics."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    user_types = (df['User Type'].value_counts()).to_string()
    total_users = df['User Type'].count()
    nan_user = df['User Type'].isnull().sum().sum()
    
    print('\nTotal number of users:', total_users)
    
    print('\nTypes of user:\n', user_types)
    
    print('\nUser-type data not available for {} users.'.format(nan_user))
    
    # Display counts of gender
    if 'Gender' in df:
        gender = (df['Gender'].value_counts()).to_string()
        
        nan_gender = df['Gender'].isnull().sum().sum()
        
        print('\nGender information of users:\n',gender)
        
        print('\nGender data not available for {} users.'.format(nan_gender))
    
    else:
        print('\nGender data not available')
    
    
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        print('\nYear of birth for oldest user:', earliest_year)
    
        latest_year = int(df['Birth Year'].max())
        print('\nYear of birth for youngest user:', latest_year)
        
        common_year = int(df['Birth Year'].mode()[0])
        print('\nMost common year of birth for users:', common_year)
        
        nan_birth_year = df['Birth Year'].isnull().sum().sum()
        print('\nBirth year data not available for {} users.'.format(nan_birth_year))
  
    else:
         print('\nBirth Year data not available')
        


    
    print('-'*40)

    
def raw_data(df):
    """Displays raw Bikeshare data in increments of five trips at a time."""
    display_raw_input = input("\nWould you like to see individual raw data? Enter 'yes' or 'no'\n").strip().lower()
    if display_raw_input in ("yes", "y"):
        i = 0

        while True:

                print(df.iloc[i:i+5, :])
                i += 5

                show_next_five_input = input("\nWould you like to see the next 5 rows? Enter 'yes' or 'no'\n").strip().lower()
                if show_next_five_input not in ("yes", "y"):
                    break 

    if display_raw_input in ("no","n"):
        pass

            

    else:
        print("\nSorry, I'm not sure if you wanted to see more data or not. Let's try again.")
        return raw_data(df) 
    
      

            
              
 
            

      

def main():
    while True:
        
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
    
       

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

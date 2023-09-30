import time
import pandas as pd
import numpy as np
import calendar  #use this co convert integer back to day of week

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#initialize dictionaries to go between text and number values
month_values = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november':11, 'december':12}
day_values = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4}

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
    invalid = True
    while invalid:
        city = input('Please enter either chicago, new york city, or washington: ')
        city = city.lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print('Invalid input')
        else:
            invalid = False

    # get user input for month (all, january, february, ... , june)
    invalid = True
    while invalid:
        month = input('Please enter a month january - december or "all": ')
        month = month.lower()
        if month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']:
            print('Invalid input')
        else:
            invalid = False

    # get user input for day of week (all, monday, tuesday, ... sunday)
    invalid = True
    while invalid:
        day = input('Please enter a day of the week monday-friday or "all": ')
        day = day.lower()
        if day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            print('Invalid input')
        else:
            invalid = False

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
    #convert new york city to new_york_city
    df = pd.read_csv('{}.csv'.format(city.replace(' ', '_')))
    # convert start time to date_time for ease of filtering
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #apply filters

    # if we have a month filter
    if month != 'all':
        df = df[df['Start Time'].dt.month == month_values[month]]
    # if we have day filter 
    if day != 'all':
        df = df[df['Start Time'].dt.dayofweek == day_values[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month of travel is: {}'.format(calendar.month_name[df['Start Time'].dt.month.mode()[0]]))

    # display the most common day of week
    print('Most common day of week is: {}'.format(calendar.day_name[df['Start Time'].dt.dayofweek.mode()[0]]))

    # display the most common start hour
    print('Most common start hour is: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station is: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most common end station is: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('Most common combination of start and end stations is: {}'.format((df['Start Station'] + ' to ' + df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is: {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Average travel time is: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Number of subscribers: {}'.format(df['User Type'].value_counts()['Subscriber']))
    print('Number of customers: {}'.format(df['User Type'].value_counts()['Customer']))

    # Display counts of gender
    print('Number of males: {}'.format(df['Gender'].value_counts()['Male']))
    print('Number of females: {}'.format(df['Gender'].value_counts()['Female']))
    print('Number of non-binary: {}'.format(df['Gender'].isna().sum()))

    # Display earliest, most recent, and most common year of birth
    print('Earliest birth year: {}'.format(df['Birth Year'].min()))
    print('Most recent birth year: {}'.format(df['Birth Year'].max()))
    print('Most common birth year: {}'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def view_raw_data(df):
    # ask if raw data wants to be seen
    see_data = True
    #initial values that will be updated in while loop
    end_row = 0
    while see_data:
        if end_row == 0:
            user_ans = input('Would you like to see the raw data? (Yes/No): ')
        else:
            user_ans = input('Would you like to see more raw data? (Yes/No): ')
        if user_ans.lower() not in ['yes', 'no']:
            print('Invalid Input')
        elif user_ans.lower() == 'no':
            see_data = False
        else:
            # we print until we printed 5 lines
            counter = 0
            while counter < 5:
                if end_row == df.shape[0]:
                    print('No more data to show')
                    see_data = False
                    break
                else:
                    print(df.iloc[end_row])
                    end_row += 1
                    counter += 1


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

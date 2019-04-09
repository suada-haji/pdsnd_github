import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
periods = ['month', 'day', 'none', 'both']


def get_city():
    city_request = '\nWould you like to see data for Chicago, New York City or Washington? \n'
    city = input(city_request).lower()
    while city not in CITY_DATA:
        city = input(city_request).lower()
    return city


def get_period():
    period_request = '\nWould you like to filter data by month, day, both or not at all? Type "none" for no time ' \
                     'filter.\n'
    period = input(period_request).lower()
    while period not in periods:
        period = input(period_request).lower()
    return period


def get_month():
    month_input = '\nWhich month? January, February, March, April, May, or June?\n'
    month = input(month_input).lower()
    while month not in months:
        month = input(month_input).lower()
    return month


def get_day():
    day_input = '\nWhich day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \n'
    day = input(day_input).lower()
    while day not in days:
        day = input(day_input).lower()
    return day

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
    city = get_city()

    filter_option = get_period()

    month = ''
    day = ''
    # get user input for month (all, january, february, ... , june)
    if filter_option == 'month':
        month = get_month()
        day = 'none'
    # get user input for day of week (monday, tuesday, ... sunday)
    elif filter_option == 'day':
        day = get_day()
        month = 'none'
    # get user input for none
    elif filter_option == 'none':
        day = 'none'
        month = 'none'
    # get user input for both month and day
    elif filter_option == 'both':
        month = get_month()
        day = get_day()

    print('-' * 40)
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
    if month != 'none':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'none':
        # filter by day of week to create the new dataframe
        day = day.title()
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    month = df['Start Time'].dt.month
    total_months = month.value_counts().count()
    if total_months > 1:
        most_common_month = months[month.mode().loc[0] - 1].title()
        print ('\nMost Common Month: {}'.format(most_common_month))

    # display the most common day of week
    day_of_week = df['Start Time'].dt.weekday_name
    total_days = day_of_week.value_counts().count()
    if total_days > 1:
        most_common_day = day_of_week.mode().loc[0]
        print ('\nMost Common Day of the Week: {}'.format(most_common_day))

    # display the most common start hour
    hour = df['Start Time'].dt.hour
    most_common_hour = hour.mode().loc[0]
    print ('\nMost Common Hour: {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    popular_station = '\nMost Popular {}: {}'

    # display most commonly used start station
    print (popular_station.format('Start Station', df['Start Station'].mode().loc[0]))

    # display most commonly used end station
    print (popular_station.format('End Station', df['End Station'].mode().loc[0]))

    # display most frequent combination of start station and end station trip
    df['frequent_combination'] = df['Start Station'] + " to " + df['End Station']
    print('\nMost Frequent Trip is from {}'.format(df['frequent_combination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    trip_duration = '{} Trip Duration: {}'
    duration_column = df['Trip Duration']

    # display total travel time
    total_trip_duration = duration_column.sum()
    time_string = convert_duration(total_trip_duration)
    print(trip_duration.format('Total', time_string))

    # display mean travel time
    mean_trip_duration = duration_column.mean()
    time_string = convert_duration(mean_trip_duration)
    print(trip_duration.format('Mean', time_string))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def convert_duration(total_trip_duration):
    # break down duration --> https://stackoverflow.com/a/775075
    minutes, seconds = divmod(total_trip_duration, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    durations = [('days', days), ('hours', hours), ('minutes', minutes), ('seconds', seconds)]
    time_string = ', '.join('{} {}'.format(value, name)
                            for name, value in durations
                            if value)
    return time_string


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('What\'s the breakdown of users?')
    print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df:
        print('\nWhat\'s the breakdown of gender?')
        print(df['Gender'].value_counts())
        print('')
    else:
        print('This city\'s data does not have a Gender column')

    # Display earliest, most recent, and most common year of birth
    birth_year = '{} Year: {}'
    if 'Birth Year' in df:
        print('Data about Year of Birth')
        print(birth_year.format('Earliest', df['Birth Year'].min().astype(int)))
        print(birth_year.format('Recent', df['Birth Year'].max().astype(int)))
        print(birth_year.format('Common', df['Birth Year'].mode()[0].astype(int)))
    else:
        print('No birth year data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

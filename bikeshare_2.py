import time
import pandas as pd
import numpy as np

pd.set_option('precision', 0)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.max.rows', 1000)
pd.set_option('display.width', 1000)

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}


# note to access the key & value in dictionary you need to use .items() method


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike share data!')
    count = 0
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('What city, month, and day would you like to analyze?\nType Chicago,'
                 ' New York City, or Washington: ').title()
    while city != 'Chicago' and city != 'New York City' and city != 'Washington':
        count = count + 1
        print('Incorrect city name\nNumber of failed attempt number is', count)
        city = input('Please re-try to type the correct city again: ').title()

    # get user input for month (all, january, february, ... , june)
    month = input('Which month (Jan, Feb, Mar, Apr, May, or Jun) would like to see?\n'
                  'You could type "all" to get all months: ').title()
    while month != 'All' and month != 'Jan' and month != 'Feb' and month != 'Mar' and month != 'Apr' and month != 'May' and month != 'Jun' and month != 'All':
        print('The month your typed cannot be found')
        month = input('Please type the correct month: ').title()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Type the day of the week (example, Sunday) to filter or type all: ').title()
    while day != 'All' and day != 'Monday' and day != 'Tuesday' and day != 'Wednesday' and day != 'Thursday' and day != 'Friday' and day != 'Saturday' and day != 'Sunday':
        print('incorrect day')
        day = input('Enter the correct day: ').title()
    print('\nYou have selected:\n{} as a city\n{} as a month\n{} as the day of week '.format(city, month, day))
    print('-' * 40)
    return city, month, day


# print('Testing the input of get_filters function \n', get_filters())


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])  # will pass city as an argument from the load file

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # df['day_of_week'] = df['Start Time'].dt.weekday_name  # this was Udacity solution
    # Below is alternative of above which works just fine. URL to the solution
    # https://stackoverflow.com/questions/60214194/error-in-reading-stock-data-datetimeproperties-object-has-no-attribute-week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    """
     we could extract hour, minute, or second like what we did with practice #2:
     df['hour'] = df['Start Time'].dt.hour
     df['minute'] = df['Start Time'].dt.minute
     df['second'] = df['Start Time'].dt.second
     """

    # filter by month if applicable
    # now we're talking about the second argument which is month
    if month != 'All':  # all here can be changed to anything as log as you pass the same in the function
        # use the index of the months list to get the corresponding int
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        month = months.index(month) + 1  # this +1 so january becomes 1 instead of 0, Feb becomes 2..
        # but there is more to it. if we don't do +1 then january can't be filtered since there's no month=0 in
        # Chicago data for example.

        # filter by month to create the new dataframe
        df = df[df['month'] == month]  # column month is = month which the index of the months provided by end user

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        # df = df[df['day_of_week'] == day]
    # print('printing raw data of first 5 rows\n', df.head(5))

    return df


# print('printing load_data function \n', load_data('Chicago', 'Feb', 'Sunday').head())


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is {}'.format(df['month'].mode().to_string(index=False)))

    # print('printing high level statistic ', df.describe())
    # print('displaying the max record: \n', df.max())
    # print('displaying the mean record: \n', df.min())
    # print('displaying the Correlation record: \n', df.corr())
    # print('printing the sum of user type % sum of trip dur\n', df.groupby(['User Type', 'month'])['Trip Duration'].sum())

    # display the most common day of week
    print('The most common day of the week is {}'.format(df['day_of_week'].mode().to_string(index=False)))

    # print('The most common day of the week', df['day_of_week'].mode().rename(index={0: 'is'}))
    # display the most common start hour  hour
    # using .to_string method to hide the index
    print('The most common hour is {}'.format(df['hour'].mode().to_string(index=False)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is {}'.format(df['Start Station'].mode().to_string(index=False)))

    # display most commonly used end station
    print('The most commonly end Station is {}'.format(df['End Station'].mode().to_string(index=False)))

    # display most frequent combination of start station and end station trip
    print('The most commonly frequent combination of start station and end station trip is\n {}'.format(
        df[['Start Station', 'End Station']].mode().to_string(index=False)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is {} '.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The mean of travel time is {} '.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('the counts of user type as following:\n{}'.format(user_types))

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('Below is the count of gender:\n{}'.format(gender))

    except KeyError:
        print('Washington city has no gender data')  # hard coded Washington since it doesn't have this date

    # Display earliest, most recent, and most common year of birth
    # remember Washington doesn't have Birth Year and Gender. try and except the error
    try:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        common_year = df['Birth Year'].mode().to_string(index=False)
        print('The earliest birth year is {}\nThe most recent birth year is {}'
              '\nFinally the most common year of birth is {}'
              ''.format(earliest.astype(int), most_recent.astype(int), common_year))
    except KeyError:
        print('Washington city has no birth year data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    view_data = input('Would like to see raw data? type Yes or No').lower()
    start_loc = 0
    end_loc = 5
    while view_data != 'yes' and view_data != 'no':
        print("You need to type only 'yes' or 'no' ")
        view_data = input('Would like to see raw data? type Yes or No').lower()

    while view_data == 'yes':
        print(df.iloc[start_loc: end_loc, :])
        start_loc = start_loc + 5
        end_loc = end_loc + 5
        view_data = input('Do you wish to see the next 5 rows?').lower()

    # print('printing raw data of first 5 rows\n', df.head(5))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

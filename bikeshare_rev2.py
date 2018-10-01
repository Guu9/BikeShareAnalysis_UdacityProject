
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta


# In[2]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new york city.csv',
              'washington': 'washington.csv' }


# In[3]:


cities = ['Chicago', 'New York City', 'Washington']
months = ['January', 'February', 'March', 'April', 'May', 'June']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    


# In[4]:


def get_data():

    print('Hello! Let\'s explore some US bikeshare data!\n')

    
    while 1: 
        city = input("Q1: What city\'s data would you like to see?\n  ({}, {}, {})---> ".format(*cities))
        if city.title() in cities:
            break
        else:
            print('***** Oops! That\'s a invalid city, please type one of sample cities. *****\n')
            continue
    while 1:
        month = input("Q2: Which month?\n  ({}, {}, {}, {}, {}, {}, or All)---> ".format(*months))
        if month.lower() == 'all' or month.title() in months:
            break
        else:
            print('***** Oops! That\'s out of range, please type one of sample month.*****\n')
            continue
    while 1:
        day = input("Q3: What day of week, or all?\n  ({}, {}, {}, {}, {}, {}, {}, or All)---> ".format(*days))
        if day.lower() == 'all' or day.title() in days:
            break
        else:
            print('***** Oops! That\'s out of range, please type one of days.*****\n')
            continue

    return city.lower(), month, day


# In[5]:


def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    
    print(months)
    if month.lower() != 'all':
        month_int = months.index(month.title()) + 1
        df = df[df['month'] == month_int ]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    print("\n"*2)
    print("\033[1mYou wanted to see the data of...\033[0;0m")
    print("\033[1m{}\033[0;0m".format('-'*50))
    print("city: \033[1m{}\033[0;0m / month: \033[1m{}\033[0;0m / days: \033[1m{}\033[0;0m\n"
          .format(city.title(), month.title(), day.title()))
    
    return df


# In[6]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    popular_month_int = df['month'].mode()[0]
    popular_month = months[popular_month_int-1]
    popular_day = df['day_of_week'].mode()[0]
    popular_start_hr = df['hour'].mode()[0]

    if len(df['month'].value_counts())>1 and len(df['day_of_week'].value_counts())==1:
        print("- The most popular month of {}s | \033[1m{}\033[0;0m".format(popular_day, popular_month.title()))
    
    elif len(df['month'].value_counts())==1 and len(df['day_of_week'].value_counts())>1:
        print("- The most popular day of {} | \033[1m{}\033[0;0m".format(popular_month.title(), popular_day))
    
    elif len(df['month'].value_counts())>1 and len(df['day_of_week'].value_counts())>1:
        print("- The most popular month | \033[1m{}\033[0;0m".format(popular_month.title()))
        print("- The most popular day of the week | \033[1m{}\033[0;0m".format(popular_day))

    print("- The most popular hour of the day to start the travels | \033[1m{}h\033[0;0m.".format(popular_start_hr))


# In[7]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    freq_start_stn = df['Start Station'].mode()[0]
    freq_end_stn = df['End Station'].mode()[0]

    df['Route'] = df['Start Station'] + ' -> ' + df['End Station']
    freq_route = df['Route'].mode()[0]
    
    print("- The most popular start station | \033[1m{}\033[0;0m".format(freq_start_stn))
    print("- The most popular end station | \033[1m{}\033[0;0m".format(freq_end_stn))
    print("- The most popular route | \033[1m{}\033[0;0m".format(freq_route))
    


# In[8]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    # Display total travel time
    ttl_time = sec_transform(df['Trip Duration'].sum())
    print("- Total travel time | \033[1m{}days, {}h {}m {}s\033[0;0m"
          .format(ttl_time['d'], ttl_time['h'], ttl_time['m'], ttl_time['s']))
    
    # Display average travel time
    mean_time = sec_transform(df['Trip Duration'].mean())
          
    if mean_time['d'] != 0:
        print("- Average travel time | \033[1m{}days, {}h {}m {}s\033[0;0m" 
              .format(mean_time['d'], mean_time['h'], mean_time['m'], mean_time['s']))
    elif mean_time['h'] != 0:
        print("- Average travel time | \033[1m{}h {}m {}s\033[0;0m"      
              .format(mean_time['h'], mean_time['m'], mean_time['s']))
    elif mean_time['m'] != 0:
        print("- Average travel time | \033[1m{}m {}s\033[0;0m"      
              .format(mean_time['m'], mean_time['s']))
    else:
        print("- Average travel time | \033[1m{}s\033[0;0m"      
              .format(mean_time['s']))
    


# In[9]:


def sec_transform(ttl_secs):

    # days, and seconds after taking out the number of days
    ttl_d = ttl_secs // 86400
    rsd_secs_aft_d = ttl_secs % 86400
    
    # hours, and seconds after taking out the number of hours
    ttl_h = rsd_secs_aft_d // 3600
    rsd_secs_aft_h = rsd_secs_aft_d % 3600
    
    # minutes, and final seconds
    ttl_m = rsd_secs_aft_h // 60
    fnl_s =  rsd_secs_aft_h % 60
    
    ttl_time_df = {'d':ttl_d, 'h':ttl_h, 'm':ttl_m, 's':fnl_s}
    
    return(ttl_time_df)
    


# In[10]:


def user_type_stats(df, city):
    """Displays statistics on bikeshare users."""

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    ttl_users = df['User Type'].count()
    
    print("- Total users | \033[1m{}\033[0;0m".format(ttl_users))
    print("- {} | \033[1m{}\033[0;0m".format(user_type.index[0], user_type[0]))
    print("- {} | \033[1m{}\033[0;0m".format(user_type.index[1], user_type[1]))
          
    
    if city.lower() != 'washington':
        # output type: series
        gndr_type = df['Gender'].value_counts()
        #print("{}: {} vs {}: {}".format(gndr_type.index[0], gndr_type[0], gndr_type.index[1], gndr_type[1]))
        print("\n- {} | \033[1m{}\033[0;0m".format(gndr_type.index[0], gndr_type[0]))
        print("- {} | \033[1m{}\033[0;0m".format(gndr_type.index[1], gndr_type[1]))
    
        # output type: tuple
        age_range = []
        age_range.append(int(df['Birth Year'].mode()[0]))
        age_range.append(int(df['Birth Year'].min()))
        age_range.append(int(df['Birth Year'].max()))
        
        print("\n- The most common year of birth | \033[1m{}\033[0;0m\n- The earliest year | \033[1m{}\033[0;0m\n- The youngest year | \033[1m{}\033[0;0m"
              .format(*age_range))


# In[11]:


def main():
        
        
    while True:
        
        
        city, month, day = get_data()
        
        df = load_data(city, month, day)
        
        #1. Time Analytics
        print("\n\033[1m1. Time Analytics\033[0;0m")
        start_sec = time.time()
        time_stats(df)
        end_sec = time.time()
        print("\n(That took {} seconds)\n\n".format(end_sec - start_sec))
        
        #2. Travel Duration Analytics
        print("\n\033[1m2. Travel Duration Analytics\033[0;0m")
        start_sec = time.time()
        trip_duration_stats(df)
        end_sec = time.time()
        print("\n(That took {} seconds)\n\n".format(end_sec - start_sec))
        
        #3. Station Analytics
        print("\n\033[1m3. Station Analytics\033[0;0m")
        start_sec = time.time()
        station_stats(df)
        end_sec = time.time()
        print("\n(That took {} seconds)\n\n".format(end_sec - start_sec))
        
        
        #4. User Analytics
        print("\n\033[1m4. User Analytics\033[0;0m")
        start_sec = time.time()
        user_type_stats(df, city)
        end_sec = time.time()
        print("\n(That took {} seconds)\n\n".format(end_sec - start_sec))
             
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


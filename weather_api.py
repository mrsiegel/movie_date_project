import requests
import json
import hide
import sqlite3
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os

def read_cache(CACHE_FNAME):
    try:
        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
        cache_contents = cache_file.read()  # If it's there, get it into a string
        CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
        cache_file.close() # Close the file, we're good, we got the data in a dictionary.
    except:
        CACHE_DICTION = {}
    
    return CACHE_DICTION

def write_cache(cache_file, cache_dict):
    dump_json = json.dumps(cache_dict)
    file_name = open(cache_file, 'w')
    file_name.write(dump_json)
    file_name.close()

user_latitude = input('What is the latitude?')
user_longitude = input('What is the longitude?')

def openweatherRequest(user_latitude, user_longitude):
    # user_latitude = input('What is the latitude?')
    # user_longitude = input('What is the longitude?')
    # latitude = 30.26
    # longitude = -97.73
    base_url = 'http://api.openweathermap.org/data/2.5/find?lat={}&lon={}&cnt=20&APPID={}'
    my_key = hide.openWeather_api_key
    request_url = base_url.format(user_latitude, user_longitude, my_key)
    # request = requests.get(request_url)
    # openWeather_text = json.loads(request.text)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "city_weather.json"
    CACHE_DICTION  = read_cache(CACHE_FNAME)

    if request_url in CACHE_DICTION:
        print('Using cache for latitude and longitude')
        return CACHE_DICTION[request_url]
    else:
        print('Fetching for latitude and longitude')
        try:
            results = requests.get(request_url)
            data = results.text
            CACHE_DICTION[request_url] = json.loads(data)
            write_cache(CACHE_FNAME, CACHE_DICTION)
        except:
            print('Exception')
            return None
    return CACHE_DICTION[request_url]
# print(openweatherRequest())

def get_city_weather():
    city_info = openweatherRequest(user_latitude, user_longitude)
    print(city_info)
    weather_dict = {}
    new_city_info = city_info['list']
    for item in new_city_info:
        city_name = item['name']
        weather_dict[city_name] = item['main']
    return weather_dict
# print(get_city_weather())

dbname = 'final_project.db'
def openweather_database(dbname):
    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
    except:
        print('Could not connect')

    statement = '''
        CREATE TABLE IF NOT EXISTS 'Weather' (
            city TEXT,
            temp INTEGER, 
            temp_max INTEGER, 
            temp_min INTEGER, 
            humidity INTEGER)
            '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE IF NOT EXISTS 'Cities' (
            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT)
            '''
    cur.execute(statement)
    conn.commit()
    conn.close()



def insert_info_data():
    weather_info= get_city_weather()
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    for weather in weather_info:
        city_=weather
        temp_=weather_info[weather]['temp']
        temp_max_ = weather_info[weather]['temp_max']
        temp_min_ = weather_info[weather]['temp_min']
        humidity_ = weather_info[weather]['humidity']
        cur.execute('INSERT OR IGNORE INTO Weather (city, temp, temp_max, temp_min, humidity) VALUES (?, ?, ?, ?, ?)', (city_, temp_, temp_max_, temp_min_, humidity_))
    conn.commit()
    for city in weather_info:
        city_ = city
        cur.execute('INSERT OR IGNORE INTO Cities (city_id, city) VALUES (?, ?)', (None, city_))
    conn.commit()
    statement = '''
        SELECT * FROM Weather
        JOIN Cities
        ON Cities.city = Weather.city
            '''
    cur.execute(statement)
    conn.commit()


    cur.execute('SELECT humidity FROM Weather')
    total = 0
    count = 0
    for humid in cur:
        total += humid[0]
        count += 1
    average_humidity = (total/count)
    print(average_humidity)

    cur.execute('SELECT city FROM Cities')
    num_words = 0
    for city_name in cur:
        print(city_name)
        split_name = city_name[0].split() 
        print(split_name)
        if len(split_name) > 1:
                num_words += 1
    print(num_words)
    
    cur.execute('SELECT city FROM Weather')
    city_list = []
    for city_temp_name in cur:
        city_list.append(city_temp_name[0])
        
    cur.execute('SELECT temp FROM Weather')
    temps_list = []
    for temperature in cur:
        celsius = temperature[0] - 273.15
        temps_list.append(celsius)
        
    data = {}
    count1 = 0
    for x in city_list:
        if x not in data:
            data[x] = temps_list[count1]
        count1 += 1 
    
    plt.bar(city_list[0:10], temps_list[0:10], align='center', color = ['magenta', 'indigo', 'blue', 'teal', 'aquamarine', 'lightpink', 'orchid', 'skyblue', 'slateblue', 'cornflowerblue'])
    plt.ylabel('Temperature (Celsius)')
    plt.xlabel('City Name')
    plt.title('Temperature in Cities')
    plt.xticks(rotation=30)
    plt.savefig('Temperature_Plot.png')
    plt.show() 



    cur.execute('SELECT city FROM Weather')
    city_list = []
    for city_temp_name in cur:
        city_list.append(city_temp_name[0])
        
    cur.execute('SELECT humidity FROM Weather')
    humidity_list = []
    for humidity_num in cur:
        humidity_list.append(humidity_num[0])
        
    data = {}
    count2 = 0
    for x in city_list:
        if x not in data:
            data[x] = humidity_list[count2]
        count2 += 1 
    
    plt.bar(city_list[0:10], humidity_list[0:10], align='center', color = ['navy', 'mediumblue', 'darkslateblue', 'mediumpurple', 'indigo', 'mediumorchid', 'thistle', 'plum', 'darkmagenta', 'purple'])
    plt.ylabel('Humidity')
    plt.xlabel('City Name')
    plt.title('Humidity in Cities')
    plt.xticks(rotation=30)
    plt.savefig('Humidity_Plot.png')
    plt.show() 
    
openweather_database(dbname)
insert_info_data()






    
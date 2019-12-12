import requests
import json
import hide
import sqlite3
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os
import numpy as np

def read_cache(CACHE_FNAME):
    try:
        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") 
        cache_contents = cache_file.read()  
        CACHE_DICTION = json.loads(cache_contents) 
        cache_file.close() 
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
    base_url = 'http://api.openweathermap.org/data/2.5/find?lat={}&lon={}&cnt=20&APPID={}'
    my_key = hide.openWeather_api_key
    request_url = base_url.format(user_latitude, user_longitude, my_key)

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

def get_city_weather():
    city_info = openweatherRequest(user_latitude, user_longitude)
    print(city_info)
    weather_dict = {}
    new_city_info = city_info['list']
    for item in new_city_info:
        city_name = item['name']
        weather_dict[city_name] = item['main']
    return weather_dict

dbname = 'final_project.sqlite'
def openweather_database(dbname):
    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
    except:
        print('Could not connect')

    statement = '''
        CREATE TABLE IF NOT EXISTS 'Weather' (
            city TEXT PRIMARY KEY UNIQUE,
            temp INTEGER, 
            temp_max INTEGER, 
            temp_min INTEGER)
            '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE IF NOT EXISTS 'Cities' (
            city_id INTEGER PRIMARY KEY UNIQUE,
            city TEXT UNIQUE,
            humidity INTEGER)
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
        cur.execute('INSERT OR IGNORE INTO Weather (city, temp, temp_max, temp_min) VALUES (?, ?, ?, ?)', (city_, temp_, temp_max_, temp_min_))
    conn.commit()
    for city in weather_info:
        city_ = city
        humidity_ = weather_info[weather]['humidity']
        cur.execute('INSERT OR IGNORE INTO Cities (city_id, city, humidity) VALUES (?, ?, ?)', (None, city_, humidity_))
    conn.commit()


    join_data = cur.execute("SELECT temp, humidity FROM Weather JOIN Cities ON Cities.city = Weather.city")
    data_needed = join_data.fetchall()
    for item in data_needed:
        x = item[0]
        y = item[1]
        plt.scatter(x, y, alpha=0.5)
    plt.title('Scatterplot of Temp vs. Humidity')
    plt.xlabel('Temperature')
    plt.ylabel('Humidity')
    plt.show()
    conn.commit()


    cur.execute('SELECT humidity FROM Cities')
    total = 0
    count = 0
    for humid in cur:
        total += humid[0]
        count += 1
    average_humidity = (total/count)
    print(average_humidity)


    cur.execute('SELECT temp FROM Weather')
    total = 0
    count = 0
    for temps in cur:
        total += (temps[0] - 273.15)
        count += 1
    average_temp = (total/count)
    print(average_temp)


    new_file = {}
    new_file['weather'] = average_humidity
    new_file['weather_2'] = average_temp
    with open('aggregateMyData.json', 'a+') as outfile:
        json.dump(new_file, outfile)
    
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

    
openweather_database(dbname)
insert_info_data()






    
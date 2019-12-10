import requests
import json
import hide2

#from yelpcalls import cityInfo
import sqlite3

import sqlite3

import matplotlib
import matplotlib.pyplot as plt
import json

def yelpRequest(city):
    header = {'Authorization': "Bearer %s" % hide2.yelp_key}
    params= {}
    params['limit'] = 20
    params['location'] = city
    url = 'https://api.yelp.com/v3/businesses/search'
    response = requests.get(url, params=params, headers=header)
    new = json.loads(response.text)
    return new

def cityInfo(city):
    data = yelpRequest(city)
    cityBusinesses = []

    for business in data['businesses']:
        try:
            price = business['price']
        except:
            price = 'NA'
        cityBusinesses.append({
                                "city": city,
                                "name": business['name'],
                                "location": business['location']['address1'],
                                "price": price,
                                'rating': business['rating'],
                                'cuisine_types': business['categories'][0]['title']
                             })
    print(cityBusinesses)
    return cityBusinesses

cityInfo('Detroit')


dbname = "final_project.db"
def yelp_database(dbname):

    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
    except:
        print('Could not connect')
    cur.execute('CREATE TABLE IF NOT EXISTS Yelp1 (CityName TEXT, BusinessName TEXT, Location TEXT, Price TEXT, CuisineType TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS Yelp2 (CityName TEXT, BusinessName TEXT, Rating INTEGER)')
    conn.commit()
    conn.close()

yelp_database(dbname)



def insert_yelp_data1():
    city = input('Please enter a city ')
    businesses = cityInfo(city) 
    conn = sqlite3.connect('final_project.db')
    cur = conn.cursor()

    for business in businesses:
        vals = list(business.values())
        city_ = vals[0]
        name_ = vals[1]
        location_ = vals[2]
        price_ = vals[3]
        cuisine_types = vals[5]
        cur.execute('SELECT * FROM Yelp1 WHERE BusinessName=?',(name_,)) 

        cur.execute('SELECT * FROM Yelp1 WHERE BusinessName=?',(name_,))
        val = cur.fetchone() 
        if val == None:
            cur.execute('INSERT INTO Yelp1 (CityName, BusinessName, Location, Price, CuisineType) VALUES (?, ?, ?, ?, ?)', (city_, name_, location_, price_, cuisine_types))
    conn.commit()


insert_yelp_data1()

def insert_yelp_data2():
    city = input('Please enter a city ')
    businesses = cityInfo(city) 
    conn = sqlite3.connect('final_project.db')
    cur = conn.cursor()

    for business in businesses:
        vals = list(business.values())
        city_ = vals[0]
        name_ = vals[1]
        rating_ = vals[4]
        cur.execute('SELECT * FROM Yelp2 WHERE BusinessName=?',(name_,)) 

        cur.execute('SELECT * FROM Yelp2 WHERE BusinessName=?',(name_,))
        val = cur.fetchone() 
        if val == None:
            cur.execute('INSERT INTO Yelp2 (CityName, BusinessName, Rating) VALUES (?, ?, ?)', (city_, name_, rating_))
    conn.commit()

insert_yelp_data2()

def database_join():
    '''SELECT Yelp1.CityName, BusinessName, Location, Price, CuisineType, Yelp2.Rating FROM Yelp1
    LEFT JOIN Yelp2
    ON Yelp1.BusinessName = Yelp2.BusinessName'''  


def calcAvgRating():
    conn = sqlite3.connect("final_project.db")
    cur = conn.cursor()

    cur.execute('SELECT CityName, Rating FROM Yelp2')

    totalRating = {}
    city_appears_dict = {}

    for row in cur:
        city = row[0]
        if city not in totalRating:
            totalRating[city] = 0
        totalRating[city] += row[1]
        if city not in city_appears_dict:
            city_appears_dict[city] = 0
        city_appears_dict[city] += 1

    avgRating = {}

    for item in totalRating.items():
        city = item[0]
        total = item[1]
        avg = total / city_appears_dict[city]
        avgRating[city] = avg
    
    return avgRating

    
  
def calcAvgPrice():
    conn = sqlite3.connect("final_project.db")
    cur = conn.cursor()

    cur.execute('SELECT CityName, Price FROM Yelp1')

    totalPrice = {}
    city_appears_dict = {}

    for row in cur:
        city = row[0]
        if city not in totalPrice:
            totalPrice[city] = 0
        totalPrice[city] += len(row[1])
        if city not in city_appears_dict:
            city_appears_dict[city] = 0
        city_appears_dict[city] += 1

    avgPrice = {}

    for item in totalPrice.items():
        city = item[0]
        total = item[1]
        avg = total / city_appears_dict[city]
        avgPrice[city] = avg
    #print(avgPrice)
    return avgPrice


def calculationsFile():
    yelp = calcAvgRating()

    new_file = {}
    new_file['yelp'] = yelp

    with open('yelp_calculations_1.json', 'w') as outfile:
        json.dump(new_file, outfile)

calculationsFile()
print(calculationsFile())

def calculationsFile2():
    yelp = calcAvgPrice()

    new_file = {}
    new_file['yelp'] = yelp

    with open('yelp_calculations_2.json', 'w') as outfile:
        json.dump(new_file, outfile)

calculationsFile2()

def createRatingVisual():
    f1 = open('yelp_calculations_1.json', 'r')
    f1_ = f1.read()
    f2 = json.loads(f1_)
    dict_ = f2['yelp']
    xvals = dict_.keys()
    yvals = dict_.values()

    plt.bar(xvals, yvals, align='center', color = ['darkred', 'red', 'salmon', 'coral', 'darkorange'])

    plt.xticks(rotation=45)
    plt.ylabel('Avg Rating')
    plt.xlabel('City')
    plt.title('Avg Restaurant Rating per City')
    plt.tight_layout()
    plt.savefig('RatingPerCity.png')
    plt.show()


def createPriceVisual():
    f1 = open('yelp_calculations_2.json', 'r')
    f1_ = f1.read()
    f2 = json.loads(f1_)
    dict_ = f2['yelp']
    xvals = dict_.keys()
    yvals = dict_.values()

    plt.bar(xvals, yvals, align='center', color = ['darkslategray', 'teal', 'cyan', 'cadetblue', 'powderblue'])

    plt.xticks(rotation=45)
    plt.ylabel('Avg Price')
    plt.xlabel('City')
    plt.title('Avg Restaurant Price per City')
    plt.tight_layout()
    plt.savefig('PricePerCity.png')
    plt.show()

createRatingVisual()
createPriceVisual()
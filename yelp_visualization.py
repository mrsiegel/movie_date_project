#import create_yelp_database

import sqlite3

import matplotlib
import matplotlib.pyplot as plt
import json

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

    with open('yelp_calculations.json', 'w') as outfile:
        json.dump(new_file, outfile)

calculationsFile()
print(calculationsFile())

def calculationsFile2():
    yelp = calcAvgPrice()

    new_file = {}
    new_file['yelp'] = yelp

    with open('yelp_calculations2.json', 'w') as outfile:
        json.dump(new_file, outfile)

calculationsFile2()


def createRatingVisual():
    f1 = open('yelp_calculations.json', 'r')
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
    f1 = open('yelp_calculations2.json', 'r')
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

# In order to create an updated visual, with updated calculations, run this file
createRatingVisual()
createPriceVisual()
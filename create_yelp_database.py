from yelpcalls import cityInfo
import sqlite3

dbname = "final_project.db"
def yelp_database(dbname):
    #cityBusinessList = yelpcalls.cityInfo(city)

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

        
        

'''except:
        print('Businesses already in DB, please enter a different city')'''


def insert_yelp_data1():
    city = input('Please enter a city ')
    businesses = cityInfo(city) 
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    for business in businesses:
        vals = list(business.values())
        city_ = vals[0]
        name_ = vals[1]
        location_ = vals[2]
        price_ = vals[3]
        #rating_ = vals[4]
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
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    for business in businesses:
        vals = list(business.values())
        city_ = vals[0]
        name_ = vals[1]
        #location_ = vals[2]
        #price_ = vals[3]
        rating_ = vals[4]
        #cuisine_types = vals[5]
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
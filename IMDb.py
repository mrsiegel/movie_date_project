from urllib.request import Request
from urllib.request import urlopen
import urllib.request, urllib.parse, urllib.error
import ssl
import requests
import json
import sqlite3
import json
import secrets
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt 



from imdb import IMDb

# ia = IMDb()
# top250 = ia.get_top250_movies()
# top20 = top250[:21]
# for item in top20['directors']:
#     print(item['name'])

#scrape list from IMDb
def getAllMovieRows(s):
    movie_rows = s.find('tbody', class_ = 'lister-list')
    tr_tags = movie_rows.find_all('tr')
    #print(movie_rows)
    return tr_tags

def getAllMovies(all_rows):
    top250 = []
    for item in all_rows:
        column = item.find('td', class_='titleColumn')
        text = column.a.text
        top250.append(text)
        #print(top250)
    return top250

url = 'https://www.imdb.com/chart/top'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

all_rows = getAllMovieRows(soup)
movies = getAllMovies(all_rows)


def getmovieapi(top250):         # maximum return items (the default value is 20)
    rankingdict = {}
    for item in top250:
        param= {'t': item, 'apikey': secrets.api_key}
        url = "http://www.omdbapi.com/"
        requested = requests.get(url,param).text
        t=json.loads(requested)
        #print(t)
        #print('----')
        if t['Response'] == 'True':
            try:
                rotten= t['Ratings'][1]['Value']
            #print(rotten)
                rating=t['Rated']
                time=t['Runtime']
                genre=t['Genre']
            except:
                rotten= None
            #print(rotten)
                rating=None
                time=None
                genre=None
            
        else:
            continue
        if item not in rankingdict:
                rankingdict[item]=(rotten, rating, time, genre)
    
    return rankingdict

#print(getmovieapi(movies))


# #database
dbname = 'final_project.db'
def make_database(dbname):
    try:
        conn=sqlite3.connect(dbname)
        cur=conn.cursor()
    except:
        print('Could not connect')
    statement='''
    DROP TABLE IF EXISTS 'Omdb';
    '''
    cur.execute(statement)
    conn.commit()
    statement= '''CREATE TABLE IF NOT EXISTS 'Omdb' (ID INTEGER PRIMARY KEY AUTOINCREMENT, TITLE TEXT, ROTTEN_TOMATOES INTEGER)'''
    statement2='''CREATE TABLE IF NOT EXISTS 'Omdb2' (ID INTEGER PRIMARY KEY AUTOINCREMENT, TITLE TEXT, GENRE TEXT)'''
    cur.execute(statement)
    cur.execute(statement2)
    conn.commit()
    conn.close()

make_database(dbname)
 
def insertion():
    #counter = 0
    newmovies = getmovieapi(movies)
    #print(newmovies)
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    for movie in newmovies:
        #if counter > 19:
            #break
        #else:
        try:
            tomatoes = int(newmovies[movie][0][:-1])
            #print(tomatoes)
            gen = newmovies[movie][-1]
            #print(gen)
        except:
            tomatoes=newmovies[movie][0]
            gen=newmovies[movie][-1]
            #if cur.execute('SELECT VALUES (?, ?)', (movie, tomatoes)) == None    
        cur.execute('INSERT INTO Omdb (TITLE, ROTTEN_TOMATOES) VALUES (?, ?)', (movie, tomatoes)) 
        cur.execute('INSERT INTO Omdb2 (TITLE, GENRE) VALUES (?, ?)', (movie, gen))
        #counter += 1  
    conn.commit()

    cur.execute('SELECT TITLE FROM Omdb')
    thetotal = 0
    for item in cur:
        #print(item)
        if "The" not in item[0]:
            thetotal += 1
    print(thetotal)

    cur.execute('SELECT ROTTEN_TOMATOES FROM Omdb')
    hightotal = 0
    for num in cur:
        #print(num)
        if num[0] == 90:
            hightotal += 1
    print(hightotal)

    cur.execute('SELECT TITLE FROM Omdb')
    title_list = []
    for name in cur:
        #print(name)
        title_list.append(name[0])

    cur.execute('SELECT ROTTEN_TOMATOES FROM Omdb')
    tomatolist= []
    for rot in cur:
        tomatolist.append(rot[0])

    data = {}
    count1 = 0
    for x in title_list:
        if x not in data:
            data[x]= tomatolist[count1]
        count1 += 1

    plt.bar(title_list[0:10], tomatolist[0:10], align='center', color=['salmon', 'orangered', 'chocolate', 'peru', 'burlywood', "midnightblue", "navy", 'darkblue', 'mediumblue', 'blue'])
    plt.ylabel('Rotten Tomatoes Score (percentage)')
    plt.xlabel("Movie Title")
    plt.title('Rotten Tomatoes')
    plt.xticks(rotation = 30)
    plt.savefig('RottenPlot.png')
    plt.show()
    

insertion()
        #inserting = (None, movie, tomatoes)
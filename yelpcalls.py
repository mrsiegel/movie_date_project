import requests
import json
import hide

def yelpRequest(city):
    header = {'Authorization': "Bearer %s" % hide.yelp_key}
    params= {}
    params['limit'] = 20
    params['location'] = city
    url = 'https://api.yelp.com/v3/businesses/search'
    response = requests.get(url, params=params, headers=header)
    new = json.loads(response.text)
    return new

def cityInfo(city):
    # city = input_city_name()
    data = yelpRequest(city)
    cityBusinesses = []
    # all_businesses = {}

    for business in data['businesses']:
        # all_businesses['city'] = city
        # all_businesses['name'] = business['name']
        # all_businesses['location'] = business['location']['address1']
        try:
            # all_businesses['price'] = business['price']
            price = business['price']
        except:
            # all_businesses['price']='NA'
            price = 'NA'
        # all_businesses['rating'] = business['rating']
        # all_businesses['cuisine_types'] = business['categories'][0]['title']
        # print(all_businesses)
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


# def input_city_name():
#     user = input('Please enter a city name ')
#     return user

cityInfo('Detroit')


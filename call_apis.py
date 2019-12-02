import requests
import json
import hide


def amcRequest(city)
url = 'https://api.amctheatres.com/v2/locations/states/Michigan'
request = requests.get(url)
r = json.loads(request.text)
print(r)
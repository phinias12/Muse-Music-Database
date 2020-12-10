from db import execute_read_query, execute_query, connection
import requests
from config import API_KEY

url = "https://theaudiodb.p.rapidapi.com/artist.php"

ID = str(input("Artist ID: "))

querystring = {"i":ID}

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "theaudiodb.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

info = response.json()

name = info['artists'][0]['strArtist']
print("Name: " + name)

dob = int(info['artists'][0]['intBornYear'])
print("DOB: " + str(dob))

location = info['artists'][0]['strCountry']
print("Country: " + location)

bio = info['artists'][0]['strBiographyEN']

print("Bio: \n" + bio)
bio = repr(bio).replace('"','\\"')
print("New Bio: \n" + bio)

query = """INSERT INTO `artist`(`name`, `dob`, `location`, `bio`) VALUES ("{}","{}","{}","{}");""".format(name, dob, location, bio)
execute_query(connection, query)
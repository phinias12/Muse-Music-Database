from db import execute_read_query, execute_query, connection
import requests
from config import API_KEY

def convertMillis(millis):
    millis = int(millis)
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    return "{:0>2}:{:0>2}".format(minutes, seconds)

ID = str(input("Album ID: "))

# Parsing Album Information
url = "https://theaudiodb.p.rapidapi.com/album.php"

querystring = {"m": ID}

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "theaudiodb.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

info = response.json()

artistID = str(input("Artist ID In DB: "))

name = info['album'][0]['strAlbum']
print("Name: " + name)

release_year = info['album'][0]['intYearReleased']
print("Release Year: " + release_year)

genre = info['album'][0]['strGenre']
print("Genre: " + genre)

# Insert Album Into Database
query = """INSERT INTO `album`(`name`, `genre`, `release_year`) VALUES ("{}","{}","{}");""".format(name, genre,release_year)
execute_query(connection, query)

# ------------------------
# Track List
album_id = """SELECT albumID FROM album WHERE name = "{}";""".format(name)
albumID = execute_read_query(connection, album_id)[0][0]
url = "https://theaudiodb.p.rapidapi.com/track.php"

querystring = {"m": ID}

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "theaudiodb.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

info = response.json()

tracks = info['track']

for track in tracks:
    # Name
    name = track['strTrack']
    print("Name: " + name)

    # Track Num
    track_num = track['intTrackNumber']
    print("Track Num: " + track_num)

    # Length (in ms -> use convertMillis to get minute form)
    duration = int(track['intDuration'])
    length = convertMillis(duration)
    print("Length: " + length)

    query = """INSERT INTO `song`(`artistID`, `albumID`, `name`, `track_num`, `length`) VALUES ("{}","{}","{}","{}","{}")""".format(artistID, albumID, name, track_num, length)
    execute_query(connection, query)
from bs4 import BeautifulSoup
import requests
import spotipy
import pprint, os
from spotipy.oauth2 import SpotifyOAuth

date = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
URL = f'https://www.billboard.com/charts/hot-100/{date}/'
response = requests.get(URL, headers=header).text

soup = BeautifulSoup(response, 'html.parser')

song_element = soup.select(selector='.c-title.a-no-trucate')
raw_song_list = [each.getText().split() for each in song_element]

song_list = [" ".join(each) for each in raw_song_list]

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

login = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope="playlist-modify-private", redirect_uri='http://example.com'))
user_id = login.current_user()['id']
print(song_list)


year = date.split("-")[0]
song_uris = []
for song in song_list:
    result = login.search(q=f"track:{song} year:{year}", type='track')
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = login.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, description=f"Playlist of 100 best Billboard songs at the date of {date}")
login.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
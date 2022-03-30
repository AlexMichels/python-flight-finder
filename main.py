import requests
from bs4 import BeautifulSoup
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)
SPOTIPY_CLIENT_ID = "[your id]"
SPOTIPY_CLIENT_SECRET = "[your secret]"
SPOTIPY_REDIRECT_URI = "https://example.com/callback"
os.environ["SPOTIPY_CLIENT_ID"] = "[client id]"
os.environ["SPOTIPY_CLIENT_SECRET"] = "[spotify secret]"
os.environ["SPOTIPY_REDIRECT_URI"] ="https://example.com/callback"

timestamp = input("what time you would like to travel to? (YYY-MM-DD format): ")

URL = f"https://www.billboard.com/charts/hot-100/{timestamp}"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

all_titles = soup.select(selector="li ul li h3")
titles = [title.getText().strip() for title in all_titles]
for title in titles:
    print(title)


import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))

spotify_uri = []
for title in titles:
    q = f"track: {title} year: {timestamp.split('-')[0]}"
    suche = sp.search(q=q, type="track",limit=1)
    try:
        uri = suche["tracks"]["items"][0]["uri"]
    except IndexError:
        print(f"{title} not found")
        continue
    else:
        pp.pprint(uri)
        spotify_uri.append(uri)

user_id = sp.current_user()["id"]
playlist_id = sp.user_playlist_create(user=user_id, name=f"{timestamp} TOP 100 Charts", public=True, collaborative=False, description=f"Top 100 Hits from {timestamp}")

sp.user_playlist_add_tracks(playlist_id=playlist_id["id"], tracks=spotify_uri, user=user_id)

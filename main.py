import os


import telebot
import requests
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
from lyricsgenius import Genius
from googletrans import Translator
from dotenv import load_dotenv

load_dotenv()

genius = Genius(os.getenv("GENUIS_TOKEN"))

cid =os.getenv("CID")
secret =os.getenv("SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
bot = telebot.TeleBot(os.getenv("SPOTIFY_TOKEN"))

translator = Translator()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Just send a spotify song's URL to translate the song into English")

def song_request(message):
    if(len(message.text)):
        return True
    else:
        return False

@bot.message_handler(func=song_request)
def get_track(message):
    try:
        
        track = sp.track(message.text)
        
        for key, value in track.items():
            if(key == 'name'):
                songname = value

            if(key == 'artists'):
                artistname = value[0]['name']

        song = genius.search_song(songname, artistname)
        
        text = scrape_lyrics(song.url)

        bot.send_message(message.chat.id, text)

        translation = translator.translate(text)

        bot.send_message(message.chat.id, translation.text)
    
    except:

        bot.send_message(message.chat.id, "Invalid song URL")
        




def scrape_lyrics(url):

    print(url)

    page = requests.get(url)

    html = BeautifulSoup(page.text, 'html.parser')
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")

    for br in lyrics2.find_all("br"):
        br.replace_with("\n")

    return lyrics2.get_text()



bot.polling()
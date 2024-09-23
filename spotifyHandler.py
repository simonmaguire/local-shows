from dotenv import load_dotenv
import base64
import requests
import os

def retrieveGeneralAccessToken(id , secret):
    idWithSecret = f'{id}:{secret}'
    encodedString = base64.b64encode(idWithSecret.encode()).decode("utf-8")
    authOptions = {
        'url': 'https://accounts.spotify.com/api/token',
        'headers' : {
            'Authorization': f'Basic {encodedString}'
            },
        'form' : {
            'grant_type' : 'client_credentials'
        }, 
        'json' : True
    }
    r = requests.post(
        'https://accounts.spotify.com/api/token',
        headers= {'Authorization': f'Basic {encodedString}'},
        data={'grant_type' : 'client_credentials'}
        )
    return(f'Bearer {r.json()['access_token']}')


class SpotifyHandler(object):
    def __init__(self, shows=[]):
        load_dotenv()
        self.shows = shows
        try:
            print('creating token')
            self.token = retrieveGeneralAccessToken(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))
        except:
            print('Failed to create Access Token')
        



    def searchArtist(self, artist):
        r = requests.get('https://api.spotify.com/v1/search', 
                     headers={'Authorization': self.token},
                     params={'q' : f'artist:{artist}', 'type' : 'artist', 'limit' : '3'})
        print(r.status_code)
        if(r.status_code == 200):
            for i in r.json()['artists']['items']:
                print(i)
        
            

    # def saveArtistInfo(self):

    # def getArtistTracks(self):

    # def createPlaylist(self):



    
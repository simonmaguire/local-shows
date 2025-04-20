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

def uriTracks(tracks):
    result = []
    for track in tracks:
        result.append('spotify:track:' + track)

    return result

class SpotifyHandler(object):
    def __init__(self, token):
        load_dotenv()
        self.token = token
        if (self.token is None):
            try:
                print('creating token')
                self.token = retrieveGeneralAccessToken(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))
            except:
                print('Failed to create Access Token')
        



    def searchArtist(self, artist):
        r = requests.get('https://api.spotify.com/v1/search', 
                     headers={'Authorization': self.token},
                     params={'q' : f'artist:{artist}', 'type' : 'artist', 'limit' : '1'})
        print('Search Artist: ' + str(r.status_code))
        if(r.status_code == 200 and r.json()['artists']['items'] and r.json()['artists']['items'][0]):
            return r.json()['artists']['items'][0]
        else:
            return {}
            
    def getTopTracks(self, artistID):
        r = requests.get(f'https://api.spotify.com/v1/artists/{artistID}/top-tracks', 
                     headers={'Authorization': self.token})
        print('Get Top Tracks: ' + str(r.status_code))
        result = []
        if(r.status_code == 200 and r.json()['tracks'] and r.json()['tracks']):
            if(r.json()['tracks'][0]):
                track1 = r.json()['tracks'][0]
                result.append({
                    'name': track1['name'],
                    'album': track1['album']['name'], 
                    'image': track1['album']['images'][0]['url'],
                    'artist': track1['album']['artists'][0]['name'],
                    'id': track1['id'],
                    'uri': track1['uri']

                    
                    })
                if(r.json()['tracks'][1]):
                    track2 = r.json()['tracks'][1]
                    result.append({
                        'name': track2['name'],
                        'album': track2['album']['name'], 
                        'image': track2['album']['images'][0]['url'],
                        'artist': track2['album']['artists'][0]['name'],
                        'id': track2['id'],
                        'uri': track2['uri']
                        })
                    if(r.json()['tracks'][2]):
                        track3 = r.json()['tracks'][2]
                        result.append({
                            'name': track3['name'],
                            'album': track3['album']['name'], 
                            'image': track3['album']['images'][0]['url'],
                            'artist': track3['album']['artists'][0]['name'],
                            'id': track3['id'],
                            'uri': track3['uri']
                            })
                
        return result
            
    def createPlaylist(self, user_id, name):
        playlistData = {"name": name, "description": "Upcoming concerts found by Local Shows"}
        r = requests.post(f'https://api.spotify.com/v1/users/{user_id}/playlists', 
                     headers={'Authorization': self.token}, json = playlistData)
        if(r.status_code != 200):
            status = {'status': r.status_code, 'msg': r.json()}
            return status
        
        return r.json()
    


    def saveSongsToPlaylist(self, playlist_id, tracks):
        #add a check for 100 songs, and create seperate calls for everything to be added
        # trackURIs = uriTracks(tracks)
        songs = {"uris": tracks}
        r = requests.post(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', 
                     headers={'Authorization': self.token}, json = songs)
        
        return r.json()    
    


    
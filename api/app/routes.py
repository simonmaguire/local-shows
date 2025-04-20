from showSearcherAlchemy import showSearcherAlchemy
from spotifyHandler import SpotifyHandler
from datetime import date, timedelta
from app import app, db
from app.models import User
from flask import request, abort, url_for, jsonify, g
from flask_httpauth import HTTPBasicAuth
from userController import saveProfile
auth = HTTPBasicAuth()

def findShows():
    searcher = showSearcherAlchemy()
    data = searcher.retrieveShows("Boise", date.today(), date.today() + timedelta(days = 14))

    print("returning shows...")
    return data


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/getShows', methods=['GET'])
def getShows():
    searcher = showSearcherAlchemy()
    data = searcher.retrieveShows("Boise", date.today(), date.today() + timedelta(days = 14))

    print("returning shows...")
    return data


@app.route('/api/getArtistsFromShows', methods=['GET'])
def getArtistsFromShows():
    shows = findShows()
    token = request.headers.get('Authorization')
    spotify = SpotifyHandler(token)
    artists = []
    for show in shows:
        artist = spotify.searchArtist(show['artist_name'])
        artists.append(artist)
        
    print(f'returning artists......')
    for artist in artists:
        if(artist and artist['name']):
            print(f'{artist['name']}')
        else:
            print(f'{artist}')
    return {'shows' : shows, 'artists': artists}


@app.route('/api/getTopTracks/<artist_spotify_id>', methods=['GET'])
def getTopTracks(artist_spotify_id):
    artist_spotify_id = request.view_args['artist_spotify_id']
    token = request.headers.get('Authorization')
    spotify = SpotifyHandler(token)
    tracks = spotify.getTopTracks(artist_spotify_id)
    return tracks
        


@app.route('/api/new_user', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None or email is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None or User.query.filter_by(email=email).first() is not None:
        abort(400)
    user = User(username=username, email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return(jsonify({"username": user.username}), 201)


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token, 'duration': 600})

@app.route('/api/saveProfileAsUser', methods=['POST'])
def saveProfileAsUser():
    profile = request.json.get('profile')
    print(profile)
    saveProfile(profile)
    response = jsonify({'spotify_id': profile['spotify_id']})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return(response)

@app.route('/api/saveShow', methods=['POST'])
def saveShow():
    user = request.json.get('user')
    show = request.json.get('show')
    searcher = showSearcherAlchemy()
    response = searcher.saveShow(user, show)
    return response

@app.route('/api/removeShow', methods=['POST'])
def removeShow():
    user = request.json.get('user')
    show = request.json.get('show')
    searcher = showSearcherAlchemy()
    response = searcher.removeShow(user, show)
    return response

@app.route('/api/getUserShows/<user>', methods=['GET'])
def getUserShows(user):
    user = request.view_args['user']
    searcher = showSearcherAlchemy()
    response = searcher.getUserShows(user)
    return response

@app.route('/api/saveSpotifyID', methods=['POST'])
def saveSpotifyID():
    concert_id = request.json.get('concert_id')
    artist_id = request.json.get('artist_id')
    artist_spotify_id = request.json.get('artist_spotify_id')
    searcher = showSearcherAlchemy()
    response = searcher.saveSpotifyID(concert_id, artist_id, artist_spotify_id)
    return response
    
@app.route('/api/spotifyArtistAtConcert/<concert_id>', methods=['GET'])
def spotifyArtistAtConcert(concert_id):
    concert_id = request.view_args['concert_id']
    searcher = showSearcherAlchemy()
    ids = searcher.getSpotifyIDs(concert_id)
    return ids

@app.route('/api/createPlaylist', methods=['POST'])
def createPlaylist():
    token = request.headers.get('Authorization')
    user_id = request.json.get('user_id')
    songs = request.json.get('songs')
    name = 'Upcoming Shows'
    spotify = SpotifyHandler(token)
    data = spotify.createPlaylist(user_id, name)
    print(data['msg']['id'])
    x = spotify.saveSongsToPlaylist(data['msg']['id'], songs)
    return data

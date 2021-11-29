from flask import Blueprint, render_template, request, redirect, session, url_for
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import time

views = Blueprint('views', __name__)
tokenInfo = "token_info"
songList = []
songRecs= []
songRecsName= []

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        auth = spotifyThing()
        url = auth.get_authorize_url()
        return redirect(url)
        
    else:
        return render_template("home.html")


@views.route('/redirectPage')
def doRedirect():
    authThing = spotifyThing()
    session.clear()
    aCode = request.args.get('code')
    token = authThing.get_access_token(aCode)
    session[tokenInfo]= token
    return redirect(url_for('views.stuff', _external=True))


def tokens():
    try:
        token = checkToken()
    except:
        return redirect(url_for('views.home'))
    return spotipy.Spotify(auth=token['access_token'])

@views.route('/list')
def stuff():
    activities = tokens()
    number = 0
    songId = []
    while True:
        songItems = activities.current_user_saved_tracks(limit=50, offset=number * 50)['items']
        for whatever in songItems:
            songList.append(whatever['track']['name'])
            if len(songId) < 4: #just testing for now would need better seeds/ more variety
                songId.append(whatever['track']['id'])
        number+=1
        if len(songItems) < 50:
            break
    
    #when using ML model add it here to replace recommendations
    dics = activities.recommendations(seed_tracks=songId)['tracks']
    for songs in dics:
        songRecs.append(songs['id'])
        songRecsName.append(songs['name'])
    print(str(songRecs))
    print(activities.current_user()['id'])

    return redirect(url_for('views.recs', _external=True))

@views.route('/recomendations',methods=['GET', 'POST'])
def recs():
    if request.method == 'POST':
        print(f"\n\n\n KORNS MASSIVE PP \n\n\n")
        activities = tokens()
        times = checkForExisting()
        activities.user_playlist_create(activities.current_user()['id'], f"test{times}", public=True, collaborative=False, description='')  
        playlists = activities.user_playlists(activities.current_user()['id'])
        target = playlists['items']
        playListID = ''
        for stuff in target:
            if stuff['name'] == f"test{times}":
                playListID = stuff['id']
        activities.user_playlist_add_tracks(activities.current_user()['id'], playListID, songRecs, position=None)
        return redirect(url_for('views.recs', _external=True))
    else:
    #send to page where they see their rec options or can simply hit button to generate playlist on their spotify account
    #pass the songlist to a function/file which then returns the list of reccomended songs then put that in place of songList=songList
    #activities.user_playlist_create(username, name=playlist_name)
        return render_template("recom.html", songList = songRecsName) # change whats being passed when using actual ML model

def checkForExisting():
    activities = tokens()
    playlists = activities.user_playlists(activities.current_user()['id'])
    target = playlists['items']
    times = 0
    for stuff in target:
        if "test" in stuff['name']:
            times += 1
    return times

def checkToken():
    token = session.get(tokenInfo, None)
    if token is None:
        raise "exception"
    current = int(time.time())
    print(f"\n\n\n {token['expires_at']} \n\n\n")
    expiration = token['expires_at'] - current < 60
    if expiration:
        auth = spotifyThing()
        token = auth.refresh_access_token(token['refresh_token'])
    return token


def spotifyThing():
    return SpotifyOAuth(
        client_id='63a6f988833b44c481eabf435d05535e',
        client_secret='a4712153d0b14a4a95dba6203ee8c582',
        redirect_uri=url_for('views.doRedirect', _external=True),
        scope="playlist-modify-private user-library-read playlist-modify-public")

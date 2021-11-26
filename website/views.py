from flask import Blueprint, render_template, request, redirect, session, url_for
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import time

views = Blueprint('views', __name__)
tokenInfo = "token_info"
songList = []

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

@views.route('/list')
def stuff():
    try:
        token = checkToken()
    except:
        return redirect(url_for('views.home'))
    activities = spotipy.Spotify(auth=token['access_token'])
    number = 0
    while True:
        songItems = activities.current_user_saved_tracks(limit=50, offset=number * 50)['items']
        for whatever in songItems:
            songList.append(whatever['track']['name'])
        number+=1
        if len(songItems) < 50:
            break
    print(len(songList))
    return redirect(url_for('views.recs', _external=True))

@views.route('/recomendations')
def recs():
    #send to page where they see their rec options or can simply hit button to generate playlist on their spotify account
    #pass the songlist to a function/file which then returns the list of reccomended songs then put that in place of songList=songList
    return render_template("recom.html", songList = songList)

def checkToken():
    token = session.get(tokenInfo, None)
    if token is None:
        raise "exception"
    current = int(time.time())
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
        scope="user-library-read")
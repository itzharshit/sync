import os
import spotipy, time
from flask import session, url_for, flash, redirect
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from flask import session, redirect, flash

# load the .env file and store the Spotify API credentials.
load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_SECRET')

# return an api object based on current logged in user, that can be used to make api calls
def get_spotify_user():
    token_info = session['spot_token_info']
    return  spotipy.Spotify(auth=token_info['access_token'])

# to be called before every function that requires spotify authorization
# check if user is logged into spotify and/or their credentials are valid.
def check_spot():
    token_info = session.get('spot_token_info', None)
    if token_info:
        if token_info['expires_at'] - int(time.time()) < 60:
            sp_oauth =  create_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    else:
        flash('Spotify account authorization needed!')
        return redirect('/')
    
    session['spot_token_info'] = token_info
     
# return an oauth object with the required scopes and api credentials
def create_spotify_oauth():
    return SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=url_for('redirectSpotify', _external=True),
                scope='playlist-read-private playlist-modify-private playlist-modify-public user-library-read')


# write (your_website)/redirectyoutube in redirect_uri
# creates an oauth flow based on the given api credentials
def youtube_oauth():
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json',
                                                    redirect_uri='http://127.0.0.1:5000/redirectyoutube',
                                                    scopes=['https://www.googleapis.com/auth/youtubepartner',
                                                        'https://www.googleapis.com/auth/youtube',
                                                        'https://www.googleapis.com/auth/youtube.force-ssl'])
    return flow

# to be called before every function that requires youtube authorization
# check if user is logged into youtube and/or their credentials are valid.
def check_yt():
    credentials = session.get('yt_token_info', None)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flash('YouTube account authorization needed!')
            return redirect('/')
        
    session['yt_token_info'] = credentials

# return an api object based on current logged in user, that can be used to make api calls
def get_yt_user():
    return build('youtube', 'v3', credentials=session['yt_token_info'], cache_discovery=False)


 


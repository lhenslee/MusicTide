import spotipy.util as util
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


'''
    Allow access to any account with the ability to read or write
    to his/her account. Read and writes are dependent on the scope.
    Defaults to my account and to read my library.
'''
def sp_authorize(username='12125553997', scope='user-library-read'):
    token = util.prompt_for_user_token(username, scope, client_id='9110e5f232f24d7ab98119edb65bc0e5',
                               client_secret='e81f456a37754b8c8b4ed4dc985b425f', redirect_uri='http://localhost/')
    if token:
        return spotipy.Spotify(auth=token)
    return None
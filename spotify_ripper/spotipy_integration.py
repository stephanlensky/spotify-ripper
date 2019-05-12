import sys

import spotipy.util as util
import spotipy.client
import os

redirect_uri = 'http://www.purple.com'
client_id = ''
client_secret = ''
scope = 'playlist-modify-public playlist-modify-private playlist-read-collaborative'

# client_id = os.environ["SPOTIPY_CLIENT_ID"] 
# client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
# redirect_uri = os.environ["SPOTIPY_REDIRECT_URI"]

token = None
spotInstance = None


def init_spotipy(username):
    global token
    token = util.prompt_for_user_token(username, scope)

    global spotInstance
    spotInstance = spotipy.Spotify(auth=token)
    spotInstance.trace = False


def remove_all_from_playlist(username, playlistURI):
    print('hello remove_all')
    tracks = get_playlist_tracks(username, playlistURI)

    track_ids = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        tid = track['id']
        track_ids.append(tid)
    results = spotInstance.user_playlist_remove_all_occurrences_of_tracks(username, rPlaylistID, track_ids)


def get_playlist_tracks(username, playlistURI):
    global rPlaylistID
    p1, p2, p3, p4, rPlaylistID = playlistURI.split(':', 5)

    # the spotify api limits the number of tracks which can be retrieved from a playlist in a single request
    # make multiple requests to collect all playlist tracks before continuing
    print('Collecting tracks from playlist', end='\r')
    tracks = spotInstance.user_playlist(username, rPlaylistID, fields='tracks,next')['tracks']
    sys.stdout.flush()
    print('Collecting tracks from playlist ({}/{})'.format(len(tracks['items']), tracks['total']), end='\r')
    paged_tracks = tracks
    while paged_tracks['next']:
        paged_tracks = spotInstance.next(paged_tracks)
        tracks['items'].extend(paged_tracks['items'])
        sys.stdout.flush()
        print('Collecting tracks from playlist ({}/{})'.format(len(tracks['items']), tracks['total']), end='\r')
    print('Collecting tracks from playlist ({}/{})'.format(len(tracks['items']), tracks['total']))

    return tracks


def get_track_json(track_uri):
    return spotInstance.track(track_uri)

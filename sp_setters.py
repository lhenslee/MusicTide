from authorization import sp_authorize
'''
Global Variable sp: A Spotify object given by the spotipy.Spotify Command.
    The object containing access to the functions provided by spotipy.
'''
sp = sp_authorize(scope='playlist-modify-public')


def set_new_playlist(tracks, user='12125553997', name='Music Tide'):
    """
    Add a new playlist with the given track ids.
    :param tracks: A list of Spotify tracks
        Tracks for each track to add to the playlist.
    :param user: A string
        The user id that wants a new playlist.
    :param name: A string
        The name of the new playlist.
    :return: None
    """
    playlist_id = sp.user_playlist_create(user, name)['id']
    track_ids = []
    for track in tracks:
        track_ids.append(track['id'])
    for i in range(0, len(track_ids), 100):
        if i+100 <= len(track_ids):
            sp.user_playlist_add_tracks(user, playlist_id, track_ids[i:i+100], i)
        else:
            sp.user_playlist_add_tracks(user, playlist_id, track_ids[i:len(track_ids)], i)

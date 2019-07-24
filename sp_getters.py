from authorization import sp_authorize
'''
Global Variable sp: A Spotify object given by the spotipy.Spotify command.
    The object containing access to the functions provided by spotipy.
'''
sp = sp_authorize()


def get_audio_features(track_ids):
    """
    Get a list of track audio_features from a list of track ids without a limit of 50 track ids.
    :param track_ids: A list of strings
        The list of track ids to find audio features for.
    :return: A list of dictionaries
        A list audio features for each track
    """
    track_feats = []
    for i in range(0, len(track_ids), 50):
        if i+50 <= len(track_ids):
            for track_feat in sp.audio_features(track_ids[i:i+50]):
                track_feats.append(track_feat)
        else:
            for track_feat in sp.audio_features(track_ids[i:len(track_ids)]):
                track_feats.append(track_feat)
    return track_feats


def get_current_user_saved_tracks(limit=20):
    """
    Get a list of the current users saved tracks by their ids without a limit of 50 songs.
    :param limit: An integer
        The number of track ids the user wants to get from his/her playlist.
    :return: A list of strings
        The list of track ids on that the user has saved ordered by date.
    """
    track_ids = []
    for i in range(0, limit, 50):
        if i+50 <= limit:
            for item in sp.current_user_saved_tracks(limit=50, offset=i)['items']:
                track_ids.append(item['track']['id'])
        else:
            for item in sp.current_user_saved_tracks(limit=limit-i, offset=i)['items']:
                track_ids.append(item['track']['id'])
    return track_ids


def get_tracks(track_ids):
    """
    Get a list of track information based on a given list of track ids without a limit of 50 track ids.
    :param track_ids: A list of strings
        The list of track ids to find track information for.
    :return: A list of dictionaries
        The list of track information for each track.
    """
    track_infos = []
    for i in range(0, len(track_ids), 50):
        if i+50 <= len(track_ids):
            for track_info in sp.tracks(track_ids[i:i+50])['tracks']:
                track_infos.append(track_info)
        else:
            for track_info in sp.tracks(track_ids[i:len(track_ids)])['tracks']:
                track_infos.append(track_info)
    return track_infos


def get_artists_tracks(artist_ids):
    """
    Get a list of dictionaries for for all
    tracks an artist has ever made.
    :param artist_ids: A list of strings
        A list of artist ids
    :return: A list of dictionaries containing all information for
        each track created by an artist.
    Dictionary Keys:
        artists, available_markets, disc_number, duration_ms, explicit,
        external_urls, href, id, is_local, name, preview_url, track_number,
        type, uri, danceability, energy, key, loudness, mode, speechiness,
        acousticness, instrumentalness, liveness, valence, tempo, track_href,
        analysis_url, time_signature
    """
    track_ids = []
    tracks = []
    artists = sp.artists(artist_ids)['artists']
    for artist in artists:
        for album in sp.artist_albums(artist['id'], limit=50)['items']:
            for track in sp.album_tracks(album['id'], limit=50)['items']:
                if artist['name'] in track['name']:
                    track_ids.append(track['id'])
                    tracks.append(track)
                for track_artist in track['artists']:
                    if artist['name'] == track_artist['name']:
                        track_ids.append(track['id'])
                        tracks.append(track)
    track_features = get_audio_features(track_ids)
    for track, track_feature in zip(tracks, track_features):
        if track_feature is None:
            tracks.remove(track)
            continue
        track.update(track_feature)
    track_variation_dict = {}
    for track in tracks:
        if track['name'].split('(')[0].strip() not in track_variation_dict.keys():
            track_variation_dict[track['name'].split('(')[0].strip()] = []
        track_variation_dict[track['name'].split('(')[0].strip()].append(track)
    for key, value in track_variation_dict.items():
        for version in value:
            if version['explicit']:
                track_variation_dict[key] = version
                break
            track_variation_dict[key] = version
    return [v for v in track_variation_dict.values()]


def remove_duplicates(tracks):
    """
    Removes song duplicates from a list of tracks
    :param tracks: The list of tracks to remove duplicates from
    :return: A list of tracks without duplicates
    """
    track_variation_dict = {}
    for track in tracks:
        if track['name'].split('(')[0].strip() not in track_variation_dict.keys():
            track_variation_dict[track['name'].split('(')[0].strip()] = []
        track_variation_dict[track['name'].split('(')[0].strip()].append(track)
    for key, value in track_variation_dict.items():
        for version in value:
            if version['explicit']:
                track_variation_dict[key] = version
                break
            track_variation_dict[key] = version
    return [v for v in track_variation_dict.values()]

def get_artists_shared_tracks(artist_ids):
    """
    Get the list of tracks that are shared by at least 2 of the artists in the
    artist_ids list
    :param artist_ids: A list of strings
        The list of artist ids to get songs from.
    :return: A list of tracks that share 2 or more artists in the list
    """
    track_ids = []
    tracks = []
    artists = sp.artists(artist_ids)['artists']
    for artist in artists:
        for album in sp.artist_albums(artist['id'], limit=50)['items']:
            for track in sp.album_tracks(album['id'], limit=50)['items']:
                if artist['name'] in track['name']:
                    for artist2 in artists:
                        if artist2 != artist and artist2['name'] in track['name']:
                            track_ids.append(track['id'])
                            tracks.append(track)
                        for track_artist in track['artists']:
                            if artist2 != artist and artist2['name'] == track_artist['name']:
                                track_ids.append(track['id'])
                                tracks.append(track)
                for track_artist in track['artists']:
                    if artist['name'] == track_artist['name']:
                        for artist2 in artists:
                            if artist2 != artist and artist2['name'] in track['name']:
                                track_ids.append(track['id'])
                                tracks.append(track)
                            for track_artist2 in track['artists']:
                                if artist2 != artist and artist2['name'] == track_artist2['name']:
                                    track_ids.append(track['id'])
                                    tracks.append(track)
    track_features = get_audio_features(track_ids)
    for track, track_feature in zip(tracks, track_features):
        track.update(track_feature)
    return remove_duplicates(tracks)


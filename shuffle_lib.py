import sp_getters
import sp_setters
import random


def shuffle_tracks(tracks, max_artist_repeats=3):
    """
    Shuffle a list of tracks and keep the audio features similar (i.e. energy)
    :param track_ids: A list of strings
        A list of arranged track ids.
    :param repeats: A boolean
        Boolean stating if the same artist can play twice in a row
    :return: A list of strings
        Returns the shuffled list of track ids.
    """
    queue = []
    last_track = None
    last_artist = None
    artist_repeats = 0
    for i in range(len(tracks)-1, -1, -1):
        no_similar = False
        ind = random.randint(0, i)
        first_ind = ind
        if last_track is not None:
            while (
                abs(float(tracks[ind]['danceability'])-float(last_track['danceability']))>.1 or
                abs(float(tracks[ind]['energy'])-float(last_track['energy']))>.1 or
                abs(float(tracks[ind]['valence'])-float(last_track['valence']))>.1 or
                artist_repeats == max_artist_repeats
            ):
                if (artist_repeats == max_artist_repeats and
                    tracks[ind]['artists'][0] != last_artist and
                    abs(float(tracks[ind]['danceability'])-float(last_track['danceability'])) < .1 and
                    abs(float(tracks[ind]['energy'])-float(last_track['energy'])) < .1 and
                    abs(float(tracks[ind]['valence'])-float(last_track['valence'])) < .1
                ):
                    artist_repeats = 0
                    break
                if len(tracks) == 1:
                    no_similar = True
                    break
                if ind == i:
                    ind = 0
                    if first_ind == 0:
                        no_similar = True
                        break
                ind += 1
                if ind == first_ind:
                    no_similar = True
                    break
            if tracks[ind]['artists'][0] == last_artist and max_artist_repeats == 0:
                tracks.remove(tracks[ind])
                continue
            if no_similar or (artist_repeats == max_artist_repeats and max_artist_repeats > 0):
                tracks.remove(tracks[ind])
                continue
            if last_artist == tracks[ind]['artists'][0] and max_artist_repeats > 0:
                artist_repeats += 1
            queue.append(tracks[ind])
            last_track = tracks[ind]
            last_artist = tracks[ind]['artists'][0]
            tracks.remove(tracks[ind])
        else:
            queue.append(tracks[ind])
            last_track = tracks[ind]
            last_artist = tracks[ind]['artists'][0]
            tracks.remove(tracks[ind])
    return queue


def sort_tracks(track_ids, tag):
    """
    Sort tracks by a certain tag (i.e. energy).
    :param track_ids: A list of strings
        A list of track ids to sort by a certain tag.
    :param tag: A string
        The tag to sort a list of tracks by.
    :return: A list of strings
        The list of track ids sorted in a new order.
        Will return None if the tag is unavailable or the track_ids list is empty.
    """
    sorted_track_ids = []
    track_features = sp_getters.get_audio_features(track_ids)
    track_features = sorted(track_features, key=lambda x: x[tag])
    for track_feature in track_features:
        sorted_track_ids.append(track_feature['id'])
    return sorted_track_ids


def filter_tracks(tracks, danceability=(0, 1), energy=(0, 1), valence=(0, 1)):
    """
    Extract songs of a certain range from a list of track ids.
    :param tracks: A list of track objects
        The tracks that must be filtered.
    :param danceability: A tuple
        The range of danceability to limit the tracks to.
    :param energy: A tuple
        The range of energy to limit the tracks to.
    :param valence: A tuple
        The range of valence to limit the tracks to.
    :return: A list of strings
        A list of filtered track ids.
    """
    filtered_tracks = []
    for track in tracks:
        if (danceability[0] < track['danceability'] < danceability[1] and
                energy[0] < track['energy'] < energy[1] and
                valence[1] > track['valence'] > valence[0]):
            filtered_tracks.append(track)
    return filtered_tracks


def print_tracks(tracks):
    """
    Print each track's information.
    :param tracks: A list of dictionaries containing track information
    :return: None
    """
    for track in tracks:
        artists = [artist['name'] for artist in track['artists']]
        print('danceability: {0:.3f} energy: {1:.3f} valence: {2:.3f} || {3} - {4}'.format(
            float(track['danceability']), float(track['energy']), float(track['valence']),
            track['name'], ', '.join(artists)
        ))


artists = {}
artists['Flatbush Zombies'] = 'spotify:artist:1dqGS5sT6PE2wEvP1gROZC'
artists['A$AP Mob'] = 'spotify:artist:7yO4IdJjCEPz7YgZMe25iS'
artists['Schoolboy Q'] = 'spotify:artist:5IcR3N7QB1j6KBL8eImZ8m'
artists['Drake'] = 'spotify:artist:3TVXtAsR1Inumwj472S9r4'
artists['Future'] = 'spotify:artist:1RyvyyTE3xzB2ZywiAwp0i'
artists['Lil Wayne'] = 'spotify:artist:55Aa2cqylxrFIXC767Z865'
artists['Lil Uzi Vert'] = 'spotify:artist:4O15NlyKLIASxsJ0PrXPfz'
artists['Gucci Mane'] = 'spotify:artist:13y7CgLHjMVRMDqxdx0Xdo'
artists['Rae Sremmurd'] = 'spotify:artist:7iZtZyCzp3LItcw1wtPI3D'
#artists['Swae Lee'] = 'spotify:artist:1zNqQNIdeOUZHb8zbZRFMX'
#artists['Slim Jxmmi'] = 'spotify:artist:7EEiVZvj6RCEtVX2F2pyxu'
artists['Migos'] = 'spotify:artist:6oMuImdp5ZcFhWP0ESe6mG'
#artists['Post Malone'] = 'spotify:artist:246dkjvS1zLTtiykXe5h60'
#artists['Young Thug'] = 'spotify:artist:50co4Is1HCEo8bhOyUWKpn'i
artists['Travis Scott'] = 'spotify:artist:0Y5tJX1MQlPlqiwlOH1tJY'
artists['Kendrick Lamar'] = 'spotify:artist:2YZyLoL8N0Wb9xBt1NhZWg'
#artists['2 Chainz'] = 'spotify:artist:17lzZA2AlOHwCwFALHttmp'
#artists['Marshmellow'] = 'spotify:artist:64KEffDW9EtZ1y2vBYgq8T'
#artists['Zedd'] = 'spotify:artist:2qxJFvFYMEDqd7ui6kSAcq'
#artists['Avicii'] = 'spotify:artist:1vCWHaC5f2uS3yhpwWbIA6'
#artists['Calvin Harris'] = 'spotify:artist:7CajNmpbOovFoOoasH2HaY'
#artists['Steve Aoki'] = 'spotify:artist:77AiFEVeAVj2ORpC85QVJs'
#artists['GASHI'] = 'spotify:artist:0JOxt5QOwq0czoJxvSc5hS'
#artists['Ace Hood'] = 'spotify:artist:31HjiqargV4NAw4GZqUale'
artists['Young Dolph'] = 'spotify:artist:3HiuzBlSW7pGDXlSFMhO2g'
artists['Waka Flocka Flame'] = 'spotify:artist:6f4XkbvYlXMH0QgVRzW0sM'
artists['Chief Keef'] = 'spotify:artist:15iVAtD3s3FsQR4w1v6M0P'
artists['Ty Dolla $ign'] = 'spotify:artist:7c0XG5cIJTrrAgEC3ULPiq'
#artists['Juicy J'] = 'spotify:artist:5gCRApTajqwbnHHPbr2Fpi'
artists['Wiz Khalifa'] = 'spotify:artist:137W8MRPWKqSmrBGDBFSop'
#artists['Imagine Dragons'] = 'spotify:artist:53XhwfbYqKCa1cC15pYq2q'
#artists['Eminem'] = 'spotify:artist:7dGJo4pcD2V6oG8kP0tJRR'
#artists['NWA'] = 'spotify:artist:4EnEZVjo3w1cwcQYePccay'
#artists['Jimi Hendrix'] = 'spotify:artist:776Uo845nYHJpNaStv1Ds4'
#artists['R.E.M.'] = 'spotify:artist:4KWTAlx2RvbpseOGMEmROg'


tracks = sp_getters.get_artists_tracks(artists.values())
tracks = filter_tracks(tracks, valence=(.9, 1))
#tracks = shuffle_tracks(tracks, max_artist_repeats=1)
print_tracks(tracks)
sp_setters.set_new_playlist(tracks, name='Happy Rap?')


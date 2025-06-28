from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import spo_config

# --- Constants ---
SPOTIPY_SCOPE = 'playlist-read-private'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SPOTIPY_CACHE_PATH = '.cache'

app = Flask(__name__)

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=spo_config.CLIENT_ID,
    client_secret=spo_config.CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SPOTIPY_SCOPE,
    cache_path=SPOTIPY_CACHE_PATH # Using a cache can prevent re-authentication often
))

# Fetches essential information about a Spotify playlist.
def get_playlist_info(playlist_id: str) -> dict:
    try:
        playlist = sp.playlist(playlist_id)
        return {
            'name': playlist['name'],
            'description': playlist['description'],
            'owner': playlist['owner']['display_name'],
            'image_url': playlist['images'][0]['url'] if playlist['images'] else None,
            'total_tracks': playlist['tracks']['total']
        }
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API Error in get_playlist_info: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred in get_playlist_info: {e}")
        return {}


# Retrieves all tracks from a given Spotify playlist.
def get_all_tracks(playlist_id: str) -> list[dict]:
    tracks_details = []
    try:
        results = sp.playlist_tracks(playlist_id)
        while results:
            for item in results['items']:
                track = item.get('track')
                if track and track.get('id'): # Ensure track and its ID exist
                    tracks_details.append({
                        'id': track['id'],
                        'name': track['name'],
                        'artists': [{'name': artist['name'], 'id': artist['id']} for artist in track['artists'] if artist.get('id')],
                        'popularity': track['popularity']
                    })
            if results['next']:
                results = sp.next(results)
            else:
                results = None # No more pages
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API Error in get_all_tracks: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in get_all_tracks: {e}")
    return tracks_details

# Gets the top N most popular tracks from a list of tracks.
def get_top_tracks(all_tracks: list[dict], top_n: int = 5) -> list[dict]:
    if not all_tracks:
        return []
    # Sort tracks by popularity in descending order
    return sorted(all_tracks, key=lambda t: t.get('popularity', 0), reverse=True)[:top_n]


# Determines the top N most common genres among artists in a playlist.
def get_top_genres(all_tracks: list[dict], top_n: int = 5) -> list[tuple[str, int]]:
    artist_ids = set()
    for track in all_tracks:
        for artist in track.get('artists', []):
            if artist.get('id'):
                artist_ids.add(artist['id'])

    genres = []
    # Spotify's artists endpoint can fetch up to 50 artists at a time
    artist_ids_list = list(artist_ids)
    for i in range(0, len(artist_ids_list), 50):
        try:
            artists_chunk = sp.artists(artist_ids_list[i:i+50])['artists']
            for artist in artists_chunk:
                if artist and artist.get('genres'):
                    genres.extend(artist['genres'])
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify API Error fetching artists for genres: {e}")
        except Exception as e:
            print(f"An unexpected error occurred fetching artists: {e}")

    genre_counts = Counter(genres)
    return genre_counts.most_common(top_n)


# Determines the top N most frequent artists in a playlist.
def get_top_artists(all_tracks: list[dict], top_n: int = 5) -> list[tuple[str, int]]:
    artist_counts = Counter()
    for track in all_tracks:
        for artist in track.get('artists', []):
            if artist.get('name'):
                artist_counts[artist['name']] += 1
    return artist_counts.most_common(top_n)


# If you want to use it, you'll need to decide how to integrate its output into your `index.html` template.
# # Fetches audio features for a list of tracks.
# def get_audio_features(tracks: list[dict]) -> list[dict]:
#     track_ids = [track_data['id'] for track_data in tracks if track_data.get('id')]
#     if not track_ids:
#         return []
#     try:
#         features = sp.audio_features(track_ids)
#         return features if features else []
#     except spotipy.exceptions.SpotifyException as e:
#         print(f"Spotify API Error in get_audio_features: {e}")
#         return []
#     except Exception as e:
#         print(f"An unexpected error occurred in get_audio_features: {e}")
#         return []


# Handles the main route for the Flask application.
# Displays a form to enter a Spotify playlist URI and shows playlist details, top artists, tracks, and genres.
@app.route('/', methods=['GET', 'POST'])
def index():

    template_context = {
        'playlist_info': None,
        'top_artists': [],
        'top_tracks': [],
        'top_genres': [],
        'error_message': None
    }

    if request.method == 'POST':
        playlist_uri = request.form.get('playlist_uri')
        if not playlist_uri:
            template_context['error_message'] = "Please enter a Spotify playlist URI."
            return render_template('index.html', **template_context)

        try:
            # Extract playlist ID from URI (handles various formats)
            # e.g., spotify:playlist:37i9dQZF1DXcBWIGoYBM5M or https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
            playlist_id = playlist_uri.split(":")[-1].split("/")[-1].split("?")[0]

            # Fetch all tracks once to reuse across multiple functions
            all_tracks_data = get_all_tracks(playlist_id)

            if not all_tracks_data:
                template_context['error_message'] = "Could not retrieve tracks from the playlist. Please check the URI."
                return render_template('index.html', **template_context)

            template_context['playlist_info'] = get_playlist_info(playlist_id)
            template_context['top_artists'] = get_top_artists(all_tracks_data, top_n=5)
            template_context['top_tracks'] = get_top_tracks(all_tracks_data, top_n=5)
            template_context['top_genres'] = get_top_genres(all_tracks_data, top_n=5)

            if not template_context['playlist_info']:
                template_context['error_message'] = "Could not retrieve playlist information. Check the URI and permissions."

        except spotipy.exceptions.SpotifyException as e:
            template_context['error_message'] = f"Spotify API Error: {e}. Please ensure the URI is correct and you have authenticated."
            print(f"Spotify API Error during POST request: {e}")
        except Exception as e:
            template_context['error_message'] = f"An unexpected error occurred: {e}. Please try again."
            print(f"Unexpected error during POST request: {e}")

    return render_template('index.html', **template_context)


if __name__ == '__main__':
    # In a production environment, set debug=False
    app.run(debug=True)
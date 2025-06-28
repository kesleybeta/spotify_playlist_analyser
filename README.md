# Spotify Playlist Analyzer

A Flask web application that allows users to input a Spotify playlist URI and get detailed insights about the playlist, including:

- Playlist information (name, description, owner, cover image, total tracks)
- Top artists by track count
- Top tracks by popularity
- Top genres among the playlist's artists

This app uses the [Spotify Web API](https://developer.spotify.com/documentation/web-api/) via the [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/) Python client library.

---

## Features

- Authenticate with Spotify using OAuth2
- Fetch all tracks from a playlist (handles pagination)
- Aggregate and display:
  - Top 5 artists by number of tracks in the playlist
  - Top 5 tracks by popularity
  - Top 5 genres from the artists in the playlist
- User-friendly web interface with Flask and Jinja2 templates

---

## Demo

<img src="https://github.com/kesleybeta/spotify_playlist_analyser/blob/main/img/screenshot_1.PNG" height="500" alt="Playlist Analyzer screen"/>
<br>
<img src="https://github.com/kesleybeta/spotify_playlist_analyser/blob/main/img/screenshot_2.png" height="500" alt="Results screen"/>

---

## Getting Started

### Prerequisites

- Python 3.7+
- A Spotify Developer account and registered app to get `CLIENT_ID` and `CLIENT_SECRET`
- Flask and Spotipy Python packages

### Installation

1. Clone the repository:

```bash
git clone https://github.com/kesleybeta/spotify_playlist_info.git
cd spotify-playlist-analyzer
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `spo_config.py` file in the project root with your Spotify credentials:

```python
CLIENT_ID = 'your_spotify_client_id'
CLIENT_SECRET = 'your_spotify_client_secret'
```

5. Run the Flask app:

```bash
flask --app app run
```

6. Open your browser and go to:

```
http://127.0.0.1:8888/
```

---

## Usage

- Enter a Spotify playlist URI or URL in the input form.
- Submit to see the playlist's top artists, tracks, and genres.
- Example playlist URI formats accepted:
  - `spotify:playlist:37i9dQZF1DXcBWIGoYBM5M`
  - `https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M`

---

## Project Structure

```
.
├── app.py               # Main Flask application
├── spo_config.py        # Spotify API credentials (not included in repo)
├── templates/
│   └── index.html       # HTML template for the web interface
├── static/              # Static files (CSS, images, etc.)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## Spotify API Scopes

This app requires the following Spotify API scope:

- `playlist-read-private` — to read private playlists

---

## Notes

- The app uses a local redirect URI (`http://127.0.0.1:8888/callback`) for OAuth. Make sure this URI is whitelisted in your Spotify Developer Dashboard.
- The `.cache` file stores OAuth tokens to avoid re-authentication on every run.
- The app currently runs in debug mode; disable debug in production.

---

## Troubleshooting

- **Authentication errors:** Ensure your Spotify app credentials are correct and the redirect URI matches.
- **Playlist not found:** Verify the playlist URI is correct and that you have access to the playlist.
- **Rate limits:** Spotify API has rate limits; if you hit them, wait and try again later.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/) for the Spotify API Python client
- [Flask](https://flask.palletsprojects.com/) for the web framework
- Spotify for their rich Web API

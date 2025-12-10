import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

# ================= CONFIG =================
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")  # Fix: should be CLIENT_SECRET
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPE = os.getenv("SPOTIFY_SCOPE")
# =========================================

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))


def get_current_track():
    """Return the currently playing track info"""
    try:
        track = sp.current_playback()
        if not track or not track.get('item'):
            return {"message": "No track currently playing."}
        
        item = track['item']
        return {
            "name": item['name'],
            "artist": item['artists'][0]['name'],
            "progress_s": track['progress_ms'] // 1000,
            "duration_s": item['duration_ms'] // 1000,
            "is_playing": track['is_playing']
        }
    except Exception as e:
        return {"error": str(e)}


def get_devices():
    """Return a list of available devices"""
    try:
        response = sp.devices()
        devices = response.get('devices', []) if response else []
        return [{"id": d['id'], "name": d['name'], "type": d['type']} for d in devices]
    except Exception as e:
        return {"error": str(e)}


def start_playback(device_id=None):
    return _safe_spotify_call(lambda: sp.start_playback(device_id=device_id))


def pause_playback(device_id=None):
    return _safe_spotify_call(lambda: sp.pause_playback(device_id=device_id))


def next_track(device_id=None):
    return _safe_spotify_call(lambda: sp.next_track(device_id=device_id))


def previous_track(device_id=None):
    return _safe_spotify_call(lambda: sp.previous_track(device_id=device_id))


def seek_track(position_s, device_id=None):
    return _safe_spotify_call(lambda: sp.seek_track(position_s * 1000, device_id=device_id))


def _safe_spotify_call(func):
    try:
        func()
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}

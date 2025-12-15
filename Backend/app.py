from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import psutil

# Extensions
from extensions import db, jwt

# Blueprints
from auth import auth_bp

# Import existing feature modules
from nos import fetch_nos_news
from weather import fetch_weather
from network_files import get_files_list
from ai_chat import chat_with_ai
import spotify as spotify


# --------------------------------------------------
# App setup
# --------------------------------------------------

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)
jwt.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)

# Create DB tables within an application context to avoid using the decorator
# (some type checkers/IDE stubs may not recognize Flask.before_first_request).
with app.app_context():
    db.create_all()

# --------------------------------------------------
# Existing routes
# --------------------------------------------------

@app.route("/system-info")
def system_info():
    return jsonify(
        {
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
            "network": psutil.net_io_counters()._asdict(),
            "process_count": len(psutil.pids()),
        }
    )


@app.route("/files")
def files_in_folder():
    path = request.args.get("path", "/Plex/")
    if not path.startswith("/Plex/"):
        return jsonify({"error": "Access restricted to /Plex/ and subpaths"}), 403
    try:
        files = get_files_list(path)
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/nos-news")
def nos_news():
    return jsonify(fetch_nos_news())


@app.route("/weather")
def weather():
    return jsonify(fetch_weather())


@app.route("/dashboard-data")
def dashboard_data():
    return jsonify(
        {
            "weather": fetch_weather("winterswijk"),
            "news": fetch_nos_news(),
        }
    )


@app.route("/chat")
def chat():
    user_input = request.args.get("prompt", "")
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400
    response = chat_with_ai(user_input)
    return jsonify({"response": response})


# --------------------------------------------------
# Spotify routes (UNCHANGED)
# --------------------------------------------------

@app.route("/spotify/current")
def spotify_current():
    return jsonify(spotify.get_current_track())


@app.route("/spotify/devices")
def spotify_devices():
    return jsonify(spotify.get_devices())


@app.route("/spotify/play", methods=["POST"])
def spotify_play():
    device_id = request.json.get("device_id")
    return jsonify(spotify.start_playback(device_id))


@app.route("/spotify/pause", methods=["POST"])
def spotify_pause():
    device_id = request.json.get("device_id")
    return jsonify(spotify.pause_playback(device_id))


@app.route("/spotify/next", methods=["POST"])
def spotify_next():
    device_id = request.json.get("device_id")
    return jsonify(spotify.next_track(device_id))


@app.route("/spotify/previous", methods=["POST"])
def spotify_previous():
    device_id = request.json.get("device_id")
    return jsonify(spotify.previous_track(device_id))


@app.route("/spotify/seek", methods=["POST"])
def spotify_seek():
    data = request.json
    device_id = data.get("device_id")
    position_s = data.get("position_s")
    return jsonify(spotify.seek_track(position_s, device_id))


# --------------------------------------------------
# App entrypoint
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1024)

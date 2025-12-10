from flask import Flask, jsonify, request
import psutil
from flask_cors import CORS

# Import custom modules
from nos import fetch_nos_news
from weather import fetch_weather
from network_files import get_files_list
from ai_chat import chat_with_ai

app = Flask(__name__)
CORS(app)  # allow all origins


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
    news = fetch_nos_news()
    return jsonify(news)


@app.route("/weather")
def weather():
    weather_data = fetch_weather()
    return jsonify(weather_data)


@app.route("/dashboard-data")
def dashboard_data():
    return jsonify({"weather": fetch_weather("winterswijk"), "news": fetch_nos_news()})


@app.route("/chat")
def chat():
    user_input = request.args.get("prompt", "")
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400
    response = chat_with_ai(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

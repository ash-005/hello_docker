from flask import Flask, render_template, redirect, url_for, send_file, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import speedtest
import csv
import os
import time
from datetime import datetime
from threading import Thread

# Initialize Flask app
app = Flask(__name__)
RESULTS_FILE = "results.csv"
is_running = False

# Configure Redis for rate limiting
app.config['REDIS_URL'] = "redis://localhost:6379/0"  # Change this URL if you're using a remote Redis server

# Initialize Redis connection
r = redis.StrictRedis.from_url(app.config['REDIS_URL'])

# Initialize Limiter with Redis as the storage backend
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=app.config['REDIS_URL']
)

limiter.init_app(app)

# Ensure results file exists
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Download_Mbps", "Upload_Mbps", "Ping_ms"])

def run_speed_logger():
    global is_running
    start_time = time.time()
    while is_running and (time.time() - start_time < 120):
        try:
            st = speedtest.Speedtest()
            st.download()
            st.upload()
            res = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Download_Mbps": round(st.results.download / 1_000_000, 2),
                "Upload_Mbps": round(st.results.upload / 1_000_000, 2),
                "Ping_ms": st.results.ping,
            }
            with open(RESULTS_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(res.values())
            
            print(f"Logged: {res}")  # Optional: for debugging
            
            # Now sleep to prevent overlapping tests
            time.sleep(15)  # ← adjust this to your vibe

        except Exception as e:
            print("Speedtest error:", e)
            time.sleep(5)  # fallback delay if an error hits

@app.route("/")
def index():
    with open(RESULTS_FILE, newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    return render_template("index.html", results=rows[::-1], running=is_running)

@app.route("/start")
def start():
    global is_running
    if not is_running:
        print("Starting new test thread")
        is_running = True
        Thread(target=run_speed_logger).start()
    else:
        print("Speed test already running")
    return redirect(url_for("index"))

@app.route("/stop") 
def stop():
    global is_running
    is_running = False
    return redirect(url_for("index"))

@app.route("/download")
def download():
    return send_file(RESULTS_FILE, as_attachment=True)

@app.route("/results")
def get_results():
    with open(RESULTS_FILE, newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    return jsonify(rows[::-1])  # latest first

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug = False)
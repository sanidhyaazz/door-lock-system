from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "logs.txt"
LED_STATE = False

def append_log(entry):
    with open(LOG_FILE, 'a') as f:
        f.write(entry + "\n")

def read_logs():
    try:
        with open(LOG_FILE, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

@app.route("/")
def index():
    logs = read_logs()[::-1]  # show newest first
    return render_template("index.html", led_state=LED_STATE, logs=logs)

@app.route("/toggle", methods=["POST"])
def toggle_led():
    global LED_STATE
    LED_STATE = not LED_STATE
    state_str = "ON" if LED_STATE else "OFF"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    append_log(f"LED turned {state_str} at {timestamp}")
    return redirect("/")

@app.route("/esp_state", methods=["GET"])
def get_state():
    return "ON" if LED_STATE else "OFF"

@app.route("/esp_log", methods=["POST"])
def esp_log():
    entry = request.data.decode()
    append_log(f"[ESP32] {entry}")
    return "Logged", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

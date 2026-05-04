from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

import os

app = Flask(__name__)

model = joblib.load("xgb_model.joblib")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        vendor_id = int(data["vendor_id"])  # 1 or 2
        passenger_count = int(data["passenger_count"])
        pickup_longitude = float(data["pickup_longitude"])
        pickup_latitude = float(data["pickup_latitude"])
        pickup_hour = int(data["pickup_hour"])
        pickup_day = int(data["pickup_day"])
        pickup_daytype = int(data["pickup_daytype"])
        distance_km = float(data["distance_km"])

        # ---------------- VALIDATION ----------------
        if passenger_count <= 0:
            return jsonify({"error": "Passenger count must be > 0"}), 400

        if distance_km <= 0:
            return jsonify({"error": "Distance must be positive"}), 400

        if vendor_id not in [1, 2]:
            return jsonify({"error": "Vendor ID must be 1 or 2"}), 400

        # ---------------- FEATURE ORDER (VERY IMPORTANT) ----------------
        features = np.array([[
            vendor_id,
            passenger_count,
            pickup_longitude,
            pickup_latitude,
            pickup_hour,
            pickup_day,
            pickup_daytype,
            distance_km
        ]])

        prediction = model.predict(features)[0]

        return jsonify({
            "seconds": round(float(prediction), 2),
            "minutes": round(float(prediction / 60), 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
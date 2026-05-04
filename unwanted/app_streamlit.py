import streamlit as st
import requests

st.title("🚖 Taxi Fare Prediction")

# Inputs
pickup_lat = st.number_input("Pickup Latitude", value=40.76)
pickup_lon = st.number_input("Pickup Longitude", value=-73.97)

dropoff_lat = st.number_input("Dropoff Latitude", value=40.65)
dropoff_lon = st.number_input("Dropoff Longitude", value=-73.88)

passenger_count = st.number_input("Passenger Count", min_value=1, max_value=6, value=1)

if st.button("Predict Fare"):

    data = {
        "pickup_lat": pickup_lat,
        "pickup_lon": pickup_lon,
        "dropoff_lat": dropoff_lat,
        "dropoff_lon": dropoff_lon,
        "passenger_count": passenger_count
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json=data
        )

        result = response.json()

        if "prediction" in result:
            st.success(f"💰 Estimated Fare: ${result['prediction']:.2f}")
        else:
            st.error(result.get("error", "Unknown error"))

    except:
        st.error("⚠️ Cannot connect to Flask API. Is it running?")
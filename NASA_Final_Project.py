import streamlit as st
import requests
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta

geolocator = Nominatim(user_agent = "My NASA Project", timeout = 10)
CROP_DATABASE = {
    "wheat": {"duration_days": 120, "min_moisture": 0.3, "max_temp": 25.0, "min_temp": 3.0 },
    "rice": {"duration_days": 110, "min_moisture": 0.6, "max_temp": 35.0, "min_temp": 10.0 },
    "cotton": {"duration_days": 150, "min_moisture": 0.2, "max_temp": 37.0, "min_temp": 12.0 },
    "sugarcane": {"duration_days": 360, "min_moisture": 0.55, "max_temp": 38.0, "min_temp": 10.0 },
    "maize": {"duration_days": 115, "min_moisture": 0.35, "max_temp": 33.0, "min_temp": 5.0 },
    "gram": {"duration_days": 95, "min_moisture": 0.15, "max_temp": 30.0, "min_temp": 2.0 },
    "potato": {"duration_days": 105, "min_moisture": 0.45, "max_temp": 24.0, "min_temp": 2.0 },
    "mango": {"duration_days": 365, "min_moisture": 0.25, "max_temp": 42.0, "min_temp": 5.0 }
}

st.set_page_config(page_title = "Kisaan Agricultute Intelligence", page_icon = "🧑‍🌾", layout = "wide")

st.title("🌾 Kisaan: Climate Resilient Agro Intelligence")
st.subheader("Climate Simulator & Decision Maker")
st.sidebar.header("Planting Parameters")

st.session_state.df = pd.DataFrame({
    "lat": [30.1956],
    "lon": [71.4753]
}
)

#asking user to enter farming location
place = st.sidebar.text_input("Enter Your Farming Location", value="Multan")
location = geolocator.geocode(place)
if place:
    st.session_state.df = pd.DataFrame({
        "lat": [location.latitude],
        "lon": [location.longitude]
        }
        )



#asking user what crop they want grow
crop = st.sidebar.selectbox(
    "Choose Your Crop:",
    ("wheat", "rice", "cotton", "sugarcane", "maize", "gram", "potato", "mango")
)

#asking user when they want to start growing
date = st.sidebar.date_input("Your Planned Sowing Date", datetime(2025, 12, 25))
usable_date = date.strftime("%m-%d")
usable_year = date.strftime("%Y")

#allowing user to stress test the temp the crop can handle
change = st.sidebar.slider("Simulate Temp Spike (Celsius)", -5.00, 5.00, 0.00, 1.00)

#button to start processing the data
run_simulation = st.sidebar.button("CLick To Start Simulation")
if not run_simulation:
    st.map(st.session_state.df, zoom = 10, width = "stretch")
else:
    historical_years = [2025, 2024, 2023]
    historical_moisture = []
    historical_hightemp = []
    historical_lowtemp = []
    choosen_crop_data = CROP_DATABASE[crop]
    #collecting recent years data 
    with st.spinner("⏳ Pulling Recent Year Data"):
        for years in historical_years:
            year = str(years)
            month , date = usable_date.split("-")
            date_final = year + month + date
            start_date = datetime.strptime(date_final, "%Y%m%d")
            days_to_add = choosen_crop_data["duration_days"]
            end_date = start_date + timedelta(days = days_to_add)
            url = "https://power.larc.nasa.gov/api/temporal/daily/point"
            param = {
                "start" : start_date.strftime("%Y%m%d"),
                "end": end_date.strftime("%Y%m%d"),
                "latitude": location.latitude,
                "longitude": location.longitude,
                "parameters": "TS,T2M_MIN,GWETPROF",
                "community": "ag",
                "format": "json",
                }
            response = requests.get(url, params = param)
            final_response = response.json()
            data = final_response["properties"]["parameter"]
            moisture = data["GWETPROF"]
            lowt = data["T2M_MIN"]
            hight = data["TS"]

            for date_key in moisture.keys():
                historical_moisture.append(moisture[date_key])
                historical_hightemp.append(hight[date_key] + change)
                historical_lowtemp.append(lowt[date_key])
        min_moisture = min(historical_moisture)
        max_temp = max(historical_hightemp)
        min_temp = min(historical_lowtemp)

    st.markdown("📊 Recent 3 year Climate Data Analysis Finished")

    data = pd.DataFrame(
        {
        "🌡️ Highest Temperature Recorded °C": [f"{max_temp:.2f}"],
        "💧 Lowest Moisture Level Recorded ": [f"{min_moisture:.3f}"],
        "❄️ Lowest Frost Level Detected °C": [f"{min_temp:.2}"]
        }
    )
    st.table(data)

    #checking if that crop can now be grown
    passed = True
    if min_moisture < choosen_crop_data["min_moisture"]:
        passed = False 
    elif min_temp < choosen_crop_data["min_temp"]:
        passed = False
    elif max_temp > choosen_crop_data["max_temp"]:
        passed = False
        
    found = False
    if not passed:
        days_to_add = choosen_crop_data["duration_days"]
        month , date = usable_date.split("-")
        start = datetime.strptime(f"{usable_year}{month}{date}", "%Y%m%d")
        end_date = start + timedelta(days = days_to_add)
        st.warning(f"{crop.upper()} CANNOT BE GROWN FROM {start.strftime("%Y-%m-%d")} TO {end_date.strftime("%Y-%m-%d")}")
        alternate = []
        new_crop = []
        for diff_crop in CROP_DATABASE:
            features = CROP_DATABASE[diff_crop]
            if features["duration_days"] <= choosen_crop_data["duration_days"] and min_moisture > features["min_moisture"] and min_temp > features["min_temp"] and max_temp < features["max_temp"]:
                alternate.append(diff_crop)
                new_crop.append(diff_crop)
                found = True
    else:
        st.balloons()
        st.success(f"CLIMATE TESTING FOR {crop} PASSED")

    if found:
        for crops in new_crop:
            days_to_add = CROP_DATABASE[crops]["duration_days"]
            month , date = usable_date.split("-")
            start = datetime.strptime(f"{usable_year}{month}{date}", "%Y%m%d")
            end_date = start + timedelta(days = days_to_add)
            st.success(f"{crops.upper()} CAN BE GROWN INSTEAD FROM {start.strftime("%Y-%m-%d")} TO {end_date.strftime("%Y-%m-%d")}")
    else:
        st.info(f"No Alternate Crops For this Season in Baseline Crops")


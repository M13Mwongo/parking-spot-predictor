import cmdstanpy
import streamlit as st
import pandas as pd
import pydeck as pdk
import pickle
import joblib

MAPBOX_STYLE = "mapbox://styles/mmm97/cl2m0aoax00a214kszmx0eefu"

# Mock car park data
car_parks_data = {
    'name': ['Car Park A', 'Car Park B', 'Car Park C'],
    'latitude': [-33.8688, -33.7490, -33.7969],
    'longitude': [151.2093, 151.2313, 150.9224],
    'likelihood': [0.8, 0.6, 0.9],
    'image_URL': ['https://via.placeholder.com/150', 'https://via.placeholder.com/150', 'https://via.placeholder.com/150']
}

car_parks_df = pd.DataFrame(car_parks_data)

# Specifying the carparks layer
car_parks_layer = pdk.Layer(
    "ScatterplotLayer",
    data=car_parks_df,
    get_position=["longitude", "latitude"],
    get_radius=200,
    get_fill_color=[255, 0, 0],
    pickable=True,
)

# Specifying custom map theme
map_layer = pdk.Deck(
  map_style=MAPBOX_STYLE,
  initial_view_state=pdk.ViewState(latitude=-33.8, longitude=151.07, zoom=10.2, bearing=0, pitch=0),
  layers=[car_parks_layer])

# Streamlit app
st.sidebar.title("Australian Car Park Finder")
st.sidebar.write("""
    Welcome to the Australian Car Park Finder app. 
    Select a future date and click on 'Process Data' to find available car parks and the likelihood of finding a parking spot.
""")
# Date picker
selected_date = st.sidebar.date_input("Select Date", min_value=pd.Timestamp.today())

# Time picker
selected_time = st.sidebar.time_input("Select Time")
# Button to process data
if st.sidebar.button("Process Data"):
    # Loading model
    # with open('./model/model.pkl', 'rb') as f:
    #     model = pickle.load(f)
    model = joblib.load('./model/model.pkl') 
    # Here you would process the data based on the selected date
    processed_data = model.predict(selected_date, selected_time)
    st.write(processed_data)

st.write("Map of New South Wales (NSW) with car parks marked:")

# Display car park locations on a map
st.pydeck_chart(map_layer)
# st.map(data=car_parks_df)

# # Placeholder for results
# results_placeholder = st.empty()
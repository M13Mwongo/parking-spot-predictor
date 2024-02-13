import streamlit as st
import pandas as pd
import pydeck as pdk

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

# Button to process data
if st.sidebar.button("Process Data"):
    # Here you would process the data based on the selected date
    # For demonstration purposes, let's assume we're just filtering car parks randomly
    selected_car_parks = car_parks_df.sample(n=2)

    # Create PyDeck ScatterplotLayer for car park locations
    car_parks_layer = pdk.Layer(
        "ScatterplotLayer",
        data=selected_car_parks,
        get_position=["Longitude", "Latitude"],
        get_radius=200,
        get_fill_color=[255, 0, 0],
        pickable=True,
    )

    # Create PyDeck Deck
    map_layer = pdk.Deck(
        map_style=MAPBOX_STYLE,
        initial_view_state=pdk.ViewState(latitude=-33.8, longitude=151.07, zoom=10.2, bearing=0, pitch=0),
        layers=[car_parks_layer],
    )

    # Display car park locations on a map
    st.write("Map of New South Wales (NSW) with selected car parks marked:")
    st.pydeck_chart(map_layer)

    # Display images when a car park marker is clicked
    for i, row in selected_car_parks.iterrows():
        st.image(row['Image_URL'], caption=row['Name'])

st.write("Map of New South Wales (NSW) with car parks marked:")

# Display car park locations on a map
st.pydeck_chart(map_layer)

# # Placeholder for results
# results_placeholder = st.empty()
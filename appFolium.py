import streamlit as st
import pandas as pd
import pydeck as pdk
import pickle
import folium
from streamlit_folium import st_folium
# Force Wide mode
st.set_page_config(
    page_title="Car Park Finder",
    page_icon=":car:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Variables
sydney_center_coords = [-33.865143, 151.2099]
# Initialize session state
if 'markers' not in st.session_state:
    st.session_state['markers'] = []
    
# Loading data
df_carparks = pd.read_json('./data/carparks_coords_spots.json')

# Creating folumn map
m = folium.Map(location=sydney_center_coords, zoom_start=10,max_zoom=40)

# Creating feature group for markers
fg = folium.FeatureGroup(name="Car Park Markers")
for marker in st.session_state['markers']:
    fg.add_child(marker)

# ----------------------------Sreamlit app----------------------------

st.sidebar.title("Australian Car Park Finder")
st.sidebar.write("""
    Welcome to the Australian Car Park Finder app. 
    Select a future date and click on 'Process Data' to find available car parks and the likelihood of finding a parking spot.
""")

# Carpark
selected_carpark = st.sidebar.selectbox("Select Car Park", df_carparks['CarParkName'],None)

# Loading marker once carpark is selected
if selected_carpark:
    cp = df_carparks.loc[df_carparks['CarParkName'] == selected_carpark]
    cp_coords = [cp['longitude'].iloc[0], cp['latitude'].iloc[0]]
    
    # Defining point/marker on map
    marker = folium.Marker(location=[cp['longitude'].iloc[0], cp['latitude'].iloc[0]], tooltip=selected_carpark,icon=folium.Icon(color='blue',icon='map-pin',prefix='fa',angle=25))
    marker.add_to(fg)
    
    # # Add to session state
    # st.session_state['markers'].append(folium.Marker(location=cp_coords, popup=selected_carpark))
    m.location = cp_coords
    m.zoom_start = 12

# Render Folium map in Streamlit
st_data = st_folium(m,width='100%',height=600,feature_group_to_add=fg,key='new')

# Aesthetics
st.divider()

# Date picker
input_date = st.sidebar.date_input('Select a date:', pd.to_datetime('today'))

# Button to process data
if st.sidebar.button("Process Data"):
    model_path = f"./model/{selected_carpark}.pkl"
    
    # Loading model
    with open(model_path, 'rb') as f:
        forecast_model = pickle.load(f)
    # Combine date and time into a single datetime object
    input_datetime = pd.to_datetime(str(input_date) + ' ' + str(pd.to_datetime("00:00:00").time()))

    # Display predictions for each facility
    st.header('Predictions:')
    result = forecast_model.loc[forecast_model['ds_forecast'] == input_datetime]
    
    # Necessary dataframes
    df_carpark_result = df_carparks[df_carparks['CarParkName'] == selected_carpark]
    
    # Display predictions
    aval = round(result[f'yhat_{selected_carpark}'],0)
    total = df_carpark_result['spots'].iloc[0]
    occupancy = total-aval
    
    
    col1,col2 = st.columns(2)
    
    col1.metric("Number of parking spots available",round(result[f'yhat_{selected_carpark}'],0))
    col1.metric("Total Parking Spots in Parking Lot",df_carpark_result['spots'].iloc[0])
    
    col2.metric("Occupancy",occupancy)
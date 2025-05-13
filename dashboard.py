from altair.vegalite.v5.display import here
# import plotly.express as px
# import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd
import streamlit as st
from datetime import datetime
import requests
from io import BytesIO
# import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Data Visualization', page_icon=':tokyo_tower:', layout = 'wide')
current_date = datetime.today().date()

st.header(':tokyo_tower: LTE Daily Report')
st.write(current_date)

# URL of the file on Dropbox (direct download link)
dropbox_url = "https://www.dropbox.com/scl/fi/r5krz6tt3xzhw1qpkc1nm/Site_Report_May_13_2025.xlsx?rlkey=g715jsbx1wem02tsoah2631ev&st=7o5tc2cg&dl=1"  # Replace with your actual URL

# Function to download and read the file, caching the download and reading process
@st.cache_data
def load_data_from_dropbox(url):
    response = requests.get(dropbox_url)
    # Check if the request was successful
    if response.status_code == 200:
        # Read the file into a pandas DataFrame (assuming it's a CSV file)
        file = BytesIO(response.content)
        df = pd.read_excel(file, sheet_name= 'Site Report')
        df.index = df.index + 1  # Adjust the index to start from 1
        return df

    else:
        st.error("Failed to download file. Please check the link or your internet connection.")
        return None

# Load data with caching    
df = load_data_from_dropbox(dropbox_url)

# If data is loaded successfully, proceed with further processing
if df is not None:
    # Total site status count
    total = df['Site Status'].value_counts()

    # Site Status Based on Network
    network_df = df.groupby('Network')['Site Status'].value_counts().reset_index(name= 'Count')
    network_df.index = range(1, len(network_df) + 1)

    # Total Sites Down By Network
    network_down = network_df[(network_df['Site Status'] == 'Down')]
    network_down.index = range(1, len(network_down) + 1)

    # Site Status Based on Region
    region_df = df.groupby('Region')['Site Status'].value_counts().reset_index(name='Count')
    region_df.index = range(1, len(region_df) + 1)

    # Total Sites Down By Region
    region_down = region_df[region_df['Site Status'] == 'Down']
    region_down.index = range(1, len(region_down) + 1)

    # Site Status Based on Province
    province_df = df.groupby('Province')['Site Status'].value_counts().reset_index(name='Count')
    province_df.index = range(1, len(province_df) + 1)

    # Total Sites Down on Province
    province_down = province_df[province_df['Site Status'] == 'Down']
    province_down.index = range(1, len(province_down) + 1)
             

# Filtering down type with province name
# selected_down_type = st.radio('Select Site Down Features', ['Down', 'Site Down. Manually Locked', 'Site Down. Not Working due to Error'])
# selected_down_pro = st.slider('Select Province', min_value= 1, max_value=7)
# filtered_down_type = df[(df['Site Report'] == selected_down_type) & (df['Province'] == selected_down_pro)]
# filtered_down_type = filtered_down_type.drop(columns=['Network', 'Region','Site Status'])


# Filtering up type with province name
# selected_up_type = st.selectbox('Select Site Up with Cell Not Working Feature', ['Up', 'Site Up; 1 Cells Manually Locked', 'Site Up; 1 Cells not Working due to Alarm', 'Site Up; 2 Cells Manually Locked', 'Site Up; 2 Cells not Working due to Alarm', 'Site Up; 3 Cells Manually Locked', 'Site Up; 3 Cells not Working due to Alarm'])
# selected_up_pro = st.slider('Select Province', min_value= 1, max_value=7, value= 3)
# filtered_up_type = df[(df['Site Report'] == selected_up_type) & (df['Province'] == selected_up_pro)]
# filtered_up_type = filtered_up_type.drop(columns=['Network', 'Region', 'Site Status'])


st.sidebar.markdown('# Info')
selected_category = st.sidebar.radio('Select Category', ['Overview', 'Network', 'Region', 'Province', 'Down Feature', 'Up Feature'])
if selected_category == 'Overview':
    st.write('Total Sites Overview', total)

elif selected_category == 'Network':
    st.write('Total Sites Down By Network Type', network_down)
    st.write('Site Status Based on Networks', network_df)

elif selected_category == 'Region':
    st.write('Total Sites Down on Region', region_down )
    st.write('Sites Status Based on Region', region_df )

elif selected_category == 'Province':
    st.write('Total Sites Down on Province', province_down)
    st.write('Site Status Based on Province', province_df)

elif selected_category == 'Down Feature':
    selected_down_type = st.radio('Select Site Down Features', ['Down', 'Site Down. Manually Locked', 'Site Down. Not Working due to Error'])
    selected_down_pro = st.slider('Select Province', min_value= 1, max_value=7)
    filtered_down_type = df[(df['Site Report'] == selected_down_type) & (df['Province'] == selected_down_pro)]
    filtered_down_type = filtered_down_type.drop(columns=['Network', 'Region','Site Status'])
    filtered_down_type.index = range(1, len(filtered_down_type) + 1)
    st.write('Sites Down By Features & Province', filtered_down_type )

elif selected_category == 'Up Feature':
    selected_up_type = st.selectbox('Select Site Up with Cell Not Working Feature', ['Up', 'Site Up; 1 Cells Manually Locked', 'Site Up; 1 Cells not Working due to Alarm', 'Site Up; 2 Cells Manually Locked', 'Site Up; 2 Cells not Working due to Alarm', 'Site Up; 3 Cells Manually Locked', 'Site Up; 3 Cells not Working due to Alarm'])
    selected_up_pro = st.slider('Select Province', min_value= 1, max_value=7, value= 3)
    filtered_up_type = df[(df['Site Report'] == selected_up_type) & (df['Province'] == selected_up_pro)]
    filtered_up_type = filtered_up_type.drop(columns=['Network', 'Region', 'Site Status'])
    filtered_up_type.index = range(1, len(filtered_up_type) + 1)
    st.write('Sites Up By Features & Province', filtered_up_type)



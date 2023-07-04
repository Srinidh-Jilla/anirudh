import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
from st_on_hover_tabs import on_hover_tabs
import seaborn as sns
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide")

# Load the data
restaurants_df = pd.read_csv('restaurants.csv')
rental_spaces_df = pd.read_excel('rental_spaces2.xlsx')

#Read CSS File
with open('style.css') as file:
    css_content = file.read()

#Background Image
def add_bg_from_url():
    st.markdown(
#         '<style>' + open('/Users/kanishkramagiri/Desktop/AA/style.css').read() + '</style>'
         f"""
         <style>
         .stApp {{
             background-image: url("");
             background-attachment: fixed;
             background-size: cover
         }}
         {css_content}
         </style>
         """,
         unsafe_allow_html=True
     )
add_bg_from_url() 


#########################SIDEBAR###################################
# Sidebar
with st.sidebar:
    tabs = on_hover_tabs(tabName=['Home', 'Recommendations' , 'Locations' , 'Advanced Analytcs'], 
                         iconName=['home', 'analytics' , 'map' , 'explore'], default_choice=0)

    
    
#########################HOME################################    
if tabs =='Home':
    center_style = """
    <style>
        .centered-text {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 60vh;
            text-align: center;
            font-size: 100px;
            font-weight: bold;
        }
    </style>
    <style>
        .sub-text {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 30vh;
            text-align: center;
            font-size: 50px;
            font-weight: bold;
        }
    </style>
    """
    # Add the CSS style to the Streamlit app
    st.write(center_style, unsafe_allow_html=True)
    # Use st.markdown with the added CSS class
    st.markdown('<div class="centered-text">DineSite</div>', unsafe_allow_html=True)
    
    
######################Recommendations##############################    
elif tabs == 'Recommendations':
    st.title('Get Recommendations')

    # Load the datasets
    restaurants_df = pd.read_csv('restaurants.csv')
    rental_spaces_df = pd.read_excel('rental_spaces2.xlsx')

    # Create four columns for the selection boxes
    col1, col2, col3, col4 = st.columns([3,3,3,1])  # Adjust the proportions

    # Create input fields for the user
    with col1:
        cuisine = st.selectbox('Choose a cuisine', ['Irish','Coffee','Japanese','Fast food','Pizza','European','Chinese','Mediterranean','Asian','Spanish','Italian','Indian','Bar','Healthy','Mexican','Brazilian'])
    with col2:
        type = st.selectbox('Choose a type', ['Cafe', 'Casual Dining', 'Fastfood', 'Fine Dining', 'Restopub'])
    with col3:
        affordability = st.selectbox('Choose affordability', ['Affordable', 'Costly', 'Cheap'])
    with col4:
        search = st.button('Search')

    if search:
        # Filter the dataframe based on the input parameters
        filtered_df = restaurants_df[
            (restaurants_df['Cuisine'] == cuisine) & 
            (restaurants_df['Type'] == type) & 
            (restaurants_df['Affordability'] == affordability)
        ]

        # Group by neighbourhood and get the top 5 neighbourhoods
        grouped_df = filtered_df.groupby('Neighbourhood').size().reset_index(name='Count')
        sorted_df = grouped_df.sort_values('Count', ascending=False)
        top_neighbourhoods = sorted_df['Neighbourhood'].head(5).tolist()

        # Display the top 5 neighbourhoods with expanders
        st.markdown("## Recommended Neighbourhoods:")
        for i, neighborhood in enumerate(top_neighbourhoods, start=1):
            st.markdown(f"**{i}. {neighborhood}**")


elif tabs == 'Locations':
    st.title('Find Properties on Map')

    # Create three columns for the selection boxes
    col1, col2 = st.columns([7,3]) # Adjust the proportions

    # Create input fields for the user
    with col1:
        neighborhood = st.selectbox('Choose a neighbourhood', rental_spaces_df['Neighbourhood'].unique())
    with col2:
        category = st.selectbox('Choose a property category', ['To Lease', 'To Sell'])
    
    # Filter the dataframe based on the input parameters
    filtered_df = rental_spaces_df[
        (rental_spaces_df['Neighbourhood'] == neighborhood) &
        (rental_spaces_df['Category'] == category)
    ]

    # Create the map using folium
    m = folium.Map(location=[filtered_df['Latitude'].mean(), filtered_df['Longitude'].mean()], zoom_start=13)

    # Add a marker for each property in the filtered dataframe
    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Address']}, {row['Rent']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # Display the map in Streamlit
    folium_static(m)


 ######################ABOUT########################################    
elif tabs =='About':
    st.title("About the Dashboard")
    video_file = open('/Users/kanishkramagiri/Desktop/AA/Video.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)           







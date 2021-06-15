import streamlit as st
from PIL import Image

import dashboard 
import cognition_scores
import general

# Config
image = Image.open("app/images/ART-4.png")
st.set_page_config(layout="wide")

PAGES = {
    "Dashboard": dashboard,
    "General Insights": general,
    "Your Cognition Scores": cognition_scores
}

def local_css(file_name): 
    with open(file_name) as f: 
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("app/style.css")   

# Sidebar
st.sidebar.image(image, use_column_width=False, width=200)

st.cache()
participant_id = st.sidebar.text_input('Participant ID', 'BGCJFHFI')

selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]

if not participant_id == "":
    page.content(participant_id)
else: 
    st.title("Please input your participant_id")

       






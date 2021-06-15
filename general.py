import streamlit as st
import pandas as pd
import numpy as np
import get_api_data

def content(participant_id):
    col1, col2 = st.beta_columns(2)
    col1.title("General Recommendations")
    col1.write("Here you can see the general affect of behaviour on you productivity in the workplace")
    
    col2.selectbox('Select a line to filter',["Sleep", "Activity"])
    
    #df = geta_api_data.get_line_chart_data()
    #st.line_chart(df)
    
    st.markdown("Generally speaking * **...** * is the most important factor when it comes to * **...** *")
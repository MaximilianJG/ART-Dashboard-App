import streamlit as st
import pandas as pd
import numpy as np

from get_api_data import get_overlayed_zscore_data
from plot_api_data import make_z_plot_overlay

import matplotlib.pyplot as plt
import seaborn as sns
#from ART_MCK.participant_plots import plot_score
# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np
# from datetime import timedelta, date

def content(participant_id):
        
    col1, col2 = st.beta_columns(2)
    
    col1.title('Dashboard')
    col1.write('Welcome to your dashboard')
    
    #Dashboard Filter
    filter = col2.selectbox('Select a line to filter',["1 Week", "6 Month", "1 Year", "All"])
    
    df = get_overlayed_zscore_data(participant_id)
    
    #st.line_chart(df)    
    fig, ax = make_z_plot_overlay(df) ## passing a dataframe
    
    st.pyplot(fig)
import streamlit as st
import pandas as pd
import numpy as np

from get_api_data import get_overlayed_zscore_data
from plot_api_data import make_z_plot_overlay, plot_z_score, colors
        
def content(participant_id):
    col1, col2 = st.beta_columns(2)#
    
    col1.title('Cognition Scores')
    col1.write('Welcome to your cogntion scores')
    
    filter_column = col2.selectbox('Select a line to filter',["Sleep Duration (mins)", "Active Minutes"])
    # 1st Row
    col1, col2 = st.beta_columns(2)#
    
    col1.header("Reaction Time")
    column = "Reaction Time RT"
    df = get_overlayed_zscore_data(participant_id)
    fig, ax = plot_z_score(df, column, colors[column], dashed=False, fig_ax=None)
    fig, ax = plot_z_score(df, filter_column, colors["Other Score"], dashed=False, fig_ax=(fig, ax))
    col1.pyplot(fig)
     
   
    col2.header("Decision Making")
    column = "Ink ID Combo Score"
    df = get_overlayed_zscore_data(participant_id)
    fig, ax = plot_z_score(df, column, colors[column], dashed=False, fig_ax=None)
    fig, ax = plot_z_score(df, filter_column, colors["Other Score"], dashed=False, fig_ax=(fig, ax))
    col2.pyplot(fig)
    
    # 2nd Row
    col1, col2 = st.beta_columns(2)
    
    col1.header("Short Term Memory")
    column = "Letter Match Combo Score"
    df = get_overlayed_zscore_data(participant_id)
    fig, ax = plot_z_score(df, column, colors[column], dashed=False, fig_ax=None)
    fig, ax = plot_z_score(df, filter_column, colors["Other Score"], dashed=False, fig_ax=(fig, ax))
    col1.pyplot(fig)
    
    col2.header("Distractibility")
    column = "Arrows Combo Score"
    df = get_overlayed_zscore_data(participant_id)
    fig, ax = plot_z_score(df, column, colors[column], dashed=False, fig_ax=None)
    fig, ax = plot_z_score(df, filter_column, colors["Other Score"], dashed=False, fig_ax=(fig, ax))
    col2.pyplot(fig)
    
    
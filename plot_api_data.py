import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np

import datetime as dt

from scipy.stats import zscore
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime as dt
from datetime import date, timedelta

plt.switch_backend('Agg')

def columns_available(df):
    df = df.select_dtypes(include="float64")
    cols_list = df.iloc[:,4:].columns
    return cols_list

def dt_string_to_dt(datetime_string):
    datetime_string.to_pydatetime()
    return datetime_string.to_pydatetime()

def previous_monday(input_date):
    """Return date of last week's start date (i.e. last Monday's day). 
    If the entered date is the start of the week, the entered date is returned."""
    weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday") # if need to return weekday name
    today_date = date.today()
    last_monday_date = input_date - timedelta( days= (input_date.weekday() - 0) % 7) # 0 = Monday
    return last_monday_date

def set_plot_date_range(from_date, to_date):
    from_date_prev_mon = previous_monday(from_date)
    
    date_range = to_date - from_date_prev_mon# + 1
    date_range_float = date_range / timedelta(days = 1)
    ticks = date_range_float // 7 + 1
    
    from_date += timedelta(days = 1) * -1
    to_date += timedelta(days = 1)
    return from_date, to_date

# Z-score plot functions:
def initiate_z_score_plot(df, figsize=(15,10)):
    df["Date"] = df["Date"].map(dt_string_to_dt) # Date from json
    sns.set_style("dark")
    fig, ax = plt.subplots(figsize=figsize)

    # Plot Mean
    ax = sns.lineplot(data=df, x='Date', y=0, label='Mean', color='blue', alpha = 0.6, dashes=[(1, 0)], style=True, legend=False)
    # Plot Standard Deviation
    ax = sns.lineplot(data=df, x='Date', y=1, label='± 1 std', color='red', alpha = 0.8, dashes=[(5, 5)], style=True, legend=False)
    ax = sns.lineplot(data=df, x='Date', y=-1, color='red', alpha = 0.8, dashes=[(5, 5)], style=True, legend=False);
    
    # Set Date Range
    from_date, to_date = previous_monday(df.Date.min()+timedelta(days=-7)), previous_monday(df.Date.max()+timedelta(days=7))
    ax.set_xlim(from_date, to_date)

    # x-axis Date Format and Ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='both', width=2)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=4, color='r')
    plt.xticks(rotation=90)
    ax.grid() #alpha=0.2
    
    # Axis labels:
    ax.set_xlabel ("Date", fontsize=12, fontweight='bold')
    ax.set_ylabel (f"Z-Score", fontsize=12, fontweight='bold')
    
    ax.set_title(f"Z-Score(s) for Participant: {df['Participant ID'].values[0]}", fontsize=15, fontweight='bold')
    return fig, ax

def plot_z_score(df, col, color, dashed=False, fig_ax=None, figsize=(10, 5)):
    # Plot Trend Data:
    if fig_ax:
        fig, ax = fig_ax
    else:
        fig, ax = initiate_z_score_plot(df, figsize=figsize)
    
    df["Date"] = df["Date"].map(dt_string_to_dt) # Date from json
    ax = sns.scatterplot(data=df, x='Date', y=col+' anomaly_zscores' , label="Anomalies", color="red")
    ax = sns.lineplot(data=df, x='Date', y=col+' zscore', label=col, color=color, alpha=0.5, dashes=[(2, int(dashed))], style=True, legend=False)
    ax.legend()
    return fig, ax

def make_z_plot_overlay(df):
    """Returns dictionary of dfs for a participant's plot overlay of z-scores"""
    
    colors = {'Reaction Time RT'    :'tab:blue',
          'Letter Match Combo Score':'tab:orange',
          'Arrows Combo Score'      :'tab:green',
          'Shape Match Combo Score' :'tab:red',
          'Ink ID Combo Score'      :'tab:purple',
          'Activity Score'          :'tab:brown',
          'Sleep Score'             :'tab:pink',
          'Other Score'             :'tab:gray'}

    #Initialize plot
    fig, ax = initiate_z_score_plot(df)
    
    df["Date"] = df["Date"].map(dt_string_to_dt) # Date from json
    
    # overlay column scores
    column_names = ['Reaction Time RT', 'Letter Match Combo Score', 'Arrows Combo Score', 'Ink ID Combo Score']
    for column_name in column_names:
        fig, ax = plot_z_score(df, column_name, colors[column_name], dashed=False, fig_ax=(fig, ax))
        
    return fig, ax

# Cognition score plot functions:
def initiate_score_plot(df, col, fig_size=(15,10)):
    df["Date"] = df["Date"].map(dt_string_to_dt) # Date from json
    #sns.set_style("dark")
    fig, ax = plt.subplots(figsize=fig_size)

    # Plot Mean
    ax = sns.lineplot(data=df, x='Date', y=col+' mean', label='Mean', color='blue', alpha = 0.6, dashes=[(1, 0)], style=True, legend=False)
    # Plot Standard Deviation
    ax = sns.lineplot(data=df, x='Date', y=col+' plus_1std', label='± 1 std', color='red', alpha = 0.8, dashes=[(5, 5)], style=True, legend=False)
    ax = sns.lineplot(data=df, x='Date', y=col+' minus_1std', color='red', alpha = 0.8, dashes=[(5, 5)], style=True, legend=False);
    
    # Set Date Range
    from_date, to_date = previous_monday(df.Date.min()+timedelta(days=-7)), previous_monday(df.Date.max()+timedelta(days=7))
    ax.set_xlim(from_date, to_date)

    # x-axis Date Format and Ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='both', width=2)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=4, color='r')
    plt.xticks(rotation=90)
    ax.grid()
    
    # Axis labels:
    ax.set_xlabel ("Date", fontsize=12, fontweight='bold')
    ax.set_ylabel (f"Cognition Score", fontsize=12, fontweight='bold')
    
    return fig, ax

def plot_score(df, col, color, dashed=False, fig_ax=None):
    # Plot Trend Data:
    if fig_ax:
        fig, ax = fig_ax
    else:
        fig, ax = initiate_score_plot(df, col)
        
    # y=df.iloc[:,2]
    ax = sns.scatterplot(data=df, x='Date', y=col+' anomaly_scores', label="Anomalies", color="red")
    ax = sns.lineplot(data=df, x='Date', y=col, label=col, color=color, alpha=0.5, dashes=[(2, int(dashed))], style=True, legend=False)
    
    ax.set_title(f"{col} trend for participant {df['Participant ID'].values[0]}", fontsize=15, fontweight='bold')
    ax.legend()
    return fig, ax

colors = {'Reaction Time RT'        :'tab:blue',
          'Letter Match Combo Score':'tab:orange',
          'Arrows Combo Score'      :'tab:green',
          'Shape Match Combo Score' :'tab:red',
          'Ink ID Combo Score'      :'tab:purple',
          'Activity Score'          :'tab:brown',
          'Sleep Score'             :'tab:pink',
          'Other Score'             :'tab:gray'}

score_label = {'Reaction Time RT'   :'RT Score',
          'Letter Match Combo Score':'Letter Score',
          'Arrows Combo Score'      :'Arrows Score',
          'Shape Match Combo Score' :'Shape Score',
          'Ink ID Combo Score'      :'Ink ID Score',
          'Activity Score'          :'Activity Score',
          'Sleep Score'             :'Sleep Score',
          'Other Score'             :'Other Score'}




# if __name__ == "__main__":
    
#     pass
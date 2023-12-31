import pdb

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import random

from db.db_connector import DB

db = DB()

SEENONS_COLORS = [
    '#00A891',  # Primary green
    '#235561',  # Dark blue
    '#F3456A',  # Action magenta
    '#97DCD0',  # Mid green
]

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
st.set_page_config(layout="wide")
st.header("Home IoT Dashboard")

st.subheader("Temperature and humidity")

measurements = db.get_measurements()

MAIN_COLS = ['timestamp', 'key', 'value', ]
METRICS = ['temp', 'humidity', 'pm_10', 'pm_25',]

df = pd.DataFrame(measurements, columns=['id', 'place', 'room', 'timestamp', 'key', 'value', 'created_at'])

TABS = ['Main floor', 'Basement', 'Attic']

tab1, tab2, tab3 = st.tabs(TABS)


def get_random_colors():
    COLOR = SEENONS_COLORS.copy()
    random.shuffle(COLOR)
    return COLOR


def plot_ts_value(df, key='temp', max_value = None, func=px.line):
    if type(key) == str:
        fig = func(df[df['key'] == key],
                   x='timestamp',
                   y='value',
                   color='room',
                   title=key,
                   color_discrete_sequence=get_random_colors())

    for line in df[(df['timestamp'].dt.hour == 0) & (df['timestamp'].dt.minute == 0)].index:
        fig.add_vline(x=df.loc[line]['timestamp'], line_width=1, line_dash="dash", line_color="green")
    if max_value:
        fig.update_layout(yaxis_range=[0, max(max_value + max_value * 0.1, df[df['key'] == key]['value'].max())])
        # Add horizontal line with max value
        fig.add_hline(y=max_value, line_width=1, line_dash="dash", line_color="red")

    if key == 'temp':
        fig.update_layout(yaxis_range=[15, 35])
    fig.update_layout(autosize=True)
    return fig


def plot_box_value(df, key='temp'):
    fig = px.box(df[df['key'] == key],
                 color='room',
                 y='value',
                 title=key,
                 color_discrete_sequence=get_random_colors())
    fig.update_layout(autosize=True)
    return fig


graph = st.sidebar.selectbox(
    "Graph type",
    ("Dot", "Line")
)
func = px.line if graph == "Line" else px.scatter

init_date = st.sidebar.date_input('Initial date', value=df['timestamp'].max())
end_date = st.sidebar.date_input('End date', value=df['timestamp'].max())

if end_date < init_date:
    st.sidebar.error('Error: End date must fall after initial date.')

df = df[(df['timestamp'].dt.date >= init_date) & (df['timestamp'].dt.date < end_date + pd.Timedelta(days=1))]

def show_data(room):
    st.subheader(room.capitalize())
    # Show the last measurements for every key in big text
    if df[df['room'] == room].shape[0] > 0:
        cols = st.columns(len(METRICS))
        for i, met in enumerate(METRICS):
            cols[i].metric(label=met,
                       value=df[df['room'] == room].loc[df[df['room'] == room]['key'] == met]['value'].iloc[-1],
                       delta=round((df[df['room'] == room].loc[df[df['room'] == room]['key'] == met]['value'].iloc[-1] -
                                df[df['room'] == room].loc[df[df['room'] == room]['key'] == met]['value'].iloc[-2]), 2)
                       )
            cols[i].metric(label=f'Max {met}',
                          value=df[df['room'] == room].loc[df[df['room'] == room]['key'] == met]['value'].max(),
                           )
            cols[i].metric(label=f'Min {met}',
                            value=df[df['room'] == room].loc[df[df['room'] == room]['key'] == met]['value'].min(),
                            )
        

        fig = func(df[df['room'] == room].reset_index(),
                   x='timestamp',
                   y='value',
                   color='key',
                   color_discrete_sequence=get_random_colors(),
                   )
        # Plot vertical lines in 00:00 hours

        for line in df[(df['timestamp'].dt.hour == 0) & (df['timestamp'].dt.minute == 0)].index:
            fig.add_vline(x=df.loc[line]['timestamp'], line_width=1, line_dash="dash", line_color="green")

        #        for x in df[(df['timestamp'].dt.hour == 0) &
        #              (df['timestamp'].dt.minute == 0)]:
        #            fig.add_vline(x=x.index, line_width=3, line_dash="dash", line_color="green")
        fig.update_layout(
            autosize=False,
            height=400,
            width=900,
        )
        st.plotly_chart(fig)

        col1, col2 = st.columns(2)
        with col1:

            st.plotly_chart(plot_ts_value(df[df['room'] == room].sort_values(by='timestamp'),
                                          key='humidity',
                                          func=func))
            st.plotly_chart(plot_ts_value(df[df['room'] == room].sort_values(by='timestamp'),
                                          key='temp',
                                          func=func))
            st.plotly_chart(plot_ts_value(df[df['room'] == room].sort_values(by='timestamp'),
                                          key='pm_10',
                                          max_value = 40,
                                          func=func))
            st.plotly_chart(plot_ts_value(df[df['room'] == room].sort_values(by='timestamp'),
                                          key='pm_25',
                                          max_value = 20,
                                          func=func))
        with col2:

            st.plotly_chart(plot_box_value(df[df['room'] == room].sort_values(by='timestamp'), key='humidity'))
            st.plotly_chart(plot_box_value(df[df['room'] == room].sort_values(by='timestamp'), key='temp'))
            st.plotly_chart(plot_box_value(df[df['room'] == room].sort_values(by='timestamp'), key='pm_10'))
            st.plotly_chart(plot_box_value(df[df['room'] == room].sort_values(by='timestamp'), key='pm_25'))
    else:
        "There's no data yet! : D"
    



if len(df) == 0:
    st.error('Error: No data available for selected dates.')
else:
    with tab1:
        show_data(TABS[0].lower())
    with tab2:
        show_data(TABS[1].lower())
    with tab3:
        show_data(TABS[2].lower())


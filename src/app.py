import streamlit as st
import plotly.express as px
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

MAIN_COLS = ['place', 'room', 'timestamp', 'temperature', 'humidity', ]

df = pd.DataFrame(measurements, columns=['id', 'place', 'room', 'timestamp', 'temperature', 'humidity', 'created_at'])

tab1, tab2, tab3 = st.tabs(['Basement', 'Main floor', 'Attic'])


def get_random_colors():
    COLOR = SEENONS_COLORS.copy()
    random.shuffle(COLOR)
    return COLOR


def plot_ts_value(df, value='temperature', func=px.line):
    fig = func(df, x='timestamp', y=value, color='room', title=value, color_discrete_sequence=get_random_colors())
    # fig.update_xaxes(rangeslider_visible=True)
    return fig


def plot_box_value(df, value='temperature'):
    fig = px.box(df, color='room', y=value, title=value, color_discrete_sequence=get_random_colors())
    return fig


graph = st.sidebar.selectbox(
    "Graph type",
    ("Line", "Dot")
)
func = px.line if graph == "Line" else px.scatter

init_date = st.sidebar.date_input('Initial date', value=df['timestamp'].min())
end_date = st.sidebar.date_input('End date', value=df['timestamp'].max())

if end_date < init_date:
    st.sidebar.error('Error: End date must fall after initial date.')

df = df[(df['timestamp'].dt.date >= init_date) & (df['timestamp'].dt.date < end_date + pd.Timedelta(days=1))]

if len(df) == 0:
    st.error('Error: No data available for selected dates.')
else:
    with tab1:
        st.subheader("Basement")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_ts_value(df[df['room'] == 'basement'].sort_values(by='timestamp'),
                                          value='humidity',
                                          func=func))
            st.plotly_chart(plot_box_value(df[df['room'] == 'basement'].sort_values(by='timestamp'), value='humidity'))
            st.subheader("Last 60 measurements")
            st.write(df.tail(60).reset_index()[MAIN_COLS])
        with col2:
            st.plotly_chart(plot_ts_value(df[df['room'] == 'basement'].sort_values(by='timestamp'),
                                          value='temperature',
                                          func=func))
            st.plotly_chart(plot_box_value(df[df['room'] == 'basement'].sort_values(by='timestamp'), value='temperature'))
            st.subheader(f"Max temp")
            st.write(df.loc[[df['temperature'].idxmax()]][['timestamp', 'temperature', 'humidity']])
            st.subheader(f"Min temp")
            st.write(df.loc[[df['temperature'].idxmin()]][['timestamp', 'temperature', 'humidity']])
            st.subheader(f"Max humidity")
            st.write(df.loc[[df['humidity'].idxmax()]][['timestamp', 'temperature', 'humidity']])
            st.subheader(f"Min humidity")
            st.write(df.loc[[df['humidity'].idxmin()]][['timestamp', 'temperature', 'humidity']])

    with tab2:
        "There's no data yet! : D"
    with tab3:
        "There's no data yet! : D"

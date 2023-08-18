import streamlit as st
import plotly.express as px
import pandas as pd
import os

from db.db_connector import DB

db = DB()

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
st.set_page_config (layout="wide")

st.subheader("Temperature and humidity")
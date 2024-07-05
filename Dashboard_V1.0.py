import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="superStore", page_icon="line_chart",layout="wide")

st.title(":chart_with_upwards_trend: Core Performance Dash")
st.markdown("""<style>div.block-container {padding-top: 1rem;}</style>""",unsafe_allow_html=True)
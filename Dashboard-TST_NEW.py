import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# Set up the Streamlit page configuration
st.set_page_config(page_title="Core Performance Dashboards", page_icon="line_chart", layout="wide")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Define file paths
file_paths = {
    "Ericsson-Hourly": r"C:\Users\Kamiran.Gabriel\Desktop\MSC Hourly.xlsx",
    "Ericsson-Daily": r"C:\Users\Kamiran.Gabriel\Desktop\MSC Daily.xlsx",
    "Ericsson-BH": r"path_to_your_Ericsson_BH.xlsx",
    "Huawei-Hourly": r"C:\Users\Kamiran.Gabriel\Desktop\ALL_Query_3.xlsx",
    "Huawei-Daily": r"path_to_your_Huawei_Sub_Dash_2.xlsx",
    "Huawei-BH": r"path_to_your_Huawei_Sub_Dash_3.xlsx",
    "Nokia-Hourly": r"path_to_your_Nokia_Sub_Dash_1.xlsx",
    "Nokia-Daily": r"path_to_your_Nokia_Sub_Dash_2.xlsx",
    "Nokia-BH": r"path_to_your_Nokia_Sub_Dash_3.xlsx"
}

# Navigation function
def navigate(page):
    st.session_state.page = page

# Style settings
def apply_styles():
    st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .sidebar .sidebar-content { background-color: #f0f2f6; }
    .block-container {
        padding: 1rem;
        background-color: #CECECE;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .css-18ni7ap { background-color: #CECECE !important; }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        width: 40%;
        padding: 0.25rem;
        font-size: 16px;
        margin-bottom: 1rem;
    }
    .file-input, .file-uploader {
        padding: 1rem;
        font-size: 16px;
        width: 100%;
    }
    .stSidebar, .css-1lcbmhc { padding: 1rem; }
    .stDataFrame { margin: 0 auto; }
    </style>""", unsafe_allow_html=True)

# Function to read all sheets from an Excel file into a dictionary of DataFrames
def read_excel_sheets(file):
    xls = pd.ExcelFile(file)
    sheets = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        sheets[sheet_name] = df
    return sheets

# Function to detect the appropriate 'ELEM', 'SN', or 'NE Name' column
def detect_elem_column(df):
    elem_columns = ['ELEM', 'element', 'SN', 'NE Name']  # Add other possible column names
    for col in elem_columns:
        if col in df.columns:
            return col
    raise ValueError("No suitable 'ELEM' column found in the sheet.")

# Function to handle the Home page
def home_page():
    st.markdown(
        '<h1 style="color: #FF5733; font-size: 40px; padding-top: 28px;">🏠 Home Page</h1>',
        unsafe_allow_html=True
    )
    st.write("Welcome to the Core Performance Dashboard Application! Please select a dashboard to proceed.")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Ericsson Dash"):
            st.session_state.show_ericsson = not st.session_state.get('show_ericsson', False)
        if st.session_state.get('show_ericsson', False):
            if st.button("Ericsson-Hourly"):
                navigate("Ericsson-Hourly")
            if st.button("Ericsson-Daily"):
                navigate("Ericsson-Daily")
            if st.button("Ericsson-BH"):
                navigate("Ericsson-BH")

    with col2:
        if st.button("Huawei Dash"):
            st.session_state.show_huawei = not st.session_state.get('show_huawei', False)
        if st.session_state.get('show_huawei', False):
            if st.button("Huawei-Hourly"):
                navigate("Huawei-Hourly")
            if st.button("Huawei-Daily"):
                navigate("Huawei-Daily")
            if st.button("Huawei-BH"):
                navigate("Huawei-BH")

    with col3:
        if st.button("Nokia Dash"):
            st.session_state.show_nokia = not st.session_state.get('show_nokia', False)
        if st.session_state.get('show_nokia', False):
            if st.button("Nokia-Hourly"):
                navigate("Nokia-Hourly")
            if st.button("Nokia-Daily"):
                navigate("Nokia-Daily")
            if st.button("Nokia-BH"):
                navigate("Nokia-BH")

# Functions to handle Ericsson sub-dashboards
def ericsson_hourly():
    handle_sub_dash("Ericsson-Hourly", include_hour=True)

def ericsson_daily():
    handle_sub_dash("Ericsson-Daily", include_hour=False)

def ericsson_bh():
    handle_sub_dash("Ericsson-BH", include_hour=True)

# Functions to handle Huawei sub-dashboards
def huawei_sub_dash_1():
    handle_sub_dash("Huawei-Hourly")

def huawei_sub_dash_2():
    handle_sub_dash("Huawei-Daily")

def huawei_sub_dash_3():
    handle_sub_dash("Huawei-BH")

# Functions to handle Nokia sub-dashboards
def nokia_sub_dash_1():
    handle_sub_dash("Nokia-Hourly")

def nokia_sub_dash_2():
    handle_sub_dash("Nokia-Daily")

def nokia_sub_dash_3():
    handle_sub_dash("Nokia-BH")

# Function to handle sub-dashboards
def handle_sub_dash(dash_name, include_hour=True):
    st.markdown(
        f'<h1 style="color: #FF5733; font-size: 40px; padding-top: 28px;">📈 {dash_name}</h1>',
        unsafe_allow_html=True
    )
    
    # Button to navigate back to home
    if st.sidebar.button("Back to Home", key=f"back_{dash_name}_button"):
        navigate("home")

    st.sidebar.markdown("""<style>div.block-container {padding: 1rem;}</style>""", unsafe_allow_html=True)

    # Read the Excel file from the specified path
    file_path = file_paths[dash_name]
    try:
        sheets = read_excel_sheets(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return

    # Option to analyze the file
    analyze_option = st.sidebar.selectbox("Options", ["Select an Option", "Analyze File", "Show KPI Summary"])

    if analyze_option == "Analyze File":
        display_dashboard(sheets, dash_name, include_hour)
    elif analyze_option == "Show KPI Summary":
        show_kpi_summary(sheets, dash_name)

def display_dashboard(sheets, dash_type, include_hour=True):
    if len(sheets) == 0:
        st.sidebar.warning("No sheets available in the file.")
        return

    selected_sheet = st.sidebar.selectbox("Select Sheet", list(sheets.keys()))

    if selected_sheet is None:
        st.warning("Please select a sheet.")
        return

    if selected_sheet not in sheets:
        st.error(f"Sheet '{selected_sheet}' not found in the file.")
        return

    df = sheets[selected_sheet]

    if "Ericsson" in dash_type:
        process_ericsson_data(df, include_hour)
    elif "Huawei" in dash_type:
        process_huawei_data(df)
    else:
        process_nokia_data(df)

    # Dropdown menu for selecting metrics
    metrics = st.sidebar.multiselect("Pick metrics to plot", [col for col in df.columns if col not in ["DATE_ID", "HOUR_ID", "ELEM", "Time", "NE Name","Date"]], key=f"{dash_type}_metrics")

    if metrics:
        df_filtered = filter_data(df, dash_type)
        create_plots(df_filtered, metrics, dash_type)
    else:
        st.warning("No metrics selected for plotting.")

# Function to process Ericsson data
def process_ericsson_data(df, include_hour=True):
    df["DATE_ID"] = pd.to_datetime(df["DATE_ID"])
    if include_hour and 'HOUR_ID' in df.columns:
        df["DateTime"] = df["DATE_ID"] + pd.to_timedelta(df["HOUR_ID"], unit='h')
    else:
        df["DateTime"] = df["DATE_ID"]

# Function to process Huawei data
def process_huawei_data(df):
    if 'Time' in df.columns:
        df["Time"] = pd.to_datetime(df["Time"])
        df["DateTime"] = df["Time"]
    else:
        st.warning("Time column not found in the data.")

# Function to process Nokia data
def process_nokia_data(df):
    df["Date"] = pd.to_datetime(df["Date"])

# Function to filter data based on user input
def filter_data(df, dash_type):
    # Example filter logic based on dashboard type
    if "Ericsson" in dash_type:
        if 'DateTime' in df.columns:
            start_date = st.sidebar.date_input("Start Date", min_value=df["DateTime"].min(), value=df["DateTime"].min())
            end_date = st.sidebar.date_input("End Date", min_value=start_date, value=df["DateTime"].max())
            df = df[(df["DateTime"] >= start_date) & (df["DateTime"] <= end_date)]
    elif "Huawei" in dash_type:
        if 'DateTime' in df.columns:
            start_date = st.sidebar.date_input("Start Date", min_value=df["DateTime"].min(), value=df["DateTime"].min())
            end_date = st.sidebar.date_input("End Date", min_value=start_date, value=df["DateTime"].max())
            df = df[(df["DateTime"] >= start_date) & (df["DateTime"] <= end_date)]
    elif "Nokia" in dash_type:
        if 'Date' in df.columns:
            start_date = st.sidebar.date_input("Start Date", min_value=df["Date"].min(), value=df["Date"].min())
            end_date = st.sidebar.date_input("End Date", min_value=start_date, value=df["Date"].max())
            df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    return df

# Function to create plots based on metrics and dashboard type
def create_plots(df, metrics, dash_type):
    if "Ericsson" in dash_type:
        df_long = pd.melt(df, id_vars=["DateTime"], value_vars=metrics, var_name="Metric", value_name="Value")
        fig = px.line(df_long, x="DateTime", y="Value", color="Metric", title=f"{dash_type} Metrics")
    elif "Huawei" in dash_type:
        df_long = pd.melt(df, id_vars=["DateTime"], value_vars=metrics, var_name="Metric", value_name="Value")
        fig = px.line(df_long, x="DateTime", y="Value", color="Metric", title=f"{dash_type} Metrics")
    elif "Nokia" in dash_type:
        df_long = pd.melt(df, id_vars=["Date"], value_vars=metrics, var_name="Metric", value_name="Value")
        fig = px.line(df_long, x="Date", y="Value", color="Metric", title=f"{dash_type} Metrics")
    
    st.plotly_chart(fig)

# Function to show KPI summary
def show_kpi_summary(sheets, dash_name):
    st.write("KPI Summary")
    # Implement your KPI summary logic here
    st.write("Summary coming soon...")

# Run the application
apply_styles()
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "Ericsson-Hourly":
    ericsson_hourly()
elif st.session_state.page == "Ericsson-Daily":
    ericsson_daily()
elif st.session_state.page == "Ericsson-BH":
    ericsson_bh()
elif st.session_state.page == "Huawei-Hourly":
    huawei_sub_dash_1()
elif st.session_state.page == "Huawei-Daily":
    huawei_sub_dash_2()
elif st.session_state.page == "Huawei-BH":
    huawei_sub_dash_3()
elif st.session_state.page == "Nokia-Hourly":
    nokia_sub_dash_1()
elif st.session_state.page == "Nokia-Daily":
    nokia_sub_dash_2()
elif st.session_state.page == "Nokia-BH":
    nokia_sub_dash_3()

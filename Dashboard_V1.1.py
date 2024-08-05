#Sumerry added but not works properly

import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

# Set up the Streamlit page configuration
st.set_page_config(page_title="Core Performance Dashboards", page_icon="line_chart", layout="wide")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"

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
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                margin-bottom: 1rem;
            }
            .css-18ni7ap { background-color: #1f77b4 !important; }
            .stButton>button {
                background-color: #1f77b4;
                color: white;
                width: 100%;
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
        </style>
    """, unsafe_allow_html=True)

# Function to read all sheets from an Excel file into a dictionary of DataFrames
def read_excel_sheets(file):
    xls = pd.ExcelFile(file)
    sheets = {sheet_name: pd.read_excel(xls, sheet_name=sheet_name) for sheet_name in xls.sheet_names}
    return sheets

# Function to handle the Home page
def home_page():
    st.markdown(
    '<h1 style="color: #FF5733; font-size: 40px; padding-top: 28px;">🏠 Home Page</h1>', 
    unsafe_allow_html=True
)
    st.write("Welcome to the Core Performance Dashboard Application! Please select a dashboard to proceed.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Ericsson Dash", key="Ericsson Dash_button"):
            navigate("Ericsson Dash")
    
    with col2:
        if st.button("Huawei Dash", key="Huawei Dash_button"):
            navigate("Huawei Dash")

# Function to handle Ericsson Dash
def ericsson_dash():
    st.markdown(
    '<h1 style="color: #FF5733; font-size: 40px; padding-top: 28px;">📈 Ericsson Dash</h1>', 
    unsafe_allow_html=True
)
    st.markdown("""<style>div.block-container {padding: 1rem;}</style>""", unsafe_allow_html=True)
    
    if st.button("Back to Home", key="back_Ericsson Dash_button"):
        navigate("home")
    
    f1 = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"], key="Ericsson Dash_file", help="Upload a file here")
    if f1 is not None:
        filename = f1.name
        st.write(filename)
        if filename.endswith('.csv'):
            df = pd.read_csv(f1)
            sheets = {'Sheet1': df}
        else:
            sheets = read_excel_sheets(f1)
        
        # Option to analyze the uploaded file
        analyze_option = st.sidebar.selectbox("Options", ["Select an Option", "Analyze Uploaded File", "Show KPI Summary"])
        if analyze_option == "Analyze Uploaded File":
            display_dashboard(sheets, "Ericsson")
        elif analyze_option == "Show KPI Summary":
            show_kpi_summary(sheets, "Ericsson")
    else:
        st.sidebar.info("Please upload a file to analyze.")

# Function to handle Huawei Dash
def huawei_dash():
    st.markdown(
    '<h1 style="color: #FF5733; font-size: 40px; padding-top: 28px;">📊 Huawei Dash</h1>', 
    unsafe_allow_html=True
)
    st.markdown("""<style>div.block-container {padding: 1rem;}</style>""", unsafe_allow_html=True)
    
    if st.button("Back to Home", key="back_Huawei Dash_button"):
        navigate("home")
    
    f2 = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"], key="Huawei Dash_file", help="Upload a file here")
    if f2 is not None:
        filename = f2.name
        st.write(filename)
        if filename.endswith('.csv'):
            df = pd.read_csv(f2)
            sheets = {'Sheet1': df}
        else:
            sheets = read_excel_sheets(f2)
        
        # Option to analyze the uploaded file
        analyze_option = st.sidebar.selectbox("Options", ["Select an Option", "Analyze Uploaded File", "Show KPI Summary"])
        if analyze_option == "Analyze Uploaded File":
            display_dashboard(sheets, "Huawei")
        elif analyze_option == "Show KPI Summary":
            show_kpi_summary(sheets, "Huawei")
    else:
        st.sidebar.info("Please upload a file to analyze.")

# Function to display the dashboard
def display_dashboard(sheets, dash_type):
    selected_sheet = st.sidebar.selectbox("Select Sheet", list(sheets.keys()))
    df = sheets[selected_sheet]
    
    if dash_type == "Ericsson":
        process_ericsson_data(df)
    else:
        process_huawei_data(df)
    
    show_table = st.checkbox("Show Data Table", value=True)
    
    if show_table:
        st.write(df)
    
    df_filtered = filter_data(df, dash_type)
    
    # Dropdown menu for selecting metrics
    metrics = st.sidebar.multiselect("Pick metrics to plot", [col for col in df.columns if col not in ["DATE_ID", "HOUR_ID", "ELEM", "Time", "NE Name"]], key=f"{dash_type}_metrics")
    
    if metrics:
        create_plots(df_filtered, metrics, dash_type)
    else:
        st.warning("No metrics selected for plotting.")

# Function to process Ericsson data
def process_ericsson_data(df):
    df["DATE_ID"] = pd.to_datetime(df["DATE_ID"])
    if 'HOUR_ID' in df.columns:
        df["DateTime"] = df["DATE_ID"] + pd.to_timedelta(df["HOUR_ID"], unit='h')
    else:
        df["DateTime"] = df["DATE_ID"]

# Function to process Huawei data
def process_huawei_data(df):
    if 'Time' in df.columns:
        df["Time"] = pd.to_datetime(df["Time"])
    else:
        st.error(f"The sheet does not contain a 'Time' column.")
        st.stop()

# Function to filter data
def filter_data(df, dash_type):
    if dash_type == "Ericsson":
        startDate, endDate = df["DATE_ID"].min(), df["DATE_ID"].max()
    else:
        startDate, endDate = df["Time"].min(), df["Time"].max()
    
    col1, col2 = st.columns(2)
    
    with col1:
        date1 = st.date_input("Start Date", startDate, key=f"{dash_type}_start_date")
        date1 = pd.to_datetime(date1)  # Convert to datetime
    
    with col2:
        date2 = st.date_input("End Date", endDate, key=f"{dash_type}_end_date")
        date2 = pd.to_datetime(date2)  # Convert to datetime
    
    if dash_type == "Ericsson":
        return df[(df["DATE_ID"] >= date1) & (df["DATE_ID"] <= date2)].copy()
    else:
        return df[(df["Time"] >= date1) & (df["Time"] <= date2)].copy()

# Function to create plots
def create_plots(df, metrics, dash_type):
    st.header("Plots for Selected Metrics")
    
    num_plots = len(metrics)
    plots_per_column = (num_plots + 1) // 2
    
    plot_col1, plot_col2 = st.columns(2)
    
    for i, metric in enumerate(metrics):
        if i < plots_per_column:
            plot_col = plot_col1
        else:
            plot_col = plot_col2
        
        with plot_col:
            if dash_type == "Ericsson":
                fig = px.line(df, x="DateTime", y=metric, color="ELEM", title=f"{metric}", line_group="ELEM")
            else:
                fig = px.line(df, x="Time", y=metric, color="NE Name", title=f"{metric}", line_group="NE Name")
            st.plotly_chart(fig, use_container_width=True)

# Function to show KPI summary
def show_kpi_summary(sheets, dash_type):
    st.header("KPI Summary")
    
    for sheet_name, df in sheets.items():
        st.subheader(f"KPIs for {sheet_name}")
        available_metrics = [col for col in df.columns if col not in ["DATE_ID", "HOUR_ID", "ELEM", "Time", "NE Name"]]
        
        if available_metrics:
            metrics_to_analyze = st.multiselect("Select metrics to analyze", available_metrics, key=f"{dash_type}_{sheet_name}_metrics")
            
            if metrics_to_analyze:
                for metric in metrics_to_analyze:
                    st.write(f"### {metric}")
                    st.write({
                        "Total Records": len(df),
                        "Average Value": df[metric].mean(),
                        "Max Value": df[metric].max(),
                        "Min Value": df[metric].min(),
                        # Add more calculations as needed
                    })
            else:
                st.warning("Select metrics to analyze from the list.")
        else:
            st.error(f"No suitable metrics found in sheet '{sheet_name}'.")

# Main code to control navigation
apply_styles()

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "Ericsson Dash":
    ericsson_dash()
elif st.session_state.page == "Huawei Dash":
    huawei_dash()

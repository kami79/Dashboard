import streamlit as st
import pandas as pd
import plotly.express as px
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
    
    f1 = st.sidebar.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"], key=f"{dash_name}_file", help="Upload a file here")
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
            display_dashboard(sheets, dash_name, include_hour)
        elif analyze_option == "Show KPI Summary":
            show_kpi_summary(sheets, dash_name)
    else:
        st.sidebar.info("Please upload a file to analyze.")

def display_dashboard(sheets, dash_type, include_hour=True):
    if len(sheets) == 0:
        st.sidebar.warning("No sheets available in the uploaded file.")
        return

    selected_sheet = st.sidebar.selectbox("Select Sheet", list(sheets.keys()))
    
    if selected_sheet is None:
        st.warning("Please select a sheet.")
        return
    
    if selected_sheet not in sheets:
        st.error(f"Sheet '{selected_sheet}' not found in the uploaded file.")
        return
    
    df = sheets[selected_sheet]
    
    if "Ericsson" in dash_type:
        process_ericsson_data(df, include_hour)
    elif "Huawei" in dash_type:
        process_huawei_data(df)
    else:
        process_nokia_data(df)
      
    # Dropdown menu for selecting metrics
    metrics = st.sidebar.multiselect("Pick metrics to plot", [col for col in df.columns if col not in ["DATE_ID", "HOUR_ID", "ELEM", "Time", "NE Name", "Date"]], key=f"{dash_type}_metrics")
    
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
        df["DateTime"] = pd.to_datetime(df["Time"])
    elif 'Date' in df.columns:
        df["DateTime"] = pd.to_datetime(df["Date"])
    else:
        st.error(f"The sheet does not contain 'Time' or 'Date' columns.")
        st.stop()

# Function to process Nokia data
def process_nokia_data(df):
    # Add processing logic for Nokia data if needed
    pass

# Function to filter data
def filter_data(df, dash_type):
    if "Ericsson" in dash_type:
        startDate, endDate = df["DATE_ID"].min(), df["DATE_ID"].max()
    else:
        startDate, endDate = df["DateTime"].min(), df["DateTime"].max()

    col1, col2 = st.sidebar.columns(2)

    with col1:
        date1 = st.date_input('Start date:', startDate, key=f"{dash_type}_start_date")
    with col2:
        date2 = st.date_input('End date:', endDate, key=f"{dash_type}_end_date")

    date1 = pd.to_datetime(date1)
    date2 = pd.to_datetime(date2)

    if "Ericsson" in dash_type:
        filtered_df = df[(df["DATE_ID"] >= date1) & (df["DATE_ID"] <= date2)]
    else:
        filtered_df = df[(df["DateTime"] >= date1) & (df["DateTime"] <= date2)]

    elem_col = detect_elem_column(filtered_df)
    elem_options = st.sidebar.multiselect("Filter elements (optional)", filtered_df[elem_col].unique(), key=f"{dash_type}_elements")

    if elem_options:
        filtered_df = filtered_df[filtered_df[elem_col].isin(elem_options)]

    return filtered_df

# Function to create plots
def create_plots(df, metrics, dash_type):
    if len(metrics) == 0:
        st.warning("No metrics selected for plotting.")
        return

    elem_col = detect_elem_column(df)
    
    col1, col2 = st.columns(2)
    
    datetime_column = "DateTime"
    
    for i, metric in enumerate(metrics):
        fig = px.line(df, x=datetime_column, y=metric, color=elem_col, title=f"{dash_type} - {metric} over Time")
        if i % 2 == 0:
            col1.plotly_chart(fig)
        else:
            col2.plotly_chart(fig)

# Function to show KPI summary
def show_kpi_summary(sheets, dash_type):
    selected_sheet = st.selectbox("Select Sheet for KPI Summary", list(sheets.keys()), key=f"{dash_type}_kpi_sheet")

    if selected_sheet is None:
        st.warning("Please select a sheet.")
        return

    df = sheets[selected_sheet]
    elem_col = detect_elem_column(df)

    st.subheader(f"KPI Summary for {selected_sheet}")
    
    df_summary = df.describe(include='all')
    
    st.write("Summary of all columns:")
    st.dataframe(df_summary)
    
    # if elem_col in df.columns:
    #     st.write("Summary grouped by elements:")
    #     df_grouped = df.groupby(elem_col).describe()
    #     st.dataframe(df_grouped)

# Page navigation
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

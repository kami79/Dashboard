import streamlit as st
import pandas as pd
import plotly.express as px
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
            .stDataFrame { margin: 0 auto; }</style>""", unsafe_allow_html=True)

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
    elem_columns = ['ELEM', 'element', 'SN','NE Name']  # Add other possible column names
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
        if st.button("Ericsson Dash", key="Ericsson Dash_button"):
            navigate("Ericsson Dash")
    
    with col2:
        if st.button("Huawei Dash", key="Huawei Dash_button"):
            navigate("Huawei Dash")

    with col3:
        if st.button("Nokia Dash", key="Nokia Dash_button"):
            navigate("Nokia Dash")

# Function to handle Ericsson Dash
def Ericsson_dash():
    st.markdown(
        '<h1 style="color: #FF5733; font-size: 40px; padding-top: 28px;">📈 Ericsson Dash</h1>',
        unsafe_allow_html=True
    )
    
    # Button to navigate back to home
    if st.sidebar.button("Back to Home", key="back_Ericsson Dash_button"):
        navigate("home")
    
    st.sidebar.markdown("""<style>div.block-container {padding: 1rem;}</style>""", unsafe_allow_html=True)
    
    f1 = st.sidebar.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"], key="Ericsson Dash_file", help="Upload a file here")
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
def Huawei_dash():
    st.markdown(
        '<h1 style="color: #FF5733; font-size: 40px; padding-top: 28px;">📈 Huawei Dash</h1>',
        unsafe_allow_html=True
    )
    
    # Button to navigate back to home
    if st.sidebar.button("Back to Home", key="back_Huawei Dash_button"):
        navigate("home")
    
    st.sidebar.markdown("""<style>div.block-container {padding: 1rem;}</style>""", unsafe_allow_html=True)
    
    f1 = st.sidebar.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"], key="Huawei Dash_file", help="Upload a file here")
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
            display_dashboard(sheets, "Huawei")
        elif analyze_option == "Show KPI Summary":
            show_kpi_summary(sheets, "Huawei")
    else:
        st.sidebar.info("Please upload a file to analyze.")
        
# Function to handle Nokia Dash
def Nokia_dash():
    st.markdown(
        '<h1 style="color: #FF5733; font-size: 40px; padding-top: 28px;">📈 Nokia Dash</h1>',
        unsafe_allow_html=True
    )
    
    # Button to navigate back to home
    if st.sidebar.button("Back to Home", key="back_Nokia Dash_button"):
        navigate("home")
    
    st.sidebar.markdown("""<style>div.block-container {padding: 1rem;}</style>""", unsafe_allow_html=True)
    
    f1 = st.sidebar.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"], key="Nokia Dash_file", help="Upload a file here")
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
            display_dashboard(sheets, "Nokia")
        elif analyze_option == "Show KPI Summary":
            show_kpi_summary(sheets, "Nokia")
    else:
        st.sidebar.info("Please upload a file to analyze.")


def display_dashboard(sheets, dash_type):
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
    
    if dash_type == "Ericsson":
        process_ericsson_data(df)
    else:
        process_huawei_data(df)
      
    # Dropdown menu for selecting metrics
    metrics = st.sidebar.multiselect("Pick metrics to plot", [col for col in df.columns if col not in ["DATE_ID", "HOUR_ID", "ELEM", "Time", "NE Name"]], key=f"{dash_type}_metrics")
    
    if metrics:
        df_filtered = filter_data(df, dash_type)
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
    
        col1, col2 = st.sidebar.columns(2)
    
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
    
    num_metrics = len(metrics)
    plots_per_column = (num_metrics + 1) // 2
    
    plot_col1, plot_col2 = st.columns(2)
    
    for i, metric in enumerate(metrics):
        if i < plots_per_column:
            plot_col = plot_col1
        else:
            plot_col = plot_col2
        
        with plot_col:
            if dash_type == "Ericsson":
                fig = px.line(df, x="DateTime", y=metric, color="ELEM", title=f"{metric} - {dash_type}", line_group="ELEM")
            else:
                fig = px.line(df, x="Time", y=metric, color="NE Name", title=f"{metric} - {dash_type}", line_group="NE Name")
            st.plotly_chart(fig, use_container_width=True)

# Function to show KPI summary
def show_kpi_summary(sheets, dash_type):
    st.header("KPI Summary")
    
    selected_sheet = st.sidebar.selectbox("Select Sheet", list(sheets.keys()))
    df = sheets[selected_sheet]
    
    st.subheader(f"KPIs for {selected_sheet}")
    available_metrics = [col for col in df.columns if col not in ["DATE_ID", "HOUR_ID", "ELEM", "Time", "NE Name"]]
    
    if available_metrics:
        metrics_to_analyze = st.sidebar.multiselect("Select metrics to analyze", available_metrics, key=f"{dash_type}_{selected_sheet}_metrics")
        
        # Check if 'ELEM' or 'SN' are in the columns of the current sheet
        if 'ELEM' in df.columns:
            elem_filters = st.sidebar.multiselect("Select Element", df["ELEM"].unique(), key=f"{dash_type}_elem_filters")
        elif 'SN' in df.columns:
            elem_filters = st.sidebar.multiselect("Select Element", df["SN"].unique(), key=f"{dash_type}_elem_filters")
        elif 'NE Name' in df.columns:
            elem_filters = st.sidebar.multiselect("Select Element", df["NE Name"].unique(), key=f"{dash_type}_elem_filters")
        else:
            st.error("No suitable 'ELEM', 'SN', or 'NE Name' column found in the selected sheet.")
            return
        
        if metrics_to_analyze:
            summary_data = []
            
            for metric in metrics_to_analyze:
                metric_summary = {}
                
                if 'ELEM' in df.columns:
                    for elem in elem_filters:
                        filtered_df = df[df["ELEM"] == elem]
                        metric_summary[f"Average Value ({elem})"] = filtered_df[metric].mean()
                        metric_summary[f"Max Value ({elem})"] = filtered_df[metric].max()
                        metric_summary[f"Min Value ({elem})"] = filtered_df[metric].min()
                elif 'SN' in df.columns:
                    for elem in elem_filters:
                        filtered_df = df[df["SN"] == elem]
                        metric_summary[f"Average Value ({elem})"] = filtered_df[metric].mean()
                        metric_summary[f"Max Value ({elem})"] = filtered_df[metric].max()
                        metric_summary[f"Min Value ({elem})"] = filtered_df[metric].min()
                elif 'NE Name' in df.columns:
                    for elem in elem_filters:
                        filtered_df = df[df["NE Name"] == elem]
                        metric_summary[f"Average Value ({elem})"] = filtered_df[metric].mean()
                        metric_summary[f"Max Value ({elem})"] = filtered_df[metric].max()
                        metric_summary[f"Min Value ({elem})"] = filtered_df[metric].min()
                
                summary_data.append({
                    "Metric": metric,
                    **metric_summary
                })
            
            # Create a DataFrame from the summary data
            summary_df = pd.DataFrame(summary_data)
            
            # Display summary table
            st.write(summary_df.set_index("Metric"))
            
          # Calculate a suitable width for the plot based on a fixed value or another method
            plot_width = 4500  # Adjust this value as needed for your layout

# Plotting summary data
    if elem_filters and len(elem_filters) > 1:  # Check if elem_filters is not empty and has more than one element
        cols = st.columns(2)  # Create two columns
        for i, metric in enumerate(summary_df['Metric'].unique()):
            filtered_data = summary_df[summary_df['Metric'] == metric]
            fig = px.bar(filtered_data.melt(id_vars="Metric"), x="Metric", y="value", color="variable", barmode="group", title=f"Summary Comparison - {metric}")
            fig.update_layout(
                legend_title_text=None,
                width=int(0.5 * plot_width),  # Adjust the width to be half of plot_width
                height=int(0.1 * plot_width),  # Adjust as needed
                margin=dict(l=10, r=10, t=50, b=10),  # Adjust margins to fit the plot within specified dimensions
                bargap=0.2,  # Adjust the gap between bars
                uniformtext_minsize=8,  # Adjust the minimum text size on bars
                uniformtext_mode='hide'  # Hide text if not all bars can fit
            )
            # Use the appropriate column for each chart
            cols[i % 2].plotly_chart(fig, use_container_width=True)
    elif elem_filters and len(elem_filters) == 1:
        st.warning("Select more than one Element to compare in the summary.")
    else:
        st.warning("No filters selected. Please select at least one Element.")

# Main code to control navigation
apply_styles()

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "Ericsson Dash":
    Ericsson_dash()
elif st.session_state.page == "Huawei Dash":
    Huawei_dash()
elif st.session_state.page == "Nokia Dash":
    Nokia_dash()

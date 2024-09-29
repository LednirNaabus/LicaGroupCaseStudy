import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
        page_title="Employee Performance Metrics",
        layout="wide",
        initial_sidebar_state="expanded"
        )

alt.themes.enable("dark")

emp_data = pd.read_csv('data/Employees_Sheet.csv')

with st.sidebar:
    st.title('Employee Performance Metrics')

    select_dept = st.selectbox("Select Department:", emp_data["Department"].unique())
    filtered_emp = emp_data[emp_data["Department"] == select_dept]
    select_emp = st.selectbox("Select Employee:", filtered_emp["Name"].tolist())
    selected_emp = filtered_emp[filtered_emp["Name"] == select_emp]

st.header(f"{selected_emp['Name'].values[0]}")
st.write(f"**Employee ID:** {selected_emp['Employee ID'].values[0]}")
st.write(f"**Department:** {selected_emp['Department'].values[0]}")
# st.write(f"**Performance Rating:** {selected_emp['Performance Rating'].values[0]}")

st.header("Employee Metrics")

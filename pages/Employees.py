import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
@st.cache_data
def load_data():
    # Replace this with your actual data loading logic
    df = pd.read_csv("data/Employees_Sheet.csv")
    return df

df = load_data()

# Sidebar for employee selection
st.sidebar.title("Employee Selection")
selected_employee = st.sidebar.selectbox("Choose an employee", df['Name'].unique())

# Filter data for selected employee
employee_data = df[df['Name'] == selected_employee].iloc[0]

# Main dashboard
st.title(f"Performance Dashboard: {selected_employee}")

# Basic Info
st.subheader("Employee Information")
col1, col2, col3 = st.columns(3)
col1.metric("Employee ID", employee_data['Employee ID'])
col2.metric("Department", employee_data['Department'])
col3.metric("Performance Rating", employee_data['Performance Rating'])

# Attendance
st.subheader("Attendance")
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = employee_data['Attendance (%)'],
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Attendance"},
    gauge = {'axis': {'range': [0, 100]},
             'bar': {'color': "darkblue"},
             'steps': [
                 {'range': [0, 60], 'color': "red"},
                 {'range': [60, 80], 'color': "yellow"},
                 {'range': [80, 100], 'color': "green"}]}))
st.plotly_chart(fig)

# Training Hours
st.subheader("Training and Development")
avg_training_hours = df['Training Hours'].mean()
fig = go.Figure(go.Bar(
    x=['Employee', 'Company Average'],
    y=[employee_data['Training Hours'], avg_training_hours],
    text=[f"{employee_data['Training Hours']:.1f}", f"{avg_training_hours:.1f}"],
    textposition='auto',
))
fig.update_layout(title_text="Training Hours Comparison")
st.plotly_chart(fig)

# Projects Completed
st.subheader("Projects Completed")
avg_projects = df['Projects Completed'].mean()
col1, col2 = st.columns(2)
col1.metric("Employee Projects", employee_data['Projects Completed'])
col2.metric("Company Average", f"{avg_projects:.1f}")

# Client Satisfaction and Sales Revenue
st.subheader("Client Satisfaction and Sales Performance")
fig = go.Figure()
fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = employee_data['Client Satisfaction'],
    title = {"text": "Client Satisfaction"},
    domain = {'row': 0, 'column': 0}
))
fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = employee_data['Sales Revenue ($)'],
    title = {"text": "Sales Revenue ($)"},
    domain = {'row': 0, 'column': 1}
))
fig.update_layout(grid = {'rows': 1, 'columns': 2, 'pattern': "independent"})
st.plotly_chart(fig)

# Performance Radar Chart
st.subheader("Performance Overview")
categories = ['Attendance', 'Training', 'Projects', 'Satisfaction', 'Sales']
employee_values = [
    employee_data['Attendance (%)'] / 100,
    employee_data['Training Hours'] / df['Training Hours'].max(),
    employee_data['Projects Completed'] / df['Projects Completed'].max(),
    employee_data['Client Satisfaction'] / 10,  # Assuming 10 is max
    employee_data['Sales Revenue ($)'] / df['Sales Revenue ($)'].max()
]
avg_values = [
    df['Attendance (%)'].mean() / 100,
    df['Training Hours'].mean() / df['Training Hours'].max(),
    df['Projects Completed'].mean() / df['Projects Completed'].max(),
    df['Client Satisfaction'].mean() / 10,
    df['Sales Revenue ($)'].mean() / df['Sales Revenue ($)'].max()
]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=employee_values,
    theta=categories,
    fill='toself',
    name='Employee'
))
fig.add_trace(go.Scatterpolar(
    r=avg_values,
    theta=categories,
    fill='toself',
    name='Company Average'
))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True)
st.plotly_chart(fig)

# Recommendations
st.subheader("Recommendations")
recommendations = []
if employee_data['Attendance (%)'] < df['Attendance (%)'].mean():
    recommendations.append("Focus on improving attendance.")
if employee_data['Training Hours'] < df['Training Hours'].mean():
    recommendations.append("Consider undertaking additional training.")
if employee_data['Projects Completed'] < df['Projects Completed'].mean():
    recommendations.append("Look for opportunities to take on more projects.")
if employee_data['Client Satisfaction'] < df['Client Satisfaction'].mean():
    recommendations.append("Work on improving client satisfaction scores.")
if employee_data['Sales Revenue ($)'] < df['Sales Revenue ($)'].mean():
    recommendations.append("Explore strategies to increase sales revenue.")

if recommendations:
    for rec in recommendations:
        st.write(f"- {rec}")
else:
    st.write("Great job! Keep up the good work across all areas.")

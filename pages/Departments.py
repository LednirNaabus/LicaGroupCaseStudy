import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
        page_title="Department Metrics",
        layout="wide",
        initial_sidebar_state="expanded"
        )

alt.themes.enable("dark")

df = pd.read_csv('data/Employees_Sheet.csv')
with st.sidebar:
    st.title('Department Metrics')

    select_dept = st.selectbox("Select Department:", df["Department"].unique())
    filtered_dept = df[df["Department"] == select_dept]

st.header(f"{select_dept} Employees Performance Rating and Dashboard (past year)")
st.subheader("Performance Rating per Employee")

def aggregate_avg_performance_score(df):
    grouped = df.groupby('Department')['Performance Rating'].mean()
    return grouped

def get_chart_53556():
    source = pd.DataFrame(filtered_dept)

    base = alt.Chart(source).encode(
        theta=alt.Theta("Performance Rating:Q", stack=True), color=alt.Color("Name:N", legend=None)
    )

    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=140, size=20).encode(text="Performance Rating:Q")

    chart = pie + text

    st.altair_chart(chart, theme="streamlit", use_container_width=True)

get_chart_53556()

st.header("Employee Count per Performance Rating")
emp_rating_count = filtered_dept.groupby('Performance Rating')['Department'].count()
st.bar_chart(emp_rating_count )

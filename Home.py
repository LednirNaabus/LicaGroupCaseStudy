import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(
        page_title="Home page",
        layout="wide",
        initial_sidebar_state="expanded"
        )

df = pd.read_csv('data/Employees_Sheet.csv')
df_copy = df.copy()
df_copy = df_copy.drop(columns=['Employee ID', 'Name', 'Department'])

st.subheader("Preview of Spreadsheet")
st.write(df.head())

st.subheader("Correlation Matrix")
st.write("Lets display a correlation matrix to see how the variables in the employee sheet correlate between each other.")
corr_matrix = df_copy.corr()
fig, ax = plt.subplots()

sns.heatmap(corr_matrix, annot=True, cmap="viridis", ax=ax)
ax.set_title("Correlation Matrix")
st.pyplot(fig)

st.subheader("Average Performance Rating by Department")
departments = df['Department'].unique()
grouped = df.groupby('Department')['Performance Rating'].mean()
st.bar_chart(grouped)

st.subheader("Top Employees by Performance Rating")
def top_emp_chart():
    source = df
    bars = alt.Chart(source).mark_bar().encode(
            x='Performance Rating:Q',
            y=alt.Y('Name:N', sort='-x'),
            color='Department',
            )
    text = bars.mark_text(
            align='left',
            baseline='middle',
            dx=3
            ).encode(
                    text='Performance Rating:Q'
                    )
    chart = (bars + text).properties(height=900)
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
top_emp_chart()

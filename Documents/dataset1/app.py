import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
# Streamlit app
st.title('Different Companies Data')

# Load the initial DataFrame
with open('C:\\Users\\ACER\\Documents\\dataset1\\filtered_output.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Sidebar for industry selection
st.sidebar.title('Select Industry')
all_industries = df['industries'].explode().unique()
selected_industry = st.sidebar.selectbox('Select an industry type', [''] + list(all_industries))

# Sidebar for revenue category selection
st.sidebar.title('Select Revenue Category')
selected_revenue_category = st.sidebar.radio('Select revenue category', ['All Companies','Less than $100,000,000', 'More than $100,000,000'], index=None)

# Sidebar for company status selection
st.sidebar.title('Select Company Status')
selected_status = st.sidebar.radio('Select company status', ['All Companies', 'Public Companies', 'Acquired Companies'], index=None)

#Sidebar for company importance
st.sidebar.title('Select Importance Status')
selected_importance = st.sidebar.slider('Importance',min_value= 70.0, max_value=100.0, step=0.1)

# Convert the 'Revenue' column to numeric
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

# Filter DataFrame based on selected industry type and revenue category
if selected_industry:
    filtered_df = df[df['industries'].apply(lambda x: selected_industry in x)]
    st.write('Companies in the', selected_industry, 'Industry:')
else:
    filtered_df = df

if selected_revenue_category: 
    if selected_revenue_category == 'Less than $100,000,000':
       filtered_df = filtered_df[filtered_df['revenue'] < 100000000]
       st.write('Companies with', selected_revenue_category, 'revenue:')
    elif selected_revenue_category == 'More than $100,000,000':
       filtered_df = filtered_df[filtered_df['revenue'] >= 100000000]
       st.write('Companies with', selected_revenue_category, 'revenue:')
    else:
        st.write('All Companies:')
if selected_status:
    if selected_status == 'Public Companies':
        filtered_df = filtered_df[filtered_df['is_public'] == True]
    elif selected_status == 'Acquired Companies':
        filtered_df = filtered_df[filtered_df['isAcquired'] == True]
if selected_importance:
    filtered_df = filtered_df[filtered_df['importance'] >= selected_importance]
    # st.write('Companies with Importance greater than or equal to', selected_importance)

# Display the filtered DataFrame
st.dataframe(filtered_df)

# Create a sunburst chart
sunburst_df = filtered_df.head(100)
fig = px.sunburst(sunburst_df, path=['id','name','type','location','importance'],
                  values='revenue',
                                color_continuous_scale='RdBu_r',
                                width=800, height=800,
                                title='Sunburst Diagram',
                                template='seaborn',
                                labels={'EmployeesMax': 'Maximum Employees'})
                                

# Display the sunburst chart
st.plotly_chart(fig)

# Sort the DataFrame by 'nbEmployeesMax' and select the top 100 rows
barchart_df = filtered_df.sort_values(by='nbEmployeesMax', ascending=False).head(100)

# Create a bar chart
fig1 = px.bar(
    barchart_df,  # DataFrame
    x='name',  # X-axis: name
    y='nbEmployeesMax',  # Y-axis: nbEmployeesMax
    color='nbEmployeesMax',  # Color based on nbEmployeesMax
    color_continuous_scale='RdBu_r',  # Color scale
    labels={'name': 'CompanyName', 'nbEmployeesMax': 'Maximum Employees'},  # Axis labels
    title='Bar Chart',  # Title
    template='seaborn',  # Template
)


# Show the plot
st.plotly_chart(fig1)

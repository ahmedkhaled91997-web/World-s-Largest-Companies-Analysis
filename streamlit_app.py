import streamlit as st
import data_visualization as dv
import pandas as pd

df=pd.read_csv('cleaned_data.csv')
old=pd.read_csv('data_collection.csv')
col1,col2,col3,col4=st.columns(4)
with col1:
    st.metric(label='Total profit margin',value=f'{df["net_profit"].sum()}B')
with col2:
    st.metric(label='Total profit',value=f'{df["profit"].sum()/1e9}B')
with col3:  
    st.metric(label='Total Revenue',value=f'{df["revenue"].sum()/1e9}B')
with col4:
    st.metric(label='Total Revenue per Employee',value=f'{df["revenue_per_employee"].sum()/1e6:.2f}M')

col7,col8=st.columns(2)
with col7:
    st.image('outputs/company_by_industry.png')
with col8:
    st.image('outputs/companies_by_country.png')

st.title('World’s Largest Companies Analysis Dashboard')
st.header('Data Overview',divider='rainbow')
col5,col6=st.columns(2)
with col5:
    st.subheader('Data Collection.csv')
    st.dataframe(old)
with col6:
    st.subheader('Cleaned Data.csv')
    st.dataframe(df)

st.header('Data Visualization')
st.sidebar.header('select the visualization you want to see')

selected_visualization=st.sidebar.selectbox('choose the visualization',('Top 5 Revenue Companies','Top 5 Profit Companies',
'Companies by Country','Company by Industry','Average Revenue and Profit by Industry',
'Relationship between Revenue and Profit','Relationship between Employees and Revenue',
'Comparison Profit Margin and Revenue per Employee','Outliers Analysis','Additional Business Analysis'))
show_visualization=st.sidebar.button('Show Visualization')


if show_visualization and selected_visualization=='Top 5 Revenue Companies':
    dv.top_revenue(df)
    st.write('This is a simple dashboard to visualize the data.')
elif show_visualization and selected_visualization=='Top 5 Profit Companies':
    dv.top_profit(df)
    st.write('This is a simple dashboard to visualize the data.')
elif show_visualization and selected_visualization=='Companies by Country':
    dv.companies_by_country(df)
    st.write('This is a simple dashboard to visualize the data.')
elif show_visualization and selected_visualization=='Company by Industry':
    dv.company_by_industry(df)
    st.write('This is a simple dashboard to visualize the data.')
elif show_visualization and selected_visualization=='Average Revenue and Profit by Industry':
    dv.average_revenue_profit_by_industry(df)
    st.write('This is a simple dashboard to visualize the data.')
elif show_visualization and selected_visualization=='Relationship between Revenue and Profit':
    dv.relationship_between_revenue_and_profit(df)
    st.write('This is a simple dashboard to visualize the data.')
elif show_visualization and selected_visualization=='Relationship between Employees and Revenue':
    dv.relationship_between_employees_and_revenue(df)
    st.write('This is a simple dashboard to visualize the data.')
elif show_visualization and selected_visualization=='Comparison Profit Margin and Revenue per Employee':
    dv.comparison_profit_margin_and_revenu_per_employee(df)
    st.write('This is a simple dashboard to visualize the data.')
elif show_visualization and selected_visualization=='Outliers Analysis':
    dv.outliers_analysis(df)
    st.write('This is a simple dashboard to visualize the data.')
elif show_visualization and selected_visualization=='Additional Business Analysis':
    dv.additional_business_analysis(df)
    st.write('This is a simple dashboard to visualize the data.')
else:
    st.warning('"👈 "👈 Please select a visualization and click the "Show Visualization" button.')



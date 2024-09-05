import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Price Analyzer",page_icon=":bar_chart")

st.header("Stock Price Analyzer")

def get_data(company):
    script_dir = os.path.dirname(__file__)
    file_name=file_path = os.path.join(script_dir, 'stockPriceData', company+'.csv')
    df=pd.read_csv(file_name)
    st.dataframe(df.head())
    return df
    
def get_trend(company):
    script_dir = os.path.dirname(__file__)
    file_name=file_path = os.path.join(script_dir, 'stockPriceData', company+'.csv')
    df=pd.read_csv(file_name)
    st.line_chart(df,x='Date',y='Open')
    
def Compare_trends(company1,company2):
    script_dir = os.path.dirname(__file__)
    file_name1=file_path = os.path.join(script_dir, 'stockPriceData', company1+'.csv')
    file_name2=file_path = os.path.join(script_dir, 'stockPriceData', company2+'.csv')
    df1=pd.read_csv(file_name1)
    df2=pd.read_csv(file_name2)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1['Date'], y=df1['Open'], mode='lines', name=company1))
    fig.add_trace(go.Scatter(x=df2['Date'], y=df2['Open'], mode='lines', name=company2))
    st.plotly_chart(fig)
    
def return_calulator(df, start_date,end_date):
    df['Date']=pd.to_datetime(df['Date'],format='%Y-%m-%d')
    start_date=pd.to_datetime(start_date)
    end_date=pd.to_datetime(end_date)
    start_date=min(max(df['Date'].min(),start_date),df['Date'].max())
    end_date=min(df['Date'].max(),end_date)
    start_price=df[df['Date']==start_date].loc[:,'Open'].values[-1]
    end_price=df[df['Date']==end_date].loc[:,'Open'].values[-1]
    return_value=(end_price-start_price)/start_price*100
    return return_value
    
current_dir = os.path.dirname(__file__)
data_folder = os.path.join(current_dir, 'stockPriceData')
company_file_name=os.listdir(data_folder)[1:]
company_name=[]
for stock in company_file_name:
    if stock.split('.')[-1]=='csv':
        company_name.append(stock.split('.')[0])
        

company=st.selectbox(label="Stocks",options=company_name,placeholder="select a stock")

df=get_data(company)

if company is not None:
    st.download_button(
        label="download data",
        data=df.to_csv(index=False),
        file_name=company+'.csv',
        mime='csv',
    )


button=st.button(label="Show Trend")

if button==True:
    get_trend(company)
    
st.subheader("Compare Stock")
    
selected_companies=st.multiselect(label="select two stocks to compare",options=company_name,max_selections=2)

compare=st.button(label="Compare stocks")
    
if len(selected_companies)==2 and compare==True:
    Compare_trends(selected_companies[0],selected_companies[1])
else:
    st.warning("Select exactly two stocks to compare")
    

script_dir = os.path.dirname(__file__)
file=os.path.join(script_dir,'stockPriceData',company+'.csv') 
df=pd.read_csv(file)

sidebar=st.sidebar

sidebar.title("Stock Performance Summary of "+company)

sidebar.markdown("*Average daily trade volume* \n")
sidebar.write(df['Volume'].mean())

sidebar.markdown("*Minimum Price* \n")
sidebar.write(df['Open'].min())

sidebar.markdown("*Maximum Price* \n")
sidebar.write(df['Open'].max()) 

col1, col2=sidebar.columns(2)

with col1:
    start_date = sidebar.date_input("Start Date",format="YYYY-MM-DD")
    
with col1:
    end_date = sidebar.date_input("End Date",format="YYYY-MM-DD")

button=sidebar.button("Calulate Return")
if button==True and start_date is not None and end_date is not None:
    sidebar.write(return_calulator(df,start_date, end_date),"%")


#Importing Packages
import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime
import plot


#Loading the Symbols Data
df_url = 'https://raw.githubusercontent.com/JackronyK/Projects_Jackrony/main/Python%20Apps/Simple%20Stock%20Price/Data/Stock%20Market%20Data.csv'
cols_ = ['Symbol', 'Name', 'Country', 'Sector', 'Industry']
symbols_df = pd.read_csv(df_url).dropna()[cols_]

# The App
#Header of the App
st.write("""
## Stock Analytics App

Select Filter to view Stock analystics             
""")

#Sidebar Filters
country_filter = st.sidebar.selectbox("Select Country", sorted(symbols_df['Country'].unique()))
#sector_filter = st.sidebar.selectbox('Select Sector', sorted(symbols_df['Sector'].unique()))
industry_filter = st.sidebar.selectbox('Select Industry', sorted(symbols_df [symbols_df['Country'] == country_filter ]['Industry'].unique()))

#Date Range selection

if 'start_date' not in st.session_state:
    st.session_state.start_date = datetime(2010, 5, 31)
if 'end_date' not in st.session_state:
    st.session_state.end_date = datetime.now().date()

# Ensure the end date is after the start date; if not, reset to today's date
if st.session_state.start_date > st.session_state.end_date:
    st.session_state.end_date = st.session_state.start_date

st.session_state.start_date = st.sidebar.date_input('Start date', st.session_state.start_date)
st.session_state.end_date = st.sidebar.date_input('End date', st.session_state.end_date, min_value=st.session_state.start_date)

#Filtering the symbol df based on the user selection
filtered_df = symbols_df[
    (symbols_df['Country'] ==country_filter) &
    #(symbols_df['Sector'] == sector_filter) &
    (symbols_df['Industry'] == industry_filter) 
]

# Displaying company Names
if not filtered_df.empty:
    st.write(f'## Companies in {country_filter} , {industry_filter}')
    selected_company = st.selectbox('Select a company: ', filtered_df['Name'].unique())

    #getting the symbol for the selected company
    selected_symbol = filtered_df.loc[filtered_df['Name'] == selected_company, 'Symbol'].iloc[0]


    #Fetch the data using yahoo-finance
    tickerData = yf.Ticker(selected_symbol)
    current_date = datetime.now().date()
    tickerDf = tickerData.history(period = '1d', start = st.session_state.start_date, end = st.session_state.end_date)

    #Displaying the Closing Price and Volume Chats
    st.write("""

    ### Closing Price

    """)
    st.line_chart(tickerDf.Close)

    st.write("""

    ### Volume

    """)
    st.line_chart(tickerDf.Volume)
else:
    st.write('No Companies mathc the selected filters')
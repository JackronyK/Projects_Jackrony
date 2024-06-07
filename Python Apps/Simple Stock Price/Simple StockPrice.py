# Importing Packages
import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Loading the Symbols Data
df_url = 'https://raw.githubusercontent.com/JackronyK/Projects_Jackrony/main/Python%20Apps/Simple%20Stock%20Price/Data/Stock%20Market%20Data.csv'
cols_ = ['Symbol', 'Name', 'Country', 'Sector', 'Industry']
symbols_df = pd.read_csv(df_url).dropna()[cols_]

# The App
# Header of the App
st.write("""
## Stock Analytics App

Use the filters to select a stock and view its analytics             
""")

# Sidebar Filters
country_filter = st.sidebar.selectbox("Select Country", sorted(symbols_df['Country'].unique()))
industry_filter = st.sidebar.selectbox('Select Industry', sorted(symbols_df[symbols_df['Country'] == country_filter]['Industry'].unique()))

# Date Range selection
if 'start_date' not in st.session_state:
    st.session_state.start_date = datetime(2010, 5, 31)
if 'end_date' not in st.session_state:
    st.session_state.end_date = datetime.now().date()



st.session_state.start_date = st.sidebar.date_input('Start date', st.session_state.start_date)
st.session_state.end_date = st.sidebar.date_input('End date', st.session_state.end_date, min_value=st.session_state.start_date)

# Filtering the symbol df based on the user selection
filtered_df = symbols_df[
    (symbols_df['Country'] == country_filter) &
    (symbols_df['Industry'] == industry_filter)
]

# Displaying company Names
if not filtered_df.empty:
    selected_company = st.selectbox('Select a company:', filtered_df['Name'].unique())
    selected_symbol = filtered_df.loc[filtered_df['Name'] == selected_company, 'Symbol'].iloc[0]

    # Fetch the data using yahoo-finance
    tickerData = yf.Ticker(selected_symbol)
    tickerDf = tickerData.history(period='1d', start=st.session_state.start_date, end=st.session_state.end_date)

    # Check if tickerDf is empty
    if not tickerDf.empty:
        # Displaying the Stock Data
        st.write(f'## {selected_company} ({selected_symbol})')

        # Creating a plotly figure
        fig = go.Figure()

        # Adding traces for closing price
        fig.add_trace(go.Scatter(x=tickerDf.index, y=tickerDf['Close'], mode='lines', name='Closing Price'))

        # Add traces for moving averages
        tickerDf['30MA'] = tickerDf['Close'].rolling(window=30).mean()
        tickerDf['90MA'] = tickerDf['Close'].rolling(window=90).mean()
        fig.add_trace(go.Scatter(x=tickerDf.index, y=tickerDf['30MA'], mode='lines', name='30 Day MA'))
        fig.add_trace(go.Scatter(x=tickerDf.index, y=tickerDf['90MA'], mode='lines', name='90 Day MA'))

        # Add Volume bar chart
        fig.add_trace(go.Bar(x=tickerDf.index, y=tickerDf['Volume'], name='Volume', yaxis='y2'))

        # Update layout for dual y-axis
        fig.update_layout(
            yaxis=dict(
                title='Stock Price'
            ),
            yaxis2=dict(
                title='Volume',
                overlaying='y',
                side='right'
            ),
            xaxis_title='Date',
            title=f'Stock Prices and Volume for {selected_company} ({selected_symbol})',
            template='plotly_dark'
        )

        # Display the Plotly figure
        st.plotly_chart(fig)

        # Additional Information Display
        last_price = tickerDf['Close'].iloc[-1]
        previous_price = tickerDf['Close'].iloc[-2]
        st.write('### Stock Data Overview')
        st.write(f'**Last Price:** {last_price:.2f}')
        st.write(f'**Previous Day Price:** {previous_price:.2f}')
        st.write(f'**Price Change:** {(last_price - previous_price):.2f}')
        st.write(f'**% Change:** {(last_price - previous_price) / previous_price * 100:.2f}%')
        st.write(f'**Max Price:** {tickerDf["Close"].max():.2f}')
        st.write(f'**Low Price:** {tickerDf["Close"].min():.2f}')
    else:
        st.write("No data available for the selected date range.")
else:
    st.write('No companies match the selected filters.')

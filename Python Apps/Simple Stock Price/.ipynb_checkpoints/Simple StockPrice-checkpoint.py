#Importing Packages
import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime


#Header of the App
st.write("""
## Simple Stock Price App

Shown are the stock **closing price** and *volume* of Google!

    
""")

#getting the data from yfinance
tickersymbol = 'GOOGL'

#Get the data on this ticker symbol
tickerData = yf.Ticker(tickersymbol)

# Getting the historical prices for this ticker
current_date = datetime.now().date()
tickerDf = tickerData.history(period = '1d', start = '2010-5-31', end = current_date)

st.write("""

### Closing Price

""")
st.line_chart(tickerDf.Close)

st.write("""

### Volume

""")
st.line_chart(tickerDf.Volume)
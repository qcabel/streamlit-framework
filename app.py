import streamlit as st
import io
import pandas as pd

import requests
import calendar
from datetime import datetime

from config import APIKEY


st.title("Alpha Vantage Stock Time Series")

history_year = [*range(2010, 2021)]

# sidebar layout for options
st.sidebar.write('**Adjusted closing price for:**')
ticker = st.sidebar.text_input(label='Ticker (e.g. AAPL):', value='AAPL', max_chars=None,
                               key='ticker', type='default', help=None)
year = st.sidebar.selectbox(label='Year:', options=history_year,
                            key='year', help=None)
month = st.sidebar.selectbox(label='Month:', options=calendar.month_name[1:13],
                             key='month')

'Adjusted closing price for ', ticker, ' on ', month, ',', str(year), ':'


# get stock price from Alpha Vantage API
def get_data(ticker, month, year):
    url = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED'
           '&outputsize=full&symbol={}&apikey={}&datatype=csv').format(ticker, APIKEY)
    response = requests.get(url)

    # parse string output
    df = pd.read_csv(io.StringIO(response.text))
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    df.sort_index(ascending=True, inplace=True)

    # slice based on month, year
    sub_df = df[str(year)+'-'+str(datetime.strptime(month, '%B').month)]
    return sub_df


df = get_data(ticker, month, year)
df_close = df['close']
st.line_chart(df_close)

"Show the raw data:"
df
# if st.checkbox('Show the raw data'):
#     df

# df.head()






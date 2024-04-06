import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def main():
    st.title('Stock Details App')
    
    page = st.sidebar.selectbox("Select one", ["Single Stock", "Compare Stocks"])

    if page == "Single Stock":
        display_single_stock()
    elif page == "Compare Stocks":
        display_compare_stocks()

def display_single_stock():
    symbol = st.text_input("Ticker Symbol ( META):")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Submit"):
        if symbol:
            data = yf.download(symbol, start=start_date, end=end_date)
            if not data.empty:
                plot_stock_price(data)
                print_stats(data)

def display_compare_stocks():
    st.title("Compare Two Stocks")
    symbol1 = st.text_input("Ticker 1 ( AAPL):")
    symbol2 = st.text_input("Ticker 2 ( MSFT):")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Compare"):
        if symbol1 and symbol2:
            data1 = yf.download(symbol1, start=start_date, end=end_date)
            data2 = yf.download(symbol2, start=start_date, end=end_date)

            if not data1.empty and not data2.empty:
                
                plot_comparison(data1, data2)
                print_stats_comparison(data1, data2)

def plot_stock_price(data):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data.index, data['Close'], label='Closing Price')
    ax.set_title('Stock Price Over the Selected Period')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($)')
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    st.pyplot(fig)

def plot_comparison(data1, data2):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data1.index, data1['Close'], label='Closing Price - Stock 1')
    ax.plot(data2.index, data2['Close'], label='Closing Price - Stock 2')
    ax.set_title('Stock Price Comparison Over the Selected Period')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($)')
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    st.pyplot(fig)

def print_stats(data):
    max_price = data['Close'].max()
    min_price = data['Close'].min()
    max_date = data[data['Close'] == max_price].index[0]
    min_date = data[data['Close'] == min_price].index[0]
    st.write(f"Maximum Price: ${max_price} on {max_date}")
    st.write(f"Minimum Price: ${min_price} on {min_date}")

def print_stats_comparison(data1, data2):
    max_price1 = data1['Close'].max()
    min_price1 = data1['Close'].min()
    max_date1 = data1[data1['Close'] == max_price1].index[0]
    min_date1 = data1[data1['Close'] == min_price1].index[0]

    max_price2 = data2['Close'].max()
    min_price2 = data2['Close'].min()
    max_date2 = data2[data2['Close'] == max_price2].index[0]
    min_date2 = data2[data2['Close'] == min_price2].index[0]

    stats_data = {
        'Stock': ['Stock 1', 'Stock 2'],
        'Maximum Price': [max_price1, max_price2],
        'Minimum Price': [min_price1, min_price2],
        'Max Date': [max_date1, max_date2],
        'Min Date': [min_date1, min_date2]
    }

    stats_df = pd.DataFrame(stats_data)
    stats_df.set_index('Stock', inplace=True)

    st.write("Statistics for Stock Prices:")
    st.write(stats_df)

    st.bar_chart(stats_df[['Maximum Price', 'Minimum Price']])

if __name__ == "__main__":
    main()

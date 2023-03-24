#!pip install yfinance
import yfinance as yf

# Define the Russell2000 ticker
ticker = "^RUT"

# Get the Russell2000 stock data for the past few years
stock_data = yf.download(ticker, start="2019-01-01", end="2022-03-22")

# Calculate the earnings surprise for each company in the Russell2000
# We'll define an earnings surprise as a 30% increase or decrease in the stock price
# after the earnings report is released
earnings_surprise = {}
for symbol in stock_data.columns:
    earnings_report_dates = stock_data[symbol].dropna().index
    for i in range(len(earnings_report_dates)):
        earnings_date = earnings_report_dates[i]
        if i+1 < len(earnings_report_dates):
            next_earnings_date = earnings_report_dates[i+1]
        else:
            next_earnings_date = stock_data.index[-1]
        price_at_earnings = stock_data[symbol][earnings_date]
        price_at_next_earnings = stock_data[symbol][next_earnings_date]
        if price_at_earnings * 1.3 <= price_at_next_earnings:
            earnings_surprise[symbol] = earnings_surprise.get(symbol, 0) + 1
        elif price_at_earnings * 0.7 >= price_at_next_earnings:
            earnings_surprise[symbol] = earnings_surprise.get(symbol, 0) - 1

# Sort the companies in the Russell2000 by earnings surprise
sorted_earnings_surprise = sorted(earnings_surprise.items(), key=lambda x: x[1], reverse=True)

# Print the top 10 most volatile stocks in the Russell2000
for i in range(10):
    print(f"{sorted_earnings_surprise[i][0]}: {sorted_earnings_surprise[i][1]}")

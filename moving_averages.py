import pandas as pd

def calculate_sma(prices, window):
    """
    Calculate the Simple Moving Average (SMA).

    :param prices: List or Series of stock prices.
    :param window: The number of periods to consider for SMA calculation.
    :return: Series with the SMA values.
    """
    return pd.Series(prices).rolling(window=window).mean()

def calculate_ema(prices, window):
    """
    Calculate the Exponential Moving Average (EMA).

    :param prices: List or Series of stock prices.
    :param window: The number of periods to consider for EMA calculation.
    :return: Series with the EMA values.
    """
    return pd.Series(prices).ewm(span=window, adjust=False).mean()

# Example usage:
stock_prices = [10.25, 10.30, 10.45, 10.60, 10.75, 10.90, 11.05, 11.20, 11.35, 11.50]
window = 3

# Calculate SMA
sma_values = calculate_sma(stock_prices, window)
print("SMA:", sma_values.tolist())

# Calculate EMA
ema_values = calculate_ema(stock_prices, window)
print("EMA:", ema_values.tolist())

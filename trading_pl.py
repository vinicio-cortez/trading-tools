#!/usr/bin/env python3
def calculate_profit_loss(initial_investment, current_value, fees=0):
    """
    Calculate the profit or loss based on initial investment,
    current value, and optional fees.

    :param initial_investment: Initial amount invested (float)
    :param current_value: Current value of the investment (float)
    :param fees: Transaction fees (default 0.0) (float)
    :return: Profit or loss (float)
    """
    profit_loss = current_value - initial_investment - fees
    return profit_loss

# Example usage:
if __name__ == "__main__":
    initial_investment = 10000.0  # Initial investment amount
    current_value = 12000.0       # Current value of the investment
    fees = 50.0                   # Transaction fees

    profit_loss = calculate_profit_loss(initial_investment, current_value, fees)
    print(f"Profit/Loss: ${profit_loss:.2f}")

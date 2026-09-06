def stock_utility(stock, stock_value, current_price):

    change = ((current_price - stock_value) / stock_value) * 100

    if change <= -10:
        decision = "BUY"
    elif change >= 10:
        decision = "SELL"
    else:
        decision = "HOLD"

    return stock, change, decision
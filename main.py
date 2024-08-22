import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def calculate_token_prices(a_amount, b_amount, usdc_amount):
    total_tokens = a_amount + b_amount
    a_price = usdc_amount / total_tokens
    b_price = 1 - a_price
    return a_price, b_price

def buy_token(token_amount, current_a, current_b, current_usdc, is_a_token):
    if is_a_token:
        new_a = current_a + token_amount
        new_b = current_b
    else:
        new_a = current_a
        new_b = current_b + token_amount
    
    k = current_a * current_b
    new_usdc = k / (new_a * new_b) * current_usdc
    
    return new_a, new_b, new_usdc

def main():
    st.title("Polymarket AMM Simulator")

    # Initial state
    initial_a = st.sidebar.number_input("Initial A Tokens", min_value=1, value=1000)
    initial_b = st.sidebar.number_input("Initial B Tokens", min_value=1, value=1000)
    initial_usdc = st.sidebar.number_input("Initial USDC", min_value=1, value=1000)

    # Buy tokens
    token_to_buy = st.sidebar.selectbox("Token to Buy", ["A", "B"])
    amount_to_buy = st.sidebar.number_input("Amount to Buy", min_value=0.0, value=0.0, step=0.1)

    # Calculate initial prices
    initial_a_price, initial_b_price = calculate_token_prices(initial_a, initial_b, initial_usdc)

    # Simulate purchase
    if amount_to_buy > 0:
        new_a, new_b, new_usdc = buy_token(amount_to_buy, initial_a, initial_b, initial_usdc, token_to_buy == "A")
        new_a_price, new_b_price = calculate_token_prices(new_a, new_b, new_usdc)
    else:
        new_a, new_b, new_usdc = initial_a, initial_b, initial_usdc
        new_a_price, new_b_price = initial_a_price, initial_b_price

    # Display results
    col1, col2, col3 = st.columns(3)
    col1.metric("A Tokens", f"{new_a:.2f}", f"{new_a - initial_a:.2f}")
    col2.metric("B Tokens", f"{new_b:.2f}", f"{new_b - initial_b:.2f}")
    col3.metric("USDC in LP", f"{new_usdc:.2f}", f"{new_usdc - initial_usdc:.2f}")

    st.subheader("Token Prices")
    price_df = pd.DataFrame({
        "Token": ["A", "B"],
        "Initial Price": [initial_a_price, initial_b_price],
        "New Price": [new_a_price, new_b_price]
    })
    st.table(price_df)

    # Visualize token distribution
    fig = go.Figure(data=[
        go.Bar(name='A Tokens', x=['Initial', 'After Purchase'], y=[initial_a, new_a]),
        go.Bar(name='B Tokens', x=['Initial', 'After Purchase'], y=[initial_b, new_b])
    ])
    fig.update_layout(barmode='group', title='Token Distribution')
    st.plotly_chart(fig)

    # Visualize price changes
    price_fig = go.Figure(data=[
        go.Bar(name='A Token Price', x=['Initial', 'After Purchase'], y=[initial_a_price, new_a_price]),
        go.Bar(name='B Token Price', x=['Initial', 'After Purchase'], y=[initial_b_price, new_b_price])
    ])
    price_fig.update_layout(barmode='group', title='Token Prices')
    st.plotly_chart(price_fig)

if __name__ == "__main__":
    main()

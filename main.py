import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def calculate_token_prices(a_amount, b_amount, usdc_amount):
    total_tokens = a_amount + b_amount
    a_price = usdc_amount / total_tokens
    b_price = 1 - a_price
    return a_price, b_price

def buy_token_with_usdc(usdc_amount, current_a, current_b, current_usdc, is_a_token):
    k = current_a * current_b
    if is_a_token:
        new_b = current_b * current_usdc / (current_usdc + usdc_amount)
        tokens_bought = current_a - k / new_b
        new_a = current_a + tokens_bought
    else:
        new_a = current_a * current_usdc / (current_usdc + usdc_amount)
        tokens_bought = current_b - k / new_a
        new_b = current_b + tokens_bought
    
    new_usdc = current_usdc + usdc_amount
    return new_a, new_b, new_usdc, tokens_bought

def main():
    st.title("Polymarket AMM Simulator")

    # Initial state
    initial_a = st.sidebar.number_input("Initial A Tokens", min_value=1, value=1000)
    initial_b = st.sidebar.number_input("Initial B Tokens", min_value=1, value=1000)
    initial_usdc = st.sidebar.number_input("Initial USDC", min_value=1, value=1000)

    # Buy tokens with USDC
    token_to_buy = st.sidebar.selectbox("Token to Buy", ["A", "B"])
    usdc_to_spend = st.sidebar.number_input("USDC to Spend", min_value=0.0, value=0.0, step=0.1)

    # Calculate initial prices
    initial_a_price, initial_b_price = calculate_token_prices(initial_a, initial_b, initial_usdc)

    # Simulate purchase
    if usdc_to_spend > 0:
        new_a, new_b, new_usdc, tokens_bought = buy_token_with_usdc(usdc_to_spend, initial_a, initial_b, initial_usdc, token_to_buy == "A")
        new_a_price, new_b_price = calculate_token_prices(new_a, new_b, new_usdc)
    else:
        new_a, new_b, new_usdc = initial_a, initial_b, initial_usdc
        new_a_price, new_b_price = initial_a_price, initial_b_price
        tokens_bought = 0

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

    # Display intermediate calculations
    st.subheader("Intermediate Calculations")
    st.write(f"Constant product k: {initial_a * initial_b:.2f}")
    if usdc_to_spend > 0:
        if token_to_buy == "A":
            st.write(f"New B tokens: current_b * current_usdc / (current_usdc + usdc_spent) = "
                     f"{initial_b} * {initial_usdc} / ({initial_usdc} + {usdc_to_spend}) = {new_b:.2f}")
            st.write(f"A tokens bought: current_a - k / new_b = "
                     f"{initial_a} - {initial_a * initial_b:.2f} / {new_b:.2f} = {tokens_bought:.2f}")
        else:
            st.write(f"New A tokens: current_a * current_usdc / (current_usdc + usdc_spent) = "
                     f"{initial_a} * {initial_usdc} / ({initial_usdc} + {usdc_to_spend}) = {new_a:.2f}")
            st.write(f"B tokens bought: current_b - k / new_a = "
                     f"{initial_b} - {initial_a * initial_b:.2f} / {new_a:.2f} = {tokens_bought:.2f}")
        st.write(f"USDC spent: {usdc_to_spend:.2f}")
        st.write(f"{token_to_buy} tokens bought: {tokens_bought:.2f}")

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

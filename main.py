import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

class PredictionMarket:
    def __init__(self):
        self.total_invested = 0
        self.investments = {"A": 0, "B": 0}
        self.shares = {"A": 0.5, "B": 0.5}
        self.history = []
        self.buy_pressure = {"A": 0, "B": 0}
        self.sell_pressure = {"A": 0, "B": 0}

    def invest(self, option, amount):
        self.investments[option] += amount
        self.total_invested += amount
        self.update_prices()
        self.history.append({
            'timestamp': datetime.datetime.now(),
            'A': self.shares['A'],
            'B': self.shares['B']
        })
        self.buy_pressure[option] += amount
        self.sell_pressure[option] = max(0, self.sell_pressure[option] - amount)

    def update_prices(self):
        for option in self.investments:
            if self.total_invested > 0:
                self.shares[option] = self.investments[option] / self.total_invested
            else:
                self.shares[option] = 0.5

    def get_price(self, option):
        return self.shares[option]

def create_price_chart(market):
    df = pd.DataFrame(market.history)
    if df.empty:
        fig = go.Figure()
        fig.update_layout(title='Price History (No Data)', xaxis_title='Time', yaxis_title='Price')
        return fig
    df.set_index('timestamp', inplace=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['A'], mode='lines', name='Option A'))
    fig.add_trace(go.Scatter(x=df.index, y=df['B'], mode='lines', name='Option B'))
    fig.update_layout(title='Price History', xaxis_title='Time', yaxis_title='Price')
    return fig

def create_pressure_chart(market):
    data = {
        'Option': ['A', 'B'],
        'Buy Pressure': [market.buy_pressure['A'], market.buy_pressure['B']],
        'Sell Pressure': [market.sell_pressure['A'], market.sell_pressure['B']]
    }
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Option', y=['Buy Pressure', 'Sell Pressure'], title='Buy and Sell Pressure')
    return fig

def create_liquidity_chart(market):
    liquidity = market.total_invested
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = liquidity,
        title = {'text': "Market Liquidity"},
        gauge = {'axis': {'range': [None, max(1000, liquidity)]}}
    ))
    return fig

def main():
    st.title('Polymarket Simulation')

    if 'market' not in st.session_state:
        st.session_state.market = PredictionMarket()

    market = st.session_state.market

    st.sidebar.header('Invest')
    option = st.sidebar.selectbox('Choose option', ['A', 'B'])
    amount = st.sidebar.number_input('Amount to invest', min_value=0.0, value=10.0, step=1.0)
    if st.sidebar.button('Invest'):
        market.invest(option, amount)
        st.sidebar.success(f'Invested {amount} in Option {option}')

    col1, col2 = st.columns(2)
    with col1:
        st.metric('Option A Price', f"{market.get_price('A'):.2f}")
    with col2:
        st.metric('Option B Price', f"{market.get_price('B'):.2f}")

    st.header('Price History')
    st.plotly_chart(create_price_chart(market))

    st.header('Buy and Sell Pressure')
    st.plotly_chart(create_pressure_chart(market))

    st.header('Market Liquidity')
    st.plotly_chart(create_liquidity_chart(market))

    st.header('Market Statistics')
    st.write(f"Total Invested: {market.total_invested:.2f}")
    st.write(f"Investments in A: {market.investments['A']:.2f}")
    st.write(f"Investments in B: {market.investments['B']:.2f}")

if __name__ == "__main__":
    main()
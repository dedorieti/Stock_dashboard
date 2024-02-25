import streamlit as st
import yfinance as yf
from datetime import date, timedelta
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# Define S&P 500 symbol
sp500_symbol = "^GSPC"


# Define top 50 companies by market cap (replace with your preferred source)
top_companies = {
    "Apple": "AAPL",
    "Saudi Aramco": "2222.SR",
    # ... add remaining companies and their symbols
}


# Get user selection
selected_symbols = st.multiselect("Select Stocks:", list(top_companies.keys()))
symbols = [top_companies[symbol] for symbol in selected_symbols]


# Get start and end date
default_end_date = date.today()
default_start_date = default_end_date - timedelta(days=30)
start_date = st.date_input("Start Date:", default_start_date)
end_date = st.date_input("End Date:", default_end_date)


# User-defined window for rolling correlation and volatility
correlation_window = st.slider("Rolling Correlation Window:", 10, 200, 50)
volatility_window = st.slider("Rolling Volatility Window:", 10, 200, 50)


# Define target labels (replace with your data and strategy)
target_labels = ["Buy", "Hold", "Sell"]


# Function to download data, calculate features, and prepare for prediction
def prepare_data_for_prediction(symbols):
    data = yf.download(symbols, period="max")["Close"]

    # Calculate technical indicators (replace with your desired features)
    data["SMA50"] = data.rolling(window=50).mean()
    data["RSI"] = 100 - 100 / (1 + data.diff().abs().rolling(window=14).mean())

    # Prepare features and target labels (replace with actual labels)
    X = data.iloc[:-1, :]
    y = target_labels[:-1]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, scaler


# Function to train and make predictions
def train_and_predict(X_scaled, symbols):
    # Load pre-trained model (replace with your trained model)
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Make predictions for each selected stock
    predictions = {}
    for symbol in symbols:
        stock_data = X_scaled[X_scaled.index.get_loc(symbol)]
        prediction = model.predict([stock_data])[0]
        predictions[symbol] = prediction

    return predictions


# Fetch data only if symbols are selected and dates are valid
if symbols and start_date <= end_date:
    company_data = yf.download([*symbols, sp500_symbol], start=start_date, end=end_date)


# Display stock information and charts
if company_data.empty:
    st.write("No data found for selected symbols or dates.")
else:
    # Prepare data for prediction
    X_scaled, scaler = prepare_data_for_prediction(company_data.symbol)

    # Train model or load pre-trained model (replace with your implementation)
    predictions = train_and_predict(X_scaled, company_data.symbol)

    # Display information and charts for each selected stock
    for symbol, data in company_data.iterrows():
        if symbol in selected_symbols:
            st.header(f"{symbol} - {data['shortName'].iloc[0]}")

            # Existing code for price chart, daily return, moving average (optional), and volatility (optional)

            # Chart for rolling correlation with S&P 500
            st.subheader(f"Rolling Correlation with S&P 500")
            st.line_chart(data[f"{symbol}-S&P 500 Correlation"])

            # Display predicted class
            st.subheader("Predicted Class")
            st.write(predictions[symbol])

            st.markdown("---")

    # Display summary table (optional)
    # ... existing code for summary table

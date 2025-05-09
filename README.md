Gold Price Forecasting using VECM (Vector Error Correction Model)
This project aims to forecast the price of gold using a Vector Error Correction Model (VECM), based on historical data and several macroeconomic variables, such as the USD/VND exchange rate, CPI, and China’s gold reserve.

The model uses Johansen cointegration test to check for long-term relationships between the variables and then builds a VECM to forecast future gold prices. The final forecasts are based on quarterly data, and the results are visualized for better understanding.

Features
Data Preprocessing: The project loads historical data on gold prices, USD/VND exchange rates, CPI, and China’s gold reserves. The data is cleaned and transformed to a quarterly frequency.

Cointegration Test: Johansen cointegration test is used to identify long-term relationships between the variables before fitting the VECM model.

VECM Model: The VECM is used to model the relationships between the variables, and forecast future gold prices.

Visualization: Forecasted gold prices are compared to actual historical values in graphs for easy interpretation.

Dataset
The following datasets are used in this project:

Gold Price: Global gold price data (quarterly).

USD/VND Exchange Rate: Exchange rate between USD and VND (quarterly).

CPI: Consumer Price Index data for Vietnam (quarterly).

China’s Gold Reserve: Data on China’s gold reserves (quarterly).

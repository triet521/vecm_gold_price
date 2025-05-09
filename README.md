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

Libraries are in the req.txt file

Data Transformation
To ensure stationarity of the time series (a key assumption in VECM), we applied the following transformations:

All variables were log-transformed to stabilize variance and reduce skewness.

Then, we took the first difference of the log-transformed series (i.e., dlog_variable) to remove unit roots and achieve stationarity.

These transformed series were used in the Johansen cointegration test and for fitting the VECM model.

Stationarity was validated using:

ADF (Augmented Dickey-Fuller) Test

KPSS (Kwiatkowski–Phillips–Schmidt–Shin) Test

Forecasting and Visualization
After running the pipeline, the forecasted gold prices will be saved to vecm_forecast.csv and vecm_forecast.xlsx. Additionally, a plot will be generated comparing the actual and forecasted gold prices.

To visualize the forecast, use the visualize.py script

This will generate a plot of the historical and forecasted gold prices.

Model Evaluation
After fitting the model, several statistical tests such as ADF (Augmented Dickey-Fuller) and KPSS (Kwiatkowski-Phillips-Schmidt-Shin) are used to check for stationarity of the data series before and after differencing.

The Johansen cointegration test was applied to determine the number of cointegrating relationships between the time series. Based on the test statistics and critical values, a cointegration rank of 4 was selected, indicating that there are four long-term equilibrium relationships among the variables used in the model.

This rank was used as a parameter in the VECM model to capture both short-term dynamics and long-term relationships effectively.

Conclusion
This project provides a framework for forecasting the price of gold using macroeconomic variables and a vector autoregressive model (VECM). The results can be used for analysis or decision-making related to investments in gold.

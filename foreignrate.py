from fredapi import Fred
from dotenv import load_dotenv
import pandas as pd
import os

# Load API key từ file .env
load_dotenv(dotenv_path=".env")
api_key = os.getenv("FRED_API_KEY")

if not api_key:
    raise ValueError("API key FRED không tồn tại. Kiểm tra lại file .env")

fred = Fred(api_key=api_key)

# Lấy tỷ giá USD/VND từ FRED (DEXVZUS)
usd_vnd_daily = fred.get_series('DEXVZUS')
usd_vnd_monthly = usd_vnd_daily.resample('M').mean().to_frame(name='usd_vnd')

print(usd_vnd_monthly.tail())

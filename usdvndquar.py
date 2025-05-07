import pandas as pd

# 1. Đọc CSV đúng delimiter
df = pd.read_csv(
    'usd_vnd_monthly.csv',
    sep=';',               # phân tách theo dấu chấm-phẩy
    parse_dates=['date'],  # tự parse cột 'date'
    dayfirst=False         # format là MM/DD/YYYY
)

# 2. Kiểm tra lại
print(df.columns)  # sẽ ra ['date', 'close', 'high', 'low', 'open']
print(df.head())

# 3. Đặt 'date' làm index
df.set_index('date', inplace=True)

# 4. Resample lên quý (lấy giá cuối mỗi quý)
#    Nếu bạn chỉ cần cột 'close' (tỷ giá trung bình cuối tháng) thì:
df_quarterly = df['close'].resample('Q').last().to_frame()

print(df_quarterly.head())

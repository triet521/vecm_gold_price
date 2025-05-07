import pandas as pd

df = pd.read_csv('AUUSD.csv', sep=';')
print(df.columns)  # Kiểm tra lại tên cột lần nữa
df['date'] = pd.to_datetime(df['date'], dayfirst=True)  # hoặc dayfirst=False nếu tháng trước ngày
df = df.sort_values('date')
df['Quarter'] = df['date'].dt.to_period('Q')

# Làm sạch dữ liệu giá (giả sử giá đang là chuỗi có dấu phẩy)
df['price'] = pd.to_numeric(df['price'].str.replace(',', ''), errors='coerce')

quarterly_avg = df.groupby('Quarter')['price'].mean().reset_index()
quarterly_avg.columns = ['Quarter', 'Average_Gold_Price']

print(quarterly_avg)
quarterly_avg.to_csv('gold_price_by_quarter.csv', index=False)

import pandas as pd
from statsmodels.tsa.vector_ar.var_model import VAR

# 1. Đọc dữ liệu log–series đã chuẩn bị
data = pd.read_csv('combined_quarterly.csv', index_col=0, parse_dates=True)
vars_log = ['log_gold_world', 'log_usd_vnd', 'log_cpi', 'log_reserve']
data_log = data[vars_log]

# 2. Tính sai phân và bỏ NaN
data_diff = data_log.diff().dropna()

# 3. Chọn số lag tối ưu
model = VAR(data_diff)
sel = model.select_order(maxlags=8)
print(sel.summary())

# 4. Lấy p_opt theo AIC, HQIC, hoặc BIC
p_aic  = sel.selected_orders['aic']
p_hqic = sel.selected_orders['hqic']
p_bic  = sel.selected_orders['bic']
print(f"AIC  đề xuất p = {p_aic}")
print(f"HQIC đề xuất p = {p_hqic}")
print(f"BIC  đề xuất p = {p_bic}")

# 5. Chọn p_opt (ví dụ ưu tiên HQIC), ép ≥1 rồi tính k_ar_diff
p_opt    = p_hqic if p_hqic >= 1 else 1
k_ar_diff = max(p_opt - 1, 1)
print(f"Sử dụng k_ar_diff = {k_ar_diff} cho VECM")

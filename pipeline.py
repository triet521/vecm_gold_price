import os
import pandas as pd
from statsmodels.tsa.vector_ar.vecm import coint_johansen, VECM
import joblib
import numpy as np
"""
python pipeline.py --gold "C:/Users/Me/Desktop/usdrate/gold_price_by_quarter.xlsx" --forex "C:/Users/Me/Desktop/usdrate/usd_vnd_quarterly.xlsx" --cpi "C:/Users/Me/Desktop/usdrate/cpivn_quarterly.xlsx" --reserve "C:/Users/Me/Desktop/usdrate/chinagold.xlsx" --date-cols "date" "date" "date" "date""""
class DataLoader:
    """
    Load and resample macro/series data into quarterly freq.
    Supports gold, forex, cpi, reserve; can handle quarter labels or dates.
    """
    def __init__(self, paths: dict, date_cols: dict=None):
        self.paths = paths
        self.date_cols = date_cols or {}

    def _load_series(self, key, col_name, agg: str):
        path = self.paths.get(key)
        if not path:
            return None
        ext = os.path.splitext(path)[1].lower()
        df = pd.read_excel(path, sheet_name=0) if ext in ('.xls', '.xlsx') else pd.read_csv(path)
        dc = self.date_cols.get(key, 'date')
        raw_dates = df.get(dc, df.columns[0])

        # Không chuyển đổi ngày nữa, chỉ giữ nguyên cột 'date'
        df['date'] = raw_dates

        df = df.rename(columns={col_name: key})
        df = df.dropna(subset=['date']).sort_values('date')
        df[key] = pd.to_numeric(df[key].astype(str).str.replace(',', ''), errors='coerce')
        df = df.dropna(subset=[key]).set_index('date')
        if agg == 'mean':
            return df[key].resample('Q').mean().to_frame(key)
        return df[key].resample('Q').last().to_frame(key)

    def load_all(self):
        parts = []
        # Load gold
        gold = self._load_series('gold', 'price', 'mean')
        if gold is not None:
            gold.columns = ['gold_world']
            # Apply log transformation
            gold['log_gold_world'] = np.log(gold['gold_world'])
            parts.append(gold)
        # Load forex
        forex = self._load_series('forex', 'close', 'last')
        if forex is not None:
            forex.columns = ['usd_vnd']
            # Apply log transformation
            forex['log_usd_vnd'] = np.log(forex['usd_vnd'])
            parts.append(forex)
        # Load CPI
        cpi = self._load_series('cpi', 'value', 'last')
        if cpi is not None:
            cpi.columns = ['cpi']
            # Apply log transformation
            cpi['log_cpi'] = np.log(cpi['cpi'])
            parts.append(cpi)
        # Load Reserve
        reserve = self._load_series('reserve', 'reserve', 'last')
        if reserve is not None:
            reserve.columns = ['reserve']
            # Apply log transformation
            reserve['log_reserve'] = np.log(reserve['reserve'])
            parts.append(reserve)

        if not parts:
            raise ValueError("No data series loaded. Please specify at least --gold file.")
        if len(parts) == 1:
            data = parts[0]
        else:
            data = pd.concat(parts, axis=1).dropna()
        # Export combined or single
        data.to_csv('combined_quarterly.csv')
        data.to_excel('combined_quarterly.xlsx')
        print("Exported combined_quarterly.csv/xlsx")
        return data

class DataPreprocessor:
    """Run Johansen test"""
    def __init__(self, det_order=0, k_ar_diff=1):
        self.det_order = det_order
        self.k_ar_diff = k_ar_diff
    def prepare(self, data):
        res = coint_johansen(data, det_order=self.det_order, k_ar_diff=self.k_ar_diff)
        print("Eigenvalues:\n", res.eig)
        return data

class VECMPipeline:
    """Fit and forecast VECM"""
    def __init__(self, data, k_ar_diff=1, coint_rank=1, deterministic='co'):
        self.data = data
        self.k_ar_diff = k_ar_diff
        self.coint_rank = coint_rank
        self.deterministic = deterministic
        self.results = None
    def fit(self):
        self.results = VECM(self.data, k_ar_diff=self.k_ar_diff,
                             coint_rank=self.coint_rank,
                             deterministic=self.deterministic).fit()
        return self.results
    def forecast(self, steps=4):
        if self.results is None:
            raise ValueError("Model must be fit first.")
        fc = self.results.predict(steps=steps)
        idx = pd.date_range(self.data.index[-1], periods=steps+1, freq='Q')[1:]
        df_fc = pd.DataFrame(fc, index=idx, columns=self.data.columns)
        
        # Calculate percentage change for each column
        last_actual = self.data.iloc[-1]  # Last actual values
        
        pct_change = {}
        for col in df_fc.columns:
            if 'log' in col:  # If the column is in log scale, we compute log difference
                pct_change[col] = (df_fc[col].iloc[0] - last_actual[col]) * 100
            else:  # For non-log values, we compute the percentage change directly
                pct_change[col] = (df_fc[col].iloc[0] - last_actual[col]) / last_actual[col] * 100
        
        # Convert to DataFrame for better readability
        pct_change_df = pd.DataFrame(pct_change, index=["Percentage Change"])
        
        print("\nPercentage Change in Forecasted Values:\n", pct_change_df)
        
        # Calculate trend (Increase/Decrease) for the first step
        trend = {}
        for col in pct_change:
            trend[col] = "Increase" if pct_change[col] > 0 else "Decrease"
        
        print("\nTrend Analysis:")
        for col in trend:
            print(f"{col}: {trend[col]}")
        
        df_fc.to_csv('vecm_forecast.csv')
        df_fc.to_excel('vecm_forecast.xlsx')
        print("Exported vecm_forecast.csv/xlsx")
        return df_fc
    def save_model(self, path='vecm_model.pkl'):
        joblib.dump(self.results, path)
        print(f"Saved model to {path}")


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='VECM with macro series')
    p.add_argument('--gold', help='World gold price file')
    p.add_argument('--forex', help='USD/VND rate file')
    p.add_argument('--cpi', help='CPI file')
    p.add_argument('--reserve', help='China gold reserve file')
    p.add_argument('--date-cols', nargs=4, metavar=('GOLD','FOREX','CPI','RESERVE'),
                   help='Date column names for gold, forex, cpi, reserve')
    p.add_argument('--lag', type=int, default=1, help='Difference lag')
    p.add_argument('--rank', type=int, default=1, help='Cointegration rank')
    p.add_argument('--det', default='co', help='Deterministic term')
    p.add_argument('--steps', type=int, default=4, help='Forecast quarters')
    args = p.parse_args()

    date_cols = {}
    if args.date_cols:
        date_cols = {'gold': args.date_cols[0],
                     'forex': args.date_cols[1],
                     'cpi': args.date_cols[2],
                     'reserve': args.date_cols[3]}
    paths = {'gold': args.gold, 'forex': args.forex, 'cpi': args.cpi, 'reserve': args.reserve}
    loader = DataLoader(paths, date_cols)
    data = loader.load_all()
    dp = DataPreprocessor(det_order=0, k_ar_diff=args.lag)
    data = dp.prepare(data)
    pipe = VECMPipeline(data, k_ar_diff=args.lag,
                        coint_rank=args.rank, deterministic=args.det)
    res = pipe.fit()
    print(res.summary())
    fc = pipe.forecast(steps=args.steps)
    print("Forecasts:\n", fc)
    pipe.save_model()

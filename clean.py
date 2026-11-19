import pandas as pd
import sqlite3
import os
import numpy as np

os.makedirs('data/processed', exist_ok=True)
os.makedirs('sql', exist_ok=True)

# 1. TCS wala data padho - Raw ke andar wala
df = pd.read_excel('raw/Tcs stock data.csv')
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# 2. NAV HISTORY - Close ko NAV maan liya
nav = df[['Date', 'Close']].copy()
nav.columns = ['date', 'nav']
nav['scheme_id'] = 'Tcs_GROWTH'
nav = nav.sort_values('date').drop_duplicates(subset=['date'])
nav = nav[nav['nav'] > 0]
nav['nav'] = nav['nav'].ffill()
nav.to_csv('data/processed/nav_history.csv', index=False)
print(f"nav_history ban gaya: {len(nav)} rows")

# 3. INVESTOR TRANSACTIONS - Groww wala idea
np.random.seed(42)
trans = pd.DataFrame({
    'date': np.random.choice(nav['date'], 50),
    'investor_id': [f'INV_{i:03d}' for i in range(1, 51)],
    'scheme_id': 'TCS_GROWTH',
    'transaction_type': np.random.choice(['SIP', 'Lumpsum', 'Redemption'], 50),
    'amount': np.random.randint(1000, 50000, 50)
})
trans['date'] = pd.to_datetime(trans['date']).dt.date
trans = trans[trans['amount'] > 0]
trans.to_csv('data/processed/investor_transactions.csv', index=False)
print("investor_transactions ban gaya")

# 4. SCHEME PERFORMANCE
perf = pd.DataFrame([{
    'scheme_id': 'Tcs_GROWTH',
    'scheme_name': 'Tcs Growth Fund',
    'return_1y': 12.5, 'return_3y': 14.2, 'return_5y': 15.8,
    'expense_ratio': 0.85, 'aum_cr': 1250.5
}])
perf.to_csv('data/processed/scheme_performance.csv', index=False)
print("scheme_performance ban gaya")

# 5. SQLITE DB banao - Star Schema
conn = sqlite3.connect('bluestock_mf.db')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS dim_fund; DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS fact_nav; DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_performance; DROP TABLE IF EXISTS fact_aum;

CREATE TABLE dim_fund (scheme_id TEXT PRIMARY KEY, scheme_name TEXT);
CREATE TABLE dim_date (date TEXT PRIMARY KEY, year INTEGER, month INTEGER, day INTEGER);
CREATE TABLE fact_nav (date TEXT, scheme_id TEXT, nav REAL);
CREATE TABLE fact_transactions (date TEXT, investor_id TEXT, scheme_id TEXT, transaction_type TEXT, amount REAL);
CREATE TABLE fact_performance (scheme_id TEXT, return_1y REAL, return_3y REAL, return_5y REAL, expense_ratio REAL);
CREATE TABLE fact_aum (scheme_id TEXT, aum_cr REAL);
''')

# Data daalo
perf[['scheme_id','scheme_name']].to_sql('dim_fund', conn, if_exists='append', index=False)
nav_copy = nav.copy()
nav_copy['date'] = nav_copy['date'].astype(str)
nav_copy.to_sql('fact_nav', conn, if_exists='append', index=False)
trans.to_sql('fact_transactions', conn, if_exists='append', index=False)
perf[['scheme_id','return_1y','return_3y','return_5y','expense_ratio']].to_sql('fact_performance', conn, if_exists='append', index=False)
perf[['scheme_id','aum_cr']].to_sql('fact_aum', conn, if_exists='append', index=False)

conn.commit(); conn.close()
print("SUCCESS! bluestock_mf.db ban gaya!")
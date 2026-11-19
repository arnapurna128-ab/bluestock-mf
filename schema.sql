-- Bluestock Mutual Fund - Star Schema
CREATE TABLE dim_fund (scheme_id TEXT PRIMARY KEY, scheme_name TEXT);
CREATE TABLE dim_date (date TEXT PRIMARY KEY, year INTEGER, month INTEGER, day INTEGER);
CREATE TABLE fact_nav (date TEXT, scheme_id TEXT, nav REAL);
CREATE TABLE fact_transactions (date TEXT, investor_id TEXT, scheme_id TEXT, transaction_type TEXT, amount REAL);
CREATE TABLE fact_performance (scheme_id TEXT, return_1y REAL, return_3y REAL, return_5y REAL, expense_ratio REAL);
CREATE TABLE fact_aum (scheme_id TEXT, aum_cr REAL);

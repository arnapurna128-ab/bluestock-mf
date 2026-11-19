SELECT transaction_type, SUM(amount) FROM fact_transactions GROUP BY transaction_type;
SELECT date, nav FROM fact_nav ORDER BY date;
SELECT * FROM fact_performance ORDER BY return_5y DESC;
SELECT date, SUM(amount) FROM fact_transactions GROUP BY date;
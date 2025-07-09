SET SQL_SAFE_UPDATES = 0;
USE fraud_detection;

ALTER TABLE transactions DROP COLUMN IsFraud;
ALTER TABLE transactions DROP COLUMN FraudReason;

ALTER TABLE transactions
ADD COLUMN IsFraud TINYINT DEFAULT 0;

ALTER TABLE transactions
ADD COLUMN FraudReason VARCHAR(255) DEFAULT "N/A";

UPDATE transactions
SET IsFraud = 1,
	FraudReason = "Over $10,000"
WHERE amount > 10000.00;

UPDATE transactions
SET IsFraud = 1,
	FraudReason = "Between 2 and 5 AM"
WHERE HOUR(date) between 2 and 4;

UPDATE transactions
SET IsFraud = 1,
	FraudReason = "Multiple Locations"
WHERE user_id IN (
	SELECT user_id
    FROM (
		select user_id
        FROM transactions
        GROUP BY user_id
        HAVING COUNT(DISTINCT location) > 6
	) AS temp
);

UPDATE transactions
SET IsFraud = 1,
	FraudReason = "5+ Transactions/Hour"
WHERE (user_id, DATE(date), HOUR(date)) IN (
    SELECT user_id, DATE(date), HOUR(date)
    FROM (
        SELECT user_id, DATE(date), HOUR(date)
        FROM transactions
        GROUP BY user_id, DATE(date), HOUR(date)
        HAVING COUNT(*) >= 5
    ) AS suspicious
);

SELECT * FROM transactions;
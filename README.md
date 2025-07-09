## Credit Card Fraud Detection & Analysis ##

## Overview ##
This project focuses on analyzing and detecting fraudulent credit card transactions using a Python-generated dataset, SQL-based detection rules, and Power BI visualizations. The goal is to identify anomalous patterns in transaction behavior based on factors such as amount, time, and location. In addition to the exploratory analysis and rule-based logic, I developed a Python script that evaluates new transactions and determines whether they are likely to be fraudulent.

## Tools Used ##
- Python - data generation and fraud detection
    - Faker - to generate fake data
    - random, csv, os, datetime - used for logic and file handling
    - NumPy, Pandas - for data manipulation and analysis
    - scikit-learn - for machine learning
- SQL - for rule-based detection queries
- PowerBI - building interactive dashboard and visualizations

## Dataset Generation ##
A dataset of 1,000 randomized credit card transactions was created using a Python script, *transaction_dataset_creation.py*, and saved as *transaction_dataset.csv*. The dataset includes the following fields:
- transaction_id (INT): Auto-incremented identifier
- user_id (INT): Randomizer user reference
- date (DATETIME): Random timestamp
- amount (FLOAT): Transaction amount
- category (STR): Merchant category from a pre-defined list
- location (STR): Random popular U.S. cities from a pre-defined list

## SQL Schema & Data Import ##
- A schema named *fraud_detection* was created in MySQL workbench.
  
        USE fraud_detection;
  
- The CSV file was imported using the Table Data Import Wizard.
Two additional columns were added to the *transactions* table:
    -  IsFraud (BOOLEAN): based on the following rules before
    - FraudReason (VARCHAR)

        ALTER TABLE transactions DROP COLUMN IsFraud;
        ALTER TABLE transactions DROP COLUMN FraudReason;
        ALTER TABLE transactions
        ADD COLUMN IsFraud TINYINT DEFAULT 0;
        ALTER TABLE transactions
        ADD COLUMN FraudReason VARCHAR(255) DEFAULT "N/A";

## Fraud Detection Rules ##
The following rules were applied to flag transactions as fraud:

1. Hihgh-Value Transactions (>$10,000)

        UPDATE transactions
        SET IsFraud = 1,
        	FraudReason = "Over $10,000"
        WHERE amount > 10000.00;

3. Suspicious Time Window (Between 2 AM - 5 AM)
   
        UPDATE transactions
        SET IsFraud = 1,
        	FraudReason = "Between 2 and 5 AM"
        WHERE HOUR(date) between 2 and 4;

5. Geographic Anomalies (More than 6 unique locations per user)
   
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

7. Transaction Velocity (>= 5 transactions per hour)
   
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

To view final dataset:

          SELECT * FROM transactions;

## Analysis ##
PowerBI was used to visualize and derive insights from the processed data:
1. Donut Chart: Fraudulent vs. Legitimate Transactions
     - Segmented by fraud reason identifying which rules are flagged as fraudulent most often
3.  Top 10 Fraud Locations Bar Chart
     - Number of fraudulent cases by U.S. city broken down by merchant category identifying high-risk geographies and industries
4. Total Fraud Cases by Reason Bar Chart
     - Number of fraudulent cases per rule highlighting the most common fraudulent patterns  
5. Timeline of Fradulent Spending (Line Chart)
     - Total fraudulent amounts spent over time by fraud reason to detect seasonal trends in specific fraud types

**High-Value Fraud**
- Threshold: > $10,000

**Time-Based Fraud**
- Window: 2 AM - 5 AM
- 11% of fraud occurs in this range
- Highlighting card misuse during sleep hours

**Geographic Anomalies**
- Users with transactions from more than six unique U.S. cities
- Highlighting potential compromised accounts or travel-related fraud

**Rapid Transaction Frequency**
- 5+ transactions/hour/user
- Suggests possible stolen card information or bots

# Files Included ##
transaction_dataset_creation.py - Python script to create transaction_dataset.csv

transaction_dataset.csv - Simulated credit card transaction dataset from the Python script

transactions_updated.csv - updated transaction dataset with the fraud labels and reasons

fraud_dashboard: PowerBI dashboard

fraud_dashboard.pdf - PowerBI dashboard as a PDF

## Conclusion ##
This project demonstrates how rule-based SQL detection and interactive dashboarding in Power BI can be used to identify and interpret suspicious activity in financial data. It serves as a foundation for future enhancements using machine learning, anomaly detection, or real-time fraud monitoring systems.'

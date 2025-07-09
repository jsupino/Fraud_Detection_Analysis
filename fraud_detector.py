import numpy as np
import pandas as pd
from datetime import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

df = pd.read_csv("C:/Users/supin/Desktop/fraud_analysis/transactions_updated.csv")
df['date'] = pd.to_datetime(df['date']) # Ensure datetime format
df = df.sort_values(by=['user_id','date'])
user_history = {}
for user_id, group in df.groupby('user_id'):
     user_history[user_id] = {
          'location': set(group['location']),
          'timestamps': list(group['date'])
     }

def detect_fraud(transaction, user_history):
    amount = transaction['amount']
    hour = pd.to_datetime(transaction['date'])
    txn_time = hour.time()
    location = transaction['location']
    user_locations = user_history.get('locations', set())
    timestamps = user_history.get('timestamps', [])

    if amount > 10000:
        return True, "High Transaction Amount"
    if hour(2,0) <= txn_time <= hour(5,0):
        return True, "Odd hour"
    if location not in user_locations and len(user_locations) > 6:
            return True, "Geographic Anomaly"
    recent_txns = [t for t in timestamps if abs((hour - t).total_seconds()) <= 3600]
    if len(recent_txns) >= 5:
        return True, "Rapid Transaction Frequency"
    
    return False, None

# Encode categorical features
df = pd.get_dummies(df, columns=['category','location'], drop_first=True) # one-hot encode

X = df.drop(columns=['IsFraud', 'date', 'user_id', 'FraudReason'])
y = df['IsFraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test, y_pred))


# Create a new transaction
new_transaction1 = {
     'user_id': 41,
     'date': '4/20/2025 8:30:40',
     'amount': 11050.00,
     'category': 'electronics',
     'location': 'Miami'
}

df1 = pd.DataFrame([new_transaction1])

# Get user history from dataset
uid = new_transaction1['user_id']
user_history = user_history.get(uid, {'locations': set(), 'timestamps': []})

# Apply the fraud detection rules
is_fraud, fraud_reason = detect_fraud(new_transaction1, user_history)
print(f"Fraud?: {'YES' if is_fraud else 'NO'} | Reason: {fraud_reason}")
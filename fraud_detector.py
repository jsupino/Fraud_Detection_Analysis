import numpy as np
import pandas as pd
from datetime import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("fraud_analysis/transactions_updated.csv")
df['date'] = pd.to_datetime(df['date']) # Ensure datetime format
df = df.sort_values(by=['user_id','date'])

# Encode categorical features
df = pd.get_dummies(df, columns=['category','location'], drop_first=True) # one-hot encode

X = df.drop(columns=['IsFraud', 'date', 'user_id', 'FraudReason'])
y = df['IsFraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest model
model = RandomForestClassifier(n_estimators=100,
                               class_weight='balanced',
                               random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test, y_pred))


# Example new transaction
new_transaction1 = {
     'user_id': 120,
     'date': '4/20/2025 8:30:40',
     'amount': 12000.00,
     'category': 'electronics',
     'location': 'Miami'
}

new_transaction1 = pd.DataFrame([new_transaction1])
new_transaction1 = pd.get_dummies(new_transaction1)

# Align columns with the training data
new_transaction1 = new_transaction1.reindex(columns=X_train.columns, fill_value=0) # fill missing columns with 0

# Apply the fraud detection rules
is_fraud = model.predict(new_transaction1)[0]
prob_is_fraud = model.predict_proba(new_transaction1)[0][1]

# Create threshold for fraudulent activity
threshold = 0.35
print(f"Fraud (threshold {threshold:.0%})... Fraud?: {'YES' if prob_is_fraud >= threshold else 'NO'} | Confidence: {prob_is_fraud:.2%}")

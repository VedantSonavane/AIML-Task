"""
train_example.py - Example model training script
This shows one possible approach to solving the problem.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)
import pickle
import json
import os

# Create outputs directory
os.makedirs('outputs', exist_ok=True)

print("=" * 60)
print("LEAD CONVERSION PREDICTION MODEL TRAINING")
print("=" * 60)

# ===== 1. LOAD DATA =====
print("\n1. Loading data...")
leads = pd.read_csv('data/leads.csv')
interactions = pd.read_csv('data/interactions.csv')

print(f"   Leads shape: {leads.shape}")
print(f"   Interactions shape: {interactions.shape}")

# ===== 2. PREPROCESSING =====
print("\n2. Preprocessing...")

# Remove rows with future timestamps
interactions = interactions[pd.to_datetime(interactions['timestamp']) <= pd.Timestamp.now()]

# Handle missing values
interactions['utm_source'].fillna('direct', inplace=True)
interactions['utm_campaign'].fillna('none', inplace=True)
interactions['funnel_stage'].fillna('awareness', inplace=True)

leads['location'].fillna('unknown', inplace=True)

print(f"   After cleaning: {interactions.shape[0]} interactions")

# ===== 3. FEATURE ENGINEERING =====
print("\n3. Engineering features...")

# Create session-level features
session_features = interactions.groupby(['lead_id', 'session_id']).agg({
    'duration_seconds': ['sum', 'mean', 'count'],
    'scroll_depth': 'mean',
    'converted': 'max'
}).reset_index()

session_features.columns = ['lead_id', 'session_id', 
                            'session_duration', 'avg_page_duration', 
                            'pages_visited', 'avg_scroll_depth', 'session_converted']

# Create lead-level features
lead_features = pd.DataFrame()

# Count features
lead_features['session_count'] = interactions.groupby('lead_id')['session_id'].nunique()
lead_features['total_interactions'] = interactions.groupby('lead_id').size()
lead_features['total_time_spent'] = interactions.groupby('lead_id')['duration_seconds'].sum()

# Event-based features
lead_features['demo_requests'] = (
    interactions[interactions['event_name'] == 'demo_request']
    .groupby('lead_id').size()
)
lead_features['pricing_views'] = (
    interactions[interactions['page_name'] == 'pricing']
    .groupby('lead_id').size()
)
lead_features['whatsapp_clicks'] = (
    interactions[interactions['event_name'] == 'whatsapp_click']
    .groupby('lead_id').size()
)
lead_features['email_opens'] = (
    interactions[interactions['event_name'] == 'email_open']
    .groupby('lead_id').size()
)

# Fill NaN with 0 for count features
lead_features = lead_features.fillna(0)

# Merge with leads data
X = leads[['lead_id']].copy()
X = X.merge(lead_features.reset_index(), on='lead_id', how='left')
X = X.merge(leads[['lead_id', 'source', 'company_size', 'segment']], on='lead_id', how='left')

# Target variable
y = leads['converted'].copy()

# Encode categorical variables
X['source_encoded'] = pd.Categorical(X['source']).codes
X['company_size_encoded'] = pd.Categorical(X['company_size']).codes
X['segment_encoded'] = pd.Categorical(X['segment']).codes

# Select features for model
feature_columns = [
    'session_count', 'total_interactions', 'total_time_spent',
    'demo_requests', 'pricing_views', 'whatsapp_clicks', 'email_opens',
    'source_encoded', 'company_size_encoded', 'segment_encoded'
]

X_model = X[feature_columns].fillna(0)

print(f"   Created {len(feature_columns)} features")
print(f"   Sample features: {feature_columns[:3]}")

# ===== 4. TRAIN/TEST SPLIT =====
print("\n4. Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X_model, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Train set: {X_train.shape[0]} ({y_train.sum()} positives)")
print(f"   Test set: {X_test.shape[0]} ({y_test.sum()} positives)")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ===== 5. MODEL TRAINING =====
print("\n5. Training models...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'XGBoost': xgb.XGBClassifier(n_estimators=100, random_state=42, verbosity=0)
}

results = {}
best_model = None
best_f1 = 0

for name, model in models.items():
    # Train
    if 'Logistic' in name:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc_roc = roc_auc_score(y_test, y_pred_proba)
    
    results[name] = {
        'accuracy': round(accuracy, 3),
        'precision': round(precision, 3),
        'recall': round(recall, 3),
        'f1': round(f1, 3),
        'auc_roc': round(auc_roc, 3)
    }
    
    print(f"\n   {name}:")
    print(f"      Accuracy:  {accuracy:.3f}")
    print(f"      Precision: {precision:.3f}")
    print(f"      Recall:    {recall:.3f}")
    print(f"      F1 Score:  {f1:.3f}")
    print(f"      AUC-ROC:   {auc_roc:.3f}")
    
    if f1 > best_f1:
        best_f1 = f1
        best_model = model
        best_model_name = name

# ===== 6. SAVE MODEL =====
print(f"\n6. Saving best model ({best_model_name})...")
with open('model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

with open('outputs/model_metrics.json', 'w') as f:
    json.dump(results, f, indent=2)

print("   ✓ Model saved to model.pkl")
print("   ✓ Metrics saved to outputs/model_metrics.json")

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

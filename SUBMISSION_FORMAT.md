# 📤 Submission Format

Follow this format exactly. Deviations may result in automatic rejection.

---

## GitHub Repository Setup

### Naming Convention
```
{your-name}-aiml-assessment
```

Example:
```
john-doe-aiml-assessment
https://github.com/johndoe/john-doe-aiml-assessment
```

---

## Repository Structure (REQUIRED)

```
your-repo/
├── README.md                    ← Main project documentation
├── analysis.md                  ← EDA findings and insights
├── requirements.txt             ← Python dependencies
├── train.py                     ← Model training script
├── app.py                       ← FastAPI application
├── model.pkl                    ← Serialized trained model
├── config.py                    ← Configuration (optional but recommended)
├── utils.py                     ← Helper functions (optional)
├── data/
│   ├── leads.csv               ← Provided dataset
│   ├── interactions.csv        ← Provided dataset
│   └── sample_data.csv         ← Optional: sample for testing
├── outputs/
│   ├── model_metrics.json      ← Model performance metrics
│   └── feature_importance.png  ← Feature importance visualization
└── .gitignore                  ← Must exclude *.csv, *.pkl from large files
```

---

## REQUIRED FILES

### 1. `README.md`

Your main documentation. Must include:

**Sections**:
- Project Overview
- Problem Statement
- Dataset Description
- Approach & Methodology
- Setup Instructions
- How to Run Training
- How to Run API
- API Documentation (endpoints, examples)
- Model Performance Results
- Key Findings
- Limitations & Future Work
- Author & Contact

**Example Structure**:
```markdown
# Lead Conversion Prediction API

## Overview
This project predicts whether a lead will convert to a customer using historical behavioral data.

## Dataset
- **leads.csv**: 2,000 customer leads with attributes (source, company, segment, etc.)
- **interactions.csv**: 40,000 behavioral interactions (page views, clicks, etc.)

## Approach
1. EDA: Analyzed lead sources, engagement patterns, temporal trends
2. Feature Engineering: Created session-level and lead-level features
3. Model Selection: Trained Logistic Regression, Random Forest, XGBoost
4. Evaluation: Selected best model based on F1 and AUC-ROC
5. Deployment: Built FastAPI service for real-time predictions

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Training
```bash
python train.py
```

## Running API
```bash
uvicorn app:app --reload
```

## API Endpoints
...
```

---

### 2. `analysis.md`

Detailed EDA findings. Must include:

**Sections**:
- Data Overview (shapes, types, missing values)
- Univariate Analysis
- Bivariate Analysis (features vs conversion)
- Behavioral Segments Discovered
- Anomalies & Data Quality Issues
- Temporal Patterns
- Key Insights
- Business Recommendations

**Example**:
```markdown
# Exploratory Data Analysis

## Data Overview
- Leads: 2,000 records with 9 features
- Interactions: 40,000 records with 15 features
- Conversion Rate: 15%
- Missing Values: 2% across all columns

## Top Insights
1. Leads from 'Referral' source have 2x higher conversion than 'Ads'
2. Leads with 3+ sessions convert at 65% vs 10% for single-session leads
3. Pricing page visits are the strongest conversion predictor
4. December shows 40% higher demo requests than other months

## Segments
- High Intent (5%): pricing + demo → 78% conversion
- Researchers (30%): case studies + resources → 8% conversion
- Window Shoppers (50%): blog views only → 2% conversion
- Fast Converters (15%): direct to pricing → 60% conversion
```

---

### 3. `requirements.txt`

All Python dependencies. Example:

```
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.3.0
xgboost==2.0.0
matplotlib==3.8.0
seaborn==0.12.0
fastapi==0.104.0
uvicorn==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
joblib==1.3.0
requests==2.31.0
openai==1.3.0  # if using OpenAI API
```

---

### 4. `train.py`

Model training script. Must:

- Load data from CSV
- Preprocess (handle missing values, outliers)
- Engineer features
- Split data (80/20)
- Train multiple models
- Evaluate and select best model
- Save model as `model.pkl`
- Output metrics to `outputs/model_metrics.json`

**Example Structure**:
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import pickle
import json

# Load data
leads = pd.read_csv('data/leads.csv')
interactions = pd.read_csv('data/interactions.csv')

# Preprocess
# ... handle missing values, outliers ...

# Feature engineering
# ... create session features, recency, frequency ...

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train models
models = {
    'logistic_regression': LogisticRegression(),
    'random_forest': RandomForestClassifier(),
    'xgboost': xgb.XGBClassifier()
}

best_model = None
best_score = 0

for name, model in models.items():
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"{name}: {score}")
    
    if score > best_score:
        best_score = score
        best_model = model

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

# Save metrics
metrics = {
    'accuracy': accuracy_score(y_test, best_model.predict(X_test)),
    'precision': precision_score(y_test, best_model.predict(X_test)),
    'recall': recall_score(y_test, best_model.predict(X_test)),
    'f1': f1_score(y_test, best_model.predict(X_test)),
    'auc_roc': roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1])
}

with open('outputs/model_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
```

---

### 5. `app.py`

FastAPI application. Must include:

**Endpoint 1: `/predict` (POST)**
```python
from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

class PredictionInput(BaseModel):
    pages_visited: int
    time_spent_minutes: float
    demo_requests: int
    whatsapp_clicks: int
    pricing_views: int
    email_opens: int
    session_count: int
    days_since_first_visit: int
    source: str
    company_size: str

@app.post('/predict')
def predict(input_data: PredictionInput):
    # Prepare features
    features = prepare_features(input_data)
    
    # Get prediction
    probability = model.predict_proba(features)[0][1]
    
    return {
        "conversion_probability": round(probability, 2),
        "confidence": "high" if probability > 0.7 else "medium" if probability > 0.4 else "low"
    }
```

**Endpoint 2: `/explain` (POST)**
```python
class ExplainInput(BaseModel):
    conversion_probability: float
    pages_visited: int
    demo_requests: int
    pricing_views: int

@app.post('/explain')
def explain(input_data: ExplainInput):
    summary = generate_explanation(input_data)
    return {"summary": summary}

def generate_explanation(data):
    # Rule-based or LLM-based explanation
    if data.demo_requests > 0:
        return "Lead showed high intent through demo request."
    elif data.pricing_views > 2:
        return "Lead demonstrated pricing interest with multiple visits."
    else:
        return "Lead shows moderate engagement."
```

---

### 6. `model.pkl`

Serialized trained model. Must be committable (< 100MB).

---

### 7. `.gitignore`

Must include:
```
venv/
__pycache__/
*.pyc
.DS_Store
.env
data/leads.csv
data/interactions.csv
outputs/*.csv
.pytest_cache/
```

---

## Commit Requirements

### Minimum Commits: 10+

Each commit should be meaningful:

```
1. Initial project setup
2. EDA: Load and explore data
3. EDA: Visualizations and analysis
4. Feature engineering: Session-level features
5. Feature engineering: Lead-level features
6. Model training: Baseline models
7. Model selection: XGBoost tuning
8. API: Implement /predict endpoint
9. API: Implement /explain endpoint
10. Documentation: Final README and comments
```

### Commit Message Format

✅ GOOD:
```
feat: Add session-level feature engineering
fix: Handle missing values in preprocessing
docs: Update README with API examples
refactor: Extract feature creation to utils
test: Add model evaluation metrics
```

❌ BAD:
```
update
fix stuff
final
asdf
```

---

## Code Quality Checklist

- [ ] All functions have docstrings
- [ ] Variable names are descriptive
- [ ] Code follows PEP 8 style guide
- [ ] No hardcoded values (use config)
- [ ] Error handling in API endpoints
- [ ] Data validation in API inputs
- [ ] Comments explaining complex logic
- [ ] No print() statements (use logging)

---

## Data Files

### DO NOT Commit Large Files

```
.gitignore
data/leads.csv           # DON'T commit
data/interactions.csv    # DON'T commit
model.pkl               # OK to commit (< 100MB)
outputs/*.pkl           # OK to commit
```

### HOW Reviewers Will Test

They will:
1. Clone your repo
2. Run `pip install -r requirements.txt`
3. Run `python train.py` (model re-trains)
4. Run `uvicorn app:app --reload`
5. Test API endpoints
6. Review code and commit history

---

## Submission Checklist

Before pushing to GitHub:

- [ ] README.md is complete and clear
- [ ] analysis.md contains detailed EDA
- [ ] requirements.txt lists all dependencies
- [ ] train.py runs without errors
- [ ] app.py runs and API endpoints work
- [ ] model.pkl exists and is < 100MB
- [ ] outputs/model_metrics.json exists
- [ ] .gitignore properly configured
- [ ] Commit history shows progression (10+ commits)
- [ ] No data files committed
- [ ] No .env files committed
- [ ] All code is clean and documented

---

## Submission Link Format

Send:
```
https://github.com/{your-username}/{your-repo-name}
```

Example:
```
https://github.com/janedoe/jane-doe-aiml-assessment
```

---

## 🚫 Auto-Rejection Criteria

Your submission will be REJECTED if:

❌ No commit history (looks AI-generated)
❌ README is missing or incomplete
❌ train.py doesn't run
❌ app.py has syntax errors
❌ API endpoints don't work
❌ Data files committed to repo
❌ No model.pkl file
❌ No analysis.md
❌ Hardcoded outputs in code
❌ Cannot reproduce results locally

---

## Questions?

Contact: **hr@vynqe.com**

Good luck! 🚀

# 🧪 Evaluation Rubric

This is how candidates will be scored. Share this with them.

---

## Scoring Overview

**Total Points**: 100

| Category | Points | Weight |
|----------|--------|--------|
| EDA & Analysis | 20 | 20% |
| Model Quality | 25 | 25% |
| API Implementation | 20 | 20% |
| Code Quality | 15 | 15% |
| Documentation | 10 | 10% |
| Git Practices | 10 | 10% |

---

## 📊 Category Breakdown

### 1. EDA & Analysis (20 points)

**Excellent (18-20 points)**
- [ ] Comprehensive data exploration with clear findings
- [ ] Identifies hidden patterns, segments, anomalies
- [ ] Creates meaningful visualizations
- [ ] Answers all business questions
- [ ] Actionable insights for stakeholders
- [ ] Analysis clearly documented in `analysis.md`

**Good (14-17 points)**
- [ ] Solid EDA covering main dimensions
- [ ] Identifies key features and patterns
- [ ] Basic visualizations
- [ ] Mostly complete analysis
- [ ] Some insights provided

**Adequate (10-13 points)**
- [ ] Basic data exploration
- [ ] Identifies obvious patterns
- [ ] Minimal visualizations
- [ ] Incomplete analysis
- [ ] Limited insights

**Poor (0-9 points)**
- [ ] Minimal exploration
- [ ] Misses key patterns
- [ ] No visualizations
- [ ] Incomplete or confusing analysis

---

### 2. Model Quality (25 points)

**Excellent (22-25 points)**
- [ ] Feature engineering is thoughtful and business-driven
- [ ] Multiple models tested (Logistic Regression, RF, XGBoost)
- [ ] Model selection is justified
- [ ] Strong metrics (F1 > 0.75, AUC-ROC > 0.80)
- [ ] Handles class imbalance (if applicable)
- [ ] No data leakage
- [ ] Proper train/test split methodology
- [ ] Feature importance explained

**Good (18-21 points)**
- [ ] Reasonable feature engineering
- [ ] 2+ models tested
- [ ] Good metrics (F1 0.65-0.75, AUC-ROC 0.70-0.80)
- [ ] Proper train/test split
- [ ] Some data validation

**Adequate (14-17 points)**
- [ ] Basic feature engineering
- [ ] 1-2 models trained
- [ ] Moderate metrics (F1 0.55-0.65, AUC-ROC 0.60-0.70)
- [ ] Train/test split present
- [ ] Limited validation

**Poor (0-13 points)**
- [ ] Minimal feature engineering
- [ ] Single model or no comparison
- [ ] Poor metrics (F1 < 0.55, AUC-ROC < 0.60)
- [ ] No proper train/test split
- [ ] Evidence of data leakage

---

### 3. API Implementation (20 points)

**Excellent (18-20 points)**
- [ ] Both endpoints (`/predict`, `/explain`) work perfectly
- [ ] Proper request/response schemas (Pydantic)
- [ ] Comprehensive error handling
- [ ] Input validation with meaningful error messages
- [ ] Explanation endpoint provides useful insights
- [ ] API documentation (docstrings)
- [ ] Can handle edge cases

**Good (14-17 points)**
- [ ] Both endpoints implemented and mostly working
- [ ] Basic request/response validation
- [ ] Some error handling
- [ ] Explanation endpoint present
- [ ] Mostly functional

**Adequate (10-13 points)**
- [ ] Both endpoints present but have issues
- [ ] Minimal validation
- [ ] Basic error handling
- [ ] Explanation endpoint partially implemented
- [ ] Requires some debugging to run

**Poor (0-9 points)**
- [ ] Endpoints missing or broken
- [ ] No validation
- [ ] No error handling
- [ ] API doesn't run

---

### 4. Code Quality (15 points)

**Excellent (13-15 points)**
- [ ] Clean, readable code following PEP 8
- [ ] Well-organized functions and modules
- [ ] Descriptive variable names
- [ ] Helpful comments explaining logic
- [ ] No code duplication
- [ ] Proper use of libraries
- [ ] Error handling throughout

**Good (10-12 points)**
- [ ] Generally clean code
- [ ] Mostly follows style guidelines
- [ ] Organized structure
- [ ] Adequate comments
- [ ] Minimal duplication

**Adequate (7-9 points)**
- [ ] Code is functional but messy
- [ ] Some style issues
- [ ] Weak organization
- [ ] Sparse comments
- [ ] Some duplication

**Poor (0-6 points)**
- [ ] Difficult to read code
- [ ] Poor organization
- [ ] No comments
- [ ] Significant duplication

---

### 5. Documentation (10 points)

**Excellent (9-10 points)**
- [ ] Comprehensive README with all sections
- [ ] Clear setup instructions
- [ ] API documentation with examples
- [ ] Explains approach and methodology
- [ ] Lists limitations and future work
- [ ] Professional formatting
- [ ] analysis.md is thorough

**Good (7-8 points)**
- [ ] README covers main points
- [ ] Setup instructions clear
- [ ] Basic API documentation
- [ ] Approach explained
- [ ] Some limitations mentioned

**Adequate (5-6 points)**
- [ ] README exists but incomplete
- [ ] Setup instructions present
- [ ] Minimal API documentation
- [ ] Limited explanation

**Poor (0-4 points)**
- [ ] Missing or minimal README
- [ ] No setup instructions
- [ ] No API documentation

---

### 6. Git Practices (10 points)

**Excellent (9-10 points)**
- [ ] 15+ meaningful commits
- [ ] Clear, descriptive commit messages
- [ ] Logical progression showing development
- [ ] Proper `.gitignore` configuration
- [ ] No sensitive data committed
- [ ] Clean commit history

**Good (7-8 points)**
- [ ] 10-14 commits
- [ ] Generally good messages
- [ ] Clear progression
- [ ] Proper `.gitignore`

**Adequate (5-6 points)**
- [ ] 5-9 commits
- [ ] Some vague commit messages
- [ ] Basic `.gitignore`

**Poor (0-4 points)**
- [ ] < 5 commits (looks AI-generated)
- [ ] Unclear messages
- [ ] Missing `.gitignore`
- [ ] Data files committed

---

## 🎯 Performance Expectations

### Model Metrics Baseline

| Metric | Minimum | Target | Excellent |
|--------|---------|--------|-----------|
| Accuracy | 0.60 | 0.70 | 0.75+ |
| Precision | 0.50 | 0.65 | 0.75+ |
| Recall | 0.50 | 0.65 | 0.75+ |
| F1 Score | 0.55 | 0.70 | 0.75+ |
| AUC-ROC | 0.60 | 0.75 | 0.80+ |

---

## 🚩 Red Flags (Automatic Rejection)

Any of these will result in **REJECTION**:

- ❌ No git commit history (appears AI-generated)
- ❌ README is missing
- ❌ Code doesn't run (Python errors)
- ❌ API endpoints don't work
- ❌ train.py fails to execute
- ❌ model.pkl not found
- ❌ Data files committed to repo
- ❌ .env or API keys committed
- ❌ No analysis.md
- ❌ Cannot explain model choices
- ❌ Evidence of direct copy-paste (ChatGPT-style code)
- ❌ Hardcoded predictions in API

---

## 📋 Scoring Checklist (For Reviewers)

```
Candidate: ________________
Date: ________________

SUBMISSION QUALITY
[ ] Repository structure is correct
[ ] README is complete and clear
[ ] analysis.md exists and is thorough
[ ] Code runs without errors
[ ] All required files present

EDA & ANALYSIS (____/20)
[ ] Data exploration comprehensive
[ ] Patterns and segments identified
[ ] Visualizations helpful
[ ] Insights are actionable
[ ] Analysis documented clearly

MODEL QUALITY (____/25)
[ ] Feature engineering thoughtful
[ ] Multiple models tested
[ ] Model selection justified
[ ] Metrics are strong
[ ] No data leakage evident
[ ] Proper train/test split
[ ] Feature importance explained

API IMPLEMENTATION (____/20)
[ ] /predict endpoint works
[ ] /explain endpoint works
[ ] Proper validation
[ ] Error handling present
[ ] API runs without modification
[ ] Documentation clear

CODE QUALITY (____/15)
[ ] Code is clean and readable
[ ] Functions well-organized
[ ] Comments helpful
[ ] PEP 8 compliance
[ ] No significant duplication

DOCUMENTATION (____/10)
[ ] README comprehensive
[ ] Setup instructions clear
[ ] API docs complete
[ ] Limitations explained

GIT PRACTICES (____/10)
[ ] 10+ meaningful commits
[ ] Clear commit messages
[ ] Logical progression
[ ] .gitignore properly configured

INTERVIEW READINESS
[ ] Can explain model choice [ ] Can discuss trade-offs
[ ] Understands feature importance
[ ] Aware of limitations
[ ] Proposes improvements

TOTAL SCORE: ____/100

COMMENTS:
_________________________________
_________________________________
_________________________________
```

---

## 📊 Score Interpretation

| Score | Decision | Next Step |
|-------|----------|-----------|
| 85+ | Strong | Advance to final round interview |
| 75-84 | Good | Phone screen to confirm capabilities |
| 65-74 | Borderline | Technical discussion required |
| 55-64 | Weak | Consider but with reservations |
| <55 | Reject | Do not advance |

---

## 🎯 Interview Questions (Based on Score)

### If Score > 85 (All-star)
1. Walk us through your feature engineering process
2. Why did you choose this specific model?
3. How would you handle a 10x increase in data volume?
4. What would you change if you had 2 weeks instead of 48 hours?

### If Score 75-84 (Strong)
1. Explain your approach to the problem
2. What was the biggest challenge?
3. How did you validate your model?
4. What limitations exist?

### If Score 65-74 (Decent)
1. Walk us through your model training
2. How did you handle missing values?
3. Why this model over others?
4. Can you explain feature X?

### If Score <65 (Weak)
1. Can you explain your code to me?
2. How would you approach this differently?
3. What's a limitation you noticed?
4. Do you have experience with similar problems?

---

## 📞 Final Hiring Decision

Combine score with:
- Technical Interview Performance
- Communication clarity
- Problem-solving approach
- Fit with team culture
- Relevant experience

---

**Last Updated**: June 2024
**Version**: 1.0

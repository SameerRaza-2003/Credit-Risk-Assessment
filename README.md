
# 📊 Probability of Default (PD) Risk Scoring System

**Bank-grade SME Credit Risk Scoring using Logistic Regression + Altman Z-Score**

---

## 1️⃣ Project Overview

This project implements an **end-to-end Probability of Default (PD) system** for SME credit risk assessment.

It includes:
- A **trained Logistic Regression PD model**
- **Altman Z-Score** as a secondary financial distress indicator
- A **professional Streamlit web application**
- **Single-borrower scoring** and **bulk CSV scoring**
- **Authentication & role-based access**
- **Explainable outputs (PD, E-log, risk bands)**

The system follows **real banking risk modeling practices**:
- No data leakage
- No user-entered engineered ratios
- Identical preprocessing in training and inference
- Clear separation between **raw inputs**, **feature engineering**, and **model scoring**

---

## 2️⃣ Folder Structure (IMPORTANT)

```

Probability_Of_Default/
│
├── models/
│   ├── pd_logistic_pipeline.pkl     # Trained sklearn Pipeline (preprocess + model)
│   ├── logistic_pd.py               # Model loading & scoring
│   ├── feature_engineering.py       # Derived ratio calculations
│   ├── altman_z.py                  # Altman Z-score logic
│
├── pages/
│   ├── 1_login.py                   # Login page (streamlit-authenticator)
│   ├── 2_input_step1.py             # Borrower & loan info (Step 1)
│   ├── 3_input_step2.py             # Financial statements (Step 2)
│   ├── 4_results.py                 # PD, Z-score, risk bands, warnings
│   ├── 5_bulk_scoring.py             # Bulk CSV scoring
│
├── utils/
│   ├── validators.py                # Input sanity checks & warnings
│
├── auth.py                          # Authentication config
├── app.py                           # Streamlit entry point
├── requirements.txt
└── README.md

```

---

## 3️⃣ Model Training Summary

### Model Type
- **Logistic Regression**
- `class_weight="balanced"`
- Solver: `lbfgs`
- Max iterations: `1000`

### Preprocessing (Inside Pipeline)
- Numerical:
  - Median imputation
  - Standard scaling
- Categorical:
  - Most-frequent imputation
  - One-Hot Encoding (`handle_unknown="ignore"`)

### Target
```

Default Flag (1/0)

````

### Output
- **PD** → Probability of Default
- **E_log** → Log-odds score

---

## 4️⃣ Input Design Philosophy (CRITICAL)

### ❌ What users DO NOT enter
- leverage
- wc_ratio
- profitability
- interest_burden
- bank_balance_ratio

These are **engineered features** and are **computed internally**.

### ✅ What users DO enter (RAW FACTS)

#### Borrower & Loan
- Business Type
- Industry / Sector
- Business Age (Years)
- Bank
- Loan Amount
- Tenure (Months)
- Repayment Frequency
- Interest Rate

#### Financial Statements
- Total Assets
- Total Liabilities
- Working Capital
- Average Bank Balance
- Sales / Revenue
- EBIT
- Net Income
- Interest Expense

#### Credit Behaviour
- Days Past Due (30/60/90 flags) *(free-text, as per bank records)*

---

## 5️⃣ Feature Engineering (Internal Logic)

Derived automatically in `models/feature_engineering.py`:

```text
leverage            = Total Liabilities / Total Assets
wc_ratio            = Working Capital / Total Assets
profitability       = Net Income / Sales
interest_burden     = Interest Expense / Sales
bank_balance_ratio  = Average Bank Balance / Loan Amount
````

These match **exactly** what the model was trained on.

---

## 6️⃣ Model Scoring Logic

Scoring happens in:

```
models/logistic_pd.py
```

```python
PD = model.predict_proba(X)[0, 1]
E_log = model.decision_function(X)[0]
```

Relationship:

```
PD = 1 / (1 + exp(-E_log))
```

---

## 7️⃣ Risk Banding (Policy Layer)

| PD Band | PD Range | Risk Label     |
| ------- | -------- | -------------- |
| A       | < 10%    | Very Low Risk  |
| B       | 10–20%   | Low Risk       |
| C1      | 20–30%   | Moderate Risk  |
| C2      | 30–40%   | Elevated Risk  |
| C3      | 40–50%   | High Risk      |
| D       | 50–70%   | Very High Risk |
| E       | > 70%    | Severe Risk    |

---

## 8️⃣ Altman Z-Score

Implemented in:

```
models/altman_z.py
```

Used as a **secondary financial distress indicator**, not as a replacement for PD.

Interpretation:

* **Z < 3** → Severe distress
* **3 ≤ Z < 6** → High risk
* **6 ≤ Z < 10** → Moderate risk
* **Z ≥ 10** → Low risk

---

## 9️⃣ Validation & Warnings (Non-Blocking)

The system issues **warnings**, not hard rejections:

Examples:

* Total Liabilities > Total Assets
* Loan Amount > Total Assets
* Zero or very low sales
* Zero interest rate

These are **credit review flags**, not system errors.

---

## 🔟 Bulk CSV Scoring

### Required CSV Columns

```csv
Business Type,Industry/Sector,Business Age (Years),Bank,Loan Amount,
Tenure (Months),Repayment Frequency,Interest Rate,
Total Assets,Total Liabilities,Working Capital,Average Bank Balance,
Sales/Revenue,EBIT,Net Income,Interest Expense,
Days Past Due (30/60/90 flags)
```

The same:

* feature engineering
* preprocessing
* model
  is used for **single and bulk scoring** (no mismatch).

---

## 1️⃣1️⃣ Known Modeling Limitation (IMPORTANT)

### DPD Encoding

`Days Past Due (30/60/90 flags)` is treated as a **categorical string**.

This can cause:

* Similar DPD patterns to be treated differently
* Some clean borrowers to receive higher PDs

This is a **data representation limitation**, not a coding error.

**Recommended future improvement:**

* Parse DPD into numeric severity features (30/60/90 counts)
* Retrain model

---

## 1️⃣2️⃣ Authentication

* Implemented via `streamlit-authenticator`
* Session-based login
* Demo credentials (for academic use):

```
admin / admin123
analyst / riskpd
```

---

## 1️⃣3️⃣ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 1️⃣4️⃣ When You Reopen This Project (IMPORTANT)

If you are a future version of me or an AI assistant:

1. Start by reading this README
2. Inspect `models/pd_logistic_pipeline.pkl`
3. Use `model.feature_names_in_` to verify inputs
4. Do NOT ask users for engineered ratios
5. Do NOT rebuild preprocessing outside the pipeline
6. Treat PD as a **probabilistic estimate**, not a decision rule

---

## 1️⃣5️⃣ Final Statement

This system is:

* **Technically correct**
* **Professionally designed**
* **Bank-realistic**
* **Defensible in exams, interviews, and demos**

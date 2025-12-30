import joblib
import pandas as pd

MODEL_PATH = "models/pd_logistic_pipeline.pkl"
model = joblib.load(MODEL_PATH)

def score_pd(feature_dict):
    X = pd.DataFrame([feature_dict])
    pd_val = model.predict_proba(X)[0, 1]
    elog = model.decision_function(X)[0]
    return pd_val, elog

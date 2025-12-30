def compute_pd(model, X):
    pd = model.predict_proba(X)[0][1]
    elog = model.decision_function(X)[0]
    return pd, elog

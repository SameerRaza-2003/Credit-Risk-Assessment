def build_model_input(raw):
    """
    Takes raw user inputs and builds full feature vector
    exactly as expected by the trained model
    """

    engineered = {}

    engineered["leverage"] = raw["Total Liabilities"] / max(raw["Total Assets"], 1)
    engineered["wc_ratio"] = raw["Working Capital"] / max(raw["Total Assets"], 1)
    engineered["profitability"] = raw["Net Income"] / max(raw["Sales/Revenue"], 1)
    engineered["interest_burden"] = raw["Interest Expense"] / max(raw["Sales/Revenue"], 1)
    engineered["bank_balance_ratio"] = raw["Average Bank Balance"] / max(raw["Loan Amount"], 1)

    return {**raw, **engineered}

def validate_inputs(raw):
    warnings = []

    if raw["Total Assets"] < raw["Total Liabilities"]:
        warnings.append("Total Liabilities exceed Total Assets")

    if raw["Sales/Revenue"] == 0:
        warnings.append("Sales are zero — profitability ratios may be unstable")

    if raw["Loan Amount"] > raw["Total Assets"]:
        warnings.append("Loan Amount exceeds Total Assets")

    if raw["Interest Rate"] == 0:
        warnings.append("Interest Rate is zero")

    return warnings

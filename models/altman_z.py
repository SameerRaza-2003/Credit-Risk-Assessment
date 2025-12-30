def compute_altman_z(fin):
    ta = fin["Total Assets"]

    z = (
        6.56 * (fin["Working Capital"] / ta) +
        3.26 * (fin["Net Income"] / ta) +
        6.72 * (fin["EBIT"] / ta) +
        1.05 * (fin["Sales/Revenue"] / ta)
    )
    return z

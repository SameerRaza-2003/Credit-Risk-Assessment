def compute_altman_z(fin):
    z_wc_ta = fin["Working Capital"] / fin["Total Assets"]
    z_ni_ta = fin["Net Income"] / fin["Total Assets"]
    z_ebit_ta = fin["EBIT"] / fin["Total Assets"]
    z_sales_ta = fin["Sales/Revenue"] / fin["Total Assets"]

    z = (
        6.56 * z_wc_ta +
        3.26 * z_ni_ta +
        6.72 * z_ebit_ta +
        1.05 * z_sales_ta
    )
    return z

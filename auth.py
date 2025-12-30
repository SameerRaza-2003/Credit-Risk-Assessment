import streamlit_authenticator as stauth

def get_authenticator():
    credentials = {
        "usernames": {
            "admin": {
                "name": "Admin",
                "password": "admin123"
            },
            "analyst": {
                "name": "Risk Analyst",
                "password": "riskpd"
            }
        }
    }

    return stauth.Authenticate(
        credentials=credentials,
        cookie_name="pd_dashboard",
        key="secure_key_123",
        cookie_expiry_days=1
    )

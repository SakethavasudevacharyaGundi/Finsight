import base64
import io
import pandas as pd
import requests


def download_daily_upi(
    month,
    year
):

    response = requests.get(
        "https://www.npci.org.in/api/products-statistics-files",
        params={
            "product_name": "upi",
            "tab_name": "upi-daily-statistics",
            "month": month,
            "year": year,
            "excel_type": "daily",
            "locale": "en"
        }
    )

    payload = response.json()

    file_b64 = payload["data"]["file"]

    excel_bytes = base64.b64decode(
        file_b64
    )

    return pd.read_excel(
        io.BytesIO(excel_bytes)
    )
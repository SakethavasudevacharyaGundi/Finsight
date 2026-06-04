import base64
import io

import pandas as pd
import requests


def download_monthly_upi(
    month,
    year
):

    response = requests.get(
        ...
    )

    payload = response.json()

    file_b64 = payload["data"]["file"]

    excel_bytes = base64.b64decode(
        file_b64
    )

    filename = (
        f"{month}_{year}.xlsx"
    )

    with open(
        f"data/raw/upi/upi_monthly_stats/{filename}",
        "wb"
    ) as f:

        f.write(excel_bytes)
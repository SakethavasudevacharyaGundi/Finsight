import os
import requests
from bs4 import BeautifulSoup

PSI_URL = (
    "https://www.rbi.org.in/Scripts/PSIUserView.aspx"
)

DOWNLOAD_DIR = (
    "data/raw/rbi_payment_indicators"
)


def download_new_files():

    response = requests.get(PSI_URL)

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    downloaded_files = []

    for link in soup.find_all("a"):

        href = link.get("href")

        if not href:
            continue

        if ".xlsx" not in href.lower():
            continue
        print(href)

        filename = os.path.basename(
            href
        )

        filepath = os.path.join(
            DOWNLOAD_DIR,
            filename
        )
        print(
            "Exists:",
            os.path.exists(filepath),
            filename
        )

        if os.path.exists(filepath):
            continue

        print(
            f"Downloading {filename}"
        )

        file_response = requests.get(
            href
        )

        file_response.raise_for_status()

        with open(
            filepath,
            "wb"
        ) as f:

            f.write(
                file_response.content
            )

        downloaded_files.append(
            filepath
        )

    return downloaded_files
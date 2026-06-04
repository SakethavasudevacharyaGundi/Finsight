from src.loaders.npci_upi_monthly_loader import (
    download_monthly_upi
)

df = download_monthly_upi(
    month="May",
    year=2026
)

print(df.head())
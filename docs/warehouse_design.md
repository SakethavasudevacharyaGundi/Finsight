# RAW
RAW.UPI_MONTHLY_STATS
RAW.RBI_PAYMENT_INDICATORS
RAW.RBI_DPI
# Purpose
Store source data exactly as received.
Minimal transformation.
Historical source of truth.

# Documnet
STAGING.STG_UPI_MONTHLY_STATS
STAGING.STG_RBI_PAYMENT_INDICATORS
STAGING.STG_RBI_DPI

# Purpose
Standardize column names
Cast data types
Handle missing values
Apply basic cleaning rules

# MARTS

MoM Growth
YoY Growth
Volume Growth
Value Growth
Bank Adoption Growth

# MARTS PAYMENT METHOD COMPARISION
UPI vs IMPS
UPI vs NEFT
UPI vs RTGS
Cards vs UPI    
# MARTS DIGITAL PAYMENT TREND
Total Digital Transactions
Transaction Value Trends
Infrastructure Growth
# MARTS DPI ANALYSIS

DPI Trend
DPI Growth Rate
DPI vs UPI Growth

# PIPELINE FLOW

NPCI UPI Statistics
          │
          ▼
RAW.UPI_MONTHLY_STATS
          │
          ▼
STAGING.STG_UPI_MONTHLY_STATS
          │
          ▼
MARTS.UPI_GROWTH_ANALYSIS


RBI Payment Indicators
          │
          ▼
RAW.RBI_PAYMENT_INDICATORS
          │
          ▼
STAGING.STG_RBI_PAYMENT_INDICATORS
          │
          ▼
MARTS.PAYMENT_METHOD_COMPARISON
          │
          ▼
MARTS.DIGITAL_PAYMENT_TRENDS


RBI DPI
          │
          ▼
RAW.RBI_DPI
          │
          ▼
STAGING.STG_RBI_DPI
          │
          ▼
MARTS.DPI_ANALYSIS
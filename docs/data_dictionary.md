# FinSight Data Dictionary

## Overview

FinSight uses data from NPCI and RBI to analyze India's digital payments ecosystem, UPI adoption, payment infrastructure growth, and overall digital payment maturity.

---

# Source 1: NPCI UPI Monthly Statistics

## Source Details

| Attribute         | Value                                         |
| ----------------- | --------------------------------------------- |
| Source Name       | NPCI UPI Monthly Statistics                   |
| Owner             | National Payments Corporation of India (NPCI) |
| Refresh Frequency | Monthly                                       |
| Format            | Excel / CSV                                   |
| Raw Table         | RAW.UPI_MONTHLY_STATS                         |

## Raw Columns

| Source Column            | Standardized Name | Data Type |
| ------------------------ | ----------------- | --------- |
| Month                    | month             | DATE      |
| No. of Banks live on UPI | banks_live        | INTEGER   |
| Volume (In Mn.)          | volume_mn         | DECIMAL   |
| Value (In Cr.)           | value_cr          | DECIMAL   |

## Business Description

Contains monthly UPI transaction statistics including participating banks, transaction volume, and transaction value since UPI launch.

---

# Source 2: RBI Payment System Indicators

## Source Details

| Attribute         | Value                         |
| ----------------- | ----------------------------- |
| Source Name       | RBI Payment System Indicators |
| Owner             | Reserve Bank of India (RBI)   |
| Refresh Frequency | Monthly                       |
| Format            | Excel                         |
| Raw Table         | RAW.RBI_PAYMENT_INDICATORS    |

## Key Metrics

### Credit Transfers

* RTGS
* NEFT
* IMPS
* UPI

### Card Payments

* Credit Cards
* Debit Cards

### Prepaid Payment Instruments

* Wallets
* PPI Cards

### Infrastructure Metrics

* ATMs
* Micro ATMs
* PoS Terminals
* Bharat QR
* UPI QR

## Measurement Types

Each payment mode may contain:

* Transaction Volume
* Transaction Value
* Monthly Metrics
* Financial Year Metrics

## Business Description

Provides comprehensive statistics on India's payment ecosystem including transaction volume, transaction value, and payment infrastructure indicators.

---

# Source 3: RBI Digital Payments Index (DPI)

## Source Details

| Attribute         | Value                       |
| ----------------- | --------------------------- |
| Source Name       | RBI Digital Payments Index  |
| Owner             | Reserve Bank of India (RBI) |
| Refresh Frequency | Semi-Annual                 |
| Format            | CSV                         |
| Raw Table         | RAW.RBI_DPI                 |

## Raw Columns

| Source Column                     | Standardized Name | Data Type |
| --------------------------------- | ----------------- | --------- |
| Period                            | period            | DATE      |
| RBI – Digital Payment Index (DPI) | dpi_value         | DECIMAL   |

## Business Description

Measures the overall level of digital payment adoption and maturity in India. The index combines payment infrastructure, payment performance, and payment adoption indicators.

---

# Data Architecture

## RAW Layer

* RAW.UPI_MONTHLY_STATS
* RAW.RBI_PAYMENT_INDICATORS
* RAW.RBI_DPI

## STAGING Layer

* STAGING.STG_UPI_MONTHLY_STATS
* STAGING.STG_RBI_PAYMENT_INDICATORS
* STAGING.STG_RBI_DPI

## MARTS Layer

* MARTS.UPI_GROWTH_ANALYSIS
* MARTS.PAYMENT_METHOD_COMPARISON
* MARTS.DIGITAL_PAYMENT_TRENDS
* MARTS.DPI_ANALYSIS

---

# Data Refresh Schedule

| Dataset                    | Frequency   |
| -------------------------- | ----------- |
| UPI Monthly Statistics     | Monthly     |
| RBI Payment Indicators     | Monthly     |
| RBI Digital Payments Index | Semi-Annual |

---

# Data Quality Requirements

* No duplicate reporting periods
* No null values in primary metrics
* Numeric fields must be non-negative
* Reporting periods must be unique
* Source files must be validated before loading

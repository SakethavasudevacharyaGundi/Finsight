# RBI Payment Indicator Parser

Source:
RBI Payment System Indicators

Sections:

1. Payment Transactions
   -> RAW.RBI_PAYMENT_TRANSACTIONS
2. Payment Channels
   -> RAW.RBI_PAYMENT_CHANNELS
3. Payment Infrastructure
   -> RAW.RBI_PAYMENT_INFRASTRUCTURE
4. Payment Frauds
   -> RAW.RBI_PAYMENT_FRAUDS

Transformation Strategy:

Wide Excel Format
        ↓
Dynamic Header Extraction
        ↓
Period Detection
        ↓
Unpivot
        ↓
Long Format
        ↓
Snowflake RAW Tables

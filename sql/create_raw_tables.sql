USE DATABASE FINSIGHT_DB;
USE SCHEMA RAW;

-- =====================================================
-- UPI MONTHLY STATISTICS
-- =====================================================

CREATE OR REPLACE TABLE UPI_MONTHLY_STATS (
    month DATE,
    banks_live INTEGER,
    volume_mn NUMBER(18,2),
    value_cr NUMBER(18,2),
    source_file VARCHAR,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =====================================================
-- RBI DIGITAL PAYMENTS INDEX
-- =====================================================

CREATE OR REPLACE TABLE RBI_DPI (
    period DATE,
    dpi_value NUMBER(10,2),
    source_file VARCHAR,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =====================================================
-- RBI PAYMENT TRANSACTIONS
-- =====================================================

CREATE OR REPLACE TABLE RBI_PAYMENT_TRANSACTIONS (
    report_period DATE,
    payment_method VARCHAR,
    volume_lakh NUMBER(20,2),
    value_crore NUMBER(20,2),
    source_file VARCHAR,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =====================================================
-- RBI PAYMENT CHANNELS
-- =====================================================

CREATE OR REPLACE TABLE RBI_PAYMENT_CHANNELS (
    report_period DATE,
    channel_name VARCHAR,
    volume_lakh NUMBER(20,2),
    value_crore NUMBER(20,2),
    source_file VARCHAR,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =====================================================
-- RBI PAYMENT INFRASTRUCTURE
-- =====================================================

CREATE OR REPLACE TABLE RBI_PAYMENT_INFRASTRUCTURE (
    report_period DATE,
    infrastructure_type VARCHAR,
    metric_value NUMBER(20,2),
    source_file VARCHAR,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =====================================================
-- RBI PAYMENT FRAUDS
-- =====================================================

CREATE OR REPLACE TABLE RBI_PAYMENT_FRAUDS (
    report_period DATE,
    fraud_volume_lakh NUMBER(20,2),
    fraud_value_crore NUMBER(20,2),
    fraud_ratio NUMBER(20,2),
    fts_bps NUMBER(20,4),
    source_file VARCHAR,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =====================================================
-- LOAD AUDIT TABLE
-- =====================================================

CREATE OR REPLACE TABLE LOAD_AUDIT (
    load_id INTEGER AUTOINCREMENT,
    dataset_name VARCHAR,
    file_name VARCHAR,
    rows_loaded INTEGER,
    load_status VARCHAR,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
# India Digital Payments Analytics Platform

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge\&logo=apacheairflow\&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge\&logo=snowflake\&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge\&logo=dbt\&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge\&logo=tableau\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)

## Overview

An end-to-end Data Engineering and Analytics platform that automates the collection, transformation, warehousing, and visualization of India's digital payments ecosystem using RBI and NPCI data.

The platform tracks UPI adoption, digital payment growth, payment rail evolution, bank participation, fraud trends, and digital payment maturity through a fully automated analytics pipeline.

---

## Dashboard Preview

Add screenshots after publishing:


images/dashboard.png
images/airflow_dag.png

---

## Key Metrics

| Metric                  |                      Value |
| ----------------------- | -------------------------: |
| Historical Coverage     |        Apr 2016 – Apr 2026 |
| Data Coverage           |                  10+ Years |
| Total Records Processed |                     6,000+ |
| Maximum Banks on UPI    |                        713 |

---

## Architecture

```text
RBI / NPCI
    ↓
Python ETL
    ↓
Apache Airflow
    ↓
Snowflake
    ↓
dbt
    ↓
Tableau
```

---

## Data Pipeline

### ETL Pipeline

The platform automates data collection from RBI and NPCI through Python-based ingestion pipelines orchestrated by Apache Airflow.

#### RBI Pipeline

1. Discover newly published RBI Payment System Indicator files
2. Download monthly XLSX datasets
3. Validate file structure and schema
4. Transform source files into tabular datasets
5. Load curated data into Snowflake RAW tables

#### NPCI UPI Pipeline

1. Extract UPI Monthly Statistics
2. Extract UPI Daily Statistics
3. Validate incoming datasets
4. Deduplicate records
5. Load data into Snowflake RAW tables

#### Airflow Orchestration

Automated using dedicated DAGs:

```text
RBI Payment Indicators DAG
UPI Monthly Statistics DAG
UPI Daily Statistics DAG
```

Features:

* Scheduled execution
* Retry handling
* Dependency management
* Pipeline monitoring

---

### ELT Pipeline

After ingestion, transformations are performed inside Snowflake using dbt.

```text
RAW
  ↓
STAGING
  ↓
BUSINESS MARTS
  ↓
TABLEAU
```

#### Staging Models

```text
stg_upi_daily
stg_upi_monthly
stg_rbi_payment_transactions
stg_rbi_payment_channels
stg_rbi_payment_infrastructure
stg_rbi_payment_frauds
stg_rbi_dpi
```

Responsibilities:

* Data standardization
* Type casting
* Deduplication
* Business key generation
* Data quality validation

#### Business Marts

```text
fact_upi_monthly
dim_date

mart_upi_growth
mart_payment_mix
mart_fraud_trends
mart_digital_payment
mart_upi_anomalies
```

Business capabilities:

* Month-over-month growth analysis
* Year-over-year growth analysis
* Payment rail market share analysis
* Fraud trend analysis
* Digital Payments Index analysis
* Statistical anomaly detection

---

## Tech Stack

| Layer                 | Technology               |
| --------------------- | ------------------------ |
| Data Ingestion        | Python, Pandas, Requests |
| Orchestration         | Apache Airflow           |
| Data Warehouse        | Snowflake                |
| Analytics Engineering | dbt, SQL                 |
| Visualization         | Tableau                  |
| Infrastructure        | Docker                   |

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Start Airflow

```bash
docker-compose up -d
```

Access Airflow:

```text
http://localhost:8080
```

### 3. Configure Snowflake

Create the warehouse objects:

```sql
CREATE DATABASE FINSIGHT_DB;

CREATE SCHEMA RAW;
CREATE SCHEMA STAGING;
```

Configure credentials in:

```text
.env
profiles.yml
```

### 4. Install dbt Dependencies

```bash
cd finsight_dbt

dbt deps
```

### 5. Build Models

```bash
dbt run
```

### 6. Run Data Quality Tests

```bash
dbt test
```

### 7. Launch Dashboard

Connect Tableau to Snowflake and use the curated MART models for reporting.

---

## Data Quality Framework

Implemented using dbt tests:

* Unique Tests
* Not Null Tests
* Source Validation
* Duplicate Detection

All production tests pass successfully.

---

## Dashboard Features

### UPI Transaction Growth

Tracks UPI adoption from launch to nationwide scale.

### UPI Network Expansion

Analyzes the relationship between participating banks and transaction growth.

### Digital Payments Index vs UPI Adoption

Compares India's digital payment maturity with UPI adoption trends.

### Payment Rail Evolution

Visualizes market share changes across UPI, NEFT, IMPS, RTGS and other payment systems.

---

## Repository Structure

```text
.
├── airflow/
│   └── dags/
│
├── src/
│   ├── ingestion/
│   ├── loaders/
│   └── utils/
│
├── finsight_dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
│
├── docker-compose.yml
└── README.md
```

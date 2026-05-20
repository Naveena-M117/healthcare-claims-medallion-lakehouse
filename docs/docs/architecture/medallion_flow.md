# Medallion Architecture Flow

## Overview

This project implements a Medallion Architecture pipeline for healthcare claims processing using Azure Databricks and Delta Lake.

The architecture follows a layered lakehouse approach:

Landing → Bronze → Silver → Gold

---

# Landing Layer

Raw vendor files are initially received in the landing zone.

## Characteristics

- Immutable raw files
- CSV and Excel ingestion
- Vendor-specific file naming conventions
- Daily batch arrival simulation

Example source:
LexisNexis healthcare claims feed

---

# Bronze Layer

Stores raw ingested data with audit and lineage metadata.

## Features

- Raw schema preservation
- Audit columns
- Source file tracking
- Batch identifiers
- Ingestion timestamps
- Delta Lake storage

---

# Silver Layer

Performs cleansing, standardization, and validation.

## Features

- Null handling
- Duplicate removal
- Invalid record rejection
- Data type standardization
- Business rule enforcement

---

# Reject Layer

Stores invalid or quarantined records.

## Examples

- Invalid claim dates
- Missing provider IDs
- Negative billing amounts
- Null claim IDs

---

# Gold Layer

Provides business-ready analytics datasets.

## KPIs

- Claims by month
- Provider performance
- Claim approval rates
- Payment trends
- Denial analysis

---

# Technologies Used

- Azure ADLS Gen2
- Azure Databricks
- PySpark
- Delta Lake
- Unity Catalog
- GitHub

---

# Enterprise Concepts Demonstrated

- Medallion Architecture
- Incremental processing
- Schema evolution
- Auditability
- Data lineage
- Retry handling
- Monitoring concepts
- Cloud-native lakehouse design

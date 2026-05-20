# Project Overview

This project demonstrates an enterprise-style healthcare claims Medallion Architecture pipeline built using Azure Databricks, ADLS Gen2, Delta Lake, and PySpark.

The pipeline simulates ingestion of healthcare claims data from a third-party vendor source into a cloud-native lakehouse platform.

## Objectives

- Ingest raw healthcare claims files
- Build Bronze, Silver, and Gold layers
- Implement audit and traceability
- Handle bad records through reject processing
- Demonstrate schema evolution
- Support incremental processing
- Simulate enterprise ETL workflows

## Architecture

Landing → Bronze → Silver → Gold → Reporting

## Domain

Healthcare Claims Processing

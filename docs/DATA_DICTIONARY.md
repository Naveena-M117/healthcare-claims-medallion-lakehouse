# Data Dictionary

## Claims Dataset

| Column Name | Data Type | Description |
|---|---|---|
| claim_id | string | Unique claim identifier |
| member_id | string | Unique patient/member identifier |
| provider_id | string | Healthcare provider identifier |
| claim_date | date | Date of claim submission |
| procedure_code | string | Medical procedure code |
| diagnosis_code | string | Diagnosis classification code |
| billed_amount | decimal | Amount billed by provider |
| paid_amount | decimal | Amount paid after adjudication |
| claim_status | string | Claim processing status |
| source_system | string | Vendor/source system name |

---

## Audit Columns

| Column Name | Description |
|---|---|
| ingestion_timestamp | Timestamp when record entered Bronze |
| source_file_name | Raw source file name |
| batch_id | Unique ingestion batch identifier |
| load_date | Pipeline load date |
| ingested_by | Notebook or process identifier |
| record_hash | Hash value for duplicate tracking |

---

## Data Quality Rules

| Rule | Description |
|---|---|
| claim_id cannot be null | Mandatory identifier |
| billed_amount >= 0 | Negative billing invalid |
| paid_amount >= 0 | Negative payment invalid |
| claim_date valid format | Invalid dates rejected |
| provider_id required | Missing provider rejected |

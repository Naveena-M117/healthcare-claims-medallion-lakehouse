# Databricks notebook source
from pyspark.sql import functions as F

# COMMAND ----------

bronze_path = "/Volumes/workspace/healthcare_claims/vol_claims_bronze/"
silver_path = "/Volumes/workspace/healthcare_claims/vol_claims_silver/claims_silver_delta"
reject_path = "/Volumes/workspace/healthcare_claims/vol_claims_reject/claims_reject_delta"
gold_path = "/Volumes/workspace/healthcare_claims/vol_claims_gold"
audit_path = "/Volumes/workspace/healthcare_claims/vol_claims_gold/audit_log"

# COMMAND ----------

bronze_df = spark.read.format("delta").load(bronze_path)
silver_df = spark.read.format("delta").load(silver_path)
reject_df = spark.read.format("delta").load(reject_path)

# COMMAND ----------

audit_df = spark.createDataFrame([
    (
        "BATCH_20260601_070001",
        "lexisnexis_medical_claims_tx_20260601_070001_batch02.csv",
        bronze_df.count(),
        silver_df.count(),
        reject_df.count(),
        "SUCCESS"
    )
], ["batch_id", "source_file_name", "bronze_count", "silver_count", "reject_count", "pipeline_status"])

# COMMAND ----------

audit_df = audit_df.withColumn("audit_timestamp", F.current_timestamp())
display(audit_df)

# COMMAND ----------

(
    audit_df.write
    .format("delta")
    .mode("overwrite")
    .save(audit_path)
)

# COMMAND ----------

display(spark.read.format("delta").load(audit_path))

# COMMAND ----------

display(audit_df)

# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# COMMAND ----------

source_path = "/Volumes/workspace/healthcare_claims/vol_claims_raw_landing/lexisnexis_medical_claims_tx_20260601_070001_batch02.csv"

# COMMAND ----------

df_raw = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(source_path)

# COMMAND ----------

df_bronze = (
    df_raw
    .withColumn("ingestion_timestamp", F.current_timestamp())
    .withColumn("source_file_name", F.lit("multi_file_ingestion"))
    .withColumn("batch_id", F.date_format(F.current_timestamp(), "yyyyMMddHHmmss"))
    .withColumn("load_date", F.current_date())
    .withColumn("ingested_by", F.lit("NB_Claims_Bronze_Ingestion"))
    .withColumn("record_hash", F.sha2(F.concat_ws("||", *df_raw.columns), 256))
)

# COMMAND ----------

bronze_path = "/Volumes/workspace/healthcare_claims/vol_claims_bronze/"
dbutils.fs.rm(bronze_path, True)

# COMMAND ----------

display(df_bronze)

# COMMAND ----------

(
    df_bronze.write
    .format("delta")
    .mode("overwrite")
    .save(bronze_path)
)

# COMMAND ----------

df_check = spark.read.format("delta").load(bronze_path)
display(df_check)

# COMMAND ----------

display(df_bronze.limit(10))

# COMMAND ----------

df_bronze.count()

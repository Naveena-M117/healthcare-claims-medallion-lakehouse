# Databricks notebook source
from pyspark.sql import functions as F

# COMMAND ----------

bronze_path = "/Volumes/workspace/healthcare_claims/vol_claims_bronze/"
silver_path = "/Volumes/workspace/healthcare_claims/vol_claims_silver/claims_silver_delta"
reject_path = "/Volumes/workspace/healthcare_claims/vol_claims_reject/claims_reject_delta"

# COMMAND ----------

df_bronze = spark.read.format("delta").load(bronze_path)
display(df_bronze)

# COMMAND ----------

# DBTITLE 1,Cell 5
from pyspark.sql import functions as F

df_clean = (
    df_bronze
    .withColumn("claim_id", F.trim(F.col("claim_id")))
    .withColumn("member_id", F.trim(F.col("member_id")))
    .withColumn("provider_name", F.trim(F.col("provider_name")))
    .withColumn("claim_status", F.upper(F.trim(F.col("claim_status"))))
    .withColumn("diagnosis_code", F.upper(F.trim(F.col("diagnosis_code"))))
    .withColumn("procedure_code", F.upper(F.trim(F.col("procedure_code"))))
    .withColumn("state", F.upper(F.trim(F.col("state"))))
    .withColumn("gender", F.upper(F.trim(F.col("gender"))))
    .withColumn("service_date", F.expr("try_to_date(service_date, 'M/d/yyyy')"))
    .withColumn("claim_received_date", F.expr("try_to_date(claim_received_date, 'M/d/yyyy')"))
)

# COMMAND ----------

dq_df = (
    df_clean
    .withColumn("billed_amount", F.col("billed_amount").cast("double"))
    .withColumn("allowed_amount", F.col("allowed_amount").cast("double"))
    .withColumn("paid_amount", F.col("paid_amount").cast("double"))
    .withColumn(
        "reject_reason",
        F.when(F.col("claim_id").isNull(), F.lit("missing_claim_id"))
         .when(F.col("provider_name").isNull(), F.lit("missing_provider_name"))
         .when(F.col("billed_amount").isNull(), F.lit("invalid_billed_amount"))
         .when(F.col("allowed_amount").isNull(), F.lit("invalid_allowed_amount"))
         .when(F.col("paid_amount").isNull(), F.lit("missing_paid_amount"))
         .when(F.col("service_date").isNull(), F.lit("invalid_service_date"))
         .when(F.col("claim_received_date").isNull(), F.lit("invalid_claim_received_date"))
         .when(~F.col("claim_status").isin("PAID", "DENIED", "PENDING", "ADJUSTED"), F.lit("invalid_claim_status"))
         .otherwise(F.lit(None))
    )
)

# COMMAND ----------

df_valid = dq_df.filter(F.col("reject_reason").isNull())
df_reject = dq_df.filter(F.col("reject_reason").isNotNull())

# COMMAND ----------

df_silver = (
    df_valid
    .withColumn("processed_timestamp", F.current_timestamp())
    .withColumn("dq_status", F.lit("VALID"))
)

# COMMAND ----------

display(df_bronze)

# COMMAND ----------

dbutils.fs.rm(silver_path, True)

df_silver.write.format("delta").mode("overwrite").save(silver_path)

# COMMAND ----------

dbutils.fs.rm(reject_path, True)

df_reject.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(reject_path)

# COMMAND ----------

df_silver = (
    df_valid
    .withColumn("processed_timestamp", F.current_timestamp())
    .withColumn("dq_status", F.lit("VALID"))
)

# COMMAND ----------

(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .save(silver_path)
)

# COMMAND ----------

df_reject = (
    df_reject
    .withColumn("claim_received_date", F.col("claim_received_date").cast("string"))
    .withColumn("service_date", F.col("service_date").cast("string"))
)

# COMMAND ----------

dbutils.fs.rm(reject_path, True)

df_reject.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(reject_path)

# COMMAND ----------

display(spark.read.format("delta").load(silver_path))
display(spark.read.format("delta").load(reject_path))

# COMMAND ----------

display(df_silver.limit(10))

# COMMAND ----------

reject_out = spark.read.format("delta").load(reject_path)

display(reject_out)

# COMMAND ----------

display(reject_out.select("claim_id","reject_reason"))
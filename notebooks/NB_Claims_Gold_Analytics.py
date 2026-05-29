# Databricks notebook source
from pyspark.sql import functions as F

# COMMAND ----------

silver_path = "/Volumes/workspace/healthcare_claims/vol_claims_silver/claims_silver_delta"
gold_path = "/Volumes/workspace/healthcare_claims/vol_claims_gold"

# COMMAND ----------

df_silver = spark.read.format("delta").load(silver_path)
display(df_silver)

# COMMAND ----------

claims_monthly = (
    df_silver
    .withColumn("claim_month", F.date_format(F.col("service_date"), "yyyy-MM"))
    .groupBy("claim_month")
    .agg(
        F.count("*").alias("total_claims"),
        F.sum("billed_amount").alias("total_billed_amount"),
        F.sum("paid_amount").alias("total_paid_amount")
    )
    .orderBy("claim_month")
)
display(claims_monthly)

# COMMAND ----------

provider_summary = (
    df_silver
    .groupBy("provider_name")
    .agg(
        F.count("*").alias("total_claims"),
        F.sum("paid_amount").alias("total_paid_amount"),
        F.avg("paid_amount").alias("avg_paid_amount")
    )
    .orderBy(F.desc("total_paid_amount"))
)
display(provider_summary)

# COMMAND ----------

status_summary = (
    df_silver
    .groupBy("claim_status")
    .agg(F.count("*").alias("claim_count"))
    .orderBy("claim_status")
)
display(status_summary)

# COMMAND ----------

claims_monthly.write.format("delta").mode("overwrite").save(f"{gold_path}/claims_monthly_summary")
provider_summary.write.format("delta").mode("overwrite").save(f"{gold_path}/provider_summary")
status_summary.write.format("delta").mode("overwrite").save(f"{gold_path}/status_summary")

# COMMAND ----------

display(spark.read.format("delta").load(f"{gold_path}/claims_monthly_summary"))
display(spark.read.format("delta").load(f"{gold_path}/provider_summary"))
display(spark.read.format("delta").load(f"{gold_path}/status_summary"))

# COMMAND ----------

state_summary = (
    df_silver
    .groupBy("state")
    .agg(
        F.count("*").alias("total_claims"),
        F.sum("paid_amount").alias("total_paid_amount")
    )
    .orderBy("state")
)

display(state_summary)

# COMMAND ----------

total_paid = df_silver.agg(
    F.sum("paid_amount").alias("total_paid_amount")
)

display(total_paid)
from pyspark.sql import SparkSession, functions as F, types as T
from pathlib import Path

spark = SparkSession.builder.appName("RoboticsTrainingDataQuality").getOrCreate()
root = Path(__file__).resolve().parents[1]

schema = T.StructType([
    T.StructField("session_id", T.StringType(), False),
    T.StructField("timestamp_ms", T.LongType(), True),
    T.StructField("camera_frame_id", T.StringType(), False),
    T.StructField("imu_ax", T.DoubleType(), True),
    T.StructField("imu_ay", T.DoubleType(), True),
    T.StructField("imu_az", T.DoubleType(), True),
    T.StructField("force_n", T.DoubleType(), True),
    T.StructField("action", T.StringType(), False),
    T.StructField("object_name", T.StringType(), False),
    T.StructField("recorded_at", T.StringType(), False),
])

raw = spark.read.option("header", True).schema(schema).csv(
    str(root / "data/raw/sensor_events.csv")
)

key_cols = ["session_id", "timestamp_ms", "camera_frame_id"]

with_reason = (
    raw.withColumn(
        "quality_reason",
        F.when(F.col("timestamp_ms").isNull(), F.lit("missing:timestamp_ms"))
         .when(F.col("force_n").isNull(), F.lit("missing:force_n"))
         .when((F.col("force_n") < 0) | (F.col("force_n") > 100), F.lit("out_of_range:force_n"))
    )
)

duplicates = (
    raw.groupBy(*key_cols).count()
       .filter(F.col("count") > 1)
       .select(*key_cols)
       .withColumn("duplicate_flag", F.lit(True))
)

joined = with_reason.join(duplicates, key_cols, "left").withColumn(
    "duplicate_flag", F.coalesce(F.col("duplicate_flag"), F.lit(False))
)

final = joined.withColumn(
    "quality_status",
    F.when(F.col("quality_reason").isNotNull(), "REJECT")
     .when(F.col("duplicate_flag"), "REJECT")
     .otherwise("ACCEPT")
)

accepted = final.filter("quality_status = 'ACCEPT'").drop("quality_reason", "duplicate_flag")
rejected = final.filter("quality_status = 'REJECT'")

out = root / "data/output/pyspark"
accepted.write.mode("overwrite").partitionBy("session_id").parquet(str(out / "curated"))
rejected.write.mode("overwrite").partitionBy("session_id").parquet(str(out / "rejected"))

print("Accepted:", accepted.count())
print("Rejected:", rejected.count())
spark.stop()

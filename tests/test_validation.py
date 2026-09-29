from pyspark.sql import SparkSession, functions as F

from src.validation import validate_customer_data


def test_customer_validation():

    spark = (
        SparkSession.builder
        .appName("TestValidation")
        .master("local[2]")
        .getOrCreate()
    )

    df = (
        spark.range(1).select(
            F.lit(101).alias("customer_id"),
            F.lit("Rahul").alias("name"),
            F.lit("rahul@gmail.com").alias("email"),
            F.lit(25).alias("age"),
            F.lit("India").alias("country")
        )
        .unionByName(
            spark.range(1).select(
                F.lit(102).alias("customer_id"),
                F.lit("John").alias("name"),
                F.lit(None).cast("string").alias("email"),
                F.lit(31).alias("age"),
                F.lit("USA").alias("country")
            )
        )
        .unionByName(
            spark.range(1).select(
                F.lit(103).alias("customer_id"),
                F.lit("Sarah").alias("name"),
                F.lit("sarah@gmail.com").alias("email"),
                F.lit(-5).alias("age"),
                F.lit("UK").alias("country")
            )
        )
    )

    valid_df, invalid_df = validate_customer_data(df)

    assert valid_df.count() == 1
    assert invalid_df.count() == 2

    spark.stop()
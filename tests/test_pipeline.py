from src.quality_report import generate_quality_report


def test_quality_report():

    report = generate_quality_report(
        total=100,
        valid=90,
        invalid=10
    )

    assert report["total_records"] == 100
    assert report["valid_records"] == 90
    assert report["invalid_records"] == 10
    assert report["quality_percentage"] == 90.0



from pyspark.sql import SparkSession, functions as F

from src.transformations import transform_customer_data


def test_transform_customer_data():

    spark = (
        SparkSession.builder
        .appName("TestTransformations")
        .master("local[2]")
        .getOrCreate()
    )

    df = spark.range(1).select(
        F.lit(101).alias("customer_id"),
        F.lit("rahul").alias("name"),
        F.lit("rahul@gmail.com").alias("email"),
        F.lit(25).alias("age"),
        F.lit("india").alias("country")
    )

    result = transform_customer_data(df)

    row = result.first()

    assert row["name"] == "Rahul"
    assert row["country"] == "INDIA"

    spark.stop()
from pyspark.sql import functions as F


def transform_customer_data(df):

    return (
        df
        .withColumn(
            "name",
            F.initcap(F.col("name"))
        )
        .withColumn(
            "country",
            F.upper(F.col("country"))
        )
    )
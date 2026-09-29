from pyspark.sql import functions as F


def validate_customer_data(df):

    valid_condition = (
        F.col("customer_id").isNotNull()
        & F.col("email").isNotNull()
        & (F.col("age") > 0)
        & F.col("country").isNotNull()
    )

    valid_df = df.filter(valid_condition)

    invalid_df = df.filter(~valid_condition)

    return valid_df, invalid_df
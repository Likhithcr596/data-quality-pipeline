from pyspark.sql import SparkSession

from transformations import transform_customer_data
from validation import validate_customer_data
from quality_report import generate_quality_report\

def create_spark_session():
    return (
        SparkSession.builder
        .appName("DataQualityPipeline")
        .master("local[*]")
        .getOrCreate()
    )


def read_customer_data(spark, file_path):
    return (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(file_path)
    )


def main():

    spark = create_spark_session()

    print("Data Quality Pipeline Started")

    df = read_customer_data(
        spark,
        "data/customers.csv"
    )

    print("Input Data:")
    df.show()

    valid_df, invalid_df = validate_customer_data(df)

    transformed_df = transform_customer_data(valid_df)

    print("Transformed Data:")
    transformed_df.show()

    print("Valid Records:")
    valid_df.show()

    print("Invalid Records:")
    invalid_df.show()

    print(f"Total Records: {df.count()}")
    print(f"Valid Records: {valid_df.count()}")
    print(f"Invalid Records: {invalid_df.count()}")


    # #write to o/p location
    # transformed_df.write.mode("overwrite").parquet("output/customers")
    # invalid_df.write.mode("overwrite").parquet("output/invalid_customers")

    total_records = df.count()
    valid_records = valid_df.count()
    invalid_records = invalid_df.count()

    report = generate_quality_report(
        total_records,
        valid_records,
        invalid_records
    )

    print("Data Quality Report:")
    print(report)


    spark.stop()


if __name__ == "__main__":
    main()
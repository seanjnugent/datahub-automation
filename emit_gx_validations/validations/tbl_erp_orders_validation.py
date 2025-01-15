import great_expectations as gx
from great_expectations.core import ExpectationConfiguration
from great_expectations.core.expectation_suite import ExpectationSuite
from datetime import datetime
import os

def run_validation(context):
    if context is None:
        raise ValueError("Context cannot be None")

    suite_name = "erp_orders_validation_suite"
    print(f"Creating suite: {suite_name}")

    try:
        suite = ExpectationSuite(expectation_suite_name=suite_name)

        expectations = [
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "erp_order_number"}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_of_type",
                kwargs={"column": "erp_customer_reference", "type_": "INTEGER"}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={"column": "erp_product_code", "regex": r'^[A-Z0-9]{1,20}$'}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={"column": "order_qty", "min_value": 1, "strict_min": True}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={"column": "unit_cost", "min_value": 0}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={"column": "order_creation_date", "min_value": "2000-01-01", "max_value": datetime.now().strftime("%Y-12-31")}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_in_set",
                kwargs={"column": "order_status", "value_set": ["PENDING", "SHIPPED", "DELIVERED", "CANCELLED"]}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={"column": "delivery_postcode", "regex": r'^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z])))) [0-9][A-Za-z]{2})$'}
            ),
        ]

        for expectation in expectations:
            suite.add_expectation(expectation)

        context.add_expectation_suite(expectation_suite=suite)
        context.save_expectation_suite(expectation_suite=suite)

        datasource = {
            "name": "erp_orders_postgres",
            "database_name": "postgres"
        }
        print(f"Datasource config: {datasource}")

        batch_request = {
            "datasource_name": datasource["name"],
            "data_connector_name": "default",
            "data_asset_name": "erp_orders",
            "table_name": "erp_orders",
            "schema_name": "public",
        }
        print(f"Batch request config: {batch_request}")

        if not all([batch_request, suite_name, datasource]):
            raise ValueError("One or more return values is None or empty")

        return batch_request, suite_name, datasource

    except Exception as e:
        print(f"Error in run_validation: {str(e)}")
        raise
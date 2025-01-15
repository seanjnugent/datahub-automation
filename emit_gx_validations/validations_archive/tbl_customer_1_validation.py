# validations/tbl_customer_validation.py

import great_expectations as gx
from great_expectations.core import ExpectationConfiguration
from great_expectations.core.expectation_suite import ExpectationSuite
from datetime import datetime
import os

def run_validation(context):
    if context is None:
        raise ValueError("Context cannot be None")

    # Define suite name
    suite_name = "customer_1_validation_suite"
    print(f"Creating suite: {suite_name}")  # Debug print
    
    try:
        # Create the suite first
        suite = ExpectationSuite(expectation_suite_name=suite_name)
        
        EMAIL_REGEX = r"^[^@]+@[^@]+\.[^@]+$"

        expectations = [
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "id"}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={
                    "column": "age",
                    "min_value": 0
                }
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={"column": "email", "regex": EMAIL_REGEX}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "email"}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={
                    "column": "signup_date",
                    "min_value": "1900-01-01",
                    "max_value": datetime.now().strftime("%Y-%m-%d")
                }
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "signup_date"}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "name"}
            ),
        ]
        
        # Add expectations to suite
        for expectation in expectations:
            suite.add_expectation(expectation)
        
        # Save the suite to the context
        context.add_expectation_suite(expectation_suite=suite)
        context.save_expectation_suite(expectation_suite=suite)
        
        # Datasource configuration
        datasource = {
            "name": "customers_postgres",
            "database_name": "postgres"  # Specify your database name here
        }
        print(f"Datasource config: {datasource}")  # Debug print

        # Batch request configuration
        batch_request = {
            "datasource_name": datasource["name"],
            "data_connector_name": "default",
            "data_asset_name": "customer_1",
            "table_name": "customers_test_data_1",
            "schema_name": "public",
        }
        print(f"Batch request config: {batch_request}")  # Debug print

        # Verify all values before returning
        if not all([batch_request, suite_name, datasource]):
            raise ValueError("One or more return values is None or empty")
            
        return batch_request, suite_name, datasource

    except Exception as e:
        print(f"Error in run_validation: {str(e)}")
        raise
# validations/tbl_prisoner_validation.py

import great_expectations as gx
from great_expectations.core import ExpectationConfiguration
from great_expectations.core.expectation_suite import ExpectationSuite
from datetime import datetime
import os

def run_validation(context):
    """Run validation for the prisoner table."""
    if context is None:
        raise ValueError("Context cannot be None")

    # Define suite name
    suite_name = "prisoner_validation_suite"
    print(f"Creating suite: {suite_name}")  # Debug print
    
    try:
        # Create the suite first
        suite = ExpectationSuite(expectation_suite_name=suite_name)
        
        # Define expectations
        NON_NUMERIC_REGEX = r"^\D+$"
        PERSONAL_IDENTIFIER_REGEX = r"^[A-Z]{2}\d{6}$"

        expectations = [
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={
                    "column": "cell_num",
                    "min_value": 1,
                    "max_value": 600
                }
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={
                    "column": "prisoner_id",
                    "min_value": 0
                }
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={
                    "column": "first_name",
                    "regex": NON_NUMERIC_REGEX
                }
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "prisoner_id"}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "first_name"}
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "cell_num"}
            ),
                # Ensure persona_identifier values are unique
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_unique",
                kwargs={
                    "column": "persona_identifier"
                }
            ),
            # Ensure persona_identifier values match the regex format
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={
                    "column": "persona_identifier",
                    "regex": PERSONAL_IDENTIFIER_REGEX
                }
            )
        ]
        
        # Add expectations to suite
        for expectation in expectations:
            suite.add_expectation(expectation)
        
        # Save the suite to the context
        context.add_expectation_suite(expectation_suite=suite)
        context.save_expectation_suite(expectation_suite=suite)
        print("Suite saved successfully")  # Debug print
        
        # Datasource configuration
        datasource = {
            "name": "prisons_demo",
            "database_name": "prisons_demo"  # Specify your database name here
        }
        print(f"Datasource config: {datasource}")  # Debug print
        
        # Batch request configuration
        batch_request = {
            "datasource_name": datasource["name"],
            "data_connector_name": "default",
            "data_asset_name": "prisoner",
            "table_name": "prisoner",
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
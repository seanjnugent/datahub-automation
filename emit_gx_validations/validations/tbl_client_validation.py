import great_expectations as gx
from great_expectations.core import ExpectationConfiguration
from great_expectations.core.expectation_suite import ExpectationSuite
from datetime import datetime
import os

def run_validation(context):
    if context is None:
        raise ValueError("Context cannot be None")

    # Define suite name
    suite_name = "client_validation_suite"
    print(f"Creating suite: {suite_name}")  # Debug print
    
    try:
        # Create the suite first
        suite = ExpectationSuite(expectation_suite_name=suite_name)
        
        # Regex for various validations
        EMAIL_REGEX = r"^[^@]+@[^@]+\.[^@]+$"
        UK_POSTCODE_REGEX = r'^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z])))) [0-9][A-Za-z]{2})$'
        NINO_REGEX = r'^[A-CEGHJ-PR-TW-Z]{1}[A-CEGHJ-NPR-TW-Z]{1}[0-9]{6}[A-D]{1}$'
        PHONE_REGEX = r'^(\+44|0)7\d{9}$|((\+44|0)[1-9]\d{8})$'  # Simplified UK mobile and landline

        # List of valid ISO 2-character country codes
        ISO_COUNTRY_CODES = [
            "GB", "IE", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST", "UV", "WX", "YZ",  # Example codes
            # Add all valid ISO 2-character country codes here
        ]

        expectations = [
            # Ensure client_id is not null
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "client_id"}
            ),
            # Validate email format
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={"column": "email_address", "regex": EMAIL_REGEX}
            ),
            # Ensure email is not null
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "email_address"}
            ),
            # Validate date_of_birth is between 1900-01-01 and the current year's end
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={
                    "column": "date_of_birth",
                    "min_value": "1900-01-01",
                    "max_value": datetime.now().strftime("%Y-12-31")  # Use end of year to avoid daily changes
                }
            ),
            # Ensure first_name is not null
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "first_name"}
            ),
            # Validate country codes are in the predefined set
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_in_set",
                kwargs={"column": "country", "value_set": ISO_COUNTRY_CODES}
            ),
            # Validate UK postcode format
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={"column": "postcode", "regex": UK_POSTCODE_REGEX}
            ),
            # Validate UK National Insurance Number format
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={"column": "national_insurance_number", "regex": NINO_REGEX}
            ),
            # Validate UK phone number format
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={"column": "phone_number", "regex": PHONE_REGEX}
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
            "name": "client_postgres",
            "database_name": "postgres"  # Specify your database name here
        }
        print(f"Datasource config: {datasource}")  # Debug print

        # Batch request configuration
        batch_request = {
            "datasource_name": datasource["name"],
            "data_connector_name": "default",
            "data_asset_name": "client",
            "table_name": "client",
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
import great_expectations as gx
from great_expectations.core import ExpectationConfiguration
from great_expectations.core.expectation_suite import ExpectationSuite

def run_validation(context):
    """Run validation for the prisoner table."""
    suite_name = "prisoner_validation_suite"
    NON_NUMERIC_REGEX = r"^\D+$"

    # Create or get the existing Expectation Suite
    try:
        suite = context.get_expectation_suite(expectation_suite_name=suite_name)
    except gx.exceptions.DataContextError:
        suite = ExpectationSuite(expectation_suite_name=suite_name)
        context.add_expectation_suite(expectation_suite=suite)

    # Add expectations to the suite
    expectations = [
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_between",
            kwargs={"column": "cell_num", "min_value": 1, "max_value": 600}
        ),
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_between",
            kwargs={"column": "prisoner_id", "min_value": 0}
        ),
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_match_regex",
            kwargs={"column": "first_name", "regex": NON_NUMERIC_REGEX}
        )
    ]

    for expectation in expectations:
        suite.add_expectation(expectation)

    # Save the suite to the context
    context.save_expectation_suite(expectation_suite=suite)

    # Create batch request
    batch_request = {
        "datasource_name": "prisons_demo",
        "data_connector_name": "default",
        "data_asset_name": "prisoner",
        "table_name": "prisoner",
        "schema_name": "public",
    }

    return batch_request, suite_name

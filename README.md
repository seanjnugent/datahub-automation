# Great Expectations Datahub Integration

This project demonstrates how to run data validations using Great Expectations on datasets stored in your database. It integrates with DataHub to send validation results and display under the Quality tab within a dataset. The project includes two simple validations.

## Project Structure
The project is structured as follows:

- validations/
    - __init__.py
    - tbl_[table]_validation.py
- validator_emit.ipynb

## Key Files
validations/: Contains Python modules for validation logic, one file per table with multiple validations per file.
__init__.py: Allows for importing the modules and validation functions as a Python package.

.env: This file should store your environment variables, including the DataHub server URL and token.
config.txt: A basic configuration file that helps users set up their .env file.
validator_emit.ipynb: Jupyter notebook for running validations and emitting results to DataHub.

## Prerequisites
1. Set Up DataHub
Before running validations, you need to have DataHub set up and running to capture the validation results.

2. Database
This project is using a Postgres DB

3. Environment Variables
Create a .env file based on the example config.txt. This file will store sensitive information like your DataHub server URL and token. The .env file should look like this:

DATAHUB_SERVER_URL=<your_datahub_server_url>
DATAHUB_TOKEN=<your_datahub_token>
PG_CONNECTION_STRING=<your_database_connection>

## Installation
Clone this repository:
Create and activate a virtual environment:
Install the required package

Custom Actions
This project uses DataHubValidationAction for sending results to DataHub:

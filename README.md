# DataHub Automation Playground  

This repo is a collection of scripts and notebooks designed to automate metadata management for Datahub, the data catalogue. This project focuses on governance, lineage, validation and custom property automation.

---

## What This Does  

- Validation with Great Expectations - Run data quality checks with Great Expectations and publish results to DataHub’s Quality tab. 
- Lineage Mapping - Emit column level lineage to datahub by defining a YAML file with column lineage.
- Governance Audits - Custom emitter to run governance checks (such as owners, completeness) and publish to Datahub.
- Custom Properties - Programatically add custom properties or custom metadatafields.

---

## Project Structure  

```plaintext

datahub-automation/
├── .env                    # Environment variables (e.g., tokens, database credentials)
├── config.txt              # Configuration reference for setting up .env
├── emit_custom_properties/ # Scripts for setting custom metadata
│   ├── custom_properties.yaml
│   ├── emit_custom_properties.ipynb
│   └── validation_schema.yaml # Template for validating custom_properties.yaml
├── emit_governance/        # Governance checks (e.g., missing owners)
│   └── governance_suite.ipynb
├── emit_gx_validations/    # Great Expectations validations
│   ├── validator_emit.ipynb
│   └── validations/ # Folder with quality checks against a given table
│       ├── __init__.py
│       ├── tbl_customer_1_validation.py
│       └── tbl_prisoner_validation.py
├── emit_lineage/           # Lineage automation scripts
│   ├── emit_custom_properties.ipynb
│   ├── lineage.yaml
│   └── validation_schema.yaml # Template for validating lineage.yaml
└── README.md

````

# DataHub Automation Playground  

Welcome to **DataHub Automation**, a collection of scripts and notebooks designed to automate and experiment with metadata management using **DataHub**. This project focuses on governance, lineage, validation, and custom property automation, connecting it all to DataHub's data catalog.  

This isn't just "another metadata project" – it’s a playground for testing and implementing metadata strategies at scale.  

---

## 🚀 What This Does  

- **Validation Integration:** Run data quality checks with Great Expectations and publish results to DataHub’s Quality tab.  
- **Lineage Mapping:** Automatically document dataset relationships without manual effort.  
- **Governance Audits:** Identify and log gaps (like missing owners) as governance tests.  
- **Custom Properties:** Add metadata details (like sensitivity or refresh dates) programmatically.  

If DataHub had a testing ground, this would be it.  

---


## Getting Started
Prerequisites
DataHub: Ensure DataHub is up and running (Docker setup recommended).
Database: This project currently supports PostgreSQL, but can be adapted for other databases.
Environment Variables: Create a .env file to store sensitive data. Use config.txt as a guide.
Example .env file:

DATAHUB_SERVER_URL=<your_datahub_url>
DATAHUB_TOKEN=<your_datahub_token>
PG_CONNECTION_STRING=<your_database_connection_string>

# Installation
Clone the repo:

git clone https://github.com/seanjnugent/datahub-automation.git
cd datahub-automation
Set up a virtual environment and install dependencies:

```plaintext

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

# How It Works
- Emit Custom Properties
Automate adding custom properties (like publisher levels or sensitivity).

- Emit Governance Tests
Run governance checks, such as identifying datasets with missing owners, and publish results to DataHub. This queries the underlying Datahub database to identify governance gaps with simple queries.

- Run Validations
Use Great Expectations to validate datasets and publish the results to DataHub’s Quality tab.

- Emit Lineage
Define lineage relationships in lineage.yaml and publish them to DataHub.

## Known Quirks
Validation suites need to be properly set up for Great Expectations, naming conventions and URI construction is case sensitive
Naming conventions matter for lineage scripts.

## Future Plans
Implement CI/CD for metadata validation
Scheduling
Build a dashboard to monitor metadata completeness over time.

## Why I Built This
Datahub is a good tool but its native functionality is quite limited. Script and interacting with the CLI makes the tool more useful, adding quality tests and column level lineage which are not available via the UI. I didn't find simple implementations of these scripts so decided to create my own suite based on the latest version of Datahub.

import json
import requests
from typing import Dict, Any
from datahub.emitter.mce_builder import make_dataset_urn, make_domain_urn, make_user_urn
from datahub.metadata.schema_classes import (
    DatasetSnapshotClass,
    DatasetPropertiesClass,
    MetadataChangeEventClass,
    OwnershipClass,
    OwnershipTypeClass,
    OwnerClass,
    DomainPropertiesClass,
    BrowsePathsClass
)
from datahub.emitter.rest_emitter import DatahubRestEmitter

# Constants
DATAHUB_REST_ENDPOINT = "http://localhost:8080"
DOMAIN_NAME = ""
PLATFORM_NAME = ""
ENV = "PROD"

def load_dcat_json(file_path: str) -> Dict[str, Any]:
    """Load and parse DCAT JSON metadata file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def transform_distribution_to_properties(distribution: list) -> Dict[str, Any]:
    """Transform DCAT distribution information into custom properties."""
    if not distribution:
        return {}
    
    properties = {}
    for idx, dist in enumerate(distribution):
        prefix = f"distribution_{idx+1}_"
        properties[f"{prefix}format"] = dist.get("format", "")
        properties[f"{prefix}accessURL"] = dist.get("accessURL", "")
        properties[f"{prefix}downloadURL"] = dist.get("downloadURL", "")
        properties[f"{prefix}mediaType"] = dist.get("mediaType", "")
    return properties

def transform_dcat_to_mce(dcat_dataset: Dict[str, Any], domain_urn: str) -> MetadataChangeEventClass:
    """Transform a DCAT dataset to DataHub MetadataChangeEvent (MCE)."""
    dataset_id = dcat_dataset.get("identifier", "unknown")
    dataset_title = dcat_dataset.get("title", "Untitled Dataset")
    description = dcat_dataset.get("description", "No description provided.")
    contact_info = dcat_dataset.get("contactPoint", {})
    contact_name = contact_info.get("fn", "unknown")
    contact_email = contact_info.get("hasEmail", "").replace("mailto:", "")
    keywords = dcat_dataset.get("keyword", [])
    access_level = dcat_dataset.get("accessLevel", "unknown")
    
    # Create distribution properties
    distribution_props = transform_distribution_to_properties(
        dcat_dataset.get("distribution", [])
    )

    # Combine all custom properties
    custom_properties = {
        "accessLevel": access_level,
        "contactName": contact_name,
        "contactEmail": contact_email,
        "issued": dcat_dataset.get("issued", ""),
        "modified": dcat_dataset.get("modified", ""),
        "landingPage": dcat_dataset.get("landingPage", ""),
        "temporal": dcat_dataset.get("temporal", ""),
        "spatial": dcat_dataset.get("spatial", ""),
        "accrualPeriodicity": dcat_dataset.get("accrualPeriodicity", ""),
        **distribution_props
    }

    # Create DataHub URNs
    dataset_urn = make_dataset_urn(PLATFORM_NAME, dataset_id, ENV)

    # Build Dataset Properties
    properties = DatasetPropertiesClass(
        name=dataset_title,
        description=description,
        customProperties=custom_properties,
        tags=keywords
    )

    # Create ownership aspect
    ownership = OwnershipClass(
        owners=[
            OwnerClass(
                owner=make_user_urn(contact_email) if contact_email != "" else make_user_urn("unknown"),
                type=OwnershipTypeClass.DATAOWNER
            )
        ]
    )

    # Create browse paths for better navigation
    browse_paths = BrowsePathsClass(
        paths=[f"/{DOMAIN_NAME}/{dataset_title}"]
    )

    # Create MetadataChangeEvent
    mce = MetadataChangeEventClass(
        proposedSnapshot=DatasetSnapshotClass(
            urn=dataset_urn,
            aspects=[
                properties,
                ownership,
                {"com.linkedin.dataset.Domain": {"domain": domain_urn}},
                browse_paths
            ]
        )
    )
    
    return mce

def emit_to_datahub(emitter: DatahubRestEmitter, mce: MetadataChangeEventClass) -> None:
    """Emit metadata to DataHub with error handling."""
    try:
        emitter.emit(mce)
        print(f"Successfully emitted: {mce.proposedSnapshot.urn}")
    except Exception as e:
        print(f"Failed to emit: {mce.proposedSnapshot.urn}")
        print(f"Error: {str(e)}")

def main():
    # Initialize emitter
    emitter = DatahubRestEmitter(DATAHUB_REST_ENDPOINT)
    
    # Create domain URN
    domain_urn = make_domain_urn(DOMAIN_NAME)
    
    try:
        # Load DCAT metadata
        dcat_data = load_dcat_json("dcat_metadata.json")
        
        # Emit each dataset to DataHub
        for dcat_dataset in dcat_data.get("dataset", []):
            mce = transform_dcat_to_mce(dcat_dataset, domain_urn)
            emit_to_datahub(emitter, mce)
            
    except FileNotFoundError:
        print("Error: dcat_metadata.json file not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in dcat_metadata.json")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()

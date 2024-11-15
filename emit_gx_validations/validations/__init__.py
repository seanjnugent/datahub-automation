"""
This package contains validation suites for different database tables.
Each validation module should implement a run_validation(context) function
that returns a tuple of (batch_request, suite_name).
"""

from pathlib import Path

# Make the validations directory a package
package_dir = Path(__file__).parent

# You can optionally add a function to list all available validation modules
def list_validation_modules():
    """List all available validation modules in the package."""
    validation_files = [
        f.stem for f in package_dir.glob("*_validation.py")
        if f.is_file() and not f.stem.startswith("_")
    ]
    return validation_files
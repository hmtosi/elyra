"""
Sample utility module for testing directory dependencies.
"""

import json
import csv


def load_config(config_path="config.json"):
    """Load configuration from JSON file."""
    with open(config_path, "r") as f:
        return json.load(f)


def load_data(data_path="data.csv"):
    """Load data from CSV file."""
    data = []
    with open(data_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def process_data(data, config):
    """Simple data processing function."""
    print(f"Processing {len(data)} rows with config: {config['model_name']}")
    return data

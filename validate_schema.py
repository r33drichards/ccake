#!/usr/bin/env python3

import json
import sys
import requests
from jsonschema import validate, ValidationError

def validate_server_json():
    """Validate server.json against the MCP schema"""

    # Read server.json
    try:
        with open('server.json', 'r') as f:
            server_data = json.load(f)
    except FileNotFoundError:
        print("Error: server.json not found")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in server.json: {e}")
        return False

    # Get schema URL from server.json
    schema_url = server_data.get('$schema')
    if not schema_url:
        print("Error: No $schema field found in server.json")
        return False

    # Download and load schema
    try:
        response = requests.get(schema_url)
        response.raise_for_status()
        schema = response.json()
    except requests.RequestException as e:
        print(f"Error downloading schema from {schema_url}: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in schema: {e}")
        return False

    # Validate server.json against schema
    try:
        validate(instance=server_data, schema=schema)
        print("✅ server.json is valid according to the schema")
        return True
    except ValidationError as e:
        print(f"❌ Validation error: {e.message}")
        print(f"Path: {' -> '.join(str(x) for x in e.absolute_path)}")
        return False

if __name__ == "__main__":
    if validate_server_json():
        sys.exit(0)
    else:
        sys.exit(1)
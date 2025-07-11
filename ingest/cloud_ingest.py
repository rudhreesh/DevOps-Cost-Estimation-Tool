import json
from typing import List, Dict

def load_cloud_data(file_path: str) -> List[Dict]:
    """Load Cloud VM/storage metrics from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading Cloud data: {e}")
        return []
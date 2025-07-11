import json
from typing import List, Dict

def load_db_data(file_path: str) -> List[Dict]:
    """Load Database metrics from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading DB data: {e}")
        return []
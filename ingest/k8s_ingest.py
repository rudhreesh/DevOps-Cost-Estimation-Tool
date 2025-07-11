import json
from typing import List, Dict

def load_k8s_data(file_path: str) -> List[Dict]:
    """Load Kubernetes pod metrics from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading Kubernetes data: {e}")
        return []
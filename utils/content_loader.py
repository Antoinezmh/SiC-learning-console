from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(relative_path: str):
    with open(ROOT / relative_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_json(relative_path: str):
    with open(ROOT / relative_path, "r", encoding="utf-8") as f:
        return json.load(f)

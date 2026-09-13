import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def save_data(filename: str, data: dict) -> None:

    file_path = DATA_DIR / f"{filename}.json"

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def load_data(filename: str) -> dict:

    file_path = DATA_DIR / f"{filename}.json"

    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)
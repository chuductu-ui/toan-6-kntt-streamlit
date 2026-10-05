"""Helper script to convert Google Cloud Service Account JSON key to Streamlit TOML format."""

import sys
import json
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def convert_json_to_toml(json_path: Path):
    if not json_path.exists():
        print(f"Error: File '{json_path}' khong ton tai!")
        return

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error doc file JSON: {e}")
        return

    print("=" * 60)
    print("COPY DOAN DUOI DAY VA DAN VAO STREAMLIT CLOUD (SETTINGS > SECRETS):")
    print("=" * 60)
    print()
    print('[gcp_service_account]')
    for k, v in data.items():
        if isinstance(v, str):
            v_escaped = v.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            print(f'{k} = "{v_escaped}"')
        else:
            print(f'{k} = {v}')
    print()
    print("=" * 60)
    print("EMAIL SERVICE ACCOUNT CAN DUOC CHIA SE (EDITOR) TREN GOOGLE DRIVE:")
    print(f"👉  {data.get('client_email', 'Khong tim thay')}")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        candidates = list(Path(".").glob("*.json"))
        if candidates:
            convert_json_to_toml(candidates[0])
        else:
            print("Cach dung: python convert_key_to_toml.py <duong_dan_file_key.json>")
    else:
        convert_json_to_toml(Path(sys.argv[1]))

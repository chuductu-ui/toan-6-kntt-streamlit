"""Helper script to convert Google Cloud Service Account JSON key to Streamlit TOML format."""

import sys
import json
from pathlib import Path

def convert_json_to_toml(json_path: Path):
    if not json_path.exists():
        print(f"Error: File '{json_path}' không tồn tại!")
        return

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error đọc file JSON: {e}")
        return

    print("=" * 60)
    print("COPY ĐOẠN DƯỚI ĐÂY VÀ DÁN VÀO STREAMLIT CLOUD (SETTINGS > SECRETS):")
    print("=" * 60)
    print()
    print('[gcp_service_account]')
    for k, v in data.items():
        if isinstance(v, str):
            # Escape double quotes and newlines for TOML
            v_escaped = v.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            print(f'{k} = "{v_escaped}"')
        else:
            print(f'{k} = {v}')
    print()
    print("=" * 60)
    print("Email Service Account cần được cấp quyền Editor trên thư mục Google Drive là:")
    print(f"👉  {data.get('client_email', 'Không tìm thấy client_email')}")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Check if there is any .json file in current folder with 'service' or 'credentials' in name
        candidates = list(Path(".").glob("*.json"))
        if candidates:
            print(f"Tự động tìm thấy file: {candidates[0].name}")
            convert_json_to_toml(candidates[0])
        else:
            print("Cách dùng: python convert_key_to_toml.py <duong_dan_file_key.json>")
    else:
        convert_json_to_toml(Path(sys.argv[1]))

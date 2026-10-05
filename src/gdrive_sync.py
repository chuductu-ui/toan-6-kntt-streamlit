"""Google Drive integration module for Streamlit Cloud synchronization."""

import io
from pathlib import Path
from typing import Optional, Dict, Any

from config import DATA_DIR, UPLOADS_DIR, DB_PATH


def is_gdrive_configured() -> bool:
    """Check if Google Drive credentials exist in streamlit secrets."""
    try:
        import streamlit as st
        return "gcp_service_account" in st.secrets
    except Exception:
        return False


class GDriveSync:
    """Manages cloud synchronization between SQLite database/images and Google Drive."""

    _service = None
    _folder_id = None

    @classmethod
    def get_service(cls):
        """Initialize and cache the Google Drive v3 resource."""
        if cls._service is not None:
            return cls._service

        try:
            import streamlit as st
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            if "gcp_service_account" not in st.secrets:
                return None

            creds_dict = dict(st.secrets["gcp_service_account"])
            credentials = service_account.Credentials.from_service_account_info(
                creds_dict,
                scopes=["https://www.googleapis.com/auth/drive"]
            )
            cls._service = build("drive", "v3", credentials=credentials)
            cls._folder_id = st.secrets.get("gdrive_folder_id", None)
            return cls._service
        except Exception as e:
            print(f"GDrive initialization skipped or failed: {e}")
            return None

    @classmethod
    def ensure_data_folder(cls) -> Optional[str]:
        """Find or create 'VuonToan6_Data' folder in Google Drive."""
        service = cls.get_service()
        if not service:
            return None

        if cls._folder_id:
            return cls._folder_id

        try:
            # Search for folder
            query = "name = 'VuonToan6_Data' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            files = results.get("files", [])

            if files:
                cls._folder_id = files[0]["id"]
            else:
                folder_metadata = {
                    "name": "VuonToan6_Data",
                    "mimeType": "application/vnd.google-apps.folder"
                }
                folder = service.files().create(body=folder_metadata, fields="id").execute()
                cls._folder_id = folder.get("id")

            return cls._folder_id
        except Exception as e:
            print(f"Error ensuring GDrive folder: {e}")
            return None

    @classmethod
    def download_db_from_gdrive(cls) -> bool:
        """Download math6.db from Google Drive if available."""
        service = cls.get_service()
        folder_id = cls.ensure_data_folder()
        if not service or not folder_id:
            return False

        try:
            from googleapiclient.http import MediaIoBaseDownload

            query = f"name = 'math6.db' and '{folder_id}' in parents and trashed = false"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            files = results.get("files", [])

            if not files:
                return False

            file_id = files[0]["id"]
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(DB_PATH, "wb") as f:
                f.write(fh.getvalue())

            print("Downloaded math6.db from Google Drive successfully.")
            return True
        except Exception as e:
            print(f"Error downloading DB from Google Drive: {e}")
            return False

    @classmethod
    def upload_db_to_gdrive(cls) -> bool:
        """Upload current math6.db to Google Drive."""
        service = cls.get_service()
        folder_id = cls.ensure_data_folder()
        if not service or not folder_id or not DB_PATH.exists():
            return False

        try:
            from googleapiclient.http import MediaFileUpload

            query = f"name = 'math6.db' and '{folder_id}' in parents and trashed = false"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            files = results.get("files", [])

            media = MediaFileUpload(str(DB_PATH), mimetype="application/x-sqlite3", resumable=True)

            if files:
                file_id = files[0]["id"]
                service.files().update(fileId=file_id, media_body=media).execute()
            else:
                file_metadata = {
                    "name": "math6.db",
                    "parents": [folder_id]
                }
                service.files().create(body=file_metadata, media_body=media).execute()

            print("Uploaded math6.db to Google Drive successfully.")
            return True
        except Exception as e:
            print(f"Error uploading DB to Google Drive: {e}")
            return False

    @classmethod
    def upload_image_to_gdrive(cls, image_filename: str) -> Optional[str]:
        """Upload a snapshot image to Google Drive folder."""
        service = cls.get_service()
        folder_id = cls.ensure_data_folder()
        local_img = UPLOADS_DIR / image_filename
        if not service or not folder_id or not local_img.exists():
            return None

        try:
            from googleapiclient.http import MediaFileUpload

            media = MediaFileUpload(str(local_img), mimetype="image/jpeg", resumable=True)
            file_metadata = {
                "name": image_filename,
                "parents": [folder_id]
            }
            res = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            return res.get("id")
        except Exception as e:
            print(f"Error uploading image to Google Drive: {e}")
            return None

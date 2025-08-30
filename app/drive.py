import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_gdrive_service(credentials_path):
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)
    return service

def list_files(service, folder_id, mime_types=None):
    q = f"'{folder_id}' in parents and trashed=false"
    if mime_types:
        q += " and (" + " or ".join([f"mimeType contains '{mtype}'" for mtype in mime_types]) + ")"
    files = []
    page_token = None
    while True:
        resp = (
            service.files()
            .list(
                q=q,
                spaces="drive",
                fields="nextPageToken, files(id, name, mimeType, size, createdTime, md5Checksum, imageMediaMetadata, videoMediaMetadata)",
                pageToken=page_token,
            )
            .execute()
        )
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files

def download_file(service, file_id, file_name, dest_folder="/tmp"):
    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(dest_folder, file_name)
    with open(file_path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    return file_path

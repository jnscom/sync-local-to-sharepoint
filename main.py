import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

# Azure AD App Information
CLIENT_ID = os.environ.get("CLIENT_ID")
TENANT_ID = os.environ.get("TENANT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

# SharePoint Website
SHAREPOINT_SITE_ID = os.environ.get("SHAREPOINT_SITE_ID")
SHAREPOINT_DOC_LIBRARY = os.environ.get("SHAREPOINT_DOC_LIBRARY")
LOCAL_FOLDER = os.environ.get("LOCAL_FOLDER")

# MS Graph API Endpoints
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
RESOURCE = "https://graph.microsoft.com/"
SCOPES = ["https://graph.microsoft.com/.default"]

app = ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
result = app.acquire_token_for_client(scopes=SCOPES)

if "access_token" in result:
    token = result["access_token"]
else:
    raise Exception("Kein Access-Token erhalten.")


def upload_file_to_sharepoint(file_path, sharepoint_folder):
    file_name = os.path.basename(file_path)
    upload_url = f"{RESOURCE}v1.0/sites/{SHAREPOINT_SITE_ID}/drive/root:/{sharepoint_folder}/{file_name}:/content"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }

    with open(file_path, 'rb') as file:
        response = requests.put(upload_url, headers=headers, data=file)

    if response.status_code == 201:
        print(f"'{file_name}' erfolgreich hochgeladen.")
    else:
        print(f"Fehler beim Hochladen von '{file_name}': {response.status_code}, {response.text}")


def get_files_in_sharepoint_folder(sharepoint_folder):
    folder_url = f"{RESOURCE}v1.0/sites/{SHAREPOINT_SITE_ID}/drive/root:/{sharepoint_folder}:/children"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(folder_url, headers=headers)
    if response.status_code == 200:
        items = response.json().get('value', [])
        return {item['name']: item['id'] for item in items}
    else:
        print(f"Fehler beim Abrufen der Dateien in SharePoint: {response.status_code}, {response.text}")
        return {}


def delete_file_from_sharepoint(file_id):
    delete_url = f"{RESOURCE}v1.0/sites/{SHAREPOINT_SITE_ID}/drive/items/{file_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(delete_url, headers=headers)
    if response.status_code == 204:
        print(f"Datei erfolgreich gelöscht.")
    else:
        print(f"Fehler beim Löschen der Datei: {response.status_code}, {response.text}")


def sync_local_folder_to_sharepoint(local_folder, sharepoint_folder):
    sharepoint_files = get_files_in_sharepoint_folder(sharepoint_folder)

    for root, dirs, files in os.walk(local_folder):
        relative_path = os.path.relpath(root, local_folder)
        sharepoint_path = os.path.join(sharepoint_folder, relative_path).replace("\\", "/")

        for file in files:
            file_path = os.path.join(root, file)
            upload_file_to_sharepoint(file_path, sharepoint_path)
            if file in sharepoint_files:
                del sharepoint_files[file]

    for file_name, file_id in sharepoint_files.items():
        print(f"Lösche Datei in SharePoint: {file_name}")
        delete_file_from_sharepoint(file_id)


if __name__ == '__main__':
    sync_local_folder_to_sharepoint(LOCAL_FOLDER, SHAREPOINT_DOC_LIBRARY)

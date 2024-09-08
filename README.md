# Synchronization of local folder and SharePoint

This script helps you sync files between a local folder and a SharePoint document library using the Microsoft Graph API. It uploads, retrieves, and deletes files to keep everything in sync.

## Requirements

1. **Python 3.x**: Make sure Python is installed.
2. **Dependencies**: Install the required packages with:

   ```bash
   pip install requests msal python-dotenv
   ```

3. **Azure AD App**: Register an app in Azure AD to obtain the necessary credentials (Client ID, Tenant ID, Client Secret).

4. **.env File**: Create a `.env` file in the script's directory and add the following values:

   ```plaintext
   CLIENT_ID=Your_Client_ID
   TENANT_ID=Your_Tenant_ID
   CLIENT_SECRET=Your_Client_Secret
   SHAREPOINT_SITE_ID=Your_SharePoint_Site_ID
   SHAREPOINT_DOC_LIBRARY=Your_SharePoint_Document_Library_Path
   LOCAL_FOLDER=Path_to_Your_Local_Folder
   ```

## How to Use the Script

1. **Run the Script**: Start the script with:

   ```bash
   python sync_script.py
   ```

2. **What Happens**:
   - An access token is retrieved to interact with the Microsoft Graph API.
   - Files in the local folder are uploaded to the SharePoint document library.
   - Files that are no longer in the local folder are deleted from SharePoint.

## Functions

- **upload_file_to_sharepoint**: Uploads a file to SharePoint.
- **get_files_in_sharepoint_folder**: Retrieves all files in a SharePoint folder.
- **delete_file_from_sharepoint**: Deletes a file from SharePoint.
- **sync_local_folder_to_sharepoint**: Syncs the local folder with SharePoint.

## Security

Keep your `.env` file secure as it contains sensitive information.

*JNS | 2024*
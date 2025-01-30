import os
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
account_url = "xxx"
container_name = "xxx"
folder_path = "xxx"
files_to_download = ['xxx']
download_dir = "C:/Users/xxx/Desktop"

blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
container_client = blob_service_client.get_container_client(container_name)

for file_name in files_to_download:
    file_found = False
    for blob in container_client.list_blobs(name_starts_with=folder_path):
        print(f"Checking blob: {blob.name}")  

        if file_name in blob.name:
            blob_client = container_client.get_blob_client(blob.name)
            download_file_path = os.path.join(download_dir, blob.name.replace("/", "_"))
            
            with open(download_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            print(f"Downloaded {blob.name} to {download_file_path}")
            file_found = True
            break

    if not file_found:
        print(f"{file_name} not found in the container within {folder_path}.")

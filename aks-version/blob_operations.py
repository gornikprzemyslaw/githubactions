from azure.storage.blob import BlobClient, BlobServiceClient
from azure.identity import DefaultAzureCredential
import json
import ast
import os
import io

storage_account_url = os.getenv("STORAGE_ACCOUNT_URL")
container_name = "versions"
creds = DefaultAzureCredential()
patch_versions_blob = "aks_patch_versions.json"
patch_versions_url = f"{storage_account_url}/{container_name}/{patch_versions_blob}"
patch_version_client = BlobClient.from_blob_url(
    blob_url=patch_versions_url,
    credential=creds
)


def read_blobs():

    patch_versions_download = patch_version_client.download_blob()
    patch_versions_content = patch_versions_download.readall().decode("utf-8")
    previous_patch_versions = ast.literal_eval(patch_versions_content)

    return previous_patch_versions


def save_blobs(list_of_patch_versions: list[str]):

    jsonData = json.dumps(list_of_patch_versions)
    binaryData = jsonData.encode()
    input_stream = io.BytesIO(binaryData)
    patch_version_client.upload_blob(input_stream, blob_type="BlockBlob", overwrite=True)

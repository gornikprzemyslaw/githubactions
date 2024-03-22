from azure.storage.blob import BlobClient, BlobServiceClient
from azure.identity import DefaultAzureCredential
from loguru import logger
import json
import ast
import os



def read_blobs():

    storage_account_url = os.getenv("STORAGE_ACCOUNT_URL")
    container_name = "versions"
    creds = DefaultAzureCredential()
    service_client = BlobServiceClient(
        account_url=storage_account_url,
        credential=creds
    )

    minor_versions_blob = "aks_versions.json"
    minor_versions_url = f"{storage_account_url}/{container_name}/{minor_versions_blob}"
    minor_version_client = BlobClient.from_blob_url(
        blob_url=minor_versions_url,
        credential=creds
    )
    # read blob
    minor_versions_download = minor_version_client.download_blob()
    minor_versions_content = minor_versions_download.readall().decode("utf-8")
    previous_minor_versions = ast.literal_eval(minor_versions_content)

    patch_versions_blob = "aks_patch_versions.json"
    patch_versions_url = f"{storage_account_url}/{container_name}/{patch_versions_blob}"
    patch_version_client = BlobClient.from_blob_url(
        blob_url=patch_versions_url,
        credential=creds
    )
    # read blob
    patch_versions_download = patch_version_client.download_blob()
    patch_versions_content = patch_versions_download.readall().decode("utf-8")
    previous_patch_versions = ast.literal_eval(patch_versions_content)

    return previous_minor_versions[0], previous_patch_versions


def save_blobs(last_version, list_of_patch_versions):

    storage_account_url = os.getenv("STORAGE_ACCOUNT_URL")
    container_name = "versions"
    creds = DefaultAzureCredential()
    service_client = BlobServiceClient(
        account_url=storage_account_url,
        credential=creds
    )

    minor_versions_blob = "aks_versions.json"
    minor_versions_url = f"{storage_account_url}/{container_name}/{minor_versions_blob}"
    minor_version_client = BlobClient.from_blob_url(
        blob_url=minor_versions_url,
        credential=creds
    )
    # save blob
    save_minor_version = [last_version]
    with open("save_minor_version", "w") as fp:
        json.dump(save_minor_version, fp)

    with open("save_minor_version", "r") as fp:
        b = json.load(fp)

    with open("save_minor_version", "rb") as blob_file:
        minor_version_client.upload_blob(data=blob_file, overwrite=True)

    patch_versions_blob = "aks_patch_versions.json"
    patch_versions_url = f"{storage_account_url}/{container_name}/{patch_versions_blob}"
    patch_version_client = BlobClient.from_blob_url(
        blob_url=patch_versions_url,
        credential=creds
    )
    # save blob

    with open("list_of_patch_versions", "w") as fp:
        json.dump(list_of_patch_versions, fp)

    with open("list_of_patch_versions", "r") as fp:
        b = json.load(fp)

    with open("list_of_patch_versions", "rb") as blob_file:
        patch_version_client.upload_blob(data=blob_file, overwrite=True)
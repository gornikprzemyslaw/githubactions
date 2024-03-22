from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from azure.core.exceptions import HttpResponseError
from azure.communication.email import EmailClient
from loguru import logger
import os
from aks_operations import check_minor_and_patch_versions
from blob_operations import read_blobs, save_blobs
import json
import hcl2

class Email(object):

    connection_string = os.getenv("ENDPOINT") + ";" + os.getenv("ACCESS_KEY")
    sender_address = os.getenv("SENDER_ADDRESS")
    recipient_address = os.getenv("RECIPIENT_ADDRESS")
    second_recipient_address = os.getenv("SECOND_RECIPIENT_ADDRESS")


    def send_email_to_multiple_recipients(self):

        last_version, preview_version, list_of_patch_versions = check_minor_and_patch_versions()
        logger.info(f"Last AKS version: {last_version}")
        logger.info(f"Preview version: {preview_version}")
        logger.info(f"List of AKS patch versions: {list_of_patch_versions}")

        previous_minor_versions, previous_patch_versions = read_blobs()
        logger.info(f"Previous minor version: {previous_minor_versions}")
        logger.info(f"Previous patch versions: {previous_patch_versions}")


        def send_message():

            # creating the email client
            email_client = EmailClient.from_connection_string(self.connection_string)


            patch_version = list(set(list_of_patch_versions) - set(previous_patch_versions))
            version_message = None
            if last_version > previous_minor_versions:
                version_message = f"Last AKS minor version is: {last_version}."
            elif(len(patch_version) != 0):
                version_message = f"Last AKS patch version is: {patch_version}."


            # creating the email message
            message = {
                "content": {
                    "subject": "Last AKS version",
                    "plainText": "This is the body",
                    "html": f"<html><h1>{version_message}</h1></html>"
                },
                "recipients": {
                    "to": [
                        {"address": self.recipient_address, "displayName": "Customer Name"},
                        {"address": self.second_recipient_address, "displayName": "Customer Name 2"}
                    ],
                    "cc": [
                        {"address": self.recipient_address, "displayName": "Customer Name"},
                        {"address": self.second_recipient_address, "displayName": "Customer Name 2"}
                    ],
                    "bcc": [
                        {"address": self.recipient_address, "displayName": "Customer Name"},
                        {"address": self.second_recipient_address, "displayName": "Customer Name 2"}
                    ]
                },
                "senderAddress": self.sender_address
            }

            try:
                # sending the email message
                if(last_version > previous_minor_versions or len(patch_version) != 0):
                    poller = email_client.begin_send(message)
                    response = poller.result()
                    logger.info("Operation ID: " + response['id'])
            except HttpResponseError as ex:
                logger.info(ex)
                pass

        # def save_blobs(last_version, list_of_patch_versions):
        #     from azure.storage.blob import BlobClient, BlobServiceClient
        #     import json
        #     import ast
        #
        #     storage_account_url = os.getenv("STORAGE_ACCOUNT_URL")
        #     container_name = "versions"
        #     creds = DefaultAzureCredential()
        #     service_client = BlobServiceClient(
        #         account_url=storage_account_url,
        #         credential=creds
        #     )
        #
        #     minor_versions_blob = "aks_versions.json"
        #     minor_versions_url = f"{storage_account_url}/{container_name}/{minor_versions_blob}"
        #     minor_version_client = BlobClient.from_blob_url(
        #         blob_url=minor_versions_url,
        #         credential=creds
        #     )
        #     # save blob
        #     save_minor_version = [last_version]
        #     with open("save_minor_version", "w") as fp:
        #         json.dump(save_minor_version, fp)
        #
        #     with open("save_minor_version", "r") as fp:
        #         b = json.load(fp)
        #
        #     with open("save_minor_version", "rb") as blob_file:
        #         minor_version_client.upload_blob(data=blob_file, overwrite=True)
        #
        #     patch_versions_blob = "aks_patch_versions.json"
        #     patch_versions_url = f"{storage_account_url}/{container_name}/{patch_versions_blob}"
        #     patch_version_client = BlobClient.from_blob_url(
        #         blob_url=patch_versions_url,
        #         credential=creds
        #     )
        #     # save blob
        #
        #     with open("list_of_patch_versions", "w") as fp:
        #         json.dump(list_of_patch_versions, fp)
        #
        #     with open("list_of_patch_versions", "r") as fp:
        #         b = json.load(fp)
        #
        #     with open("list_of_patch_versions", "rb") as blob_file:
        #         patch_version_client.upload_blob(data=blob_file, overwrite=True)

        send_message()
        save_blobs(last_version, list_of_patch_versions)

if __name__ == '__main__':
    sample = Email()
    sample.send_email_to_multiple_recipients()

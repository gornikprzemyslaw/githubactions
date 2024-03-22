from azure.core.exceptions import HttpResponseError
from azure.communication.email import EmailClient
from loguru import logger
import os
from aks_operations import check_minor_and_patch_versions, check_current_aks_version
from blob_operations import read_blobs, save_blobs


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

        previous_patch_versions = read_blobs()
        current_minor_version = check_current_aks_version()
        logger.info(f"Current AKS minor version: {current_minor_version}")
        logger.info(f"Previous patch versions: {previous_patch_versions}")


        def send_message():

            # creating the email client
            email_client = EmailClient.from_connection_string(self.connection_string)

            patch_version = list(set(list_of_patch_versions) - set(previous_patch_versions))
            logger.info(f"New patch version: {patch_version}")
            version_message = None
            if last_version > current_minor_version + 1:
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
                if last_version > current_minor_version + 1 or (len(patch_version) != 0 and str(current_minor_version) in patch_version[0]):
                    logger.info("Sending an email...")
                    poller = email_client.begin_send(message)
                    response = poller.result()
                    logger.info("Operation ID: " + response['id'])
            except HttpResponseError as ex:
                logger.info(ex)
                pass

        send_message()
        save_blobs(list_of_patch_versions)

if __name__ == '__main__':
    sample = Email()
    sample.send_email_to_multiple_recipients()

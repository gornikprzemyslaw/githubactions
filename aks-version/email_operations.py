from azure.core.exceptions import HttpResponseError
from azure.communication.email import EmailClient
from loguru import logger
import os


class Email(object):

    connection_string = os.getenv("CONNECTION_STRING")
    sender_address = os.getenv("SENDER_ADDRESS")
    recipient_address = os.getenv("RECIPIENT_ADDRESS")
    second_recipient_address = os.getenv("SECOND_RECIPIENT_ADDRESS")

    def __init__(
        self,
        last_version,
        preview_version,
        current_minor_version,
        list_of_patch_versions,
        previous_patch_versions,
    ):
        self.last_version = last_version
        self.preview_version = preview_version
        self.current_minor_version = current_minor_version
        self.list_of_patch_versions = list_of_patch_versions
        self.previous_patch_versions = previous_patch_versions

    def send_email_to_multiple_recipients(self):

        email_client = EmailClient.from_connection_string(self.connection_string)
        logger.info(f"Last AKS version: {self.last_version}")
        logger.info(f"Preview version: {self.preview_version}")
        logger.info(f"List of AKS patch versions: {self.list_of_patch_versions}")
        logger.info(f"Current AKS minor version: {self.current_minor_version}")
        logger.info(f"Previous patch versions: {self.previous_patch_versions}")

        patch_version = list(
            set(self.list_of_patch_versions) - set(self.previous_patch_versions)
        )
        logger.info(f"New patch version: {patch_version}")
        version_message = None
        if self.last_version > self.current_minor_version + 0.01:
            version_message = f"Last AKS minor version is: {self.last_version}."
        elif len(patch_version):
            version_message = f"Last AKS patch version is: {patch_version}."


        # creating the email message
        message = {
            "content": {
                "subject": "Last AKS version",
                "plainText": "This is the body",
                "html": f"<html><h1>{version_message}</h1></html>",
            },
            "recipients": {
                "to": [
                    {"address": self.recipient_address, "displayName": "Customer Name"},
                    {
                        "address": self.second_recipient_address,
                        "displayName": "Customer Name 2",
                    },
                ],
                "cc": [
                    {"address": self.recipient_address, "displayName": "Customer Name"},
                    {
                        "address": self.second_recipient_address,
                        "displayName": "Customer Name 2",
                    },
                ],
                "bcc": [
                    {"address": self.recipient_address, "displayName": "Customer Name"},
                    {
                        "address": self.second_recipient_address,
                        "displayName": "Customer Name 2",
                    },
                ]
            },
            "senderAddress": self.sender_address,
        }

        # these conditions checks if new patch version from current version has been released or new minor version is 2 greater than the current one
        minor_version_condition = self.last_version > self.current_minor_version + 0.01
        patch_version_condition = (
            len(patch_version) and str(self.current_minor_version) in patch_version[0]
        )
        logger.info(f"Minor version condition: {minor_version_condition}")
        logger.info(f"Patch version condition: {patch_version_condition}")
        try:
            if minor_version_condition or patch_version_condition:
                logger.info("Sending an email...")
                poller = email_client.begin_send(message)
                response = poller.result()
                logger.info("Operation ID: " + response["id"])
        except HttpResponseError as ex:
            logger.info(ex)
            pass

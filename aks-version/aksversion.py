from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
import os
import sys
from azure.core.exceptions import HttpResponseError

from azure.communication.email import EmailClient


class Email(object):

    #connection_string = os.getenv("COMMUNICATION_CONNECTION_STRING_EMAIL")
    connection_string = "endpoint=https://akstest.unitedstates.communication.azure.com/;accesskey=Ct2cXmnwnYKW8eGEiA0BVdjIJcXJM+twFBox/SF9fTGf1kORB1zUMwj/WT7Xdf4QL28KCHt8RivTGjkrBynbLQ=="
    #sender_address = os.getenv("SENDER_ADDRESS")
    sender_address = "DoNotReply@f5ca9f5e-eee2-4e19-9b3d-e9a13e7c54fb.azurecomm.net"
    #recipient_address = os.getenv("RECIPIENT_ADDRESS")
    recipient_address = "przemyslaw.gornik@dxc.com"
    #second_recipient_address = os.getenv("SECOND_RECIPIENT_ADDRESS")
    second_recipient_address = "gornik.przemek@gmail.com"

    def send_email_to_multiple_recipients(self):

        def check_last_aks_versions():
            client = ContainerServiceClient(
                credential=DefaultAzureCredential(),
                subscription_id="9c68d842-8240-43e8-9cad-3495f9769729",
            )

            response = client.managed_clusters.list_kubernetes_versions(
                location="westeurope",
            )
            list_of_versions = []
            list_of_preview_versions = []
            #print(response.values)
            for i in response.values:
                if(i.is_preview) == True:
                    list_of_preview_versions.append(float(i.version))
                else:
                    list_of_versions.append(float(i.version))

            print(f"List of AKS versions: {list_of_versions}")
            print(f"List of AKS preview: {list_of_preview_versions}")

            last_version = max(list_of_versions)
            if len(list_of_preview_versions) == 0:
                preview_version = null
            else:
                preview_version = max(list_of_preview_versions)
            return last_version, preview_version

        last_version, preview_version = check_last_aks_versions()
        print(f"Last AKS version: {last_version}")
        print(f"Preview version: {preview_version}")


        def read_blob():
            from azure.storage.blob import BlobClient, BlobServiceClient
            import json
            import ast

            account_url = "https://aksversion.blob.core.windows.net/"

            creds = DefaultAzureCredential()
            service_client = BlobServiceClient(
                account_url=account_url,
                credential=creds
            )

            blob_name = "aks_versions.json"
            container_name = "versions"
            blob_url = f"{account_url}/{container_name}/{blob_name}"

            blob_client = BlobClient.from_blob_url(
                blob_url=blob_url,
                credential=creds
            )
            # read blob
            blob_download = blob_client.download_blob()
            blob_content = blob_download.readall().decode("utf-8")

            saved_aks_versions = ast.literal_eval(blob_content)
            # print( saved_aks_versions[0])
            # print(type( saved_aks_versions))
            return saved_aks_versions[0]



        saved_version = read_blob()
        print(f"Saved_version: {saved_version}")


        def send_message():

            # creating the email client
            email_client = EmailClient.from_connection_string(self.connection_string)
            # creating the email message
            message = {
                "content": {
                    "subject": "Last AKS version",
                    "plainText": "This is the body",
                    "html": f"<html><h1>Last AKS version is: {last_version}</h1></html>"
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
                poller = email_client.begin_send(message)
                response = poller.result()
                print("Operation ID: " + response['id'])
            except HttpResponseError as ex:
                print(ex)
                pass

        send_message()

if __name__ == '__main__':
    sample = Email()
    sample.send_email_to_multiple_recipients()

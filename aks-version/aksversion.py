from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
import os
import sys
from azure.core.exceptions import HttpResponseError

from azure.communication.email import EmailClient


class EmailMultipleRecipientSample(object):

    #connection_string = os.getenv("COMMUNICATION_CONNECTION_STRING_EMAIL")
    connection_string = "endpoint=https://akstest.unitedstates.communication.azure.com/;accesskey=Ct2cXmnwnYKW8eGEiA0BVdjIJcXJM+twFBox/SF9fTGf1kORB1zUMwj/WT7Xdf4QL28KCHt8RivTGjkrBynbLQ=="
    #sender_address = os.getenv("SENDER_ADDRESS")
    sender_address = "DoNotReply@f5ca9f5e-eee2-4e19-9b3d-e9a13e7c54fb.azurecomm.net"
    #recipient_address = os.getenv("RECIPIENT_ADDRESS")
    recipient_address = "przemyslaw.gornik@dxc.com"
    #second_recipient_address = os.getenv("SECOND_RECIPIENT_ADDRESS")
    second_recipient_address = "gornik.przemek@gmail.com"

    def send_email_to_multiple_recipients(self):
        # creating the email client
        email_client = EmailClient.from_connection_string(self.connection_string)

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

        print(f"list of versions: {list_of_versions}")
        print(f"list of preview versions: {list_of_preview_versions}")

        #response2 = "la la la la"

        # creating the email message
        message = {
            "content": {
                "subject": "This is the subject",
                "plainText": "This is the body",
                "html": f"<html><h1>{list_of_versions}</h1></html>"
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

if __name__ == '__main__':
    sample = EmailMultipleRecipientSample()
    sample.send_email_to_multiple_recipients()














#connection_string = "endpoint=https://akstest.unitedstates.communication.azure.com/;accesskey=Ct2cXmnwnYKW8eGEiA0BVdjIJcXJM+twFBox/SF9fTGf1kORB1zUMwj/WT7Xdf4QL28KCHt8RivTGjkrBynbLQ=="
#client = EmailClient.from_connection_string(connection_string);

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-containerservice
# USAGE
    python kubernetes_versions_list.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


# def main():
#     client = ContainerServiceClient(
#         credential=DefaultAzureCredential(),
#         subscription_id="9c68d842-8240-43e8-9cad-3495f9769729",
#     )
#
#     response = client.managed_clusters.list_kubernetes_versions(
#         location="westeurope",
#     )
#     print(response.values)
    # for i in response.values:
    #     print(i)


# # x-ms-original-file: specification/containerservice/resource-manager/Microsoft.ContainerService/aks/stable/2023-11-01/examples/KubernetesVersions_List.json
# if __name__ == "__main__":
#     main()
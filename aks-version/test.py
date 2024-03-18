from azure.identity import DefaultAzureCredential
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
#print(f"Your content is: '{blob_content}'")

b = ast.literal_eval(blob_content)
print(b[0])
print(type(b))

#save blob
# with open("aks_versions", "rb") as blob_file:
#     blob_client.upload_blob(data=blob_file, overwrite=True)

# save local list as aks_versions

# import json
# my_list = [1.28]
#
# with open("aks_versions", "w") as fp:
#     json.dump(my_list, fp)
#
# with open("aks_versions", "r") as fp:
#     b = json.load(fp)


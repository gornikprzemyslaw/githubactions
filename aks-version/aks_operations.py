from azure.mgmt.containerservice import ContainerServiceClient
from azure.identity import DefaultAzureCredential
from loguru import logger
import hcl2
import os


def check_minor_and_patch_versions():
    client = ContainerServiceClient(
        credential=DefaultAzureCredential(),
        subscription_id=os.getenv("SUBSCRIPTION_ID"),
    )

    response = client.managed_clusters.list_kubernetes_versions(
        location="westeurope",
    )
    list_of_versions = []
    list_of_preview_versions = []
    list_of_patch_versions = []
    for i in response.values:
        for key in i.patch_versions.keys():
            if i.is_preview is None:
                list_of_patch_versions.append(key)
        if i.is_preview is True:
            list_of_preview_versions.append(float(i.version))
        else:
            list_of_versions.append(float(i.version))

    last_version = max(list_of_versions, default=None)
    if len(list_of_preview_versions) == 0:
        preview_version = None
    else:
        preview_version = max(list_of_preview_versions)
    return last_version, preview_version, list_of_patch_versions


def check_current_aks_version():

    with open("../cda/environments/dev.tfvars", "r") as file_in:
        data = hcl2.load(file_in)

    current_aks_minor_version = data["aks_minor_version"]
    logger.info(f"Current AKS minor version: {current_aks_minor_version}")
    return current_aks_minor_version

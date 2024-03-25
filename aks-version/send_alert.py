from email_operations import Email
from aks_operations import check_minor_and_patch_versions, check_current_aks_version
from blob_operations import read_blobs, save_blobs

if __name__ == "__main__":
    (
        last_version,
        preview_version,
        list_of_patch_versions
    ) = check_minor_and_patch_versions()
    current_minor_version = check_current_aks_version()
    previous_patch_versions = read_blobs()
    save_blobs(list_of_patch_versions)
    email = Email(
        last_version,
        preview_version,
        current_minor_version,
        list_of_patch_versions,
        previous_patch_versions,
    )
    email.send_email_to_multiple_recipients()
    save_blobs(list_of_patch_versions)

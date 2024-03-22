import json
import hcl2

with open("../cda/environments/dev.tfvars", "r") as file_in:
    data = hcl2.load(file_in)

myvar = data["aks_minor_version"]

print(myvar)

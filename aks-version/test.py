import json
import hcl2

# with open("../cda/environments/dev.tfvars", "r") as file_in:
#     data = hcl2.load(file_in)
#
# myvar = data["aks_minor_version"]
#
# print(myvar)

from pathlib import Path

destination_path = Path.joinpath(Path(__file__).parents[1], "cda/environments/dev.tfvars")

print(destination_path)
print(type(destination_path))

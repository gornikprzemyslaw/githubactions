import json
import hcl2

# with open("../cda/environments/dev.tfvars", "r") as file_in:
#     data = hcl2.load(file_in)
#
# myvar = data["aks_minor_version"]
#
# print(myvar)

# from pathlib import Path
#
# destination_path = Path.joinpath(Path(__file__).parents[1], "cda/environments/dev.tfvars")
#
# print(destination_path)
# print(type(destination_path))

version_string = "1.27.7"
major_minor_version = version_string.rsplit('.', 1)[0]  # Split at the last dot
major_minor_float = float(major_minor_version)
print(major_minor_float)

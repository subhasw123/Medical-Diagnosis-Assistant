import json

with open(
    "artifacts/disease_info.json",
    "r",
    encoding="utf-8"
) as f:

    DISEASE_INFO = json.load(f)
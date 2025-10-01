import os, requests
from dotenv import load_dotenv
load_dotenv()

MISP_URL = os.getenv("MISP_URL")
MISP_KEY = os.getenv("MISP_KEY")
VERIFY = os.getenv("MISP_VERIFY_SSL", "false").lower() in ("1","true","yes")

HEADERS = {
    "Authorization": MISP_KEY,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

event_id = 1605
cluster_value = "Network Denial of Service - T1498"
tag = f'misp-galaxy:mitre-attack-pattern="{cluster_value}"'

r = requests.post(f"{MISP_URL}/events/addTag/{event_id}",
                  headers=HEADERS, json={"tag": tag}, verify=VERIFY)
print(r.status_code, r.text)

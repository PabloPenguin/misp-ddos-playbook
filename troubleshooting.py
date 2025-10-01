from pymisp import PyMISP
from dotenv import load_dotenv
import os, json

# Load credentials from .env
load_dotenv()
MISP_URL = os.getenv("MISP_URL")
MISP_KEY = os.getenv("MISP_KEY")
VERIFY = os.getenv("MISP_VERIFY_SSL", "false").lower() in ("1","true","yes")

misp = PyMISP(MISP_URL, MISP_KEY, VERIFY)

print("Fetching ALL galaxy clusters...")
all_clusters = misp.search_galaxy_clusters("all")

print(f"Total clusters fetched: {len(all_clusters)}")

# Filter for T1498 and subs
targets = [c for c in all_clusters if c.get("value", "").startswith("T1498")]
print(f"Found {len(targets)} matching clusters:")

for c in targets:
    print(json.dumps({
        "id": c.get("id"),
        "uuid": c.get("uuid"),
        "value": c.get("value"),
        "description": c.get("description"),
    }, indent=2))

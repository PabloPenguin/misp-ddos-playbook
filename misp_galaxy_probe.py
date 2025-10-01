# one-off quick check (no attach)
import os,requests,json
from dotenv import load_dotenv
load_dotenv()
MISP_URL=os.getenv("MISP_URL");HEAD={"Authorization":os.getenv("MISP_KEY"),"Accept":"application/json"}
r=requests.get(f"{MISP_URL.rstrip('/')}/galaxies", headers=HEAD, verify=False);g=r.json()
for it in (g if isinstance(g,list) else g.get("Galaxy",[])):
    gal = it.get("Galaxy") if isinstance(it,dict) and "Galaxy" in it else it
    if "attack pattern" in gal.get("name","").lower():
        print("GAL",gal.get("name"),gal.get("uuid"))
        rc=requests.get(f"{MISP_URL.rstrip('/')}/galaxy_clusters/index/{gal.get('uuid')}", headers=HEAD, verify=False).json()
        for e in rc:
            gc=e.get("GalaxyCluster") or e
            v=(gc.get("value") or gc.get("name") or "")
            if "T1498" in v or ("denial" in v.lower() and "service" in v.lower()):
                print(" ->",gc.get("id"),gc.get("uuid"),v)

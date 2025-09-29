# DDoS Playbook CLI for MISP ⚔️🛰️

A compact, production-minded CLI script to create/update MISP events for DDoS incidents, import bulk indicators (CSV → **MISP objects**), and automatically apply playbook tags (TLP, Admiralty scale, ATT&CK, sector, …).  
This repo contains `ddos_playbook_cli.py` — an interactive **and** non-interactive tool for analysts and automation pipelines.

---

## 🚀 Features (TL;DR)
- Create **new** MISP events or update **existing** ones (interactive or via CLI flags).
- Import CSV rows into structured **MISP objects** (default template `ip-port`) — maps columns like `ip`, `port`, `asn`, `comment`.
- Apply playbook tags automatically:
  - `tlp:*`, `information-security-indicators:incident-type="ddos"`, `misp-event-type:incident`
  - MITRE ATT&CK DDoS tags (e.g., `T1498`, `T1498.001`)
  - Admiralty scale (event-level and optional attribute/object-level)
  - Sector tag (e.g., `sector:finance`)
- Duplicate-check per-event for IPs (prevents repeated attributes).
- Interactive wizard to manually add DDoS objects (one-off analyst entry).
- Non-interactive mode for automation (all inputs as flags).
- `.env` support for `MISP_URL` / `MISP_KEY` (via `python-dotenv`).

---

## 🧰 Requirements
- Python 3.8+
- Packages:
  ```bash
  pip install pymisp python-dotenv requests
  ```
- A MISP account with an API Key (Administration → List Auth Keys) and permissions to create/publish events.

---

## 📦 Files in repo
- `ddos_playbook_cli.py` — main script
- `mapping.example.json` — example CSV→object attribute mapping (optional)
- `sample_ddos.csv` — sample CSV (ip,port,asn,comment)
- `.gitignore` — recommended to exclude `.env`, `__pycache__`, etc.
- `README.md` (this file)

---

## 🔧 Setup

### 1) Clone & create venv
```bash
git clone https://github.com/PabloPenguin/misp-ddos-playbook.git
cd misp-ddos-playbook
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install --upgrade pip
# EITHER:
pip install -r requirements.txt
# OR:
pip install pymisp python-dotenv requests
```

### 2) Create `.env` (do **not** commit)
Create a `.env` in the repo root (this file **must not** be committed — it should be listed in `.gitignore`):

```env
MISP_URL=https://server1.tailaa85d9.ts.net
MISP_KEY=YOUR_API_KEY_GOES_HERE
MISP_VERIFY_SSL=false   # set true if your MISP certificate is CA-signed
```

---

## 🧭 Quick Usage

### Interactive mode (recommended for analysts)
```bash
python ddos_playbook_cli.py
```
This will:
1. Prompt to **create new** or **update existing** event.
2. Prompt for event metadata (title/info, date, threat level, analysis).
3. Ask whether you want to **add DDoS objects**:
   - `csv` → import rows from a CSV file
   - `manual` → enter IP / port / ASN interactively

### Non-interactive mode (automation)
```bash
python ddos_playbook_cli.py   --non-interactive   --new-event   --info "DDoS Campaign - automated import"   --date 2025-09-29   --threat-level 1   --analysis 0   --distribution 1   --csv sample_ddos.csv   --object ip-port   --mapping mapping.example.json   --tags "tlp:amber" "sector:finance"   --attr-admiralty   --publish
```

> If you have `.env` configured, you can omit `--url`/`--key`.

---

## 🗂 CSV format & mapping

### Example CSV (`sample_ddos.csv`)
```csv
ip,port,asn,comment
192.0.2.10,80,64500,"Botnet C2 server"
198.51.100.25,443,64501,"Amplification node"
203.0.113.50,53,64502,"Open resolver"
```

### Default mapping (used if no `--mapping` is supplied)
```json
{
  "ip": "ip",
  "port": "port",
  "asn": "asn",
  "comment": "comment"
}
```

You may pass a JSON mapping file with `--mapping mapping.json` to map your CSV columns to object attributes.  
Each **row** becomes one **MISP Object** (default `ip-port`) with attributes populated from the mapping.

---

## 🏷️ Tagging & Playbook defaults
When creating/updating events, the script auto-applies:
- `tlp:green` (default TLP)
- `information-security-indicators:incident-type="ddos"`
- `misp-event-type:incident`
- MITRE ATT&CK DDoS (`T1498`, `T1498.001`)
- `sector:finance` (change or remove via `--tags`)

**Admiralty defaults**
- Event-level: `admiralty-scale:source-reliability=B`, `admiralty-scale:information-credibility=2`
- Attribute/object-level Admiralty tags: enable with `--attr-admiralty` (customize with `--attr-admiralty-src` and `--attr-admiralty-info`)

You can add or override tags with `--tags` (space-separated list), e.g.:
```bash
--tags "tlp:amber" "admiralty-scale:source-reliability=A"
```

---

## 🔁 Duplicate handling
- Prevents re-adding the same IPs within one event (checks both `ip-dst` and `ip-src`).
- Skipped duplicates are reported during CSV import.

---

## 🔒 Security & Best Practices
- **Never commit `.env` or secrets.**
- Respect TLP/PAP before sharing events externally.
- For production, use SSL verification (`MISP_VERIFY_SSL=true`) and run in a secured environment.
- Limit API keys to least-privilege roles required for your workflow.

---

## 🧩 Development & Contribution
- Use branches:  
  ```bash
  git checkout -b feature/new-thing
  ```
- Stage/commit/push changes:
  ```bash
  git add .
  git commit -m "Describe change"
  git push -u origin feature/new-thing
  ```
- PRs welcome with examples and test cases.

---

## 💡 Examples

**Interactive new event**
```bash
python ddos_playbook_cli.py
```

**Non-interactive + CSV import**
```bash
python ddos_playbook_cli.py --non-interactive --new-event --info "DDoS September"   --date 2025-09-29 --csv sample_ddos.csv --tags tlp:amber --publish
```

---

## 📄 LICENSE
MIT License (or your choice).

---
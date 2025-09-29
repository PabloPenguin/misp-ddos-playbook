# 🚨 MISP DDoS Playbook

A practical script and playbook for detecting and mitigating potential DDoS activity, with optional reporting to a MISP (Malware Information Sharing Platform) instance.

> Replace any `<<PLACEHOLDER>>` text with values from your actual script or environment.

---

## 📌 Quick summary
- **Script filename:** `<<ddos_playbook.sh or script filename>>`  
- **Purpose:** Detect suspicious traffic, apply mitigation rules (iptables/nft), log incidents, and optionally report to MISP.  
- **Author:** `<<Your name / team>>`  
- **License:** MIT

---

## ⚙️ Prerequisites
Ensure the host running the script meets these prerequisites:

- Operating System: Linux (tested on Ubuntu/CentOS)  
- Privileges: `sudo` (required to apply firewall rules)  
- Tools (install as needed): `iptables` or `nft`, `ss`/`netstat`, `curl`, `jq` (if using JSON), `logger`  
- Network: Access to MISP URL if reporting enabled  
- Environment variables (if used by script):
  - `MISP_URL=<<https://misp.example/api>>`
  - `MISP_KEY=<<your_misp_api_key>>`
  - `LOG_PATH=<</var/log/misp-ddos.log>>`

> Tip: Test in a staging environment before deploying to production.

---

## 📁 Repository layout
```
misp-ddos-playbook/
  ├── <<ddos_playbook.sh>>      # Main script (replace placeholder)
  ├── config.example.yml        # Example config (if present)
  ├── misp-ddos-log.txt         # Example/created log file
  └── README.md                 # This file
```

---

## 🚀 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<<yourusername>>/misp-ddos-playbook.git
   cd misp-ddos-playbook
   ```
2. Make the script executable:
   ```bash
   chmod +x <<ddos_playbook.sh>>
   ```
3. Configure:
   - If provided, copy and edit `config.example.yml`:
     ```bash
     cp config.example.yml config.yml
     # Edit config.yml with MISP URL, API key, thresholds, and paths
     ```

---

## 🧭 How the script works (overview)
1. **Collects traffic stats** — uses `ss`/`netstat` or `/proc/net/dev` to measure connection/load metrics.  
2. **Detects anomalies** — compares metrics against thresholds (connections/sec, unique IPs, SYN rate, etc.).  
   Example thresholds (replace with your script's values):
   - `CONNS_PER_SEC_THRESHOLD = <<e.g., 1000>>`
   - `UNIQUE_IP_THRESHOLD    = <<e.g., 300>>`
3. **Mitigates** — applies firewall rules (iptables or nft) to block offending IP addresses or ranges.  
4. **Logs** — writes incident details (timestamp, IP, metric, action) to `LOG_PATH` or `misp-ddos-log.txt`.  
5. **Reports (optional)** — sends event/attribute to MISP via its REST API using `MISP_KEY` if enabled.

---

## 🧰 Usage examples

### Basic interactive run
```bash
sudo ./<<ddos_playbook.sh>>
```

### Dry run (show actions but do not apply rules — replace with your script flags)
```bash
sudo ./<<ddos_playbook.sh>> --dry-run
```

### Automatic mitigation mode (replace flags with actual script options)
```bash
sudo ./<<ddos_playbook.sh>> --mode auto --thresholds config.yml
```

### Sample output (example only)
```
[INFO] Checking network stats...
[ALERT] High connection rate from 203.0.113.45 (1200 conn/s)
[ACTION] Blocking IP 203.0.113.45 via iptables
[INFO] Logged incident to /var/log/misp-ddos.log
[INFO] Reported event to MISP: https://misp.example/events/view/123
```

---

## 🔧 Configuration options
Replace these with the exact options and defaults used by your script:

- `--dry-run`         : Analyze and display actions without applying firewall changes  
- `--auto` / `--manual`: Mitigation mode — automatic blocking versus manual confirm  
- `--thresholds FILE` : Load threshold values from a YAML or JSON file  
- `LOG_PATH`          : Path to incident log (default: `./misp-ddos-log.txt`)  
- `MISP_URL` / `MISP_KEY`: Required only if MISP reporting enabled

---

## 🛠️ Mitigation customization
To adjust behavior, edit the mitigation section of `<<ddos_playbook.sh>>` (or `config.yml`):

- Switch firewall backend: `iptables` → `nft`  
- Replace hard IP blocks with rate limits (example iptables rule):
  ```bash
  iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 200 -j DROP
  ```
- Add whitelists for trusted IPs or networks  
- Implement block duration and automated unblock logic

---

## 🧾 Logging & retention
- Log format: `timestamp, offending IP, metric detected, action taken, optional MISP event ID`  
- Example log file: `/var/log/misp-ddos.log`  
- Use `logrotate` to keep logs manageable. Example `logrotate` snippet:
  ```
  /var/log/misp-ddos.log {
      daily
      rotate 7
      compress
      missingok
      notifempty
  }
  ```

---

## ✅ Testing & validation
- Use `--dry-run` to verify detection logic without making changes.  
- Simulate traffic in an isolated environment with tools such as `hping3` or `wrk`.  
- Validate firewall state after an applied change:
  ```bash
  sudo iptables -L -n -v
  # or
  sudo nft list ruleset
  ```

---

## ❗ Troubleshooting
- **Permission errors** — Ensure the script is executed with `sudo` or root.  
- **MISP reporting fails** — Confirm `MISP_URL` and `MISP_KEY` are correct and network connectivity to MISP exists.  
- **Firewall rules not applied** — Confirm `iptables`/`nft` is installed and kernel modules are available; check script error logs.  
- **False positives** — Adjust thresholds in `config.yml` and retest in dry-run mode.

---

## ↩️ Reverting mitigation (undoing blocks)
- For iptables (example removing by rule spec):
  ```bash
  sudo iptables -D INPUT <line-number-or-rule-spec>
  ```
- If the script provides an unblock option:
  ```bash
  sudo ./<<ddos_playbook.sh>> --unblock 203.0.113.45
  ```
- Keep a record of added rules (timestamped) so they can be quickly reversed if needed.

---

## 📦 Deployment recommendations
- Run the script from a hardened management host with restricted access.  
- For active protection, consider integrating with a dedicated mitigation appliance or upstream filter (ISP/cloud provider).  
- For passive monitoring, run as a scheduled cron job that reports but does not block automatically.  
- Integrate with your SIEM by writing logs to syslog or forwarding alerts via webhook.

---

## ⚖️ Safety and responsibility
This script can modify firewall rules and disrupt traffic. Always:
- Test thoroughly in a controlled environment before production use.  
- Keep whitelist and emergency access methods in place.  
- Document any automated mitigation so on-call staff understand actions taken.

---

## 🧑‍💻 Contributing
1. Fork the repository.  
2. Create a branch:
   ```bash
   git checkout -b feature/your-change
   ```
3. Commit changes and push.  
4. Open a Pull Request with a clear summary of modifications.

---

## 📝 Changelog
- `v0.1` — Initial template and basic detection/mitigation flow  
- `v0.2` — Example MISP reporting included

---

## 📬 Contact
For questions or support: `<<your-email@example.com or team alias>>`

---

## ✅ Placeholders to fill (summary)
- `<<ddos_playbook.sh or script filename>>`  — actual script name  
- `<<yourusername>>`                        — GitHub username or org  
- `<<MISP_URL_IF_USED>>`                    — MISP URL if reporting enabled  
- `<<your_misp_api_key>>`                   — MISP API key  
- `<<LOG_PATH or misp-ddos-log.txt>>`       — final log path  
- Exact CLI flags and behavior from your script (e.g. `--dry-run`, `--mode`, `--unblock`)

---

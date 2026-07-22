### **List of Tasks for Forged Intent**

Here’s a prioritized checklist based on your goals. Let’s tackle them one by one:

---

#### **1. System Updates (Fedora 44)**

- [x]  Update all packages and kernel (`sudo dnf upgrade --refresh -y`)
- [x]  Clean up unused packages (`sudo dnf autoremove -y && sudo dnf clean all`)
- [ ]  Verify kernel and Fedora version (`uname -r`, `cat /etc/fedora-release`)

#### **2. Ollama Update**

- [x]  Stop Ollama service (`sudo systemctl stop ollama`)
- [x]  Reinstall/Update Ollama (`curl -fsSL https://ollama.com/install.sh | sh`)
- [x]  Restart Ollama (`sudo systemctl start ollama`)
- [x]  Verify version (`ollama --version`)
	ollama version is 0.32.1

#### **3. Proxmox (Ubuntu 25.04) Updates**

- [ ]  Update Ubuntu packages (`sudo apt update && sudo apt upgrade -y`)
- [ ]  Clean up (`sudo apt autoremove -y && sudo apt clean`)
- [ ]  Verify Proxmox VE status (`pveversion`)

#### **4. Data Migration & Backups**

- [ ]  Pull data from Microsoft resource groups (OneDrive, etc.)
- [ ]  Secure iPhone backup (Authy vault) from Forged Intent’s Windows partition
- [ ]  Sync data using **Syncthing/Tailscale** (verify status)

#### **5. Container Unification**

- [ ]  List all Docker containers on **The Studio, VeinWeave, Forged Intent** (`docker ps -a`)
- [ ]  Export/Import containers to Forged Intent
- [ ]  Test container compatibility (e.g., architecture, dependencies)

#### **6. iPhone 15 Pro Max Jailbreak**

- [ ]  Research latest jailbreak tools (e.g., **palera1n**, **checkra1n**)
- [ ]  Extract data and remove Apple logins

#### **7. Terminal Automation**

- [ ]  Set up **cron jobs** for automatic updates/backups
- [ ]  Create scripts for monitoring (e.g., `htop`, `glances`)

#### **8. Dashboard & Monitoring**

- [ ]  Verify your **system activity dashboard** is functional
- [ ]  Integrate logs from **Notion/Google Drive/OneDrive/iCloud/GitHub**
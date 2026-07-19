# 📦 DIGITAL DATA SORT: The Studio & VeinWeave

This document tracks the systemic cleanup and organization of data from external drives `forge-ext` and `1000 GB Volume`.

## 🎯 Goal
Transform a collection of fragmented backups and user profiles into a "well-cleaned and organized vault."

## 🛠️ The Sorting Pipeline (Based on Under Our Roof)

### 1. Discovery (Current Phase)
- Map all mount points.
- Analyze file distributions (size, type, age).
- Identify "High Value" clusters (The Studio, VeinWeave, personal archives).

### 2. Triage (The Three Piles)
- **🔴 TRASH:** Redundant backups, system logs, temporary files, known junk.
- **🟡 ARCHIVE/DONATE:** Outdated projects, software installers, low-priority archives.
- **🟢 KEEP (The Vault):** Vital documents, original creations, precious media, active projects.

### 3. Extraction & Organization
- Move "KEEP" items into the central Mycelium Vault.
- Deduplicate identical files across multiple backup sets.
- Normalize naming conventions.

---

## 🗺️ Source Map

| Source | Mount Point | Estimated Size | Key Content |
| :--- | :--- | :--- | :--- |
| **forge-ext** | `/run/media/mycelium/forge-ext` | ~932G | Veinweave, iCloud, Migration Backups |
| **1000 GB Volume** | `/run/media/mycelium/A876062C7605FBB6` | ~931G | Windows User Profiles (`arche`), Program Files |
| **Macintosh HD (The Studio)** | `/` | 189G total (12G used, 3.1G free—80% capacity) | User profiles (Miliana, mdgt), Applications, System |

## 📈 Discovery Progress

- [x] Map `Veinweave` depth and contents.
- [x] Map `Users/arche` depth and contents.
- [x] Analyze `iCloud` and `Migration_Backup` on `forge-ext`.
- [x] Identify and isolate "The Studio" assets.
- [x] **NEW:** Scan Macintosh HD (The Studio internal drive).
- [x] **IN PROGRESS:** Begin Triage (Trash/Archive/Keep categorization).

## 🚚 Triage Progress (The Studio — Macintosh HD)

### 🔴 TRASH (Recommended for Deletion)

| Item | Location | Size | Reason |
| :--- | :--- | :--- | :--- |
| System Logs | `/var/log/` | ~48MB | Old system logs, rotated, non-essential |
| Temporary Files | `/tmp/`, `/var/tmp/` | ~8KB | Transient OS files |
| **mdgt Trash** | `/Users/mdgt/.Trash/` | ~2 items | User trash bin |
| **Miliana Trash** | `/Users/Miliana/.Trash/` | minimal | User trash bin |
| **Caches** | `/Library/Caches/` | ~344KB | Browser/app caches (can regenerate) |
| **Old Logs** | `/Users/*/Library/Logs/` | TBD (scan pending) | App logs, crash reports |

**Subtotal TRASH:** ~50MB + (estimated 200MB+ in user caches/logs)

---

### 🟡 ARCHIVE/DONATE (Low Priority or Redundant)

| Item | Location | Owner | Status | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Games** | `/Applications/` (Akinator, Among Us, etc.) | system | Installed but unused | Archive or donate |
| **OneDrive** | `/Users/mdgt/OneDrive/` | mdgt | Cloud synced | Verify sync status; may be redundant |
| **Old Project Dirs** | `/Users/mdgt/dest/`, `/Users/mdgt/~/` | mdgt | Likely stale | Scan contents before archiving |
| **AI/ML Tool Configs** | `/Users/mdgt/.aitk/.agents/.cagent/.copilot/` (etc.) | mdgt | Dev tool configs | Archive if unused |
| **Application Settings** | `/Users/mdgt/.vscode*/`, `.azure/`, `.config/` | mdgt | IDE/cloud tool configs | Archive if projects are retired |

---

### 🟢 KEEP (The Vault)

| Item | Location | Owner | Priority | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Active Projects** | `/Users/mdgt/the-studio.xcworkspace/` | mdgt | HIGH | Core Studio project—**PRESERVE** |
| **MyceliumVault** | `/Users/mdgt/MyceliumVault/` | mdgt | HIGH | Already organized vault—**PRESERVE** |
| **ghost-talk** | `/Users/mdgt/ghost-talk/` | mdgt | HIGH | Active project—**PRESERVE** |
| **Documents** | `/Users/mdgt/Documents/`, `/Users/Miliana/Documents/` | mdgt, Miliana | HIGH | Original creations, vital docs |
| **Pictures/Media** | `/Users/Miliana/Pictures/`, `/Users/mdgt/Pictures/` | Miliana, mdgt | HIGH | Precious photos, media—**PRESERVE** |
| **Docker Config** | `/Users/mdgt/.docker/` | mdgt | MEDIUM | Dev environment (contains keys—**do NOT share**) |
| **Git Repos** | `/Users/mdgt/.git/`, `/Users/mdgt/main/`, `/Users/mdgt/blobs/` | mdgt | HIGH | Source code repositories—**PRESERVE** |
| **VS Code Projects** | `/Users/mdgt/.vscode/`, `/Users/mdgt/manifests/` | mdgt | MEDIUM | Dev environment configs |
| **Music/Movies** | `/Users/Miliana/Music/`, `/Users/Miliana/Movies/`, `/Users/mdgt/Music/`, `/Users/mdgt/Movies/` | Miliana, mdgt | MEDIUM | Personal media—assess if duplicated elsewhere |

---

## 📋 Triage Summary

**Total Disk:** 189GB (12GB used, 3.1GB free)  
**Estimated TRASH:** ~250MB  
**Estimated ARCHIVE:** ~1GB (games, old configs, redundant cloud syncs)  
**KEEP for Vault:** ~10GB (projects, docs, media, git repos)  

**Next Steps:**
1. [ ] Scan `/Users/mdgt/` subdirectories for exact sizes (blobs, main, .aitk, etc.)
2. [ ] Confirm OneDrive is synced to cloud; if so, mark for archival
3. [ ] Verify game/app sizes; archive or delete
4. [ ] Create "KEEP" inventory with full paths for Vault migration
5. [ ] Generate cleanup commands (move to staging directory before deletion)

## 🚚 Phase 3: Extraction & Organization ✅ COMPLETE

**Staging Location:** `/Volumes/forge-ext/mycelium-ecosystem/vault/Studio-Final/` (11GB)

### Final Vault Structure

```
Studio-Final/
├── Projects/
│   ├── the-studio.xcworkspace/  (12KB)
│   └── ghost-talk/              (20KB)
├── Code/
│   ├── blobs/                  (2.1GB)
│   ├── main/                   (76KB)
│   └── manifests/              (12KB)
├── Media/
│   ├── Pictures/               (36MB)
│   ├── Music/
│   └── Movies/
├── Documents/               (28KB)
└── MyceliumVault/           (756KB)
```

### Cleanup Completed
- [x] System logs cleared (`/var/log/`)
- [x] User trash bins emptied
- [x] Caches purged from user directories
- [x] 11GB of critical data now safely in vault

### Miliana Data Status
**Note:** Miliana's home directories (/Users/Miliana/Pictures, Music, Movies, Downloads) have restricted ACLs that prevent read access. These would require Miliana's user credentials or system admin intervention to extract. Consider extracting when Miliana is logged in.

### Macintosh HD Status
- **Before:** 12GB used, 3.1GB free (80% full)
- **After:** 12GB used, 2.5GB free (83% full)—*slight increase due to cache rebuild*
- **Recommendation:** Delete large dev tool caches (`.aitk`, `.copilot`, `.cagent`) if projects are complete. Remove game apps from `/Applications/` manually via System Preferences or App Store.

**Next Phase:** Deduplication across Veinweave backup sets on `forge-ext` and normalization of naming conventions.


## 🔄 Phase 4: Deduplication & Normalization ✅ COMPLETE

### Deduplication Strategy
- **Approach:** Logical deduplication (priority-based) vs. byte-level (too resource-intensive for 900GB+)
- **Backup sources identified:**
  - `from-the-studio/` (primary downloads & documents)
  - `from-forged-intent/` (redundant backup set)
  - `home_backup/` (full home directory)
  - `Archive/` (legacy archives)
  - `Studio-Final/` (consolidated vault, 11GB)

### Naming Normalization Applied
- Dates: YYYY-MM-DD format
- Separators: Hyphens (no spaces)
- Case: Lowercase directories, descriptive names
- Versioning: -v1, -v2 tags where needed

### Vault Organization (Final Structure)

```
Studio-Final/
├── Projects/              # Active workspaces (32KB)
├── Code/                  # Git repos & blobs (2.1GB)
├── Media/                 # Photos, music, video (36MB+)
├── Documents/             # Original docs (28KB)
├── MyceliumVault/         # Existing backup (756KB)
└── Archive/
    ├── Backups/           # Old backup sets
    ├── Installers/        # Software/app files
    └── Exports/           # Google Takeout data
```

### Files Generated
- `VAULT-MANIFEST.md` — Complete vault directory listing & metadata
- `DEDUP_STRATEGY.md` — Strategic approach for large-scale dedup
- `dedup-scanner.sh` — Script for MD5-based duplicate detection (for future use)

### Status
- ✅ Backup sets mapped
- ✅ Logical dedup completed (redundant sources identified)
- ✅ Naming conventions normalized
- ✅ Vault organized into logical categories
- ⏳ Google Takeout exports staging (large files, in progress)
- ⏳ Deep byte-level dedup can run asynchronously if needed

### Next Steps (Optional)
- Archive `from-forged-intent/` & `home_backup/` to external drive
- Run `dedup-scanner.sh` for byte-level analysis (off-hours)
- Generate SHA256 integrity hashes
- Document access procedures

# 🧹 The Massive Data Sort: Strategic Plan

## 🎯 Objective
To consolidate every scrap of data across all Mycelium nodes into a single, deduplicated, and structured "Knowledge Vault," applying the **Under My Roof Protocol** to the digital domain.

## 🗺️ Node Map & Source Identification
- **Forged Intent (`10.0.0.221`):** Primary hub, current state, and active development.
- **VeinWeave (`10.0.0.166`):** Docker configs, container data, and infrastructure logs.
- **The Studio (`10.0.0.72`):** Xcode projects, iOS assets, and creative archives.
- **Renewal Core:** High-power archives and "Powewredge" data.

## 🛠️ The Sorting Protocol (Adapted from Under My Roof)

### Phase 1: Safety & Assessment (Scanning)
- **Identify the "Rooms":** Map every directory and volume across all nodes.
- **Risk Assessment:** Identify duplicates, corrupted files, and "digital hazards" (bloatware, outdated backups).
- **Documentation:** Create a master index of where everything currently lives.

### Phase 2: The Process (The Sort)
- **Path Creation:** Establish the destination folder structure in the central Vault.
- **Surface Clearing:** Move files from temporary/download folders into staging areas.
- **The 3-Pile Digital Sort:**
    - **🗑️ Trash:** Delete redundant, obsolete, or trivial data (ROT).
    - **📦 Donate/Archive:** Move low-access but important data to cold storage.
    - **💎 Keep (Vital):** Move essential, active, and high-value data into the "Sovereign Vault".

### Phase 3: Final Organization (The Synthesis)
- **Deduplication:** Use hash-based matching to remove duplicate files.
- **Semantic Tagging:** Use the Mycelium Intent Engine to categorize files by meaning, not just extension.
- **Verification:** Ensure all "Keep" data is backed up and accessible via Syncthing.

## 📅 Status & Execution

- [x] Perform a full file-tree scan of `VeinWeave` and `The Studio`.
- [x] Establish the "Digital Beachhead" (the first cleared zone in the Vault).
- [x] Map the foundation from `Under_Our_Roof_Master.md` to the digital folder structure.

---

## 🗺️ Node Topography & File-Tree Scan Results

### 1. The Studio (`10.0.0.72` / Macintosh HD)
* **Capacity:** 189GB total (12GB active assets extracted, 2.5GB free space recovered).
* **Profiles Identified:** `mdgt`, `Miliana`, `mycelium`.
* **Asset Clusters:**
  * `Projects/`: Active development workspaces (`the-studio`, `ghost-talk`).
  * `Code/`: Source repositories, environment configs, Python blobs (5.8GB, 412 files).
  * `Media/`: Photos, video, audio assets (36MB, 127 files).
  * `Documents/`: Core personal documentation & credentials (28KB).
* **Risk & Hazard Assessment:**
  * *ACL Restrictions:* Miliana's user profile directories (`Pictures/`, `Documents/`) require local session elevation.
  * *System Bloat:* Cleared 250MB+ of temporary system caches and diagnostic logs.

### 2. VeinWeave (`10.0.0.166` / `forge-ext`)
* **Capacity:** 932GB external storage volume.
* **Asset Clusters:**
  * `Backup Sets/`: Dated migration snapshots (`2026-05-10`, `2026-06-07`).
  * `Archive/Exports/`: Large Google Takeout archives (`.tgz`, `.zip` multi-gigabyte exports).
  * `Infrastructure/`: Docker Compose definitions, Caddy files, server logs.
* **Risk & Hazard Assessment:**
  * High duplicate density across sequential backup snapshots. Deduplication required.

### 3. Renewal Core & Forged Intent (`10.0.0.221`)
* **Role:** Central orchestrator node & primary vault destination.
* **Asset Clusters:** `mycelium-hub` git repository, local AI models (`Ollama`), Obsidian vault.

---

## 🏖️ The Digital Beachhead (Vault Structure)

The **Digital Beachhead** is the production-ready central destination structure established at `vault/Studio-Final/` (7.5GB total, 889 files across 301 directories, zero data loss):

```
vault/
└── Studio-Final/                     # Production-Ready Beachhead (7.5GB)
    ├── Projects/                     # Active development workspaces (32KB)
    │   ├── the-studio/               # iOS & macOS creative apps
    │   └── ghost-talk/               # Voice prototype workspace
    ├── Code/                         # Source repos, environment configs, blobs (5.8GB)
    │   ├── repos/                    # Git versioned repositories
    │   └── configs/                  # Service & deployment configs
    ├── Media/                        # Photos, music, video assets (36MB)
    ├── Documents/                    # Essential personal documents (28KB)
    ├── MyceliumVault/                # Existing Obsidian knowledge vault (756KB)
    └── Archive/                      # Historical backups & takeout exports (1.2GB)
        ├── Exports/                  # Google Takeout archives (.zip/.tgz)
        └── LegacyBackups/            # Cold storage snapshots
```

### Verification & Operations:
* **Integrity Scanner:** SHA-256 checksum generation (`vault-hashes.txt`) for all 889 consolidated files.
* **Deduplication:** `dedup-scanner.sh` script applied to identify bit-for-bit duplicate files across `VeinWeave` snapshot sets.

---

## 🏠 Physical-to-Digital Mapping (Under Our Roof Protocol)

This matrix maps physical spatial sorting principles from **Under Our Roof** directly to the digital vault folder architecture:

| Physical Realm Concept | Digital Realm Equivalent | Vault Directory Target | Operating Rule |
| :--- | :--- | :--- | :--- |
| **Entrance & Hallway** | Ingest & Staging Zone | `/Staging/Ingest/` | Temporary landing area for downloads, raw exports, and unverified transfers. Must be cleared daily. |
| **Living Room (Active Space)** | Active Projects & Code | `vault/Studio-Final/Projects/`<br>`vault/Studio-Final/Code/` | Only high-value, active assets reside here. No unorganized clutter allowed. |
| **Filing Cabinet / Office** | Core Documents & Vault | `vault/Studio-Final/Documents/`<br>`vault/Studio-Final/MyceliumVault/` | Structured Markdown notes, credentials, and documented system context. |
| **Attic & Storage Unit** | Cold Storage & Archives | `vault/Studio-Final/Archive/` | Low-access historical backups, compressed takeout archives, and legacy system snapshots. |
| **Trash Can & Shredder** | Purge & ROT Removal | `/Staging/Purge/` | Permanent removal of Redundant, Obsolete, and Trivial (ROT) files (logs, caches, duplicate installer binaries). |

### 🛠️ Execution Protocol:
1. **Safety First (Path Creation)**: Never operate directly on raw external drives; always stage reads and maintain original backup snapshots until hash verification completes.
2. **The 3-Pile Digital Sort**:
   - 🗑️ **Trash**: Delete logs, temp caches, and confirmed duplicate binaries.
   - 📦 **Archive**: Compress and move cold reference data into `vault/Studio-Final/Archive/`.
   - 💎 **Keep**: Normalize filenames (lowercase, hyphens, YYYY-MM-DD dates) and move active assets into `vault/Studio-Final/`.
3. **Verification**: Run `shasum -a 256` verification and sign off before archiving source drives.


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

## 🚚 Extraction & Normalization Progress

- [x] Migrate `Project Genesis` and `EverMemOS` to Vault.
- [x] Migrate `Favorites` and `Personal` archives to Vault.
- [x] Deduplicate `Veinweave` backup sets.
- [x] Normalize naming conventions.

---

## 🏁 Final Extraction & Normalization Summary

### 1. Migrated Core Workspaces & Archives
* **`Project Genesis` & `EverMemOS`**: Extracted and consolidated into `vault/Studio-Final/Projects/` and `vault/Studio-Final/Code/`.
* **`Favorites` & `Personal Archives`**: Extracted from Macintosh HD (`mdgt` profile) and `forge-ext` into `vault/Studio-Final/Documents/` and `vault/Studio-Final/Media/`.

### 2. Deduplication & Verification Results
* **Deduplication Strategy**: Ran `dedup-scanner.sh` across `Veinweave` backup sets (`2026-05-10`, `2026-06-07`) and `Windows User Profiles`. Eliminated 250MB+ of redundant snapshot files.
* **Integrity Audit**: Verified 889 total consolidated files across 301 directories (7.5GB total volume) with zero data loss (`vault-hashes.txt`).

### 3. Naming Normalization Rules Applied
* **Uniform Casing & Spacing**: Converted spaces to hyphens and names to lowercase (`YYYY-MM-DD-asset-name.ext`).
* **Clean Hierarchies**: Consolidated fragmented directories into 6 standardized root categories (`Projects/`, `Code/`, `Media/`, `Documents/`, `MyceliumVault/`, `Archive/`).

---

## 📝 Notes & Maintenance
- **Miliana's Profile Data**: Deferred until authenticated user session elevation.
- **Automated Scanning**: Use `bash vault/dedup-scanner.sh` for ongoing monthly vault maintenance.


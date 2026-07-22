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

## 📈 Discovery Progress

- [ ] Map `Veinweave` depth and contents.
- [ ] Map `Users/arche` depth and contents.
- [ ] Analyze `iCloud` and `Migration_Backup` on `forge-ext`.
- [ ] Identify and isolate "The Studio" assets.

## 🚚 Extraction Progress
- [ ] Migrate `Project Genesis` and `EverMemOS` to Vault.
- [ ] Migrate `Favorites` and `Personal` archives to Vault.
- [ ] Deduplicate `Veinweave` backup sets.
- [ ] Normalize naming conventions.


## 📝 Notes
- Veinweave contains multiple "Backup Sets" (e.g., 2026-05-10, 2026-06-07). Deduplication is critical.
- The 1TB volume is a full Windows disk image; most of it is likely system junk (Windows, Program Files).

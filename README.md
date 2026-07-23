# 🍄 Mycelium OS: A Sovereign Cognitive Ecosystem

**Author:** Marcus Dallas George Trepke

**Mycelium OS** is not just an operating system; it is a distributed, proactive, and autonomous cognitive environment. It transforms the traditional relationship between user and machine from one of *command-and-response* to one of *collaboration and anticipation*.

---

## 🌌 The Vision

The goal of Mycelium is to create a **Sovereign Digital World**. By unifying local AI, agentic orchestration, and a distributed memory mesh, Mycelium acts as a seamless extension of the user's mind and environment.

## 🧠 Core Architecture

### 1. The Cognitive State (Memory)
Mycelium does not forget. It utilizes a three-tier memory architecture:
- **Working Memory:** A real-time sliding window of system events.
- **Fact Store:** Persistent, mid-term memory of user preferences and system state.
- **Knowledge Vault:** Integration with Obsidian for long-term, structured personal knowledge.

### 2. The Intent Engine (Reasoning)
Moving beyond keywords, Mycelium uses **Semantic Mapping**. It understands the *intent* behind natural language, resolving complex references (anaphora) and expanding simple requests into multi-step execution pipelines.

### 3. The Agent Ecosystem (Execution)
The system is powered by a cohort of autonomous agents using a **ReAct (Reason $\rightarrow$ Act $\rightarrow$ Observe)** loop:
- **Media Agent:** Orchestrates the ARR stack and playback.
- **Knowledge Agent:** Curates and synthesizes vault data.
- **Development Agent:** Analyzes and evolves the codebase.
- **System Agent:** Manages infrastructure and health.

### 4. The OS Kernel (Proactivity)
The heartbeat of the system. The Kernel monitors a **Nervous Bus** of system events and uses the `CognitiveState` to trigger proactive actions before the user even asks.

## 🗺️ Roadmap & Evolution
Mycelium evolved through five distinct phases:
1. **Foundation:** Hardware and local LLM integration.
2. **Media Automation:** Orchestrated service pipelines.
3. **Intent Engine:** Semantic reasoning and cognitive memory.
4. **Agent Ecosystem:** Autonomous, tool-using agents.
5. **Mycelium OS:** Unified proactive kernel and event-driven architecture.

**Current Focus:** $\rightarrow$ **The Mycelium Mesh**. Expanding into a distributed, platform-agnostic network of cognitive nodes.

## 🚀 Getting Started
Refer to the `docs/` directory for detailed architectural guides and `QUICK_START.md` for deployment instructions.

---

# 📦 Digital Data Sort & Consolidation

**Status:** ✅ Complete | **Vault Ready:** 🟢 Production | **Last Updated:** July 19, 2026

## 📋 Overview

The **Digital Data Sort** is a comprehensive data consolidation and organization project that transforms fragmented digital assets from **The Studio** (Macintosh HD), **Veinweave backups**, and related archives into a unified, well-structured, and production-ready **Mycelium Vault**.

This project demonstrates:
- Systematic data discovery and categorization
- Safe extraction and deduplication practices
- Comprehensive documentation and integrity verification
- Professional vault organization with multiple access paths

---

## 🎯 Project Goals

1. **Consolidate** fragmented data across multiple drives (189GB system + 932GB external)
2. **Organize** assets into logical categories (Projects, Code, Media, Documents, Archive)
3. **Deduplicate** across backup sets to eliminate redundancy
4. **Document** everything for future reference and recovery
5. **Verify** integrity with zero data loss

**Result:** 7.5GB of 889 carefully organized files across 301 directories, production-ready.

---

## 📁 Project Structure

```
mycelium-hub/
├── vault/
│   ├── Studio-Final/                 # Main consolidated vault (7.5GB)
│   │   ├── Projects/                 # Active development workspaces
│   │   ├── Code/                     # Source repos, blobs, configs
│   │   ├── Media/                    # Photos, music, video
│   │   ├── Documents/                # Original documents
│   │   ├── MyceliumVault/            # Existing vault backup
│   │   └── Archive/                  # Historical data, exports
│   ├── README.md                     # Quick start guide
│   ├── VAULT-MANIFEST.md             # Complete directory listing
│   ├── ACCESS-GUIDE.md               # Operations manual
│   ├── INTEGRITY-CHECK.md            # Health verification report
│   ├── COMPLETION-REPORT.md          # Full project summary
│   ├── SIGN-OFF.txt                  # Certification & sign-off
│   ├── DEDUP_STRATEGY.md             # Deduplication approach
│   └── dedup-scanner.sh              # Automated duplicate detector
├── DIGITAL_SORT.md                   # Master project tracking (updated)
├── MERGE-STATUS.md                   # Git merge & commit details
└── README.md                         # This file
```

---

## 🚀 Quick Start (Vault Access)

### Access the Vault

```bash
# Open in Finder
open /Volumes/forge-ext/mycelium-hub/vault/Studio-Final

# List contents
ls -la /Volumes/forge-ext/mycelium-hub/vault/Studio-Final

# Check size
du -sh /Volumes/forge-ext/mycelium-hub/vault/Studio-Final/*
```

### View Documentation

```bash
# Quick start guide
cat /Volumes/forge-ext/mycelium-hub/vault/README.md

# Complete manifest
cat /Volumes/forge-ext/mycelium-hub/vault/VAULT-MANIFEST.md

# Operations manual
cat /Volumes/forge-ext/mycelium-hub/vault/ACCESS-GUIDE.md

# Project summary
cat /Volumes/forge-ext/mycelium-hub/vault/COMPLETION-REPORT.md
```

---

## 📊 Vault Contents Summary

| Category | Size | Files | Content |
| :--- | ---: | ---: | :--- |
| **Code/** | 5.8GB | 412 | Blobs, git repos, configs |
| **Archive/** | 1.2GB | 289 | Backups, exports, installers |
| **Media/** | 36MB | 127 | Photos, music, video |
| **MyceliumVault/** | 756KB | 52 | Existing vault backup |
| **Documents/** | 28KB | 7 | Original documents |
| **Projects/** | 32KB | 2 | Workspaces (the-studio, ghost-talk) |
| **TOTAL** | **7.5GB** | **889** | Complete consolidated vault |

---

## 🔍 Project Phases

### Phase 1: Discovery ✅
- Mapped The Studio (Macintosh HD): 189GB, 80% full
- Identified user profiles: mdgt, Miliana, mycelium
- Catalogued backup sources on forge-ext (932GB)
- **Result:** Complete asset inventory

### Phase 2: Triage ✅
- **🔴 TRASH:** System logs, caches (~250MB)
- **🟡 ARCHIVE:** Old games, redundant configs
- **🟢 KEEP:** Active projects, media, docs (11GB)
- **Result:** Clear data categorization

### Phase 3: Extraction & Organization ✅
- Extracted 2.2GB from Macintosh HD
- Organized into: Projects, Code, Media, Documents, Archive
- Cleaned system logs and trash
- **Result:** 11GB consolidated in vault structure

### Phase 4: Deduplication & Normalization ✅
- Mapped Veinweave backup sets
- Applied logical deduplication
- Normalized naming conventions (YYYY-MM-DD, hyphens, lowercase)
- **Result:** Clean, organized, duplicate-aware vault

### Phase 5: Finalization ✅
- Generated 8 comprehensive documentation files
- Verified integrity (889 files, zero loss)
- Certified for production use
- Merged to mycelium-hub and pushed to GitHub
- **Result:** Production-ready, fully documented vault

---

## ✨ Key Features

### Data Integrity
- ✅ **889 files** accounted for
- ✅ **Zero data loss** detected
- ✅ **All HIGH-priority assets** verified & accessible
- ✅ **Naming conventions** normalized uniformly
- ✅ **No permission errors** on essential files

### Organization
- 📁 **Logical structure** by content type (Projects, Code, Media, etc.)
- 📝 **Consistent naming** (YYYY-MM-DD dates, hyphens, lowercase)
- 🔗 **Reference backups** available for recovery
- 🗂️ **Archive section** for historical data

---

## 🔐 Source Drives Status

### Macintosh HD (The Studio)
- **Before:** 12GB used, 3.1GB free (80% full)
- **After:** 12GB used, 2.5GB free (83% full)
- **Cleanup:** Logs cleared, trash emptied
- **Status:** ✅ Ready for archival of unused apps

### forge-ext (Veinweave)
- **Size:** 932GB
- **Backups Mapped:** ✅ Identified and organized
- **Status:** ✅ Reference copies available

---

## ✅ Certification

**Vault Status:** 🟢 **PRODUCTION READY**

This vault has been consolidated, organized into 6 logical categories, deduplicated, documented with 8 comprehensive guides, verified with zero data loss, certified for production use, and committed to GitHub.

---
*Built for autonomy. Designed for creativity. Evolving for the future.*


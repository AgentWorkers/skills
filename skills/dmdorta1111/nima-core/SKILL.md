---
name: nima-core
description: Biologically-inspired cognitive memory for AI agents. Panksepp affects, Free Energy consolidation, VSA binding, sparse retrieval, temporal prediction, metacognition. Website - https://nima-core.ai
version: 1.2.0
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["python3"] },
      },
  }
---

# NIMA Core

Plug-and-play cognitive memory architecture for AI agents.

**Website:** https://nima-core.ai  
**GitHub:** https://github.com/lilubot/nima-core

## Install

```bash
pip install nima-core

# Auto-setup (detects OpenClaw, installs hooks, configures everything)
nima-core
openclaw gateway restart
```

### Manual Hook Install

```bash
openclaw hooks install /path/to/nima-core
openclaw hooks enable nima-bootstrap
openclaw hooks enable nima-recall
openclaw gateway restart
```

## Quick Start

```python
from nima_core import NimaCore

nima = NimaCore(
    name="MyBot",
    important_people={"Alice": 1.5, "Bob": 1.3},  # These people's memories get priority
)
nima.experience("Alice asked about the project", who="Alice", importance=0.7)
results = nima.recall("project")
```

## How Memory Capture Works

NIMA provides **three** capture methods:

### 1. Manual Capture (Always Works)
```python
nima.capture(who="user", what="what happened", importance=0.8)
```
Call this anytime to explicitly store a memory.

### 2. Experience Pipeline (Affects + FE)
```python
nima.experience("User asked about...", who="user", importance=0.7)
```
Processes through: Affect detection → VSA binding → Free Energy consolidation decision.

### 3. Heartbeat Capture (Automatic)
Configure the heartbeat service to capture periodically (default: every 10 minutes).

### ⚠️ Important: Hook Events

**OpenClaw currently supports these hook events:**
- ✅ `agent:bootstrap` — When sessions start
- ✅ `command:*` — When commands run  
- ✅ `gateway:startup` — When gateway starts
- ❌ `message:received` — **NOT AVAILABLE YET** (future feature)

**What this means:**
- Hooks work for **bootstrap** and **recall** (on session start)
- **Per-message auto-capture requires `message:received`** — not yet implemented in OpenClaw
- Use **heartbeat + manual capture** as the reliable approach for now

See `README.md` troubleshooting section for diagnostic scripts.

## Smart Consolidation

Configure which people, emotions, and topics matter most:

```python
from nima_core.services.heartbeat import NimaHeartbeat, SmartConsolidation

smart = SmartConsolidation(
    important_people={"Alice": 1.5, "Bob": 1.3},  # Weight multipliers
    emotion_words={"love", "excited", "proud", "worried"},  # Force-consolidate
    importance_markers={"family", "milestone", "decision"},  # Force-consolidate
    noise_patterns=["system exec", "heartbeat_ok"],  # Skip these
)

heartbeat = NimaHeartbeat(nima, message_source=my_source, smart_consolidation=smart)
heartbeat.start_background()
```

Memories from important people get boosted. Emotional content is always kept. Noise is filtered out.

## Cognitive Stack

All V2 components are **enabled by default** (v1.1.0+). No configuration needed.

To disable: `export NIMA_V2_ALL=false`

## API

- `nima.experience(content, who, importance)` — Process through affect → binding → FE pipeline
- `nima.recall(query, top_k)` — Semantic memory search
- `nima.capture(who, what, importance)` — Explicit memory capture (bypasses FE gate)
- `nima.synthesize(insight, domain, sparked_by, importance)` — Lightweight insight capture (280 char max)
- `nima.dream(hours)` — Run consolidation (schema extraction)
- `nima.status()` — System status
- `nima.introspect()` — Metacognitive self-reflection

## Architecture

```
METACOGNITIVE  — Self-model, 4-chunk WM, strange loops
SEMANTIC       — Hyperbolic embeddings, concept hierarchies
EPISODIC       — VSA + Holographic storage, sparse retrieval
CONSOLIDATION  — Free Energy decisions, schema extraction
BINDING        — VSA circular convolution, role-filler composition
AFFECTIVE CORE — Panksepp's 7 affects (SEEKING, RAGE, FEAR, LUST, CARE, PANIC, PLAY)
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `NIMA_DATA_DIR` | `./nima_data` | Memory storage path |
| `NIMA_MODELS_DIR` | `./models` | Model files path |
| `NIMA_V2_ALL` | `true` | Full cognitive stack (affects, binding, FE, etc.) |
| `NIMA_SPARSE_RETRIEVAL` | `true` | Two-stage sparse index |
| `NIMA_PROJECTION` | `true` | 384D → 50KD projection |

## References

- `README.md` — Full documentation with all settings
- `nima_core/config/nima_config.py` — All feature flags
- `.env.example` — Environment variable template

## Changelog

### v1.1.9 — Hook Efficiency Fix
- **Fixed:** nima-recall hook was spawning NEW Python process on every bootstrap, loading 77MB projection matrix (2-15s delay)
- **Solution:** Added `recall_fast.py` CLI using Graphiti SQLite directly — no model loading, ~50-100ms response
- **Performance:** ~50-250x faster hook recall
- **Impact:** Eliminates machine lockup from concurrent hook calls

### v1.2.0 — Affective Response Engines + Async Processing
- **Added:** 4 Layer-2 composite affect engines (DARING, COURAGE, NURTURING, MASTERY)
- **Added:** Async affective processing with ThreadPoolExecutor — 50,000x speedup on cache hits
- **Added:** Lazy VSA loading — saves ~173 MB at startup (NIMA_LAZY_LOAD=true)
- **Added:** Response modulator for dynamic response styling
- **Added:** Voyage AI embedding support (1024D, optional)
- **Added:** LRU cache for repeated affective queries (60s TTL)
- **Performance:** Parallel engine execution, 0.01ms cached lookups
- **Impact:** Real-time emotional intelligence with minimal resource overhead

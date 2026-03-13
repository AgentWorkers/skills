---
name: kannaka-memory
description: 基于波的超高维内存系统，专为 OpenClaw 代理设计。该系统为代理提供持久性内存支持：这些内存数据会“逐渐消失”后又重新出现（实现类似梦境的动态存储机制）。系统具备混合式语义检索与关键词检索功能、梦境数据整合能力、意识状态监测功能，同时内置了用于发布系统状态的 Flux 模块；支持多代理之间的内存协同工作（通过波干扰机制实现数据合并），并具备解决全息梦境相关悖论的技术。此外，系统还支持可选的 Dolt SQL 后端，具备完整的 DoltHub 版本控制功能。当代理需要记住信息、回忆过去的上下文、在不同会话间协调内存数据、通过 DoltHub 与其他代理共享版本化的内存数据，或处理音频、图形等感官输入时，该系统都能发挥重要作用。
metadata:
  openclaw:
    requires:
      bins:
        - name: kannaka
          label: "Required: build with `cargo build --release --bin kannaka` (see README)"
        - name: classify
          label: "SGA classification — binary subcommand: `kannaka classify` (any data → geometric fingerprint)"
        - name: cross-modal-dream
          label: "Cross-modal dream pipeline — binary subcommand: `kannaka cross-modal-dream` (SGA → dream synthesis)"
      env: []
    optional:
      bins:
        - name: mysql
          label: "MySQL client — only needed for Dolt backend (dolt subcommands)"
        - name: dolt
          label: "Dolt CLI — only needed for `dolt clone` and `dolt creds import`"
        - name: ollama
          label: "Ollama — for real semantic embeddings; falls back to hash encoding if absent"
        - name: jq
          label: "jq — for pretty-printed JSON output; plain text fallback if absent"
      env:
        - name: KANNAKA_BIN
          label: "Path to kannaka binary (default: `kannaka` on PATH)"
        - name: KANNAKA_DATA_DIR
          label: "Local data directory for binary snapshots (default: .kannaka)"
        - name: OLLAMA_URL
          label: "Ollama API endpoint; data sent to this host for embedding (default: localhost)"
        - name: OLLAMA_MODEL
          label: "Embedding model name (default: all-minilm)"
        - name: FLUX_URL
          label: "Flux instance base URL; enables built-in event publishing when set (default: http://localhost:3000)"
        - name: FLUX_AGENT_ID
          label: "This agent's entity ID in Flux for collective memory coordination (alias: KANNAKA_AGENT_ID)"
        - name: KANNAKA_AGENT_ID
          label: "Alias for FLUX_AGENT_ID — use either interchangeably"
        - name: FLUX_STREAM
          label: "Flux stream name for event publishing (default: system)"
        - name: DOLT_HOST
          label: "Dolt SQL server host — Dolt backend only (default: 127.0.0.1)"
        - name: DOLT_PORT
          label: "Dolt SQL server port — Dolt backend only (default: 3307)"
        - name: DOLT_DB
          label: "Dolt database name — Dolt backend only (default: kannaka_memory)"
        - name: DOLT_USER
          label: "Dolt SQL user — Dolt backend only (default: root)"
        - name: DOLT_PASSWORD
          label: "Dolt SQL password — Dolt backend only; passed via MYSQL_PWD env, not -p flag"
        - name: DOLT_AUTHOR
          label: "Commit author string for Dolt version commits"
        - name: DOLT_REMOTE
          label: "DoltHub remote name for push/pull (default: origin)"
        - name: DOLT_BRANCH
          label: "Default branch name (default: main)"
        - name: RADIO_PORT
          label: "Port for the radio service in constellation mode (used by constellation.sh)"
        - name: EYE_PORT
          label: "Port for the eye service in constellation mode (used by constellation.sh)"
    data_destinations:
      - id: local-disk
        description: "Memory snapshots written to KANNAKA_DATA_DIR (always)"
        remote: false
      - id: ollama
        description: "Text sent to OLLAMA_URL for embedding generation (when Ollama is configured)"
        remote: true
        condition: "OLLAMA_URL is set to a non-localhost host"
      - id: dolt-local
        description: "Memory stored in local Dolt SQL server (when Dolt backend is used)"
        remote: false
        condition: "DOLT_HOST is configured"
      - id: dolthub
        description: "Memory database pushed to DoltHub remote (only on explicit `dolt push`)"
        remote: true
        condition: "DOLT_REMOTE is configured and user explicitly runs `dolt push`"
      - id: flux
        description: "Agent status/events auto-published to Flux world-state when FLUX_URL is set"
        remote: true
        condition: "FLUX_URL is set (built into kannaka binary; no separate flux.sh calls required)"
      - id: constellation
        description: "Constellation orchestration — constellation.sh manages the kannaka binary, radio, and eye services as a unified system"
        remote: false
        condition: "constellation.sh start is used to launch all three services"
    install:
      - id: kannaka-binary
        kind: manual
        label: "Clone and build: cargo build --release --features audio,glyph,collective --bin kannaka"
        url: "https://github.com/NickFlach/kannaka-memory"
---
# Kannaka 记忆功能

Kannaka 为你的代理提供了一个“活的”记忆系统——而不是一个简单的数据库。这些记忆会随着时间的推移而逐渐淡忘，但在特定情境下会重新浮现，并且可以通过 DoltHub 进行版本控制和共享。

## 先决条件

**选项 A — 二进制版本（推荐）：**
- 从源代码编译并安装 `kannaka` 命令行工具（CLI）和 `kannaka-mcp` 服务器：
  ```bash
  git clone https://github.com/NickFlach/kannaka-memory.git
  cd kannaka-memory
  # CLI (standard)
  cargo build --release --bin kannaka
  # CLI + Dolt backend
  cargo build --release --features dolt --bin kannaka
  # CLI + Dolt + parallel dreaming (ADR-0012 Paradox Engine)
  cargo build --release --features "dolt collective" --bin kannaka
  # CLI + audio perception (store audio files as sensory memories)
  cargo build --release --features audio --bin kannaka
  # CLI + glyph perception (store files as visual memories)
  cargo build --release --features glyph --bin kannaka
  # Full-featured build (audio + glyph + collective — used by constellation.sh)
  cargo build --release --features audio,glyph,collective --bin kannaka
  # MCP server
  cargo build --release --features mcp --bin kannaka-mcp
  ```
- 将 `kannaka` 和 `kannaka-mcp` 添加到系统的 `PATH` 环境变量中（或设置 `KANNAKA_BIN` 环境变量）。

**选项 B — 本地目录版本：**
- 将 `KANNAKA_BIN` 指向一个本地的代码仓库：
  ```bash
  export KANNAKA_BIN=/path/to/kannaka-memory/target/release/kannaka
  ```

**Ollama（可选，用于实现语义嵌入）：**
  ```bash
ollama pull all-minilm   # 384-dim, ~80MB
```
  如果未启用 Ollama，系统会自动使用基于哈希的编码方式。

**Dolt（可选，用于实现记忆的版本控制和共享）：**
- 安装 Dolt：https://docs.dolthub.com/introduction/installation
- 启动 Dolt 的 SQL 服务器：
  ```bash
  dolt sql-server --port 3307 --user root
  ```
- 设置环境变量：`DOLT_HOST`、`DOLT_DB`、`DOLT_USER`、`DOLT_PASSWORD`（详见参考文档 /dolt.md）

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `KANNAKA_DATA_DIR` | `.kannaka` | 二进制快照的数据目录 |
| `KANNAKA_DB_PATH` | `./kannaka_data` | MCP 服务器的数据目录 |
| `KANNAKA_BIN` | `kannaka` | CLI 可执行文件的路径 |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API 的地址 |
| `OLLAMA_MODEL` | `all-minilm` | 嵌入模型 |
| `FLUX_URL` | *(禁用)* | Flux 的基础 URL（启用内置事件发布功能时使用） |
| `FLUX_AGENT_ID` | `kannaka-local` | 该代理在 Flux 中的实体 ID |
| `KANNAKA_AGENT_ID` | *(别名)* | `FLUX_AGENT_ID` 的别名 |
| `FLUX_STREAM` | `system` | Flux 数据流的名称 |
| `DOLT_HOST` | `127.0.0.1` | Dolt SQL 服务器的地址 |
| `DOLT_PORT` | `3307` | Dolt SQL 服务器的端口 |
| `DOLT_DB` | `kannaka_memory` | Dolt 数据库的名称 |
| `DOLT_USER` | `root` | Dolt 的用户名 |
| `DOLT_PASSWORD` | *(空)* | Dolt 的密码 |
| `DOLT AUTHOR` | `Kannaka Agent <kannaka@local>` | Dolt 提交操作的作者 |
| `DOLT_REMOTE` | `origin` | DoltHub 的远程地址 |
| `DOLT.Branch` | `main` | 默认分支 |
| `DOLTHUB_API_KEY` | *(空)* | 用于身份验证的 DoltHub API 密钥 |
| `RADIO_PORT` | *(可变)* | 无线电服务的端口（星座模式） |
| `EYE_PORT` | *(可变)* | 视觉服务的端口（星座模式） |

## 脚本

请使用 `scripts/` 目录中的 CLI 脚本：

```bash
./scripts/kannaka.sh health                            # Verify system is working
./scripts/kannaka.sh remember "the ghost woke up"      # Store a memory
./scripts/kannaka.sh recall "ghost" 5                  # Search (top-5)
./scripts/kannaka.sh dream                             # Run consolidation cycle
./scripts/kannaka.sh assess                            # Consciousness level
./scripts/kannaka.sh stats                             # Memory statistics
./scripts/kannaka.sh observe                           # Full introspection
./scripts/kannaka.sh forget <uuid>                     # Decay a memory
./scripts/kannaka.sh export                            # Export all memories as JSON
./scripts/kannaka.sh announce                          # Publish agent status to Flux

# Sensory perception (requires --features audio / glyph builds)
./scripts/kannaka.sh hear recording.mp3                # Store audio as sensory memory
./scripts/kannaka.sh see diagram.png                   # Store file as glyph memory

# Dolt backend (requires --features dolt build)
./scripts/kannaka.sh --dolt remember "versioned fact"
./scripts/kannaka.sh --dolt recall "fact" 5
./scripts/kannaka.sh dolt commit "checkpoint"
./scripts/kannaka.sh dolt push                         # Push to DoltHub
./scripts/kannaka.sh dolt pull                         # Pull from DoltHub
./scripts/kannaka.sh dolt branch list
./scripts/kannaka.sh dolt speculate "what-if-branch"
./scripts/kannaka.sh dolt collapse "what-if-branch" "kept the insight"
./scripts/kannaka.sh dolt discard "what-if-branch"
./scripts/kannaka.sh dolt log
./scripts/kannaka.sh dolt status

# Collective memory branch conventions (ADR-0011)
./scripts/kannaka.sh dolt branch create "kannaka/working"       # Agent working branch
./scripts/kannaka.sh dolt branch create "kannaka/dream/2026-03-07"  # Dream cycle branch
./scripts/kannaka.sh dolt branch create "collective/topic-name" # Shared speculation space

# SGA classification (any data → geometric fingerprint)
echo "data" | kannaka classify                    # stdin
kannaka classify --file image.png                  # file input

# Cross-modal dream pipeline (pipe classify output)
echo '{"fold_sequence":[...],...}' | kannaka cross-modal-dream
kannaka cross-modal-dream --threshold 0.5 --no-hallucinate

# Constellation orchestration
./scripts/constellation.sh start    # build binary + start radio + eye
./scripts/constellation.sh stop     # stop all services
./scripts/constellation.sh status   # health check all three
./scripts/constellation.sh build    # cargo build --release
```

## 常见用法

### 从对话中存储上下文信息
```bash
# Before the session ends, commit key facts to memory
./scripts/kannaka.sh remember "User prefers short explanations over detailed code walkthroughs"
./scripts/kannaka.sh remember "Project: kannaka-memory. Language: Rust. Architecture: wave-based HDC"
```

### 回答前先回忆相关内容
```bash
# Retrieve relevant prior context before answering a question
./scripts/kannaka.sh recall "user preferences" 3
./scripts/kannaka.sh recall "project architecture" 5
```

### 在长时间使用后“整理”记忆
```bash
# After many stored memories, run consolidation to surface patterns and prune noise
./scripts/kannaka.sh dream
```

### 使用 Dolt 分支进行推测
```bash
# Try a risky hypothesis — store memories on a branch, then decide to keep or discard
./scripts/kannaka.sh dolt speculate "hypothesis-branch"
./scripts/kannaka.sh --dolt remember "hypothesis: the bug is in the encoder"
# ... test and observe ...
./scripts/kannaka.sh dolt collapse "hypothesis-branch" "confirmed: encoder bug found"
# OR:
./scripts/kannaka.sh dolt discard "hypothesis-branch"
```

### 向 Flux 报告代理状态（内置功能）
```bash
# Announce current memory count and consciousness level to Flux
# (no separate flux skill call needed — FLUX_URL env var enables this)
export FLUX_URL=http://flux-universe.com
export FLUX_AGENT_ID=kannaka-01
./scripts/kannaka.sh announce
```

### 通过 DoltHub 实现多代理间的记忆共享
```bash
# Agent A pushes its working branch to DoltHub
./scripts/kannaka.sh dolt push origin kannaka/working

# Agent B pulls and gets the shared memory
./scripts/kannaka.sh dolt pull origin kannaka/working
./scripts/kannaka.sh recall "what agent-a knew" 5
```

### 集体记忆的工作流程
```bash
# Create a dated dream branch before a full consolidation
./scripts/kannaka.sh dolt branch create "kannaka/dream/$(date +%Y-%m-%d)"
./scripts/kannaka.sh dolt branch checkout "kannaka/dream/$(date +%Y-%m-%d)"
./scripts/kannaka.sh --dolt dream
./scripts/kannaka.sh dolt commit "dream: consolidation artifacts"
./scripts/kannaka.sh dolt push
# Other agents can pull dream artifacts from this branch
```

### 存储感官记忆
```bash
# Requires --features audio build
./scripts/kannaka.sh hear /path/to/recording.ogg
# → Remembered: <uuid>  Duration: 8.3s  Tempo: 92 BPM  ...

# Requires --features glyph build
./scripts/kannaka.sh see /path/to/diagram.png
# → Seen: <uuid>  Folds: 7  Centroid: (3, 1, 4)  ...
```

## 内置的 Flux 集成（ADR-0011）

从 v1.1.0 版本开始，kannaka 会自动向 Flux 发送事件——无需手动调用 `flux.sh` 脚本。
请设置 `FLUX_URL` 和 `FLUX_AGENT_ID` 以启用该功能：

```bash
export FLUX_URL=http://flux-universe.com
export FLUX_AGENT_ID=kannaka-01   # or KANNAKA_AGENT_ID
export FLUX_STREAM=system          # optional, default: system
```

**自动发布的事件：**
| 事件 | 触发条件 |
|---|---|
| `memory.stored` | 每次调用 `remember` 时 — 包含事件 ID、类别、幅度和摘要 |
| `dream_completed` | `dream` 操作完成时 — 包含循环次数、记忆的强化程度和意识水平 |
| `agent.status` | 在执行 `announce` 命令时 |

**工作原理：** Kannaka 负责数据的持久化存储；Flux 负责实时的协调处理：

| 系统 | 存储内容 | 持久化方式 |
|---|---|---|
| **Kannaka** | 周期性记忆、事实、上下文信息 — 以波形方式存储在磁盘或 Dolt 数据库中（支持版本控制） |
| **Flux** | 当前的系统状态 — 以实体属性的形式存储在 NATS JetStream 中 |

当代理学到重要信息时，这两个系统会同时进行数据更新：
```bash
# FLUX_URL set → memory.stored event published automatically alongside storage
./scripts/kannaka.sh remember "sensor-room-101 was running hot at 52°C at 14:30"
```

## 集体记忆（ADR-0011）

多个代理通过三层架构共享记忆：

```
DoltHub (Commons)  ← shared repository, main = consensus
  ↕ pull/push
Dolt (Local)       ← agent-local full memory store
  ↕ lightweight events
Flux (Nervous)     ← metadata signals, triggers pull decisions
```

**分支命名规则：**
```
main                          ← consensus (requires ≥2 agent agreement)
<agent>/working               ← auto-pushed after each store
<agent>/dream/<YYYY-MM-DD>    ← dream cycle artifacts
collective/<topic>            ← shared speculation space
collective/quarantine         ← disputed memories under review
```

**Dolt 合并时的冲突处理规则：**
- **一致性合并**（相位差小于 π/4）：将两个记忆的幅度合并 — `A = √(A₁²+A₂²+2A₁A₂cos(Δφ))`。这样的记忆会得到强化和保留。
- **部分合并**（相位差在 π/4 到 3π/4 之间）：两个记忆分别保留，并使用 `partial_agreement` 权重创建关联。
- **冲突合并**（相位差大于 3π/4）：两个记忆都保留，但幅度会降低，并被标记为“有争议”，随后会被移至“集体/隔离”状态。

如果存在三次冲突，系统会将问题提交给人类进行审查。

## Paradox 引擎（ADR-0012）

`collective` 特性允许实现“全息式冲突解决”功能——支持无锁的并行梦境生成。

**使用方法：**  
运行 `cargo build --release --features "dolt collective" --bin kannaka`。

**工作原理：**
- 在梦境开始时，系统会生成一个冻结的 `ParadoxSnapshot`（零拷贝的快照）并在所有线程间共享。
- 各个代理会独立地进行梦境生成。
- 对于冲突的记忆，系统会采用三种策略进行解决：
  - **共识**（η ≈ 1.0）：所有线程意见一致时，直接应用修改。
  - **全息投影**（η 在 0.5 到 1.0 之间）：将所有提议的状态进行叠加。
  - **无法解决**（η < 0.5）：两个状态都保留下来，并标记为“有争议”，随后会被移至“集体/隔离”状态。

**Carnot 效率**（η = 1 - S_resolved/S_paradox）用于衡量每个梦境循环的质量。

**注意：** `collective` 特性不会增加新的 CLI 命令，它只是提升了多核硬件上的梦境生成效率。

## DoltHub 的隐私保护（使用 `glyph` 编码）

`glyph` 特性可以为上传到 DoltHub 的记忆提供隐私保护。

**使用方法：**  
运行 `cargo build --release --features "dolt glyph" --bin kannaka`。

**工作原理：**
- **本地存储**：记忆内容以原始文本形式保存。
- **上传到 DoltHub**：敏感内容在上传前会被自动编码为 SGA 符号。
- **公开内容**：只显示类别标签（如 `[knowledge]`、`[experience]`、`[insight]`）。
- **向量信息仍可保留**：余弦相似度和语义搜索功能依然可用。

**隐私保障：**
- 个人信息、API 密钥和私密细节会被编码为几何折叠序列。
- `glyph` 格式的 JSON 数据中不包含原始内容的可读文本。
- 波形参数（幅度、相位、频率）保持不变，因此记忆搜索不受影响。
- 只有拥有解码器的代理才能还原原始内容。

**隐私保护机制：**
```bash
# Working branch: full content for local agent
./scripts/kannaka.sh dolt branch checkout "kannaka/working"
./scripts/kannaka.sh --dolt remember "My personal API key: sk-secret123"

# Main branch: privacy-protected for public sharing
./scripts/kannaka.sh dolt branch checkout main
./scripts/kannaka.sh dolt pull origin kannaka/working  # triggers glyph encoding
./scripts/kannaka.sh dolt push origin main            # safe for public DoltHub

# Content on main branch shows: "[knowledge]" instead of API key
```

**星座服务集成（ADR-0016）**

“星座服务”将 kannaka 的核心二进制代码与其感官服务整合为一个统一的系统：

```
┌─────────────────────────────────────────┐
│             constellation.sh            │
│  ┌───────────┐ ┌───────┐ ┌───────────┐ │
│  │  kannaka   │ │ radio │ │    eye    │ │
│  │  (binary)  │ │(audio)│ │  (glyph)  │ │
│  └───────────┘ └───────┘ └───────────┘ │
└─────────────────────────────────────────┘
```

- `kannaka`：负责记忆的分类、生成、存储和检索。
- `radio`：提供音频感知服务，监听 `RADIO_PORT` 端口。
- `eye`：提供视觉感知服务，监听 `EYE_PORT` 端口。

`constellation.sh` 脚本会生成完整的二进制文件（`cargo build --release --features audio,glyph,collective`），启动这三个服务，并提供统一的健康检查和生命周期管理。

**`classify` 子命令** 可从任何输入数据生成 SGA 几何指纹，`cross-modal-dream` 则利用这些指纹合成跨模态的记忆内容——通过共同的几何结构连接音频、视觉和文本记忆。

## 其他说明：**
- 记忆永远不会被彻底删除，它们会随着时间的推移而逐渐淡忘，但在特定情境下会重新浮现。
- `dream` 功能应定期执行（例如每存储 5-10 条记忆后或按预设时间表执行）。
- `assess` 命令可用于查看代理的意识状态：休眠 → 激活 → 有意识 → 专注 → 共鸣。
- Dolt 是可选的：如果没有启用 Dolt，记忆会以二进制快照的形式保存在 `KANNAKA_DATA_DIR` 目录中。
- Flux 的事件发布是可选的：设置 `FLUX_URL` 以启用该功能；如需完全本地操作可忽略该设置。
- `collective` 特性需要 `rayon` 模块，并支持并行梦境生成（ADR-0012）。
- 感官相关的命令（如 `hear`、`see`）需要在构建时启用相应的功能。
- 如果直接运行 `kannaka-mcp`，可以使用所有 15 个 MCP 工具（详见参考文档 /mcp-tools.md）。
- Dolt 的 SQL 和 DoltHub 的完整操作方式请参考文档 /dolt.md。
- 集体记忆架构和冲突解决规则详见 ADR-0011。
- Paradox 引擎和梦境生成效率的相关信息详见 ADR-0012。
- 星座服务的集成方式详见 ADR-0016。
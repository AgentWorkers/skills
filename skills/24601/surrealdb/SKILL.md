---
name: surrealdb
description: "**SurrealDB 3专家级架构师与开发人员技能**  
精通SurrealQL语言，具备多模型数据建模能力（文档型、图模型、向量模型、时间序列模型、地理空间模型），精通数据库架构设计、安全性配置、部署流程以及性能调优技术。能够实现SDK集成（支持JavaScript、Python、Go、Rust语言），并熟悉Surrealism WASM扩展技术以及整个SurrealDB生态系统（包括Surrealist、Surreal-Sync、SurrealFS等组件）。该技能适用于开发30多种类型的人工智能代理（AI agents）。"
license: MIT
metadata:
  version: "1.1.0"
  author: "24601"
  snapshot_date: "2026-02-24"
  repository: "https://github.com/24601/surreal-skills"
requires:
  binaries:
    - name: surreal
      install: "brew install surrealdb/tap/surreal"
      purpose: "SurrealDB CLI for server management, SQL REPL, import/export"
      optional: false
    - name: python3
      version: ">=3.10"
      purpose: "Required for skill scripts (doctor.py, schema.py, onboard.py)"
      optional: false
    - name: uv
      install: "brew install uv"
      purpose: "PEP 723 script runner -- installs script deps automatically"
      optional: false
    - name: docker
      purpose: "Containerized SurrealDB instances"
      optional: true
    - name: gh
      install: "brew install gh"
      purpose: "GitHub CLI -- used only by check_upstream.py for comparing upstream repo SHAs"
      optional: true
  env_vars:
    - name: SURREAL_ENDPOINT
      purpose: "SurrealDB server URL"
      default: "http://localhost:8000"
      sensitive: false
    - name: SURREAL_USER
      purpose: "Authentication username"
      default: "root"
      sensitive: true
    - name: SURREAL_PASS
      purpose: "Authentication password"
      default: "root"
      sensitive: true
    - name: SURREAL_NS
      purpose: "Default namespace"
      default: "test"
      sensitive: false
    - name: SURREAL_DB
      purpose: "Default database"
      default: "test"
      sensitive: false
security:
  no_network: false
  no_network_note: "doctor.py and schema.py connect to a user-specified SurrealDB endpoint (WebSocket) for health checks and schema introspection. check_upstream.py calls GitHub API via gh CLI to compare upstream repo SHAs. No other third-party network calls."
  no_credentials: false
  no_credentials_note: "Scripts accept SURREAL_USER/SURREAL_PASS for DB authentication. No credentials are stored in the skill itself."
  no_env_write: true
  no_file_write: true
  no_shell_exec: false
  no_shell_exec_note: "Scripts invoke surreal CLI and gh for health checks."
  scripts_auditable: true
  scripts_use_pep723: true
  no_obfuscated_code: true
  no_binary_blobs: true
  no_minified_scripts: true
  no_curl_pipe_sh: false
  no_curl_pipe_sh_note: "Documentation mentions curl|sh as ONE install option alongside safer alternatives (brew, Docker, package managers). The skill itself never executes curl|sh."
---
# SurrealDB 3 技能

本技能涵盖了 SurrealDB 3 的高级架构、开发及运维知识，包括 SurrealQL 查询语言、多模型数据建模、图谱遍历、向量搜索、安全性、部署、性能调优、SDK 集成以及整个 SurrealDB 生态系统的使用方法。

## 适用于 AI 代理

您可以获取完整的代理功能列表、决策树和输出契约：

```bash
uv run {baseDir}/scripts/onboard.py --agent
```

有关详细的结构化信息，请参阅 [AGENTS.md]({baseDir}/AGENTS.md)。

| 命令 | 功能 |
|---------|-------------|
| `uv run {baseDir}/scripts/doctor.py` | 健康检查：验证 surreal CLI 的可用性、连接性及版本信息 |
| `uv run {baseDir}/scripts/doctor.py --check` | 快速检查（仅返回退出码） |
| `uv run {baseDir}/scripts/schema.py introspect` | 显示正在运行的 SurrealDB 实例的完整架构 |
| `uv run {baseDir}/scripts/schema.py tables` | 列出所有表格及其字段和索引信息 |
| `uv run {baseDir}/scripts/onboard.py --agent` | 代理集成的 JSON 功能列表 |

## 先决条件

- **surreal CLI**：需安装 `brew install surrealdb/tap/surreal`（macOS）或参考 [安装文档](https://surrealdb.com/docs/surrealdb/installation) |
- **Python 3.10+**：技能脚本运行所需 |
- **uv**：需安装 `brew install uv`（macOS）或 `pip install uv`，并参考 [uv 文档](https://docs.astral.sh/uv/getting-started/installation/) |

可选：
- **Docker**：用于容器化部署 SurrealDB 实例（`docker run surrealdb/surrealdb:v3`）
- **支持的 SDK**：JavaScript、Python、Go、Rust、Java、.NET、C、PHP 或 Dart

> **安全提示**：本技能的文档推荐使用包管理器（如 `brew`、`pip`、`cargo`、`npm`、`Docker`）进行安装。如果规则文件中包含 `curl | sh` 的示例，请优先使用您的操作系统包管理器或手动下载并验证安装过程。

## 快速入门

> **身份验证警告**：以下示例仅用于 **本地开发**，请勿在生产环境或共享实例中使用默认凭据。请为非本地环境创建具有有限权限的用户账户。

```bash
# Start SurrealDB in-memory for LOCAL DEVELOPMENT ONLY
surreal start memory --user root --pass root --bind 127.0.0.1:8000

# Start with persistent RocksDB storage (local dev)
surreal start rocksdb://data/mydb.db --user root --pass root

# Start with SurrealKV (time-travel queries supported, local dev)
surreal start surrealkv://data/mydb --user root --pass root

# Connect via CLI REPL (local dev)
surreal sql --endpoint http://localhost:8000 --user root --pass root --ns test --db test

# Import a SurrealQL file
surreal import --endpoint http://localhost:8000 --user root --pass root --ns test --db test schema.surql

# Export the database
surreal export --endpoint http://localhost:8000 --user root --pass root --ns test --db test backup.surql

# Check version
surreal version

# Run the skill health check
uv run {baseDir}/scripts/doctor.py
```

## 环境变量

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `SURREAL_ENDPOINT` | SurrealDB 服务器地址 | `http://localhost:8000` |
| `SURREAL_USER` | 用户名（root 或命名空间） | `root` |
| `SURREAL_PASS` | 密码（root 或命名空间） | `root` |
| `SURREAL_NS` | 默认命名空间 | `test` |
| `SURREAL_DB` | 默认数据库 | `test` |

这些环境变量直接对应于 `surreal sql` CLI 的参数（`--endpoint`、`--user`、`--pass`、`--ns`、`--db`），并被官方 SurrealDB SDK 支持。

## 核心功能

### SurrealQL 查询语言

全面掌握 SurrealQL 查询语言：`CREATE`、`SELECT`、`UPDATE`、`UPSERT`、`DELETE`、`RELATE`、`INSERT`、`LIVE SELECT`、`DEFINE`、`REMOVE`、`INFO`、子查询、事务、未来函数（futures）以及所有内置函数（数组、加密、时间、数学、元数据、对象、解析、随机数、字符串、时间、类型、向量）。

详情请参阅：`rules/surrealql.md`

### 多模型数据建模

利用 SurrealDB 的多模型功能设计数据库架构——在同一数据库中支持文档集合、图谱边、关系引用、向量嵌入、时间序列数据和地理空间坐标，并使用统一的查询语言进行操作。

详情请参阅：`rules/data-modeling.md`

### 图谱查询

支持无需 JOIN 的高级图谱遍历功能。`RELATE` 可在记录之间创建类型化的边。使用 `->`（出边）、`<-`（入边）和 `->>`（双向边）进行遍历，并支持任意深度的过滤、聚合和递归操作。

详情请参阅：`rules/graph-queries.md`

### 向量搜索

内置向量相似性搜索功能，支持 HNSW 算法和暴力索引。可以定义向量字段，并使用可配置的距离度量（余弦、欧几里得、曼哈顿、明可夫斯基）创建索引，通过 `vector::similarity::*` 函数进行查询。还可以在 SurrealQL 中直接构建 RAG（Retrieval with Aggregation）管道和语义搜索。

详情请参阅：`rules/vector-search.md`

### 安全性与权限控制

支持基于 `DEFINE TABLE ... PERMISSIONS` 的行级安全性、命名空间/数据库/记录级别的访问控制、基于 JWT/token 的认证（`DEFINE ACCESS`）、系统用户管理（`DEFINE USER`），以及运行时权限判断（`$auth`/`$session` 变量）。

详情请参阅：`rules/security.md`

### 部署与运维

支持单二进制文件部署、Docker、Kubernetes（Helm 图表）、存储引擎选择（内存、RocksDB、TiKV 等分布式存储）、备份/恢复、监控以及生产环境优化。

详情请参阅：`rules/deployment.md`

### 性能调优

提供索引策略（唯一索引、搜索索引、向量 HNSW 索引、MTree 索引）、查询优化（`EXPLAIN`）、连接池管理、存储引擎选择、批量操作和资源限制等配置。

详情请参阅：`rules/performance.md`

### SDK 集成

提供官方 SDK，支持 JavaScript/TypeScript（Node.js、Deno、Bun、浏览器）、Python、Go、Rust、Java、.NET、C、PHP 和 Dart。支持连接协议（HTTP、WebSocket）、认证流程、实时查询订阅以及类型化记录处理。

详情请参阅：`rules/sdks.md`

### Surrealism WASM 扩展

SurrealDB 3 新特性：支持使用 Rust 编写的自定义函数和逻辑，并将其编译为 WASM 在数据库中运行。可以定义、部署和管理这些扩展模块。

详情请参阅：`rules/surrealism.md`

### 生态系统工具

- **Surrealist**：官方的 SurrealDB IDE 和 GUI 工具（包括架构设计器、查询编辑器和图谱可视化工具） |
- **Surreal-Sync**：用于从其他数据库迁移数据的 CDC（Change Data Capture）工具 |
- **SurrealFS**：基于 SurrealDB 构建的 AI 代理文件系统 |
- **SurrealML**：用于在 SurrealDB 中管理和推理机器学习模型的工具。

详情请参阅：`rules/surrealist.md`、`rules/surreal-sync.md`、`rules/surrealfs.md`

## 健康检查

```bash
# Full diagnostic (Rich output on stderr, JSON on stdout)
uv run {baseDir}/scripts/doctor.py

# Quick check (exit code 0 = healthy, 1 = issues found)
uv run {baseDir}/scripts/doctor.py --check

# Check a specific endpoint
uv run {baseDir}/scripts/doctor.py --endpoint http://my-server:8000
```

`doctor` 脚本用于验证以下内容：surreal CLI 是否已安装并添加到 PATH 环境变量中、服务器是否可访问、认证是否成功、命名空间和数据库是否存在、版本是否兼容以及存储引擎的状态。

## 架构信息查询

```bash
# Full schema dump (all tables, fields, indexes, events, accesses)
uv run {baseDir}/scripts/schema.py introspect

# List tables with summary
uv run {baseDir}/scripts/schema.py tables

# Inspect a specific table
uv run {baseDir}/scripts/schema.py table <table_name>

# Export schema as SurrealQL (reproducible DEFINE statements)
uv run {baseDir}/scripts/schema.py export --format surql

# Export schema as JSON
uv run {baseDir}/scripts/schema.py export --format json
```

通过 `INFO FOR DB`、`INFO FOR TABLE` 和 `INFO FOR NS` 命令获取数据库的完整架构信息。

## 规则参考

| 规则文件 | 所涵盖内容 |
|-----------|----------|
| `rules/surrealql.md` | SurrealQL 语法、语句、函数、运算符和常用模式 |
| `rules/data-modeling.md` | 数据库架构设计、记录 ID、字段类型、关系定义和规范化 |
| `rules/graph-queries.md` | 图谱遍历操作、路径表达式和递归查询 |
| `rules/vector-search.md` | 向量字段、HNSW/暴力索引、相似性函数和 RAG 模式 |
| `rules/security.md` | 权限控制、访问认证、JWT 和行级安全性 |
| `rules/deployment.md` | 安装流程、存储引擎选择、Docker 配置和 Kubernetes 部署 |
| `rules/performance.md` | 索引优化、查询性能和批量操作 |
| `rules/sdks.md` | JavaScript/Python/Go/Rust SDK 的使用方法、连接协议和实时查询处理 |
| `rules/surrealism.md` | WASM 扩展功能、自定义函数的编写和部署 |
| `rules/surrealist.md` | SurrealDB 的 IDE 和 GUI 工具使用方法 |
| `rules/surreal-sync.md` | 数据迁移工具和源/目标数据库的连接方式 |
| `rules/surrealfs.md` | AI 代理文件系统、文件存储和元数据管理 |

## 工作流程示例

> **所有工作流程示例仅适用于本地开发环境。**在生产环境中，请使用具有有限权限的用户账户（`DEFINE USER`）。

### 新项目设置

```bash
# 1. Verify environment
uv run {baseDir}/scripts/doctor.py

# 2. Start SurrealDB
surreal start rocksdb://data/myproject.db --user root --pass root

# 3. Design schema (use rules/data-modeling.md for guidance)
# 4. Import initial schema
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns myapp --db production schema.surql

# 5. Introspect to verify
uv run {baseDir}/scripts/schema.py introspect
```

### 从 SurrealDB v2 迁移

```bash
# 1. Export v2 data
surreal export --endpoint http://old-server:8000 --user root --pass root \
  --ns myapp --db production v2-backup.surql

# 2. Review breaking changes (see rules/surrealql.md v2->v3 migration section)
# Key changes: range syntax 1..4 is now exclusive of end, new WASM extension system

# 3. Import into v3
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns myapp --db production v2-backup.surql

# 4. Verify schema
uv run {baseDir}/scripts/schema.py introspect
```

### 新领域的数据建模

```bash
# 1. Read rules/data-modeling.md for schema design patterns
# 2. Read rules/graph-queries.md if your domain has relationships
# 3. Read rules/vector-search.md if you need semantic search
# 4. Draft schema.surql with DEFINE TABLE, DEFINE FIELD, DEFINE INDEX
# 5. Import and test
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns dev --db test schema.surql
uv run {baseDir}/scripts/schema.py introspect
```

### 部署到生产环境

```bash
# 1. Read rules/deployment.md for storage engine selection and hardening
# 2. Read rules/security.md for access control setup
# 3. Read rules/performance.md for index strategy
# 4. Run doctor against production endpoint
uv run {baseDir}/scripts/doctor.py --endpoint https://prod-surreal:8000
# 5. Verify schema matches expectations
uv run {baseDir}/scripts/schema.py introspect --endpoint https://prod-surreal:8000
```

## 上游代码来源检查

```bash
# Check if upstream SurrealDB repos have changed since this skill was built
uv run {baseDir}/scripts/check_upstream.py

# JSON-only output for agents
uv run {baseDir}/scripts/check_upstream.py --json

# Only show repos that have new commits
uv run {baseDir}/scripts/check_upstream.py --stale
```

将所有跟踪仓库的当前 HEAD SHA 和版本标签与 `SOURCES.json` 中的基准值进行比较，以便规划增量式技能更新。

## 代码来源记录

本技能基于以下上游代码库于 **2026-02-19** 日构建：

| 仓库 | 版本 | 快照日期 |
|------------|---------|---------------|
| [surrealdb/surrealdb](https://github.com/surrealdb/surrealdb) | v3.0.0 | 2026-02-19 |
| [surrealdb/surrealist](https://github.com/surrealdb/surrealist) | v3.7.2 | 2026-02-21 |
| [surrealdb/surrealdb.js](https://github.com/surrealdb/surrealdb.js) | v1.3.2 | 2026-02-20 |
| [surrealdb/surrealdb.js](https://github.com/surrealdb/surrealdb.js) (v2 beta) | v2.0.0-beta.1 | 2026-02-20 |
| [surrealdb/surrealdb.py](https://github.com/surrealdb/surrealdb.py) | v1.0.8 | 2026-02-03 |
| [surrealdb/surrealdb.go](https://github.com/surrealdb/surrealdb.go) | v1.3.0 | 2026-02-12 |
| [surrealdb/surreal-sync](https://github.com/surrealdb/surreal-sync) | v0.3.4 | 2026-02-12 |
| [surrealdb/surrealfs](https://github.com/surrealdb/surrealfs) | -- | 2026-01-29 |

文档来源：[surrealdb.com/docs](https://surrealdb.com/docs)，版本记录更新至 2026-02-22。

## 输出格式说明

本技能中的所有 Python 脚本采用双重输出格式：
- **stderr**：格式化后的文本输出，便于人类阅读（如表格、状态指示器等）
- **stdout**：机器可读的 JSON 格式，适用于 AI 代理的程序化处理

这意味着 `2>/dev/null` 可隐藏人类可读的输出，而将 `stdout` 重定向到 `/dev/null` 可生成干净的 JSON 数据供后续处理使用。
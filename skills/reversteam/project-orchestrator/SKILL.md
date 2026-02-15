---
name: project-orchestrator
description: AI代理协调器，集成Neo4j知识图谱、Meilisearch搜索功能以及Tree-sitter解析技术。用于在具有共享上下文和计划的复杂项目中协调多个编码代理的工作。
metadata:
  clawdbot:
    emoji: "🎯"
    requires:
      bins: ["docker", "cargo"]
---

# 项目编排器（Project Orchestrator）

该工具用于协调多个 AI 编码代理，并利用共享的知识库来协同工作。

## 主要功能

- **多项目支持**：能够管理多个具有独立数据结构的代码库。
- **Neo4j 知识图谱**：用于存储代码结构、项目关系、计划以及决策信息。
- **Meilisearch**：提供快速的语义搜索功能，可在代码和决策记录中查找所需内容。
- **Tree-sitter**：支持 12 种语言的精确代码解析。
- **计划管理**：支持结构化任务管理，包括任务之间的依赖关系和约束条件。
- **MCP 集成**：兼容 62 种工具，包括 Claude Code、OpenAI Agents 和 Cursor。

## 文档资料

- [安装指南](docs/setup/installation.md)
- [入门教程](docs/guides/getting-started.md)
- [API 参考](docs/api/reference.md)
- [MCP 工具参考](docs/api/mcp-tools.md)
- 集成指南：[Claude Code](docs/integrations/claude-code.md) | [OpenAI](docs/integrations/openai.md) | [Cursor](docs/integrations/cursor.md)

## 快速入门

### 1. 启动后端服务

```bash
cd {baseDir}
docker compose up -d neo4j meilisearch
```

### 2. 构建并运行项目编排器

```bash
cargo build --release
./target/release/orchestrator serve
```

### 或者使用 Docker 运行：

```bash
docker compose up -d
```

### 3. 同步代码库

```bash
# Via CLI
./target/release/orch sync --path /path/to/project

# Via API
curl -X POST http://localhost:8080/api/sync \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/project"}'
```

## 使用方法

### 创建项目

```bash
# Create a new project
curl -X POST http://localhost:8080/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Embryon",
    "root_path": "/Users/triviere/projects/embryon",
    "description": "Neural network composition framework"
  }'

# List all projects
curl http://localhost:8080/api/projects

# Sync a project
curl -X POST http://localhost:8080/api/projects/embryon/sync

# Search code within a project
curl "http://localhost:8080/api/projects/embryon/code/search?q=tensor&limit=10"
```

### 创建计划

```bash
orch plan create \
  --title "Implement GPU Backend" \
  --desc "Add Metal GPU support for neural network operations" \
  --priority 10
```

### 向计划中添加任务

```bash
orch task add \
  --plan <plan-id> \
  --desc "Implement MatMul Metal shader"

orch task add \
  --plan <plan-id> \
  --desc "Add attention layer GPU support" \
  --depends <task-1-id>
```

### 获取代理的上下文信息

```bash
# JSON context
orch context --plan <plan-id> --task <task-id>

# Ready-to-use prompt
orch context --plan <plan-id> --task <task-id> --prompt
```

### 记录决策结果

```bash
orch decision add \
  --task <task-id> \
  --desc "Use shared memory for tile-based MatMul" \
  --rationale "Better cache locality, 2x performance improvement"
```

### 查找过去的决策记录

```bash
orch decision search "memory management GPU"
```

## API 接口

### 项目（多项目支持）

| 方法 | 路径          | 描述                        |
|--------|-----------------------------|
| GET    | `/api/projects`     | 列出所有项目                        |
| POST    | `/api/projects`     | 创建新项目                        |
| GET    | `/api/projects/{slug}`    | 根据 slug 获取项目信息                |
| DELETE | `/api/projects/{slug}`    | 删除项目                        |
| POST    | `/api/projects/{slug}/sync`   | 同步项目的代码库                    |
| GET    | `/api/projects/{slug}/plans` | 查看项目的计划列表                |
| GET    | `/api/projects/{slug}/code/search` | 在项目中搜索代码                    |

### 计划与任务

| 方法 | 路径          | 描述                        |
|--------|-----------------------------|
| GET    | `/health`       | 检查系统运行状态                    |
| POST    | `/api/plans`     | 创建新计划                        |
| GET    | `/api/plans/{id}`     | 获取计划详情                      |
| PATCH    | `/api/plans/{id}`     | 更新计划状态                      |
| GET    | `/api/plans/{id}/next-task` | 获取下一个可执行的任务                |
| POST    | `/api/plans/{id}/tasks` | 向计划中添加任务                    |
| GET    | `/api/tasks/{id}`     | 获取任务详情                      |
| PATCH    | `/api/tasks/{id}`     | 更新任务信息                      |
| GET    | `/api/plans/{plan}/tasks/{task}/context` | 获取任务的上下文信息                |
| GET    | `/api/plans/{plan}/tasks/{task}/prompt` | 获取任务生成的提示信息                |
| POST    | `/api/tasks/{id}/decisions` | 为任务添加决策记录                  |
| GET    | `/api/decisions/search?q=...` | 搜索过去的决策记录                |

### 同步与监控

| 方法 | 路径          | 描述                        |
|--------|-----------------------------|
| POST    | `/api/sync`     | 将目录内容同步到知识库                    |
| GET    | `/api/watch`     | 获取文件监控状态                    |
| POST    | `/api/watch`     | 开始监控指定目录                    |
| DELETE | `/api/watch`     | 停止对目录的监控                    |
| POST    | `/api/wake`     | 发送代理完成通知的 Webhook                |

### 代码探索（代码图谱与搜索）

| 方法 | 路径          | 描述                        |
|--------|-----------------------------|
| GET    | `/api/code/search?q=...` | 进行语义代码搜索                    |
| GET    | `/api/code/symbols/{path}` | 获取文件中的符号信息                  |
| GET    | `/api/code/references?symbol=...` | 查找符号的所有引用                    |
| GET    | `/api/code/dependencies/{path}` | 获取文件的导入/依赖关系图                |
| GET    | `/api/code/callgraph?function=...` | 获取函数的调用关系图                |
| GET    | `/api/code/impact?target=...` | 分析代码变更的影响                  |
| GET    | `/api/code/architecture` | 查看代码库的整体结构                  |
| POST    | `/api/code/similar`     | 查找相似的代码片段                    |
| GET    | `/api/code/trait-impls?trait_name=...` | 查找实现特定 trait 的代码片段            |
| GET    | `/api/code/type-traits?type_name=...` | 查找由特定类型实现的 trait                |
| GET    | `/api/code/impl-blocks?type_name=...` | 获取特定类型的所有实现块                  |

## 与文件监控器的自动同步

在编码过程中，知识库会自动更新：

```bash
# Start watching a project directory
curl -X POST http://localhost:8080/api/watch \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/project"}'

# Check watcher status
curl http://localhost:8080/api/watch

# Stop watching
curl -X DELETE http://localhost:8080/api/watch
```

该工具会自动同步 `.rs`、`.ts`、`.tsx`、`.js`、`.jsx`、`.py`、`.go` 文件的变更。同时，它会忽略 `node_modules/`、`target/`、`.git/`、`__pycache__`、`dist/`、`build/` 目录。

## 代码探索方式

可以直接查询代码图谱，而无需直接阅读源代码：

```bash
# Semantic search across code
curl "http://localhost:8080/api/code/search?q=error+handling&language=rust&limit=10"

# Get symbols in a file (functions, structs, etc.)
curl "http://localhost:8080/api/code/symbols/src%2Flib.rs"

# Find all references to a symbol
curl "http://localhost:8080/api/code/references?symbol=AppState&limit=20"

# Get file dependencies (imports and dependents)
curl "http://localhost:8080/api/code/dependencies/src%2Fneo4j%2Fclient.rs"

# Get call graph for a function
curl "http://localhost:8080/api/code/callgraph?function=handle_request&depth=2&direction=both"

# Analyze impact before changing a file
curl "http://localhost:8080/api/code/impact?target=src/lib.rs&target_type=file"

# Get architecture overview
curl "http://localhost:8080/api/code/architecture"

# Find similar code patterns
curl -X POST http://localhost:8080/api/code/similar \
  -H "Content-Type: application/json" \
  -d '{"snippet": "async fn handle_error", "limit": 5}'

# Find all types implementing a trait
curl "http://localhost:8080/api/code/trait-impls?trait_name=Module"

# Find all traits implemented by a type
curl "http://localhost:8080/api/code/type-traits?type_name=Orchestrator"

# Get all impl blocks for a type
curl "http://localhost:8080/api/code/impl-blocks?type_name=Neo4jClient"
```

### 为代理提供的功能

- **开始工作前的上下文获取**：帮助代理了解项目背景。
- **工作过程中的决策记录**：确保代理能够基于最新信息进行操作。
- **完成任务的实时通知**：及时通知代理任务已完成。

## 配置参数

环境变量设置：

| 变量        | 默认值        | 描述                                      |
|-------------|-------------|-----------------------------------------|
| `NEO4J_URI`    | `bolt://localhost:7687` | Neo4j 数据库连接地址                        |
| `NEO4J_USER`    | `neo4j`       | Neo4j 用户名                                    |
| `NEO4J_PASSWORD` | `orchestrator123`   | Neo4j 密码                                    |
| `MEILISEARCH_URL` | `http://localhost:7700` | Meilisearch 服务地址                        |
| `MEILISEARCH_KEY` | `orchestrator-meili-key-change-me` | Meilisearch API 密钥                        |
| `WORKSPACE_PATH` | `.`         | 默认工作空间路径                                  |
| `SERVER_PORT`    | `8080`       | 服务器端口号                                  |
| `RUST_LOG`     | `info`       | 日志记录级别                                  |

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR API                          │
│                    (localhost:8080)                          │
└─────────────────────────────┬───────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│    NEO4J      │     │  MEILISEARCH  │     │  TREE-SITTER  │
│   (7687)      │     │    (7700)     │     │   (in-proc)   │
│               │     │               │     │               │
│ • Code graph  │     │ • Code search │     │ • AST parsing │
│ • Plans       │     │ • Decisions   │     │ • Symbols     │
│ • Decisions   │     │ • Logs        │     │ • Complexity  │
│ • Relations   │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘
```

## 开发说明

```bash
# Run tests
cargo test

# Run with debug logging
RUST_LOG=debug cargo run -- serve

# Format code
cargo fmt

# Lint
cargo clippy
```
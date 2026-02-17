---
name: project-orchestrator
description: AI代理协调器，集成Neo4j知识图谱、Meilisearch搜索功能以及Tree-sitter解析技术。用于在具有共享上下文和计划的复杂项目中协调多个编码代理的工作。
metadata: { "openclaw": { "emoji": "🎯", "requires": { "bins": ["docker", "cargo"] } } }
---
# 项目编排器（Project Orchestrator）

该项目用于协调多个AI编码代理，并利用共享的知识库来协同工作。

## 主要功能

- **多项目支持**：能够管理多个代码库，每个代码库的数据相互独立。
- **Neo4j知识图谱**：用于存储代码结构、代码之间的关系、项目计划以及相关决策。
- **Meilisearch**：提供快速的语义搜索功能，可在代码和决策记录中查找所需信息。
- **Tree-sitter**：支持12种语言的精确代码解析。
- **计划管理**：支持结构化的任务管理，包括任务之间的依赖关系和约束条件。
- **MCP集成**：支持与Claude Code、OpenAI Agents以及Cursor等工具的集成。

## 文档资料

- [安装指南](docs/setup/installation.md)
- [入门教程](docs/guides/getting-started.md)
- [API参考](docs/api/reference.md)
- [MCP工具参考](docs/api/mcp-tools.md)
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

**或使用Docker：**
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

### 创建项目计划

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

## API接口

### 项目（多项目支持）

| 方法 | 路径          | 描述                                      |
|--------|--------------|-------------------------------------------|
| GET    | `/api/projects`    | 列出所有项目                          |
| POST    | `/api/projects`    | 创建新项目                          |
| GET    | `/api/projects/{slug}`    | 根据slug获取项目信息                    |
| DELETE | `/api/projects/{slug}`    | 删除项目                          |
| POST    | `/api/projects/{slug}/sync`    | 同步项目的代码库                      |
| GET    | `/api/projects/{slug}/plans`    | 获取项目的计划列表                      |
| GET    | `/api/projects/{slug}/code/search` | 在项目中搜索代码                        |

### 计划与任务

| 方法 | 路径          | 描述                                      |
|--------|--------------|-------------------------------------------|
| GET    | `/health`       | 检查系统运行状态                        |
| GET    | `/api/plans`    | 列出所有活跃的计划                        |
| POST    | `/api/plans`    | 创建新的计划                        |
| GET    | `/api/plans/{id}`    | 获取计划的详细信息                      |
| PATCH    | `/api/plans/{id}`    | 更新计划的状态                        |
| GET    | `/api/plans/{id}/next-task` | 获取计划的下一项可用任务                    |
| POST    | `/api/plans/{id}/tasks` | 向计划中添加任务                        |
| GET    | `/api/tasks/{id}`    | 获取任务的详细信息                      |
| PATCH    | `/api/tasks/{id}`    | 更新任务信息                        |
| GET    | `/api/plans/{plan}/tasks/{task}/context` | 获取任务的上下文信息                    |
| GET    | `/api/plans/{plan}/tasks/{task}/prompt` | 获取为任务生成的提示信息                    |
| POST    | `/api/tasks/{id}/decisions` | 为任务添加决策记录                        |
| GET    | `/api/decisions/search?q=...` | 搜索过去的决策记录                        |

### 同步与监控

| 方法 | 路径          | 描述                                      |
|--------|--------------|-------------------------------------------|
| POST    | `/api/sync`    | 将目录内容同步到知识库                      |
| GET    | `/api/watch`    | 获取文件监控的状态                        |
| POST    | `/api/watch`    | 开始监控指定目录                        |
| DELETE | `/api/watch`    | 停止对目录的监控                        |
| POST    | `/api/wake`    | 发送代理完成任务的Webhook                    |

### 代码探索（代码图谱与搜索）

| 方法 | 路径          | 描述                                      |
|--------|--------------|-------------------------------------------|
| GET    | `/api/code/search?q=...` | 进行语义代码搜索                        |
| GET    | `/api/code/symbols/{path}` | 获取文件中的符号信息                        |
| GET    | `/api/code/references?symbol=...` | 查找符号的所有引用                        |
| GET    | `/api/code/dependencies/{path}` | 获取文件的导入/依赖关系图                    |
| GET    | `/api/code/callgraph?function=...` | 获取函数的调用关系图                    |
| GET    | `/api/code/impact?target=...` | 分析代码变更的影响                    |
| GET    | `/api/code/architecture` | 获取代码库的总体结构                        |
| POST    | `/api/code/similar` | 查找相似的代码片段                        |
| GET    | `/api/code/trait-impls?trait_name=...` | 查找实现特定特性的代码片段                        |
| GET    | `/api/code/type-traits?type_name=...` | 查找由特定类型实现的特性                        |
| GET    | `/api/code/impl-blocks?type_name=...` | 获取特定类型的所有实现代码块                        |

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

当`.rs`、`.ts`、`.tsx`、`.js`、`.jsx`、`.py`、`.go`文件被修改时，文件监控器会自动同步这些文件的内容。系统会忽略`node_modules/`、`target/`、`.git/`、`__pycache__`、`dist/`、`build/`目录。

## 代码探索方式

可以直接查询代码图谱来了解代码的结构和依赖关系，而无需直接阅读源代码：

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

### 在开始工作前获取上下文信息

```bash
# Fetch your task context
curl http://localhost:8080/api/plans/$PLAN_ID/tasks/$TASK_ID/prompt
```

### 在执行任务时记录决策结果

```bash
curl -X POST http://localhost:8080/api/tasks/$TASK_ID/decisions \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Chose X over Y",
    "rationale": "Because..."
  }'
```

### 任务完成后发送通知

```bash
curl -X POST http://localhost:8080/api/wake \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "'$TASK_ID'",
    "success": true,
    "summary": "Implemented feature X",
    "files_modified": ["src/foo.rs", "src/bar.rs"]
  }'
```

## 配置参数

环境变量：

| 变量            | 默认值          | 描述                                      |
|-----------------|--------------|-------------------------------------------|
| `NEO4J_URI`       | `bolt://localhost:7687`    | Neo4j数据库连接地址                    |
| `NEO4J_USER`       | `neo4j`         | Neo4j用户名                          |
| `NEO4J_PASSWORD`     | `orchestrator123`     | Neo4j密码                          |
| `MEILISEARCH_URL`     | `http://localhost:7700`    | Meilisearch API地址                        |
| `MEILISEARCH_KEY`     | `orchestrator-meili-key-change-me` | Meilisearch API密钥                        |
| `WORKSPACE_PATH`     | `.`           | 默认工作目录路径                        |
| `SERVER_PORT`      | `8080`         | 服务器端口号                        |
| `RUST_LOG`        | `info`         | 日志记录级别                          |

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

## 开发流程

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
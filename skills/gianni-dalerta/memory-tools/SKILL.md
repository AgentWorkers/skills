---
name: memory-tools
description: OpenClaw的代理控制内存插件，支持信心评分（confidence scoring）、数据衰减（decay）以及语义搜索（semantic search）功能。该插件由代理决定何时存储或检索数据，避免自动捕获不必要的数据（即避免自动捕获“噪声”信息）。版本2采用基于文件的存储方式，并提供可选的QMD搜索功能（无需外部API）。
homepage: https://github.com/Purple-Horizons/memory-tools
metadata:
  openclaw:
    emoji: 🧠
    kind: plugin
---
# Memory Tools v2

这是一个由 OpenClaw 控制的持久性记忆系统。

## v2 的新特性

- **基于文件的存储**：记忆以可读的 Markdown 文件形式存储。
- **无需外部 API**：完全不依赖 OpenAI，所有功能都在本地运行。
- **QMD 搜索（可选）**：使用 BM25 算法进行文本索引，并结合向量模型和本地 GGUF 模型进行重新排序。
- **自动迁移**：能够从 v1 的 SQLite/LanceDB 存储格式无缝升级到 v2 的新格式。

## 为什么选择“将记忆作为工具”？

传统的记忆系统会自动捕获所有信息，导致上下文被大量无关内容淹没。Memory Tools 遵循 [AgeMem](https://arxiv.org/abs/2409.02634) 的设计理念：由代理决定何时存储和检索记忆。

## 主要功能

- **6 个核心工具**：`memory_store`、`memory_update`、`memory_forget`、`memory_search`、`memory_summarize`、`memory_list`。
- **置信度评分**：记录信息的可靠性（1.0 表示完全确定，0.5 表示推测）。
- **重要性评分**：优先处理关键指令而非次要信息。
- **数据衰减/过期**：临时性记忆会自动失效。
- **人类可读的存储格式**：使用带有 YAML 标签的 Markdown 文件。
- **冲突解决**：新信息会自动替换旧信息（避免数据矛盾）。

## 安装步骤

### 第一步：从 ClawHub 安装插件

```bash
clawhub install memory-tools
```

### 第二步：构建插件

```bash
cd skills/memory-tools
npm install
npm run build
```

### 第三步：激活插件

```bash
openclaw plugins install --link .
openclaw plugins enable memory-tools
```

### 第四步：重启 OpenClaw 服务器

```bash
openclaw gateway restart
```

### 可选步骤：安装 QMD 以提升搜索功能

```bash
npm install -g @tobilu/qmd
```

即使不安装 QMD，系统也支持基本过滤功能；安装 QMD 后可启用语义搜索（基于 BM25 算法和向量模型）。

### Node.js 兼容性（关于 QMD）

- QMD 可能无法立即与最新的 Node.js ABI 兼容。
- 如果 QMD 安装失败（例如 `NODE_MODULE_VERSION` 不匹配），Memory Tools 会自动切换到基本模式。
- 如需强制使用基本模式，请设置 `MEMORY_TOOLS_DISABLE_QMD=true`。
- 为确保 QMD 的稳定性，请使用与已安装的 QMD 版本兼容的 Node.js LTS 版本。

## 安全性

- 无需 API 密钥或外部凭证。
- 数据存储在本地路径 `~/.openclaw/memories`（或通过配置文件 `memoriesPath` 指定）。
- 当 `autoInjectInstructions=true` 时，插件会在代理启动前自动添加上下文信息。
- 当 `autoMigrateLegacy=true` 时，插件会自动将旧版本的记忆数据从 `~/.openclaw/memory/tools/memory.db` 迁移到新格式。
- 默认设置较为保守：`autoInjectInstructions` 和 `autoMigrateLegacy` 均设置为 `false`。

## 数据存储格式

记忆数据以 Markdown 文件的形式存储在 `~/.openclaw/memories/` 目录下：

```
~/.openclaw/memories/
├── facts/
│   └── abc123-def4-5678-90ab-cdef12345678.md
├── preferences/
│   └── def456-7890-abcd-ef12-345678901234.md
├── instructions/
│   └── ghi789-0abc-def1-2345-678901234567.md
└── .deleted/
    └── old-memory.md
```

每个记忆文件的结构如下：

```markdown
---
id: abc123-def4-5678-90ab-cdef12345678
category: preference
confidence: 0.9
importance: 0.7
created_at: 2024-01-15T10:30:00Z
tags: [ui, settings]
---

User prefers dark mode in all applications.
```

## 记忆分类

| 分类        | 用途                | 示例                          |
|-------------|------------------|------------------------------|
| fact        | 静态信息            | “用户的狗名叫 Rex”                    |
| preference   | 喜好/厌恶            | “用户偏好暗色模式”                    |
| event       | 临时性事件            | “牙医预约在周二下午 3 点”                |
| relationship | 人物关系            | “Sarah 是用户的妻子”                    |
| instruction   | 固定指令            | “始终用西班牙语回复”                    |
| decision     | 决策结果            | “我们决定使用 PostgreSQL 作为数据库”            |
| context     | 情境相关信息          | “用户正在找工作”                    |
| entity      | 具体实体            | “Project Apollo 是他们的初创公司”            |

## 工具参考

- `memory_store`：用于存储记忆数据。
- `memory_search`：用于搜索记忆内容。
- `memory_update`：用于更新记忆信息。
- `memory_forget`：用于删除记忆记录。
- `memory_summarize`：用于总结记忆内容。
- `memory_list`：用于列出所有记忆记录。
- `memory_list`：用于显示记忆列表。

## 命令行接口（CLI）命令

```bash
# Show memory statistics
openclaw memory-tools stats

# List memories
openclaw memory-tools list
openclaw memory-tools list --category fact

# Search memories (requires QMD)
openclaw memory-tools search "dark mode"

# Export all memories as JSON
openclaw memory-tools export

# Force re-index with QMD
openclaw memory-tools reindex

# Show storage path
openclaw memory-tools path
```

## 调试说明

记忆数据以纯 Markdown 格式存储，可以直接阅读文件内容。

## 所有记忆数据的导出

```bash
openclaw memory-tools export > memories.json
```

## 从 v1 版本升级

v2 会自动检测并迁移 v1 版本的记忆数据：

1. 启动时，v2 会检查 `~/.openclaw/memory/tools/memory.db` 文件。
2. 如果找到该文件，会将所有记忆数据导出为 Markdown 文件。
3. 原始数据库会被保留作为备份。
4. 完全无需手动操作。

若要启用自动迁移功能，请在插件配置中设置 `autoMigrateLegacy=true`。

## 许可证

Memory Tools 使用 MIT 许可协议，由 [Purple Horizons](https://github.com/Purple-Horizons) 开发。
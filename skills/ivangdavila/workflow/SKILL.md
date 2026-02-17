---
name: Workflow
slug: workflow
version: 1.0.0
description: 使用可重用的组件构建自动化管道，实现节点之间的数据流动以及状态管理。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["jq","yq","curl","uuidgen","flock"]},"os":["linux","darwin"]}}
---
## 架构

工作流（workflows）存储在 `workflows/` 目录下，其中包含各个组件（components）和流程（flows）：

```
workflows/
├── index.md                 # Inventory with tags
├── components/
│   ├── connections/         # Auth configs
│   ├── nodes/               # Reusable operations
│   └── triggers/            # Event sources
└── flows/{name}/
    ├── flow.md              # Definition
    ├── config.yaml          # Parameters
    ├── run.sh               # Executable
    ├── state/               # Persistent between runs
    └── logs/
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 目录结构、命名规范、文件格式 | `structure.md` |
| 节点之间的数据传递 | `data-flow.md` |
| 游标（cursor）、已处理的数据（seen data）、检查点（checkpoint） | `state.md` |
| 重试（retry）、回滚（rollback）、幂等性（idempotency） | `errors.md` |
| 连接（connections）、节点（nodes）、触发器（triggers） | `components.md` |
| 创建（create）、测试（test）、更新（update）、归档（archive） | `lifecycle.md` |

## 所需工具/库

- **jq**：用于处理 JSON 数据
- **yq**：用于解析 YAML 配置文件
- **curl**：用于发送 HTTP 请求
- **flock**：用于锁定文件，防止多个进程同时执行相同操作
- 在 macOS 上，可以使用 Keychain 存储敏感信息（`security find-generic-password`）

## 数据存储

- **存储位置**：工作区根目录下的 `workflows/` 目录
- **状态数据**：`flows/{name}/state/` 目录下的 `cursor.json`、`seen.json`、`checkpoint.json` 文件
- **日志**：`flows/{name}/logs/` 目录下，每个运行过程都会生成一个 JSONL 文件
- **中间数据**：`flows/{name}/data/` 目录，用于存储节点之间的临时数据

## 核心规则

### 1. 数据流模式
每个节点会将处理结果写入 `data/{NN}-{name}.json` 文件中，下一个节点会读取该文件。  
**注意**：如果违反此模式，节点将无法正常通信。

### 2. 错误处理
`flow.md` 文件中的每个节点都必须明确指定错误处理方式：
- **发生错误时**：可以选择重试（retry(N)）、失败（fail）、继续执行（continue）或发出警报（alert）。
- **处理空数据时**：可以选择跳过当前步骤（skip）、继续执行或失败（fail）。
未定义错误处理方式会导致工作流程行为不可预测。

### 3. 文件锁定
为防止多个进程同时执行相同的操作，需要对相关文件进行锁定：

```bash
LOCKFILE="/tmp/workflow-${NAME}.lock"
exec 200>"$LOCKFILE"
flock -n 200 || exit 0
```

### 4. 状态文件
- `cursor.json`：记录当前处理的进度位置。
- `seen.json`：记录已经处理的数据。
- `checkpoint.json`：用于实现多步骤操作的恢复功能。

### 5. 组件复用
在创建新的连接、节点或触发器之前，请先尝试使用现有的组件。  
**新增组件时**，需要更新相应的文档（`Workflows Using This` 部分）。

---

**相关内容**：对于由大型语言模型（LLM）驱动的多阶段流程，可以参考 `cycle` 技能文档。
# Jasper Recall - OpenClaw 插件

使用 ChromaDB 对索引化的内存进行语义搜索，并在代理处理之前自动插入相关上下文。

## 特点

- **`recall` 工具** — 手动对内存进行语义搜索
- **`/recall` 命令** — 从聊天记录中快速查找信息
- **`/index` 命令** — 重新索引内存文件
- **自动回忆** — 在处理消息之前自动插入相关的内存内容

---

## 自动回忆（神奇的功能 ✨）

当启用 `autoRecall` 时，jasper-recall 会挂载到代理的生命周期中，并在处理每条消息之前自动搜索内存。

### 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│  1. Message arrives from user                               │
│  2. before_agent_start hook fires                           │
│  3. jasper-recall searches ChromaDB with message as query   │
│  4. Results filtered by minScore (default: 30%)             │
│  5. Relevant memories injected via prependContext           │
│  6. Agent sees memories + original message                  │
│  7. Agent responds with full context                        │
└─────────────────────────────────────────────────────────────┘
```

### 被插入的内容

```xml
<relevant-memories>
The following memories may be relevant to this conversation:
- [memory/2026-02-05.md] Worker orchestration decisions...
- [MEMORY.md] Git workflow: feature → develop → main...
- [memory/sops/codex-integration-sop.md] Codex Cloud sync...
</relevant-memories>
```

### 被跳过的内容

自动回忆功能不会执行以下操作：
- 心跳检查（`HEARTBEAT...`）
- 包含 `NO_REPLY` 的系统提示
- 长度小于 10 个字符的消息

---

## 配置

在 `openclaw.json` 文件中：

```json
{
  "plugins": {
    "entries": {
      "jasper-recall": {
        "enabled": true,
        "config": {
          "autoRecall": true,
          "minScore": 0.3,
          "defaultLimit": 5,
          "publicOnly": false
        }
      }
    }
  }
}
```

### 选项

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `enabled` | 布尔值 | `true` | 启用/禁用插件 |
| `autoRecall` | 布尔值 | `false` | 在处理消息之前自动插入相关内存 |
| `minScore` | 数值 | `0.3` | 自动回忆的最低相似度分数（0-1） |
| `defaultLimit` | 数值 | `5` | 默认结果数量 |
| `publicOnly` | 布尔值 | `false` | 仅搜索公共内存（沙箱代理） |

### 分数调整

- `minScore: 0.3` — 包括关联度较低的内存内容（提供更多上下文，但可能包含无关信息）
- `minScore: 0.5` — 仅包含中等相关性的内容（平衡性较好）
- `minScore: 0.7` — 仅包含高度相关的内容（精确性较高，但可能遗漏有用信息）

---

## 工具

### `recall`

手动对内存进行语义搜索。

**参数：**
- `query`（字符串，必填）：自然语言搜索查询
- `limit`（数值，可选）：最大结果数量（默认：5）

**示例：**
```
recall query="what did we decide about the API design" limit=3
```

**返回结果：** 格式化后的 Markdown 文本，包含匹配的内存内容、分数和来源。

---

## 命令

### `/recall <query>`

从聊天记录中快速搜索内存内容。

```
/recall worker orchestration decisions
```

### `/index`

将内存文件重新索引到 ChromaDB。在更新笔记后运行此命令。

```
/index
```

---

## RPC 方法

用于外部集成：

### `recall.search`

```json
{ "query": "search terms", "limit": 5 }
```

### `recall.index`

重新索引内存文件（无需参数）。

---

## 必备条件

- `~/.local/bin/` 目录下存在 `recall` 命令
- `~/.openclaw/chroma-db` 目录下有 ChromaDB 索引
- `~/.openclaw/rag-env` 目录下有 Python 虚拟环境

## 安装

```bash
npx jasper-recall setup
```

安装过程包括：
1. 创建包含 ChromaDB 和 sentence-transformers 的 Python 虚拟环境
2. 安装 `recall`、`index-digests`、`digest-sessions` 脚本
3. 初始化内存文件的索引

---

## 自动回忆的适用场景

✅ **非常适合用于：**
- 询问过去的决策（“我们关于 X 有什么决定？”）
- 回顾之前的工作（“我们在 worker 设置方面进展到哪里了？”）
- 了解人员信息、偏好和项目详情
- 查找标准操作程序（SOP）和流程

⚠️ **不太适用的情况：**
- 完全新颖且没有相关记忆记录的主题
- 简单的命令（如 “列出文件”）
- 实时数据（如天气、时间）

---

## 沙箱代理

对于处理不受信任输入的代理，使用 `publicOnly` 选项：

```json
{
  "jasper-recall": {
    "config": {
      "publicOnly": true,
      "autoRecall": true
    }
  }
}
```

这会将搜索范围限制在 `memory/shared/` 目录和带有 `public` 标签的内容上，防止私人记忆内容泄露。

---

## 链接

- **GitHub**：https://github.com/E-x-O-Entertainment-Studios-Inc/jasper-recall
- **npm**：`npx jasper-recall setup`
- **ClawHub**：`clawhub install jasper-recall`
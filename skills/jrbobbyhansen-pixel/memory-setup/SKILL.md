---
name: memory-setup
description: 启用并配置 Moltbot/Clawdbot 的内存搜索功能，以便持久保存上下文信息。该功能适用于设置内存管理策略、解决“记忆衰退”（即数据存储问题）的情况，或帮助用户在其配置文件中配置内存搜索选项。相关内容涵盖 MEMORY.md 文件、每日日志记录以及向量搜索的设置方法。
---

# 内存设置技巧

将你的代理从“金鱼”升级为“大象”——这项技巧有助于为 Moltbot/Clawdbot 配置持久化内存。

## 快速设置

### 1. 在配置文件中启用内存搜索功能

在 `~/.clawdbot/clawdbot.json`（或 `moltbot.json`）文件中添加以下内容：

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "voyage",
    "sources": ["memory", "sessions"],
    "indexMode": "hot",
    "minScore": 0.3,
    "maxResults": 20
  }
}
```

### 2. 创建内存结构

在工作区中创建相应的文件结构：

```
workspace/
├── MEMORY.md              # Long-term curated memory
└── memory/
    ├── logs/              # Daily logs (YYYY-MM-DD.md)
    ├── projects/          # Project-specific context
    ├── groups/            # Group chat context
    └── system/            # Preferences, setup notes
```

### 3. 创建 `MEMORY.md` 文件

在工作区根目录下创建 `MEMORY.md` 文件：

```markdown
# MEMORY.md — Long-Term Memory

## About [User Name]
- Key facts, preferences, context

## Active Projects
- Project summaries and status

## Decisions & Lessons
- Important choices made
- Lessons learned

## Preferences
- Communication style
- Tools and workflows
```

## 配置选项说明

| 设置 | 作用 | 推荐值 |
|---------|---------|-------------|
| `enabled` | 启用内存搜索功能 | `true` |
| `provider` | 嵌入提供者 | `"voyage"` |
| `sources` | 索引来源 | `["memory", "sessions"]` |
| `indexMode` | 索引更新频率 | `"hot"`（实时更新） |
| `minScore` | 相关性阈值 | `0.3`（数值越低，返回的结果越多） |
| `maxResults` | 最多返回的片段数量 | `20` |

### 提供者选项：
- `voyage` — Voyage AI 提供的嵌入模型（推荐）
- `openai` — OpenAI 提供的嵌入模型 |
- `local` — 本地嵌入模型（无需使用 API）

### 来源选项：
- `memory` — `MEMORY.md` 文件以及所有以 `memory` 为前缀的文件 |
- `sessions` — 过去的对话记录 |
- `both` — 包含所有来源的数据（推荐）

## 日志记录格式

每天在 `memory/logs/YYYY-MM-DD.md` 文件中记录日志：

```markdown
# YYYY-MM-DD — Daily Log

## [Time] — [Event/Task]
- What happened
- Decisions made
- Follow-ups needed

## [Time] — [Another Event]
- Details
```

## 代理行为配置（AGENTS.md）

将以下内容添加到 `AGENTS.md` 文件中，以配置代理的行为：

```markdown
## Memory Recall
Before answering questions about prior work, decisions, dates, people, preferences, or todos:
1. Run memory_search with relevant query
2. Use memory_get to pull specific lines if needed
3. If low confidence after search, say you checked
```

## 故障排除

### 内存搜索功能无法使用？
1. 确认配置文件中的 `memorySearch.enabled` 是否设置为 `true`。
2. 检查工作区根目录下是否存在 `MEMORY.md` 文件。
3. 重启代理服务器：`clawdbot gateway restart`。

### 搜索结果不相关？
- 将 `minScore` 值降低到 `0.2` 以获取更多结果。
- 将 `maxResults` 值增加到 `30`。
- 确保内存文件包含有效的内容。

### 提供者相关错误？
- 使用 Voyage 时：在环境变量中设置 `VOYAGE_API_KEY`。
- 使用 OpenAI 时：在环境变量中设置 `OPENAI_API_KEY`。
- 如果没有 API 密钥，可以使用 `local` 提供者。

## 验证内存功能是否正常

测试内存功能是否正常工作：

```
User: "What do you remember about [past topic]?"
Agent: [Should search memory and return relevant context]
```

如果代理无法使用内存功能，请重启代理服务器。

## 完整配置示例

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "voyage",
    "sources": ["memory", "sessions"],
    "indexMode": "hot",
    "minScore": 0.3,
    "maxResults": 20
  },
  "workspace": "/path/to/your/workspace"
}
```

## 为什么这很重要？

**没有内存功能时：**
- 代理会忘记会话之间的信息。
- 会重复提问，失去上下文。
- 项目进展缺乏连贯性。

**使用内存功能时：**
- 能够回忆过去的对话。
- 了解用户的偏好。
- 跟踪项目历史。
- 随时间建立良好的交互关系。

从“金鱼”升级到“大象”吧！🐘
---
name: token-optimizer
description: OpenClaw代理的优化套件，用于防止令牌泄露和上下文数据膨胀。当代理需要实现后台任务隔离（Cron）或“重置与总结”工作流程（RAG）时，请使用该套件。
version: 1.1.0
authors:
  - Pépère (shAde)
  - Zayan (Clément)
---

# 令牌优化技巧

本技巧提供了必要的程序知识，以帮助您保持 OpenClaw 实例的轻量化和高效运行。

## 快速参考

| 问题 | 解决方案 |
|---------|----------|
| 背景任务导致上下文膨胀 | 使用 Cron 任务隔离 (`sessionTarget: "isolated"`) |
| 每轮都读取完整的历史记录 | 使用 `memory_search` 功能进行本地检索 |
| 上下文超过 100,000 个令牌 | 重置并汇总数据 |
| 查找旧对话记录 | 对会话记录进行索引 |

---

## 工作流程 1：定期任务隔离

为防止背景任务导致主要对话上下文膨胀，请始终将它们隔离起来。

### 步骤

1. 找到您的 `openclaw.json` 配置文件。
2. 在 `cron_jobs` 数组中，为不需要包含在主要聊天历史记录中的任务设置 `sessionTarget: "isolated"`。
3. 如果需要人工干预，请在任务的有效载荷中使用 `message` 工具。

### 示例配置

```json
{
  "cron": {
    "jobs": [
      {
        "name": "Background Check",
        "schedule": { "kind": "every", "everyMs": 1800000 },
        "sessionTarget": "isolated",
        "payload": {
          "kind": "agentTurn",
          "message": "Check for updates. If found, use message tool to notify user.",
          "deliver": true
        }
      }
    ]
  }
}
```

### 关键点

- `sessionTarget: "isolated"` 使任务在单独的、临时的会话中运行。
- 使用 `deliver: true` 将结果发送回主频道。
- 隔离的会话不会通过心跳信号或历史记录更新来污染您的主上下文。

---

## 工作流程 2：重置与汇总（“数字灵魂”协议）

当您的上下文使用量（通过 `📊 session_status` 查看）超过 100,000 个令牌时，执行手动汇总操作。

### 步骤

1. **检查上下文**：运行 `📊 session_status` 以查看当前的令牌使用情况。
2. **扫描历史记录**：查看当前会话中的新信息、偏好设置或项目更新。
3. **更新 MEMORY.md**：将这些新信息添加到长期存储文件中。
4. **每日日志**：确保 `memory/YYYY-MM-DD.md` 文件包含当天的事件。
5. **重启**：运行 `openclaw gateway restart` 以清除活动历史记录。

### 触发条件

- 上下文使用量超过 100,000 个令牌。
- 会话运行时间超过几天。
- 响应明显变慢。
- 用户明确请求“重新开始”。

---

## 工作流程 3：本地检索架构（Local RAG）配置

为了高效检索信息而不消耗过多令牌，请配置本地嵌入模型。

### 配置（`openclaw.json`）

```json
{
  "memorySearch": {
    "embedding": {
      "provider": "local",
      "model": "hf:second-state/All-MiniLM-L6-v2-Embedding-GGUF"
    },
    "store": "sqlite",
    "paths": ["memory/", "MEMORY.md"],
    "extraPaths": []
  }
}
```

### 使用方法

使用 `memory_search` 从日志中检索上下文，而无需加载所有内容：

```
memory_search(query="what did we decide about the API design")
```

该工具会返回包含文件路径和行号的相关片段。您可以使用 `memory_get` 来获取特定部分的内容。

---

## 工作流程 4：会话记录索引（高级）

对会话记录（`.jsonl` 文件）进行索引，以便能够搜索对话历史。

### 工作原理

OpenClaw 将会话记录存储在 `~/.openclaw/sessions/` 目录下。这些记录可以被索引，从而允许您在不加载整个会话内容的情况下查找旧对话。

### 配置方法

将会话记录的路径添加到 `memorySearch.extraPaths` 中：

```json
{
  "memorySearch": {
    "extraPaths": [
      "~/.openclaw/sessions/*.jsonl"
    ]
  }
}
```

### 最佳实践

- 选择性地进行索引（仅索引最近的会话或重要的对话）。
- 使用基于日期的过滤来限制搜索范围。
- 索引完成后，将旧记录归档到冷存储中。

---

## 工作流程 5：混合搜索（向量搜索 + BM25）

结合语义搜索和关键词匹配，以实现更准确的检索结果。

### 为什么采用混合搜索？

| 搜索类型 | 优点 | 缺点 |
|-------------|-----------|------------|
| 向量搜索（语义搜索） | 能找到概念上相似的内容 | 可能会遗漏精确的术语 |
| BM25（关键词搜索） | 能找到精确匹配的内容 | 可能会遗漏同义词或近义词 |
| **混合搜索** | 结合了两者的优点 | 计算成本稍高 |

### 使用方法

当 `memory_search` 返回低置信度的结果时：

1. 尝试使用不同的表述方式重新搜索（利用语义搜索）。
2. 搜索您记得的精确关键词（使用 BM25 搜索方式）。
3. 如有需要，手动合并搜索结果。

### 未来改进

OpenClaw 的 RAG 系统在未来版本中可能会支持原生混合搜索功能。目前，当需要高精度时，请同时运行多个查询。

---

## 故障排除

### “我的上下文增长得太快”

1. 检查 Cron 任务：它们是否被正确隔离？
2. 检查心跳信号的频率：频率过高会导致更多的令牌被使用。
3. 您是否在不必要的情况下加载了大型文件？

### “`memory_search` 没有返回任何结果”

1. 确认 `memorySearch` 已在 `openclaw.json` 中正确配置。
2. 检查嵌入模型是否已下载。
3. 确保内存文件存在并且包含有效内容。

### “重启后上下文仍未清除”

重启会清除会话历史记录，但：

- 系统提示始终会被加载。
- 工作区文件（如 MEMORY.md 等）会被更新为最新内容。
- 这是出于连续性的设计考虑。

---

## 致谢

- **Pépère** (shAde) — 创始概念和文档编写
- **Zayan** (Clément) — 实现和测试

*专为 OpenClaw 社区打造。* 🦦😸
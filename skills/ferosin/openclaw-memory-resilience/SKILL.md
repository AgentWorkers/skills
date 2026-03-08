---
name: openclaw-memory-resilience
description: "配置 OpenClaw 代理的内存，以确保其在数据压缩和会话重启后仍能正常运行。适用场景包括：  
(1) 设置新的 OpenClaw 代理或工作区；  
(2) 代理在会话之间丢失指令或上下文信息；  
(3) 配置数据压缩前的内存刷新策略；  
(4) 设置用于内存存档的文件结构；  
(5) 诊断代理为何会丢失某些信息；  
(6) 调整数据压缩的缓冲空间和上下文剪裁机制。  
该配置涉及三层内存防护机制中的第一层（网关数据压缩配置）和第三层（文件架构）。"
---
# OpenClaw 的内存弹性机制

本文介绍了 OpenClaw 代理中影响内存持久性的两个关键层面。

## 四个内存层级（快速参考）

| 层级 | 作用 | 是否能在压缩过程中保留？ |
|-------|-----------|---------------------|
| 自启动文件（SOUL.md、AGENTS.md 等） | 在每次会话开始时从磁盘加载 | 可以——会从磁盘重新加载 |
| 会话记录（磁盘上的 JSONL 格式数据） | 对话历史记录 | 会丢失部分信息——在压缩过程中会被简化 |
| LLM（大型语言模型）上下文窗口 | 模型当前处理的数据 | 不可以——大小固定，超出容量时会丢失数据 |
| 检索索引（memory_search/QMD） | 用于搜索内存文件的索引 | 可以——会从文件中重新生成 |

**核心原则：** 如果数据没有被写入文件，那么在压缩后这些数据就会丢失。

## 三种故障类型

- **故障类型 A**：指令仅存在于对话中，从未被写入文件。这是最常见的情况。
- **故障类型 B**：数据在压缩过程中被简化或丢失，导致细节丢失。
- **故障类型 C**：会话清理机制删除了旧的工具结果。这种情况是暂时的，数据不会丢失。

**诊断提示：**
- **忘记某个偏好设置？** → 可能是故障类型 A。
- **忘记某个工具返回的结果？** → 可能是故障类型 C。
- **忘记整个对话内容？** → 可能是故障类型 B。

## 第 1 层：网关压缩配置

通过 `gateway config.patch` 进行配置。这是全局默认设置，适用于所有代理：

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard",
        "reserveTokensFloor": 40000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000,
          "systemPrompt": "Session nearing compaction. Store durable memories now.",
          "prompt": "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
        }
      },
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "1h"
      }
    }
  }
}
```

请参阅 `references/config-explained.md`，了解每个配置项的设置原因。

## 第 3 层：文件架构

请参阅 `references/file-architecture.md`，了解完整的文件架构设计，包括自启动文件、每日记录、归档文件以及 QMD 索引的存储方式。

## 上下文信息显示标准

每个代理的 SOUL.md 文件中都会包含这些上下文信息。这有助于您实时了解上下文的填充情况以及压缩次数，从而在内存压缩达到危险水平之前及时采取行动。

```markdown
## Context Management (Auto-Applied)
**Every response:** fetch live status via `session_status`, append footer: `🧠 [used]/[total] ([%]) | 🧹 [compactions]`
- Auto-clear: **85% context** OR **6 compactions**
- Warn: **70% context** OR **4 compactions**
- Before clearing: file critical info to memory, then reset
```

请参阅 `references/context-footer.md`，了解这些信息的重要性以及如何调整相关阈值。

## 问题诊断

在任何 OpenClaw 会话中运行 `/context list` 命令，可以查看：
- 加载了哪些自启动文件及其大小；
- 是否有文件因超过文件大小限制而被截断；
- 总注入字符数与原始字符数的对比情况。

如果发现某个文件被截断：减少该文件的大小，或调整配置文件中的 `bootstrapMaxChars` 值。
如果某个文件完全丢失：检查代理配置中的工作区路径设置。
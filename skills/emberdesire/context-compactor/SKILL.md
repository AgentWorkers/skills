---
name: context-compactor
version: 0.3.8
description: 基于令牌的上下文压缩技术，适用于那些不报告上下文限制的本地模型（如 MLX、lama.cpp、Ollama）。
---

# 上下文压缩器（Context Compactor）

当使用本地模型时，如果这些模型未能正确报告令牌限制或上下文溢出错误，OpenClaw 会自动执行上下文压缩功能。

## 问题所在

云 API（如 Anthropic、OpenAI）会报告上下文溢出错误，从而触发 OpenClaw 的内置压缩机制。然而，本地模型（如 MLX、llama.cpp、Ollama）通常会：
- 在上下文超出限制时默默地截断数据；
- 返回无效或错误的信息；
- 无法提供准确的令牌计数。

这会导致在对话内容过长时出现通信异常。

## 解决方案

上下文压缩器会在客户端预估令牌数量，并在达到模型限制之前主动对旧消息进行总结。

## 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│  1. Message arrives                                         │
│  2. before_agent_start hook fires                           │
│  3. Plugin estimates total context tokens                   │
│  4. If over maxTokens:                                      │
│     a. Split into "old" and "recent" messages              │
│     b. Summarize old messages (LLM or fallback)            │
│     c. Inject summary as compacted context                 │
│  5. Agent sees: summary + recent + new message             │
└─────────────────────────────────────────────────────────────┘
```

## 安装

```bash
# One command setup (recommended)
npx jasper-context-compactor setup

# Restart gateway
openclaw gateway restart
```

安装命令会自动完成以下操作：
- 将插件文件复制到 `~/.openclaw/extensions/context-compactor/` 目录；
- 将插件配置添加到 `openclaw.json` 文件中，并设置合理的默认值。

## 配置

在 `openclaw.json` 文件中添加以下配置：

```json
{
  "plugins": {
    "entries": {
      "context-compactor": {
        "enabled": true,
        "config": {
          "maxTokens": 8000,
          "keepRecentTokens": 2000,
          "summaryMaxTokens": 1000,
          "charsPerToken": 4
        }
      }
    }
  }
}
```

### 配置选项

| 选项          | 默认值       | 说明                        |
|-----------------|------------|-----------------------------------------|
| `enabled`     | `true`       | 是否启用该插件                     |
| `maxTokens`     | `8000`      | 压缩前的最大上下文令牌数                 |
| `keepRecentTokens` | `2000`      | 从最近的消息中保留的令牌数量                |
| `summaryMaxTokens` | `1000`      | 摘要中使用的最大令牌数量                 |
| `charsPerToken`   | `4`        | 每个令牌对应的字符数                   |
| `summaryModel`    | （会话模型）    | 用于生成摘要的模型                    |

### 针对不同模型的配置调整

**针对 MLX（8K 上下文模型）的配置：**
```json
{
  "maxTokens": 6000,
  "keepRecentTokens": 1500,
  "charsPerToken": 4
}
```

**针对更大上下文（32K 模型）的配置：**
```json
{
  "maxTokens": 28000,
  "keepRecentTokens": 4000,
  "charsPerToken": 4
}
```

**针对较小上下文（4K 模型）的配置：**
```json
{
  "maxTokens": 3000,
  "keepRecentTokens": 800,
  "charsPerToken": 4
}
```

## 命令

### `/compact-now`

强制清除摘要缓存，并在接收新消息时立即执行压缩操作。

```
/compact-now
```

### `/context-stats`

显示当前的上下文令牌使用情况以及是否需要压缩。

```
/context-stats
```

## 摘要生成流程

当压缩机制被触发时：
1. 将消息分为“旧消息”（需要压缩）和“最近消息”（需要保留）；
2. 使用会话模型（或配置的 `summaryModel`）生成摘要；
3. 将生成的摘要缓存起来，以避免重复生成相同的内容；
4. 在发送消息时将摘要内容前置。

如果 LLM 运行时不可用（例如在启动过程中），则会使用基于截断的备用摘要生成方式。

## 与内置压缩机制的差异

| 功能                | 内置机制       | 上下文压缩器                     |
|------------------|-------------|-----------------------------------------|
| 触发条件            | 模型报告溢出错误     | 令牌数量达到预设阈值                 |
| 是否适用于本地模型        | 不适用（需要溢出错误）   | 可以                         |
| 是否保存在转录文本中       | 可以         | 仅保存在会话数据中                   |
| 摘要生成方式          | 使用 Pi 运行时      | 通过插件调用 LLM 进行生成                 |

上下文压缩器起到了补充作用——它能够在问题影响到模型性能之前就提前发现并处理相关问题。

## 故障排除

**摘要质量较差：**
- 尝试更换更合适的 `summaryModel`；
- 增加 `summaryMaxTokens` 的值；
- 如果 LLM 运行时不可用，系统会使用基于截断的备用摘要生成方式。

**压缩操作过于频繁：**
- 增加 `maxTokens` 的值；
- 减少 `keepRecentTokens` 的值（保留更少的旧消息，从而更早触发压缩）。

**未按预期进行压缩：**
- 查看 `/context-stats` 以获取当前的上下文使用情况；
- 确认配置文件中的 `enabled` 选项是否设置为 `true`；
- 检查日志中是否有 `[context-compactor]` 相关的错误信息。

**每个令牌对应的字符数不正确：**
- 默认值 4 适用于英文文本；
- 对于中文和日文等语言，可以尝试使用 3；
- 对于高度技术性的文本，可以尝试使用 5。

## 日志记录

启用调试日志记录：

```json
{
  "plugins": {
    "entries": {
      "context-compactor": {
        "config": {
          "logLevel": "debug"
        }
      }
    }
  }
}
```

关注以下日志信息：
- `[context-compactor] 当前上下文：约 XXXX 个令牌`
- `[context-compactor] 已压缩 X 条消息以生成摘要`

## 链接

- **GitHub 仓库**：https://github.com/E-x-O-Entertainment-Studios-Inc/openclaw-context-compactor
- **OpenClaw 文档**：https://docs.openclaw.ai/concepts/compaction
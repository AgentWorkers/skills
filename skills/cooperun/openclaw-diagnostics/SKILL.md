---
name: openclaw-diagnostics
description: OpenClaw configuration diagnostics and troubleshooting expert. Use when users encounter OpenClaw config issues, channel connection problems, group messages not responding, cron jobs not executing, authentication failures, or need help understanding OpenClaw settings. Triggers: diagnose, troubleshoot, why no reply, config problem, openclaw issue, log analysis.
---

# OpenClaw 诊断工具

这是一个用于 OpenClaw 的配置诊断和故障排除工具，它基于内置的 AI 技术，无需依赖任何外部组件。

## 快速诊断

当用户报告 OpenClaw 相关问题时，可以按照以下步骤进行诊断：

### 1. 收集诊断信息

```bash
~/.openclaw/workspace/skills/openclaw-diagnostics/scripts/get-diagnostic-info.sh
```

### 2. 运行基本检查

```bash
~/.openclaw/workspace/skills/openclaw-diagnostics/scripts/check-common-issues.sh
```

### 3. 根据问题类型进行分析

具体诊断规则请参考 `references/common-issues.md` 文件。

## 诊断工作流程

```
User reports issue
        ↓
Gather info (config + status + logs)
        ↓
Run basic checks
        ↓
Lookup relevant docs from knowledge base
        ↓
Analyze and provide diagnosis
        ↓
Suggest fixes
```

## 知识库

该工具包含一个内置的知识库，其中包含 335 份 OpenClaw 相关的文档。

**存储位置：** `assets/default-snapshot.json`

**文档查找方式：**
1. 阅读 `references/knowledge-base-index.md` 以获取文档的标识符（slug）。
2. 加载 `assets/default-snapshot.json` 文件。
3. 通过 `pages[slug]` 访问相应的文档内容。

**常见文档标识符（Slugs）：**

| 主题 | 文档标识符（Slugs） |
|-------|-------|
| 组消息（Group Messages） | `008888be`, `0bfb808e` |
| 配对（Pairing） | `919c126f` |
| 消息路由（Message Routing） | `a99b0ed8` |
| 自动化故障排除（Automation Troubleshooting） | `a632126a` |
| 认证监控（Auth Monitoring） | `87e3285b` |
| 定时任务（Cron Jobs） | `b239629c` |
| 频道概述（Channels Overview） | `6569d3b4` |
| WhatsApp | `d09047a0` |
| Telegram | `d423ce29` |
| Feishu | `90a33c43` |

### 更新知识库

知识库可以随时更新，以获取最新的 OpenClaw 文档内容。

**使用要求：** 需要网络连接（无需使用大型语言模型，LLM）。

**检查更新：**
```bash
cd ~/.openclaw/workspace/skills/openclaw-diagnostics
npx tsx scripts/update-knowledge-base.ts --check
```

**更新至最新版本：**
```bash
cd ~/.openclaw/workspace/skills/openclaw-diagnostics
npx tsx scripts/update-knowledge-base.ts
```

**强制更新：**
```bash
npx tsx scripts/update-knowledge-base.ts --force
```

**工具特点：**
- 根据站点地图（sitemap）的 `lastmod` 字段自动检查版本信息。
- 无需依赖大型语言模型（LLM），轻量且响应速度快。
- 能记住用户之前跳过的版本信息。

## 常见问题及解决方法：

### 组消息（Group Messages）未响应

1. **检查基本设置：**
   - 机器人是否已加入该组？
   - 用户是否在消息中@了机器人？
   - Gateway 是否正在运行？

2. **检查配置：**
   - `ackReactionScope` 的值为 `group-mentions` 时，机器人仅会回复被@的消息。
   - `groupPolicy` 的值为 `open` 时，机器人会响应所有组的消息；设置为 `allowlist` 时，则需要白名单。

3. ⚠️ **注意区分：** `groupPolicy` 的正确值是 `open`，而非 `empty`。

### 私信（DM）未响应

检查机器人的配对状态（pairing）以及 `allowFrom` 配置。

### 定时任务（Cron Jobs）未执行

1. 确认 Gateway 是否正在运行。
2. 检查定时任务的配置表达式。
3. 查看日志以确认任务是否被触发。
4. 检查静音时间设置。

### 频道连接问题

1. 运行 `openclaw status` 命令查看机器人状态。
2. 检查特定频道的配置。
3. 查看日志中是否有错误信息。

## 诊断原则：

1. **先确认基本设置** —— 不要跳过简单的检查步骤。
2. **查看日志** —— 日志通常包含最直接的错误信息。
3. **避免过度诊断** —— 如果配置正确，不要建议进行不必要的“优化”。
4. **引用文档** —— 在诊断过程中引用相关的文档标识符（Slugs）。

## 相关资源：

### 脚本（Scripts）：
- `get-diagnostic-info.sh`：获取配置信息、状态和日志。
- `check-common-issues.sh`：用于检查常见问题。
- `update-knowledge-base.ts`：用于更新知识库（需要 TypeScript 编译）。

### 文件夹（Assets）：
- `default-snapshot.json`：内置的知识库（包含 335 份文档）。
- `update-meta.json`：用于记录更新信息（在首次检查后生成）。

### 参考文档（References）：
- `knowledge-base-index.md`：按类别分类的文档索引。
- `common-issues.md：常见问题的诊断规则。
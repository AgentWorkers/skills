---
name: search-openclaw-docs
description: 在修改任何 `openclaw.json` 文件之前，必须执行此操作。这可以防止由于嵌入的错误模式（anti-patterns）或正确的模式（correct patterns）而导致配置错误。在配置 OpenClaw（包括绑定（bindings）、通道（channels）、会话（sessions）、定时任务（cron）、心跳检测（heartbeat）等功能）或排查配置问题时，请使用此步骤。
metadata:
  openclaw:
    emoji: "📚"
    homepage: https://github.com/karmanverma/search-openclaw-docs
    requires:
      bins: ["node"]
    install:
      - id: "deps"
        kind: "npm"
        package: "better-sqlite3"
        label: "Install better-sqlite3 (SQLite bindings)"
    postInstall: "node scripts/docs-index.js rebuild"
---

# OpenClaw 文档搜索与配置模式

**在修改 `openclaw.json` 之前务必遵循以下规则**：嵌入的配置模式有助于避免配置错误的发生。

**两种搜索模式：**
1. **嵌入式引用**（快速查找）：包含常见的配置模式及其对应的反模式（错误配置示例）。
2. **文档搜索**（备用方式）：可查询完整的 OpenClaw 文档索引。

---

## 🚨 重要提示：请先阅读 `AGENTS.md`

在使用本功能之前，请务必先阅读 `AGENTS.md` 文件：

```bash
cat ~/.openclaw/skills/search-openclaw-docs/AGENTS.md
```

**`AGENTS.md` 包含以下内容：**
- 配置更改的必备工作流程
- 决策树（指导您应参考哪些文档）
- 关键的反模式（错误配置的常见原因）
- 何时不应使用本功能

---

## 决策树

| 任务 | 应采取的操作 |
|------|--------|
| 添加/删除代理绑定 | 阅读 `references/config-bindings.md` |
| 启用/禁用通道 | 阅读 `references/config-channel-management.md` |
| 会话重置设置 | 阅读 `references/config-session-reset.md` |
| 心跳配置 | 阅读 `references/config-heartbeat.md` |
| Cron 作业设置 | 阅读 `references/config-cron.md` |
| 配置更新后出现问题 | 阅读 `references/troubleshooting-config-breaks.md` |
| 配置最佳实践 | 阅读 `references/best-practices-config.md` |
| 版本迁移（2026.2.9） | 阅读 `references/migration-2026-2-9.md` |
| 其他配置相关问题 | 在文档中查找答案 |

---

## 嵌入式引用（共 8 个文件）

**配置模式文档：**
- `config-bindings.md`：代理路由配置（关键配置）
- `config-channel-management.md`：通道的启用/禁用设置（关键配置）
- `config-session-reset.md`：会话生命周期管理（重要配置）
- `config-heartbeat.md`：主动监控配置（中等重要性）
- `config-cron.md`：定时任务配置（中等重要性）

**辅助文档：**
- `troubleshooting-config-breaks.md`：配置错误的排查方法（关键文档）
- `best-practices-config.md`：安全的配置模式（重要文档）
- `migration-2026-2-9.md`：版本更新指南（中等重要性）

**每份文档都包含：**
- ✅ 正确的配置模式
- ❌ 常见的错误配置方式
- 错误配置的后果
- 配置示例

---

## 使用场景

| 情况 | 应采取的操作 |
|----------|--------|
| 在修改 `openclaw.json` 之前 | ✅ 先阅读相关文档 |
| 配置更改后出现问题 | ✅ 查阅故障排查文档 |
| 学习 OpenClaw 的配置规则 | ✅ 阅读最佳实践文档 |
- 仅依赖个人记忆或上下文时 | ❌ 可使用 `memory_search` 功能 |
- 与 Supabase 或 PostgreSQL 相关的问题 | ❌ 可参考 `supabase-postgres-best-practices` 文档 |
- Next.js 代码相关问题 | ❌ 可参考 `next-best-practices` 文档 |

---

## 文档搜索（备用方式）

对于未在嵌入式引用中提及的主题，您可以直接在完整文档中进行搜索：

```bash
# Search
node ~/.openclaw/skills/search-openclaw-docs/scripts/docs-search.js "discord requireMention"

# Check index health
node ~/.openclaw/skills/search-openclaw-docs/scripts/docs-status.js

# Rebuild (after OpenClaw update)
node ~/.openclaw/skills/search-openclaw-docs/scripts/docs-index.js rebuild
```

## 使用示例

```bash
# Config question
node scripts/docs-search.js "discord requireMention"

# Troubleshooting  
node scripts/docs-search.js "webhook not working"

# More results
node scripts/docs-search.js "providers" --top=5

# JSON output
node scripts/docs-search.js "heartbeat" --json
```

## 输出格式

```
🔍 Query: discord only respond when mentioned

🎯 Best match:
   channels/discord.md
   "Discord (Bot API)"
   Keywords: discord, requiremention
   Score: 0.70

📄 Also relevant:
   concepts/groups.md (0.66)

💡 Read with:
   cat /usr/lib/node_modules/openclaw/docs/channels/discord.md
```

## 工作原理：
- 使用 FTS5 算法对文档标题、头部内容及配置键进行关键词匹配。
- 支持驼峰式命名（CamelCase）的术语（例如 `requireMention`）。
- 采用 Porter 规则进行词干提取，以实现更灵活的匹配效果。
- 完全离线操作，无需网络连接。

## 文档索引位置：
- **索引文件**：`~/.openclaw/docs-index/openclaw-docs.sqlite`
- **文档目录**：`/usr/lib/node_modules/openclaw/docs/`

索引会根据您使用的 OpenClaw 版本自动生成。

## 故障排查：
- **无结果或结果错误**：请检查搜索条件或检查索引文件是否完整。

---

## 集成方式

```javascript
const { search } = require('./lib/search');
const INDEX = process.env.HOME + '/.openclaw/docs-index/openclaw-docs.sqlite';

const results = await search(INDEX, "discord webhook");
// results[0].path → full path to read
```
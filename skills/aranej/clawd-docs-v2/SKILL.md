---
name: clawd-docs-v2
description: **Smart ClawdBot 文档访问功能：**  
支持本地搜索索引、缓存片段以及按需获取文档内容。该系统在处理令牌（token）时高效节能，并能实时监控文档的更新状态，确保用户始终获取到最新信息。
homepage: https://docs.clawd.bot/
metadata: {"clawdbot":{"emoji":"📚"}}
version: 2.2.0
---

# Clawd-Docs v2.0 - 智能文档访问系统

本功能提供了对ClawdBot文档的智能访问方式，包括以下特性：

- **本地搜索索引**：支持即时关键词查找（无需发送任何请求）。
- **缓存片段**：预先加载常见的文档内容（约300-500个字符）。
- **按需获取**：在需要时可以获取完整页面内容（约8000-12000个字符）。
- **新鲜度跟踪**：根据页面类型设置不同的过期时间（TTL）。

---

## 快速入门

### 第一步：先查看“黄金片段”

在获取任何文档内容之前，请先检查是否存在“黄金片段”（即预先缓存的常用文档片段）：

```bash
ls ~/clawd/data/docs-snippets/
```

**可用的文档片段（请先检查缓存！）：**
| 文档片段 | 相关查询 |
|---------|---------------|
| `telegram-setup.md` | “如何设置Telegram” |
| `telegram-allowfrom.md` | “允许谁给我发送消息” |
| `oauth-troubleshoot.md` | “令牌过期” |
| `update-procedure.md` | “如何更新ClawdBot” |
| `restart-gateway.md` | “重启ClawdBot” |
| `config-basics.md` | “配置设置” |
| `config-providers.md` | “添加新的通信渠道” |
| `memory-search.md` | “内存管理” |

**阅读文档片段：**
```bash
cat ~/clawd/data/docs-snippets/telegram-setup.md
```

### 第二步：搜索索引（如果片段不存在）

查看`~/clawd/data/docs-index.json`文件以获取页面推荐内容。

**关键词匹配规则：**
- “telegram” → 查找与“channels/telegram”相关的文档
- “oauth” → 查找与“concepts/oauth”或“gateway/troubleshooting”相关的文档
- “update” → 查找与“install/updating”相关的文档
- “config” → 查找与“gateway/configuration”相关的文档

### 第三步：检查页面缓存

在通过`brightdata`获取文档内容之前，请先检查该页面是否已被缓存：

```bash
# Convert path: concepts/memory → concepts_memory.md
ls ~/clawd/data/docs-cache/ | grep "concepts_memory"
```

**如果页面已缓存，则直接在本地读取（无需发送请求）：**
```bash
cat ~/clawd/data/docs-cache/concepts_memory.md
```

### 第四步：获取页面内容（仅在未缓存的情况下）

使用Clawdbot核心中的`web_fetch`工具（免费且速度快！）：

```javascript
web_fetch({ url: "https://docs.clawd.bot/{path}", extractMode: "markdown" })
```

**示例：**
```javascript
web_fetch({ url: "https://docs.clawd.bot/tools/skills", extractMode: "markdown" })
```

**`web_fetch`的优势：**
| | web_fetch | brightdata |
|---|-----------|------------|
| **成本** | 免费！ | 每次请求约0.003美元 |
| **速度** | 约400毫秒 | 约2-5秒 |
| **格式** | Markdown格式 | Markdown格式 |

---

## 搜索索引结构

**文件位置：`~/clawd/data/docs-index.json`**

**使用同义词进行模糊匹配。**

---

## 新鲜度策略（TTL）

| 页面类别 | 过期时间（TTL） | 原因 |
|---------------|-----|-----|
| `install/updating` | 1天 | 内容经常更新 |
| `gateway/*` | 7天 | 配置设置可能变化 |
| `channels/*` | 7天 | 通信渠道可能更新 |
| `tools/*` | 7天 | 新功能可能添加 |
| `concepts/*` | 14天 | 内容变化较少 |
| `reference/*` | 30天 | 模板内容相对稳定 |

**检查文档片段的过期时间：**
```bash
head -10 ~/clawd/data/docs-snippets/telegram-setup.md | grep expires
```

---

## 常见使用场景

- **“如何设置Telegram？”** → 请阅读`~/clawd/data/docs-snippets/telegram-setup.md`
- **“allowFrom”功能无法使用？”** → 请阅读`~/clawd/data/docs-snippets/telegram-allowfrom.md`
- **“令牌过期/OAuth错误？”** → 请阅读`~/clawd/data/docs-snippets/oauth-troubleshoot.md`
- **“如何更新ClawdBot？”** → 请阅读`~/clawd/data/docs-snippets/update-procedure.md`
- **“如何添加新功能？”** （如果相关文档片段不存在） → 先搜索索引，然后使用`web_fetch`获取`https://docs.clawd.bot/tools/skills`页面
- **“多代理路由”** → 先搜索索引，然后使用`web_fetch`获取`https://docs.clawd.bot/concepts/multi-agent`页面

---

## 备用方案：刷新整个索引

如果找不到所需内容，系统会返回所有文档页面的完整列表。

---

## 令牌使用效率指南

| 方法 | 使用的字符数 | 适用场景 |
|--------|--------|-------------|
| **黄金片段** | 约300-500个字符 | 始终优先使用！ |
| **搜索索引** | 0个字符 | 用于关键词查找 |
| **获取完整页面** | 约8000-12000个字符 | 最后才使用 |
| **批量获取** | 约20-30000个字符 | 用于获取多个相关文档 |

**80-90%的查询请求可以通过缓存片段得到快速响应！**

---

## 数据存储位置

```
~/clawd/data/
├── docs-index.json       # Search index
├── docs-stats.json       # Usage tracking
├── docs-snippets/        # Cached Golden Snippets
│   ├── telegram-setup.md
│   ├── telegram-allowfrom.md
│   ├── oauth-troubleshoot.md
│   ├── update-procedure.md
│   ├── restart-gateway.md
│   └── config-basics.md
└── docs-cache/           # Full page cache (future)
```

---

## 版本信息

| 项目 | 值 |
|------|-------|
| **技能版本** | 2.1.0 |
| **创建时间** | 2026-01-14 |
| **更新时间** | 2026-01-26 |
| **开发者** | Claude Code + Clawd（合作开发） |
| **来源** | https://docs.clawd.bot/ |
| **依赖库** | `web_fetch`（Clawdbot核心工具） |
| **索引页面数量** | 约50个核心文档页面 |
| **预缓存的黄金片段数量** | 7个 |

---

## 更新日志

### v2.2.0 (2026-01-26)
- **使用`web_fetch`替代`brightdata MCP`：** 更快（约400毫秒 vs 2-5秒），且完全免费。
- **无需外部依赖**：不再需要`mcporter`。
- **开发过程**：Claude Code负责实现，Clawd参与审查。

### v2.1.3 (2026-01-25) - ClawdHub相关更新
- 文档格式说明进行了优化。

### v2.0.0 (2026-01-14)
- 采用三层架构：搜索索引 → 文档片段 → 按需获取。
- 常用查询的文档片段被预先缓存。
- 实现了基于TTL的新鲜度跟踪机制。
- 支持使用同义词进行模糊匹配。
- 常见查询的字符使用量减少了80-90%。

### v1.0.0 (2026-01-08)
- 初始版本，仅使用`brightdata`进行文档获取。

---

*本功能提供智能的文档访问体验：优先显示缓存片段，仅在必要时才获取完整页面内容。*
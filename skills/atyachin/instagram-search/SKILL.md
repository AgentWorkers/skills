---
name: instagram-search
description: "**Instagram搜索功能**  
您可以搜索超过4亿条Instagram帖子、Reels内容以及用户资料。该功能支持查找网红、追踪热门标签、分析用户互动数据，并支持数据导出。无需使用Instagram的API或Meta开发者账户，仅需通过Xpoz MCP平台即可实现所有操作。"
homepage: https://xpoz.ai
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["mcporter"], "skills": ["xpoz-setup"], "network": ["mcp.xpoz.ai"], "credentials": "Xpoz account (free tier) — auth via xpoz-setup skill (OAuth 2.1)" },
        "install": [{"id": "node", "kind": "node", "package": "mcporter", "bins": ["mcporter"], "label": "Install mcporter (npm)"}],
      },
  }
tags:
  - instagram
  - instagram-search
  - instagram-api
  - reels
  - influencer
  - hashtag
  - social-media
  - mcp
  - xpoz
  - research
  - discovery
---

# Instagram搜索

**搜索4亿多条Instagram帖子和Reels——包括文字说明和视频字幕。**

您可以找到网红、追踪话题标签、发现内容趋势，并导出搜索结果。无需Meta开发者账户，无需设置Instagram Graph API，也无需经过应用审核流程。

---

## ⚡ 设置

👉 **关注 [`xpoz-setup`](https://clawhub.ai/skills/xpoz-setup)` — 该工具会自动处理身份验证。

---

## 使用方法

运行 `xpoz-setup` 工具。验证身份：`mcporter call xpoz.checkAccessKeyStatus`

## 可用的搜索功能

| 工具 | 功能 |
|------|-------------|
| `getInstagramPostsByKeywords` | 通过关键词搜索帖子和Reels |
| `getInstagramUsersByKeywords` | 查找发布特定主题内容的用户 |
| `getInstagramUser` | 查找特定用户的资料 |
| `searchInstagramUsers` | 通过显示名称查找用户 |
| `getInstagramPostsByAuthor` | 获取用户的全部帖子历史 |

---

## 快速示例

### 搜索帖子和Reels

```bash
mcporter call xpoz.getInstagramPostsByKeywords \
  query="sustainable fashion" \
  startDate=2026-01-01 \
  limit=100

# Poll for results:
mcporter call xpoz.checkOperationStatus operationId=op_abc123
```

Xpoz同时索引了**文字说明**和**视频字幕**，因此您可以依据用户实际所说的内容来查找Reels，而不仅仅是他们输入的文字。

### 按主题查找网红

```bash
mcporter call xpoz.getInstagramUsersByKeywords \
  query="fitness transformation OR workout routine" \
  limit=200
```

### 查找用户资料

```bash
mcporter call xpoz.getInstagramUser \
  identifier=natgeo \
  identifierType=username
```

### 按显示名称搜索

```bash
mcporter call xpoz.searchInstagramUsers query="National Geographic" limit=20
```

---

## 布尔查询

```bash
mcporter call xpoz.getInstagramPostsByKeywords \
  query="(vegan OR plant-based) AND recipe NOT sponsored"
```

---

## CSV导出

每次搜索都会生成完整的导出文件。可以通过 `dataDumpExportOperationId` 获取CSV下载链接（最多可导出64,000行数据）。

---

## 为什么不用Instagram的API直接搜索？

| | Instagram Graph API | Xpoz Instagram搜索 |
|--|-------------------|----------------------|
| **设置要求** | 需要Meta开发者账户且需应用审核 | 一键完成身份验证 |
| **关键词搜索** | 不支持 | 支持全文搜索及字幕显示 |
| **查找网红** | 仅能通过用户名查找 | 可按主题或内容搜索 |
| **Reels内容** | 仅提供元数据 | 提供文字说明和语音内容 |
| **导出方式** | 需手动分页 | 支持一键导出CSV文件 |
| **成本** | 免费，但设置过程较复杂 | 提供免费试用版本 |

Instagram Graph API根本不支持关键词搜索功能，Xpoz填补了这一空白。

---

## 相关工具

- **[xpoz-social-search](https://clawhub.ai/skills/xpoz-social-search)** — 跨平台搜索（Twitter + Instagram + Reddit）
- **[expert-finder](https://clawhub.ai/skills/expert-finder)** — 寻找领域专家 |
- **[social-lead-gen](https://clawhub.ai/skills/social-lead-gen)** — 寻找潜在客户 |

---

**官方网站：** [xpoz.ai](https://xpoz.ai) • **提供免费试用版本** • 无需Meta开发者账户

由ClawHub开发 • 2026年发布
---
name: local-web-search
description: 这是一个免费的、私有的、实时的OpenClaw网络搜索工具——完全不需要任何API密钥。该工具由自托管的SearXNG和Scrapling反机器人引擎提供支持。它支持多引擎并行搜索（包括Bing、DuckDuckGo、Google、Startpage和Qwant），具备意图识别功能（Agent Reach），以及三层级的浏览/查看机制（Fetcher → StealthyFetcher → DynamicFetcher，适用于Cloudflare和JavaScript网站）。此外，它还具备跨引擎的反错误验证机制（cross-engine anti-hallucination validation），并在必要时会自动切换到公共搜索资源（public fallback）。
homepage: https://github.com/wd041216-bit/openclaw-free-web-search
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      env: []
    files: ["scripts/*"]
---
# 本地免费网络搜索 v3.0

当用户需要获取当前或实时的网络信息时，可以使用此技能。

该技能基于 **Scrapling**（反爬虫技术）和 **SearXNG**（自托管搜索引擎）实现，完全在本地运行，无需任何 API 密钥或费用。

---

## 外部端点

| 端点 | 发送的数据 | 用途 |
|---|---|---|
| `http://127.0.0.1:18080`（本地） | 仅搜索查询字符串 | 本地 SearXNG 实例 |
| `https://searx.be`（仅作为备用） | 仅搜索查询字符串 | 当本地 SearXNG 停用时的公共备用方案 |
| 传递给 `browse_page.py` 的任何 URL | 仅 HTTP GET 请求 | 获取页面内容以供阅读 |

所有数据（包括个人信息、凭证或对话历史）都不会被发送到任何外部端点。

---

## 安全性与隐私

- 所有搜索请求默认发送到您的本地 SearXNG 实例，不会被第三方追踪。
- 公共备用端点 (`searx.be`) 仅在本地服务不可用时使用，并且仅接收原始查询字符串。
- `browse_page.py` 仅向您指定的 URL 发送标准 HTTP GET 请求，不会上传任何数据。
- 所有数据抓取操作都在本地完成，不会使用云 API 或进行遥测。
- 无需也不存储任何 API 密钥。
- 用户的对话历史和个人数据不会离开您的设备。

**信任声明：** 该技能会将搜索请求发送到您的本地 SearXNG 实例（默认）或 `searx.be`（备用方案）。页面内容通过标准 HTTP GET 请求获取。除非您信任 `searx.be` 上的公共 SearXNG 服务，否则请勿安装此技能。

---

## 模型调用说明

当需要实时网络信息时，该技能会由代理自动调用。您可以通过从工作空间中移除此技能来禁用自动调用功能。代理仅会在确定需要实时信息时才会使用该技能。

---

## 工具 1 — 网络搜索

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/search_local_web.py \
  --query "YOUR QUERY" \
  --intent general \
  --limit 5
```

**意图选项**（用于控制搜索引擎选择和查询扩展）：

| 意图 | 适用场景 |
|---|---|
| `general` | 默认选项，适用于多种查询类型 |
| `factual` | 查找事实、定义、官方文档 |
| `news` | 最新事件、突发新闻 |
| `research` | 文章、GitHub 资源、技术相关内容 |
| `tutorial` | 教程指南、代码示例 |
| `comparison` | A 与 B 的对比、优缺点分析 |
| `privacy` | 敏感查询（如 ddg、startpage、qwant） |

**附加参数：**

| 参数 | 说明 |
|---|---|
| `--engines bing,duckduckgo,...` | 替换默认搜索引擎 |
| `--freshness hour\|day\|week\|month\|year` | 按时间新鲜度筛选结果 |
| `--max-age-days N` | 过期超过 N 天的结果将被排除 |
| `--browse` | 使用 `browse_page.py` 自动获取顶部结果 |
| `--no-expand` | 禁用查询扩展功能 |
| `--json` | 以机器可读的 JSON 格式输出结果 |

---

## 工具 2 — 浏览/查看页面内容（完整页面）

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/browse_page.py \
  --url "https://example.com/article" \
  --max-words 600
```

**获取器模式**（使用 `--mode` 参数进行选择）：

| 模式 | 获取器 | 适用场景 |
|---|---|---|
| `auto` | 依次尝试 Tier 1 → 2 → 3 的获取器 | 默认模式，优先选择快速响应的获取器 |
| `fast` | `Fetcher` | 适用于普通网站 |
| `stealth` | `StealthyFetcher` | 适用于使用 Cloudflare 或反爬虫技术的网站 |
| `dynamic` | `DynamicFetcher` | 适用于包含大量 JavaScript 或单页应用程序 (SPA) 的网站 |

返回结果包括：页面标题、发布日期、字数、置信度（高/中/低）、提取的完整文本以及防伪提示。

---

## 推荐工作流程

1. 运行 `search_local_web.py`，根据分数和 `[cross-validated]` 标签筛选结果。
2. 对于排名最高的 URL，运行 `browse_page.py` 检查其置信度。
3. 如果置信度较低（如因付费墙或被屏蔽），尝试使用 `--mode stealth` 重新获取结果，或尝试下一个 URL。
4. 仅在使用高置信度的页面内容后给出答案。
5. **切勿仅依据片段内容来陈述事实**。

---

## 规则

- 始终使用 `--intent` 参数来指定查询类型，以获得最佳结果。
- 当本地 SearXNG 不可用时，两个脚本会自动切换到 `searx.be`。
- 如果备用方案也失败，请提示用户启动本地 SearXNG。

---

---  
**注意事项：**  
- 如果所有数据来源均无法使用，请勿伪造搜索结果。  
- `search_local_web.py` 和 `browse_page.py` 是互补工具：先搜索，再浏览。  
- 对于需要验证的事实性内容，请优先选择在多个搜索引擎中都出现的结果（标记为 `[cross-validated]`）。  
- 对于使用 Cloudflare 或需要加载 JavaScript 的网站，请使用 `browse_page.py --mode stealth`。
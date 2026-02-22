---
name: solo-seo-audit
description: >
  **URL的SEO健康检查工具**  
  该工具用于分析URL的元标签（meta tags）、OpenGraph元数据（OG meta data）、JSON-LD结构、站点地图（sitemap）、robots.txt文件内容，以及该URL在搜索引擎结果页（SERP）中的排名情况，并给出0-100分的评分。适用于用户请求“检查SEO”、“审核此页面”、“获取SEO评分”或“检查元标签”等场景。  
  **注意：**  
  - 请勿使用该工具生成用于网站首页（landing page）的内容（请使用 `/landing-gen` 工具），也不适用于生成社交媒体帖子（请使用 `/content-gen` 工具）。
license: MIT
metadata:
  author: fortunto2
  version: "1.1.1"
  openclaw:
    emoji: "📊"
allowed-tools: Read, Grep, Bash, Glob, Write, WebSearch, WebFetch, AskUserQuestion, mcp__solograph__web_search, mcp__solograph__project_info
argument-hint: "<url or project-name>"
---
# /seo-audit

这是一个用于检查任何URL或项目登录页的SEO健康状况的工具。它会获取页面内容，分析元标签、Open Graph标签、JSON-LD数据、站点地图（sitemap）、robots.txt文件，并检查目标关键词在搜索引擎结果页（SERP）中的排名情况，最后生成一份评分报告。

## MCP工具（如果可用，请使用）

- `web_search(query, engines, include_raw_content)` — 检查目标URL在搜索引擎结果页中的排名情况，并分析竞争对手
- `project_info(name)` — 如果按项目名称进行审计，可以获取项目的URL

如果MCP工具不可用，可以使用Claude WebSearch/WebFetch作为替代方案。

## 步骤

1. 从 `$ARGUMENTS` 中获取目标URL或项目名称：
   - 如果是URL（以 `http` 开头）：直接使用该URL。
   - 如果是项目名称：从项目的README文件、CLAUDE.md文件或`docs/prd.md`文件中查找对应的URL。
   - 如果目标信息为空：通过AskUserQuestion询问用户：“要审计哪个URL或项目？”

2. 使用WebFetch获取页面内容，并提取以下信息：
   - `<title>` 标签（理想长度为50-60个字符）
   - `<meta name="description">` 标签（理想长度为150-160个字符）
   - Open Graph标签：`og:title`、`og:description`、`og:image`、`og:url`、`og:type`
   - Twitter Card标签：`twitter:card`、`twitter:title`、`twitter:image`
   - JSON-LD结构化数据（`<script type="application/ld+json">`）
   - `<link rel="canonical">` 标签（用于指定页面的规范URL）
   - `<html lang="...">` 标签（用于指定页面的语言）
   - `<link rel="alternate" hreflang="...">` 标签（用于多语言支持）
   - 标题层级结构：必须有一个H1标签，且H2-H3标签层次结构清晰

3. 检查基础设施文件：
   - 获取 `{origin}/sitemap.xml` 文件：是否存在？格式是否正确？页面数量是否合理？
   - 获取 `{origin}/robots.txt` 文件：是否存在？其中是否包含禁止访问的规则？是否在站点地图中引用了该文件？
   - 获取 `{origin}/favicon.ico` 文件：是否存在？

4. 在评分之前进行初步评估：
   - 列出页面中存在的元素。
   - 列出缺失的元素。
   - 识别可能阻碍页面被索引或分享的关键问题。

5. 检查目标URL在搜索引擎结果页（SERP）中的排名情况（针对3-5个关键词）：
   - 从页面标题、元描述和H1标签中提取关键词。
   - 对每个关键词，使用MCP工具 `web_search(query="{keyword}")` 或 WebSearch进行搜索。
   - 记录目标URL在搜索结果中的排名（1-10位，或“未找到”）。
   - 记录每个关键词排名前3的竞争对手URL。

6. 计算评分（0-100分）：
   | 检查项 | 最高分 | 评分标准 |
|-------|-----------|----------|
| 标题标签 | 10 | 存在，长度为50-60个字符，包含目标关键词 |
| 元描述 | 10 | 存在，长度为150-160个字符，内容具有吸引力 |
| Open Graph标签 | 10 | `og:title`、`og:description`、`og:image` 均存在 |
| JSON-LD | 10 | 存在有效的结构化数据 |
| 规范URL | 5 | 存在且正确 |
| 站点地图 | 10 | 存在，格式正确，并在robots.txt中被引用 |
| robots.txt | 5 | 存在，且没有过于宽泛的访问限制规则 |
| 标题层级结构 | 5 | 有一个H1标签，描述性较强 |
| HTTPS | 5 | 网站使用HTTPS协议 |
| 移动设备适配 | 5 | 页面包含viewport标签 |
| 语言设置 | 5 | `<html>` 标签中包含`lang`属性 |
   - 图标 | 5 | 图标文件（favicon.ico）存在 |
| 在SERP中的排名 | 15 | 目标关键词在搜索结果前10位内出现 |

7. 将评分报告写入`docs/seo-audit.md`文件（放在项目对应的目录下），或直接输出到控制台：

   ```markdown
   # SEO Audit: {URL}

   **Date:** {YYYY-MM-DD}
   **Score:** {N}/100

   ## Summary
   {2-3 sentence overview of SEO health}

   ## Checks

   | Check | Status | Score | Details |
   |-------|--------|-------|---------|
   | Title | pass/fail | X/10 | "{actual title}" (N chars) |
   | ... | ... | ... | ... |

   ## SERP Positions

   | Keyword | Position | Top Competitors |
   |---------|----------|----------------|
   | {kw} | #N or N/A | competitor1, competitor2, competitor3 |

   ## Critical Issues
   - {issue with fix recommendation}

   ## Recommendations (Top 3)
   1. {highest impact fix}
   2. {second priority}
   3. {third priority}
   ```

8. 输出评分结果和主要的改进建议。

## 注意事项

- 评分结果仅供参考：80分以上表示页面表现良好，90分以上表示非常优秀。
- SERP排名检查结果是近期的估算值（非实时数据）。
- 在内容更新后或项目发布前定期运行此工具。

## 常见问题及解决方法

### 页面获取失败
**原因**：URL受到身份验证限制、CORS设置影响，或返回非HTML内容。
**解决方法**：确保URL可以公开访问。对于单页应用（SPA），请确认内容是由服务器生成的。

### SERP排名显示“未找到”
**原因**：网站是新建立的，或尚未被搜索引擎收录。
**解决方法**：对于新网站，这是正常现象。将站点地图提交到Google Search Console，2-4周后再重新进行审计。

### 尽管内容不错但评分较低
**原因**：缺少必要的基础设施文件（如站点地图、robots.txt、JSON-LD数据）。
**解决方法**：生成站点地图文件，添加包含站点地图引用的robots.txt文件，并添加JSON-LD结构化数据。
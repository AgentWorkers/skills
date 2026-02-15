---
name: ahrefs-mcp
description: >
  Access Ahrefs SEO data through Model Context Protocol (MCP) for comprehensive SEO analysis, keyword research, backlink analysis, site audits, and competitive intelligence. Use when users mention: (1) SEO-related queries about websites, domains, or URLs, (2) Keyword research, rankings, or search volume data, (3) Backlink analysis or link profiles, (4) Domain metrics (DR, UR, traffic), (5) Competitor analysis or site comparison, (6) Rank tracking or SERP analysis, (7) Content gap analysis, (8) Site Explorer data requests. When uncertain if a query is SEO-related, ask if Ahrefs should be used.
---

# Ahrefs MCP

通过 Model Context Protocol 直接访问 Ahrefs 的实时 SEO 数据，用于分析网站、研究关键词、跟踪排名，并基于数据做出 SEO 决策。

## 首次使用说明

如果您是第一次使用 Ahrefs MCP，请阅读 [references/setup.md](references/setup.md) 以获取完整的连接说明。您需要：
- 一个 Ahrefs 账户（Lite 计划或更高版本）
- 通过远程 MCP 服务器的连接 URL：`https://api.ahrefs.com/mcp/mcp`

设置完成后，请返回此处查看使用指南。

## 核心功能

Ahrefs MCP 提供以下功能：

1. **网站分析工具**（Site Explorer）：域名指标、反向链接、自然流量、引用域名
2. **关键词分析工具**（Keywords Explorer）：搜索量、关键词难度、SERP 分析、相关关键词
3. **排名跟踪工具**（Rank Tracker）：排名跟踪、可见性指标、竞争对手排名
4. **网站审计工具**（Site Audit）：技术 SEO 问题、爬虫数据、网站健康状况
5. **内容分析工具**（Content Explorer）：表现最佳的内容、内容缺口

有关详细功能的详细信息，请参阅 [references/capabilities.md](references/capabilities.md)。

## 使用流程

### 1. 明确需求

确定需要哪些 SEO 数据：
- **域名/URL 分析** → 使用网站分析工具
- **关键词数据** → 使用关键词分析工具
- **排名跟踪** → 使用排名跟踪工具
- **技术 SEO** → 使用网站审计工具
- **内容创意** → 使用内容分析工具

### 2. 向 Ahrefs 提交请求

使用自然语言提交数据请求。示例：

```
"Get backlink profile for example.com"
"What's the search volume for 'best running shoes'?"
"Show me keyword difficulty scores for this list: [keywords]"
"Analyze competitor domains for example.com"
"Get current rankings from rank tracker project 'My Website'"
```

### 3. 分析与呈现

- 以清晰、可操作的格式呈现数据
- 突出关键见解和机会
- 根据分析结果提出下一步建议
- 在必要时跨多个数据点进行关联分析

## 常见工作流程

### 关键词研究 + 跨数据点分析

1. 用户提供关键词列表
2. 向 Ahrefs 查询每个关键词的指标（搜索量、难度、CPC）
3. 呈现综合分析结果
4. 根据标准（难度、搜索量、意图等）帮助确定优先级

详细的工作流程模式请参阅 [references/workflows.md](references/workflows.md)。

### 竞争分析

1. 确定目标域名和竞争对手
2. 比较域名指标（引用域名、自然流量）
3. 分析热门自然搜索关键词
4. 识别内容缺口
5. 提出优化建议

### 网站审计

1. 查看网站的审计数据
2. 按严重程度识别关键问题
3. 根据影响程度优先处理问题
4. 提供技术建议

## 如何解决 Ahrefs 连接问题

如果 MCP 连接未配置：
1. 查看 [references/setup.md](references/setup.md) 中的设置说明
2. 分享连接 URL：`https://api.ahrefs.com/mcp/mcp`
3. 指导用户完成授权流程
4. 在继续使用前测试连接是否正常

## API 使用限制

- 每个计划对每次请求都有行数限制和每月的 API 使用量上限
- 在账户设置 → “限制与使用” 中查看使用情况
- 企业用户可以购买额外的 API 使用量
- 设计高效的查询以节省 API 资源

## 最佳实践

- **具体说明需求**：明确目标域名、时间范围或所需的具体指标
- **批量请求**：在分析多个关键词或域名时，高效地提交数据请求
- **关联数据**：通过跨数据点分析获得更深入的见解
- **提供可操作的输出**：始终提供建议，而不仅仅是原始数据
- **进行大规模数据查询前先确认**：在提交大规模数据请求前确认需求范围
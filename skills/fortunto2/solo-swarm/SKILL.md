---
name: solo-swarm
description: 启动3个并行研究代理（分别负责市场、用户和技术方面），从多个角度同时调查某个想法。适用于用户提出“群组研究”、“并行研究”、“快速调查”、“使用3个代理”或“团队研究”等需求的情况，也可作为对现有研究方法（/research）的快速替代方案。该功能会生成研究报告（research.md）。请勿将其用于个人独立研究（请使用/rsearch），也不适用于想法的评分（请使用/validate）。
license: MIT
metadata:
  author: fortunto2
  version: "1.5.0"
  openclaw:
    emoji: "🐝"
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch, Write, mcp__solograph__web_search, mcp__solograph__kb_search, mcp__solograph__project_info, mcp__solograph__codegraph_query, mcp__solograph__codegraph_explain, mcp__solograph__project_code_search, mcp__solograph__session_search
argument-hint: "[idea name or description]"
---
# /swarm

创建一个代理团队，从多个角度并行研究 `$ARGUMENTS`。

## 团队结构

生成 3 名团队成员，每位成员都有不同的研究重点：

### 1. 市场研究员
研究重点：竞争对手、市场规模、定价模式、商业模式。
- 搜索直接和间接竞争对手
- 查找包含 TAM/SAM/SOM 数据的市场报告
- 分析定价策略和盈利模式
- 识别市场空白和机会
- 在 Product Hunt、G2、Capterra 等平台查找现有产品

### 2. 用户研究员
研究重点：用户痛点、用户反馈、功能需求。
- 在 Reddit 上进行搜索（使用 SearXNG 的 `engines: reddit`、MCP 的 `web_search` 或 WebSearch 的 `site:reddit.com`）
- 在 Hacker News 上搜索技术社区的意见（`site:news.ycombinator.com`）
- 如果 MCP 提供 `session_search` 功能：检查该想法是否在之前的研究会议中已被讨论过
- 查找应用评论和评分
- 提取用户关于产品问题的直接反馈
- 识别未满足的需求和功能需求

### 3. 技术分析师
研究重点：项目的可行性、技术栈、现有解决方案、实施难度。
- 在 GitHub 上搜索开源替代方案（`site:github.com <query>`）
- 评估技术栈选项
- 如果 MCP 提供 `project_info` 功能：检查现有项目中可复用的代码
- 如果 MCP 提供 `codegraph_explain` 功能：获取类似项目的架构概览
- 如果 MCP 提供 `codegraph_query` 功能：查找项目中共享的包
- 如果 MCP 提供 `project_code_search` 功能：搜索项目中可复用的模式、服务或基础设施
- 评估实施难度和时间表

## 搜索后端

团队成员应使用以下工具：
- **MCP `web_search`**（如果可用）——结合 SearXNG 的搜索功能
- **WebSearch**（内置工具）——用于广泛的信息搜索和市场报告获取
- **WebFetch**——用于抓取特定 URL 的详细信息

**域名过滤：** 使用 `site:github.com`、`site:reddit.com` 等进行精确过滤。

如果未使用 MCP，请检查 SearXNG 是否可用：
```bash
curl -sf http://localhost:8013/health && echo "searxng_ok" || echo "searxng_down"
```

## 协调工作

- 每位团队成员将研究结果记录到共享的任务列表中
- 在开始深入研究之前，需要获得团队领导的批准
- 所有成员完成研究后，将结果整合到 `research.md` 文件中
- 使用 `/research` 技能中提供的 `research.md` 格式

## 输出结果

团队完成研究后，负责人应：
1. 整合所有团队成员的研究结果
2. 将 `research.md` 文件保存到 `4-opportunities/<project-name>/`（针对独立创业者的知识库）或 `docs/`（适用于任何项目）
3. 提出“可行”/“不可行”/“需要调整方向”的建议
4. 建议下一步行动：`/validate <idea>`

## 常见问题

### 代理团队无法启动
**原因：`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 环境变量未设置**
**解决方法：** 确保 `.claude/settings.json` 文件中包含 `"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}`。

### 团队成员的研究结果重复
**原因：** 研究领域划分不明确
**解决方法：** 为每位团队成员设定明确的研究重点（市场/用户/技术）。负责人负责整合并消除重复的结果。

### 团队成员无法使用 SearXNG
**原因：** SSH 隧道未启用
**解决方法：** 在启动团队任务之前运行 `make search-tunnel` 命令。如果 SearXNG 不可用，团队成员可切换使用 WebSearch。
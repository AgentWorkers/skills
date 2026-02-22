---
name: solo-swarm
description: 启动3个并行研究代理（分别负责市场、用户和技术方面），从多个角度同时调查某个想法。适用于用户提出“群体研究”、“并行研究”、“快速调查”、“使用3个代理”或“团队研究”等需求的情况，也可作为对常规研究流程的快速替代方案。该功能会生成名为`research.md`的研究报告。请勿将其用于个人独立研究（请使用`/research`功能），也不适用于想法的评估或验证（请使用`/validate`功能）。
license: MIT
metadata:
  author: fortunto2
  version: "1.6.0"
  openclaw:
    emoji: "🐝"
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch, Write, mcp__solograph__web_search, mcp__solograph__kb_search, mcp__solograph__project_info, mcp__solograph__codegraph_query, mcp__solograph__codegraph_explain, mcp__solograph__project_code_search, mcp__solograph__session_search
argument-hint: "[idea name or description]"
---
# /swarm

创建一个代理团队，从多个角度并行研究 `$ARGUMENTS`。

## 团队结构

生成3名团队成员，每位成员都有各自的研究重点：

### 1. 市场研究员
研究重点：竞争对手、市场规模、定价模式、商业模式。
- 搜索直接和间接竞争对手
- 查找包含TAM/SAM/SOM数据的市场报告
- 分析定价策略和盈利模式
- 识别市场空白和机会
- 在Product Hunt、G2、Capterra等平台上搜索现有产品

### 2. 用户研究员
研究重点：用户痛点、用户反馈、功能需求。
- 通过WebSearch（`site:reddit.com <query>`）或在MCP中使用`web_search`功能搜索Reddit上的用户讨论
- 在Hacker News上搜索技术社区的意见
- 如果MCP支持`session_search`功能：检查该想法是否在之前的会议中已被研究过
- 查找应用评论和评分
- 提取用户关于产品不足之处的直接反馈
- 识别未满足的需求和功能需求

### 3. 技术分析师
研究重点：项目的可行性、技术栈、现有解决方案、实施难度。
- 在GitHub上搜索开源替代方案（`site:github.com <query>`）
- 评估技术栈选项
- 如果MCP支持`project_info`功能：检查现有项目中可复用的代码
- 如果MCP支持`codegraph_explain`功能：获取类似项目的架构概览
- 如果MCP支持`codegraph_query`功能：查找项目之间共用的软件包
- 如果MCP支持`project_code_search`功能：在现有项目中搜索可复用的模式、服务或基础设施
- 评估实施难度和所需时间

## 搜索后端

团队成员应使用以下可用的搜索工具：
- **WebSearch**（内置）——用于广泛的信息收集，始终可用
- **WebFetch**——用于抓取特定URL的详细信息，始终可用
- **MCP `web_search`**（如果可用）——提供额外的搜索功能
- **MCP `kb_search`**（如果可用）——在本地知识库中搜索相关内容

**领域过滤：** 使用`site:github.com`、`site:reddit.com`等来获取针对性的搜索结果

## 协调工作

- 每位团队成员将研究结果记录在共享的任务列表中
- 在开始深入研究之前，需要获得团队的批准
- 所有成员完成研究后，将结果整合到`research.md`文件中
- 使用`/research`技能中提供的`research.md`格式

## 输出结果

团队完成研究后，负责人应：
1. 整合三位团队成员的研究结果
2. 将`research.md`文件保存到当前项目目录下的`docs/`文件夹中
3. 提出“可行”/“不可行”/“需要调整方向”的建议
4. 建议下一步行动：`/validate <idea>`

## 常见问题

### 代理团队无法创建
**原因：`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`环境变量未设置**
**解决方法：** 确保`.claude/settings.json`文件中包含`"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}`。

### 团队成员的研究结果重复
**原因：** 研究领域划分不明确
**解决方法：** 为每位团队成员设定明确的研究重点（市场/用户/技术）。负责人负责整合并消除重复的结果。

### Web搜索返回的结果较少
**原因：** 未配置额外的搜索后端
**解决方法：** 团队成员可以依赖内置的WebSearch工具。如果需要更丰富的搜索结果（如Reddit、GitHub、YouTube），可以安装并配置[SearXNG](https://github.com/fortunto2/searxng-docker-tavily-adapter)（私有、自托管、免费），并配置solograph MCP。
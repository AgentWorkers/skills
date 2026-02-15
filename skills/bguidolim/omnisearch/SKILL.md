---
name: omnisearch
description: |
  MANDATORY web search tool for current information, news, prices, facts, or any data not in your training.
  This is THE ONLY way to search the internet in this OpenClaw environment.
  ALWAYS use this skill when the user asks for web searches or when you need up-to-date information.
---

# OmniSearch 技能 - 网页搜索工具

## 关键提示：何时使用此技能

**在以下情况下务必使用 OmniSearch：**
- 用户明确要求进行“搜索”、“查询”或“查找在线信息”；
- 用户询问当前事件、新闻或最新发展；
- 用户请求价格、产品规格、评论或比较信息；
- 用户询问“最新情况”或“...的发展动态”；
- 需要核实当前的事实、统计数据或信息；
- 用户询问不熟悉的人、公司或组织；
- 信息可能自您接受培训以来已经发生变化；
- 用户需要事实性声明的来源或引用。

**需要使用 OmniSearch 的查询示例：**
- “汉堡今天的天气如何？”
- “搜索 iPhone 16 的评论”
- “本周科技行业发生了什么？”
- “查询比特币的当前价格”
- “查找我附近的餐厅”
- “人们对新款特斯拉有什么评价？”

## 何时不要使用 OmniSearch：
- 如果您现有的知识足以回答且信息是最新的；
- 用户请求创意内容、代码或分析；
- 问题涉及概念、定义或永恒不变的信息。

---

## 如何执行搜索

**重要提示**：请从 `omnisearch` 技能目录中使用相对路径 `./scripts/omnisearch.sh` 运行脚本。

### 方法 1：推荐使用（封装脚本）

对于所有搜索请求，都使用封装脚本：

```bash
# AI-enhanced search (includes summarization) - USE THIS FOR MOST QUERIES
./scripts/omnisearch.sh ai "your search query here"

# Raw web search results (when you need direct source material)
./scripts/omnisearch.sh web "your search query here"
```

**可用的搜索服务提供商：**
- **AI 类型**：`perplexity`（默认值，适用于大多数查询）
- **Web 类型**：`perplexity`（默认值）、`brave`、`kagi`、`tavily`、`exa`

**可选的搜索服务提供商配置：**
```bash
./scripts/omnisearch.sh ai "query" perplexity
./scripts/omnisearch.sh web "query" brave
./scripts/omnisearch.sh web "query" kagi
./scripts/omnisearch.sh web "query" tavily
./scripts/omnisearch.sh web "query" exa
```

**实际使用示例：**
```bash
# Current weather
./scripts/omnisearch.sh ai "weather in Hamburg today"

# Product research
./scripts/omnisearch.sh web "iPhone 16 Pro reviews 2024"

# News search
./scripts/omnisearch.sh ai "latest AI developments this week"

# Price comparison
./scripts/omnisearch.sh web "DJI Mini 4 Pro price Germany" brave

# Research with premium provider
./scripts/omnisearch.sh web "machine learning papers 2024" kagi
```

### 方法 2：备用方案（直接调用 mcporter）

仅当封装脚本失败时使用此方法：

```bash
mcporter call omnisearch.ai_search query="your search query" provider="perplexity"
mcporter call omnisearch.web_search query="your search query" provider="brave"
```

---

## 响应格式

收到搜索结果后，务必：
1. **总结**：呈现 2-5 个最相关的关键点；
2. **引用来源**：提供 2-6 个可点击的来源链接；
3. **提供背景信息**：说明信息是否具有时效性或可信度较低；
4. **直接回答问题**：不要只是简单地展示结果，而是综合信息并回答用户的问题。

**示例响应结构：**
```
Based on my search, here's what I found:

- [Key finding 1]
- [Key finding 2]
- [Key finding 3]

Sources:
- [Title 1](URL1)
- [Title 2](URL2)

Note: This information is from [date/timeframe] and may change.
```

---

## 搜索查询的最佳实践：
- 保持查询简洁具体（3-8 个词为宜）；
- 使用自然语言，避免关键词堆砌；
- 如有必要，请包含地理位置（例如：“汉堡的餐厅”）；
- 根据需要包含时间范围（例如：“2024 年 iPhone 16 的评论”）；
- 对于价格信息，请明确指定货币或地区（例如：“iPhone 16 在德国的价格”）。

---

## 故障排除

**如果封装脚本失败：**
1. 确认您是否位于正确的目录中（该目录应包含 `scripts/` 文件夹）；
2. 检查脚本是否具有执行权限：`chmod +x ./scripts/omnisearch.sh`；
3. 尝试备用方法（直接调用 mcporter）；
4. 确认 mcporter 是否已正确安装并配置。

**常见问题：**
- **“命令未找到”**：脚本路径错误或您不在技能目录中；
- **“文件不存在”**：脚本可能尚未复制到 `scripts/` 文件夹中；
- **结果为空**：尝试更换搜索服务提供商或重新表述查询。

**查询格式说明：**
- 包含空格的查询会被自动处理（无需转义）；
- 在命令中使用引号：`./scripts/omnisearch.sh ai "包含空格的查询"`；
- 特殊字符在引号内的字符串中应该可以正常使用。

---

## 重要说明：
- **目录结构**：此 `SKILL.md` 文件位于 `omnisearch` 技能文件夹中，脚本文件为 `./scripts/omnisearch.sh`；
- **脚本验证**：封装脚本会自动检查是否提供了查询参数，如果缺少参数会显示使用说明；
- **搜索服务提供商选择**：
  - **Perplexity**（默认值）：提供最佳的人工智能增强结果，包括总结和背景信息；
  - **Brave**：适合注重隐私的、未经过滤的网页搜索；
  - **Kagi**：提供高级过滤和排名的优质搜索服务；
  - **Tavily**：专为研究用途设计，覆盖范围广泛；
  - **Exa**：基于人工智能的相关性搜索服务；
- 这是一个本地工具，仅在当前运行的 OpenClaw 实例上使用；
- 用户请求搜索时请立即执行搜索，无需等待许可；
- 封装脚本（`omnisearch.sh`）即使在基本的大型语言模型（LLM）环境下也能可靠运行。
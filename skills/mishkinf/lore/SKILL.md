---
name: lore
description: 从 Lore（一个包含引用信息的研究知识库）中搜索并获取知识。
version: "1.0"
user-invocable: false
---

# Lore 知识库

Lore 是一个研究知识库，您可以通过 MCP 工具访问它。该库存储了文档、会议记录、访谈内容以及决策记录，并附带完整的引用信息——不仅仅是摘要，还包括指向原始内容的链接。利用 Lore，您可以根据证据来回答问题，并保留对话中的重要背景信息。

## 何时将内容导入 Lore

每当遇到值得保存的信息时，使用 `ingest` 工具将内容导入 Lore：

- **会议结束后**：当用户分享会议记录、访谈记录或重要文档时，将它们导入 Lore 以便日后能够进行搜索。
- **外部内容**：当您从 Slack、Notion、GitHub、电子邮件或其他系统获取内容时，将相关部分导入 Lore。
- **决策和背景信息**：当做出重要决策或分享对未来对话有用的背景信息时。

务必包含以下信息：
- `source_url`：原始内容的链接（Slack 的永久链接、Notion 页面链接、GitHub 问题链接），用于引用。
- `source_name`：易于理解的标签，例如 “Slack #product-team” 或 “GitHub issue #42”。
- `project`：该内容所属的项目。

导入操作是幂等的——多次使用 `ingest` 函数处理相同的内容是安全的且不会产生额外开销（系统会立即返回 `deduplicated: true` 的结果）。

## 何时在 Lore 中搜索

在回答关于过去决策、用户反馈、项目历史或任何已有记录的内容的问题之前，请执行以下操作：

1. **使用 `search`** 进行快速查询。选择合适的搜索模式：
   - `hybrid`（默认模式）：适用于大多数查询。
   - `keyword`：用于查找精确的术语、名称或标识符。
   - `semantic`：用于概念性查询（例如 “用户的不满” 或 “痛点”）。
2. **仅在需要跨引用多个来源或综合分析结果时使用 `research`**。该功能的成本是 `search` 的 10 倍——请勿将其用于简单的查询。
3. **当需要获取特定文档的完整原文时，使用 `get_source` 并设置 `include_content=true`。

## 何时保留某些见解

对于简短、独立的知识点，使用 `retain` 而不是 `ingest`：
- 关键决策：例如 “我们选择 X 是因为 Y”。
- 综合分析的见解：例如 “3/5 的用户认为 Z 是他们最关心的问题”。
- 需求：例如 “必须支持企业级的单点登录（SSO）”。

## 引用最佳实践

在引用 Lore 中的信息时，请始终注明来源：
- 提及来源的标题和日期。
- 如果可能，请直接引用原文。
- 如果有 `source_url`，请提供原始链接。

## 示例工作流程

**用户询问过去的决策**：
1. `search("authentication approach decisions", project: "my-app")`
2. 如有需要，获取完整来源内容：`get_source(source_id, include_content: true)`
3. 带着引用展示查询结果。

**用户分享会议记录**：
1. `ingest(content: "...", title: "Sprint Planning Jan 15", project: "my-app", source_type: "meeting", source_name: "Google Meet", participants: ["Alice", "Bob"])`
2. 向用户确认内容已成功导入 Lore。

**用户提出广泛的研究问题**：
1. `research(task: "用户对我们的入职流程有何看法？", project: "my-app")`
2. 带着引用展示综合分析的结果。
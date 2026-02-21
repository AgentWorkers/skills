---
name: igpt-email-search
description: 通过 iGPT API 提供安全、用户隔离的语义邮件搜索功能。该功能能够结合语义分析和关键词检索技术，遍历用户的所有 Gmail、Outlook 或 IMAP 收件箱历史记录进行搜索——无需访问 shell 或文件系统，仅使用 API 密钥进行身份验证。搜索结果会按照邮件内容的意义进行排序，而不仅仅是关键词的匹配程度。当用户需要根据主题、参与者、日期范围或邮件内容来查找特定的邮件、对话或信息流时，可以使用此功能。如需进一步分析、生成摘要或进行结构化数据提取，请使用配套技能 `igpt-email-ask`。
homepage: https://igpt.ai/hub/playground/
metadata: {"clawdbot":{"emoji":"📧","requires":{"env":["IGPT_API_KEY"]},"primaryEnv":"IGPT_API_KEY"},"author":"igptai","version":"1.0.0","license":"MIT","tags":["email","search","retrieval","semantic-search","context","productivity"]}
---
# iGPT 邮件搜索

通过邮件内容的含义进行搜索，而不仅仅是关键词。该功能结合了语义搜索和关键词搜索技术，能够遍历用户整个收件箱的历史记录。

## 该技能的功能

该技能通过调用 iGPT 的 `recall/search` 端点来查找用户关联收件箱中的相关邮件和对话记录。搜索引擎具备以下特点：
- 结合了语义向量搜索（理解邮件内容的含义）和关键词匹配（捕捉精确的词汇）；
- 可以搜索用户所有已索引的邮件记录（不受某些服务仅限 90 天时间范围的限制）；
- 支持按时间范围筛选查询结果；
- 返回带有相关性评分的排名结果；
- 如果邮件包含附件，会一并显示附件的引用信息。

请注意，该技能仅用于检索邮件内容，不对其进行解析、总结或提取结构化数据。如需这些功能，请使用配套的 [`igpt-email-ask`](https://clawhub.ai/skills/igpt-email-ask) 技能，它可以通过 iGPT 的上下文引擎来实现分析、总结和结构化数据提取。

## 适用场景

- 查找与特定主题、项目或人员相关的邮件；
- 定位指定时间范围内的邮件记录；
- 检索原始邮件内容以供进一步处理；
- 将邮件信息传递给其他工具或流程；
- 在采取行动前了解关于某个主题的讨论内容；
- 获取与特定联系人或公司的最新通信记录。

## 何时使用 `igpt-email-ask` 而不是本技能

如果您需要摘要或综合性的答案、结构化数据提取、情感分析、跨多个邮件的推理，或者需要理解邮件内容而非仅仅查找邮件，那么请使用 [`igpt-email-ask`](https://clawhub.ai/skills/igpt-email-ask) 而不是本技能。

**使用建议**：如果查询是一个问题，使用 `igpt-email-ask`；如果查询是一个查找操作，使用本技能。

## 先决条件

1. 一个 iGPT API 密钥（可在 https://igpt.ai/hub/apikeys/ 获取）；
2. 已连接的邮件数据源——用户必须通过 `connectors/authorize` 完成 OAuth 授权，搜索才能返回结果；
3. 安装了 Python 3.8 及 `igptai` 包。

## 设置

```bash
pip install igptai
```

将您的 API 密钥设置为环境变量：

```bash
export IGPT_API_KEY="your-api-key-here"
```

## 使用方法

### 基本用法：按主题搜索

```python
from igptai import IGPT
import os

igpt = IGPT(api_key=os.environ["IGPT_API_KEY"], user="user_123")

results = igpt.recall.search(query="board meeting notes")
print(results)
```

返回与查询匹配的相关邮件和对话记录的排名列表，结果按相关性排序。

### 按时间范围搜索

将搜索结果限制在特定的时间范围内：

```python
results = igpt.recall.search(
    query="budget allocation",
    date_from="2026-01-01",
    date_to="2026-01-31"
)
print(results)
```

### 限制搜索结果数量

```python
results = igpt.recall.search(
    query="partnership proposals",
    max_results=10
)
print(results)
```

### 搜索特定人员的邮件

该语义引擎能够理解参与者的上下文：

```python
results = igpt.recall.search(
    query="emails from Sarah about the product launch",
    date_from="2026-01-01"
)
print(results)
```

### 结合 `igpt-email-ask` 实现两步工作流程

常见的使用方式是：先使用本技能搜索以获取初步结果，再使用 `igpt-email-ask` 进行进一步分析：

```python
# Step 1: Find relevant threads
results = igpt.recall.search(
    query="Acme Corp contract negotiation",
    max_results=20
)
print(f"Found {len(results)} relevant threads")

# Step 2: Ask for structured analysis
analysis = igpt.recall.ask(
    input="Summarize the current status of the Acme Corp contract negotiation. What are the open issues and who owns them?",
    output_format="json"
)
print(analysis)
```

## 参数

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| query | 字符串 | 是 | 搜索查询。支持自然语言查询（基于语义理解）和精确关键词查询。 |
| user | 字符串 | 是（或在构造函数中设置） | 用于限定查询范围的唯一用户标识符。 |
| date_from | 字符串 | 否 | 以 YYYY-MM-DD 格式指定的开始日期过滤条件。 |
| date_to | 字符串 | 否 | 以 YYYY-MM-DD 格式指定的结束日期过滤条件。 |
| max_results | 整数 | 否 | 返回的最大结果数量。 |

## 错误处理

该 SDK 采用无异常抛出的设计，错误会以数值形式返回：

```python
results = igpt.recall.search(query="Q4 planning")

if isinstance(results, dict) and results.get("error"):
    error = results["error"]
    if error == "auth":
        print("Check your API key")
    elif error == "params":
        print("Check your request parameters")
    elif error == "network_error":
        print("Network issue, retry")
else:
    for result in results:
        print(result)
```

## 外部接口

该技能仅与以下接口进行通信：
- `https://api.igpt.ai/v1/recall/search` — 搜索接口；
- `https://api.igpt.ai/v1/connectors/authorize` — 仅在初次连接数据源时使用。

不会与其他外部接口交互，也不会将数据发送给任何第三方服务。`igptai` 的 PyPI 包源代码可在 https://github.com/igptai/igptai-python 获取。

## 安全性与隐私

- **API 密钥限制**：所有请求均通过 HTTPS 以Bearer 令牌的形式验证 `IGPT_API_KEY`。无 shell 访问权限、无文件系统访问权限、无系统命令执行权限。
- **用户隔离**：每个查询都针对特定的用户标识符进行。用户 A 无法访问用户 B 的邮件数据。隔离措施在索引和执行层面实施，而非通过过滤层实现。
- **OAuth 仅读权限**：邮件数据源连接使用 OAuth 且仅具有读取权限。该技能不发送、修改或删除邮件。
- **无数据保留**：查询完成后，相关数据会被立即销毁。内存按需重新生成，不会被持久化存储。
- **传输加密**：所有通信均通过 HTTPS 进行。没有明文传输。
- **无本地数据存储**：该技能不会写入磁盘、修改环境文件，也不会在 `IGPT_API_KEY` 环境变量之外创建持久化配置。

有关完整的安全模型，请参阅：https://docs.igpt.ai/docs/security/model。

## 与普通邮件搜索的区别

| 普通邮件/Gmail 搜索 | iGPT 邮件搜索 |
|---|---|
| 仅支持关键词匹配 | 结合语义搜索和关键词搜索 |
| 可能错过使用不同词汇的相关内容 | 理解邮件含义，找到概念上相关的邮件 |
| 仅限于 Gmail 的搜索功能 | 支持自然语言查询 |
| 依赖特定服务提供商（如 Gmail 或 Outlook） | 可搜索所有关联的服务提供商的邮件 |
| 历史记录通常有限（例如 Nylas 服务为 90 天） | 全部邮件记录均被索引 |
| 返回原始 MIME 数据 | 返回结构化、易于阅读的结果 |

## 示例查询

以下查询均支持自然语言输入：
- `"board meeting notes"` — 查找与董事会会议相关的邮件（即使邮件中未包含该确切短语）；
- `"emails about the product launch timeline"` — 基于主题的语义理解进行搜索；
- `"anything from legal about compliance"` — 根据部门和主题进行搜索；
- `"invoices from Q4 2025"` — 结合主题和隐含的时间范围进行搜索；
- `"conversations where deadlines were mentioned"` — 基于概念进行搜索。

## 配套技能

| 技能 | 功能 | 适用场景 |
|-------|-------------|----------------|
| **[igpt-email-ask](https://clawhub.ai/skills/igpt-email-ask)** | 进行推理、总结、结构化数据提取、情感分析 | 当您需要分析结果而非仅仅获取数据时 |
| **igpt-email-search**（本技能） | 结合语义搜索和关键词搜索 | 当您需要查找和检索邮件内容时 |

这两个技能使用相同的 `IGPT_API_KEY` 和关联的数据源。请同时安装这两个技能以实现完整的搜索和分析流程。

## 资源

- **获取 API 密钥**：https://igpt.ai/hub/apikeys/
- **文档**：https://docs.igpt.ai
- **API 参考**：https://docs.igpt.ai/docs/api-reference/search
- **测试平台**：https://igpt.ai/hub/playground/
- **Python SDK**：https://pypi.org/project/igptai/
- **Node.js SDK**：https://www.npmjs.com/package/igptai
- **GitHub**：https://github.com/igptai/igptai-python
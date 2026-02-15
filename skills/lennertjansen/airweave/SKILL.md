---
name: airweave
description: **AI代理的上下文检索层**  
该层用于在用户的各种应用程序中为AI代理提供上下文检索功能。它能够从Airweave数据库中搜索并获取所需的信息。Airweave会对用户应用程序中的数据进行索引和同步，从而确保AI代理能够高效地检索上下文。支持语义搜索、关键词搜索以及基于用户角色的搜索方式。  

**应用场景：**  
- 当用户在Slack、GitHub、Notion、Jira、Confluence、Google Drive、Salesforce、Linear、SharePoint、Stripe等连接的应用程序中查询自己的数据时；  
- 当用户需要从工作空间中查找文档或信息时；  
- 当用户希望基于公司数据获得答案时；  
- 当用户需要你检查应用程序中的数据以完成某项任务时。
metadata: {"clawdbot":{"requires":{"bins":["python3"],"env":["AIRWEAVE_API_KEY","AIRWEAVE_COLLECTION_ID"]},"primaryEnv":"AIRWEAVE_API_KEY"}}
---

# Airweave 搜索

您可以使用位于 `{baseDir}/scripts/search.py` 的搜索脚本，在 Airweave 收集中搜索并检索所需信息。

## 何时进行搜索

**在以下情况下进行搜索：**
- 用户询问其连接的应用程序中的数据（例如：“我们在 Slack 中讨论了什么...”）
- 需要查找文档、消息、问题或记录
- 用户对其工作空间提出事实性问题（例如：“谁负责...”，“我们的政策是...”）
- 用户按名称引用特定工具（例如：“在 Notion 中”，“在 GitHub 上”，“在 Jira 中”）
- 用户需要您查找培训中未包含的最新信息
- 用户要求您检查应用程序数据以获取上下文（例如：“查看我们的 Notion 文档”，“查看 Jira 票据”）

**在以下情况下不要进行搜索：**
- 用户提出一般性知识问题（请参考您的培训资料）
- 用户已在对话中提供了所有所需的上下文
- 问题与 Airweave 本身相关，而非其中的数据

## 查询构建

将用户的意图转化为有效的搜索查询：

| 用户的提问 | 搜索查询 |
|-----------|--------------|
| “Sarah 对产品发布说了什么？” | “Sarah 产品发布” |
| “查找 API 文档” | “API 文档” |
| “这周有报告的错误吗？” | “错误报告问题” |
| “我们的退款政策是什么？” | “退款政策 客户” |

**提示：**
- 使用自然语言——Airweave 支持语义搜索
- 包含上下文信息——例如，“定价反馈”比单纯的“定价”更准确
- 问题要具体，但不要过于狭隘
- 省略诸如“请查找”之类的填充词

## 运行搜索

执行搜索脚本：

```bash
python3 {baseDir}/scripts/search.py "your search query"
```

**可选参数：**
- `--limit N` — 最大结果数量（默认值：20）
- `--temporal N` — 时间相关性范围（0-1，默认值：0；0.7 表示“最近”，1 表示“最新”）
- `--strategy TYPE` — 检索策略：混合式、语义式、关键词式（默认值：混合式）
- `--raw` — 返回原始结果而非 AI 生成的内容
- `--expand` — 启用查询扩展以获得更广泛的结果
- `--rerank` / `--no-rerank` — 切换 LLM 重新排序功能（默认值：开启）

**示例：**

```bash
# Basic search
python3 {baseDir}/scripts/search.py "customer feedback pricing"

# Recent conversations
python3 {baseDir}/scripts/search.py "product launch updates" --temporal 0.8

# Find specific document
python3 {baseDir}/scripts/search.py "API authentication docs" --strategy keyword

# Get raw results for exploration
python3 {baseDir}/scripts/search.py "project status" --limit 30 --raw

# Broad search with query expansion
python3 {baseDir}/scripts/search.py "onboarding" --expand
```

## 处理搜索结果

**解读搜索结果得分：**
- 0.85 及以上 → 高度相关，可放心使用
- 0.70–0.85 → 可能相关，需结合上下文使用
- 0.50–0.70 → 可能相关，需说明不确定性
- 低于 0.50 → 匹配度较低，建议重新表述问题

**向用户展示结果：**
1. 先给出答案，不要以“我找到了 5 个结果”开头
- 引用信息来源（例如：“根据您在 Slack 中的对话...”）
- 综合相关内容，给出连贯的回复
- 如结果未能完全满足需求，要说明这一点

## 处理无结果的情况

如果搜索没有返回有用的结果：
- 扩展查询范围，去掉特定的关键词
- 尝试不同的表述方式
- 增加结果数量
- 请求用户提供更多上下文信息

## 参数参考

详细参数说明请参见 [PARAMETERS.md](references/PARAMETERS.md)。

## 示例

完整的搜索场景示例请参见 [EXAMPLES.md](references/EXAMPLES.md)。
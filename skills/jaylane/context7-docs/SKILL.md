---
name: context7-docs
description: 从 Context7 中获取任何编程库或框架的最新、特定版本的文档和代码示例。当用户需要某个库、包或框架的当前 API 文档、代码示例、设置指南或配置帮助时，可以使用此技能——尤其是在不确定自己的训练数据是否是最新的情况下。当用户提到需要文档、示例，或询问库的 API、版本或配置时，激活该技能。
  Fetches up-to-date, version-specific documentation and code examples for any
  programming library or framework from Context7. Use this skill when the user
  needs current API docs, code examples, setup guides, or configuration help for
  any library, package, or framework — especially when you are unsure if your
  training data is current. Activate when the user mentions needing docs, examples,
  or asks about library APIs, versions, or configuration.
license: MIT
compatibility: Requires curl, jq, and internet access. Optional CONTEXT7_API_KEY env var for higher rate limits.
metadata:
  author: context7
  version: "1.0"
  source: https://github.com/upstash/context7
allowed-tools: Bash(curl:*) Bash(jq:*) Read
---
# Context7 文档查询

## 概述

Context7 提供了数千个编程库和框架的最新、特定版本的文档及代码示例。每当您需要不同于训练数据中的最新文档时（尤其是对于像 Next.js、React、Supabase、LangChain 等发展迅速的库），都可以使用这项技能。

## 何时使用此技能

- 用户询问某个库的 API，而您不确定自己的知识是否是最新的；
- 用户请求某个特定库版本的代码示例；
- 用户需要设置、配置或迁移指南；
- 用户提到“使用 Context7”或请求最新的文档；
- 您需要验证某个 API 或方法是否仍然存在于最新版本中。

## 两步工作流程

### 第一步：获取库 ID

首先，找到用户所询问的库在 Context7 中兼容的库 ID。

```bash
bash scripts/resolve-library.sh --query "How to set up authentication" --library-name "next.js"
```

这将返回一个匹配的库列表，其中包含：
- **库 ID**（例如：`/vercel/next.js`，用于第二步）；
- **名称**和**描述**；
- **代码片段**数量（数量越多越好）；
- **基准测试分数**（满分 100 分，分数越高越好）；
- **源代码信誉**（高、中、低或未知，建议选择高/中等信誉的库）；
- **版本**（例如：`/vercel/next.js/v14.3.0`）。

**选择标准**：
1. 名称相似度（优先选择完全匹配的库）；
2. 描述与用户任务的相关性；
3. 代码片段数量较多；
4. 基准测试分数较高；
5. 源代码信誉较高或中等。

如果用户已经提供了 `/org/project` 格式的库 ID，请跳过此步骤。

### 第二步：查询文档

使用第一步获取的库 ID 来获取相关的文档：

```bash
bash scripts/query-docs.sh --library-id "/vercel/next.js" --query "How to set up authentication with JWT"
```

这将返回与查询直接相关的文档文本及代码示例。

### 快捷方式：直接使用 curl 命令

您也可以直接调用 API，而无需使用脚本：

**搜索库：**
```bash
curl -s "https://context7.com/api/search" \
  -H "Content-Type: application/json" \
  ${CONTEXT7_API_KEY:+-H "Authorization: Bearer $CONTEXT7_API_KEY"} \
  -d '{"query": "How to set up auth", "libraryName": "next.js"}' | jq .
```

**查询文档：**
```bash
curl -s "https://context7.com/api/context" \
  -H "Content-Type: application/json" \
  ${CONTEXT7_API_KEY:+-H "Authorization: Bearer $CONTEXT7_API_KEY"} \
  -d '{"query": "JWT authentication middleware", "libraryId": "/vercel/next.js"}' | jq .
```

## 重要指南

- 每个问题最多调用 `resolve` 3 次。如果找不到所需内容，请使用最佳的结果。
- 每个问题最多调用 `query-docs` 3 次。请使用您掌握的最佳信息。
- 请确保查询具体明确。例如：“如何在 Express.js 中使用 JWT 进行身份验证”；避免使用过于模糊的查询（如“auth”）。
- 在适用的情况下，请指定版本。如果用户指定了版本，请在 `resolve` 的结果中查找该版本，并使用相应的库 ID（例如：`/vercel/next.js/v14.3.0`）。
- **不要在查询中包含敏感数据**（API 密钥、密码等），因为这些数据会被发送到 Context7 API。

## 处理特殊情况

| 情况 | 应对措施 |
|-----------|--------|
| `resolve` 没有返回结果 | 尝试使用不同的库名称或更宽泛的搜索词 |
| 有多个匹配结果 | 选择名称最匹配且代码片段数量最多的库 |
| 用户指定了版本 | 在 `resolve` 的结果中查找对应的版本 ID |
| 文档查询返回空内容 | 尝试使用更具体的查询或更换查询方式 |
| 触发速率限制 | 稍等片刻后重试，或建议用户设置 `CONTEXT7_API_KEY` |

## 环境配置

为了提高查询速率，可以申请一个免费的 API 密钥：

```bash
export CONTEXT7_API_KEY="your-key-here"
```

免费密钥获取地址：https://context7.com/dashboard

## 下一步操作

- 请参阅 [API-REFERENCE.md](references/API-REFERENCE.md) 以获取完整的端点文档。
- 请参阅 [LIBRARY-ID-FORMAT.md](references/LIBRARY-ID-FORMAT.md) 以了解库 ID 的格式和版本信息。
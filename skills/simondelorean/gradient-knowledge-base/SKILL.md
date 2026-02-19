---
name: gradient-knowledge-base
description: >
  **社区技能（非官方）：用于 DigitalOcean Gradient 知识库**  
  **构建 RAG（Retrieval, Augmentation, and Generation）管道：**  
  - 将文档存储在 DigitalOcean 的 DO Spaces（对象存储服务）中；  
  - 配置数据源；  
  - 管理索引；  
  - 运行语义搜索或混合搜索查询。
files: ["scripts/*"]
homepage: https://github.com/Rogue-Iteration/TheBigClaw
metadata:
  clawdbot:
    emoji: "📚"
    primaryEnv: DO_API_TOKEN
    requires:
      env:
        - DO_API_TOKEN
        - DO_SPACES_ACCESS_KEY
        - DO_SPACES_SECRET_KEY
        - GRADIENT_API_KEY
      bins:
        - python3
      pip:
        - requests>=2.31.0
        - boto3>=1.34.0
  author: Rogue Iteration
  version: "0.1.4"
  tags: ["digitalocean", "gradient-ai", "knowledge-base", "rag", "semantic-search", "do-spaces"]
---
# 🦞 Gradient AI — 知识库与检索增强生成（Retrieval-Augmented Generation, RAG）

> ⚠️ **这是一个非官方的社区技能**，并非由 DigitalOcean 维护。使用本技能需自行承担风险。

> “龙虾永远不会忘记。你的智能助手也同样不应忘记。” —— 来自 Knowledge Base 的龙虾

使用 DigitalOcean 的 Gradient 知识库构建一个 [检索增强生成（RAG）** 流程**。将文档存储在 DO Spaces 中，将其索引到由 OpenSearch 支持的知识库中，并通过语义或混合搜索方式查询这些文档。

## 架构

```
Your Agent                   DigitalOcean
┌─────────────┐     upload    ┌──────────────┐
│  Documents  │ ──────────▶  │  DO Spaces   │
└─────────────┘              │  (S3-compat) │
                              └──────┬───────┘
                                     │ auto-index
                              ┌──────▼───────┐
                              │ Knowledge    │
                              │ Base (KBaaS) │
                              │ ┌──────────┐ │
                              │ │OpenSearch│ │
                              │ └──────────┘ │
                              └──────┬───────┘
                                     │ retrieve
┌─────────────┐     answer    ┌──────▼───────┐
│  Your Agent │ ◀──────────  │  RAG Results │
│  + LLM      │              │  + Citations │
└─────────────┘              └──────────────┘
```

📖 *[知识库文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/create-manage-knowledge-bases/)*

## API 端点

此技能连接到三个官方的 DigitalOcean 服务端点：

| 主机名 | 功能 | 文档 |
|----------|---------|------|
| `api.digitalocean.com` | 知识库管理（创建、列出、删除、数据源） | [DO API 参考](https://docs.digitalocean.com/reference/api/) |
| `kbaas.do-ai.run` | 知识库检索 —— 语义/混合搜索查询 | [知识库检索文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/create-manage-knowledge-bases/) |
| `inference.do-ai.run` | 用于 RAG 合成的 LLM 聊天式回答 | [推理文档](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/) |
| `<region>.digitaloceanspaces.com` | 与 S3 兼容的对象存储 | [Spaces 文档](https://docs.digitalocean.com/products/spaces/) |

所有端点均归 DigitalOcean 所有和运营。`*.do-ai.run` 主机名属于 Gradient AI 平台的服务域名。

## 认证

此技能使用 **两种不同的凭证** —— 可以将其视为一种“双爪”认证机制：

| 凭证 | 用途 | 环境变量 |
|------------|----------|---------|
| DO API Token | 知识库管理、索引、查询 | `DO_API_TOKEN` |
| Gradient API Key | 用于 RAG 合成的 LLM 推理 | `GRADIENT_API_KEY` |
| Spaces Keys | 与 S3 兼容的上传操作 | `DO_SPACES_ACCESS_KEY` + `DO_SPACES_SECRET_KEY` |

> **凭证权限设置：** 使用最小权限范围的令牌。为 `GRADIENT_API_KEY` 创建一个专用的 [模型访问密钥](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/manage-access-keys/)。对于 `DO_API_TOKEN`，请使用仅具有知识库和 Spaces 权限的 [受限 API 令牌](https://docs.digitalocean.com/reference/api/create-personal-access-token/)。避免使用您的账户根令牌。

**可选但推荐：**
```bash
export GRADIENT_KB_UUID="your-kb-uuid"     # Default KB for queries
export DO_SPACES_BUCKET="your-bucket"      # Default bucket for uploads
export DO_SPACES_ENDPOINT="https://nyc3.digitaloceanspaces.com"
```

---

## 工具

### 📦 将文档存储在 DO Spaces 中

将文件上传到 DO Spaces 以进行索引。这是存储层——文档在索引之前会先存储在这里。

```bash
# Upload a file
python3 gradient_spaces.py --upload /path/to/report.md --bucket my-kb-data

# Upload with a key prefix (folder structure)
python3 gradient_spaces.py --upload report.md --bucket my-kb-data --prefix "research/2026-02-15/"

# List files in a bucket
python3 gradient_spaces.py --list --bucket my-kb-data

# List files with a prefix filter
python3 gradient_spaces.py --list --bucket my-kb-data --prefix "research/"

# Delete a file
python3 gradient_spaces.py --delete "research/old_report.md" --bucket my-kb-data
```

📖 *[DO Spaces 文档](https://docs.digitalocean.com/products/spaces/)*

---

### 🏗️ 创建和管理知识库

提供对知识库的完整创建、读取、更新和删除（CRUD）操作。可以通过编程方式创建知识库，而无需像传统方式那样通过控制台手动操作。

```bash
# List all Knowledge Bases
python3 gradient_kb_manage.py --list

# Create a new KB
python3 gradient_kb_manage.py --create --name "My Research KB" --region nyc3

# Show details for a specific KB
python3 gradient_kb_manage.py --show --kb-uuid "your-kb-uuid"

# Delete a KB (⚠️ permanent!)
python3 gradient_kb_manage.py --delete --kb-uuid "your-kb-uuid"
```

📖 *[通过 API 创建知识库](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/create-manage-knowledge-bases/)*

---

### 📁 管理数据源

将您的 DO Spaces 存储桶（或网页 URL）连接到知识库。这告诉知识库：“对这些文档进行索引”。

```bash
# Add a DO Spaces data source
python3 gradient_kb_manage.py --add-source \
  --kb-uuid "your-kb-uuid" \
  --bucket my-kb-data \
  --prefix "research/"

# List data sources for a KB
python3 gradient_kb_manage.py --list-sources --kb-uuid "your-kb-uuid"

# Trigger re-indexing (auto-detects the data source)
python3 gradient_kb_manage.py --reindex --kb-uuid "your-kb-uuid"

# Trigger re-indexing for a specific source
python3 gradient_kb_manage.py --reindex --kb-uuid "your-kb-uuid" --source-uuid "ds-uuid"
```

> **🦞 专业提示：自动索引。** 如果您的知识库启用了自动索引功能，就可以跳过手动触发重新索引的步骤。知识库会自动检测 DO Spaces 存储桶中的变化。您可以在 [DigitalOcean 控制台](https://cloud.digitalocean.com) → 知识库 → 设置中进行配置。

---

### 🔍 查询知识库

使用语义或混合查询方式搜索已索引的文档。这就是魔法发生的地方——您的文档将转化为答案。

```bash
# Basic query
python3 gradient_kb_query.py --query "What happened with the Q4 earnings?"

# Control number of results
python3 gradient_kb_query.py --query "Revenue trends" --num-results 20

# Tune hybrid search balance (see below)
python3 gradient_kb_query.py --query "$CAKE price movement" --alpha 0.5

# JSON output (for piping to other tools)
python3 gradient_kb_query.py --query "SEC filings summary" --json
```

**直接 API 调用：**
```bash
curl -s https://kbaas.do-ai.run/v1/{kb-uuid}/retrieve \
  -H "Authorization: Bearer $DO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What happened with Q4 earnings?",
    "num_results": 10,
    "alpha": 0.5
  }'
```

📖 *[知识库检索 API](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/create-manage-knowledge-bases/#query-a-knowledge-base)*

---

### 🎛️ `alpha` 参数 —— 混合搜索调优

`alpha` 参数用于控制 **词汇**（关键词）搜索和 **语义**（含义）搜索之间的平衡：

| Alpha | 行为 | 适用场景 |
|-------|----------|----------|
| `0.0` | 纯词汇搜索（精确匹配关键词） | 例如：股票代码、文件编号、日期 |
| `0.5` | 平衡的混合搜索 | 一般性研究查询 |
| `1.0` | 纯语义搜索（基于含义） | 开放式问题：例如：“发生了什么？”，“总结...” |

> **🦞 使用建议：** 从 `0.5` 开始设置。在搜索特定内容时（如 `$CAKE`、`10-K`、`2026-02-15`）可以降低 `alpha` 值；在探索概念时（如“市场情绪如何？”）可以提高 `alpha` 值。

---

### 🧠 RAG 增强查询

完整的流程如下：查询知识库 → 构建上下文提示 → 调用 LLM 进行合成。通过一个命令即可获得带有引用的完整答案。

```bash
python3 gradient_kb_query.py \
  --query "Summarize all research on $CAKE" \
  --rag \
  --model "openai-gpt-oss-120b"
```

此过程会自动执行以下操作：
1. 🔍 查询知识库以找到相关文档
2. 📝 根据检索到的上下文构建提示
3. 🤖 调用 LLM 合成答案

> **注意：** RAG 查询会在后台调用 [Gradient Inference API](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/)，因此需要设置 `GRADIENT_API_KEY`。如果您同时启用了 `gradient-inference` 技能，那么一切就准备就绪了。

---

## 高级配置

### 嵌入模型与分块

在创建知识库时，您可以选择文档的分块方式：

| 分块策略 | 工作原理 | 适用场景 |
|----------|-------------|----------|
| **基于章节** | 按文档结构（标题、段落）分割 | 结构化报告 |
| **语义分割** | 按语义边界分割 | 叙述性内容 |
| **层次化** | 保持文档的层次结构 | 技术文档 |
| **固定长度** | 所有块大小相同 | 规则化数据 |

您可以在 [DigitalOcean 控制台](https://cloud.digitalocean.com) 中配置这些选项，或通过 API 的 `embedding_model` 和 `chunking` 参数进行设置。

📖 *[知识库配置选项](https://docs.digitalocean.com/products/gradient-ai-platform/details/features/#retrieval-augmented-generation-rag)*

---

## CLI 参考

所有脚本都支持使用 `--json` 选项以生成机器可读的输出。

```
gradient_spaces.py      --upload FILE | --list | --delete KEY
                        [--bucket NAME] [--prefix PATH] [--key KEY] [--json]

gradient_kb_manage.py   --list | --create | --show | --delete
                        | --list-sources | --add-source | --reindex
                        [--kb-uuid UUID] [--source-uuid UUID]
                        [--name NAME] [--region REGION] [--bucket NAME]
                        [--prefix PATH] [--json]

gradient_kb_query.py    --query TEXT [--kb-uuid UUID] [--num-results N]
                        [--alpha F] [--rag] [--model ID] [--json]
```

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `DO_API_TOKEN` | ✅ | DO API 令牌（权限范围：GenAI + Spaces） |
| `DO_SPACES_ACCESS_KEY` | ✅ | Spaces 访问密钥 |
| `DO_SPACES_SECRET_KEY` | ✅ | Spaces 秘密密钥 |
| `DO_SPACES_ENDPOINT` | 可选 | Spaces 端点（默认：`https://nyc3.digitaloceanspaces.com`） |
| `DO_SPACES_BUCKET` | 可选 | 默认存储桶名称 |
| `GRADIENT_KB_UUID` | 可选 | 默认知识库 UUID（避免每次都输入 `--kb-uuid`） |
| `GRADIENT_API_KEY` | 用于 RAG 功能 | 在使用 `--rag` 进行 LLM 合成时需要 |

## 外部端点

| 端点 | 功能 |
|----------|---------|
| `https://kbaas.do-ai.run/v1/{uuid}/retrieve` | 知识库检索 API |
| `https://api.digitalocean.com/v2/gen-ai/knowledgebases/` | 知识库管理 API |
| `https://{region}.digitaloceanspaces.com` | DO Spaces（与 S3 兼容） |

## 安全与隐私

- 您的 `DO_API_TOKEN` 会以承载令牌（Bearer token）的形式发送到 `api.digitalocean.com` 和 `kbaas.do-ai.run`
- Spaces 凭证用于向 `{region}.digitaloceanspaces.com` 进行与 S3 兼容的上传操作
- 您上传的文档在 DO Spaces 存储桶中默认为 **私有** 状态
- 知识库查询仅限于您的账户范围——不会跨租户共享
- 任何凭证或数据都不会发送到第三方端点

## 信任声明

> 使用此技能时，文档和查询数据会被发送到 DigitalOcean 的知识库和 Spaces API。只有在您信任 DigitalOcean 并愿意让其处理这些文档的情况下，才建议安装此技能。

## 重要说明

- 上传到 DO Spaces 的文档默认为 **私有** 状态
- 重新索引操作为 **尽力而为** —— 如果 API 调用失败，系统会按照预设计划自动重新索引
- 检索 API 返回的是文档的 **片段**，而非完整文档
- 删除知识库操作是 **永久性的** —— 索引数据将被彻底删除。但 DO Spaces 中的源文件不会受到影响
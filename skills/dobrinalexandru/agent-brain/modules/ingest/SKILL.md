# 数据摄取 📥

**状态：** 📋 代理指南（默认禁用） | **模块：** 数据摄取 | **所属部分：** 代理大脑

本指南用于指导代理如何获取外部知识。代理会获取 URL，提取关键信息，并通过 `add` 函数将这些信息存储到内存中。请注意，这里并没有专门的数据摄取代码，仅提供工作流程说明。

## ⚠️ 安全性

**默认情况下，该功能是禁用的。** 要启用该功能，协调器必须满足以下条件：
1. 仅处理用户在对话中明确提供的 URL；
2. 绝不自动获取文本、文档或内存中存在的 URL；
3. 在获取 URL 之前对其进行验证（详见下文“验证”部分）。

### URL 验证

以下 URL 将被拒绝：
- `localhost`、`127.0.0.1`、`0.0.0.0`、`::1`
- `file://`、`ftp://`、`gopher://`
- 私有 IP 地址范围（如 `10.*`、`172.16-31.*`、`192.168.*`
- 不包含点的内部主机名

仅允许以下类型的 URL：
- 公共域上的 `https://` URL；
- 用户明确允许的 `http://` URL。

## 工作流程

### 第 1 步：获取 URL 内容

使用运行时的网络请求功能来获取 URL 的内容。

```bash
# The agent runtime handles fetching — this module processes the result
# Content arrives as text extracted from the page
```

### 第 2 步：提取信息

从获取的内容中提取以下信息：
1. **标题/主题**：内容的主要内容是什么？
2. **关键观点**：3 至 7 个主要观点（非完整总结）；
3. **可操作的见解**：这些信息可以如何应用？
4. **关联性**：这些信息与现有知识有何关联？

### 第 3 步：存储信息

每个提取出的信息都会被存储为独立的内存条目。

```bash
./scripts/memory.sh add ingested "Ideas are things that generate other ideas" \
  ingested "concepts,creativity" "https://paulgraham.com/ideas.html"

./scripts/memory.sh add ingested "Execution is more concrete than ideas" \
  ingested "concepts,execution" "https://paulgraham.com/ideas.html"
```

### 第 4 步：建立关联

存储信息后，检查这些信息是否与现有知识存在关联。

```bash
./scripts/memory.sh get "ideas creativity"
# If existing entries found → note the connection in response
```

## 内容类型处理

| 内容类型 | 处理策略 |
|-------------|----------|
| **文章/博客** | 提取文章主旨和支持性观点 |
| **研究论文** | 提取摘要、主要发现和局限性 |
| **新闻文章** | 提取事实内容，忽略评论部分 |
| **文档** | 提取操作步骤和关键概念 |
| **讨论帖** | 提取共识点和主要分歧意见 |

### 不支持的内容类型
- YouTube（需要转录服务）；
- PDF 文件（需要使用运行时的 PDF 解析工具）；
- 需支付访问权限的内容（会优雅地提示失败）。

## 命令

```
"Ingest: <url>"                → Full pipeline: fetch → extract → store
"Learn from: <url>"            → Same as Ingest
"What did you learn from X?"   → Search ingested entries by source_url
"Summarize what you've read"   → List all ingested entries
```

## 提取提示

在处理获取到的内容时，请使用以下提取框架：

```
Given this content from [URL]:

1. What are the 3-7 key claims or insights?
2. What is actionable or applicable?
3. What is surprising or contrarian?
4. How does this connect to: [list existing memory topics]

For each key point, output:
- One-sentence claim
- Tags (2-4 keywords)
```

## 可能出现的问题及应对措施

| 问题 | 对策 |
|---------|----------|
| 无法访问 URL | “无法获取该 URL。它是公开可访问的吗？” |
| 内容太短 | 仅存储现有内容，并注明内容较少 |
| 内容太长 | 从第一部分提取信息，并提供进一步提取的选项 |
| 遇到访问限制 | “该内容似乎需要支付访问权限” |
| 非文本内容 | “目前仅能处理文本内容” |

## 集成方式
- 所有摄取的内容都会通过 `add` 函数以 `ingested` 类型存储；
- 代理在存储信息前应使用 `conflicts` 函数检查是否存在冲突；
- 摄取到的内容的置信度初始值为 `likely`（而非 `sure`）。
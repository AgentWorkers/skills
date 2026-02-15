---
name: telnyx-embeddings
description: 使用 Telnyx AI 进行语义搜索和文本嵌入。您可以使用自然语言搜索任何 Telnyx 存储桶中的内容，无需使用 OpenAI 或 Google API 密钥。
metadata: {"openclaw":{"emoji":"🔮","requires":{"bins":["python3"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx 嵌入技术

Telnix 提供了原生的 AI API，支持语义搜索和文本嵌入功能。您可以使用自然语言查询来搜索任何 Telnix 存储桶中的内容——查询嵌入过程在服务器端完成，因此您只需要一个 `TELNYX_API_KEY` 即可。无需使用 OpenAI 或 Google 的 API 密钥。

## 系统要求

- **Python 3.8+** — 仅需要标准库，无需外部依赖
- **TELNYX_API_KEY** — 可在 [portal.telnyx.com](https://portal.telnyx.com/#/app/api-keys) 获取

## 快速入门

```bash
export TELNYX_API_KEY="KEY..."
python3 {baseDir}/tools/embeddings/search.py "your query" --bucket your-bucket
```

无需安装任何软件包，也无需配置向导，更不需要外部服务提供商的密钥。

## 搜索功能

您可以搜索任何启用了嵌入功能的 Telnix 存储桶。查询会在服务器端被转换成嵌入格式，并与索引中的内容进行匹配。

### 基本用法

```bash
# Search with default bucket (from config.json)
./search.py "what are the project requirements?"

# Search a specific bucket
./search.py "meeting notes" --bucket my-bucket

# Get more results
./search.py "API rate limits" --num 10

# JSON output (for scripting)
./search.py "deployment steps" --json

# Custom timeout
./search.py "long query" --timeout 45

# Full content (no truncation)
./search.py "details" --full
```

### 输出格式

搜索结果会根据置信度进行排序，并附带置信度指示：

```
--- Result 1 [HIGH] (certainty: 0.923) ---
Source: docs/requirements.md

The project requires Python 3.8+ and a valid Telnyx API key...

--- Result 2 [MED] (certainty: 0.871) ---
Source: notes/planning.md

We discussed the requirements in the planning meeting...
```

置信度等级：`[HIGH]` >= 0.90, `[MED]` >= 0.85, `[LOW]` < 0.85

### 从 Python 中进行搜索

```python
from search import search, similarity_search

# Quick search (returns formatted text)
print(search("your query", bucket_name="my-bucket"))

# Get structured results
results = similarity_search("your query", num_docs=5, bucket_name="my-bucket")
for doc in results.get("data", []):
    print(doc["source"], doc["certainty"])
    print(doc["content"][:200])
```

## 索引内容

将文件上传到 Telnix 存储桶后，这些文件就会自动被索引并支持搜索。

### 上传文件

```bash
# Upload a single file
./index.py upload path/to/file.md

# Upload to a specific bucket
./index.py upload path/to/file.md --bucket my-bucket

# Upload with a custom key (filename in bucket)
./index.py upload path/to/file.md --key docs/custom-name.md

# Upload all markdown files from a directory
./index.py upload path/to/dir/ --pattern "*.md"

# Upload all files from a directory
./index.py upload path/to/dir/
```

### 触发嵌入过程

上传文件后，需要执行嵌入操作以使文件可被搜索：

```bash
# Embed files in default bucket
./index.py embed

# Embed files in a specific bucket
./index.py embed --bucket my-bucket
```

### 检查嵌入状态

```bash
./index.py status <task_id>
```

### 列出文件和存储桶

```bash
# List files in default bucket
./index.py list

# List files in a specific bucket
./index.py list --bucket my-bucket

# List files with a prefix filter
./index.py list --prefix docs/

# Show embedding status for a bucket
./index.py list --embeddings

# List all embedded buckets
./index.py buckets
```

### 创建存储桶

```bash
./index.py create-bucket my-new-bucket

# With a specific region
./index.py create-bucket my-new-bucket --region us-central-1
```

### 删除文件

```bash
./index.py delete filename.md
./index.py delete filename.md --bucket my-bucket
```

## 直接生成嵌入向量

可以为原始文本生成嵌入向量，适用于自定义相似性比较、聚类或构建自定义搜索索引。

### 可用的模型

| 模型 | 描述 |
|-------|-------------|
| `thenlper/gte-large` | 通用文本嵌入（默认模型） |
| `intfloat/multilingual-e5-large` | 多语言文本嵌入 |

```bash
# List available models
./embed.py --list-models

# Embed text (uses thenlper/gte-large by default)
./embed.py "text to embed"

# Use a specific model
./embed.py "text to embed" --model intfloat/multilingual-e5-large

# Read from file
./embed.py --file input.txt

# Pipe from stdin
echo "text to embed" | ./embed.py --stdin

# JSON output
./embed.py "text" --json
```

### 兼容 OpenAI 的客户端

Telnix 的嵌入 API 与 OpenAI 兼容，您可以将 `base_url` 设置为 Telnix 的地址，然后使用 OpenAI 的 Python SDK：

```python
from openai import OpenAI

client = OpenAI(
    api_key="KEY...",
    base_url="https://api.telnyx.com/v2/ai/openai"
)

response = client.embeddings.create(
    model="thenlper/gte-large",
    input="Hello, world!"
)
print("Dimensions:", len(response.data[0].embedding))
```

## 工作流程

使内容可被搜索的典型工作流程如下：

```
1. Upload files          2. Trigger embedding       3. Search
   ./index.py upload        ./index.py embed           ./search.py "query"
        |                        |                          |
        v                        v                          v
   Telnyx Storage  --->  Telnyx AI Embeddings  --->  Similarity Search
   (S3-compatible)       (server-side vectors)       (server-side matching)
```

### 逐步示例

```bash
# 1. Create a bucket for your content
./index.py create-bucket my-knowledge

# 2. Upload files
./index.py upload ~/docs/ --pattern "*.md" --bucket my-knowledge

# 3. Trigger embedding (converts files to searchable vectors)
./index.py embed --bucket my-knowledge

# 4. Wait 1-2 minutes for embedding to process

# 5. Search!
./search.py "how do I deploy?" --bucket my-knowledge
```

## 配置

编辑 `config.json` 文件以设置默认值：

```json
{
  "bucket": "openclaw-main",
  "region": "us-central-1",
  "default_num_docs": 5
}
```

| 参数 | 默认值 | 说明 |
|-------|---------|-------------|
| `bucket` | `openclaw-main` | 用于搜索和索引操作的默认存储桶 |
| `region` | `us-central-1` | Telnix 存储区域 |
| `default_num_docs` | `5` | 默认的搜索结果数量 |

所有设置都可以通过 CLI 参数（`--bucket`, `--num`）进行修改。

## 集成

### 与其他工具/机器人的集成

```bash
# Search and capture results
results=$(python3 {baseDir}/tools/embeddings/search.py "your query" --json)

# Upload and index a file
python3 {baseDir}/tools/embeddings/index.py upload /path/to/file.md --bucket my-bucket
python3 {baseDir}/tools/embeddings/index.py embed --bucket my-bucket
```

### 从 Python 中进行集成

```python
import subprocess, json

# Search
result = subprocess.run(
    ["python3", "{baseDir}/tools/embeddings/search.py", "your query", "--json"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
```

### 替代 OpenAI/Google 的记忆搜索功能

如果您的机器人当前使用 OpenAI 或 Google 的嵌入服务，可以切换到 Telnix 的服务：

```bash
# Before (requires OPENAI_API_KEY):
# memory_search("query")

# After (only needs TELNYX_API_KEY):
python3 {baseDir}/tools/embeddings/search.py "query" --bucket your-memory-bucket --json
```

## 与 RAG 工具的关系

该工具与 `tools/rag/` 是互补的关系，而非替代关系：

| 功能 | Telnix 嵌入技术 | RAG （tools/rag/） |
|---------|----------------------|-------------------|
| **用途** | 提供简单的直接搜索功能 | 提供完整的 RAG（检索 + 重新排序 + 生成答案）流程 |
| **搜索方式** | 直接进行相似性搜索 | 检索 + 重新排序 + 生成答案 |
| **索引方式** | 上传文件后自动嵌入 | 自动同步数据并智能分块处理 |
| **问答支持** | 不支持（返回原始结果） | 支持（基于 LLM 的智能问答） |
| **适用场景** | 独立搜索、集成应用 | 工作区级知识库 |

- 当需要简单的直接搜索时，使用 Telnix 的嵌入技术。
- 当需要基于 AI 的智能问答功能（包含来源引用）时，使用 RAG 工具。

## 常见问题解决方法

### “未找到 Telnix API 密钥”
请确保您已正确设置 API 密钥：
```bash
export TELNYX_API_KEY="KEY..."
# or
echo 'TELNYX_API_KEY=KEY...' > .env
```

### “HTTP 401” 或 “HTTP 403”
您的 API 密钥无效或已过期，请在 [portal.telnyx.com](https://portal.telnyx.com/#/app/api-keys) 重新获取。

### 搜索时出现 “HTTP 404”
- 确保存储桶存在，且已启用嵌入功能：
  ```
  ./index.py list --bucket your-bucket
  ```
- 验证嵌入是否已生效：
  ```
  ./index.py list --embeddings --bucket your-bucket
  ```

### “未找到结果”
- 等待 1-2 分钟后再尝试搜索。
- 确认文件已成功上传。
- 检查嵌入过程是否已完成：
  ```
  ./index.py list --embeddings --bucket your-bucket
  ```

### “网络错误”
请检查您的互联网连接。该工具需要访问 `api.telnyx.com` 和 `*.telnyxcloudstorage.com`。

## 致谢

本功能基于 [OpenClaw](https://github.com/openclaw/openclaw) 开发，使用了 [Telnx Storage](https://telnyx.com/products/cloud-storage) 及其 AI API。
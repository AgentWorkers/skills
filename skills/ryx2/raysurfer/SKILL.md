---
name: raysurfer
description: "通过 Raysurfer 从之前的 AI 代理执行中缓存并重用代码。在编写代码之前先进行搜索，成功后上传结果。"
argument-hint: "[search query or \"upload\"]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Raysurfer 代码缓存技巧

您可以使用 Raysurfer 这个代码缓存系统，它能够存储和检索之前 AI 代理执行过的代码。在编写新代码之前，请务必先检查缓存，之后再将成功的结果上传。

## 环境配置

- **API 基本 URL**：`https://api.raysurfer.com`
- **认证方式**：通过 `RAYSURFER_API_KEY` 环境变量传递 bearer token
- 所有 API 调用均使用 `Content-Type: application/json` 格式

## 工作流程

对于每个编码任务，请按照以下步骤操作：

### 第 1 步：搜索缓存

在编写任何代码之前，先搜索现有的缓存结果。

如果您希望包含来自 GitHub 的公共代码片段，可以在请求头中添加 `X-Raysurfer-Public-Snips: true`。

```bash
curl -s -X POST https://api.raysurfer.com/api/retrieve/search \
  -H "Authorization: Bearer $RAYSURFER_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Raysurfer-Public-Snips: true" \
  -d '{"task": "<describe the task here>", "top_k": 5, "min_verdict_score": 0.3}'
```

响应内容如下：
```json
{
  "matches": [
    {
      "code_block": {
        "id": "uuid",
        "name": "descriptive name",
        "description": "what this code does",
        "source": "the actual code content",
        "language": "python"
      },
      "combined_score": 0.85,
      "filename": "suggested_filename.py",
      "thumbs_up": 12,
      "thumbs_down": 1
    }
  ],
  "total_found": 3,
  "cache_hit": true
}
```

**决策逻辑**：
- 如果 `total_found > 0`，且最匹配的代码的 `combined_score` 大于或等于 0.7，并且投票结果（`thumbs_up > thumbs_down`）为正，则使用缓存的代码。
- 如果存在匹配结果但分数较低，可以将这些代码作为起点进行修改后再使用。
- 如果没有匹配结果，则从头开始生成代码。

### 第 2a 步：使用缓存代码（缓存命中）

当找到合适的缓存结果时：
1. 从最佳匹配的代码块中提取 `source` 字段。
2. 将其写入相应的文件中。
3. 根据当前项目的需求调整文件路径、变量名或配置。
4. 运行代码以验证其是否正常工作。
5. 继续执行第 3 步（投票）。

### 第 2b 步：生成代码（缓存未命中）

当没有合适的缓存结果时：
1. 按照常规方式编写代码。
2. 运行代码以验证其是否正常工作。
3. 继续执行第 4 步（上传）。

### 第 3 步：对缓存代码进行投票

使用缓存代码后，需要报告代码的执行结果：
```bash
curl -s -X POST https://api.raysurfer.com/api/store/cache-usage \
  -H "Authorization: Bearer $RAYSURFER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code_block_id": "<id from the match>", "code_block_name": "<name from the match>", "code_block_description": "<description from the match>", "succeeded": true, "task": "<the task description>"}'
```

如果代码运行成功，将 `succeeded` 设置为 `true`；如果代码失败或需要重大修改，则将 `succeeded` 设置为 `false`。

### 第 4 步：上传新代码

在成功生成并运行新代码后（即缓存未命中时），将其上传以供将来重复使用：
```bash
curl -s -X POST https://api.raysurfer.com/api/store/execution-result \
  -H "Authorization: Bearer $RAYSURFER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "<describe what this code does>",
    "file_written": {"path": "relative/path/to/file.py", "content": "<full file content>"},
    "succeeded": true
  }'
```

请仅上传成功执行的代码。系统默认会启用用户投票功能。

## 参数处理

- 如果通过搜索查询调用 Raysurfer（例如：`/raysurfer parse CSV and generate chart`），则将查询内容作为任务参数传递给第 1 步。
- 如果通过 `upload` 命令调用 Raysurfer（例如：`/raysurfer upload`），则上传最近生成的代码。
- 如果没有传递参数，系统会显示工作流程的摘要并询问用户的具体操作需求。

当 `$ARGUMENTS` 被提供时，可以使用 `$ARGUMENTS` 变量来接收这些参数。

## 可执行脚本

可执行的脚本位于该技能的目录中。使用 Raysurfer 时需要设置 `RAYSURFER_API_KEY`。

### 搜索功能
```
python search.py "Parse a CSV and plot a chart"
bun search.ts "Parse a CSV and plot a chart"
bash search.sh "Parse a CSV and plot a chart"
```

### 上传功能
```
python upload.py "Generate a bar chart" chart.py
bun upload.ts "Generate a bar chart" chart.py
bash upload.sh "Generate a bar chart" chart.py
```

## 注意事项

- 在进行 API 调用之前，请务必确保 `RAYSURFER_API_KEY` 已设置。如果未设置该变量，请通知用户并跳过缓存操作。
- 为每个任务编写描述性的字符串，说明代码的功能而非实现方式（例如：“解析 CSV 文件并使用 matplotlib 生成条形图”，而不是 “执行 pandas 的 read_csv 和 plt.bar 函数”）。
- 不要在任何命令或文件中硬编码 API 密钥。
- 如果 API 无法访问，应继续执行代码生成流程，以免阻塞用户。
- 尽可能使上传的代码具有独立性，以便最大化其复用性。

## 快速参考

| 操作        | API 端点            | 方法                |
|-------------|------------------|-------------------|
| 搜索缓存        | `/api/retrieve/search`      | POST                |
| 上传代码        | `/api/store/execution-result`    | POST                |
| 对代码进行投票      | `/api/store/cache-usage`      | POST                |

有关完整的请求和响应格式，请参阅 `references/api-reference.md`。
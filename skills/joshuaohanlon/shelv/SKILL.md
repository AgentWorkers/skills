---
name: shelv
description: 将 PDF 文件转换为结构化的 Markdown 文件系统，并将其导入到您的工作空间中，以便使用标准的 Unix 工具进行浏览和探索。
version: 1.0.3
metadata:
  openclaw:
    requires:
      env: [SHELV_API_KEY]
      bins: [curl, tar, jq, shasum]
    primaryEnv: SHELV_API_KEY
    emoji: "📚"
    homepage: https://shelv.dev
    os: [macos, linux]
---
# Shelv

Shelv 将 PDF 文档（合同、书籍、研究论文、法规等）转换为结构化的 Markdown 文件系统。只需上传 PDF 文件，等待处理完成后，这些文件就会作为实际的文件出现在您的工作空间中，您可以使用 `ls`、`cat`、`grep` 和 `find` 等工具来查看和操作这些文件。

**API 基本地址：** `https://api.shelv.dev`  
**认证：** 每个请求都需要使用 `Authorization: Bearer $SHELV_API_KEY` 进行认证。  
您可以在 [shelv.dev](https://shelv.dev) 的 “设置” → “API 密钥” 中获取 API 密钥。

## 核心工作流程

### 1. 上传文档

上传 PDF 文件以创建一个新的文档存储空间（shelf）。处理过程是异步进行的。

```bash
SHELF_ID=$({baseDir}/scripts/shelv-upload.sh /path/to/document.pdf --name "My Document")
```

**可选参数：**

```bash
# Use a structuring template
SHELF_ID=$({baseDir}/scripts/shelv-upload.sh document.pdf --name "Q4 Contract" --template legal-contract)

# Enable review mode (pause before finalizing)
SHELF_ID=$({baseDir}/scripts/shelv-upload.sh document.pdf --review)

# Upload and wait for processing to complete
SHELF_ID=$({baseDir}/scripts/shelv-upload.sh document.pdf --wait)
```

脚本会将文档存储空间的公共 ID（例如 `shf_0123456789abcdef01234567`）输出到标准输出（stdout）。

**可用模板：** `book`、`legal-contract`、`academic-paper`。如果省略这些参数，Shelv 会自动检测文档的结构。

**无需脚本的替代方法：**

```bash
curl -X POST "https://api.shelv.dev/v1/shelves" \
  -H "Authorization: Bearer $SHELV_API_KEY" \
  -F "file=@document.pdf" \
  -F "name=My Document"
```

**响应状态（201 状态）：**

```json
{
  "publicId": "shf_0123456789abcdef01234567",
  "name": "My Document",
  "status": "uploading",
  "template": null,
  "reviewMode": false,
  "pageCount": null,
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z"
}
```

### 2. 监控处理进度

等待文档存储空间的处理完成：

```bash
{baseDir}/scripts/shelv-poll-status.sh shf_0123456789abcdef01234567
```

脚本会每 5 秒发送一次 `GET /v1/shelves/{id}` 的请求来检查处理进度。当文档存储空间状态变为 `ready` 或 `review` 时，脚本会退出；如果处理失败（返回 `failed` 状态）或超时（10 分钟后），脚本会退出，并显示错误信息。

**处理流程：** `上传 → 解析 → 结构化 → 验证 → 准备就绪`

如果启用了 `review` 模式，脚本会在文档存储空间状态变为 `review` 时暂停处理，而不会直接进入 `ready` 状态。

**无需脚本的替代方法：**

```bash
curl -s "https://api.shelv.dev/v1/shelves/$SHELF_ID" \
  -H "Authorization: Bearer $SHELV_API_KEY" | jq '.status'
```

### 3. 将文档存储空间内容导入工作空间

将文档存储空间的 Markdown 文件系统下载并解压到您的工作空间中：

```bash
{baseDir}/scripts/shelv-hydrate.sh shf_0123456789abcdef01234567
```

脚本会下载压缩文件，验证其校验和，然后将其解压到 `~/.openclaw/workspace/shelves/<name>/` 目录下。解压完成后，脚本会输出文件列表。

**修改目录名称：**

```bash
{baseDir}/scripts/shelv-hydrate.sh shf_0123456789abcdef01234567 --name my-contract
```

**替换现有的文档存储空间：**

```bash
{baseDir}/scripts/shelv-hydrate.sh shf_0123456789abcdef01234567 --force
```

**文件浏览：**

```bash
ls ~/.openclaw/workspace/shelves/my-contract/
cat ~/.openclaw/workspace/shelves/my-contract/README.md
find ~/.openclaw/workspace/shelves/my-contract/ -name "*.md"
grep -r "force majeure" ~/.openclaw/workspace/shelves/my-contract/
```

### 4. 列出并浏览所有文档存储空间**

列出所有的文档存储空间：

```bash
curl -s "https://api.shelv.dev/v1/shelves?page=1&limit=20" \
  -H "Authorization: Bearer $SHELV_API_KEY" | jq '.data[] | {publicId, name, status}'
```

获取文档存储空间的文件结构（以扁平化的 JSON 格式显示路径和文件内容）：

```bash
curl -s "https://api.shelv.dev/v1/shelves/$SHELF_ID/tree" \
  -H "Authorization: Bearer $SHELV_API_KEY" | jq '.files | keys[]'
```

**响应格式：**

```json
{
  "shelfPublicId": "shf_0123456789abcdef01234567",
  "name": "My Contract",
  "fileCount": 8,
  "files": {
    "README.md": "# My Contract\n...",
    "clauses/force-majeure.md": "# Force Majeure\n..."
  }
}
```

### 5. 无需解压直接读取文件

通过文件路径直接读取单个文件（适用于无需下载整个文件库的特定查询场景）：

```bash
curl -s "https://api.shelv.dev/v1/shelves/$SHELF_ID/files/README.md" \
  -H "Authorization: Bearer $SHELV_API_KEY"
```

**返回内容格式：** `text/markdown`

## 工作空间约定

解压后的文档存储空间文件会保存在以下路径：

```
~/.openclaw/workspace/shelves/{name}/
```

`{name}` 是根据文档存储空间的显示名称生成的（全部转换为小写，空格和特殊字符会被替换为连字符）。在导入时可以通过 `--name` 参数自定义目录名称。

如果目标路径下已经存在同名目录，除非使用了 `--force` 参数，否则脚本会拒绝覆盖该目录。

解压完成后，可以使用标准的 Unix 工具来查看文件内容：

```bash
# List all files
find ~/.openclaw/workspace/shelves/{name}/ -type f

# Read a specific file
cat ~/.openclaw/workspace/shelves/{name}/README.md

# Search across all files
grep -r "keyword" ~/.openclaw/workspace/shelves/{name}/

# Count files
find ~/.openclaw/workspace/shelves/{name}/ -type f | wc -l
```

## 异步操作

文档存储空间的处理是异步进行的。上传完成后，处理过程会按以下顺序进行：

```
uploading → parsing → structuring → verifying → ready
```

**使用监控脚本等待处理完成：**

```bash
{baseDir}/scripts/shelv-poll-status.sh $SHELF_ID
```

如果文档存储空间的处理失败，脚本会显示错误信息并提示您可以重试：

```bash
curl -X POST "https://api.shelv.dev/v1/shelves/$SHELF_ID/retry" \
  -H "Authorization: Bearer $SHELV_API_KEY"
```

对于处于 `review` 模式的文档存储空间，您需要批准才能完成处理：

```bash
curl -X POST "https://api.shelv.dev/v1/shelves/$SHELF_ID/approve" \
  -H "Authorization: Bearer $SHELV_API_KEY"
```

或者您可以重新生成文件结构：

```bash
curl -X POST "https://api.shelv.dev/v1/shelves/$SHELF_ID/regenerate" \
  -H "Authorization: Bearer $SHELV_API_KEY"
```

## 端点可用性说明

并非所有 API 端点在所有状态下都可用。以下端点仅在文档存储空间处于 `ready` 或 `review` 状态时可用：

| 端点                        | 处理状态    | `review` 状态 | `ready` 状态 | `failed` 状态 |
| --------------------------- | ---------- | -------- | ------- | -------- |
| `GET /v1/shelves/{id}`           | 可用       | 可用       | 可用       | 可用       |
| `GET .../tree`                | 不可用     | 可用       | 可用       | 不可用     |
| `GET .../files/*`              | 不可用     | 可用       | 可用       | 不可用     |
| `GET .../archive-url`           | 不可用     | 可用       | 可用       | 不可用     |
| `POST .../approve`              | 不可用     | 可用       | 不可用     | 不可用     |
| `POST .../regenerate`            | 不可用     | 可用       | 不可用     | 不可用     |
| `POST .../retry`                | 不可用     | 不可用     | 不可用     | 可用       |

如果您尝试在文档存储空间未处于允许的状态下调用某些端点，系统会返回 `409 Conflict` 错误。

## 速率限制

- **读取操作（GET 请求）**：每分钟 120 次请求  
- **写入操作（POST/DELETE 请求）**：每分钟 20 次请求  
- **创建新的文档存储空间**：每小时 10 次请求  

如果达到请求速率限制，系统会返回 `429 Too Many Requests` 错误，您需要等待一段时间后再尝试。

## 参考资料

有关详细的 API 文档、错误代码和生命周期信息，请参阅以下文件：  
- `{baseDir}/references/api-reference.md` — 完整的 API 文档和响应格式  
- `{baseDir}/references/shelf-lifecycle.md` — 文档存储空间的状态流程、审核模式和模板行为  
- `{baseDir}/references/error-handling.md` — 错误代码和重试策略
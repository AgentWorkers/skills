---
name: batchjob-async-job
description: "使用 BatchJob 的 HTTP API 进行严格的上传验证、预检查、提交、轮询以及取消操作。系统能够全自动地解析文件来源信息（包括 file_id、本地路径、公共 URL 或渠道附件路径），仅在文件来源无法被读取时才会采用备用方案进行交互。"
metadata: { "openclaw": { "emoji": "🧪", "requires": { "bins": ["curl"], "env": ["BATCHJOB_BASE_URL", "BATCHJOB_BEARER_TOKEN"] } } }
---
# 批量作业（BatchJob）异步任务技能

当用户希望通过 BatchJob 服务运行或管理批量作业时，请使用此技能。

## 所需环境

- `BATCHJOB_BASE_URL`
- `BATCHJOB_BEARER_TOKEN`

所有 HTTP 请求都必须包含以下内容：

```bash
-H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}"
-H "Content-Type: application/json"
```

## API 端点

- `POST /v1/batch/files:upload`  
- `POST /v1/batch/jobs:precheck`  
- `POST /v1/batch/jobs`  
- `GET /v1/batch/jobs/{job_id}`  
- `GET /v1/batch/jobs?page=1&page_size=10&status=...`  
- `POST /v1/batch/jobs/{job_id}:cancel`  

## 自动化策略（默认设置）

- 始终以全自动模式运行。  
- 不需要先询问用户 `file_id`。  
- 从当前消息/上下文中确定文件来源，并在需要时自动上传文件。  
- 仅在无法获取可读文件来源时才询问用户进一步信息。  
- 支持的上传文件格式：`jsonl`、`csv`、`xlsx`、`xls`（BatchJob 会将其转换为内部使用的 JSONL 格式）。  
- 对于 `jsonl` 格式，每行数据必须符合以下格式之一：  
  - 标准的 Vertex 格式（`contents` + 可选的 `generationConfig`）  
  - 简单的提示格式（`prompt` + 可选的 `aspect_ratio` / `image_urls`，其中 `image_urls` 必须是可公开访问的 URL）  
- 如果用户仅提供了 `model mode`，则视为确认并自动继续执行。  

## 必须遵守的规则

- 除非用户明确要求，否则不要自动创建第二个作业来进行重试。  
- 除非用户明确要求，否则在终端失败后不要自动更改数据集格式。  
- 在上传前，仅允许对已知的安全映射类型（例如简单的提示格式 JSONL -> Vertex JSONL）进行一次自动转换。  
- 如果上传失败，本次作业将终止；不要继续进行预检查或提交。  
- 当 `row_count` 小于或等于 0 时，切勿提交作业。  
- 不要自动获取或解析 `output_summary_url`；仅在用户请求详细失败原因时才进行解析。  
- 一旦作业达到终止状态（`completed`、`failed`、`partially_failed`），立即停止执行并返回摘要信息。  

## JSONL 兼容性规则（重要）

BatchJob 的内部执行要求每行 JSONL 数据都符合 `VertexGeminiImageRequest` 的格式：  
- 标准的行格式：  
  - `contents[0].parts[0].text` 包含提示文本  
  - `generationConfig.imageConfig.aspectRatio` 是可选的  
  - `generationConfig.responseModalities` 必须包含 `IMAGE` 和 `TEXT`  
- 非标准的简单 JSONL 格式（例如 `{"prompt":"...","aspect_ratio":"1:1"}` 也是可接受的；服务器会将其转换为 Vertex 格式。  
- 如果 JSONL 数据中既没有 `contents` 也没有 `prompt`，则停止操作并要求用户提供有效的数据。  
- 明确不支持的格式（提交前必须拒绝）：包含 `method`、`url` 和 `body` 的 OpenAI 批量作业格式（例如 `/v1/chat/completions` 的数据格式）。  
- 这种格式会导致 Vertex 错误：至少需要 `contents` 字段。  

## 数据集输出规则（重要）

当用户要求为 BatchJob 图像任务生成模板/示例文件时：  
- 优先使用 CSV 格式，包含 `prompt`、`aspect_ratio`、`image_urls` 标头；  
- 或者使用 JSONL 格式，包含 `prompt`、`aspect_ratio`、`image_urls`；  
- 如果提供了 `image_urls`，则必须确保这些 URL 是可公开访问的（http/https）。  
- 不要将 OpenAI 批量作业的封装格式（`custom_id` + `method` + `url` + `body`）作为最终上传文件。  

## 用户模板响应（重要）

当用户请求格式/模板时，返回以下内容：  
1. 简短的解释（必须包含 `prompt`，`aspect_ratio`/`image_urls` 是可选的，且 `image_urls` 必须是可公开访问的 URL）；  
2. 一个可复制的 CSV 样本；  
3. （可选）一个 JSONL 样本（简单的提示格式）；  
4. 本地模板文件路径（如果可用）：  
   - `/home/node/.openclaw/workspace/templates/batchjob-input-template.csv`  
   - `/home/node/.openclaw/workspace/templates/batchjob-input-template.jsonl`  
   - `/home/node/.openclaw/workspace/templates/batchjob-format-guide.md`  

在模板响应中不要包含 OpenAI 批量作业的封装格式示例。  

## 文件来源解析规则（严格顺序）  

1. 如果提供了 `file_id`，则跳过上传步骤。  
2. 如果提供了公共的 `file_url`（`http://` 或 `https://`），则下载到本地临时文件后上传。  
3. 如果提供了明确的本地 `file_path`，且文件可读，则上传该文件。  
4. 如果通道/运行时上下文提供了附件的本地路径（例如 `/tmp/...`、`MEDIA:<path>`、`/tmp/openclaw-media/...`），且文件可读，则上传该文件。  
5. 如果通道提供了私有的文件令牌/对象（没有本地路径且无法通过公共 URL 访问），则使用通道的下载功能来上传文件；如果无法下载，则采用备用方案。  

解析后的文件来源必须转换为以下格式之一：  
- `file_id`  
- `file_path`（可读的本地文件路径）  

## 执行流程  

1. 确认 `model` 和 `mode`；如果缺失，则使用默认值（`model=google/gemini-2.5-flash-image`，`mode=fast`），并告知用户。  
2. 使用上述规则解析文件来源。  
3. 如果解析结果得到了 `file_path`，则通过 `POST /v1/batch/files:upload` 上传文件以获取 `file_id`：  
   - 对于 `.jsonl` 格式的文件，先检查几行非空内容：  
     - 如果存在 `contents`，则按原格式上传；  
     - 如果仅存在 `prompt`/`aspect_ratio`/`image_urls`，则按原格式上传（服务器会进行转换）；  
     - 如果存在 `method` + `url` + `body`，则要求用户切换到 BatchJob 的数据格式；  
     - 如果文件格式未知，要求用户提供有效的数据格式。  
   - 向后兼容性处理：  
     - 如果上传失败且文件类型为 `csv/xlsx/xls`，尝试将其转换为 JSONL 后重新上传；最多重试一次。  
     - 如果上传失败且出现验证错误（如 `unsupported schema`、`no valid data rows`），立即停止并返回修复指南。  
5. 使用 `record_count`（优先使用上传文件的 `row_count`）执行预检查。  
6. 使用 `file_id` 提交作业。  
7. 定时检查作业状态（`completed`、`failed`、`partially_failed`），最多检查 12 次（约 60 秒）；  
   - 如果仍未达到终止状态，则返回当前状态和 `job_id`，然后停止。  
8. 返回包含 `job_id`、状态、进度以及 `output_summary_url` 的简洁摘要信息。  

如果用户仅请求估算结果，则在预检查阶段停止操作，不进行提交。  

## 备用方案（仅在必要时使用）

当解析器无法从当前通道/上下文中读取文件内容时，使用以下提示：  
“我收到了文件引用，但当前运行环境无法直接读取该附件内容。请选择以下方式之一：”  
1) 提供一个可公开下载的 URL；  
2) 提供本机上的可读文件路径（例如 `/tmp/xxx.csv`）；  
3) 先将文件上传到 BatchJob，然后提供 `file_id`。  

如果当前通道支持在上下文中直接发送附件路径，请同时要求用户重新发送文件。  

## 文件来源处理方案  

### A) 公共 URL -> 本地临时文件  
```bash
FILE_URL="https://example.com/input.jsonl"
EXT="${FILE_URL##*.}"
FILE_PATH="$(mktemp "/tmp/batchjob-input.XXXXXX.${EXT:-jsonl}")"
curl -fL --retry 3 --connect-timeout 10 "$FILE_URL" -o "$FILE_PATH"
```  

### A2) JSONL 格式验证  

在上传前使用此步骤以避免提交错误的文件格式。  
```bash
SRC_JSONL="/tmp/input.jsonl"
FIRST_LINE="$(grep -m1 -v '^[[:space:]]*$' "$SRC_JSONL")"
echo "$FIRST_LINE" | jq -e '
  (has("contents")) or
  (has("prompt")) and ( (has("method")|not) and (has("url")|not) and (has("body")|not) )
' >/dev/null || {
  echo "JSONL schema invalid for BatchJob: requires contents or prompt-only schema"
  exit 1
}
```  

### B) Feishu/通道附件路径  

如果消息上下文中已经包含了附件的本地路径，直接使用该路径作为文件来源。  
```bash
FILE_PATH="/tmp/openclaw-media/your-uploaded-file.jsonl"
```  

如果仅提供了通道令牌/链接，但没有可下载的 URL 且没有本地路径，首先尝试使用通道的下载功能；如果下载失败，则采用备用方案。  

## 其他相关代码模板  
```bash
FILE_PATH="/path/to/input.jsonl"
FILE_NAME="$(basename "${FILE_PATH}")"
test -f "${FILE_PATH}" || { echo "文件 ${FILE_PATH} 不存在"; exit 1; }
FILE_CONTENT_B64="$(base64 < "${FILE_PATH}" | tr -d '\n')"

curl -sS "${BATCHJOB_BASE_URL}/v1/batch/files:upload" \
  -H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"filename\":\"${FILE_NAME}\",\"mode\":\"fast\",\"content\":\"${FILE_CONTENT_B64}\"}"
```  
```bash
curl -sS "${BATCHJOB_BASE_URL}/v1/batch/jobs:precheck" \
  -H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"record_count": 100, "model": "google/gemini-2.5-flash-image", "mode": "fast"}'
```  
```bash
curl -sS "${BATCHJOB_BASE_URL}/v1/batch/jobs" \
  -H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "your-file-id", "model": "google/gemini-2.5-flash-image", "mode": "fast"}'
```  
```bash
curl -sS "${BATCHJOB_BASE_URL}/v1/batch/jobs/${JOB_ID}" \
  -H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}"
```  
```bash
curl -sS "${BATCHJOB_BASE_URL}/v1/batch/jobs/${JOB_ID}:cancel" \
  -H "Authorization: Bearer ${BATCHJOB_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"reason":"user requested cancellation"}'
```
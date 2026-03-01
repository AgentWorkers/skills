---
name: whentomeet
description: 通过经过身份验证的 tRPC v1 API，创建、列出、获取和删除 WhenToMeet 计划事件。
compatibility: Requires Python 3, internet access, and WHENTOMEET_API_KEY in environment.
metadata: {"openclaw":{"emoji":"📅","primaryEnv":"WHENTOMEET_API_KEY","requires":{"env":["WHENTOMEET_API_KEY"]}}}
---
# WhenToMeet Skill

此技能用于对计划事件进行身份验证后的管理。  
有关 whentomeet.io 的更多信息，请访问：https://whentomeet.io/llms.txt  

## 激活条件  
当用户请求以下操作时使用此技能：  
- 创建包含时间选项的事件  
- 列出他们的事件  
- 获取某个事件的详细信息  
- 删除事件  

如果请求需要使用未记录的接口或字段，请勿使用此技能。  

## 所需环境变量  
- 环境变量：`WHENTOMEET_API_KEY`  
- 基本 URL：`https://whentomeet.io/api/trpc`  
- 认证方式：`Authorization: Bearer $WHENTOMEET_API_KEY`  
- tRPC 请求体格式：`{"json": {...}`  
- 对于 GET 请求，传递 URL 编码的请求数据：`input=<encoded {"json": ...}>`  

## 可用的脚本  
- `scripts/w2m_events.py` — 提供用于 `create`、`list`、`get`、`delete` 和 `encode-input` 的非交互式命令行工具。  

## 支持的 API 端点（版本 1）  
- `v1.event.create`（POST）  
- `v1.event.list`（GET）  
- `v1.event.get`（GET）  
- `v1.event.delete`（POST）  

## 核心数据模型  
- **事件字段**：  
  - `id`（UUID）  
  - `title`（字符串）  
  - `description`（可选字符串）  
  - `status`（`PLANNING` 或 `FINALIZED`）  
  - `publicUrl`（URL）  

- **时间选项字段**：  
  - `startTime`（ISO-8601 格式）  
  - `endTime`（ISO-8601 格式）  

## 使用前的准备  
- 确保 API 密钥存在。  
- 确保每个时间选项的时间戳有效，并且 `endTime` 大于 `startTime`。  
- 对于删除操作，需要用户明确确认事件 ID。  

## 建议的工作流程（优先使用脚本）  
从技能的根目录运行相应的命令：  

- 列出事件：  
  ```bash
python3 scripts/w2m_events.py list
```  

- 创建事件：  
  ```bash
python3 scripts/w2m_events.py create \
  --title "Team Sync" \
  --description "Optional description" \
  --slots-json '[{"startTime":"2026-03-02T12:00:00.000Z","endTime":"2026-03-02T13:00:00.000Z"}]' \
  --modification-policy EVERYONE
```  

- 获取事件详细信息：  
  ```bash
python3 scripts/w2m_events.py get --event-id "uuid"
```  

- 删除事件（需要用户确认）：  
  ```bash
python3 scripts/w2m_events.py delete --event-id "uuid" --confirm
```  

- 编码 GET 请求数据：  
  ```bash
python3 scripts/w2m_events.py encode-input --json '{"eventId":"uuid"}'
```  

## HTTP 备用方案  
仅在脚本无法执行时使用：  
- 创建事件（`v1.event.create`）：  
  ```bash
curl -sS -X POST "https://whentomeet.io/api/trpc/v1.event.create" \
  -H "Authorization: Bearer $WHENTOMEET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"json": {
    "title": "My Event",
    "description": "Optional description",
    "slots": [
      {"startTime": "2026-03-02T12:00:00.000Z", "endTime": "2026-03-02T14:00:00.000Z"},
      {"startTime": "2026-03-03T12:00:00.000Z", "endTime": "2026-03-03T14:00:00.000Z"}
    ],
    "modificationPolicy": "EVERYONE"
  }}'
```  

- 列出事件（`v1.event.list`）：  
  ```bash
curl -sS -X GET "https://whentomeet.io/api/trpc/v1.event.list?input=%7B%22json%22%3A%7B%7D%7D" \
  -H "Authorization: Bearer $WHENTOMEET_API_KEY"
```  

- 获取事件详细信息（`v1.event.get`）：  
  ```bash
curl -sS -X GET "https://whentomeet.io/api/trpc/v1.event.get?input=%7B%22json%22%3A%7B%22eventId%22%3A%22uuid%22%7D%7D" \
  -H "Authorization: Bearer $WHENTOMEET_API_KEY"
```  

- 删除事件（`v1.event.delete`）：  
  ```bash
curl -sS -X POST "https://whentomeet.io/api/trpc/v1.event.delete" \
  -H "Authorization: Bearer $WHENTOMEET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"json": {"eventId": "uuid"}}'
```  

- GET 请求数据编码辅助工具：  
  ```bash
INPUT=$(python3 - <<'PY'
import json, urllib.parse
payload = {"json": {"eventId": "uuid"}}
print(urllib.parse.quote(json.dumps(payload, separators=(",", ":"))))
PY
)

curl -sS "https://whentomeet.io/api/trpc/v1.event.get?input=${INPUT}" \
  -H "Authorization: Bearer $WHENTOMEET_API_KEY"
```  

## 代理执行规范  
1. 首先使用 `scripts/w2m_events.py` 脚本。  
2. 选择最匹配的 API 端点进行调用。  
3. 传递准确的请求数据格式（不得添加自定义字段）。  
4. 仅解析 `result.data.json` 的内容。  
5. 返回简洁的结果：  
  - 创建事件：`id`、`status`、`publicUrl`  
  - 列出事件：事件数量及每个事件的简要信息  
  - 获取事件详细信息：核心字段及时间选项  
  - 删除事件：明确显示操作是否成功  
6. 在失败时记录限速相关信息。  

## 错误处理与重试规则  
- 400：请求格式或时间戳无效  
- 401/403：API 密钥无效或访问受限  
- 404：事件未找到  
- 429：达到请求速率限制；请等待 `X-RateLimit-Reset` 后再重试  

- 对于非幂等操作（如创建/删除），切勿盲目多次重试。  

## 请求速率限制  
- 免费账户：每生命数量限制为 32 次请求  
- 高级账户：每小时 1,000 次请求  
- 相关请求头信息：`X-RateLimit-Limit`、`X-RateLimit-Remaining`、`X-RateLimit-Reset`  

## 安全规则  
- 严禁记录或显示原始 API 密钥。  
- 不得伪造事件 ID、URL 或状态信息。  
- 除非响应明确确认成功，否则不得声称操作成功。  
- 如果响应格式与预期不符，需报告错误并返回实际接收到的数据。  

## 参考资料  
- `references/quickstart.md`：提供创建、列出、获取和删除事件的请求示例。  
- `references/troubleshooting.md`：包含错误诊断、重试机制及安全检查指南。
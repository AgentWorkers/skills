---
name: letsclarify
description: 通过网页表单收集结构化的人类输入（如审批意见、决策结果、评论以及数据）。创建一个基于 JSON 模式的表单，向用户发送唯一的 URL，然后等待用户的反馈。当你的工作流程需要用户在继续之前进行确认或提供意见时，可以使用这种方法。
homepage: https://letsclarify.ai
license: MIT
metadata: {"clawdbot":{"emoji":"📋","primaryEnv":"LETSCLARIFY_API_KEY"}}
---
# 了解 Skill 的具体功能

**Human-in-the-Loop (HITL) 基础设施**：当您的工作流程需要结构化的人类输入（如审批、决策或数据收集）时，可以使用该基础设施。  
**基础 URL：** `https://letsclarify.ai`  
**身份验证：** 所有 API 调用时需使用 `Authorization: Bearer lc_...`  

> 有关完整的 curl 示例、详细的响应内容、MCP 工具说明、所有轮询策略、嵌入小部件的详细信息以及高级预填充规则，请参阅 [REFERENCE.md](./REFERENCE.md)。  

## 推荐使用 MCP 服务器（MCP Server）  

兼容 MCP 的代理应使用远程 MCP 端点，而非原始的 REST 调用。  
**端点：** `https://letsclarify.ai/mcp`  
**配置：**  
```json
{
  "mcpServers": {
    "letsclarify": {
      "url": "https://letsclarify.ai/mcp",
      "headers": {
        "Authorization": "Bearer lc_..."
      }
    }
  }
}
```
**可用工具：**  
`register`（无需身份验证）、`create_form`、`add_recipients`、`get_summary`、`get_results`、`delete_form`（所有这些操作都需要身份验证）。  

## REST API 参考  

### 注册/删除 API 密钥  

- **注册 API：**  
  `POST /api/v1/register`  
  参数：`{"name": "...", "email": "..."}`  
  返回值：`{"api_key": "lc_...", "key_prefix": "lc_xxxxx"}`  
  注意：API 密钥仅生成一次，需妥善保管。  

- **删除 API：**  
  `DELETE /api/v1/register`  
  需携带身份验证头信息，返回值：`{"deleted": true}`  

### 创建表单（Create Form）  
`POST /api/v1/forms`  
**必填参数：** 身份验证  
**可选参数：** `theme_color`（十六进制颜色代码，例如 `#1a2b3c`）；`recipient_count`（接受 1 至 1,000 个接收者）  
**返回值：** `form_token`、`delete_token`、`recipients`（UUID 列表）、`base_url_template`、`poll_url`、`summary_url`、`delete_url`  

**接收者链接：**  
`https://letsclarify.ai/f/{form_token}/{recipient_uuid}`  
（可通过电子邮件、Slack、WhatsApp 等方式发送表单链接。）  

**客户端提供的 UUID 和预填充数据：**  
若需为接收者提供预填充信息，可传递以下格式的数据：  
`{"recipients": [{"uuid": "...", "prefill": {"field_id": "value"}}, {}]`  
注意：UUID 必须是有效的 v4 格式，预填充数据大小不超过 10KB。`recipient_count` 和 `recipients` 可同时使用（接收者数量至少等于接收者列表的长度）。  

### 添加接收者（Add Recipients）  
`POST /api/v1/forms/{form_token}/recipients`  
参数：`{"count": 5}` 或 `{"recipients": [...]}`  
**限制：** 每次请求最多添加 1,000 个接收者，每个表单最多添加 10,000 个接收者；预填充规则与创建表单时相同。  

### 获取表单汇总信息（Poll Summary）  
`GET /api/v1/forms/{form_token}/summary`  
返回值：`{"expired", "known_total", "submitted_total", "pending_total", "updated_at_max"`  

### 获取表单结果（Poll Results）  
`GET /api/v1/forms/{form_token}/results`  
**查询参数：**  
`limit`（分页参数）、`status`（已提交/待处理状态）、`cursor`（分页索引）、`include_files=1`（是否包含文件）、`updated_since`（时间戳，格式为 ISO 8601）  
**返回值：** `{"expired", "next_cursor", "server_time", "results": [{"recipient_uuid", "status", "submitted_at", "updated_at", "response_json", "files"]}`  

**高效轮询：**  
- 先使用 `cursor` 分页查询，直到 `next_cursor` 为 `null`；  
- 然后使用 `updated_since={server_time}` 进行后续轮询。  

### 删除表单（Delete Form）  
`DELETE /api/v1/forms/{form_token}`  
**参数：** `X-Delete-Token`（必须包含 `delete_token`）  
**返回值：`{"deleted": true}`  
表单、提交的数据及相关文件将被永久删除。  

### Webhook：**  
如果设置了 `webhook_url`（HTTPS），每次表单提交时都会发送 POST 请求，包含 `form_token`、`recipient_uuid`、`submitted_at` 和 `response_json`。  
在遇到 5xx 错误或网络问题时，系统会自动重试 3 次。  

## 等待结果（Waiting for Results）**  
创建表单并发送链接后，需设置异步轮询机制。请注意：系统不会立即返回结果。  
**推荐使用方法：** 使用 Cron 任务进行轮询。  
**示例命令：**  
`openclaw cron add --name "check-lc-{form_token}" --at +1h --delete-after-run --message "检查表单 {form_token} 的结果并报告状态。"  

**工作流程示例：**  
1. 创建表单 → 发送链接 → 使用 Cron 任务轮询汇总信息 → 收到所有回复或表单过期后 → 获取结果 → 删除 Cron 任务 → （可选）删除表单。  

### 嵌入表单（Embed Form）**  
可以直接将表单嵌入任何页面中，而无需使用外部链接：  
**实现方式：** [参见 CODE_BLOCK_2_](...)  

**表单字段类型及配置：**  
| 字段类型 | 描述 | 是否需要配置选项 |
|---|---|---|
| `text` | 单行输入 | 否 |
| `textarea` | 多行输入 | 否 |
| `checkbox` | 单个复选框 | 否 |
| `checkbox_group` | 多个复选框 | 是 |
| `radio` | 单选按钮 | 是 |
| `select` | 下拉菜单 | 是 |
| `file` | 文件上传 | 否 |

**验证规则（可选）：**  
- `text`/`textarea`：`min_length`/`max_length`（最小/最大长度）；`pattern`（正则表达式）  
- `checkbox_group`：`min_items`/`max_items`（可选字段数量）  
**文件上传配置（可选）：** `accept`（允许的文件格式）、`max_size_mb`（文件最大大小，单位：MB）、`max_files`（允许上传的文件数量）  

**速率限制：**  
- 注册 API：每小时 5 次  
- 创建表单 API：每分钟 10 次  
- 所有 API/MCP 请求：每分钟 60 次  
- 嵌入表单的 GET/POST 请求：每分钟 30 次/20 次  

**错误处理：**  
当遇到 429 状态码时，系统会读取 `Retry-After` 头信息，并采用指数级重试策略（`Retry-After × 2^attempt`），最多重试 5 次。  

**数据保留策略：**  
默认数据保留 30 天，最长 365 天。过期的表单会标记为 `expired: true`；如需立即清除数据，请使用删除 API。
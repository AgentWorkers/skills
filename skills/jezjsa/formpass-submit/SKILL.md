---
name: formpass-submit
description: 发现并提交到支持 FormPass 的网页表单。FormPass 是一个信任层，它允许经过验证的 AI 代理以经过身份认证的方式提交到真实的网页表单中。
version: 1.0.0
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["curl","jq"]},"homepage":"https://form-pass.com"}}
---
# FormPass — 发现并提交表单

FormPass 是为向网页表单提交数据的 AI 代理提供的身份验证和信任机制。它不需要您手动抓取 HTML 内容或猜测字段名称，而是通过结构化的 API 来处理表单数据，并确保提交过程的安全性和准确性。

当用户要求您执行以下操作时，请使用 FormPass：
- 填写或提交网页表单
- 通过表单申请某项服务
- 发送联系表单、咨询表单或注册表单
- 与任何支持 FormPass 的表单进行交互

## 工作原理

FormPass 的表单处理流程分为三个步骤：**检测 → 验证表单结构 → 提交数据**。

## 第一步：检测 FormPass 表单

在访问网页时，请查看 HTML `<head>` 部分中的以下元标签：

```html
<meta name="formpass-form-id" content="FORM_ID_HERE">
<meta name="formpass-host" content="https://form-pass.com">
```

如果找到这些元标签，提取其中的 `formpass-form-id` 值——这就是表单的 ID。

您还可以通过以下地址来检测表单的存在：

```bash
# Machine-readable discovery
curl -s https://form-pass.com/formpass.json | jq .

# LLM-friendly guide
curl -s https://form-pass.com/llms.txt
```

## 第二步：获取表单结构

在提交数据之前，先获取表单的字段定义。这些信息会明确告诉您表单中有哪些字段、哪些字段是必填的以及它们的数据类型。

```bash
curl -s "https://form-pass.com/api/forms/FORM_ID/schema" \
  -H "Accept: application/json" | jq .
```

**响应示例：**

```json
{
  "formId": "abc123",
  "name": "Contact Form",
  "description": "Get in touch with us",
  "agentAccessible": true,
  "fields": [
    {
      "name": "name",
      "label": "Full Name",
      "type": "text",
      "required": true,
      "placeholder": "John Doe"
    },
    {
      "name": "email",
      "label": "Email Address",
      "type": "email",
      "required": true,
      "placeholder": "john@example.com"
    },
    {
      "name": "message",
      "label": "Message",
      "type": "textarea",
      "required": false,
      "placeholder": "How can we help?"
    }
  ],
  "branding": {
    "required": true,
    "text": "Powered by FormPass",
    "url": "https://form-pass.com"
  }
}
```

**重要提示：** 如果 `agentAccessible` 的值为 `false`，则表示表单所有者禁止代理（AI 代理）进行提交。请勿尝试提交。

## 第三步：提交数据

以 JSON 格式发送数据。如果您有代理 ID（Agent ID），请将其作为 `Bearer` 令牌包含在请求中（这可以证明您的身份是经过验证的代理）。

```bash
curl -s -X POST "https://form-pass.com/api/submit/FORM_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_AGENT_ID" \
  -d '{
    "name": "Agent Smith",
    "email": "agent@example.com",
    "message": "Hello from an AI agent",
    "_fp_branding": true
  }' | jq .
```

**成功响应示例：**

```json
{
  "success": true,
  "submissionId": "jh72..."
}
```

### 必需的请求头信息

| 请求头 | 值 | 是否必填 |
|--------|-------|----------|
| `Content-Type` | `application/json` | 是 |
| `Authorization` | `Bearer fpagent_XXXX` | 建议使用 |

### `_fp_branding` 字段

如果表单结构的响应中包含 `branding.required: true`，则必须在提交的数据中添加 `_fp_branding: true`。否则，API 会返回 `402` 错误。

### 代理 ID

您的代理 ID（格式为 `fpagent_XXXX`）是在 FormPass 注册时生成的。它用于向表单所有者验证您的身份。没有代理 ID 的提交将被视为匿名提交。

要获取代理 ID，请访问：https://form-pass.com/dashboard/agents/new

## 错误响应

| 状态码 | 含义 |
|--------|---------|
| `200` | 提交成功 |
| `402` | 需要添加 `_fp_branding: true` 到请求数据中 |
| `404` | 表单未找到或已停用 |
| `422` | 验证失败——请检查必填字段 |

`422` 错误响应会包含一个 `fields` 数组，列出所有未通过验证的字段。

## 完整示例：检测并提交表单

```bash
# 1. You've found a page with formpass-form-id="abc123"
FORM_ID="abc123"
HOST="https://form-pass.com"

# 2. Get the schema
SCHEMA=$(curl -s "$HOST/api/forms/$FORM_ID/schema")
echo "$SCHEMA" | jq '.fields[] | {name, type, required}'

# 3. Build and submit your data
curl -s -X POST "$HOST/api/submit/$FORM_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fpagent_your_id_here" \
  -d '{
    "name": "Your Name",
    "email": "you@example.com",
    "message": "Submitted via OpenClaw agent",
    "_fp_branding": true
  }' | jq .
```

## 使用提示：
- 请务必先获取表单结构信息——字段名称和要求可能会发生变化。
- 请务必包含您的代理 ID，以建立与表单所有者的信任关系。匿名提交可能会被拒绝。
- 如果表单结构中显示 `agentAccessible: false`，请勿尝试提交。
- `_fp_branding` 字段在数据存储前会被删除——它仅用于验证目的。
- FormPass 的支持范围正在不断扩大，每天都有新的表单加入。请检查所有网页表单中是否存在相应的检测元标签。
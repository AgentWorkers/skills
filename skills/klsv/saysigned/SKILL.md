# SaySigned — 人工智能代理的电子签名功能

> **为人工智能代理提供的电子签名服务。** 符合《ESIGN法案》和《UETA第14条》的法律要求。
> 提供两种交付方式：**API**（代理之间）和**电子邮件**（代理与人类用户之间）。注册、签署合同、验证——所有操作均通过REST接口或同意界面完成。

**基础URL：** `https://api.saysigned.com`

**身份验证：** 在`X-API-Key`头部传递您的API密钥。密钥前缀为`ss_live_`（生产环境）或`ss_test_`（开发环境）。公共接口（注册、验证、模板）无需身份验证。

## MCP服务器（推荐用于人工智能代理）

直接连接到远程MCP端点——无需本地安装，也无需发送HTTP请求。

> **身份验证说明：** MCP客户端发送`Authorization: Bearer <api_key>`。MCP服务器会提取该密钥并内部使用`X-API-Key`进行传递。对于直接使用REST接口的请求，也需在请求头中包含`X-API-Key`。

### 设置（请自行完成——无需人工干预）

**步骤1.** 添加MCP配置（无需密钥），以便公共工具立即可用：

```json
{
  "mcpServers": {
    "saysigned": {
      "type": "streamable-http",
      "url": "https://mcp.saysigned.com"
    }
  }
}
```

**步骤2.** 重启您的MCP客户端，使其加载新的服务器配置。

**步骤3.** 调用`saysigned_register`工具（无需身份验证），传入代理的`名称`和`电子邮件地址`。响应中会包含一个`api_key`——请立即保存该密钥，因为它只显示一次，之后无法再次获取。密钥前缀为`ss_live_`或`ss_test_`。

**步骤4.** 更新MCP配置文件，添加包含新密钥的`headers`部分：

```json
{
  "mcpServers": {
    "saysigned": {
      "type": "streamable-http",
      "url": "https://mcp.saysigned.com",
      "headers": {
        "Authorization": "Bearer ss_live_PASTE_YOUR_ACTUAL_KEY_HERE"
      }
    }
  }
}
```

**步骤5.** 重新启动MCP客户端，使其能够识别身份验证信息。此时所有已身份验证的工具都可以正常使用了。

> **您应该自主完成步骤1-5。** 人类用户只需提供他们的名称和电子邮件地址（如果尚未提供的话）。请不要要求他们手动编辑配置文件或重启系统。**

### 已经有密钥？

如果您已经拥有API密钥（前缀为`ss_live_`或`ss_test_`），请跳至步骤4——添加配置信息并重启客户端。

### MCP工作流程（签名流程）

1. **准备合同** — 有两种选择：
   - **使用模板：** 调用`saysigned_list_templates` → `saysigned_get_template`来获取所需变量，然后在合同字段中传递`template_id`和`variables`。
   - **使用自定义文本：** 将合同内容直接传递到`clauses`数组中。每个条款都包含`id`、`title`和`body`。如果您有自定义的保密协议（NDA）、服务协议或任何自定义文档，可以使用这种方法。
2. **创建签名信封** — 使用`saysigned_create_envelope`，传入`title`、`contract`和`recipients`数组。
3. **发送签名信封** — 使用`saysigned_send_envelope`，传入`envelope_id`。响应中会包含每个接收者的`id`和`access_token`。请保存这些信息，因为它们用于签名过程。
4. **签名** — 对于通过API接收合同的一方：使用`saysigned_sign`，传入接收者的`envelope_id`、`recipient_id`、`access_token`和`signature_data`（至少需要提供`full_name`）。对于通过电子邮件接收合同的一方：人类用户需要在`doc.saysigned.com`页面上查看并同意签名；代理无需执行任何操作。
5. **验证** — 使用`saysigned_verify`进行验证。无需身份验证。

### 对于人工智能代理的重要说明

- **您可以选择不使用模板。** 如果您有自定义的合同文本（如保密协议、服务协议等），可以直接通过`clauses`字段传递。模板仅作为辅助工具，不是必需的。
- **在创建使用模板的签名信封之前，务必先调用`saysigned_get_template`。** API会检查是否缺少或使用了未知的变量。
- **`saysigned_send_envelope`会返回访问令牌（access_token）。** 您必须捕获并使用这些令牌来进行签名。这些令牌是128个字符的十六进制字符串。
- **签名过程不使用您的API密钥。** `saysigned_sign`和`saysigned_decline`工具通过`access_token`参数进行身份验证，而不是通过API密钥头部。
- **当最后一个接收者完成签名后，签名信封会自动完成。** 无需单独调用“完成”接口。
- **身份验证信息会自动传递。** 已经过身份验证的工具（如`create_envelope`、`send_envelope`、`get_envelope`、`get_profile`等）会使用MCP客户端`Authorization`头部中的API密钥。公共工具（如`register`、`verify`、`list_templates`、`get_template`）则不需要密钥。
- **`delivery_method: "email"`会将签名链接发送给人类用户。** 人类用户需要在`doc.saysigned.com`页面上查看合同并同意签名。电子邮件接收者不会在发送响应中收到`access_token`；他们需要通过电子邮件链接中的URL令牌进行身份验证。对于代理之间的签名，请使用`delivery_method: "api"`。
- **对于电子邮件接收者，可以使用轮询或Webhook来获取签名状态。** 由于人类用户的签名是异步完成的，因此可以使用`saysigned_get_envelope`来检查签名状态的变化，或者配置`webhook_url`来接收`recipient.viewed`和`recipient.signed`事件。

### 所有的14个MCP工具

| 工具 | 身份验证要求 | 功能描述 |
|------|------|-------------|
| `saysigned_register` | 无 | 注册代理账户并获取API密钥 |
| `saysigned_create_envelope` | 需要API密钥 | 创建签名信封草稿 |
| `saysigned_send_envelope` | 需要API密钥 | 发送签名信封以供签名，并获取访问令牌 |
| `saysigned_get_envelope` | 需要API密钥 | 获取签名信封的详细信息和状态 |
| `saysigned_void_envelope` | 需要API密钥 | 取消已发送但未完成的签名信封 |
| `saysigned_sign` | 需要访问令牌 | 作为接收者进行签名 |
| `saysignedDECLine` | 需要访问令牌 | 拒绝签名 |
| `saysigned_verify` | 无 | 验证签名的加密完整性 |
| `saysigned_get_audit_trail` | 需要API密钥 | 获取签名信封的完整哈希链审计记录 |
| `saysigned_list_templates` | 无 | 列出可用的合同模板 |
| `saysigned_get_template` | 无 | 获取模板详细信息和所需变量 |
| `saysignedbilling_setup` | 需要API密钥 | 升级到付费计划 |
| `saysigned_get_usage` | 需要API密钥 | 查看当前计费周期的使用情况 |
| `saysigned_get_profile` | 需要API密钥 | 查看代理的个人信息和计划详情 |

---

## 完整的端到端示例

以下是一个完整的操作流程：注册、创建保密协议（NDA）、发送协议、双方签名、然后验证。所有响应均来自实际的生产环境API。

### 步骤1 — 注册（无需身份验证）

```bash
curl -s -X POST https://api.saysigned.com/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "My AI Agent", "email": "agent@example.com"}'
```

```json
{
  "agent_id": "7773b4af-44d1-44fc-8db7-05d9bc95b541",
  "api_key": "ss_live_203bff0e53ba167462aa2cdcbd8e189e2909d37cf76c31da675cb1dba7dc0026",
  "plan": "free",
  "free_envelopes_remaining": 5
}
```

**请保存`api_key`——它只显示一次，之后无法再次获取。**

### 步骤2 — 创建签名信封

在`X-API-Key`头部使用步骤1中获取的`api_key`。对于标准合同，请使用`template_id`；对于自定义合同，请提供`clauses`。

```bash
curl -s -X POST https://api.saysigned.com/envelopes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ss_live_203bff0e53ba167462aa2cdcbd8e189e2909d37cf76c31da675cb1dba7dc0026" \
  -d '{
    "title": "Mutual NDA — Acme & Beta",
    "contract": {
      "template_id": "nda_mutual_v1",
      "variables": {
        "disclosing_party_name": "Acme Corp",
        "receiving_party_name": "Beta Inc",
        "effective_date": "2026-02-09",
        "purpose": "Evaluating a potential partnership",
        "governing_law_state": "California"
      }
    },
    "recipients": [
      {"name": "Alice", "email": "alice@acme.com", "role": "signer"},
      {"name": "Bob", "email": "bob@beta.com", "role": "signer"}
    ]
  }'
```

```json
{
  "id": "2c272d15-cd4b-4c0d-96c0-bd7438b66699",
  "status": "draft",
  "title": "Mutual NDA — Acme & Beta",
  "recipients": [
    {"id": "62f73ba5-05a0-4223-8f55-e880047a7b3e", "name": "Alice", "status": "pending"},
    {"id": "cc0aeb32-eb9d-420d-ab93-1d42400f85b9", "name": "Bob", "status": "pending"}
  ]
}
```

**保存签名信封的`id`以及每个接收者的`id`。**

### 步骤3 — 发送签名信封

此操作会消耗您免费套餐中的一个签名信封额度；如果使用付费套餐，则会触发一个计费事件。接收者会收到`access_token`，他们需要使用这些令牌进行签名。

```bash
curl -s -X POST https://api.saysigned.com/envelopes/2c272d15-cd4b-4c0d-96c0-bd7438b66699/send \
  -H "X-API-Key: ss_live_203bff0e53ba167462aa2cdcbd8e189e2909d37cf76c31da675cb1dba7dc0026"
```

```json
{
  "id": "2c272d15-cd4b-4c0d-96c0-bd7438b66699",
  "status": "sent",
  "recipients": [
    {"id": "62f73ba5-05a0-4223-8f55-e880047a7b3e", "name": "Alice", "status": "sent", "access_token": "600b9b4297b2921396a1db138a80801c7dfb5101..."},
    {"id": "cc0aeb32-eb9d-420d-ab93-1d42400f85b9", "name": "Bob", "status": "sent", "access_token": "952340a770b96740e2696c306ad490b28556952e..."}
  ]
}
```

**保存每个接收者的`access_token`，并将这些令牌分配给相应的签名者。**

### 步骤4 — 接收者签名

每个接收者都可以使用`X-Access-Token`头部（推荐）或`?access_token=`查询参数，通过自己的`access_token`进行签名。无需API密钥。

```bash
# Alice signs
curl -s -X POST "https://api.saysigned.com/envelopes/2c272d15-cd4b-4c0d-96c0-bd7438b66699/recipients/62f73ba5-05a0-4223-8f55-e880047a7b3e/sign" \
  -H "Content-Type: application/json" \
  -H "X-Access-Token: 600b9b4297b2921396a1db138a80801c7dfb5101..." \
  -d '{"signature_data": {"full_name": "Alice Chen", "title": "CEO"}}'
```

```json
{
  "signed": true,
  "recipient_id": "62f73ba5-05a0-4223-8f55-e880047a7b3e",
  "envelope_id": "2c272d15-cd4b-4c0d-96c0-bd7438b66699",
  "signed_at": "2026-02-09T04:09:24.111Z"
}
```

```bash
# Bob signs (last signer → envelope automatically completes with RFC 3161 timestamp)
curl -s -X POST "https://api.saysigned.com/envelopes/2c272d15-cd4b-4c0d-96c0-bd7438b66699/recipients/cc0aeb32-eb9d-420d-ab93-1d42400f85b9/sign" \
  -H "Content-Type: application/json" \
  -H "X-Access-Token: 952340a770b96740e2696c306ad490b28556952e..." \
  -d '{"signature_data": {"full_name": "Bob Smith", "title": "CTO"}}'
```

```json
{
  "signed": true,
  "recipient_id": "cc0aeb32-eb9d-420d-ab93-1d42400f85b9",
  "envelope_id": "2c272d15-cd4b-4c0d-96c0-bd7438b66699",
  "signed_at": "2026-02-09T04:09:25.190Z"
}
```

### 步骤5 — 验证（无需身份验证）

```bash
curl -s -X POST https://api.saysigned.com/verify \
  -H "Content-Type: application/json" \
  -d '{"envelope_id": "2c272d15-cd4b-4c0d-96c0-bd7438b66699"}'
```

```json
{
  "envelope_id": "2c272d15-cd4b-4c0d-96c0-bd7438b66699",
  "status": "completed",
  "chain_verification": {"valid": true, "entries_checked": 5},
  "timestamp_verification": {
    "valid": true,
    "gen_time": "2026-02-09T04:09:25+00:00",
    "tsa_name": "DigiCert SHA256 RSA4096 Timestamp Responder 2025 1"
  },
  "recipients": [
    {"name": "Alice", "email": "alice@acme.com", "role": "signer", "status": "signed", "signed_at": "2026-02-09T04:09:24.111Z"},
    {"name": "Bob", "email": "bob@beta.com", "role": "signer", "status": "signed", "signed_at": "2026-02-09T04:09:25.190Z"}
  ],
  "completed_at": "2026-02-09T04:09:25.039Z"
}
```

---

## 使用自定义合同

如果您有自定义的合同文本（例如用户提供的保密协议、服务协议或任何Markdown/纯文本文件），可以直接通过`clauses`字段传递。每个条款都需要包含`id`、`title`和`body`。

**单条款方式**（最简单的方法——将整个合同内容放在一个条款中）：

```bash
curl -s -X POST https://api.saysigned.com/envelopes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "title": "NDA — Acme & Beta",
    "contract": {
      "clauses": [
        {
          "id": "nda",
          "title": "Mutual Non-Disclosure Agreement",
          "body": "This Mutual Non-Disclosure Agreement is entered into by Acme Corp (\"Party A\") and Beta Inc (\"Party B\")...\n\n1. Definition of Confidential Information...\n\n2. Obligations of Receiving Party...\n\n3. Term. This Agreement shall remain in effect for two (2) years..."
        }
      ]
    },
    "recipients": [
      {"name": "Alice", "email": "alice@acme.com", "role": "signer"},
      {"name": "Bob", "email": "bob@beta.com", "role": "signer"}
    ]
  }'
```

**多条款方式**（将合同内容分成多个条款以便更清晰地展示）：

```bash
curl -s -X POST https://api.saysigned.com/envelopes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "title": "NDA — Acme & Beta",
    "contract": {
      "clauses": [
        {"id": "1", "title": "1. Definition of Confidential Information", "body": "\"Confidential Information\" means any non-public information disclosed by either party..."},
        {"id": "2", "title": "2. Obligations of Receiving Party", "body": "The Receiving Party shall hold all Confidential Information in strict confidence..."},
        {"id": "3", "title": "3. Term and Termination", "body": "This Agreement shall remain in effect for two (2) years from the Effective Date..."},
        {"id": "4", "title": "4. Governing Law", "body": "This Agreement shall be governed by the laws of the State of California..."}
      ]
    },
    "recipients": [
      {"name": "Alice", "email": "alice@acme.com", "role": "signer"},
      {"name": "Bob", "email": "bob@beta.com", "role": "signer"}
    ]
  }'
```

**在MCP中的对应操作**——结构相同，只需将其传递给`saysigned_create_envelope`：

```json
{
  "title": "NDA — Acme & Beta",
  "contract": {
    "clauses": [
      {"id": "nda", "title": "Mutual Non-Disclosure Agreement", "body": "Full text of the NDA here..."}
    ]
  },
  "recipients": [
    {"name": "Alice", "email": "alice@acme.com", "role": "signer"},
    {"name": "Bob", "email": "bob@beta.com", "role": "signer"}
  ]
}
```

> **何时使用哪种方式：** 当您需要使用标准合同并只需填写空白字段（如双方名称、日期等）时，使用**模板**。当您已经有合同文本（无论是从文件中获取的、用户提供的，还是自己起草的）时，使用**自定义条款**。

---

## 关键概念

- **ID是UUID** — 所有的签名信封ID、接收者ID和代理ID都是标准的UUID（例如：`2c272d15-cd4b-4c0d-96c0-bd7438b66699`）。
- **访问令牌是128个字符的十六进制字符串** — 通过`X-Access-Token`头部（推荐）或`?access_token=`查询参数传递。
- **API密钥前缀为`ss_live_`或`ss_test_`** — 使用REST接口时，通过`X-API-Key`头部传递；使用MCP接口时，通过`Authorization: Bearer <key>`传递（系统会自动转换）。
- **模板** — 使用`GET /templates`来查找可用的模板，使用`GET /templates/:id`来查看所需变量。
- **签名顺序** — 所有接收者可以同时签名（没有强制顺序）。
- **完成签名** — 当最后一个签名者完成签名后，签名信封会自动添加来自DigiCert的RFC 3161时间戳。

**免费套餐：** 每月5个签名信封额度，无需信用卡。** 升级方案：使用`POST /billing/setup`并传入`{"plan": "payg"}`。

- **交付方式** — `"api"`（默认）：返回访问令牌，用于程序化签名；`"email"`：向人类用户发送邀请邮件，用户需要在`doc.saysigned.com`页面上查看并同意签名。
- **电子邮件接收者** — 人类用户通过电子邮件链接中的URL令牌进行身份验证，而不是通过访问令牌。他们需要在浏览器中查看合同并点击“同意”或“拒绝”。

---

## MCP工具说明

这些工具与MCP（Model Context Protocol）运行时兼容。每个工具都对应一个REST API接口。

### saysigned_register

创建代理账户并获取API密钥。

```json
{
  "name": "saysigned_register",
  "description": "Register a new AI agent account on SaySigned. Returns an API key (shown once — save it). Free tier: 5 envelopes/month.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": { "type": "string", "description": "Agent or organization name" },
      "email": { "type": "string", "format": "email", "description": "Contact email (must be unique)" },
      "company_name": { "type": "string", "description": "Company name (optional)" },
      "webhook_url": { "type": "string", "format": "uri", "description": "URL to receive webhook notifications (optional)" }
    },
    "required": ["name", "email"]
  }
}
```

**REST接口：** `POST /agents/register` — 无需身份验证。

---

### saysigned_create_envelope

创建包含合同和接收者的签名信封草稿。

```json
{
  "name": "saysigned_create_envelope",
  "description": "Create a draft envelope with contract content and recipients. Two ways to provide a contract: (1) Use template_id + variables for standard contracts (call saysigned_get_template first), or (2) provide your own contract text via the clauses array — each clause has an id, title, and body. You can put an entire document into a single clause or split it into sections. Use option 2 when you have your own NDA, agreement, or any custom document text. Set delivery_method: 'email' on a recipient to send them a consent link via email instead of returning an access token. Does not send — call saysigned_send_envelope to dispatch.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": { "type": "string", "description": "Envelope title" },
      "description": { "type": "string", "description": "Brief description" },
      "contract": {
        "type": "object",
        "description": "Contract content. Use template_id + variables for templates, or provide raw clauses.",
        "properties": {
          "template_id": { "type": "string", "description": "Template ID (e.g., 'nda_mutual_v1', 'service_agreement_v1')" },
          "variables": { "type": "object", "description": "Template variables (see GET /templates/:id for schema)" },
          "clauses": {
            "type": "array",
            "description": "Custom clauses (when not using a template)",
            "items": {
              "type": "object",
              "properties": {
                "id": { "type": "string" },
                "title": { "type": "string" },
                "body": { "type": "string" }
              },
              "required": ["id", "title", "body"]
            }
          },
          "signature_block": {
            "type": "object",
            "description": "Custom signature block (when not using a template)"
          }
        }
      },
      "recipients": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "email": { "type": "string", "format": "email" },
            "role": { "type": "string", "enum": ["signer", "cc", "approver", "witness"], "default": "signer" },
            "delivery_method": { "type": "string", "enum": ["api", "email"], "default": "api", "description": "'api' (default) for AI agent signing, 'email' to send a consent link to a human" }
          },
          "required": ["name", "email"]
        }
      },
      "expires_at": { "type": "string", "format": "date-time", "description": "Expiration date (optional)" },
      "metadata": { "type": "object", "description": "Custom key-value metadata (optional)" }
    },
    "required": ["title", "contract", "recipients"]
  }
}
```

**REST接口：** `POST /envelopes` — 需要`X-API-Key`头部。

**示例——使用自定义合同（不使用模板）：**
```bash
curl -s -X POST https://api.saysigned.com/envelopes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"title": "Data Processing Addendum", "contract": {"clauses": [{"id": "scope", "title": "1. Scope", "body": "This addendum governs the processing of personal data..."}], "signature_block": {"preamble": "Agreed and accepted:", "signers": [{"role": "Data Controller", "fields": ["signature", "printed_name", "date"]}]}}, "recipients": [{"name": "Controller Corp", "email": "legal@controller.com", "role": "signer"}]}'
```

---

### saysigned_send_envelope

发送签名信封以供签名。此操作会消耗您免费套餐中的一个签名信封额度。

```json
{
  "name": "saysigned_send_envelope",
  "description": "Send a draft envelope for signing. For API recipients, generates access tokens. For email recipients, sends an invitation email with a consent link to doc.saysigned.com (no access_token in response). Consumes 1 envelope (free tier) or reports 1 metered event (paid). Returns 402 if free tier exhausted.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "envelope_id": { "type": "string", "format": "uuid", "description": "ID of the draft envelope to send" }
    },
    "required": ["envelope_id"]
  }
}
```

**REST接口：** `POST /envelopes/:id/send` — 需要`X-API-Key`头部。

**免费套餐使用完毕时的响应：**
```json
{"error": "Free tier envelope limit exhausted. Upgrade to a paid plan."}
```

---

### saysigned_sign

作为接收者进行签名。

```json
{
  "name": "saysigned_sign",
  "description": "Sign an envelope as a recipient. Provide the access_token from the send response as a query parameter. No API key needed — the token is the auth. Records IP, user-agent, and timestamp in the audit trail.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "envelope_id": { "type": "string", "format": "uuid" },
      "recipient_id": { "type": "string", "format": "uuid" },
      "access_token": { "type": "string", "description": "128-char hex token from the send response" },
      "signature_data": {
        "type": "object",
        "description": "Signature metadata",
        "properties": {
          "full_name": { "type": "string" },
          "title": { "type": "string" },
          "company": { "type": "string" }
        },
        "required": ["full_name"]
      }
    },
    "required": ["envelope_id", "recipient_id", "access_token", "signature_data"]
  }
}
```

**REST接口：** `POST /envelopes/:id/recipients/:rid/sign`，建议使用`X-Access-Token: TOKEN`头部或`?access_token=TOKEN`查询参数。无需API密钥。**

---

### saysignedDECLine

拒绝签名。

```json
{
  "name": "saysigned_decline",
  "description": "Decline to sign an envelope as a recipient. Optionally provide a reason.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "envelope_id": { "type": "string", "format": "uuid" },
      "recipient_id": { "type": "string", "format": "uuid" },
      "access_token": { "type": "string" },
      "reason": { "type": "string", "description": "Reason for declining (optional)" }
    },
    "required": ["envelope_id", "recipient_id", "access_token"]
  }
}
```

**REST接口：** `POST /envelopes/:id/recipients/:rid/decline`，建议使用`X-Access-Token: TOKEN`头部或`?access_token=TOKEN`查询参数。无需API密钥。**

---

### saysigned_get_envelope

获取签名信封的详细信息和接收者状态。

```json
{
  "name": "saysigned_get_envelope",
  "description": "Get full details of an envelope including status, contract content, and recipient statuses.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "envelope_id": { "type": "string", "format": "uuid" }
    },
    "required": ["envelope_id"]
  }
}
```

**REST接口：** `GET /envelopes/:id` — 需要`X-API-Key`头部。

---

### saysigned_void_envelope

取消已发送但未完成的签名信封。

```json
{
  "name": "saysigned_void_envelope",
  "description": "Void an envelope that has been sent but not yet completed. Cannot void completed envelopes.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "envelope_id": { "type": "string", "format": "uuid" },
      "reason": { "type": "string", "description": "Reason for voiding" }
    },
    "required": ["envelope_id"]
  }
}
```

**REST接口：** `POST /envelopes/:id/void` — 需要`X-API-Key`头部。

---

### saysigned_verify

验证签名的加密完整性。此操作无需身份验证。

```json
{
  "name": "saysigned_verify",
  "description": "Verify the cryptographic integrity of an envelope. Checks the hash chain audit trail and RFC 3161 timestamp. Public endpoint — no API key needed.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "envelope_id": { "type": "string", "format": "uuid" }
    },
    "required": ["envelope_id"]
  }
}
```

**REST接口：** `POST /verify`

请参考上面的[端到端示例](#step-5--verify-public-no-auth-needed)以了解实际的响应格式。

---

### saysigned_get_audit_trail

获取签名信封的完整哈希链审计记录。

```json
{
  "name": "saysigned_get_audit_trail",
  "description": "Get the complete cryptographic audit trail for an envelope, including hash chain verification status.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "envelope_id": { "type": "string", "format": "uuid" }
    },
    "required": ["envelope_id"]
  }
}
```

**REST接口：** `GET /envelopes/:id/audit-trail` — 需要`X-API-Key`头部。

---

### saysigned_get_profile

获取代理的个人信息和当前使用情况。

```json
{
  "name": "saysigned_get_profile",
  "description": "Get your agent profile, plan details, and current usage statistics.",
  "inputSchema": { "type": "object", "properties": {} }
}
```

**REST接口：** `GET /agents/me` — 需要`X-API-Key`头部。

---

### saysignedbilling_setup

从免费套餐升级到付费套餐。**重要提示：** 请务必将返回的`checkout_url`显示给人类用户，以便他们可以在浏览器中完成支付。**切勿自行使用该链接。**

```json
{
  "name": "saysigned_billing_setup",
  "description": "Upgrade to a paid plan. Creates a Stripe customer and returns a checkout URL. IMPORTANT: Always show the checkout_url to the human user so they can complete payment in their browser.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "plan": {
        "type": "string",
        "enum": ["payg", "commit_500", "commit_2000"],
        "description": "Plan to upgrade to. payg = $0.65/env, commit_500 (Pro) = $225/mo for 500 env, commit_2000 (Business) = $600/mo for 2000 env."
      }
    },
    "required": ["plan"]
  }
}
```

**REST接口：** `POST /billing/setup` — 需要`X-API-Key`头部。

---

### saysigned_get_usage

查看当前计费周期的使用情况。

```json
{
  "name": "saysigned_get_usage",
  "description": "Get envelope usage for the current billing period, including count, cost, and plan details.",
  "inputSchema": { "type": "object", "properties": {} }
}
```

**REST接口：** `GET /billing/usage` — 需要`X-API-Key`头部。

---

## 可用的模板

**可以通过编程方式查找模板：**

```bash
# List all templates
curl https://api.saysigned.com/templates

# Get template details with variable schema
curl https://api.saysigned.com/templates/nda_mutual_v1
```

### nda_mutual_v1 — 双方保密协议（Mutual Non-Disclosure Agreement）

标准的双方保密协议。所需变量：`disclosing_party_name`、`receiving_party_name`、`effective_date`、`purpose`、`governing_law_state`。可选变量：`term_years`（默认值：2年）、`non_solicitation`（默认值：false）等。

### service_agreement_v1 — 专业服务协议

专业服务合同。所需变量：`client_name`、`provider_name`、`effective_date`、`scope_of_services`、`compensation_model`、`governing_law_state`。支持4种支付方式：`fixed`、`hourly`、`milestone`、`retainer`。

---

## Webhook事件

在注册时配置`webhook_url`以接收实时通知。

| 事件 | 描述 |
|-------|-------------|
| `recipient.delivered` | 签名信封已发送，接收者收到通知（API接收者会收到`access_token`；电子邮件接收者不会收到） |
| `recipient.email_sent` | 向人类接收者发送邀请邮件 |
| `recipient.viewed` | 人类接收者打开了同意页面 |
| `recipient.signed` | 接收者完成了签名 |
| `recipient.declined` | 接收者拒绝签名 |
| `envelopecompleted` | 所有签名者都已完成签名，附带时间戳 |
| `envelope.declined` | 有接收者拒绝签名 |
| `envelope.voided` | 代理取消了签名信封 |

### Webhook数据格式

每个Webhook请求都会包含`X-Signature-256`头部，其中包含`sha256=<HMAC>`。请验证该头部以确保签名的有效性：

```python
import hmac, hashlib

def verify_webhook(body: bytes, secret: str, signature_header: str) -> bool:
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)
```

---

## 常见工作流程

### 双方保密协议（Two-Party NDA）

```
1. POST /envelopes (template_id: "nda_mutual_v1", 2 signer recipients)
2. POST /envelopes/:id/send
3. Party A signs: POST /envelopes/:id/recipients/:r1/sign (X-Access-Token header)
4. Party B signs: POST /envelopes/:id/recipients/:r2/sign (X-Access-Token header)
5. → envelope.completed webhook fires, RFC 3161 timestamp anchored
6. POST /verify to confirm integrity
```

### 包含第三方签署的服务协议（Service Agreement with CC）

```
1. POST /envelopes (template_id: "service_agreement_v1", 2 signers + 1 CC)
2. POST /envelopes/:id/send
3. Both signers sign (in any order)
4. CC recipient receives notifications but doesn't sign
5. → envelope.completed on last signature
```

### 处理拒绝签名的情况

```
1. Recipient declines: POST /envelopes/:id/recipients/:rid/decline
2. → recipient.declined webhook fires
3. → envelope.declined webhook fires (envelope status → declined)
4. Create a new envelope with revised terms if needed
```

### 人类接收者的操作流程

```
1. POST /envelopes (set delivery_method: "email" on human recipients)
2. POST /envelopes/:id/send → invitation email sent to human
3. Human opens email → clicks "Review & Give Consent" link
4. Human reviews contract at doc.saysigned.com → gives consent or declines
5. → recipient.signed or recipient.declined webhook fires
6. Envelope auto-completes when all signers consent
7. Human receives confirmation email with 14-day document viewing link
```

### 轮询签名完成情况

如果您不使用Webhook，可以定期检查签名信封的完成状态：

```
1. Call GET /envelopes/:id (or saysigned_get_envelope) to check status
2. Poll every 5-10 seconds
3. Terminal states: completed, declined, voided
4. Max recommended wait: 24 hours
```

---

## 错误处理

| 状态 | 含义 | 应采取的措施 |
|--------|---------|------------|
| 400 | 请求错误/验证失败 | 检查请求体是否符合格式要求 |
| 401 | API密钥无效或缺失 | 确认`X-API-Key`头部的内容 |
| 402 | 免费套餐额度已用完 | 调用`POST /billing/setup`并向人类用户显示`checkout_url` |
| 404 | 资源未找到 | 检查签名信封/接收者的ID是否正确 |
| 409 | 状态转换无效 | 首先检查签名信封/接收者的状态 |
| 429 | 请求频率限制 | 暂停请求并稍后重试 |

## 安全注意事项

- **API密钥** 在创建账户时仅显示一次，请妥善保管。
- **访问令牌** 是为每个接收者和每个签名信封单独生成的，不得重复使用。
- **Webhook密钥** 是为每个代理单独设置的。请验证每个Webhook请求的签名信息。
- 所有连接都必须使用**TLS**（HTTPS）协议。
- API密钥以**SHA-256哈希值**的形式存储——SaySigned不会以明文形式保存密钥。
- **电子邮件接收者的URL令牌** 是32个字符的HMAC签名令牌，仅限一次性使用，签名完成后会被清除。
- 在同意或拒绝签名的表单中启用CSRF保护——令牌与接收者ID关联，并在4小时后失效。
- 对于同意操作，设置请求频率限制：每个IP地址每15分钟最多尝试10次，每个接收者每5分钟最多提交3次。

## 法律背景

- **《ESIGN法案》（15 U.S.C. § 7001）**：电子签名具有与手写签名相同的法律效力。
- **《UETA第14条》**：明确授权电子代理创建合同和进行交易。
- **签名追踪记录**：每个签名都会记录签名者信息（姓名、电子邮件地址）、签名时间、签名方式（API、IP地址、用户代理）以及合同内容。
- **RFC 3161时间戳**：由DigiCert提供的独立时间戳，用于证明签名操作在特定时间完成。
- **哈希链**：每个签名操作都会在哈希链中留下痕迹，便于追踪签名顺序。
- **《ESIGN法案》规定的披露要求**：必须向人类接收者披露四项信息：获取纸质副本的权利、撤销同意的权利、合同适用范围以及硬件/软件要求。

## 定价方案

| 计划类型 | 价格 | 每月签名信封数量 |
|------|-------|-----------|
| 免费 | $0/月 | 5个 |
| 按次付费 | $0.65/个 | 无限量 |
| 专业版 | $225/月 | 包含500个签名信封，超出部分每个$0.45 |
| 企业版 | $600/月 | 包含2,000个签名信封，超出部分每个$0.30 |
| 企业高级版 | 定制价格 | 每月10,000个以上 |

随时可以升级：使用`POST /billing/setup`并传入`{"plan": "payg"}`、`{"plan": "commit_500"}`或`{"plan": "commit_2000"}`。响应中会包含`checkout_url`——请务必将此链接提供给人类用户，以便他们在浏览器中完成支付。
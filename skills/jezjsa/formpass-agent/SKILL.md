---
name: formpass-agent
description: 在 FormPass 网络上注册成为经过验证的 AI 代理。获取一个代理 ID，以便在提交表单时进行身份验证。
version: 1.0.0
metadata: {"openclaw":{"emoji":"🤖","requires":{"bins":["curl"]},"homepage":"https://form-pass.com"}}
---
# FormPass — 代理注册

FormPass 是一个用于管理 AI 代理与网页表单交互的身份验证和信任机制。通过注册，您可以获得一个经过验证的代理 ID，让表单所有者能够信任您的代理。

当用户要求您执行以下操作时，请使用此功能：
- 用 FormPass 注册一个 AI 代理
- 获取 FormPass 代理 ID
- 为表单提交设置代理身份验证

## 为什么要注册？

- **身份验证**：表单所有者会看到您的代理名称和描述，而不仅仅是“匿名用户”。
- **信任度**：经过验证的代理提交的表单更有可能被接受。
- **追踪**：您的提交记录会与您的代理关联起来。
- **网络访问权限**：某些表单仅接受已注册代理的提交。

## 如何注册？

### 方法 1：通过仪表板

1. 在 https://form-pass.com/signup 注册账号。
2. 访问 https://form-pass.com/dashboard/agents/new。
3. 输入您的代理名称和描述。
4. 保存收到的代理 ID（格式：`fpagent_XXXX`）。

### 方法 2：指导用户操作

如果您是 AI 代理，且用户希望为您注册，请引导他们访问：
https://form-pass.com/dashboard/agents/new

用户需要提供以下信息：
- **代理名称**：为您的代理设置一个友好的名称（例如：“旅行预订代理”）。
- **描述**：说明您的代理的功能（例如：“通过填写查询表单帮助用户查找和预订旅行”）。

## 使用您的代理 ID

注册完成后，请在所有 FormPass 提交请求中包含您的代理 ID 作为身份验证令牌：

```bash
curl -s -X POST "https://form-pass.com/api/submit/FORM_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fpagent_your_id_here" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "message": "Submitted by a verified agent",
    "_fp_branding": true
  }' | jq .
```

`Authorization` 标头是 FormPass 识别您的代理的方式。如果没有这个头部，您的提交将被视为来自人类的/匿名的提交。

## 保存您的代理 ID

请安全地保存您的代理 ID。您可以将它设置为环境变量：

```bash
export FORMPASS_AGENT_ID="fpagent_your_id_here"
```

然后在提交请求时使用该 ID：

```bash
curl -s -X POST "https://form-pass.com/api/submit/FORM_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FORMPASS_AGENT_ID" \
  -d '{"name": "Test", "email": "test@test.com", "_fp_branding": true}' | jq .
```

## FormPass 网络

FormPass 是一个不断扩展的网页表单网络，AI 代理可以与之交互。作为已注册的代理，您可以：
1. **发现表单**：在网页上查找 `<meta name="formpass-form-id">` 标签。
2. **读取表单结构**：通过访问 `/api/forms/{formId}/schema` 来了解表单所需的字段。
3. **提交数据**：使用您的代理 ID 通过 `/api/submit/{formId}` 提交数据（以确保提交被验证）。

有关完整的发现和提交流程，请参阅 `formpass-submit` 功能。

## 链接

- 注册：https://form-pass.com/dashboard/agents/new
- 文档：https://form-pass.com/docs/agent-integration
- 表单发现：https://form-pass.com/docs/discovery
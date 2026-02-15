---
name: jotform
description: |
  JotForm API integration with managed OAuth. Create forms, manage submissions, and access form data. Use this skill when users want to interact with JotForm forms and submissions. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# JotForm

您可以使用托管的 OAuth 认证来访问 JotForm API。该 API 允许您创建和管理表单、检索表单提交数据以及配置 Webhook 功能。

## 快速入门

```bash
# List user forms
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/jotform/user/forms?limit=20')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/jotform/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 JotForm API 端点路径。该网关会将请求代理到 `api.jotform.com`，并自动插入您的 API 密钥。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 JotForm 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=jotform&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'jotform'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "jotform",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 JotForm 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/jotform/user/forms')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户

```bash
GET /jotform/user
GET /jotform/user/forms?limit=20
GET /jotform/user/submissions?limit=20
GET /jotform/user/usage
```

### 表单

#### 获取表单信息

```bash
GET /jotform/form/{formId}
```

#### 获取表单问题（表单字段信息）

```bash
GET /jotform/form/{formId}/questions
```

#### 获取表单提交数据

```bash
GET /jotform/form/{formId}/submissions?limit=20
```

**支持过滤：**

```bash
GET /jotform/form/{formId}/submissions?filter={"created_at:gt":"2024-01-01"}
```

#### 创建表单

```bash
POST /jotform/user/forms
Content-Type: application/json

{
  "properties": {"title": "Contact Form"},
  "questions": {
    "1": {"type": "control_textbox", "text": "Name", "name": "name"},
    "2": {"type": "control_email", "text": "Email", "name": "email"}
  }
}
```

#### 删除表单

```bash
DELETE /jotform/form/{formId}
```

### 表单提交数据

#### 获取提交信息

```bash
GET /jotform/submission/{submissionId}
```

#### 删除提交数据

```bash
DELETE /jotform/submission/{submissionId}
```

### Webhook

```bash
GET /jotform/form/{formId}/webhooks
POST /jotform/form/{formId}/webhooks
DELETE /jotform/form/{formId}/webhooks/{webhookIndex}
```

## 表单字段类型

- `control_textbox` - 单行文本
- `control_textarea` - 多行文本
- `control_email` - 电子邮件地址
- `control_phone` - 电话号码
- `controlDropdown` - 下拉菜单
- `control_radio` - 单选按钮
- `controlCheckbox` - 复选框
- `control_datetime` - 日期/时间选择器
- `control_fileupload` - 文件上传

## 过滤语法

```json
{"field:gt":"value"}  // Greater than
{"field:lt":"value"}  // Less than
{"field:eq":"value"}  // Equal to
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/jotform/user/forms?limit=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/jotform/user/forms',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 10}
)
```

## 注意事项

- 表单 ID 为数字类型。
- 分页使用 `limit` 和 `offset` 参数。
- 使用 `orderby` 参数对结果进行排序。
- 重要提示：当 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 选项可以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致 “无效 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 JotForm 连接 |
| 401 | API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自 JotForm API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保已设置 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出所有连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称错误

1. 确保您的 URL 路径以 `jotform` 开头。例如：
- 正确格式：`https://gateway.maton.ai/jotform/user/forms`
- 错误格式：`https://gateway.maton.ai/user/forms`

## 资源

- [JotForm API 概述](https://api.jotform.com/docs/)
- [用户表单](https://api.jotform.com/docs/#user-forms)
- [表单提交数据](https://api.jotform.com/docs/#form-id-submissions)
- [Webhook](https://api.jotform.com/docs/#form-id-webhooks)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)
---
name: google-forms
description: |
  Google Forms API integration with managed OAuth. Create forms, add questions, and retrieve responses. Use this skill when users want to interact with Google Forms. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google 表单

通过管理的 OAuth 认证来访问 Google 表单 API。您可以创建表单、添加问题并检索回复。

## 快速入门

```bash
# Get form
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-forms/v1/forms/{formId}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-forms/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google 表单 API 端点路径。该网关会将请求代理到 `forms.googleapis.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-forms&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-forms'}).encode()
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
    "app": "google-forms",
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

如果您有多个 Google 表单连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-forms/v1/forms/{formId}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 获取表单信息

```bash
GET /google-forms/v1/forms/{formId}
```

### 创建表单

```bash
POST /google-forms/v1/forms
Content-Type: application/json

{
  "info": {
    "title": "Customer Feedback Survey"
  }
}
```

### 批量更新表单

```bash
POST /google-forms/v1/forms/{formId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "createItem": {
        "item": {
          "title": "What is your name?",
          "questionItem": {
            "question": {
              "required": true,
              "textQuestion": {"paragraph": false}
            }
          }
        },
        "location": {"index": 0}
      }
    }
  ]
}
```

### 列出回复

```bash
GET /google-forms/v1/forms/{formId}/responses
```

### 获取单个回复

```bash
GET /google-forms/v1/forms/{formId}/responses/{responseId}
```

## 常见的批量更新请求

### 创建文本问题

```json
{
  "createItem": {
    "item": {
      "title": "Question text",
      "questionItem": {
        "question": {
          "required": true,
          "textQuestion": {"paragraph": false}
        }
      }
    },
    "location": {"index": 0}
  }
}
```

### 创建多项选择题

```json
{
  "createItem": {
    "item": {
      "title": "Select an option",
      "questionItem": {
        "question": {
          "choiceQuestion": {
            "type": "RADIO",
            "options": [
              {"value": "Option A"},
              {"value": "Option B"}
            ]
          }
        }
      }
    },
    "location": {"index": 0}
  }
}
```

### 创建评分题

```json
{
  "createItem": {
    "item": {
      "title": "Rate your experience",
      "questionItem": {
        "question": {
          "scaleQuestion": {
            "low": 1,
            "high": 5,
            "lowLabel": "Poor",
            "highLabel": "Excellent"
          }
        }
      }
    },
    "location": {"index": 0}
  }
}
```

## 问题类型

- `textQuestion` - 简短文本或段落文本
- `choiceQuestion` - 单选、复选或下拉选项
- `scaleQuestion` - 线性评分题
- `dateQuestion` - 日期选择器
- `timeQuestion` - 时间选择器

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/google-forms/v1/forms/FORM_ID/responses',
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
    f'https://gateway.maton.ai/google-forms/v1/forms/FORM_ID/responses',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
```

## 注意事项

- 表单 ID 可以从表单 URL 中找到。
- 使用 `updateMask` 来指定需要更新的字段。
- 位置索引从 0 开始。
- 重要提示：当 URL 包含括号时，使用 `curl -g` 以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致 “无效的 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Google 表单连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自 Google 表单 API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `google-forms` 开头。例如：

- 正确：`https://gateway.maton.ai/google-forms/v1/forms/{formId}`
- 错误：`https://gateway.maton.ai/forms/v1/forms/{formId}`

## 资源

- [表单 API 概述](https://developers.google.com/workspace/forms/api/reference/rest)
- [获取表单信息](https://developers.google.com/workspace/forms/api/reference/rest/v1/forms/get)
- [创建表单](https://developers.google.com/workspace/forms/api/reference/rest/v1/forms/create)
- [批量更新表单](https://developers.google.com/workspace/forms/api/reference/rest/v1/forms/batchUpdate)
- [列出回复](https://developers.google.com/workspace/forms/api/reference/rest/v1/formsresponses/list)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)
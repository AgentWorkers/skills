---
name: typeform
description: |
  Typeform API integration with managed OAuth. Create forms, manage responses, and access insights. Use this skill when users want to interact with Typeform surveys and responses. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Typeform

通过管理的OAuth认证来访问Typeform API。您可以创建和管理表单、检索响应数据以及获取分析报告。

## 快速入门

```bash
# List forms
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/typeform/forms?page_size=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/typeform/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Typeform API端点路径。该网关会将请求代理到 `api.typeform.com` 并自动插入您的OAuth令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的Typeform OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=typeform&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'typeform'}).encode()
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

**响应数据：**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "typeform",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth认证。

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

如果您有多个Typeform连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/typeform/forms?page_size=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API参考

### 用户

```bash
GET /typeform/me
```

### 表单

#### 列出表单

```bash
GET /typeform/forms?page_size=10
```

#### 获取表单信息

```bash
GET /typeform/forms/{formId}
```

#### 创建表单

```bash
POST /typeform/forms
Content-Type: application/json

{
  "title": "Customer Survey",
  "fields": [
    {"type": "short_text", "title": "What is your name?"},
    {"type": "email", "title": "What is your email?"}
  ]
}
```

#### 更新表单

```bash
PUT /typeform/forms/{formId}
Content-Type: application/json

{
  "title": "Updated Survey Title",
  "fields": [...]
}
```

#### 删除表单

```bash
DELETE /typeform/forms/{formId}
```

### 响应数据

#### 列出响应

```bash
GET /typeform/forms/{formId}/responses?page_size=25
```

支持过滤：

```bash
GET /typeform/forms/{formId}/responses?since=2024-01-01T00:00:00Z&until=2024-12-31T23:59:59Z&completed=true
```

### 分析报告

```bash
GET /typeform/insights/{formId}/summary
```

### 工作区

```bash
GET /typeform/workspaces
GET /typeform/workspaces/{workspaceId}
```

## 字段类型

- `short_text` - 单行文本
- `long_text` - 多行文本
- `email` - 电子邮件地址
- `number` - 数字输入
- `rating` - 星级评分
- `opinion_scale` - 0-10 分数等级
- `multiple_choice` - 单选或多选
- `yes_no` - 布尔值
- `date` - 日期选择器
- `dropdown` - 下拉菜单

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/typeform/forms?page_size=10',
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
    'https://gateway.maton.ai/typeform/forms',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'page_size': 10}
)
```

## 注意事项

- 表单ID是字母数字字符串。
- 响应数据的分页使用 `before` 令牌。
- 时间戳采用ISO 8601格式。
- DELETE操作返回HTTP 204状态码。
- 重要提示：当URL包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 命令可以避免全局解析问题。
- 重要提示：在将curl输出传递给 `jq` 或其他命令时，某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确解析，这可能导致“无效API密钥”的错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立Typeform连接 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 每个账户的请求限制（10次/秒） |
| 4xx/5xx | 来自Typeform API的传递错误 |

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的URL路径以 `typeform` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/typeform/forms`
- 错误的路径：`https://gateway.maton.ai/forms`

## 资源

- [Typeform API概述](https://www.typeform.com/developers/get-started)
- [表单](https://www.typeform.com/developers/create/reference/retrieve-forms)
- [响应数据](https://www.typeform.com/developers/responses/reference/retrieve-responses)
- [工作区](https://www.typeform.com/developers/create/reference/retrieve-workspaces)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)
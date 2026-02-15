---
name: google-slides
description: |
  Google Slides API integration with managed OAuth. Create presentations, add slides, insert content, and manage slide formatting. Use this skill when users want to interact with Google Slides. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Slides

您可以使用托管的 OAuth 认证来访问 Google Slides API。该 API 允许您创建和管理演示文稿、添加幻灯片、插入文本和图片，并控制格式设置。

## 快速入门

```bash
# Create a new presentation
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'title': 'My Presentation'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/google-slides/v1/presentations', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-slides/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google Slides API 端点路径。该网关会将请求代理到 `slides.googleapis.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-slides&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-slides'}).encode()
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
    "app": "google-slides",
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

如果您有多个 Google Slides 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'title': 'My Presentation'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/google-slides/v1/presentations', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API 参考

### 演示文稿

#### 创建演示文稿

```bash
POST /google-slides/v1/presentations
Content-Type: application/json

{
  "title": "My Presentation"
}
```

#### 获取演示文稿信息

```bash
GET /google-slides/v1/presentations/{presentationId}
```

### 幻灯片（Pages）

#### 获取幻灯片信息

```bash
GET /google-slides/v1/presentations/{presentationId}/pages/{pageId}
```

#### 获取幻灯片缩略图

```bash
GET /google-slides/v1/presentations/{presentationId}/pages/{pageId}/thumbnail
```

**自定义尺寸：**

```bash
GET /google-slides/v1/presentations/{presentationId}/pages/{pageId}/thumbnail?thumbnailProperties.mimeType=PNG&thumbnailProperties.thumbnailSize=LARGE
```

### 批量更新

`batchUpdate` 端点用于执行大多数修改操作。它接受一个请求数组，并将这些请求原子性地应用到演示文稿中。

```bash
POST /google-slides/v1/presentations/{presentationId}:batchUpdate
Content-Type: application/json

{
  "requests": [...]
}
```

#### 创建幻灯片

```bash
POST /google-slides/v1/presentations/{presentationId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "createSlide": {
        "objectId": "slide_001",
        "slideLayoutReference": {
          "predefinedLayout": "TITLE_AND_BODY"
        }
      }
    }
  ]
}
```

可用的预定义布局：
- `BLANK`
- `TITLE`
- `TITLE_AND_BODY`
- `TITLE_AND_TWO_COLUMNS`
- `TITLE_ONLY`
- `SECTION_HEADER`
- `ONE_COLUMN_TEXT`
- `MAIN_POINT`
- `BIG_NUMBER`

#### 插入文本

```bash
POST /google-slides/v1/presentations/{presentationId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "insertText": {
        "objectId": "{shapeId}",
        "text": "Hello, World!",
        "insertionIndex": 0
      }
    }
  ]
}
```

#### 删除文本

```bash
POST /google-slides/v1/presentations/{presentationId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "deleteText": {
        "objectId": "{shapeId}",
        "textRange": {
          "type": "ALL"
        }
      }
    }
  ]
}
```

#### 创建形状

```bash
POST /google-slides/v1/presentations/{presentationId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "createShape": {
        "objectId": "shape_001",
        "shapeType": "TEXT_BOX",
        "elementProperties": {
          "pageObjectId": "{slideId}",
          "size": {
            "width": {"magnitude": 300, "unit": "PT"},
            "height": {"magnitude": 100, "unit": "PT"}
          },
          "transform": {
            "scaleX": 1,
            "scaleY": 1,
            "translateX": 100,
            "translateY": 100,
            "unit": "PT"
          }
        }
      }
    }
  ]
}
```

#### 创建图片

```bash
POST /google-slides/v1/presentations/{presentationId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "createImage": {
        "objectId": "image_001",
        "url": "https://example.com/image.png",
        "elementProperties": {
          "pageObjectId": "{slideId}",
          "size": {
            "width": {"magnitude": 200, "unit": "PT"},
            "height": {"magnitude": 200, "unit": "PT"}
          },
          "transform": {
            "scaleX": 1,
            "scaleY": 1,
            "translateX": 200,
            "translateY": 200,
            "unit": "PT"
          }
        }
      }
    }
  ]
}
```

#### 删除对象

```bash
POST /google-slides/v1/presentations/{presentationId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "deleteObject": {
        "objectId": "{objectId}"
      }
    }
  ]
}
```

#### 更新文本样式

```bash
POST /google-slides/v1/presentations/{presentationId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "updateTextStyle": {
        "objectId": "{shapeId}",
        "textRange": {
          "type": "ALL"
        },
        "style": {
          "bold": true,
          "fontSize": {"magnitude": 24, "unit": "PT"},
          "foregroundColor": {
            "opaqueColor": {
              "rgbColor": {"red": 0.2, "green": 0.4, "blue": 0.8}
            }
          }
        },
        "fields": "bold,fontSize,foregroundColor"
      }
    }
  ]
}
```

#### 替换所有文本

```bash
POST /google-slides/v1/presentations/{presentationId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "replaceAllText": {
        "containsText": {
          "text": "{{placeholder}}",
          "matchCase": true
        },
        "replaceText": "Actual Value"
      }
    }
  ]
}
```

## 代码示例

### JavaScript

```javascript
// Create a presentation
const response = await fetch(
  'https://gateway.maton.ai/google-slides/v1/presentations',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({ title: 'My Presentation' })
  }
);

const presentation = await response.json();
const presentationId = presentation.presentationId;

// Add a slide
await fetch(
  `https://gateway.maton.ai/google-slides/v1/presentations/${presentationId}:batchUpdate`,
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      requests: [
        {
          createSlide: {
            slideLayoutReference: { predefinedLayout: 'TITLE_AND_BODY' }
          }
        }
      ]
    })
  }
);
```

### Python

```python
import os
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'
}

# Create a presentation
response = requests.post(
    'https://gateway.maton.ai/google-slides/v1/presentations',
    headers=headers,
    json={'title': 'My Presentation'}
)
presentation = response.json()
presentation_id = presentation['presentationId']

# Add a slide
requests.post(
    f'https://gateway.maton.ai/google-slides/v1/presentations/{presentation_id}:batchUpdate',
    headers=headers,
    json={
        'requests': [
            {
                'createSlide': {
                    'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}
                }
            }
        ]
    }
)
```

## 注意事项

- 对象 ID 在整个演示文稿中必须是唯一的。
- 所有修改操作（添加幻灯片、文本、形状等）都应使用 `batchUpdate` 方法。
- `batchUpdate` 中的多个请求会原子性地应用。
- 尺寸和位置以 PT（点）为单位（72 点 = 1 英寸）。
- 使用 `replaceAllText` 方法生成基于模板的演示文稿。
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 选项可以禁用全局解析。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致“无效 API 密钥”错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Google Slides 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 演示文稿未找到 |
| 429 | 每个账户的请求速率限制（10 次/秒） |
| 4xx/5xx | 来自 Google Slides API 的传递错误 |

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

1. 确保您的 URL 路径以 `google-slides` 开头。例如：
- 正确：`https://gateway.maton.ai/google-slides/v1/presentations`
- 错误：`https://gateway.maton.ai/slides/v1/presentations`

## 资源

- [Slides API 概述](https://developers.google.com/slides/api/reference/rest)
- [演示文稿](https://developers.google.com/slides/api/reference/rest/v1/presentations)
- [幻灯片（Pages）](https://developers.google.com/slides/api/reference/rest/v1/presentations/pages)
- [批量更新请求](https://developers.google.com/slides/api/reference/rest/v1/presentations/batchUpdate)
- [幻灯片布局](https://developers.google.com/slides/api/reference/rest/v1/presentations/create#predefinedlayout)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)
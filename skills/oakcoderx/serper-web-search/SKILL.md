---
name: serper
description: 通过 Serper API 进行 Google 搜索。当用户需要搜索网页且拥有 Serper API 密钥时，可以使用此功能。触发条件包括：(1) 用户请求进行网页搜索；(2) 用户希望获取 Google 搜索结果；(3) 用户提供了 Serper API 密钥。
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["curl"], "env": ["SERPER_API_KEY"] } } }
---

# Serper Search

使用 Serper API 来获取 Google 搜索结果。

## API 详情

- **端点**: `https://google.serper.dev/search`
- **方法**: POST
- **请求头**: `X-API-Key: $SERPER_API_KEY`, `Content-Type: application/json`
- **请求体**: `{"q": "你的查询内容"}`

## 使用方法

### 使用 API 环境变量

```bash
SERPER_API_KEY="your-key" curl -s -X POST "https://google.serper.dev/search" \
  -H "X-API-Key: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "your query"}'
```

### 直接使用 API 密钥

```bash
curl -s -X POST "https://google.serper.dev/search" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "your query"}'
```

## 脚本示例

使用随附的 `search` 脚本：

```bash
./scripts/search "your query"
```

## 响应格式

返回 JSON 数据，包含以下内容：
- `organic[]` - 搜索结果（标题、链接、摘要）
- `searchParameters.q` - 原始查询内容
- `credits` - 使用的信用信息（如 API 许可证等）

示例响应：
```json
{
  "searchParameters": {"q": "test", "type": "search"},
  "organic": [
    {"title": "Result Title", "link": "https://...", "snippet": "Description...", "position": 1}
  ],
  "credits": 1
}
```

## 获取 API 密钥

1. 访问 https://serper.dev
2. 注册一个账户
3. 从控制面板中获取 API 密钥
4. 将 `SERPER_API_KEY` 设置为环境变量，或直接在代码中传递该密钥
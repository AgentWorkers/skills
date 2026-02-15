---
name: octolens
description: **从 Octolens API 查询和分析品牌提及**  
当用户需要获取品牌提及信息、追踪关键词、按来源平台（如 Twitter、Reddit、GitHub、LinkedIn 等）进行筛选、进行情感分析或分析社交媒体互动时，可以使用此功能。该 API 支持使用 AND/OR 逻辑进行复杂过滤、设置日期范围、查看粉丝数量以及添加书签等操作。
license: MIT
metadata:
  author: octolens
  version: "1.0"
compatibility: Requires Node.js 18+ (for fetch API) and access to the internet
allowed-tools: Node Read
---

# Octolens API 技能

## 何时使用此技能

当用户需要执行以下操作时，可以使用此技能：
- 从社交媒体和其他平台获取品牌提及信息
- 按来源（Twitter、Reddit、GitHub、LinkedIn、YouTube、HackerNews、DevTO、StackOverflow、Bluesky、新闻通讯、播客）筛选提及内容
- 分析情感（正面、中性、负面）
- 按作者的关注者数量或互动程度进行筛选
- 搜索特定关键词或标签
- 按日期范围查询提及内容
- 列出可用的关键词或已保存的查看记录
- 应用包含 AND/OR 条件的复杂筛选逻辑

## API 认证

Octolens API 需要使用 Bearer 令牌进行认证。用户应提供他们的 API 密钥，您可以在 `Authorization` 头部中使用该密钥：

```
Authorization: Bearer YOUR_API_KEY
```

**重要提示**：在进行任何 API 调用之前，务必先获取用户的 API 密钥，并将其存储在变量中以供后续请求使用。

## 基础 URL

所有 API 端点都使用以下基础 URL：`https://app.octolens.com/api/v1`

## 速率限制

- **限制**：每小时 500 次请求
- **检查头部信息**：`X-RateLimit-*` 头部字段可显示当前使用情况

## 可用的端点

### 1. POST /mentions

获取与关键词匹配的提及内容，并支持可选的筛选条件。返回按时间戳排序的帖子（最新内容优先）。

**关键参数**：
- `limit`（数字，1-100）：返回的最大结果数量（默认值：20）
- `cursor`（字符串）：来自上一次响应的分页游标
- `includeAll`（布尔值）：是否包含相关性较低的帖子（默认值：false）
- `view`（数字）：用于筛选的查看记录 ID
- `filters`（对象）：筛选条件（详见筛选部分）

**示例响应**：
```json
{
  "data": [
    {
      "id": "abc123",
      "url": "https://twitter.com/user/status/123",
      "body": "Just discovered @YourProduct - this is exactly what I needed!",
      "source": "twitter",
      "timestamp": "2024-01-15T10:30:00Z",
      "author": "user123",
      "authorName": "John Doe",
      "authorFollowers": 5420,
      "relevance": "relevant",
      "sentiment": "positive",
      "language": "en",
      "tags": ["feature-request"],
      "keywords": [{ "id": 1, "keyword": "YourProduct" }],
      "bookmarked": false,
      "engaged": false
    }
  ],
  "cursor": "eyJsYXN0SWQiOiAiYWJjMTIzIn0="
}
```

### 2. GET /keywords

列出组织配置的所有关键词。

**示例响应**：
```json
{
  "data": [
    {
      "id": 1,
      "keyword": "YourProduct",
      "platforms": ["twitter", "reddit", "github"],
      "color": "#6366f1",
      "paused": false,
      "context": "Our main product name"
    }
  ]
}
```

### 3. GET /views

列出所有已保存的查看记录（预配置的筛选条件）。

**示例响应**：
```json
{
  "data": [
    {
      "id": 1,
      "name": "High Priority",
      "icon": "star",
      "filters": {
        "sentiment": ["positive", "negative"],
        "source": ["twitter"]
      },
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## 筛选提及内容

`/mentions` 端点支持两种强大的筛选模式：

### 简单模式（隐式 AND）

直接在筛选条件中输入字段。所有条件都会被组合成 AND 关系进行筛选。

```json
{
  "filters": {
    "source": ["twitter", "linkedin"],
    "sentiment": ["positive"],
    "minXFollowers": 1000
  }
}
```
→ `source IN (twitter, linkedin) AND sentiment = positive AND followers ≥ 1000`

### 排除某些值

在数组字段前加上 `!` 以排除特定值：

```json
{
  "filters": {
    "source": ["twitter"],
    "!keyword": [5, 6]
  }
}
```
→ `source = twitter AND keyword NOT IN (5, 6)`

### 高级模式（AND/OR 组合）

使用 `operator` 和 `groups` 来实现复杂的逻辑：

```json
{
  "filters": {
    "operator": "AND",
    "groups": [
      {
        "operator": "OR",
        "conditions": [
          { "source": ["twitter"] },
          { "source": ["linkedin"] }
        ]
      },
      {
        "operator": "AND",
        "conditions": [
          { "sentiment": ["positive"] },
          { "!tag": ["spam"] }
        ]
      }
    ]
  }
}
```
→ `(source = twitter OR source = linkedin) AND (sentiment = positive AND tag ≠ spam)`

### 可用的筛选字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `source` | 字符串数组 | 平台：twitter、reddit、github、linkedin、youtube、hackernews、devto、stackoverflow、bluesky、newsletter、podcast |
| `sentiment` | 字符串数组 | 情感值：positive、neutral、negative |
| `keyword` | 字符串数组 | 关键词 ID（从 /keywords 端点获取） |
| `language` | 字符串数组 | ISO 639-1 语言代码：en、es、fr、de、pt、it、nl、ja、ko、zh |
| `tag` | 字符串数组 | 标签名称 |
| `bookmarked` | 布尔值 | 筛选已标记的帖子（true）或未标记的帖子（false） |
| `engaged` | 布尔值 | 筛选互动过的帖子（true）或未互动的帖子（false） |
| `minXFollowers` | 数字 | 最小 Twitter 关注者数量 |
| `maxXFollowers` | 数字 | 最大 Twitter 关注者数量 |
| `startDate` | 字符串 | ISO 8601 格式（例如：2024-01-15T00:00:00Z） |
| `endDate` | 字符串 | ISO 8601 格式 |

## 使用捆绑脚本

此技能包含用于常见操作的辅助脚本。使用这些脚本可以快速与 API 进行交互：

### 获取提及内容
```bash
node scripts/fetch-mentions.js YOUR_API_KEY [limit] [includeAll]
```

### 列出关键词
```bash
node scripts/list-keywords.js YOUR_API_KEY
```

### 列出查看记录
```bash
node scripts/list-views.js YOUR_API_KEY
```

### 自定义筛选查询
```bash
node scripts/query-mentions.js YOUR_API_KEY '{"source": ["twitter"], "sentiment": ["positive"]}' [limit]
```

### 高级查询
```bash
node scripts/advanced-query.js YOUR_API_KEY [limit]
```

## 最佳实践

1. **在进行请求之前，务必先获取 API 密钥**
2. **尽可能使用已配置的筛选条件（如 `views`）**
3. **从简单筛选开始，根据需要逐步增加复杂性**
4. **检查响应头部中的速率限制信息（`X-RateLimit-*`）**
5. **对于大量结果，使用分页和游标进行获取**
6. **日期必须使用 ISO 8601 格式（例如：2024-01-15T00:00:00Z）**
7. **在按关键词筛选之前，先从 `/keywords` 端点获取关键词 ID**
8. **使用 `!` 来排除不需要的内容**
9. **将 `includeAll=false` 与相关性筛选结合使用，以获得更准确的结果**

## 常见用例

### 查找 Twitter 上的正面提及内容且关注者数量较多的帖子
```json
{
  "limit": 20,
  "filters": {
    "source": ["twitter"],
    "sentiment": ["positive"],
    "minXFollowers": 1000
  }
}
```

### 排除垃圾信息，并获取 Reddit 和 GitHub 上的提及内容
```json
{
  "limit": 50,
  "filters": {
    "source": ["reddit", "github"],
    "!tag": ["spam", "irrelevant"]
  }
}
```

### 复杂查询：（Twitter 或 LinkedIn）且情感为正面，时间范围为过去 7 天
```json
{
  "limit": 30,
  "filters": {
    "operator": "AND",
    "groups": [
      {
        "operator": "OR",
        "conditions": [
          { "source": ["twitter"] },
          { "source": ["linkedin"] }
        ]
      },
      {
        "operator": "AND",
        "conditions": [
          { "sentiment": ["positive"] },
          { "startDate": "2024-01-20T00:00:00Z" }
        ]
      }
    ]
  }
}
```

## 错误处理

| 状态码 | 错误信息 | 描述 |
|--------|-------|-------------|
| 401 | 未经授权 | 缺少或无效的 API 密钥 |
| 403 | 被禁止 | 密钥有效，但没有权限 |
| 404 | 未找到 | 资源（例如查看记录 ID）未找到 |
| 429 | 超过速率限制 | 请求次数过多 |
| 400 | 请求格式错误 | 请求体格式不正确 |
| 500 | 内部错误 | 服务器错误，请稍后重试 |

## 逐步工作流程

当用户请求查询 Octolens 数据时：

1. **如果尚未提供 API 密钥，请先请求获取**
2. **了解用户的需求**：他们想要查找什么？
3. **确定所需的筛选条件**：来源、情感、日期范围等
4. **检查是否有合适的查看记录**：如果用户使用了预配置的筛选条件，先列出相关记录
5. **构建查询**：先使用简单模式，对于复杂逻辑再使用高级模式
6. **执行请求**：使用捆绑的 Node.js 脚本或直接调用 API
7. **解析结果**：提取关键信息（作者、内容、情感、来源）
8. **处理分页**：如果需要更多结果，使用响应中的游标
9. **展示结果**：总结分析结果，突出显示关键信息

## 示例

### 示例 1：简单查询
**用户**：“显示过去 7 天内来自 Twitter 的正面提及内容”

**操作**（使用捆绑脚本）：
```bash
node scripts/query-mentions.js YOUR_API_KEY '{"source": ["twitter"], "sentiment": ["positive"], "startDate": "2024-01-20T00:00:00Z"}'
```

**另一种方式**（直接使用 fetch API）：
```javascript
const response = await fetch('https://app.octolens.com/api/v1/mentions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    limit: 20,
    filters: {
      source: ['twitter'],
      sentiment: ['positive'],
      startDate: '2024-01-20T00:00:00Z',
    },
  }),
});
const data = await response.json();
```

### 示例 2：高级查询
**用户**：“查找来自 Reddit 或 GitHub 的提及内容，排除带有 spam 标签的帖子，情感为正面或中性”

**操作**（使用捆绑脚本）：
```bash
node scripts/query-mentions.js YOUR_API_KEY '{"operator": "AND", "groups": [{"operator": "OR", "conditions": [{"source": ["reddit"]}, {"source": ["github"]}]}, {"operator": "OR", "conditions": [{"sentiment": ["positive"]}, {"sentiment": ["neutral"]}]}, {"operator": "AND", "conditions": [{"!tag": ["spam"]}]}]}'
```

**另一种方式**（直接使用 fetch API）：
```javascript
const response = await fetch('https://app.octolens.com/api/v1/mentions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    limit: 30,
    filters: {
      operator: 'AND',
      groups: [
        {
          operator: 'OR',
          conditions: [
            { source: ['reddit'] },
            { source: ['github'] },
          ],
        },
        {
          operator: 'OR',
          conditions: [
            { sentiment: ['positive'] },
            { sentiment: ['neutral'] },
          ],
        },
        {
          operator: 'AND',
          conditions: [
            { '!tag': ['spam'] },
          ],
        },
      ],
    },
  }),
});
const data = await response.json();
```

### 示例 3：先获取关键词
**用户**：“显示与我们主要产品相关的关键词的提及内容”

**操作步骤**：
1. 首先列出所有关键词：
```bash
node scripts/list-keywords.js YOUR_API_KEY
```

2. 然后使用关键词 ID 查询提及内容：
```bash
node scripts/query-mentions.js YOUR_API_KEY '{"keyword": [1]}'
```

## 代理人员的建议

- **使用捆绑脚本**：Node.js 脚本会自动处理 JSON 解析
- **缓存关键词**：首次获取关键词后，将其保存在会话中
- **解释筛选逻辑**：在使用复杂筛选条件时，向用户解释其逻辑
- **提供示例**：当用户不确定如何使用筛选条件时，展示示例结构
- **合理使用分页**：在请求下一页之前，先询问用户是否需要更多结果
- **提供分析**：不要只是简单地展示数据，还要提供分析结果（如情感趋势、主要作者、平台分布等）
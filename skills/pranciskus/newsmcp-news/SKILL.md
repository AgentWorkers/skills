---
name: newsmcp
description: 实时世界新闻简报，包含人工智能聚合的事件、主题分类和地理过滤功能。无需使用API密钥。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📰"
    homepage: https://newsmcp.io
---
# 世界新闻技能

该技能可实时获取来自人工智能驱动的新闻聚合服务的全球新闻。新闻内容会被聚类成**事件**（这些事件会从多个来源中去重），然后进行总结、按主题分类，并标注地理位置。

**无需API密钥，也无需身份验证，只需调用API即可。**

## 该技能的独特之处

- **事件而非文章**：单个文章会被整合成一条新闻，因此用户看到的每条新闻都只包含一次摘要，而不会出现重复内容。
- **预先总结**：每个事件都会由AI生成摘要，用户无需阅读完整文章。
- **分类清晰**：新闻分为12个主题类别和100多个地理区域。
- **重要度指标**：提供`sources_count`（报道该事件的媒体数量）和`impact_score`（AI评估的重要性）。
- **多源信息**：每个事件都会列出所有相关媒体的文章，包括标题、URL和域名。

## API基础URL

```
https://newsmcp.io/v1
```

## API端点

### 1. 获取新闻事件

```bash
curl -s "https://newsmcp.io/v1/news/?hours=24&per_page=10&order_by=-sources_count"
```

**参数：**
| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `hours` | int | 24 | 时间范围（1-168小时，即最多7天） |
| `topics` | string | — | 用逗号分隔的主题标签（例如 `politics,military`） |
| `geo` | string | — | 用逗号分隔的地理标签（例如 `europe,united-states`） |
| `page` | int | 1 | 页码 |
| `per_page` | int | 20 | 每页显示的结果数量（最多50条） |
| `order_by` | string | `-sources_count` | 排序方式。可选值：`sources_count`, `entries_count`, `impact_score`, `first_seen_at`, `last_seen_at`（以 `-` 开头表示降序排序） |

**响应格式：**
```json
{
  "events": [
    {
      "id": "uuid",
      "summary": "AI-generated event summary",
      "topics": ["politics", "military"],
      "geo": ["europe", "ukraine"],
      "entries_count": 15,
      "sources_count": 8,
      "first_seen_at": "2026-03-03T10:00:00Z",
      "last_seen_at": "2026-03-03T14:00:00Z",
      "impact_score": 4,
      "entries": [
        {
          "title": "Article headline",
          "url": "https://example.com/article",
          "domain": "example.com",
          "published_at": "2026-03-03T12:00:00Z"
        }
      ]
    }
  ],
  "total": 42,
  "page": 1,
  "per_page": 10
}
```

### 2. 获取事件详情

```bash
curl -s "https://newsmcp.io/v1/news/{event_id}/"
```

返回与列表相同的字段，此外还包括`context`——即事件的详细背景和分析信息。

### 3. 列出可用主题

```bash
curl -s "https://newsmcp.io/v1/news/topics/"
```

返回的主题包括：`politics`（政治）、`economy`（经济）、`technology`（科技）、`science`（科学）、`health`（健康）、`environment`（环境）、`sports`（体育）、`culture`（文化）、`crime`（犯罪）、`military`（军事）、`education`（教育）、`society`（社会）。

### 4. 列出可用地区

```bash
curl -s "https://newsmcp.io/v1/news/regions/"
```

返回的地区包括各大洲（`europe`、`asia`、`africa`、`north-america`、`south-america`、`oceania`）以及具体国家（例如 `united-states`、`ukraine`、`china`、`lithuania` 等）。每个地区都有一个`type`字段，值为 `"continent"` 或 `"country"`。

## 使用方法

当用户请求新闻、头条或当前事件时：

1. **默认简报**：获取过去24小时内按重要性排序的热门事件：
   ```bash
   curl -s "https://newsmcp.io/v1/news/?hours=24&per_page=10&order_by=-sources_count"
   ```

2. **特定主题**：如果用户询问某个特定主题（例如“科技新闻”或“体育新闻”），可以使用`topics`参数：
   ```bash
   curl -s "https://newsmcp.io/v1/news/?topics=technology&hours=24"
   ```

3. **特定地区**：如果用户询问某个地区（例如“欧洲新闻”或“亚洲正在发生什么”），可以使用`geo`参数：
   ```bash
   curl -s "https://newsmcp.io/v1/news/?geo=europe&hours=24"
   ```

4. **组合过滤**：可以同时使用`topics`和`geo`参数进行过滤：
   ```bash
   curl -s "https://newsmcp.io/v1/news/?topics=politics,military&geo=europe&hours=48"
   ```

5. **深入查看**：如需了解某个事件的详细信息，可以获取该事件的详细内容：
   ```bash
   curl -s "https://newsmcp.io/v1/news/{event_id}/"
   ```

## 简报的展示方式

结果将以简洁的新闻简报形式呈现：
- 首先展示最重要的事件（`sources_count`或`impact_score`最高）。
- 对于每个事件，显示其摘要以及报道该事件的媒体数量。
- 为每个事件提供1-2个媒体链接，方便用户进一步阅读。
- 如果用户要求全面了解情况，可以按主题或地区进行分组展示。
- 显示时间范围以及找到的事件数量。
- 如果提供了`topics`或`geo`参数，会使用这些参数添加相应的标签以提供更多背景信息。

## 主题标签参考

`politics`（政治）、`economy`（经济）、`technology`（科技）、`science`（科学）、`health`（健康）、`environment`（环境）、`sports`（体育）、`culture`（文化）、`crime`（犯罪）、`military`（军事）、`education`（教育）、`society`（社会）

## 示例交互

**用户：**“今天世界上发生了什么？”

**操作：** 获取 `https://newsmcp.io/v1/news/?hours=24&per_page=10&order_by=-sources_count`

**用户：**“给我最新的乌克兰新闻”

**操作：** 获取 `https://newsmcp.io/v1/news/?geo=ukraine&hours=48&order_by=-last_seen_at`

**用户：**“这周有什么科技新闻吗？**

**操作：** 获取 `https://newsmcp.io/v1/news/?topics=technology&hours=168&order_by=-sources_count`
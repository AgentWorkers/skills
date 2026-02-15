---
name: brave-images
description: 使用 Brave Search API 搜索图片。当您需要查找任何主题的图片、照片或视觉内容时，可以使用该 API。需要设置 `BRAVE_API_KEY` 环境变量。
---

# Brave 图片搜索

通过 Brave Search API 搜索图片。

## 使用方法

```bash
curl -s "https://api.search.brave.com/res/v1/images/search?q=QUERY&count=COUNT" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

## 参数

| 参数 | 是否必填 | 描述 |
|-------|----------|-------------|
| `q` | 是 | 搜索查询（需进行 URL 编码） |
| `count` | 否 | 结果数量（1-100，默认为 20） |
| `country` | 否 | 用于指定搜索区域的两位字母代码（如 US、DE、IL） |
| `search_lang` | 否 | 语言代码（en、de、he） |
| `safesearch` | 否 | 安全搜索级别：off、moderate、strict（默认为 moderate） |

## 响应解析

每个搜索结果包含以下关键字段：
- `results[].title` — 图片标题 |
- `results[].properties.url` — 图片的完整 URL |
- `results[].thumbnail.src` — 图片的缩略图 URL |
- `results[].source` — 图片的来源网站 |
- `results[].properties.width/height` — 图片的尺寸 |

## 示例

在以色列搜索“sunset beach”相关的图片：
```bash
curl -s "https://api.search.brave.com/res/v1/images/search?q=sunset%20beach&count=5&country=IL" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

然后从 JSON 响应中提取以下信息：
- 缩略图：`.results[0].thumbnail.src`
- 完整图片：`.results[0].properties.url`

## 显示结果

在展示图片搜索结果时，请注意：
1. 直接将图片发送给用户（而不仅仅是列出图片的 URL）；
2. 使用 `results[].properties.url` 获取完整图片，或使用 `results[].thumbnail.src` 获取缩略图；
3. 将图片标题作为图片的说明文字；
4. 如果实际找到的结果数量超过显示的数量，请告知用户（例如：“找到了 20 张图片，当前显示 3 张——需要查看更多吗？”）

示例流程：
```
User: "find me pictures of sunsets"
→ Search with count=10
→ Send 3-5 images with captions
→ "Found 10 sunset images, showing 5. Want to see more?"
```

## 注意事项：
- 必须对查询字符串进行 URL 编码（空格需替换为 `%20`）；
- API 密钥从环境变量 `$BRAVE_API_KEY` 中获取；
- 请遵守订阅等级对应的请求速率限制。
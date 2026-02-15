---
name: x-trends
description: 在 X（Twitter）上搜索和分析热门话题。当你需要查找当前的热门趋势、探索话题标签（hashtags）、按地理位置获取热门话题，或分析 X 上当前流行的内容时，可以使用此功能。
metadata: {"openclaw":{"requires":{"bins":["twurl"]},"install":[{"id":"ruby","kind":"gem","package":"twurl","bins":["twurl"],"label":"Install twurl CLI (gem)"}]}}
---

# X（Twitter）趋势命令行工具（X-Trends CLI）

**GitHub地址：** https://github.com/aycvs2/x-trends

## 安装

首先安装官方的Twitter命令行工具 `twurl`：
```bash
gem install twurl
```

然后使用您的X/Twitter账号进行授权：
```bash
twurl authorize --consumer-key YOUR_API_KEY --consumer-secret YOUR_API_SECRET
```

## 获取热门话题

- 全球热门话题：
```bash
twurl "/1.1/trends/place.json?id=1" | jq '.[0].trends[:10]'
```

- 按地理位置获取热门话题（使用WOEID）：
```bash
# USA (WOEID: 23424977)
twurl "/1.1/trends/place.json?id=23424977" | jq '.[0].trends[:10]'

# Russia (WOEID: 23424936)
twurl "/1.1/trends/place.json?id=23424936" | jq '.[0].trends[:10]'

# UK (WOEID: 23424975)
twurl "/1.1/trends/place.json?id=23424975" | jq '.[0].trends[:10]'
```

## 可用的地理位置

- 查看所有可用的地理位置：
```bash
twurl "/1.1/trends/available.json" | jq '.[] | {name, woeid}'
```

- 根据坐标查找最近的地理位置：
```bash
twurl "/1.1/trends/closest.json?lat=55.7558&long=37.6173" | jq '.'
```

## 按热门话题搜索推文

- 搜索与特定热门话题相关的最新推文：
```bash
twurl "/2/tweets/search/recent?query=%23YourHashtag&max_results=10" | jq '.data'
```

- 使用过滤器进行搜索：
```bash
# Only tweets with media
twurl "/2/tweets/search/recent?query=%23trend%20has:media&max_results=10" | jq '.data'

# Only verified accounts
twurl "/2/tweets/search/recent?query=%23trend%20is:verified&max_results=10" | jq '.data'
```

## 常见WOEID代码

| 地点 | WOEID |
|------|------|
| 全球 | 1       |
| 美国 | 23424977   |
| 俄罗斯 | 23424936   |
| 英国 | 23424975   |
| 德国 | 23424829   |
| 法国 | 23424819   |
| 日本 | 23424856   |
| 巴西 | 23424768   |
| 印度 | 23424848   |
| 加拿大 | 23424775   |

## 输出格式

趋势查询的结果包含以下信息：
- `name`：热门话题的名称/标签
- `url`：搜索结果的链接
- `tweet_volume`：相关推文的数量（如有）
- `promoted_content`：该话题是否被推广

## 注意事项

- 请注意API的使用限制：每15分钟内只能发送75次请求。
- 部分热门话题可能没有推文数量数据。
- 使用 `jq` 工具进行JSON数据的解析和过滤。
- 热门话题信息大约每5分钟更新一次。
- 本工具使用Twitter的API v1.1来获取趋势数据，使用API v2来执行搜索操作。
---
name: brightdata
description: 通过 Bright Data API 进行网页抓取和搜索。需要使用 `BRIGHTDATA_API_KEY` 和 `BRIGHTDATA_UNLOCKER_ZONE`。该 API 可用于将任意网页内容抓取为 Markdown 格式（从而绕过机器人检测和 CAPTCHA 验证），或用于在 Google 上进行结构化搜索并获取搜索结果。
---

# Bright Data - 网页抓取与搜索

可以直接通过 API 访问 Bright Data 的 Web Unlocker 和 SERP API。

## 设置

**1. 获取 API 密钥：**
从 [Bright Data 仪表板](https://brightdata.com/cp) 获取 API 密钥。

**2. 创建 Web Unlocker 区域：**
在 brightdata.com/cp 网站上，点击右上角的 “Add”（添加），然后选择 “Unlocker zone”（解锁器区域）来创建一个新的区域。

**3. 设置环境变量：**
```bash
export BRIGHTDATA_API_KEY="your-api-key"
export BRIGHTDATA_UNLOCKER_ZONE="your-zone-name"
```

## 使用方法

### 谷歌搜索
在谷歌上进行搜索，并获取结构化的 JSON 结果（包含标题、链接和描述）。
```bash
bash scripts/search.sh "query" [cursor]
```
- `cursor`：可选的页码（从 0 开始计数，默认值为 0）

### 网页抓取
可以将任何网页内容以 Markdown 格式抓取下来。该功能可以绕过机器人检测和验证码。
```bash
bash scripts/scrape.sh "url"
```

## 输出格式

### 搜索结果
返回包含结构化数据的 JSON 对象（其中包含 “organic” 字段）：
```json
{
  "organic": [
    {"link": "...", "title": "...", "description": "..."}
  ]
}
```

### 抓取结果
从网页中提取干净的 Markdown 内容。
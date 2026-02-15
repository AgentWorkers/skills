---
name: "multi-search-engine"
description: "多搜索引擎集成，支持17个搜索引擎（8个中国境内搜索引擎 + 9个全球搜索引擎）。提供高级搜索操作符、时间过滤功能、站点搜索选项以及WolframAlpha知识查询服务。无需使用API密钥。"
---

# 多搜索引擎 v2.0.1

本版本集成了17个搜索引擎，支持无需API密钥即可进行网页爬取的功能。

## 支持的搜索引擎

### 国内搜索引擎（8个）
- **百度**: `https://www.baidu.com/s?wd={keyword}`
- **必应中文**: `https://cn.bing.com/search?q={keyword}&ensearch=0`
- **必应国际**: `https://cn.bing.com/search?q={keyword}&ensearch=1`
- **360**: `https://www.so.com/s?q={keyword}`
- **搜狗**: `https://sogou.com/web?query={keyword}`
- **微信**: `https://wx.sogou.com/weixin?type=2&query={keyword}`
- **抖音**: `https://so.toutiao.com/search?keyword={keyword}`
- **知乎**: `https://www.jisilu.cn/explore/?keyword={keyword}`

### 国际搜索引擎（9个）
- **谷歌**: `https://www.google.com/search?q={keyword}`
- **谷歌香港**: `https://www.google.com.hk/search?q={keyword}`
- **DuckDuckGo**: `https://duckduckgo.com/html/?q={keyword}`
- **雅虎**: `https://search.yahoo.com/search?p={keyword}`
- **Startpage**: `https://www.startpage.com/sp/search?query={keyword}`
- **Brave**: `https://search.brave.com/search?q={keyword}`
- **Ecosia**: `https://www.ecosia.org/search?q={keyword}`
- **Qwant**: `https://www.qwant.com/?q={keyword}`
- **WolframAlpha**: `https://www.wolframalpha.com/input?i={keyword}`

## 快速使用示例

```javascript
// Basic search
web_fetch({"url": "https://www.google.com/search?q=python+tutorial"})

// Site-specific
web_fetch({"url": "https://www.google.com/search?q=site:github.com+react"})

// File type
web_fetch({"url": "https://www.google.com/search?q=machine+learning+filetype:pdf"})

// Time filter (past week)
web_fetch({"url": "https://www.google.com/search?q=ai+news&tbs=qdr:w"})

// Privacy search
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy+tools"})

// DuckDuckGo Bangs
web_fetch({"url": "https://duckduckgo.com/html/?q=!gh+tensorflow"})

// Knowledge calculation
web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY"})
```

## 高级搜索操作符

| 操作符 | 例子 | 说明 |
|----------|---------|-------------|
| `site:` | `site:github.com python` | 在指定网站内搜索 |
| `filetype:` | `filetype:pdf report` | 指定文件类型 |
| `""` | `"machine learning"` | 精确匹配 |
| `-` | `python -snake` | 排除指定词汇 |
| `OR` | `cat OR dog` | 任意一个词汇 |

## 时间筛选

| 参数 | 说明 |
|-----------|-------------|
| `tbs=qdr:h` | 过去1小时 |
| `tbs=qdr:d` | 过去1天 |
| `tbs=qdr:w` | 过去1周 |
| `tbs=qdr:m` | 过去1个月 |
| `tbs=qdr:y` | 过去1年 |

## 隐私保护功能

- **DuckDuckGo**: 不会进行用户数据追踪 |
- **Startpage**: 结果基于谷歌搜索，同时提供隐私保护 |
- **Brave**: 使用独立的搜索引擎索引 |
- **Qwant**: 遵守欧盟GDPR数据保护法规

## DuckDuckGo的快捷键

| 快捷键 | 目标网站 |
|------|-------------|
| `!g` | 谷歌 |
| `!gh` | GitHub |
| `!so` | Stack Overflow |
| `!w` | 维基百科 |
| `!yt` | YouTube |

## WolframAlpha的查询示例

- 数学计算: `integrate x^2 dx`
- 货币转换: `100 USD to CNY`
- 股票查询: `AAPL stock`
- 天气查询: `weather in Beijing`

## 文档资料

- `references/advanced-search.md` - 国内搜索使用指南
- `references/international-search.md` - 国际搜索使用指南
- `CHANGELOG.md` - 版本更新记录

## 许可证

MIT许可证
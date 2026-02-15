---
name: baidu-scholar-search-skill
description: 百度学术搜索 - 可搜索中文和英文的学术文献（期刊、会议论文等）
homepage: https://xueshu.baidu.com/
metadata: { "openclaw": { "emoji": "🔬", "requires": { "bins": ["curl"] ,"env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" }  }
---

# Baidu Scholar 搜索功能

## 功能
支持通过关键词搜索中文和英文的学术文献，包括期刊论文、会议论文、学位论文等。

## LLM 使用指南

### 基本用法
```bash
bash baidu_scholar_search.sh "keyword"
bash baidu_scholar_search.sh "keyword" page_number
bash baidu_scholar_search.sh "keyword" page_number include_abstract
```

### 参数说明
| 参数 | 是否必填 | 默认值 | 说明 |
|-----------|----------|---------|-------------|
| keyword | ✅ | - | 搜索词，例如 "机器学习" 或 "癌症免疫疗法" |
| page_number | ❌ | 0 | 从第0页开始，0表示第1页 |
| include_abstract | ❌ | false | true：返回详细摘要；false：仅返回标题和基本信息 |

### 默认行为
- **不返回摘要**：响应速度快，适合快速浏览文献列表
- 从第1页开始显示结果

### 何时返回摘要
- 用户明确请求 "abstract"、"include abstract" 或 "detailed content"
- 用户表示 "需要理解论文内容" 或 "请给出详细解释"

### 何时不返回摘要
- 用户仅输入 "search"、"retrieve" 或 "check"
- 用户表示 "查看有哪些资源" 或 "帮我查找"
- 未明确请求摘要信息

## API 规范

### 端点
`GET https://qianfan.baidubce.com/v2/tools/baidu_scholar/search`

### 请求参数
- `wd` - 搜索关键词（必填）
- `pageNum` - 页码（可选，默认为0）
- `enable_abstract` - 是否返回摘要（可选，默认为false）

### 响应字段
- `title` - 论文标题
- `abstract` - 摘要（仅在 `enable_abstract` 为 true 时返回）
- `keyword` - 搜索词
- `paperId` - 论文ID
- `publishYear` - 发表年份
- `url` - Baidu Scholar 的链接

## 示例

### 快速搜索（不返回摘要）
```bash
bash baidu_scholar_search.sh "cancer immunotherapy"
# Returns title, year, keywords and other basic information
```

### 详细搜索（包含摘要）
```bash
bash baidu_scholar_search.sh "cancer immunotherapy" 0 true
# Returns detailed information including abstract
```

### 分页搜索
```bash
bash baidu_scholar_search.sh "machine learning" 1
# Search page 2 (no abstract)
```

## 注意事项
- 需要设置 `BAIDU_API_KEY` 环境变量
- 关键词必须用引号括起来
- 返回摘要会显著增加响应时间
- 支持中文和英文关键词
---
name: baidu-scholar-search
description: 百度学术搜索工具支持检索中文和英文的文献，涵盖多种类型的文献资源，包括学术期刊、会议论文和学位论文等。
homepage: https://xueshu.baidu.com/
metadata: { "openclaw": { "emoji": "🔬", "requires": { "bins": ["curl"] } } }
---

# Baidu Scholar 搜索

根据用户输入的关键词，搜索中文和英文文献，涵盖学术期刊、会议论文和学位论文等多种类型的文献。

## 设置

1. **API 密钥：** 确保 `BAIDU_API_KEY` 环境变量已设置为您的有效 API 密钥。
2. **运行时环境：** API 密钥必须在运行时环境中可用。

## API 表格
|     名称    |               路径              |            描述                                      |
|-------------|---------------------------------|---------------------------------------|
|scholar_search|/v2/tools/baidu_scholar/search|根据用户输入的关键词，搜索中文和英文文献            |

## 工作流程

1. 脚本向 Baidu Scholar 搜索 API 发送 GET 请求。
2. API 返回结构化的搜索结果，包含文献的摘要、关键词、paperId、标题等信息。

## Scholar 搜索 API

### 参数

- `wd`：搜索关键词（必填，例如 'machine learning'）
- `pageNum`：页码（默认值：0）
- `enable_abstract`：是否显示摘要（默认值：false）；如果设置为 true，则返回文献的摘要

### 使用示例
```bash
curl -XGET 'https://qianfan.baidubce.com/v2/tools/baidu_scholar/search?wd=人工智能&enable_abstract=true' \
-H 'Authorization: Bearer API_KEY'
```

## 执行脚本
```bash
#!/bin/bash

# Baidu Scholar Search Skill Implementation

set -e

# Check if required environment variable is set
if [ -z "$BAIDU_API_KEY" ]; then
    echo '{"error": "BAIDU_API_KEY environment variable not set"}'
    exit 1
fi

WD="$1"
if [ -z "$wd" ]; then
    echo '{"error": "Missing wd parameter"}'
    exit 1
fi
pageNum="$2"
if [ -z "$pageNum" ]; then
    pageNum=0
fi
enable_abstract="$3"
if [ -z "$pageNum" ]; then
    enable_abstract=false
fi
curl -XGET "https://qianfan.baidubce.com/v2/tools/baidu_scholar/search?wd=$WD&pageNum=$pageNum&enable_abstract=$enable_abstract" -H "Authorization: Bearer $BAIDU_API_KEY" 
```
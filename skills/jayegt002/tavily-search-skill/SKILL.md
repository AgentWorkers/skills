---
name: tavily-search-skill
description: Tavily API支持与实时配额管理功能集成，并提供付费模式切换选项。适用于需要使用Web搜索的场景。
version: 1.0.4
author: JayeGT002
triggers:
  - tavily
  - search
  - web search
---
# Tavily 搜索技能 🔍

这是一个使用 Tavily API 进行高质量网络搜索的 OpenClaw 技能。

## 主要功能

- **智能搜索**：通过结构化数据调用 Tavily API，获得搜索结果。
- **实时配额管理**：每次搜索后自动更新配额使用情况。
- **免费/付费配额区分**：分别显示免费和付费配额的使用情况。
- **付费模式切换**：在免费和付费配额之间切换使用优先级。
- **全面的错误处理**：能够处理网络故障、配额不足等异常情况。

## 使用方法

### 先决条件 ⚠️

**需要配置环境变量：**
```bash
export TAVILY_API_KEY="your_api_key"
```

获取 API 密钥：https://app.tavily.com/api-keys

> ⚠️ 注意：此技能要求用户提供自己的 Tavily API 密钥。

### 基本搜索
```bash
./search.sh "search query"
```

### 指定搜索结果数量
```bash
./search.sh "query" 10
```

### 包含图片
```bash
./search.sh "query" 5 true
```

### 查看配额使用情况
```bash
./search.sh --usage
```

### 切换付费模式
```bash
./search.sh --toggle-paid-mode
```

### 查看状态
```bash
./search.sh --status
```

## 输出格式

搜索结果以 JSON 格式返回：
```json
{
  "query": "keyword",
  "results": [
    {
      "title": "Result Title",
      "url": "link",
      "content": "summary"
    }
  ],
  "quota_info": {
    "plan": "free",
    "total": 1000,
    "used": 15,
    "remaining": 985
  }
}
```

## 所需依赖库

- `curl`：用于发送 HTTP 请求。
- `jq`：用于处理 JSON 数据。

### 安装依赖库

**Ubuntu/Debian：**
```bash
sudo apt-get install curl jq
```

**macOS：**
```bash
brew install curl jq
```

## 使用限制

- 免费计划：每月 1000 次请求。
- 每次搜索最多返回 20 个结果。
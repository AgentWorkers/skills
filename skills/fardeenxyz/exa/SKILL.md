---
name: exa
description: 通过 Exa AI API 实现神经网络驱动的网页搜索及代码上下文分析功能。需要使用 EXA_API_KEY 这个密钥。该 API 可用于查找文档、代码示例、研究论文或公司信息。
metadata: {"clawdbot":{"emoji":"🧠","requires":{"env":["EXA_API_KEY"]}}}
---

# Exa - 神经网络搜索引擎

提供对 Exa 神经网络搜索引擎的直接 API 访问。

## 设置

**1. 获取 API 密钥：**
从 [Exa 仪表板](https://dashboard.exa.ai/api-keys) 获取 API 密钥。

**2. 在环境中配置 API 密钥：**
```bash
export EXA_API_KEY="your-key-here"
```

## 使用方法

### 网页搜索
```bash
bash scripts/search.sh "query" [num_results] [type]
```
* `type`: auto (默认值), neural, fast, deep
* `category`: company, research-paper, news, github, tweet, personal-site, pdf

### 代码示例
用于查找相关的代码片段和文档。
```bash
bash scripts/code.sh "query" [num_results]
```

### 提取内容
从 URL 中提取完整文本。
```bash
bash scripts/content.sh "url1" "url2"
```
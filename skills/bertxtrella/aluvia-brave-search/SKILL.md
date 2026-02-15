---
name: aluvia-brave-search
description: 通过Brave Search API进行网络搜索和内容提取，利用Aluvia移动代理实现无限制的访问。适用于搜索文档、事实或任何网页内容。无需使用浏览器；可绕过网络限制和验证码。
---

# Aluvia Brave Search

这是一个基于Brave Search的无头网页搜索工具，支持通过Aluvia移动代理进行内容提取。无需使用浏览器，能够绕过网络限制和验证码。

## 设置

首次使用前请运行以下命令：

```bash
cd ~/Projects/agent-scripts/skills/aluvia-brave-search
npm ci
```

## 设置您的API密钥（所有功能均需设置）：

export ALUVIA_API_KEY=your_aluvia_key
export BRAVE_API_KEY=your_brave_key

## 可选：重用现有的Aluvia连接

export ALUVIA_CONNECTION_ID=your_connection_id

`ALUVIA_API_KEY`和`BRAVE_API_KEY`都是必需的。如果设置了`ALUVIA_CONNECTION_ID`，则可以重用现有的Aluvia连接来代理请求。

## 搜索

```bash
./search.js "query"                    # Basic search (5 results)
./search.js "query" -n 10              # More results
./search.js "query" --content          # Include page content as markdown
./search.js "query" -n 3 --content     # Combined
```

## 提取页面内容

```bash
./content.js https://example.com/article
```

该功能可以获取指定URL的页面内容，并将其以Markdown格式提取出来。

## 输出格式

```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results
Content: (if --content flag used)
  Markdown content extracted from the page...

--- Result 2 ---
...
```

## 适用场景

- 搜索文档或API参考资料
- 查找事实或实时信息
- 从特定URL获取内容
- 所有不需要交互式浏览的网页搜索任务
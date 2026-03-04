---
name: tavily-search
description: "使用 Tavily API 进行安全的网页搜索和提取 URL 内容。适用场景：快速进行网页搜索、收集来源信息、从特定 URL 中提取文本并进行摘要处理。"
---
# Tavily 搜索（安全版）

使用 Tavily API 执行安全的搜索或数据提取操作。

## 要求

- 必须定义 `TAVILY_API_KEY` 环境变量。
- 请勿将 API 密钥写入文件、提交到代码仓库，或显示在输出结果中。

## 搜索功能

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 8 --deep
node {baseDir}/scripts/search.mjs "query" --topic news --days 3
```

## 提取 URL 内容

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
node {baseDir}/scripts/extract.mjs "https://a.com" "https://b.com"
```

## 安全规则

- 仅接受 `http` 或 `https` 协议的 URL。
- 拒绝使用 localhost、loopback、私有 IP 地址以及 `.local` 和 `.internal` 域名。
- 限制单次请求中的 URL 数量（遵循脚本的默认设置）。
- 在发生错误时，仅显示简短且清晰的错误信息；切勿泄露 API 密钥或敏感数据。
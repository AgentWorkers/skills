---
name: meyhem-capabilities
description: 在超过 20,000 台 MCP 服务器和 OpenClaw 工具中，为您的任务找到最适合的工具。排名依据是社区的信任度。无需使用 API 密钥。
version: 0.1.2
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---
# Meyhem 功能

Meyhem 可帮助您在 MCP 服务器和 OpenClaw 技能中找到最适合完成特定任务的工具。系统索引了 20,000 多种工具，这些工具会根据社区的信任度（GitHub 星标）和相关性进行排序。只需用简单的语言描述您的需求，Meyhem 就会为您推荐最合适的工具。

无需 API 密钥，无需注册，也没有使用限制。

## 为什么选择 Meyhem 功能？

- **20,000 多种工具可供选择**：涵盖 15,000 多种 OpenClaw 技能和 4,600 多个 MCP 服务器
- **自然语言搜索**：只需描述您的任务，系统会返回相关结果
- **基于信任度排序**：结合 GitHub 星标和内容相关性进行排序
- **按生态系统筛选**：可以搜索所有工具，也可以仅搜索 MCP 或 OpenClaw 相关的工具
- **完全无依赖**：仅使用 Python 标准库

## 快速入门

```bash
python3 capabilities.py "I need to query a Postgres database"
python3 capabilities.py "browser automation" -n 3
python3 capabilities.py "kubernetes monitoring" --ecosystem mcp
python3 capabilities.py "manage emails" --ecosystem openclaw
```

## REST API

```bash
curl -X POST https://api.rhdxm.com/find-capability \
  -H 'Content-Type: application/json' \
  -d '{"task": "kubernetes monitoring", "max_results": 5}'
```

**按生态系统筛选**：

```bash
curl -X POST https://api.rhdxm.com/find-capability?ecosystem=mcp \
  -H 'Content-Type: application/json' \
  -d '{"task": "kubernetes monitoring", "max_results": 5}'
```

完整 API 文档：https://api.rhdxm.com/docs

## MCP

通过 `https://api.rhdxm.com/mcp/` 使用 `find_capability` 工具进行连接

## 数据安全性

该工具会将您的搜索请求发送到 `api.rhdxm.com`。该工具本身不会访问本地文件、环境变量或凭据，但您在请求中包含的任何内容都会被传输。请避免发送敏感或专有信息。

源代码：https://github.com/c5huracan/meyhem
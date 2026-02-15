---
description: 监控网站的正常运行时间（uptime），测量响应时间（response times），并检查任意 URL 的 HTTP 状态码（HTTP status codes）。
---

# 运行时间监控器

用于检查网站的可用性和性能。

## 功能

- **运行时间检查**：验证网站是否正常运行（是否处于“上线”或“下线”状态）
- **响应时间**：测量DNS解析时间、连接时间、TLS传输时间以及总响应时间
- **状态码**：报告HTTP状态码及页面重定向情况
- **批量检查**：同时监控多个URL
- **历史记录**：记录多次检查的结果并生成汇总报告

## 使用方法

您可以要求代理执行以下操作：
- “example.com现在是否可以访问？”
- “测量mysite.org的响应时间”
- “检查这5个URL的状态”
- “每隔30秒监控api.example.com的状态，持续5分钟”

## 工作原理

该工具通过`curl`命令实现数据采集，并记录相应的执行时间：

```bash
curl -o /dev/null -s -w "HTTP %{http_code} | DNS: %{time_namelookup}s | Connect: %{time_connect}s | TLS: %{time_appconnect}s | Total: %{time_total}s\n" https://example.com
```

## 系统要求

- 需要安装`curl`（大多数系统均已预装）
- 无需使用API密钥
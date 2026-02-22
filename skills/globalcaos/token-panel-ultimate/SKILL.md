---
name: token-panel-ultimate
version: 2.1.1
description: "准确了解您的人工智能代币的去向。多提供商跟踪、预算警报以及REST API——所有这些功能都集成在一个仪表板中。"
metadata:
  openclaw:
    owner: kn7623hrcwt6rg73a67xw3wyx580asdw
    category: monitoring
    tags:
      - tokens
      - usage
      - budget
      - anthropic
      - openai
      - gemini
      - manus
      - dashboard
    license: MIT
    notes:
      security: "Runs a local REST API on localhost:8765 for usage tracking. SQLite database stored locally. Reads provider usage from local transcripts and official APIs using your existing credentials. No external data sharing, no cloud dependencies. Systemd service runs as your user, not root."
---
# Token Panel Ultimate

**一个用于管理您所使用所有代币的仪表板。** 无论是 Anthropic、Gemini、OpenAI 还是 Manus，都能在账单生成前对其进行追踪、存储和查询。

## 为什么需要这个工具？

您可能已经查看了 Anthropic 的控制台，也浏览了 OpenAI 的仪表板，甚至打开了 Gemini 的页面，但仍然不清楚上周二花费的 14 美元去了哪里。Token Panel Ultimate 将这四个服务提供商的所有信息整合在一个平台上，让您只需一次查询就能找到答案。

## 它的功能包括：

- **多服务提供商追踪**：将 Anthropic、Gemini、OpenAI 和 Manus 的使用数据存储在同一个 SQLite 数据库中。
- **预算提醒**：为每个服务提供商设置每月的预算限制，确保在超出预算前收到警告。
- **REST API**：通过端口 8765 提供程序化查询接口，您可以将其集成到自己的脚本或仪表板中。
- **会话记录解析**：自动从 OpenClaw 的会话记录中提取代币使用情况。
- **完全无依赖**：仅使用 SQLite 进行数据存储，无需 Postgres、Redis 或云服务。
- **以守护进程形式运行**：通过 Systemd 服务在后台持续运行。

## 快速入门

```bash
pip install -r requirements.txt
python3 api.py
```

## 架构

```
OpenClaw Plugin → Budget Collector API → SQLite DB
                        ↓
                Transcripts / Anthropic API / Manus Tracker
```

## API 端点

| 方法      | 路径               | 描述                          |
|---------|-------------------|------------------------------|
| GET      | /usage            | 所有服务提供商的使用情况                |
| GET      | /usage/:provider     | 单个服务提供商的使用情况                |
| GET      | /budget           | 当前的预算限制                    |
| POST     | /budget           | 设置或更新预算限制                    |

*克隆该项目，根据需要进行修改，然后让它成为属于您的工具。*

👉 访问完整项目：[github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)
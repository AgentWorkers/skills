---
name: virlo
description: Virlo 社交媒体智能工具：支持病毒式视频分析、标签排名、趋势汇总，以及跨 YouTube、TikTok 和 Instagram 的社交监听功能。可用于内容策略制定、趋势发现、竞争分析及细分市场监测。
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "☄️",
        "requires": { "bins": ["curl"], "env": ["VIRLO_API_KEY"] },
        "primaryEnv": "VIRLO_API_KEY",
      },
  }
---
# Virlo

专为短视频内容提供社交媒体情报分析的工具——相当于博尔伯格新闻（Bloomberg）在病毒式内容（viral content）领域的解决方案。

## 配置

请设置 `VIRLO_API_KEY` 环境变量。您的 API 密钥格式为 `virlo_tkn_<your_key>`，可以从 [Virlo 仪表板](https://dev.virlo.ai/dashboard) 获取。

## 功能概述

Virlo API 提供跨 YouTube、TikTok 和 Instagram 的分析服务。主要功能包括：

- **标签（Hashtags）**：超过 50 万个标签，按使用次数和总观看次数排名
- **趋势（Trends）**：每日精选的热门话题，更新时间为 UTC 时间 1 点
- **视频（Videos）**：超过 200 万个病毒式视频的性能数据（观看次数、点赞数、分享次数、评论数）
- **Orbit**：基于关键词的社交内容监控服务，支持异步分析
- **Comet**：自动化的细分领域内容监控工具，支持定时抓取

所有 API 端点均使用 `/v1` 前缀，并采用 `snake_case` 命名规则；返回的数据格式为 `{"data": ... }`。

## API 访问方式

```bash
# GET request
{baseDir}/scripts/virlo-api.sh GET <endpoint>

# POST request with JSON body
{baseDir}/scripts/virlo-api.sh POST <endpoint> '<json-body>'
```

示例：
- `{baseDir}/scripts/virlo-api.sh GET /v1/hashtags` — 列出热门标签
- `{baseDir}/scripts/virlo-api.sh GET "/v1/videos?limit=10"` — 获取热门病毒式视频列表
- `{baseDir}/scripts/virlo-api.sh GET /v1/trends` — 查看每日趋势摘要
- `{baseDir}/scripts/virlo-api.sh POST /v1/orbit '{"name":"AI research","keywords":["artificial intelligence","AI tools"]}'` — 发送搜索请求

## 本地 API 参考文档

请先阅读 `{baseDir}/references/api-overview.md`，了解认证、分页和常用操作模式。然后根据需要加载相应的领域文档：

| 领域          | 文件                            | 所涵盖的内容                                                                                              |
| --------------- | ------------------------------- | --------------------------------------------------------------------------------------------- |
| API 概述    | `references/api-overview.md`    | 认证、分页、基础 URL、响应数据格式                                                                                   |
| 标签（Hashtags）        | `references/hashtags.md`        | 标签排名（按使用次数和观看次数）、过滤功能                                                                                   |
| 趋势（Trends）          | `references/trends.md`          | 每日趋势摘要、趋势分类                                                                                         |
| 视频（Videos）          | `references/videos.md`          | 跨平台热门视频列表、平台特定端点、过滤与排序功能                                                                                   |
| Orbit           | `references/orbits.md`          | 基于关键词的搜索任务、异步数据获取、视频内容、广告信息、创作者数据分析                                                                       |
| Comet           | `references/comets.md`          | 自动化细分领域监控配置、任务调度、CRUD 操作、视频内容、广告信息、创作者数据分析                                                                       |
| 速率限制（Rate Limits）     | `references/rate-limits.md`     | 速率限制策略及相关头部信息                                                                                         |
| 错误处理（Error Handling） | `references/error-handling.md`    | HTTP 状态码、错误响应格式                                                                                         |

请仅加载与当前任务相关的参考文档，无需一次性加载所有文件。

## 远程文档

完整的 API 文档可在 [https://dev.virlo.ai/docs](https://dev.virlo.ai/docs) 查阅，同时提供交互式测试环境 [https://dev.virlo.ai/docs/playground](https://dev.virlo.ai/docs/playground)。
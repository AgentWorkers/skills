---
name: lightrag
description: 使用 LightRAG API 搜索和管理知识库。该 API 支持多服务器环境、上下文感知的写作功能以及直接的信息检索。当用户需要查询由 LightRAG 提供支持的知识库，或将其作为任务执行的上下文信息时，可以使用该 API。
---

# LightRAG 技能

此技能允许您与一个或多个 LightRAG API 服务器进行交互。您可以在不同的模式下执行查询（本地模式、全局模式、混合模式、简单模式），并使用检索到的上下文数据进行进一步处理。

## 配置

该技能使用位于 `~/.lightrag_config.json` 的配置文件来存储服务器详细信息。
格式：
```json
{
  "servers": {
    "alias1": {
      "url": "http://server1:9621",
      "api_key": "optional_key"
    },
    "alias2": {
      "url": "http://server2:9621",
      "api_key": "optional_key"
    }
  },
  "default_server": "alias1"
}
```

## 工作流程

### 1. 直接搜索
要查找信息，请使用 `scripts/query_lightrag.py`。
支持的模式：`local`、`global`、`hybrid`、`mix`、`naive`。

### 2. 使用上下文数据进行写作
要将知识库作为上下文数据使用（例如，用于测试或撰写文章）：
1. 运行 `query_lightrag.py` 并使用 `--only-context` 标志。
2. 将生成的上下文数据传递给您的写作任务或模型。

## 参考资料
有关端点详情，请参阅 [API_DOCS.md](references/API_DOCS.md)。
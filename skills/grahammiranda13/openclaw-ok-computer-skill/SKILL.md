---
name: ok-computer-swarm
description: 根据 Kimi.com 的 OK Computer 和 Agent Swarm 功能【453334500861599†L40-L99】的启发，该技能会生成多个子代理来同时对一系列主题进行并行研究。每个子代理会使用 DuckDuckGo 对其分配的主题进行搜索，并返回最相关的结果。所有子代理完成搜索后，该技能会将它们的发现汇总成一份结构化的报告。这种技能适用于需要广泛、多主题的研究场景，在这些场景中，并行处理能够显著节省时间。
user-invocable: true
metadata:
  moltbot:
    emoji: "🧠"
    requires:
      bins: ["python"]
    homepage: https://www.grahammiranda.com/
---
# OK 计算机群组（OK Computer Swarm）

## 概述

该技能允许 OpenClaw 模拟 Kimi 的 Agent Swarm【453334500861599†L40-L99】所使用的“100 个子代理”架构。当您需要同时研究多个主题时，该技能会启动多个轻量级的子代理，通过 DuckDuckGo 获取网页搜索结果。通过并行执行这些任务，可以减少整体等待时间，并获取更丰富的信息来源。

## 命令

### `/ok-computer-swarm search`

同时搜索多个主题。

**输入参数**

- `query`（字符串，可重复输入）：一个或多个搜索关键词。您可以输入多个 `query` 参数来同时搜索多个主题。至少需要提供一个 `query` 参数。

**示例**

```bash
python scripts/swarm_search.py --query "Agent Swarm" --query "OpenClaw skills"
```

**输出**

脚本会输出一个 JSON 数组，其中每个元素代表一个搜索请求。每个元素包含原始的搜索查询以及一个结果对象数组（标题和网址）。这种格式便于后续处理或汇总。

## 适用场景

在需要同时收集多个主题的高层次信息时，可以使用 `ok-computer-swarm`。它适用于以下场景：

- 涉及多个不同主题的广泛研究任务。
- 为更深入的分析提供初始数据。
- 时间紧迫、顺序搜索效率较低的情况。

## 限制

- 该技能使用 DuckDuckGo 的免费 API，因此搜索结果可能不如付费搜索 API 全面。
- 它仅进行最基本的汇总处理。如需更深入的见解，建议集成额外的汇总或阅读工具。
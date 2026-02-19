---
name: smart-spawn-api
description: "使用 Smart Spawn API 为任何任务选择最佳 AI 模型。无需任何插件，只需向 ss.deeflect.com/api 发送 HTTP 请求即可。"
---
# 智能模型选择 API (Smart Model Selection API)

该 API 可帮助您为任何任务选择最适合的 AI 模型。只需调用该 API，即可获得模型推荐，并使用所选模型来执行任务。

**无需任何插件**，适用于任何 OpenClaw 实例或任何 HTTP 客户端。

## 快速入门

```
1. GET ss.deeflect.com/api/pick?task=<description>&budget=<tier>
2. Use the returned model ID in sessions_spawn
```

## 选择最佳模型

```bash
GET https://ss.deeflect.com/api/pick?task=build+a+react+dashboard&budget=medium
```

响应结果：
```json
{
  "data": {
    "id": "anthropic/claude-opus-4.6",
    "name": "Claude Opus 4.6",
    "score": 86,
    "pricing": { "prompt": 5, "completion": 25 },
    "reason": "Best general model at medium budget ($0-5/M) — score: 86"
  }
}
```

随后使用所选模型执行任务：
```
sessions_spawn(task="Build a React dashboard with auth", model="anthropic/claude-opus-4.6")
```

## 参数说明

| 参数 | 是否必填 | 说明 |
|-------|----------|-------------|
| `task` | 是 | 任务描述或类别（例如：`coding`、`reasoning`、`creative`、`vision`、`research`、`fast-cheap`、`general`） |
| `budget` | 否 | 预算范围：`low`（0-100 美元/月）、`medium`（0-500 美元/月，默认值）、`high`（200-2000 美元/月）、`any` |
| `exclude` | 否 | 用逗号分隔的模型 ID，表示需要排除的模型 |
| `context` | 否 | 标签（如 `vision`、`long-context`）用于优化模型选择 |

## 获取多个模型推荐

```bash
GET https://ss.deeflect.com/api/recommend?task=coding&budget=low&count=3
```

该 API 会从多个提供商处获取多样化的模型推荐，适用于需要同时使用多个模型的场景。

## 比较模型

```bash
GET https://ss.deeflect.com/api/compare?models=anthropic/claude-opus-4.6,openai/gpt-5.2
```

提供模型的详细评分、价格和功能信息。

## 浏览所有模型

```bash
GET https://ss.deeflect.com/api/models?category=coding&sort=score&limit=10
```

支持按 `score`、`cost`、`efficiency` 或其他类别名称对模型进行排序。

## 分解复杂任务

```bash
POST https://ss.deeflect.com/api/decompose
{"task": "Build and deploy a SaaS app", "budget": "medium"}
```

为复杂任务分解为多个子任务，并为每个子任务推荐最合适的模型。

## 并行任务调度（Swarm）

```bash
POST https://ss.deeflect.com/api/swarm
{"task": "Research competitors and build pitch deck", "budget": "low"}
```

生成包含模型分配的并行任务依赖图。

## 使用示例

对于需要多个子任务的场景：
1. **确定预算**：`low` 预算适用于低成本/快速任务；`medium` 预算适用于高质量任务；`high` 预算适用于最佳模型 |
2. 调用 `/api/pick` 并传入任务描述 |
3. 将返回的模型 ID 作为 `sessions_spawn` 函数的 `model` 参数 |
4. 如果任务复杂，可以使用 `/api/decompose` 或 `/api/swarm` 将任务分解为多个子任务，并为每个子任务选择合适的模型 |

## 错误处理
- API 无法访问 → 跳过模型选择，直接使用 `sessions_spawn` 函数（默认模型） |
- 未找到合适的模型（404 错误） → 增加预算范围（设置为 `any`）并重试 |
- 被限制请求次数（429 错误） → 等待片刻后重试，或使用默认模型 |

## API 状态信息

```bash
GET https://ss.deeflect.com/api/status
```

显示模型数量、数据更新频率以及数据来源的运行状态。数据每 6 小时从 5 个基准数据源更新一次。
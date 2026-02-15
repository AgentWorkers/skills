---
name: blackclaw
description: "实时加密风险情报：在问题发生之前以及问题发生时提供预警。提供两种工具：  
- **Flare**：具备15分钟的前兆检测能力，并能立即发出警报；  
- **Core**：能够进行60分钟的状态分析，并提供全面的背景评估。  
用户可以免费查看最新的分析报告，无需使用API密钥。如需自定义分析功能，可升级至x402版本。"
homepage: https://github.com/blackswanwtf/blackswan-mcp
metadata: {"emoji": "🦢", "requires": {"bins": ["curl"]}}
---

# BlackSwan 风险情报

BlackSwan 24/7 监控加密货币市场，并生成两种风险评估报告：

- **Flare**：基于 15 分钟时间窗口的预警信号，用于即时风险检测（在新闻发布前）。  
- **Core**：基于 60 分钟时间窗口的市场状况分析，用于了解市场背景和进行全面的风险评估（在新闻发布时）。

## 各工具的使用场景

| 问题 | 工具 |
|------|------|
| “现在有什么情况吗？” | Flare |
| “整体市场风险状况如何？” | Core |
| “我需要担心市场突然的波动吗？” | Flare |
| “请提供全面的风险评估报告” | 先使用 Flare，再使用 Core |

## 基础 URL

```
https://mcp.blackswan.wtf
```

## 端点

### GET /api/flare

返回最新的 Flare 预警风险评估结果。

```bash
curl -s https://mcp.blackswan.wtf/api/flare
```

**响应字段：**

| 字段 | 描述 |
|-------|-------------|
| `agent` | 始终为 `"flare"` |
| `data_age` | 数据的可用时间（例如：“12 分钟前”） |
| `status` | `"clear"` 或 `"alert"` |
| `severity` | `"none"`, `"low"`, `"medium"`, `"high"`, 或 `"critical"` |
| `checked_at` | 评估的 ISO 8601 时间戳 |
| `assessment` | 用自然语言表达的风险评估结果 |
| `signals` | 检测到的信号数组，每个信号包含 `type`（类型）、`source`（来源）和 `detail`（详细信息） |

### GET /api/core

返回最新的 Core 市场状况分析结果。

```bash
curl -s https://mcp.blackswan.wtf/api/core
```

**响应字段：**

| 字段 | 描述 |
|-------|-------------|
| `agent` | 始终为 `"core"` |
| `data_age` | 数据的可用时间（例如：“1 小时前”） |
| `timestamp` | 评估的 ISO 8601 时间戳 |
| `environment` | `"stable"`, `"elevated"`, `"stressed"`, 或 `"crisis"` |
| `assessment` | 用自然语言表达的风险评估结果 |
| `key_factors` | 描述主要风险因素的字符串数组 |
| `sources_used` | 用于评估的数据源名称数组 |
| `data_freshness` | 数据的更新频率 |

## 解释风险等级（Flare）

| 风险等级 | 含义 |
|---------|---------|
| `none` | 未检测到预警信号，市场平静 |
| `low` | 出现了值得注意的轻微信号，但无需立即行动 |
| `medium` | 出现了显著的信号，需要关注 |
| `high` | 检测到强烈的预警信号，市场可能出现突然波动 |
| `critical` | 出现极端信号，市场可能面临重大事件的风险 |

## 解释市场状况等级（Core）

| 市场状况 | 含义 |
|-------------|---------|
| `stable` | 市场状况正常，系统性风险较低 |
| `elevated` | 风险高于正常水平，存在一些压力迹象 |
| `stressed` | 多个指标显示出显著的市场压力 |
| `crisis` | 市场压力严重，可能出现混乱或传染性事件 |

## 错误处理

| HTTP 状态码 | 含义 |
|-------------|---------|
| `200` | 请求成功，响应中包含完整评估结果 |
| `502` | 代理输出验证失败——格式可能已更改 |
| `503` | 最近没有运行代理——系统可能正在启动 |
| `500` | 服务器出现意外错误 |

对于非 200 状态码的响应，响应体中会包含 `{"error": "..."` 以及相应的错误信息。

## 完整的风险检查流程

为了获得全面的市场情况，需要同时调用这两个端点：

```bash
curl -s https://mcp.blackswan.wtf/api/flare
curl -s https://mcp.blackswan.wtf/api/core
```

首先查看 Flare 的结果（即时风险），然后查看 Core 的结果（更全面的市场背景）。
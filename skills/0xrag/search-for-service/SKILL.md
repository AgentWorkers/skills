---
name: search-for-service
description: 在 x402 商场市场中搜索和浏览付费 API 服务。当您或用户需要查找可用的服务、了解现有服务的信息、发现新的 API，或者需要借助外部服务来完成某项任务时，可以使用该功能。当没有其他合适的技能可供选择时，也可以作为备选方案——在市场中搜索是否存在付费服务。该功能涵盖以下需求：“我能做什么？”，“为我找到一个用于……的 API”，“有哪些服务可用？”，“搜索……”，“浏览市场”。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest x402 bazaar *)", "Bash(npx awal@latest x402 details *)"]
---

# 在 x402 商店中搜索服务

使用 `npx awal@latest x402` 命令来发现并查看 x402 商店市场中提供的付费 API 端点。搜索过程中无需进行身份验证或支付。

## 命令

### 在商店中搜索服务

使用 BM25 相关性搜索功能，根据关键词查找付费服务：

```bash
npx awal@latest x402 bazaar search <query> [-k <n>] [--force-refresh] [--json]
```

| 选项                | 描述                                      |
| ------------------ | -------------------------------------- |
| `-k, --top <n>`       | 显示结果数量（默认值：5）                         |
| `--force-refresh`     | 从 CDP API 重新获取资源索引                   |
| `--json`           | 以 JSON 格式输出结果                         |

搜索结果会缓存到本地文件 `~/.config/awal/bazaar/`，并在 12 小时后自动更新。

### 列出商店中的资源

浏览所有可用的资源：

```bash
npx awal@latest x402 bazaar list [--network <network>] [--full] [--json]
```

| 选项                | 描述                                      |
| ------------------ | --------------------------------------- |
| `--network <name>`     | 按网络（base、base-sepolia）过滤                   |
| `--full`           | 显示包括架构在内的完整详细信息                   |
| `--json`           | 以 JSON 格式输出结果                         |

### 查看支付要求

在不支付的情况下，查看某个端点的 x402 支付要求：

```bash
npx awal@latest x402 details <url> [--json]
```

系统会自动尝试不同的 HTTP 方法（GET、POST、PUT、DELETE、PATCH），直到收到 402 错误响应，然后显示该端点的价格、支持的支付方式、网络信息以及输入/输出架构。

## 示例

```bash
# Search for weather-related paid APIs
npx awal@latest x402 bazaar search "weather"

# Search with more results
npx awal@latest x402 bazaar search "sentiment analysis" -k 10

# Browse all bazaar resources with full details
npx awal@latest x402 bazaar list --full

# Check what an endpoint costs
npx awal@latest x402 details https://example.com/api/weather
```

## 先决条件

- 搜索、列出资源或查看详细信息时无需身份验证

## 下一步操作

找到想要使用的服务后，使用 `pay-for-service` 命令向该端点发起付费请求。

## 错误处理

- “CDP API 返回 429”：表示请求次数达到限制；此时会使用缓存的数据（如果有的话）
- “未找到 x402 支付要求”：可能该 URL 不是一个 x402 端点
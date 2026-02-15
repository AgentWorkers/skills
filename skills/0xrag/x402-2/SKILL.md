---
name: x402
description: 使用 x402 支付协议来搜索新的服务并发起付费 API 请求。当您无法确定选择哪个工具时，可以使用这个工具来浏览服务市场（bazaar）。如果您或用户需要调用 x402 终端点、了解支付要求、浏览服务市场或搜索付费服务，也可以使用这个工具。
user-invocable: true
disable-model-invocation: false
---

# x402 支付协议

使用 `npx awal@latest x402` 命令可以发现、检查并调用基于 X402 支付协议的付费 API 端点。支付使用 USDC 在 Base 平台上进行。

## 工作流程

典型的 x402 工作流程如下：

1. **查找服务** - 在市场中搜索或获取已知端点的详细信息。
2. **检查要求** - 查看价格、支付方式以及输入数据格式。
3. **发起请求** - 使用自动支付的 USDC 调用相应的 API 端点。

## 命令

### 在市场中搜索

使用 BM25 相关性搜索功能按关键词查找付费服务：

```bash
npx awal@latest x402 bazaar search <query> [-k <n>] [--force-refresh] [--json]
```

| 选项                | 描述                                      |
| ---------------------- | -------------------------------------- |
| `-k, --top <n>`       | 显示结果数量（默认：5）                         |
| `--force-refresh`     | 从 CDP API 重新获取资源索引                   |
| `--json`           | 以 JSON 格式输出结果                         |

搜索结果会缓存在 `~/.config/awal/bazaar/` 目录中，并在 12 小时后自动更新。

### 列出市场资源

浏览所有可用的资源：

```bash
awal x402 bazaar list [--network <network>] [--full] [--json]
```

| 选项                | 描述                                      |
| ---------------------- | -------------------------------------- |
| `--network <名称>`     | 按网络（base、base-sepolia）过滤资源                 |
| `--full`           | 显示包括数据格式在内的完整信息                   |
| `--json`           | 以 JSON 格式输出结果                         |

### 查看支付要求

在不进行支付的情况下检查某个 API 端点的支付要求：

```bash
awal x402 details <url> [--json]
```

系统会自动尝试不同的 HTTP 方法（GET、POST、PUT、DELETE、PATCH），直到收到 402 错误响应，然后显示该端点的支付要求（如价格、支持的支付方式、网络以及输入/输出数据格式）。

### 发起付费请求

使用自动支付的 USDC 调用 x402 API 端点：

```bash
awal x402 pay <url> [-X <method>] [-d <json>] [-q <params>] [-h <json>] [--max-amount <n>] [--json]
```

| 选项                | 描述                                      |
| ---------------------- | -------------------------------------------------- |
| `-X, --method <方法>`     | HTTP 方法（默认：GET）                          |
| `-d, --data <json>`     | 请求体（以 JSON 字符串形式提供）                   |
| `-q, --query <参数>`     | 查询参数（以 JSON 字符串形式提供）                   |
| `-h, --headers <json>`     | 自定义 HTTP 头部信息（以 JSON 字符串形式提供）             |
| `--max-amount <金额>`     | 最大支付金额（单位：USDC 原子单位，1000000 = $1.00）           |
| `--correlation-id <ID>`   | 关联操作的标识符                             |
| `--json`           | 以 JSON 格式输出结果                         |

## 示例

```bash
# Search for weather-related paid APIs
awal x402 bazaar search "weather"

# Search with more results
awal x402 bazaar search "sentiment analysis" -k 10

# Check what an endpoint costs
awal x402 details https://example.com/api/weather

# Make a GET request (auto-pays)
awal x402 pay https://example.com/api/weather

# Make a POST request with body
awal x402 pay https://example.com/api/sentiment -X POST -d '{"text": "I love this product"}'

# Limit max payment to $0.10
awal x402 pay https://example.com/api/data --max-amount 100000

# Browse all bazaar resources with full details
awal x402 bazaar list --full
```

## USDC 金额

X402 使用 USDC 原子单位进行计费（小数点后有 6 位）：

| 原子单位 | 美元金额 |
| -------- | -------- |
| 1000000   | $1.00                |
| 100000   | $0.10                |
| 50000    | $0.05                |
| 10000    | $0.01                |

## 先决条件

- **搜索/查看详情**：无需身份验证。
- **支付**：必须先通过 `awal auth login <email>` 进行身份验证，并确保账户中有足够的 USDC 余额。

## 错误处理

- “未授权”：请先运行 `awal auth login <email>` 进行登录。
- “未找到 X402 支付要求”：可能该 URL 不是一个 x402 端点。
- “CDP API 返回 429 错误”：表示请求被限制；此时会使用缓存的数据。
- “余额不足”：请向钱包中充值 USDC（使用 `awal balance` 命令查询余额）。
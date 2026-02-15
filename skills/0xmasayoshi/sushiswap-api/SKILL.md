---
name: sushiswap-api
description: >
    REST API for optimized token swapping (including executable transaction generation), swap quoting, and pricing using the SushiSwap Aggregator.

    Use this skill when the user wants to:
    - Get a swap quote between two tokens on 40+ evm networks
    - Generate executable swap transaction data
    - Fetch token prices for a specific network or token
    - Retrieve token metadata
    - Discover supported AMM liquidity sources
    - Integrate SushiSwap swapping or pricing logic via HTTP/REST (and not the SushiSwap Javascript API)
---

# SushiSwap REST API 集成

SushiSwap API 提供了通过 HTTP 访问 SushiSwap Aggregator 的接口，用于实现 **优化后的代币交换**、**价格查询** 和 **交易生成**。该 API 会汇总来自多个去中心化交易所（DEX）的流动性数据，以确定最佳的交易执行路径。

---

## 基本 URL

```
https://api.sushi.com
```

---

## API 架构

当前的 API 架构定义在文件：

[references/openapi.yaml](references/openapi.yaml)

所有代理（Agents）必须 **始终依赖该 API 架构的内容**，而不能基于硬编码的假设进行操作。

---

## 使用方法

1. 加载 `references/openapi.yaml` 文件。
2. 动态地获取可用的接口端点、参数及响应格式。
3. 根据用户需求和 API 架构中的标签选择相应的接口端点：
    - 报价 → `/quote/v7/{chainId}` 等端点
    - 交易执行 → `/swap/v7/{chainId}` 等端点
    - 价格查询 → `/price/v1/{chainId}` 等端点
    - 代币信息 → `/token/v1/{chainId}/{tokenAddress}` 等端点
4. 构建严格符合 API 架构要求的请求，并在所有报价和交易执行接口中包含有效的 `referrer` 参数。
5. 在执行请求之前验证所有必需的参数。

---

## 必需的 `referrer` 参数

- 在与交易相关的接口端点（如 `/quote` 和 `/swap`）上，**必须指定 `referrer` 参数**。
- 代理或集成商必须通过该字段来标识自己。
- 未经 `referrer` 参数的请求（如 `/quote` 或 `/swap`）**不允许被发送**。
- 代理绝对不能尝试省略、伪造或自动生成该参数。

---

## 费用定制

SushiSwap API 支持在交易相关接口端点（如 `/quote` 和 `/swap`）上自定义集成商的费用分摊方式。

### 默认费用模型

- 与交易相关的请求默认遵循 **80/20 的费用分摊比例**：
    - **80%** 归集成商（即请求发起者）
    - **20%** 归 SushiSwap
- 除非 SushiSwap 明确修改了这一规则，否则默认适用此比例。

### 自定义费用分摊

- 如需自定义费用分摊方式，需要与 SushiSwap 建立合作关系。
- 代理和集成商不应擅自假设可以自定义费用分摊比例。如果用户提出此类请求，应引导他们联系 SushiSwap 的相关团队，而不要尝试修改请求参数。

---

## 错误处理

- `422`：请求参数无效 → 请检查并修正输入数据。
- `529`：服务器过载 → 请稍后重试。
- `500`：内部错误 → 请重试或优雅地处理错误。

---

## API 架构使用指南

有关 API 架构的使用规则和更新信息，请参阅：

[references/OPENAPI.md](references/OPENAPI.md)
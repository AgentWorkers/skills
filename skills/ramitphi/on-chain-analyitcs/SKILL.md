---
name: onchain-analysis
description: 分析任何以太坊虚拟机（EVM）智能合约：自动获取合约的抽象接口（ABI）信息，识别合约的使用模式，通过 Dune 解码合约中的函数调用，生成基于人工智能的分析结果（图表、统计数据、时间序列数据），并返回结构化的数据。支持 Ethereum、Polygon、BSC、Arbitrum、Optimism、Base、Avalanche 等区块链平台。
---
# 在链分析技能

通过粘贴智能合约的地址，您可以对该合约进行全面的分析。该技能会执行以下分析流程：

1. **ABI获取** — 从Etherscan获取已验证的ABI（或接受用户提供的手动ABI）。
2. **使用情况查询** — 通过Dune查询哪些方法被最频繁地调用，以及调用者是谁、调用了多少次。
3. **解码后的数据表** — 人工智能使用`decode_evm_function_call()`生成DuneSQL查询，从而在Dune上构建原始的解码数据表。
4. **数据分析** — 第二轮人工智能处理会从解码后的数据表中生成6-10个可视化查询（统计信息、时间序列图、条形图、饼图）。
5. **执行** — 所有查询都在Dune上执行，结果以结构化JSON的形式返回。

## 使用场景

- 用户请求“分析这个合约”或“这个合约的功能是什么”。
- 用户需要智能合约的链上分析数据、使用情况统计或仪表板。
- 用户提供了合约地址，并希望了解其活动情况。
- 用户想了解交易模式、调用者行为或函数使用情况。
- 用户想比较函数的使用频率或识别主要调用者。
- 用户想知道“谁在使用这个合约”或“这个合约的受欢迎程度”。

## 使用方法

**POST** `https://esraarlhpxraucslsdle.supabase.co/functions/v1/onchain-analysis`

### 请求体

```json
{
  "contractAddress": "0x00000000009726632680FB29d3F7A9734E3010E2",
  "chain": "base",
  "abi": "(optional — raw ABI JSON string if contract is unverified)"
}
```

### 参数

| 参数 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `contractAddress` | string | 是 | EVM合约地址（以0x开头，共42个字符） |
| `chain` | string | 是 | 可选值：`ethereum`、`polygon`、`bsc`、`arbitrum`、`optimism`、`base`、`avalanche` |
| `abi` | string/array | 否 | 如果合约未在Etherscan上验证，则需要提供手动ABI |

### 支持的链

| 链 | 对应的浏览器/工具 |
|-------|-----------------|
| `ethereum` | etherscan.io |
| `polygon` | polygonscan.com |
| `bsc` | bscscan.com |
| `arbitrum` | arbiscan.io |
| `optimism` | optimistic.etherscan.io |
| `base` | basescan.org |
| `avalanche` | snowtrace.io |

### 响应结果

```json
{
  "contractAddress": "0x...",
  "chain": "base",
  "tldr": "## TLDR\n\n- **Key insight 1** ...\n- **Key insight 2** ...",
  "abiSummary": "Events (5):\n  - Transfer(...)\nWrite Functions (8):\n  - swap(...)",
  "dashboardUrl": "https://onchainwizard.ai/shared/abc123-uuid",
  "topMethods": [
    {
      "function_name": "swap",
      "call_count": 142000,
      "unique_callers": 5200,
      "total_eth": 1234.5678
    }
  ],
  "rawTables": [
    {
      "function_name": "swap",
      "query_id": 12345,
      "dune_url": "https://dune.com/queries/12345",
      "execution_state": "QUERY_STATE_COMPLETED"
    }
  ],
  "queryResults": [
    {
      "id": "total_swaps",
      "title": "Total Swaps",
      "type": "stat",
      "sql": "SELECT COUNT(*) AS value FROM query_12345",
      "rows": [{ "value": 142000 }]
    },
    {
      "id": "daily_swaps",
      "title": "Daily Swap Volume",
      "type": "timeseries",
      "sql": "SELECT DATE_TRUNC('day', block_time) AS date, COUNT(*) AS value FROM query_12345 GROUP BY 1 ORDER BY 1",
      "rows": [
        { "date": "2026-01-01", "value": 500 },
        { "date": "2026-01-02", "value": 620 }
      ]
    }
  ]
}
```

### 查询结果类型

| 类型 | 描述 | 关键字段 |
|------|-------------|------------|
| `stat` | 单个指标 | `rows[0].value` — 主要统计结果 |
| `timeseries` | 时间序列数据 | `rows[].date`, `rows[].value` |
| `bar` | 分类对比 | `rows[].label`, `rows[].value` |
| `pie` | 分布情况 | `rows[].label`, `rows[].value` |
| `scatter` | 相关性 | `rows[].x`, `rows[].y` |

## 结果展示方式

1. **首先提供简要概述** — 以Markdown格式展示结果，让用户快速了解情况。
2. **提供仪表板链接** — 始终提供`dashboardUrl`，让用户可以查看完整的交互式仪表板：“📊 [查看完整仪表板](dashboardUrl)”。
3. **统计查询**（`type: "stat"`） — 以标题形式展示统计结果（例如：“总交易次数：142,000次”）。
4. **时间序列图**（`type: "timeseries"`） — 描述趋势（“每日交易量在Y日期达到峰值X”）。
5. **条形图/饼图**（`type: "bar"` / `type: "pie"`） — 总结分布情况（“前5大调用者占交易量的60%”）。
6. **提供Dune链接** — 提供`dune_url`，让用户可以进一步查看原始数据表。
7. **查询失败** — 如果查询返回`error`而非`rows`，简要说明原因，但不要影响其他结果的展示。

## 示例对话

### 基本用法：
**用户：** 分析0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D在以太坊上的合约。
**操作：** 调用该技能，传入`{"contractAddress": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", "chain": "ethereum"}`。
**结果展示：** 简要概述 → 统计数据 → 趋势分析 → 分布情况 → Dune数据链接。

### 缺少链信息：
**用户：** 0xABC...DEF这个合约是做什么的？
**操作：** 在调用前询问合约所在的链：“这个合约是在哪个链上运行的？我支持Ethereum、Polygon、BSC、Arbitrum、Optimism、Base和Avalanche。”

### 合约未验证的情况：
**用户：** 在Base链上分析0xABC...DEF。
**API返回：** `“无法获取ABI”**
**操作：** 要求用户提供ABI的JSON格式内容，然后重新调用`{"contractAddress": "...", "chain": "base", "abi": "<用户提供的ABI>"}`。

### 分析后的后续操作：
- “请详细说明主要的调用者是谁？” — 根据`queryResults`中的条形图/饼图数据进行扩展说明。
- “`swap`函数的功能是什么？” — 使用`abiSummary`进行解释。
- “我能查看原始数据吗？” — 提供`rawTables[].dune_url`链接。

## 重要说明：

- 由于Dune的查询和数据处理需要时间（2-5分钟），请用户做好等待准备。
- 仅适用于具有已验证ABI的合约（除非提供了手动ABI）。
- 人工智能会根据使用情况自动选择最相关的函数。
- 解码后的原始数据表会保存在Dune上，以便后续参考。
- 如果合约在链上的活动非常少，查询结果可能为空。

## 错误处理：

| 错误 | 含义 | 建议的操作 |
|-------|---------|-------------------|
| `“无法获取ABI”` | 合约未经过验证 | 要求用户提供ABI。 |
| `“未找到可修改状态的函数”` | 合约可能是只读的或代理合约 | 通知用户。 |
| `“不支持的链”` | 链不在支持列表中 | 列出支持的链并重新请求。 |
| `“缺少必要的API密钥”` | 服务器配置问题 | 作为服务错误报告。 |
| 超时/无响应 | 分析超时 | 建议重试；Dune可能正在处理大量请求。 |
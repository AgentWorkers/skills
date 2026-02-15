---
name: create-test-pool
description: >-
  Deploy a custom Uniswap pool on the local testnet with configurable parameters.
  Create pools with specific conditions (thin liquidity, wide spreads, exact tick
  ranges) to test agent behavior under controlled scenarios. Requires a running
  local testnet.
model: sonnet
allowed-tools:
  - mcp__uniswap__deploy_mock_pool
  - mcp__uniswap__fund_test_account
  - mcp__uniswap__get_pool_info
  - mcp__uniswap__search_tokens
---

# 创建测试池

## 概述

该工具会在本地测试网络上部署一个自定义的 Uniswap 池，参数由用户指定。这允许您创建受控的测试环境——例如流动性较低的池、价格范围极端的池、特定费用级别的池——以测试代理在极端条件下的行为。

**为什么这比手动操作好10倍：**

1. **无需编写 Solidity 脚本**：手动创建 V3 池需要调用 `createAndInitializePoolIfNecessary`、计算 `sqrtPriceX96`、确定价格变动范围、批准代币以及调用 `mint` 等操作，而该工具可以自动完成这些步骤。
2. **代币解析**：只需输入 “WETH/USDC” 等格式，工具就能正确解析地址、小数位数并排序代币，无需手动查找合约地址。
3. **自动资金注入**：如果部署者账户的代币不足，工具会自动模拟“鲸鱼交易”来为部署提供资金。
4. **价格到价格变动范围的转换**：指定价格（如 “2000” 表示每 WETH 2000 USDC），工具会自动计算出正确的 `sqrtPriceX96` 和价格变动范围。
5. **边缘情况测试**：可以创建流动性仅为 100 美元的池来测试市场疲软时的行为，或者创建价格极端的池来测试边界条件。
6. **验证**：部署完成后，可以使用 `get_pool_info` 立即查询池的状态。

## 适用场景

当用户提出以下请求时，请使用此工具：

- “创建一个流动性较低的 WETH/USDC 池”
- “部署一个费用为 0.05% 的测试池”
- “设置一个 DAI/USDC 比例为 1:1 的池”
- “创建一个仅有 1000 美元流动性的池”
- “部署一个 V2 类型的池进行测试”
- “我需要一个价格变动范围较小的池”
- “创建一个当前价格下的 WBTC/WETH 池”
- “设置一个用于测试高滑点情况的池”

**不适用场景**：
- 当本地测试网络未运行时（请先使用 `setup-local-testnet`）；
- 当用户希望与现有的主网池交互时（请使用 `analyze-pool`）。

## 参数

| 参数          | 是否必填 | 默认值     | 获取方式                                                                                              |
|--------------|--------|---------|-------------------------------------------------------------------------------------------------------------------------|
| token0        | 是      | --        | 第一种代币：WETH、USDC 或 0x 地址                                                                                         |
| token1        | 是      | --        | 第二种代币：USDC、DAI 或 0x 地址                                                                                         |
| version       | 否      | v3        | “v2” 或 “v3”                                                                                          |
| fee           | 否      | 3000      | 费用级别：100（0.01%）、500（0.05%）、3000（0.3%）、10000（1%）                                                                                   |
| initialPrice    | 否      | --        | token0 用 token1 表示的价格（例如：当 ETH 价格为 2000 时，initialPrice 为 2000）                                                                 |
| liquidityUsd     | 否      | 1,000,000    | 初始流动性的美元价值                                                                                         |
| tickLower       | 否      | 自动设置    | V3 版本下的价格变动下限（仅限高级用户使用）                                                                                   |
| tickUpper       | 否      | 自动设置    | V3 版本下的价格变动上限（仅限高级用户使用）                                                                                   |

## 工作流程

### 第一步：验证测试网络是否运行

如果工具返回 `TESTNET_NOT_RUNNING`，请告知用户：

```text
No local testnet is running. Let me set one up first.
```

然后建议用户使用 `setup-local-testnet`，或者代为执行该操作。

### 第二步：解析参数

仔细解析用户的请求：

- **代币对**：例如 “WETH/USDC”、“ETH/DAI”、“WBTC/WETH”：
  - “ETH” 应被解析为 “WETH”（Uniswap 使用的是封装后的 ETH）。
- **费用级别**：例如 “0.05%” 对应 500，依此类推。
- **价格**：例如 “2000” 表示初始价格为 2000（WETH/USDC）。
- **流动性**：例如 “thin liquidity” 对应 liquidityUsd 为 1000，或 “$10M” 对应 liquidityUsd 为 1,000,000。
- **版本**：例如 “V2 pair” 对应 version 为 “v2”，默认为 “v3”。

**常见的流动性描述**：
- **thin** / **low** / **shallow**：流动性在 1,000 到 10,000 美元之间。
- **moderate** / **normal**：流动性在 100,000 到 1,000,000 美元之间。
- **deep** / **high**：流动性在 1,000,000 美元以上。

### 第三步：（如有必要）为部署者充值

如果池需要部署者没有的代币，先调用 `mcp__uniswap__fund_test_account` 确保部署者（账户号 #1：`0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266`）拥有足够的代币。

### 第四步：部署池

使用解析出的参数调用 `mcp__uniswap__deployMockPool`。

### 第五步：验证并展示结果

展示已部署的池的详细信息：

```text
Test Pool Deployed

  Pool:       WETH/USDC (V3, 0.05% fee)
  Address:    0xNEW...
  Price:      1 WETH = 2,000 USDC
  Liquidity:  ~$1,000,000
  Tick Range: -204714 to -199514 (±50% around current price)

  Token0: USDC  0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48  (6 decimals)
  Token1: WETH  0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2  (18 decimals)

  Test Scenarios This Pool Enables:
  - Swap testing: "Get a quote for 1 WETH → USDC"
  - LP testing: "Add liquidity to the WETH/USDC pool"
  - Price impact: "What's the price impact of swapping 100 WETH?"
  - Time-dependent: "Advance 7 days and check fee accumulation"
```

### 第六步：提供后续操作建议

```text
  Next Steps:
  - Query pool state: "Get info on pool 0xNEW..."
  - Test a swap against this pool
  - Create another pool with different parameters
  - Advance time to test fee accumulation: "Time travel 7 days"
```

## 重要说明

- **代币会自动排序**：Uniswap 要求 token0 的地址在 token1 的地址之前。该工具会自动处理这一排序。
- **V3 版本的池需要初始化**：工具会调用 `createAndInitializePoolIfNecessary` 来设置初始价格。
- **默认的价格变动范围是 ±50%**：如果未指定价格变动范围，流动性会均匀分布在初始价格的附近。
- **部署者使用的是 Anvil 账户 #1**：默认使用 Anvil 的第一个账户进行部署。
- **池可能已经存在**：如果您在分叉后的以太坊网络上尝试创建某个池（例如 WETH/USDC 0.05% 的池），该池可能已经存在，工具会向现有池中添加流动性。
- **V2 版本的池始终费用为 0.3%**：V2 版本的池会忽略费用参数。

## 错误处理

| 错误类型            | 显示给用户的消息                                      | 建议的操作                                      |
|------------------|--------------------------------------------------|-----------------------------------------------------------|
| `TESTNET_NOT_RUNNING`     | “本地测试网络未运行。”                                      | 先运行 `setup-local-testnet`                            |
| `TESTNET_TOKEN_NOT_FOUND`     | “无法解析代币 X。”                                      | 使用常见的代币符号或提供 0x 地址                         |
| `TESTNET_CONTRACT_NOT_FOUND`    | “该链上找不到 NonfungiblePositionManager 合约。”                   | 分叉以太坊主网（包含所有 V3 版本的合约）                   |
| `TESTNET_DEPLOY_POOL_FAILED`     | “部署池失败：{原因}”                                      | 检查代币余额，如有需要为部署者充值                         |
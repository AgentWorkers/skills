---
name: lifi
description: 通过 LI.FI 协议实现跨链代币互换与桥接功能：获取报价、执行转账、追踪交易进度，并在 35 个以上的区块链上完成去中心化金融（DeFi）操作。
user-invocable: true
argument-hint: "[swap|bridge|track|routes|zap] <details>"
metadata: {"openclaw":{"emoji":"🔗","requires":{"bins":["curl"]},"primaryEnv":"LIFI_API_KEY"}}
---
# /lifi — 跨链交易与桥接服务

LI.FI 是一个跨链桥接服务及去中心化交易所（DEX）聚合协议。它能够通过比较数十个桥接服务（如 Stargate、Hop、Across 等）和去中心化交易所（如 Uniswap、SushiSwap、1inch 等），在 35 个以上的区块链之间找到最优的交易路径，从而实现代币的交换和跨链转账。

## 参数：`$ARGUMENTS`

解析参数：
- **第一个参数**：操作类型 — `swap`（交换）、`bridge`（桥接）、`track`（追踪）、`routes`（路由查询）、`zap`（快速交易）或自然语言请求
- **其余参数**：详细信息（代币名称、数量、目标链、交易哈希值等）

如果未提供参数，系统会询问用户具体需要执行什么操作。

## 关键概念

- **基础 URL**：`https://liQUEST/v1`
- API 返回的 `transactionRequest` 对象包含交易信息（`to`、`data`、`value`、`gasLimit`、`gasPrice`），可直接用于代理钱包的签名操作
- **原生代币地址**：`0x0000000000000000000000000000000000000000`（例如 ETH、MATIC、BNB 等的地址）
- 数量始终以代币的最小单位表示（wei）：1 ETH = `1000000000000000000`（18 位小数），1 USDC = `1000000`（6 位小数）
- 可通过 `x-lifi-api-key` 头部字段设置 API 密钥以提升交易速率限制（非强制要求）

---

## API 参考

### 发现相关端点

#### GET /v1/chains — 列出支持的区块链
```bash
curl -s "https://li.quest/v1/chains"
# Optional: ?chainTypes=EVM or ?chainTypes=SVM
```

#### GET /v1/tokens — 列出支持的代币
```bash
curl -s "https://li.quest/v1/tokens?chains=1,137"
# Optional: chainTypes, minPriceUSD
```

#### GET /v1/token — 获取特定代币的详细信息
```bash
curl -s "https://li.quest/v1/token?chain=1&token=USDC"
# chain (required): chain ID or name. token (required): address or symbol
```

#### GET /v1/connections — 检查可用的交易路径
```bash
curl -s "https://li.quest/v1/connections?fromChain=1&toChain=137&fromToken=0x0000000000000000000000000000000000000000"
# Optional: toToken, chainTypes, allowBridges
```

#### GET /v1/tools — 列出可用的桥接服务和去中心化交易所
```bash
curl -s "https://li.quest/v1/tools"
# Returns {bridges: [{key, name}], exchanges: [{key, name}]}
```

### 报价与交易相关端点

#### GET /v1/quote — 获取最优交易路径及交易数据
这是发起任何交易或桥接操作的主要接口。
**必需参数**：`fromChain`、`toChain`、`fromToken`、`toToken`、`fromAddress`、`fromAmount`
**可选参数**：`toAddress`、`slippage`（小数形式，例如 0.03 表示 3%）、`integrator`（集成器）、`order`（推荐、最快、最便宜、最安全）、`allowBridges`（是否允许使用桥接服务）、`allowExchanges`（是否允许使用去中心化交易所）

返回值：`action`、`estimate`（目标数量、费用、执行时间）以及 `transactionRequest`（交易信息）。

#### GET /v1/status — 跟踪跨链转账状态
```bash
curl -s "https://li.quest/v1/status?txHash=0xTX_HASH"
# Optional: bridge, fromChain, toChain
```
返回值：`status`（NOT_FOUND、PENDING、DONE、FAILED）、`substatus`（COMPLETED、PARTIAL、REFUNDED）以及源链/目标链的交易详情。

### 高级路由功能

#### POST /v1/advanced/routes — 比较多个交易路径
**必需参数**：`fromChainId`、`toChainId`、`fromTokenAddress`、`toTokenAddress`、`fromAmount`
**可选参数**：`toAddress`、`slippage`、`options.order`（交易顺序）

返回值：`routes[]` 数组，每个路径包含步骤、预计输出、费用和执行时间。

#### POST /v1/advanced/stepTransaction — 获取某个交易步骤的交易数据
**必需参数**：来自某个路径的步骤对象
返回值：可签名的 `transactionRequest` 对象。

#### POST /v1/quote/contractCalls — 多步骤 DeFi 操作组合
**必需参数**：`fromChain`、`toChain`、`fromToken`、`toToken`、`fromAddress`、`fromAmount`、`contractCalls[]`
**可选参数**：`slippage`（滑点）

### 燃气费用信息

#### GET /v1/gas/prices — 所有区块链的燃气价格信息
```bash
curl -s "https://li.quest/v1/gas/prices"
```

#### GET /v1/gas/suggestion/{chainId} — 某个区块链的推荐燃气费用参数
```bash
curl -s "https://li.quest/v1/gas/suggestion/1"
```

---

## 工作流程

### 工作流程 1 — 交换或桥接代币

适用于“将 X 代币交换为 Y 代币”或“将代币桥接到目标链”的请求：
1. **从用户请求中提取参数**：
   - 来源链和目标代币（例如：“以太坊上的 ETH”）
   - 目标链和目标代币（例如：“Polygon 上的 USDC”）
   - 以人类可读的形式输入数量（例如：“1.5 ETH”）
   - 钱包地址（代理钱包地址或用户提供的地址）

2. **如果用户提供了代币符号**，查询代币地址：
   ```bash
   curl -s "https://li.quest/v1/token?chain=1&token=USDC"
   ```
   从响应中提取 `address` 和 `decimals`（小数位数）

3. **将数量转换为代币的最小单位**：
   - 将人类可读的数量乘以 `decimals`（小数位数）
   - 例如：1.5 ETH（18 位小数）→ `1500000000000000000`
   - 100 USDC（6 位小数）→ `100000000`

4. **获取报价**：
   ```bash
   curl -s "https://li.quest/v1/quote?fromChain=1&toChain=137&fromToken=0x0000000000000000000000000000000000000000&toToken=0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359&fromAddress=0xWALLET&fromAmount=1500000000000000000&slippage=0.03"
   ```

5. **向用户展示交易概要**（在返回交易数据前必须展示）：
   ```
   Swap: 1.5 ETH (Ethereum) → ~2,850 USDC (Polygon)
   Route: Stargate bridge → Uniswap V3
   Fees: ~$2.50 (gas) + $0.50 (bridge)
   Estimated time: ~2 minutes
   Slippage: 3%
   ```

6. **如果是 ERC20 代币**：检查 LiFi 合同是否有足够的代币余额。 spender 地址为报价响应中的 `transactionRequest.to`。如果余额不足，请引导用户先批准代币。

7. **返回 `transactionRequest`，供代理钱包签名。

8. **如果是跨链交易**：说明桥接操作是异步的——首先需要确认来源链的交易，然后桥接服务才会将代币传输到目标链。建议使用工作流程 3 进行后续跟踪。

### 工作流程 2 — 比较交易路径

当用户希望查看多种交易选项或寻找最优方案时使用：
1. **收集参数**（与工作流程 1 的步骤 1-3 相同）。
2. **请求多个交易路径**：
   ```bash
   curl -s -X POST "https://li.quest/v1/advanced/routes" \
     -H "Content-Type: application/json" \
     -d '{
       "fromChainId": "1",
       "toChainId": "137",
       "fromTokenAddress": "0x0000000000000000000000000000000000000000",
       "toTokenAddress": "0x0000000000000000000000000000000000000000",
       "fromAddress": "0xWALLET",
       "fromAmount": "1000000000000000000",
       "options": {"order": "RECOMMENDED"}
     }'
   ```

3. **展示比较结果**：
   ```
   #  Route                     Output       Fees     Time    Bridge
   1  Stargate → Uniswap V3    2,850 USDC   $3.00    2 min   Stargate
   2  Hop → SushiSwap          2,845 USDC   $2.80    5 min   Hop
   3  Across → 1inch           2,848 USDC   $3.20    3 min   Across
   ```

4. **用户选择路径后**，获取该路径的详细交易信息：
   ```bash
   curl -s -X POST "https://li.quest/v1/advanced/stepTransaction" \
     -H "Content-Type: application/json" \
     -d '{ ...step object... }'
   ```

5. **返回 `transactionRequest`，供用户签名。

### 工作流程 3 — 跟踪交易状态

当用户需要查看跨链转账的状态时使用：
1. **获取用户提供的交易哈希值、来源链和目标链信息**。
2. **检查交易状态**：
   ```bash
   curl -s "https://li.quest/v1/status?txHash=0xTX_HASH&fromChain=1&toChain=137"
   ```

3. **解释状态**：
   - `NOT_FOUND`：交易尚未被记录。
   - `PENDING`：交易正在进行中，建议每 30 秒检查一次。
   - `DONE`（substatus 为 `COMPLETED`）：转账完成，显示目标交易哈希值。
   - `DONE`（substatus 为 `PARTIAL`）：用户收到了目标链上的桥接代币，但不是最终目标代币（例如收到了 USDC.e 而不是原生 USDC），用户可能需要手动进行二次交换。
   - `DONE`（substatus 为 `REFUNDED`）：转账失败，资金已退还到来源地址。
   - `FAILED`：转账失败，报告错误原因并建议用户查看来源链的交易记录。

4. **如果是 `PENDING` 状态**：建议用户定期检查交易状态。

### 工作流程 4 — 多步骤 DeFi 操作组合

适用于需要执行多步骤 DeFi 操作的情况（例如：“将 ETH 桥接到 Polygon 并存入 Aave”或“将代币交换为 USDC 并存入 DeFi 借贷池”）：
1. **确定操作步骤**：
   - 来源链/代币/数量
   - 目标链/中间代币
   - 目标合约及要调用的函数

2. **收集合约调用所需信息**：
   - `toContractAddress`：目标合约地址（例如 Aave 借贷池）
   - `toContractCallData`：ABI 编码的函数调用参数（例如 `deposit(address,uint256,address,uint16)`）
   - `toContractGasLimit`：合约调用的燃气费用上限（例如 “200000”）

3. **请求报价**：
   ```bash
   curl -s -X POST "https://li.quest/v1/quote/contractCalls" \
     -H "Content-Type: application/json" \
     -d '{
       "fromChain": "1",
       "toChain": "137",
       "fromToken": "0x0000000000000000000000000000000000000000",
       "toToken": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
       "fromAddress": "0xWALLET",
       "fromAmount": "1000000000000000000",
       "contractCalls": [{
         "toContractAddress": "0xTARGET",
         "toContractCallData": "0xENCODED_CALL",
         "toContractGasLimit": "200000"
       }]
     }'
   ```

4. **展示整个操作流程的概要**。
5. **返回 `transactionRequest`，供用户签名。

### 工作流程 5 — 信息查询

当用户询问“支持哪些区块链？”、“可以交换哪些代币？”、“有哪些桥接服务？”等问题时使用：
1. **确定用户需要了解的信息**：
   - 支持的区块链 → `GET /v1/chains`
   - 某个链上的代币 → `GET /v1/tokens?chains={chainId}`
   - 代币详情 → `GET /v1/token?chain={chainId}&token={symbol}`
   - 可用的交易路径 → `GET /v1/connections?fromChain={id}&toChain={id}`
   - 可用的桥接服务/去中心化交易所 → `GET /v1/tools`
   - 燃气价格 → `GET /v1/gas/prices` 或 `GET /v1/gas/suggestion/{chainId}`

2. **调用相应的 API 端点**。
3. **以易读的表格格式展示结果**。对于大量结果（如所有代币），总结最相关的信息并提供进一步筛选的选项。

---

## 安全协议

以下规则是强制性的，请务必遵守：

### 地址验证
- **始终** 确认 `fromAddress` 是有效的十六进制地址（以 `0x` 开头，共 42 个字符）。
- **绝对** 不要将地址 `0x0000000000000000000000000000000000000000` 作为 `toAddress` 发送，因为这会导致资金永久丢失。该地址仅适用于表示原生代币的 `fromToken`/`toToken`。

### 数量验证
- **始终** 在调用 API 之前将人类可读的数量转换为代币的最小单位：
  - 根据代币的 `decimals` 字段进行转换（ETH=18、USDC=6、WBTC=8、DAI=18）
  - 公式：`amount_wei = human_amount × 10^decimals`
- 数量必须是正整数（无小数、无负数、不能为 0）
- 最大长度为 78 位（uint256 类型）

### 滑点验证
- 如果用户未指定滑点，默认值为 `0.03`（3%）
- **警告** 如果滑点超过 3%，告知用户这可能导致实际收到的代币数量减少。
- **拒绝** 滑点超过 50%（例如 0.5%）的情况，因为这几乎肯定是错误。
- 滑点必须在 0% 到 1% 之间。

### ERC20 代币授权
- **在执行 ERC20 交易前**，务必检查代币的余额。
- 如果余额不足，请引导用户先批准代币。
- **绝对** 不要批准超过最大允许的数量（`MaxUint256 / 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff`），除非用户明确要求。
- spender 地址为报价响应中的 `transactionRequest.to`。

### 交易信息展示
- **始终** 在返回 `transactionRequest` 数据之前，提供人类可读的概要信息。
- 概要应包括：交易的代币和数量、使用的路径/桥接服务、预计费用、预计时间、滑点设置。
- **绝对** 不要直接返回原始的交易数据。

### 跨链安全注意事项
- 跨链交易是**非原子性操作**——资金可能在传输过程中需要几分钟到几小时。
- 提交来源链交易后，务必提供转账状态的跟踪服务。
- 如果交易状态显示为 `PARTIAL`，说明用户收到了桥接后的代币，但尚未收到最终目标代币。

### 无交易路径的情况
- 如果报价返回无可用路径，建议用户尝试其他代币、减少数量或更换目标链对。

---

## 错误处理

| 错误类型 | 原因 | 处理方式 |
|-------|-------|--------|
| HTTP 429 | 请求速率受限 | 等待 30 秒后重试，采用指数级退避策略（30 秒 → 60 秒 → 120 秒）。建议用户设置 `LIFI_API_KEY` 以提高请求速率。 |
| 未找到交易路径 | 无法找到合适的交易路径或数量不合适 | 检查 `/v1/connections` 以确认可用路径。建议更换代币、调整数量或目标链。 |
| 滑点错误 | 价格变动超出容忍范围 | 增加滑点（例如从 0.03 增加到 0.05）后重试，并告知用户可能的影响。 |
| 资金不足 | 钱包余额不足 | 告知用户余额不足，并建议用户使用代理钱包工具检查余额。 |
| 交易被撤销 | 价格变动、流动性不足或燃气费用过低 | 解释可能的原因，并建议用户尝试提高滑点或增加燃气费用后重试。 |
| 交易部分完成 | 桥接服务已发送代币，但未完成最终交易 | 用户可以在目标链上手动完成剩余交易或尝试重新操作。 |
| 交易失败 | 转移失败，资金已退还 | 确认资金已退还，并建议用户尝试其他桥接服务。 |
| 地址无效 | 地址格式错误 | 确认地址格式正确（以 `0x` 开头，共 42 个十六进制字符）。 |

---

## 链路快速参考

| 链路 | ID | 原生代币 |
|-------|----|-------------|
| 以太坊 | 1 | ETH |
| Polygon | 137 | MATIC |
| Arbitrum One | 42161 | ETH |
| Optimism | 10 | ETH |
| BSC | 56 | BNB |
| Base | 8453 | ETH |
| Avalanche | 43114 | AVAX |
| Fantom | 250 | FTM |
| zkSync Era | 324 | ETH |
| Gnosis | 100 | xDAI |
| Scroll | 534352 | ETH |
| Linea | 59144 | ETH |
| Blast | 81457 | ETH |
| Mode | 34443 | ETH |
| Solana | 1151111081099710 | SOL |

如需查看所有支持的区块链列表，请调用 `GET /v1/chains`。

所有 EVM 链路上的原生代币地址：`0x000000000000000000000000000000000000000`
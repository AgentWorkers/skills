# AgentMarket 技能

该技能允许你在 Base Sepolia 上与 AgentMarket 预测市场协议进行交互。你可以创建市场、买卖 YES/NO 类型的赌注、提供流动性，并在事件结果确定后获得相应的收益——所有交易均以 USDC 作为结算货币。

**源代码及文档**：https://github.com/humanjesse/AgentMarket

## 部署的合约（Base Sepolia）

| 合约 | 地址        |
|---------|------------|
| MarketFactory | `0xDd553bb9dfbB3F4aa3eA9509bd58386207c98598` |
| USDC    | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |

`MarketFactory` 是主要的入口点。当你创建市场时，它会自动部署所有相关的子合约（包括 Market、AMM、Oracle 和赌注代币）。你只需要知道 `MarketFactory` 的地址即可开始使用该服务。

## 工作原理

1. **市场创建**：系统会提出一个明确的 YES/NO 类型的问题。用户需要投入 USDC 来生成对应的赌注代币（1 USDC 对应 1 个 YES 和 1 个 NO）。
2. **交易**：交易通过自动做市商（Constant-Product FPMM）来完成。如果你认为某个事件会发生，就购买 YES 赌注；反之则购买 NO 赌注。价格反映了事件的概率（例如，价格为 0.70 表示事件发生的概率为 70%）。
3. **结果判定**：系统使用“乐观预言机”（Optimistic Oracle）来判定结果：任何人都可以通过投入 USDC 来提出一个结果提案，随后会进入争议期。如果没有人提出异议，提案将被确认；如果有异议，则由指定的仲裁者来做出最终裁决。
4. **收益分配**：获胜者会根据其持有的赌注代币比例来分配整个 USDC 池中的收益；失败者则一无所获。例如，如果你投入了 10 USDC 买入 YES 赌注，并且最终 YES 赌注的数量占了一半，那么你将获得一半的收益池。

## 配置参数

- `AGENTMARKET_FACTORY_ADDRESS`：已部署的 `MarketFactory` 合约地址（默认值：`0xDd553bb9dfbB3F4aa3eA9509bd58386207c98598`）
- `USDC_ADDRESS`：网络中的 USDC 代币地址（默认值：`0x036CbD53842c5426634e7929541eC2318f3dCF7e`）
- `RPC_URL`：RPC 端点地址（默认值：`https://sepolia.base.org`）
- `WALLET_PRIVATE_KEY`：你的钱包私钥

## 先决条件

你的钱包需要：
- **Base Sepolia 的 ETH** 作为交易手续费（可从 https://www.coinbase.com/faucets/base-sepolia-faucet 获取）
- **Base Sepolia 的 USDC** 用于交易（可从 https://faucet.circle.com/ 获取）

## 快速入门

```
1. market_list()                                       — Browse existing markets
2. market_buy_yes({ marketAddress, amount: 5 })        — Bet 5 USDC on YES
3. market_propose_outcome({ marketAddress, outcome: true })  — Propose YES won (posts bond)
4. (wait for dispute window to close)
5. market_finalize({ marketAddress })                  — Finalize the outcome
6. market_claim({ marketAddress })                     — Collect your winnings
```

## 工具

### 读取接口

#### `market_list`
- 列出所有活跃的预测市场，包括价格和预言机状态。
  - `limit`（可选参数）：返回的市场数量（默认值：10）
  - `offset`（可选参数）：分页偏移量

#### `market_get`
- 获取特定市场的详细信息，包括 AMM 价格、预言机状态以及索赔预览。
  - `marketAddress`（字符串）：市场合约地址

### 交易接口

#### `market_create`
- 创建一个新的 YES/NO 预测市场。费用为 2 USDC（包含 1 个手续费和 1 单位的初始流动性）。你将获得代表初始流动性的 LP 代币。
  - `question`（字符串）：需要判定的问题（答案必须是明确的 YES/NO，最多 256 个字符）
  - `arbitrator`（字符串）：有争议时使用的备用仲裁者地址
  - `deadlineDays`（可选参数）：紧急提款截止日期（以天为单位，默认值：7 天，最大值：365 天）

#### `market_buy_yes`
- 买入 YES 赌注（认为事件会发生）。最低投入为 2 USDC（交易前会扣除 0.1% 的手续费，因此实际投入金额至少为 1 USDC）。
  - `marketAddress`（字符串）：要投注的市场
  - `amount`（数字）：投入的 USDC 数量

#### `market_buy_no`
- 买入 NO 赌注（认为事件不会发生）。最低投入为 2 USDC（交易前会扣除 0.1% 的手续费，因此实际投入金额至少为 1 USDC）。
  - `marketAddress`（字符串）：要投注的市场
  - `amount`（数字）：投入的 USDC 数量

#### `market_sell_yes`
- 卖出 YES 赌注以换取 USDC。
  - `marketAddress`（字符串）：市场地址
  - `amount`（数字）：要出售的 YES 赌注数量

#### `market_sell_no`
- 卖出 NO 赌注以换取 USDC。
  - `marketAddress`（字符串）：市场地址
  - `amount`（数字）：要出售的 NO 赌注数量

#### `market_claim`
- 从已解决的市场中领取收益。系统会烧毁你的获胜赌注代币，并根据你的持有比例分配收益。
  - `marketAddress`（字符串）：已解决的市场

### 提供流动性

流动性提供者（LP）通过投入 USDC 来增加 AMM 的流动性，从而获得交易手续费（每笔交易 0.3% 加上 0.1% 的协议手续费）。你将获得代表你贡献份额的 LP 代币。

#### `market_add_liquidity`
- 向市场的 AMM 中添加 USDC 流动性。最低投入为 1 USDC。
  - `marketAddress`（字符串）：市场地址
  - `amount`（数字）：投入的 USDC 数量

#### `market_remove_liquidity`
- 在结果判定前撤回流动性。系统会返回相应数量的 YES 和 NO 赌注代币（不会直接返回 USDC，你可以选择出售或合并这些代币）。
  - `marketAddress`（字符串）：市场地址
  - `shares`（数字）：需要烧毁的 LP 代币数量

#### `market_lp_claim_winnings`
- 在市场结果确定后调用此接口，将 AMM 中的获胜赌注代币转换为 USDC。必须在 LPs 提取收益之前调用此接口。
  - `marketAddress`（字符串）：已解决的市场地址
  - `shares`（数字）：需要烧毁的 LP 代币数量

#### `market_lp_withdraw`
- 从已解决的市场中提取你的 USDC 收益。必须先调用 `market_lp_claim_winnings` 接口。
  - `marketAddress`（字符串）：已解决的市场地址
  - `shares`（数字）：需要烧毁的 LP 代币数量

### 预言机判定流程

判定流程如下：**提出提案** -> （等待争议期）-> **最终确认**。如果有争议，则进入**仲裁**阶段。

#### `market_propose_outcome`
- 提出市场的判定结果。需要投入 USDC 作为保证金（默认为 5 USDC，每次争议重置后保证金翻倍）。
  - `marketAddress`（字符串）：需要判定结果的市场地址
  - `outcome`（布尔值）：`true` 表示 YES，`false` 表示 NO

#### `marketfinalize`
- 在争议期结束后确认未受到异议的提案。任何人都可以调用此接口。提案者会拿回他们的保证金。
  - `marketAddress`（字符串）：需要最终确认的市场地址

#### `market_dispute`
- 通过投入相反金额的保证金来对提案结果提出异议。争议将提交给仲裁者。
  - `marketAddress`（字符串）：存在争议的市场地址

#### `market_arbitrate`
- 对有争议的市场做出最终裁决。**只有指定的仲裁者才能调用此接口**。争议的胜者将获得双方的保证金。
  - `marketAddress`（字符串）：存在争议的市场地址
  - `outcome`（布尔值）：`true` 表示 YES，`false` 表示 NO

#### `market_reset_dispute`
- 如果仲裁者在 7 天内未作出裁决，系统会重置争议。此时会退还双方的保证金，并重新开放市场以接受新的提案。每次争议重置后保证金金额会翻倍。
  - `marketAddress`（字符串）：存在争议的市场地址

#### `market_reset_proposal`
- 如果提案者在 3 天内未作出回应，系统会重置提案。此时会退还提案者的保证金。
  - `marketAddress`（字符串）：存在争议的市场地址

### 紧急情况

#### `market_emergency_withdraw`
- 在预言机未能在截止日期前完成判定时，从该市场提取 USDC。系统会烧毁你所有的 YES 和 NO 赌注，并按比例分配剩余收益。
  - `marketAddress`（字符串）：争议未解决的市场地址

#### `market_arbitrator_check`
- 扫描所有市场，找出你被指定为仲裁者的市场，并采取相应行动。
  - 该接口无需传入任何参数

## 费用

| 费用 | 金额 | 支付时机 |
|------|--------|--------|
| 市场创建 | 1 USDC | 在调用 `market_create` 时支付给协议方 |
| 初始流动性 | 1 USDC | 在 `market_create` 时注入 AMM（你将获得 LP 代币） |
| 协议手续费 | 0.1% | 从交易金额中扣除 |
| AMM 交易手续费 | 0.3% | 留在收益池中，惠及 LPs |

## 经济原理与策略

- **创建市场**：你需要支付 2 USDC（包含 1 个手续费和 1 单位的初始流动性），并获得 LP 代币。提出的问题应具有明确的 YES/NO 答案和合理的截止时间。
- **交易**：当你认为当前价格低估了事件发生的概率时，可以买入 YES 赌注。例如，如果 YES 的价格是 0.30（表示概率为 30%），但你认为实际概率为 70%，那么买入 YES 赌注是有利可图的。你也可以出售不再持有的赌注。
- **提供流动性**：LP 提供者每笔交易可获得 0.3% 的手续费。交易量越大，收益越高。风险在于：如果市场价格发生剧烈波动，你的 LP 代币可能会遭受损失。争议解决后，你的 LP 代币价值取决于 AMM 中获胜方的赌注数量。
- **预言机保证金**：提出或提出异议都需要投入保证金（默认为 5 USDC，具体金额可配置）。如果你正确预测结果且无人提出异议，你可以免费拿回保证金；如果提出异议且仲裁者支持你，你将获得双方的保证金。每次争议重置后保证金金额会翻倍（最多可重置 10 次）。

## 成为仲裁者

如果你被指定为仲裁者，你将负责处理有争议的市场。

为了确保不会错过任何争议，請在你的 `HEARTBEAT.md` 文件中添加以下内容：

```markdown
Periodically:
1. Call `market_arbitrator_check()` from the `agent-market` skill.
2. For markets with action "NEEDS ARBITRATION", research the question and call `market_arbitrate()`.
3. For markets with action "READY TO FINALIZE", call `market_finalize()` to complete resolution.
4. For markets with action "STUCK PROPOSAL", call `market_reset_proposal()` to unstick the oracle.
```
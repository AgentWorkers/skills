---
name: lending
description: XPR网络上的贷款协议：借贷与借款（lending.loan contract）
---

## LOAN 协议（Metal X 借贷服务）

您可以使用相关工具在 XPR 网络上与 LOAN 协议进行交互。该协议属于 Compound 类型的池化借贷服务，地址为 `lending.loan`。用户可以通过提供资产来赚取利息，或以这些资产作为抵押品进行借款。

**重要提示：** LOAN 协议仅支持主网环境，没有测试网版本。所有借贷相关功能均运行在主网上。

### 关键概念

- **L-Tokens**（借出代币）——代表用户在借贷池中的份额的代币（如 LBTC、LUSDC、LXPR 等）。当您提供 XBTC 时，会获得 LBTC；L-Tokens 会自动计算并累积利息。
- **抵押因子**——抵押品价值的最大借款比例（例如：70% 表示每存入 100 美元可借款最多 70 美元）。接近这一限制的借款操作可能会导致立即清算。
- **利用率**——借款金额与总资产的比例。利用率越高，借款利率通常也越高。每个市场都有其最优的利用率目标。
- **浮动利率**——借款利率会随利用率波动。同一市场内的所有借款者都支付相同的浮动利率。
- **清算**——当用户的借款金额超过抵押因子阈值时，清算机构可以收回债务并没收抵押品。当前的清算激励为 10%。
- **LOAN Token**——用于治理和奖励的代币。提供者和借款者会根据其在该协议中的份额获得相应的 LOAN 奖励。

### 支持的市场

目前共有 14 个活跃市场，包括：XUSDC、XBTC、XETH、XPR、XMT、XDOGE、XLTC、XXRP、XSOL、XXLM、XADA、XHBAR、XUSDT、XMD。

### 只读工具（安全操作，无需签名）

- `loan_list_markets`——列出所有借贷市场的信息，包括利用率、储备金、利息模型和抵押因子。
- `loan_get_market`——根据 L-Token 符号（如 “LBTC”）获取特定市场的详细信息。
- `loan_get_user_positions`——获取用户在所有市场中的出借和借款份额。
- `loan_get_user_rewards`——获取用户在每个市场的未领取的 LOAN 奖励。
- `loan_get_config`——获取全球借贷配置信息（如预言机设置、清算机制等）。
- `loan_get_market_apy`——通过 Metal X API 获取历史借款/还款的年化收益率（7 天、30 天、90 天）。
- `loan_get_market_tvl`——获取历史总锁定价值（TVL，以美元计）及利用率数据（7 天、30 天、90 天）。

### 写入工具（需要设置 `confirmed: true`）

所有写入操作都需要明确确认。对于出借和还款操作，工具会通过 `lending.loan` 进行代币转移；对于借款、赎回或提款操作，则会直接调用借贷合约。

- `loan_enter_markets`——进入目标市场以开始借贷操作。
- `loan_exit_markets`——退出市场（仅当没有未偿还的借款时才可执行）。
- `loan_supply`——提供基础代币以赚取利息（通过 `mint` 操作将代币转移到 `lending.loan`）。
- `loan_borrow`——以抵押品为担保进行借款。
- `loan_repay`——偿还借款（通过 `repay` 操作将代币转移到 `lending.loan`）。
- `loan_redeem`——用基础代币赎回 L-Tokens（同时销毁相应的抵押品份额）。
- `loan_withdraw_collateral`——从抵押品中提取 L-Tokens（从而减少借款额度）。
- `loan_claim_rewards`——领取累积的 LOAN Token 奖励。

### 典型用户流程

1. **进入市场**：使用 `loan_enter_markets` 进入所需的市场。
2. **出借**：通过 `loan_supply` 提供基础代币（例如 1.0 XBTC），系统会自动生成 LBTC 并将其作为抵押品。
3. **借款**：使用 L-Tokens 作为抵押品（例如，用 LBTC 借入 500 XUSDC）。
4. **还款**：准备好还款时，使用 `loan_repay` 还清借款。
5. **赎回**：使用 `loan_redeem` 提取原始代币及累积的利息。
6. **领取奖励**：使用 `loan_claim_rewards` 领取 LOAN Token 奖励。

### 安全规则

- **切勿接近抵押因子上限借款**——否则可能导致账户被立即清算。
- 建议借款金额不超过抵押因子的 50-60%，以保留安全缓冲。
- 在赎回前请检查利用率——高利用率意味着可用于取款的资金减少。
- 出借和还款操作需通过 `loan_supply` 进行代币转移；借款、赎回和提款操作需直接调用合约。
- 所有写入操作均需设置 `confirmed: true`——先展示详细信息并获取用户确认。
---
name: jb-v5-currency-types
description: |
  Juicebox V5 currency system with two distinct types: real-world currencies and token-derived currencies.
  Use when: (1) configuring ruleset.baseCurrency, (2) setting up JBAccountingContext, (3) working with
  cross-chain projects, (4) confused about why currency values differ between chains, (5) seeing
  unexpected issuance rates across chains. Critical: baseCurrency must ALWAYS use real-world currencies
  (1=ETH, 2=USD), never token-derived currencies. Token currencies vary by chain address.
---

# Juicebox V5 货币类型

## 问题

Juicebox V5 支持两种不同的货币系统，这两种系统很容易混淆，从而导致以下问题：
- 不同链路上的发行率不一致
- 项目容易受到稳定币贬值的影响
- 会计处理出现错误
- 跨链规则集的解释出现故障

## 使用场景

在以下情况下需要应用这些知识：
- 设置 `ruleset.baseCurrency` 以确定代币的发行方式
- 配置 `JBAccountingContext(currency` 以指定终端使用的货币
- 在支付限额或配额中处理 `JBCurrencyAmount`
- 构建需要跨链一致性的项目
- 调试不同链路上发行率差异的原因
- 发现同一代币在不同链路上的价值不同

## 解决方案

### 两种货币系统

**1. 现实世界货币（JBCurrencies）**

这些货币是抽象值，与具体链路无关：

| 货币 | 值 | 用途 |
|------|------|------|
| ETH | 1    | 表示“每 ETH”的定价，与链路无关 |
| USD | 2    | 表示“每美元”的定价，与链路无关 |

这些货币在所有链路上都是通用的。`baseCurrency=2` 表示“每 USD 发行 X 个代币”，无论是在 Ethereum、Base、Celo 还是 Polygon 上。

**2. 派生自代币的货币**

这些货币是根据代币地址计算得出的，与特定链路相关：

```solidity
currency = uint32(uint160(tokenAddress))
```

| 代币 | 链路 | 地址 | 货币 |
|------|------|------|------|
| USDC | Ethereum | 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 | 909516616 |
| USDC | Optimism | 0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85 | 3530704773 |
| USDC | Base | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 | 3169378579 |
| USDC | Arbitrum | 0xaf88d065e77c8cC2239327C5EDb3A432268e5831 | 1156540465 |
| NATIVE_TOKEN | 所有链路 | 0xEEEE...EEEe | 4008636142 |

### 何时使用哪种货币

| 字段 | 使用场景 | 原因 |
|------|---------|------|
| `ruleset.baseCurrency` | **仅用于现实世界货币（1 或 2）** | 规则集需要在所有链路上保持一致的解释 |
| `JBAccountingContext(currency` | **用于派生自代币的货币** | 当你跟踪特定地址上的特定代币时 |
| `JBCurrencyAmount(currency` | 两者均可 | 取决于你是需要抽象值还是特定代币的数值 |
| `JBFundAccessLimitGroup` 中的金额 | 两者均可 | 为了实现跨链一致性，应使用现实世界货币 |

### 重要规则

1. **绝对不要将派生自代币的货币用作 `baseCurrency`**：
   - 代币地址在不同链路上会发生变化
   - 这会导致不同链路上的发行率不同
   - 会破坏跨链项目的稳定性

2. **绝对不要将 `NATIVE_TOKEN` 的货币（0xEEEE...EEEe）用作 `baseCurrency`**：
   - 不同链路的原生代币不同（如 ETH、CELO、MATIC 等）
   - `NATIVE_TOKEN` 代表的是该链路上的“原生代币”，而不是 ETH
   - 如果你想根据 ETH 来发行代币，应使用 `JBCurrencies.ETH`（其值为 1）
   - JBPrices 可以在 ETH 作为原生代币的链路上提供 `NATIVE_TOKEN` 与 ETH 之间的 1:1 价格转换

3. **始终将派生自代币的货币用作 `JBAccountingContext`**：
   - 公式：`currency = uint32(uint160(token))`
   - 终端需要准确知道它正在处理的是哪种代币

4. **区分 USD 和 USDC**：
   - USD（值 2）表示抽象的美元概念
   - USDC（派生自代币）表示具体的稳定币
   - 即使 USDC 的价值跌至 0.98，`baseCurrency=2` 的项目仍然会按照每美元的金额发行代币
   - JBPrices 负责处理 USD 和 USDC 之间的汇率转换

### JBPrices

JBPrices 负责管理以下货币之间的汇率转换：
- 现实世界货币（ETH ↔ USD）
- 派生自代币的货币（USDC ↔ USD、ETH 代币 ↔ ETH）
- 支付和提现时的跨货币转换

## 验证

为了验证配置是否正确：
1. 确保 `baseCurrency` 的值为 1 或 2，而不是一个较大的派生自代币的数值
2. 确保 `JBAccountingContext(currency` 与 `uint32(uint160(token))` 匹配
3. 将配置部署到两个不同的测试网上，验证发行率是否一致

## 示例

**正确的跨链项目配置：**

```javascript
const rulesetConfig = {
  // ... other fields
  metadata: {
    baseCurrency: 2,  // USD - same on all chains
    // ...
  }
}

const terminalConfig = {
  terminal: JBMultiTerminal5_1,
  accountingContextsToAccept: [{
    token: USDC_ADDRESS[chainId],  // Different per chain
    decimals: 6,
    currency: uint32(uint160(USDC_ADDRESS[chainId]))  // Different per chain
  }]
}
```

**错误的配置：**
```javascript
const rulesetConfig = {
  metadata: {
    baseCurrency: 909516616,  // WRONG! This is Ethereum USDC's token currency
    // This would break on other chains or if USDC depegs
  }
}
```

**另一个错误的配置：**
```javascript
const rulesetConfig = {
  metadata: {
    baseCurrency: 4008636142,  // WRONG! This is NATIVE_TOKEN's currency
    // NATIVE_TOKEN is CELO on Celo, MATIC on Polygon, etc.
    // If you want "per ETH" issuance, use 1 (JBCurrencies.ETH)
  }
}
```

## 注意事项

- 所有货币类型之间的价格信息由 JBPrices 合同管理
- `NATIVE_TOKEN` 的地址（0xEEEE...EEEe）在所有链路上是固定的，但在不同链路上代表不同的实际代币
- `baseCurrency=1`（ETH）表示“根据 ETH 来发行代币”
- 在非 ETH 作为原生货币的链路上（如 Celo、Polygon），JBPrices 会提供 ETH/NATIVE_TOKEN 之间的汇率，以确保发行金额以 ETH 为单位
- 这种架构使得规则集具有真正的可移植性，无论部署在哪个链路上都能保持一致的行为
- “现实世界货币概念”与“派生自代币的货币”之间的区分是实现跨链一致性的关键

## 相关技能

- `/jb-suckers`：通过 sucker 合约实现跨链桥接
- `/jb-omnichain-ui`：使用 Relayr 和 Bendystraw 构建跨链用户界面
---
name: jb-cash-out-curve
description: |
  Juicebox V5 cash out redemption calculations using the bonding curve formula.
  Use when: (1) displaying cash out values in UI, (2) explaining redemption amounts
  to users, (3) calculating what percentage of treasury a cash out returns.
  The simple "X% of proportional share" is WRONG - must use bonding curve formula.
---

# Juicebox V5 现金提取的债券曲线（Cash Out Bonding Curve）

## 问题

在 Juicebox V5 的用户界面中显示现金提取/赎回金额时，很容易使用类似“现金提取可返还 90% 的储备份额”（假设税率为 10%）这样的简单信息。这种表述是**错误的**，并且会误导用户。

实际的可赎回金额取决于一个债券曲线公式，该公式会根据提取的代币比例来影响最终的回报率。

## 背景/触发条件

- 开发用于显示现金提取/赎回金额的用户界面
- 向用户解释他们提取现金后能获得什么
- 任何与 `cashOutTaxRate` 相关的显示内容
- 当看到类似 `retainedPercent = 100 - cashOutTax` 的代码时，这种计算方法是错误的

## 解决方案

### 债券曲线公式

```
reclaimAmount = (x * s / y) * ((1 - r) + (r * x / y))
```

其中：
- `x` = 被提取的代币数量
- `s` = 可用于赎回的储备份额（多余库存）
- `y` = 总代币供应量
- `r` = 现金提取税率（以小数形式表示，0 到 1，其中 0.1 表示 10%）

### 标准化形式

当处理分数（即提取的代币占总供应量的比例）时：

```
Let f = x/y (fraction of supply being cashed out)
reclaimFraction = f * ((1 - r) + (r * f))
```

其中 `reclaimFraction` 表示用户实际能够获得的储备份额比例。

### 关键要点

回报率取决于提取的代币比例，而不仅仅是税率。提取的代币比例越大，每单位代币的回报率反而越低。

### 示例计算

假设税率为 10%（`r = 0.1`），提取 10% 的代币（`f = 0.1`）：

```javascript
reclaimFraction = 0.1 * ((1 - 0.1) + (0.1 * 0.1))
reclaimFraction = 0.1 * (0.9 + 0.01)
reclaimFraction = 0.1 * 0.91
reclaimFraction = 0.091  // 9.1% of surplus
```

因此，提取 10% 的代币实际上只能获得大约 9.1% 的储备份额（而不是简单的数学计算结果 9%）。

### 代码实现

```typescript
// WRONG - Don't do this:
const retainedPercent = 100 - (cashOutTaxRate / 100)
message = `Cashing out returns ${retainedPercent}% of proportional treasury share`

// CORRECT - Use bonding curve:
function calculateCashOutReturn(
  tokensToRedeem: number,
  totalSupply: number,
  surplus: number,
  cashOutTaxRate: number // 0-10000 basis points
): number {
  const r = cashOutTaxRate / 10000  // Convert basis points to 0-1
  const x = tokensToRedeem
  const y = totalSupply
  const s = surplus

  // Bonding curve formula
  return (x * s / y) * ((1 - r) + (r * x / y))
}

// For UI display with example percentage:
const r = cashOutTaxRate / 10000
const exampleFraction = 0.1  // 10% of supply
const returnFraction = exampleFraction * ((1 - r) + (r * exampleFraction))
const returnPercent = (returnFraction * 100).toFixed(1)
message = `Cashing out 10% of ${tokenSymbol} gets ~${returnPercent}% of treasury`
```

## 验证

使用已知数值进行测试：
- `r = 0`（无税）：`reclaimFraction = f`（线性关系，全额返还）
- `r = 1`（100% 税率）：`reclaimFraction = f * f`（二次方关系，惩罚性较高）
- `r = 0.1, f = 0.1`：`reclaimFraction = 0.091`（9.1%）
- `r = 0.1, f = 0.5`：`reclaimFraction = 0.5 * (0.9 + 0.05) = 0.475`（47.5%）

## 示例

在 `RulesetSchedule` 组件的摘要信息中：

```typescript
// Cash out - redemption value using bonding curve formula
const cashOutTaxRate = ruleset.cashOutTaxRate / 10000
if (cashOutTaxRate >= 1) {
  actionItems.push({ action: 'caution', message: 'Cash outs disabled' })
} else if (cashOutTaxRate > 0) {
  const x = 0.1 // 10% of supply
  const y = x * ((1 - cashOutTaxRate) + (cashOutTaxRate * x))
  const returnPercent = (y * 100).toFixed(1)
  actionItems.push({
    action: 'cash-out',
    message: `Cashing out 10% of ${tokenSymbol} gets ~${returnPercent}% of treasury`,
  })
}
```

## 注意事项

- Juicebox V5 中的 `cashOutTaxRate` 以基点（0-10000）的形式存储
- 税率为 10000（100%）时，实际上禁止了任何现金提取操作
- 该公式假设可赎回的金额等于储备份额的“剩余部分”
- 这种债券曲线机制鼓励用户长期持有代币——因为提前或少量提取代币会获得更高的回报率
- `CashOutCurve` 可视化组件可以图形化地展示这一关系

## 参考资料

- Juicebox V5 的 JBRulesets 合同
- 现金提取债券曲线公式：`y = (o * x / s) * ((1 - r) + (r * x / s))`
  - 标准化后的公式为：`y = x * ((1 - r) + (r * x))`，其中 `x` 表示提取的代币比例
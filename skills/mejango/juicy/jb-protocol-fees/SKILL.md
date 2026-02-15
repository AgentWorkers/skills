---
name: jb-protocol-fees
description: |
  Juicebox V5 and Revnet protocol fee structures and UI integration patterns.
  Use when: (1) implementing payout limits with fee calculations, (2) building cash out/redeem UIs,
  (3) building loan interfaces for revnets, (4) displaying fee breakdowns to users,
  (5) calculating net amounts after fees, (6) adding custom UI fees on top of protocol fees.
  Covers the 2.5% NANA fee, 2.5% Revnet cash out fee, 1% REV loan fee, and variable loan fees.
---

# Juicebox V5 与 Revnet 协议费用

本文档全面介绍了协议费用的相关信息，以及用户界面（UI）应如何正确处理这些费用。

## 问题

Juicebox V5 和 Revnet 有多种费用类型，用户界面需要准确计算并显示这些费用：
- NANA 协议的支付费用为 2.5%
- Revnet 协议的提现费用为 2.5%
- Revnet 协议的贷款费用为 1% + 2.5%
- 贷款费用会随时间变化（具有浮动性）

用户界面需要向用户显示准确的净金额，并提供透明的费用明细。

## 费用结构概述

| 费用 | 费率 | 来源合约 | 收费方 |
|-----|------|-----------------|-----------|
| NANA 支付费用 | 2.5% | `JBMultiTerminal.sol:86` | Project #1 (JBX) |
| Revnet 提现费用 | 2.5% | `REVDeployer.sol:95` | REV revnet |
| REV 贷款费用 | 1% | `REVLoans.sol:89` | REV revnet |
| 来源贷款费用 | 2.5%-50% | `REVLoans.sol:92` | 来源 revnet |
| 变动贷款费用 | 0-100% | `REVLoans.sol:377-403` | 来源 revnet |

---

## 1. NANA 费用（2.5%）

### 合约定义

**文件：`nana-core-v5/src/JBMultiTerminal.sol:86`**

### 费用适用场景

- 向钱包地址的支付（非 Juicebox 项目）
- 向分账挂钩（split hooks）的支付
- 使用剩余金额时的费用

### 费用不适用场景

- 向其他 Juicebox 项目的支付（项目间转账免费）
- 免费账户（由 `JBFeelessAddresses` 合约管理）
- 提现税率为 100% 的情况（`cashOutTaxRate == 0`）

### 费用计算库

**文件：`nana-core-v5/src/libraries/JBFees.sol`

### 用户界面实现（juice-interface）

**文件：`juice-interface/src/packages/v4/utils/distributions.ts`

### 用户界面显示方式

在支付金额上显示费用提示：
> “向以太坊地址支付时会产生 2.5% 的费用。您的项目将收到 JBX 作为回报。”

---

## 2. Revnet 提现费用（2.5%）

### 合约定义

**文件：`revnet-core-v5/src/REVDeployer.sol:95`**

### 工作原理

1. 用户发起 X 代币的提现操作。
2. 2.5% 的代币（X * 0.025）会被转交给 REV revnet。
3. 用户会收到剩余的 97.5% 代币作为回报。
4. 剩余的代币将用于兑换实际资产。

### 免费情况

- **Suckers**（跨链桥接合约）无需支付提现费用（详见 `REVDeployer.sol:282-283`）

### 用户界面实现（revnet-app）

**文件：`revnet-app/src/lib/feeHelpers.ts`

### 费用叠加规则

在提现时，需要同时收取这两种费用。

### 用户界面显示方式

直接显示净金额，并注明已扣除的费用。

---

## 3. Revnet 贷款费用

### 合约定义

**文件：`revnet-core-v5/src/REVLoans.sol:83-92`

### 费用构成

| 费用 | 费率 | 收费时间 | 收费方 |
|-----|------|--------------|-----------|
| REV 费用 | 1% | 借款时 | REV revnet |
| 来源费用 | 2.5%-50% | 借款时（预先支付） | 来源 revnet |
| 变动费用 | 0-100% | 预付期结束后 | 来源 revnet |

### 预付费机制

- 用户可以选择预付费比例（2.5% 至 50%）。
- 预付费比例越高，免费期越长。
- 预付费期 = `(预付费比例 / 50%) * 10 年`。

**示例：**
- 预付费 2.5% → 免费期 6 个月
- 预付费 25% → 免费期 5 年
- 预付费 50% → 免费期 10 年（此后费用固定为 2.5%）

### 变动费用计算

**文件：`revnet-core-v5/src/REVLoans.sol:377-403`

**费用变化规则**

预付费期结束后，费用会从 0% 线性增加到 100%。

### 用户界面实现（revnet-app）

**文件：`revnet-app/src/lib/feeHelpers.ts`

### 用户界面显示方式

- `SimulatedLoanCard` 组件会以内联方式显示费用明细。
- `LoanFeeChart` 组件会可视化费用曲线：
  - X 轴：时间（0-10 年）
  - Y 轴：解锁抵押品的总成本
  - 滑块：预付费比例（2.5%-50%）

---

## 4. 自定义用户界面费用

用户界面可以根据需要添加额外的费用。

**最佳实践：**
1. 保持透明——向用户展示全部费用明细。
2. 在协议费用之外再收取用户界面费用（仅针对剩余金额）。
3. 将用户界面费用收取到运营者的账户。
4. 分别显示费用：`协议费用：2.5% | 平台费用：0.5%`

---

## 5. 费用显示最佳实践

### 支付表格（juice-interface）

### 提现预览

### 贷款概览

---

## 关键源文件

### 合约

| 文件 | 用途 |
|------|---------|
| `nana-core-v5/src/JBMultiTerminal.sol` | NANA 费用逻辑 |
| `nana-core-v5/src/libraries/JBFees.sol` | 费用计算库 |
| `nana-core-v5/src/JBFeelessAddresses.sol` | 免费账户管理 |
| `revnet-core-v5/src/REVDeployer.sol` | 提现费用 |
| `revnet-core-v5/src/REVLoans.sol` | 贷款费用 |

### 用户界面实现

| 文件 | 用途 |
|------|---------|
| `juice-interface/src/packages/v4/utils/distributions.ts` | 支付费用计算 |
| `juice-interface/src/packages/v4/components/FeeTooltipLabel.tsx` | 费用显示组件 |
| `revnet-app/src/lib/feeHelpers.ts` | Revnet 费用辅助功能 |
| `revnet-app/src/app/[slug]/components/Value/SimulatedLoanCard.tsx` | 贷款费用显示 |
| `revnet-app/src/app/[slug]/components/Value/LoanFeeChart.tsx` | 费用曲线可视化 |

---

## 需避免的常见错误

1. **忘记检查项目类型**：在收取费用前务必使用 `isJuiceboxProjectSplit()` 函数判断项目类型。
2. **重复收费**：协议费用已在链上收取，用户界面不应再次收费。
3. **忽略 NANA 提现费用**：提现时需要同时支付 Revnet 和 NANA 费用。
4. **显示总额而非净金额**：用户关心的是实际收到的金额。
5. **遗漏变动贷款费用**：贷款费用会在预付费期后逐渐增加。

## 验证方法

为确保费用计算与链上行为一致，请执行以下操作：
1. 将用户界面显示的金额与实际交易结果进行对比。
2. 使用免费账户进行测试，确认费用免除规则正确生效。
3. 验证贷款费用曲线是否与合约中的 `_determineSourceFeeAmount()` 逻辑一致。
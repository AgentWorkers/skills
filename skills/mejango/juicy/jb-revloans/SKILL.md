---
name: jb-revloans
description: |
  REVLoans contract mechanics for Juicebox V5 revnets. Use when: (1) implementing loan
  borrow/repay/refinance flows, (2) calculating loan fees and prepaid amounts, (3) understanding
  collateral burn/remint mechanics, (4) building loan-related UIs, (5) explaining loan solvency.
  Covers borrowFrom, repayLoan, reallocateCollateralFromLoan, and liquidation mechanics.
---

# REVLoans 合同机制

## 问题

为 revnets 构建贷款功能需要理解 REVLoans 合同的具体机制：抵押品如何运作（销毁还是锁定）、费用结构，以及借款、还款和再融资的流程。

## 背景/触发条件

- 在 revnet 用户界面中实现借款流程
- 构建还款或再融资功能
- 向用户解释贷款费用的计算方式
- 计算预付费用金额
- 理解抵押品机制（为什么抵押品会被销毁而不是被锁定）
- 实现清算检测功能

## 解决方案

### 合同常量

```solidity
// Liquidation timeline
uint256 constant LOAN_LIQUIDATION_DURATION = 3650 days  // 10 years

// Prepaid fee bounds (basis points)
uint256 constant MIN_PREPAID_FEE_PERCENT = 25   // 0.25% minimum (6 months)
uint256 constant MAX_PREPAID_FEE_PERCENT = 500  // 5% maximum (10 years)

// REV protocol fee on prepaid amount
uint256 constant REV_PREPAID_FEE_PERCENT = 10   // 0.1% to REV
```

### 费用结构

当发生贷款时：

1. **预付费用**（2.5% - 50%）：提前支付，用于覆盖预付期间的利息
2. **REV 费用**（0.1%）：从预付金额中提取，支付给 REV 协议
3. **内部费用**（2.5%）：作为收入重新加入资金库

```
Total Fee = prepaidFee + revFee
Net to Borrower = borrowAmount - prepaidFee - revFee
Treasury Impact = -borrowAmount + internalFee
```

### 关键函数

#### borrowFrom - 借款

```solidity
function borrowFrom(
    uint256 projectId,
    address terminal,
    address token,
    uint256 amount,           // Amount to borrow (in base token)
    uint256 collateral,       // Tokens to lock as collateral
    address beneficiary,      // Who receives borrowed funds
    uint256 prepaidFeePercent // Fee percent (25-500 basis points)
) external returns (uint256 loanId)
```

**抵押品机制：**
- 抵押品代币在贷款发放时会被**销毁**，而不是被锁定
- 这是关键点：贷款的担保是基于还款时重新铸造代币的权利
- 抵押品的销毁会提高所有剩余持有者的代币价格

#### repayLoan - 还款并解锁抵押品

```solidity
function repayLoan(
    uint256 loanId,
    uint256 collateralToReturn, // Portion of collateral to unlock
    address beneficiary         // Who receives the unlocked tokens
) external payable
```

**还款机制：**
- 可以部分还款（返还部分抵押品）
- 代币会根据比例重新铸造给受益人
- 还款金额 = 原始借款金额的比例

```
repaymentRequired = (collateralToReturn / totalCollateral) * borrowAmount
```

#### reallocateCollateralFromLoan - 再融资

```solidity
function reallocateCollateralFromLoan(
    uint256 loanId,
    uint256 collateralToReallocate, // Collateral to move
    uint256 minBorrowAmount,        // Min additional borrow (slippage)
    address beneficiary,            // Who receives new funds
    uint256 newPrepaidFeePercent    // New prepaid duration
) external returns (uint256 newLoanId)
```

**再融资机制：**
- 从增值的抵押品中提取价值
- 原始贷款的抵押品部分或全部转移到新贷款中
- “可用额度” = 可借款金额 - 当前债务

```typescript
// Calculate headroom
const borrowableNow = revLoans.borrowableAmountFrom(projectId, collateral, ...)
const headroom = borrowableNow - originalBorrowAmount
// If headroom > 0, can refinance to extract the difference
```

#### liquidateExpiredLoansFrom - 清算旧贷款

```solidity
function liquidateExpiredLoansFrom(
    uint256 projectId,
    uint256[] calldata loanIds,
    address payable beneficiary
) external
```

**清算机制：**
- 仅在 `LOAN_LIQUIDATION_DURATION`（10 年）之后才能触发清算
- 抵押品会被永久销毁（已经被销毁了，无法取回）
- 原始借款金额已经取出

### 计算可借款金额

可借款金额取决于抵押品的当前现金价值：

```typescript
// On-chain: REVLoans.borrowableAmountFrom()
function borrowableAmountFrom(
    uint256 projectId,
    uint256 collateral,      // Token amount as collateral
    uint256 decimals,        // Token decimals (18 for ETH)
    uint256 currency         // 1 = ETH, 2 = USDC
) external view returns (uint256)

// The borrowable amount ≈ cash-out value of collateral
// Uses bonding curve formula internally
```

### 贷款状态跟踪

每笔贷款都是一个 ERC-721 NFT，具有以下状态：

```solidity
struct REVLoan {
    uint256 projectId;
    uint256 collateral;       // Remaining collateral
    uint256 borrowAmount;     // Original borrow amount
    uint256 prepaidDuration;  // Seconds of prepaid time remaining
    uint256 prepaidFeePercent;
    uint256 createdAt;        // Timestamp
    address terminal;
    address token;
    string tokenUri;
}
```

### 偿付能力保证

根据学术白皮书：

> “无论贷款的数量、规模或是否违约，revnet 都能保持偿付能力。”

这是因为：
1. 抵押品在贷款发放时会被销毁（减少了市场供应）
2. 借款金额 ≤ 被销毁抵押品的现金价值
3. 资金库的储备从未低于零

### 用户界面实现模式

```typescript
// BorrowDialog flow
function BorrowDialog({ projectId, userBalance }) {
  const [collateral, setCollateral] = useState(0n)

  // Get borrowable amount for selected collateral
  const { data: borrowable } = useReadContract({
    address: REVLOANS_ADDRESS,
    abi: revLoansAbi,
    functionName: 'borrowableAmountFrom',
    args: [projectId, collateral, 18, 1],
  })

  // Calculate fees
  const prepaidFeePercent = 250 // 2.5% = 6 months
  const prepaidFee = (borrowable * BigInt(prepaidFeePercent)) / 10000n
  const revFee = (prepaidFee * 10n) / 10000n // 0.1%
  const netReceived = borrowable - prepaidFee - revFee

  // Execute borrow
  const { write: borrow } = useContractWrite({
    address: REVLOANS_ADDRESS,
    abi: revLoansAbi,
    functionName: 'borrowFrom',
    args: [projectId, terminal, token, borrowable, collateral, beneficiary, prepaidFeePercent],
  })

  return (
    <Dialog>
      <CollateralInput value={collateral} max={userBalance} onChange={setCollateral} />
      <BorrowableDisplay amount={borrowable} />
      <FeeBreakdown prepaid={prepaidFee} rev={revFee} net={netReceived} />
      <Button onClick={() => borrow()}>Borrow</Button>
    </Dialog>
  )
}
```

## 验证

1. 检查 `loanOf(loanId)` 在借款后返回正确的状态
2. 验证 `borrowableAmountFrom` 是否与预期的现金价值相符
3. 测试部分还款是否能正确返回相应的抵押品
4. 确认再融资能正确提取可借款金额

## 示例

完整的借款交易流程：

```typescript
import { revLoansAbi } from '@/abi/revLoans'

async function borrowFromRevnet(
  wallet: WalletClient,
  params: {
    projectId: bigint
    terminal: Address
    token: Address
    collateral: bigint
    prepaidMonths: number // 6-120 months
  }
) {
  // Calculate prepaid fee percent (25 BPS = 6 months, 500 BPS = 10 years)
  const prepaidFeePercent = Math.min(
    500,
    Math.max(25, Math.floor(params.prepaidMonths / 6 * 25))
  )

  // Get borrowable amount
  const borrowable = await revLoans.read.borrowableAmountFrom([
    params.projectId,
    params.collateral,
    18n,
    1n
  ])

  // Execute borrow
  const txHash = await wallet.writeContract({
    address: REVLOANS_ADDRESS,
    abi: revLoansAbi,
    functionName: 'borrowFrom',
    args: [
      params.projectId,
      params.terminal,
      params.token,
      borrowable,
      params.collateral,
      wallet.account.address, // beneficiary
      BigInt(prepaidFeePercent)
    ]
  })

  return txHash
}
```

## 注意事项

- 贷款是非托管的：除了借款人外，任何人都无法取走抵押品（直到清算）
- 抵押品的销毁使得贷款具有“自我清算”功能
- 10 年的清算期限非常长——大多数 DeFi 贷款的清算速度要快得多
- 预付费用按比例计算：6 个月内为 2.5%，10 年内为 5%
- 预付期后的利息为年利率 5%，加到还款金额中
- 多链支持：贷款存在于特定链上，不能跨链转移

## 参考资料

- [REVLoans.sol](https://github.com/rev-net/revnet-core-v5/blob/main/src/REVLoans.sol)
- [useBorrowDialog.tsx](https://github.com/rev-net/revnet-app/blob/main/src/app/[slug]/components/Value/hooks/useBorrowDialog.tsx)
- 白皮书：“Revnets 的密码经济学” - 关于贷款偿付能力的部分
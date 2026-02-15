---
name: jb-loan-queries
description: |
  Query REVLoans data via Bendystraw GraphQL. Use when: (1) displaying a user's loans
  across all revnets, (2) showing all loans for a specific revnet/project, (3) checking
  borrow permissions, (4) building loan management UIs. Covers LoansByAccount query,
  permission checking, and multi-chain loan aggregation.
---

# 通过 Bendystraw 查询 REVLoans

## 问题

在 revnet 用户界面中显示贷款信息，需要使用正确的 GraphQL 查询来访问 Bendystraw 的 API，并了解如何跨链和项目筛选/汇总贷款数据。

## 背景/触发条件

- 构建用户界面以显示用户的未偿还贷款
- 显示特定 revnet 的所有贷款信息
- 检查用户是否有借款权限
- 计算贷款的可用额度（可再融资金额）
- 多链贷款数据的汇总

## 解决方案

### GraphQL 查询

#### 获取用户的全部贷款信息

```graphql
query LoansByAccount($owner: String!, $version: Int!) {
  loans(where: { owner: $owner, version: $version }) {
    items {
      borrowAmount
      collateral
      prepaidDuration
      projectId
      terminal
      token
      chainId
      createdAt
      id
      project {
        version
      }
    }
  }
}
```

**参数：**
- `owner`：用户的钱包地址（小写）
- `version`：协议版本（V5 为 `5`）

#### 获取特定项目的贷款信息

```graphql
query LoansDetailsByAccount($owner: String!, $projectId: Int!, $version: Int!) {
  loans(where: { owner: $owner, projectId: $projectId, version: $version }) {
    items {
      borrowAmount
      collateral
      prepaidDuration
      createdAt
      projectId
      terminal
      token
      chainId
      id
      project {
        version
      }
    }
  }
}
```

#### 检查借款权限

```graphql
query HasPermission(
  $account: String!
  $chainId: Float!
  $projectId: Float!
  $operator: String!
  $version: Float!
) {
  permissionHolder(
    account: $account
    chainId: $chainId
    projectId: $projectId
    operator: $operator
    version: $version
  ) {
    permissions
  }
}
```

**权限 ID 1 表示具有借款权限**：检查 `permissions` 数组中是否包含 `1`。

### 贷款实体字段

```typescript
type Loan = {
  id: BigInt                 // Unique loan ID
  owner: String              // Borrower address
  beneficiary: String        // Recipient of borrowed funds
  borrowAmount: BigInt       // Amount borrowed (in base token wei)
  collateral: BigInt         // Tokens locked as collateral
  prepaidDuration: Int       // Seconds of prepaid fee time
  prepaidFeePercent: Int     // Basis points of prepaid fee
  projectId: Int             // Revnet project ID
  chainId: Int               // Chain where loan exists
  terminal: String           // Terminal address
  token: String              // Base token address (ETH = 0x0...0)
  createdAt: Int             // Unix timestamp
  sourceFeeAmount: BigInt    // Total fees charged
  tokenUri: String | null    // NFT metadata URI (loans are ERC-721)
  version: Int               // Protocol version
}
```

### React Hook 的使用（revnet-app 模式）

```typescript
import { useBendystrawQuery } from 'juice-sdk-react'
import { LoansByAccountDocument } from '@/generated/graphql'

const LOAN_POLL_INTERVAL = 3000 // 3 seconds

function useUserLoans(address: string, version: number = 5) {
  const { data, loading, error } = useBendystrawQuery(
    LoansByAccountDocument,
    { owner: address.toLowerCase(), version },
    { pollInterval: LOAN_POLL_INTERVAL }
  )

  return {
    loans: data?.loans.items ?? [],
    loading,
    error
  }
}
```

### 按 revnet 筛选贷款

在显示特定 revnet 的贷款信息时（这些贷款可能分布在多个链上）：

```typescript
function filterLoansByRevnet(
  loans: Loan[],
  revnetProjectIds: number[]  // projectIds across all chains
): Loan[] {
  return loans.filter(loan =>
    revnetProjectIds.includes(Number(loan.projectId))
  )
}

// Usage: Get projectIds from suckerGroup
const { data: projectData } = useBendystrawQuery(ProjectDocument, { ... })
const revnetProjectIds = projectData.project.suckerGroup?.projects_rel
  .map(p => Number(p.projectId)) ?? [Number(projectData.project.projectId)]

const filteredLoans = filterLoansByRevnet(loans, revnetProjectIds)
```

### 计算贷款的可用额度（可再融资金额）

通过调用合约来获取现有抵押品的可借款金额：

```typescript
import { useReadContract } from 'wagmi'
import { revLoansAbi } from '@/abi/revLoans'

function useLoanHeadroom(loan: Loan) {
  const { data: borrowableAmount } = useReadContract({
    address: REVLOANS_ADDRESS,
    abi: revLoansAbi,
    functionName: 'borrowableAmountFrom',
    args: [
      BigInt(loan.projectId),
      BigInt(loan.collateral),
      18, // decimals
      1,  // currency (ETH)
    ],
  })

  // Headroom = what you could borrow - what you already borrowed
  const headroom = borrowableAmount
    ? borrowableAmount - BigInt(loan.borrowAmount)
    : 0n

  return headroom
}
```

### 多链代币处理

不同链上的贷款可能使用不同的代币。从 suckerGroup 获取代币配置：

```graphql
query GetSuckerGroup($id: String!) {
  suckerGroup(id: $id) {
    projects_rel {
      projectId
      chainId
      decimals    # 18 for ETH, 6 for USDC
      currency    # 1 for ETH, 2 for USDC
    }
  }
}
```

```typescript
function getTokenConfigForLoan(loan: Loan, suckerGroup: SuckerGroup) {
  const project = suckerGroup.projects_rel.find(
    p => p.chainId === loan.chainId && p.projectId === loan.projectId
  )
  return {
    decimals: project?.decimals ?? 18,
    currency: project?.currency ?? 1,
  }
}
```

## 验证

使用已知的贷款数据进行测试：
1. 查询已知有贷款的用户的贷款信息
2. 确认 `borrowAmount` 与链上的 `REVLoans.loanOf()` 返回的值一致
3. 检查 `prepaidDuration` 随时间减少（表示费用消耗情况）

## 示例

用于显示用户贷款信息的完整组件：

```typescript
function UserLoansTable({ address, revnetProjectIds }) {
  const { loans, loading } = useUserLoans(address)

  // Filter to this revnet only
  const revnetLoans = filterLoansByRevnet(loans, revnetProjectIds)

  if (loading) return <Spinner />
  if (revnetLoans.length === 0) return <EmptyState />

  return (
    <Table>
      <thead>
        <tr>
          <th>Chain</th>
          <th>Borrowed</th>
          <th>Collateral</th>
          <th>Fee Time</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {revnetLoans.map(loan => (
          <LoanRow key={loan.id} loan={loan} />
        ))}
      </tbody>
    </Table>
  )
}
```

## 注意事项

- 贷款是 ERC-721 NFT——每笔贷款都有一个唯一的 `tokenUri`
- `prepaidDuration` 以秒为单位，会随时间减少
- 贷款在 10 年后（`LOAN_LIQUIDATION_DURATION`）可以清算
- 权限检查使用 Bendystraw，但实际的借款操作是通过链上合约完成的
- 每 3 秒进行一次轮询，以确保用户界面能够实时反映贷款状态的变化

## 参考资料

- [loansByAccount.graphql](https://github.com/rev-net/revnet-app/blob/main/srcgraphql/loansByAccount.graphql)
- [LoansDetailsTable.tsx](https://github.com/rev-net/revnet-app/blob/main/src/app/[slug]/components/Value/LoansDetailsTable.tsx)
- [useHasBorrowPermission.ts](https://github.com/rev-net/revnet-app/blob/main/src/hooks/useHasBorrowPermission.ts)
- REVLoans 合约：`/jb-revloans`，用于处理合约逻辑
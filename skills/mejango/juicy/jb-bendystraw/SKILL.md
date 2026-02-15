---
name: jb-bendystraw
description: **Bendystraw GraphQL API参考**  
用于查询所有链上的Juicebox项目数据。可获取项目统计信息、支付记录、代币持有者信息、贷款详情、NFT层级信息、统一的活动日志、历史数据快照以及跨链聚合数据。
---

# Bendystraw：跨链Juicebox数据API

Bendystraw是一个用于查询所有支持链上Juicebox V5事件的GraphQL索引器。它汇总数据，并为项目、支付、代币持有者和NFT提供统一的跨链查询功能。

## API基础URL

```
Production: https://bendystraw.xyz/{API_KEY}/graphql
Testnet: https://testnet.bendystraw.xyz/{API_KEY}/graphql
Playground: https://bendystraw.xyz (browser-based GraphQL explorer)
```

## 认证

**需要API密钥。** 请通过Twitter/X联系[@peripheralist](https://x.com/peripheralist)获取API密钥。

```javascript
const response = await fetch(`https://bendystraw.xyz/${API_KEY}/graphql`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: '...',
    variables: { ... }
  })
});
```

**重要提示：** 绝不要在前端代码中暴露API密钥。请使用服务器端代理。

---

## 支持的链

| 链 | 链ID | 网络 |
|-------|----------|---------|
| Ethereum | 1 | 主网 |
| Optimism | 10 | 主网 |
| Base | 8453 | 主网 |
| Arbitrum | 42161 | 主网 |
| Sepolia | 11155111 | 测试网 |

---

## GraphQL模式参考

### 项目实体

```graphql
type Project {
  # Identifiers
  id: String!                    # "{chainId}-{projectId}-{version}"
  projectId: Int!
  chainId: Int!
  version: Int!                  # Protocol version (4 or 5)

  # Metadata
  handle: String
  name: String
  description: String
  logoUri: String
  infoUri: String
  owner: String!
  deployer: String

  # Financial
  balance: String!               # Current balance (wei)
  volume: String!                # Total received (wei)
  volumeUsd: String              # USD equivalent
  redeemVolume: String!          # Total redeemed (wei)
  redeemVolumeUsd: String

  # Tokens
  tokenSupply: String!           # Total token supply
  token: String                  # ERC20 address if deployed
  tokenSymbol: String

  # Activity counts
  paymentsCount: Int!
  redeemCount: Int!
  contributorsCount: Int!
  nftsMintedCount: Int!

  # Trending (7-day window)
  trendingScore: Float
  trendingVolume: String
  trendingPaymentsCount: Int

  # Omnichain
  suckerGroupId: String          # Linked cross-chain group

  # Timestamps
  createdAt: Int!
  deployedAt: Int
}
```

### SuckerGroup实体（多链项目）

```graphql
type SuckerGroup {
  id: String!                    # Unique group identifier
  projects: [String!]!           # Array of project IDs

  # Aggregated totals across all chains
  volume: String!
  volumeUsd: String
  balance: String!
  tokenSupply: String!
  paymentsCount: Int!
  contributorsCount: Int!

  # Related projects (expanded)
  projects_rel: [Project!]!
}
```

### 参与者实体（代币持有者）

```graphql
type Participant {
  id: String!                    # "{chainId}-{projectId}-{address}"
  address: String!
  projectId: Int!
  chainId: Int!

  # Balances
  balance: String!               # Total balance (credits + ERC20)
  creditBalance: String!         # Unclaimed credits
  erc20Balance: String!          # Claimed ERC20 tokens

  # Activity
  volume: String!                # Total contributed
  volumeUsd: String
  paymentsCount: Int!
  redeemCount: Int!

  # Timestamps
  lastPaidAt: Int
  firstPaidAt: Int
}
```

### PayEvent实体

```graphql
type PayEvent {
  id: String!
  projectId: Int!
  chainId: Int!
  rulesetId: Int!

  # Transaction
  txHash: String!
  timestamp: Int!
  logIndex: Int!
  blockNumber: Int!

  # Payment details
  from: String!                  # Payer address
  beneficiary: String!           # Token recipient
  amount: String!                # Payment amount (wei)
  amountUsd: String
  distributionFromPayAmount: String!

  # Tokens
  newlyIssuedTokenCount: String!
  beneficiaryTokenCount: String!

  # Metadata
  memo: String
  feeFromPayAmount: String
}
```

### CashOutEvent实体

```graphql
type CashOutEvent {
  id: String!
  projectId: Int!
  chainId: Int!
  rulesetId: Int!

  # Transaction
  txHash: String!
  timestamp: Int!

  # Redemption details
  holder: String!
  beneficiary: String!
  cashOutCount: String!          # Tokens burned
  reclaimAmount: String!         # ETH received
  reclaimAmountUsd: String
  metadata: String
}
```

### NFT实体

```graphql
type NFT {
  id: String!
  tokenId: Int!
  projectId: Int!
  chainId: Int!
  hook: String!                  # 721 hook address

  # Tier
  tierId: Int!
  tierCategory: Int

  # Ownership
  owner: String!
  createdAt: Int!

  # Metadata
  tokenUri: String
}
```

### ActivityEvent实体（统一活动流）

这是一种多态事件类型，可以提供所有项目活动的统一视图。在构建活动流时，建议查询此实体而非单独的事件类型。

```graphql
type ActivityEvent {
  id: String!
  chainId: Int!
  projectId: Int!
  suckerGroupId: String
  version: Int!

  # Transaction
  txHash: String!
  timestamp: Int!
  from: String!

  # Event type discriminator
  type: ActivityEventType!       # Determines which embedded event is populated

  # Embedded events (one will be non-null based on type)
  payEvent: PayEvent
  cashOutTokensEvent: CashOutTokensEvent
  mintNftEvent: MintNftEvent
  sendPayoutsEvent: SendPayoutsEvent
  sendPayoutToSplitEvent: SendPayoutToSplitEvent
  borrowLoanEvent: BorrowLoanEvent
  repayLoanEvent: RepayLoanEvent
  liquidateLoanEvent: LiquidateLoanEvent
  deployErc20Event: DeployErc20Event
  burnEvent: BurnEvent
  mintTokensEvent: MintTokensEvent
  projectCreateEvent: ProjectCreateEvent
  addToBalanceEvent: AddToBalanceEvent
  useAllowanceEvent: UseAllowanceEvent
  decorateBannyEvent: DecorateBannyEvent
  # ... and more

  # Relations
  project: Project
  suckerGroup: SuckerGroup
}

enum ActivityEventType {
  payEvent
  cashOutTokensEvent
  mintNftEvent
  sendPayoutsEvent
  sendPayoutToSplitEvent
  borrowLoanEvent
  repayLoanEvent
  liquidateLoanEvent
  reallocateLoanEvent
  deployErc20Event
  burnEvent
  mintTokensEvent
  manualMintTokensEvent
  manualBurnEvent
  autoIssueEvent
  projectCreateEvent
  addToBalanceEvent
  useAllowanceEvent
  sendReservedTokensToSplitEvent
  sendReservedTokensToSplitsEvent
  decorateBannyEvent
}
```

### Loan实体（RevLoans）

来自RevLoans协议的活跃贷款状态。

```graphql
type Loan {
  id: BigInt!                    # Loan ID (NFT token ID)
  projectId: Int!
  chainId: Int!
  version: Int!
  createdAt: Int!

  # Loan terms
  borrowAmount: BigInt!          # Amount borrowed (wei)
  collateral: BigInt!            # Collateral locked (project tokens)
  sourceFeeAmount: BigInt!       # Fee amount
  prepaidDuration: Int!          # Prepaid period in seconds
  prepaidFeePercent: Int!        # Fee percent (basis points)

  # Addresses
  beneficiary: String!           # Who receives borrowed funds
  owner: String!                 # Loan NFT owner
  token: String!                 # Collateral token address
  terminal: String!              # Terminal address

  # Metadata
  tokenUri: String               # Loan NFT metadata URI

  # Relations
  project: Project
  participant: Participant
  wallet: Wallet
}
```

### Wallet实体

跨所有项目参与的账户级汇总数据。

```graphql
type Wallet {
  address: String!               # Wallet address

  # Aggregated stats
  volume: BigInt!                # Total volume across all projects
  volumeUsd: BigInt!             # USD equivalent (18 decimals)
  lastPaidTimestamp: Int         # Most recent payment timestamp

  # Relations
  participants: ParticipantPage  # All project participations
  nfts: NFTPage                  # All owned NFTs
}
```

### NFTTier实体

NFT层级配置，包括价格和供应量。

```graphql
type NFTTier {
  chainId: Int!
  projectId: Int!
  version: Int!
  tierId: Int!

  # Pricing
  price: BigInt!                 # Price in terminal token (wei)

  # Supply
  initialSupply: Int!            # Original supply
  remainingSupply: Int!          # Current available

  # Configuration
  allowOwnerMint: Boolean!       # Owner can mint without payment
  cannotBeRemoved: Boolean!      # Tier is permanent
  transfersPausable: Boolean!    # Transfers can be paused
  votingUnits: BigInt!           # Governance weight per NFT
  category: Int                  # Tier category
  reserveFrequency: Int          # Reserve rate
  reserveBeneficiary: String     # Reserve recipient

  # Metadata
  encodedIpfsUri: String         # IPFS hash (encoded)
  resolvedUri: String            # Full resolved URI
  metadata: JSON                 # Parsed metadata
  svg: String                    # SVG content if available

  createdAt: Int!

  # Relations
  hook: NFTHook
  nfts: NFTPage                  # Minted NFTs in this tier
  project: Project
}
```

### NFTHook实体

721挂钩合约配置。

```graphql
type NFTHook {
  chainId: Int!
  projectId: Int!
  version: Int!
  createdAt: Int!

  address: String!               # Hook contract address
  name: String                   # Collection name
  symbol: String                 # Collection symbol

  # Relations
  nfts: NFTPage
  nftTiers: NFTTierPage
  project: Project
}
```

### ProjectMoment实体（历史快照）

项目状态的历史快照，适用于历史图表和分析。

```graphql
type ProjectMoment {
  projectId: Int!
  chainId: Int!
  version: Int!

  # Snapshot point
  block: Int!                    # Block number
  timestamp: Int!                # Unix timestamp

  # State at snapshot
  volume: BigInt!
  volumeUsd: BigInt!
  balance: BigInt!
  trendingScore: BigInt!

  # Relations
  project: Project
}
```

### SuckerGroupMoment实体

跨链聚合状态的历史快照。

```graphql
type SuckerGroupMoment {
  suckerGroupId: String!

  # Snapshot point
  block: Int!
  timestamp: Int!

  # Aggregated state
  volume: BigInt!
  volumeUsd: BigInt!
  balance: BigInt!
  tokenSupply: BigInt!

  # Relations
  suckerGroup: SuckerGroup
}
```

### SuckerTransaction实体（跨链桥接）

通过sucker在链之间进行代币桥接的交易。

```graphql
type SuckerTransaction {
  index: Int!                    # Transaction index
  projectId: Int!
  chainId: Int!                  # Source chain
  version: Int!
  suckerGroupId: String!
  createdAt: Int!

  # Bridge details
  token: String!                 # Token being bridged
  sucker: String!                # Source sucker address
  peer: String!                  # Destination sucker address
  peerChainId: Int!              # Destination chain
  beneficiary: String!           # Recipient address

  # Amounts
  projectTokenCount: BigInt!     # Project tokens bridged
  terminalTokenAmount: BigInt!   # Terminal tokens (if any)

  # State
  root: String                   # Merkle root
  status: SuckerTransactionStatus!

  # Relations
  suckerGroup: SuckerGroup
}

enum SuckerTransactionStatus {
  pending
  completed
  failed
}
```

### SendPayoutsEvent实体

来自终端的支付分配事件。

```graphql
type SendPayoutsEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  logIndex: Int!

  # Payout details
  caller: String!                # Who triggered payout
  from: String!                  # Source address
  rulesetId: Int!
  rulesetCycleNumber: Int!

  # Amounts
  amount: BigInt!                # Total payout amount
  amountUsd: BigInt!
  amountPaidOut: BigInt!         # Actually distributed
  amountPaidOutUsd: BigInt!
  netLeftoverPayoutAmount: BigInt!  # Remaining after splits
  fee: BigInt!                   # Protocol fee
  feeUsd: BigInt!

  # Relations
  project: Project
}
```

### UseAllowanceEvent实体

代币剩余额的使用事件。

```graphql
type UseAllowanceEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!

  # Transaction
  txHash: String!
  timestamp: Int!

  # Allowance details
  caller: String!
  beneficiary: String!           # Who receives funds
  rulesetId: Int!
  rulesetCycleNumber: Int!

  # Amounts
  amount: BigInt!                # Amount used
  amountUsd: BigInt!
  netAmount: BigInt!             # After fees
  netAmountUsd: BigInt!

  # Relations
  project: Project
}
```

### PermissionHolder实体

授予账户的运营商权限。

```graphql
type PermissionHolder {
  chainId: Int!
  projectId: Int!
  version: Int!

  account: String!               # Account with permissions
  operator: String!              # Operator address
  permissions: [Int!]!           # Permission IDs granted
  isRevnetOperator: Boolean!     # Is a revnet operator

  # Relations
  project: Project
}
```

### BorrowLoanEvent实体

来自RevLoans的贷款创建事件。

```graphql
type BorrowLoanEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Loan details
  borrowAmount: BigInt!          # Amount borrowed
  collateral: BigInt!            # Collateral locked
  sourceFeeAmount: BigInt!       # Fee paid
  prepaidDuration: Int!          # Prepaid period (seconds)
  prepaidFeePercent: Int!        # Fee percent (basis points)
  beneficiary: String!           # Loan recipient
  token: String!                 # Collateral token
  terminal: String!              # Terminal address

  # Relations
  project: Project
}
```

### RepayLoanEvent实体

贷款偿还事件。

```graphql
type RepayLoanEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Repayment details
  loanId: BigInt!                # Loan being repaid
  paidOffLoanId: BigInt          # If fully paid off
  repayBorrowAmount: BigInt!     # Amount repaid
  collateralCountToReturn: BigInt!  # Collateral returned

  # Relations
  project: Project
}
```

### LiquidateLoanEvent实体

贷款清算事件。

```graphql
type LiquidateLoanEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Liquidation details
  borrowAmount: BigInt!          # Outstanding borrow
  collateral: BigInt!            # Collateral seized

  # Relations
  project: Project
}
```

### ReallocateLoanEvent实体

贷款重新分配事件（在贷款之间转移抵押品）。

```graphql
type ReallocateLoanEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Reallocation details
  loanId: BigInt!                # Source loan
  reallocatedLoanId: BigInt!     # Target loan
  removedCollateralCount: BigInt!  # Collateral moved

  # Relations
  project: Project
}
```

### BurnEvent实体

代币销毁事件（来自支付操作）。

```graphql
type BurnEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  from: String!

  # Burn details
  amount: BigInt!                # Total burned
  creditAmount: BigInt!          # Credits burned
  erc20Amount: BigInt!           # ERC20 burned

  # Relations
  project: Project
}
```

### MintTokensEvent实体

代币铸造事件（来自支付操作）。

```graphql
type MintTokensEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Mint details
  beneficiary: String!           # Token recipient
  beneficiaryTokenCount: BigInt! # Tokens to beneficiary
  reservedPercent: BigInt!       # Reserved rate
  tokenCount: BigInt!            # Total minted
  memo: String                   # Payment memo

  # Relations
  project: Project
}
```

### ManualMintTokensEvent实体

项目所有者手动铸造代币的事件。

```graphql
type ManualMintTokensEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Mint details
  beneficiary: String!
  beneficiaryTokenCount: BigInt!
  reservedPercent: BigInt!
  tokenCount: BigInt!
  memo: String

  # Relations
  project: Project
}
```

### ManualBurnEvent实体

手动销毁代币的事件。

```graphql
type ManualBurnEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  from: String!

  # Burn details
  amount: BigInt!
  creditAmount: BigInt!
  erc20Amount: BigInt!

  # Relations
  project: Project
}
```

### MintNftEvent实体

NFT铸造事件。

```graphql
type MintNftEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Mint details
  hook: String!                  # 721 hook address
  beneficiary: String!           # NFT recipient
  tierId: Int!                   # Tier minted
  tokenId: BigInt!               # Token ID
  totalAmountPaid: BigInt!       # Amount paid

  # Relations
  project: Project
  tier: NFTTier
  nft: NFT
}
```

### DeployErc20Event实体

ERC20代币部署事件。

```graphql
type DeployErc20Event {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Token details
  symbol: String!                # Token symbol
  name: String!                  # Token name
  token: String!                 # Token address

  # Relations
  project: Project
}
```

### ProjectCreateEvent实体

项目创建事件。

```graphql
type ProjectCreateEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Relations
  project: Project
}
```

### AddToBalanceEvent实体

直接添加余额的事件。

```graphql
type AddToBalanceEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Details
  amount: BigInt!                # Amount added
  memo: String                   # Memo
  metadata: String               # Additional metadata
  returnedFees: BigInt           # Fees returned

  # Relations
  project: Project
}
```

### SendPayoutToSplitEvent实体

单独的分发支付事件。

```graphql
type SendPayoutToSplitEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Split details
  rulesetId: Int!
  group: BigInt!                 # Split group
  beneficiary: String!           # Split recipient
  splitProjectId: Int            # If split to project
  hook: String                   # Split hook if any

  # Amounts
  amount: BigInt!                # Gross amount
  netAmount: BigInt!             # After fees
  amountUsd: BigInt!
  percent: Int!                  # Split percent
  lockedUntil: BigInt            # Lock timestamp
  preferAddToBalance: Boolean!   # Add to balance vs pay

  # Relations
  project: Project
}
```

### SendReservedTokensToSplitEvent实体

将预留代币分配给特定接收者。

```graphql
type SendReservedTokensToSplitEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Split details
  rulesetId: Int!
  groupId: BigInt!
  beneficiary: String!
  splitProjectId: Int
  hook: String
  tokenCount: BigInt!            # Tokens sent
  percent: Int!
  lockedUntil: BigInt
  preferAddToBalance: Boolean!

  # Relations
  project: Project
}
```

### SendReservedTokensToSplitsEvent实体

批量分配预留代币的事件。

```graphql
type SendReservedTokensToSplitsEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!
  suckerGroupId: String

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Distribution details
  rulesetId: Int!
  rulesetCycleNumber: Int!
  owner: String!                 # Project owner
  tokenCount: BigInt!            # Total distributed
  leftoverAmount: BigInt!        # Remaining after splits

  # Relations
  project: Project
}
```

### AutoIssueEvent实体

自动发行事件（用于revnet阶段转换）。

```graphql
type AutoIssueEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Issuance details
  stageId: BigInt!               # Revnet stage
  beneficiary: String!           # Token recipient
  count: BigInt!                 # Tokens issued

  # Relations
  project: Project
}
```

### StoreAutoIssuanceAmountEvent实体

自动发行配置事件。

```graphql
type StoreAutoIssuanceAmountEvent {
  id: String!
  chainId: Int!
  version: Int!
  projectId: Int!

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Config details
  stageId: BigInt!               # Revnet stage
  beneficiary: String!           # Configured recipient
  count: BigInt!                 # Amount to auto-issue

  # Relations
  project: Project
}
```

### DecorateBannyEvent实体

NFT装饰事件。

```graphql
type DecorateBannyEvent {
  id: String!
  chainId: Int!
  version: Int!

  # Transaction
  txHash: String!
  timestamp: Int!
  caller: String!
  from: String!
  logIndex: Int!

  # Decoration details
  bannyBodyId: BigInt!           # Banny being decorated
  outfitIds: [BigInt!]!          # Outfit NFT IDs
  backgroundId: BigInt           # Background NFT ID
  tokenUri: String               # Updated token URI
  tokenUriMetadata: JSON         # Parsed metadata

  # Relations
  bannyNft: NFT
}
```

### CashOutTaxSnapshot实体

历史现金支出税率快照。

```graphql
type CashOutTaxSnapshot {
  chainId: Int!
  projectId: Int!
  suckerGroupId: String
  version: Int!

  # Snapshot period
  start: BigInt!                 # Period start timestamp
  duration: BigInt!              # Period duration
  rulesetId: BigInt!             # Ruleset ID

  # Tax rate
  cashOutTax: Int!               # Tax rate (basis points)
}
```

### ParticipantSnapshot实体（GraphQL）

通过GraphQL获取的历史参与者余额快照（REST端点的替代方案）。

```graphql
type ParticipantSnapshot {
  chainId: Int!
  projectId: Int!
  suckerGroupId: String
  version: Int!

  # Snapshot point
  block: Int!
  timestamp: Int!

  # Participant
  address: String!

  # Balances at snapshot
  balance: BigInt!
  creditBalance: BigInt!
  erc20Balance: BigInt!
  volume: BigInt!
  volumeUsd: BigInt!
}
```

---

## 关键概念

### 项目标识

**Juicebox项目通过三个字段唯一标识：`projectId + chainId + version`。**

这一点非常重要，因为：
- **V4和V5是完全不同的协议。** 例如，Ethereum V4上的项目#64与Ethereum V5上的项目#64不是同一个项目。
- 相同的projectId可以存在于多个链上（通过sucker/omnichain），但这些项目是同一个项目。
- 在查询或显示项目时，务必包含`version`字段。

```javascript
// WRONG: Groups V4 and V5 together
const groupKey = `${project.projectId}-${project.chainId}`;

// CORRECT: Keeps V4 and V5 separate
const groupKey = `${project.projectId}-v${project.version}`;
```

### 多链分组

在显示“顶级项目”或汇总统计数据时：
- **相同projectId + version** → 将其分组（通过sucker关联的项目视为同一个项目）
- **相同projectId，不同version** → 分开显示（属于不同的项目）

```javascript
// Group projects by projectId + version (V4 and V5 are different projects!)
const grouped = new Map();

for (const project of projects) {
  const groupKey = `${project.projectId}-v${project.version || 4}`;
  const existing = grouped.get(groupKey);

  if (existing) {
    // Add chain to existing group
    if (!existing.chainIds.includes(project.chainId)) {
      existing.chainIds.push(project.chainId);
    }
    // Sum volumes
    existing.totalVolumeUsd += parseFloat(project.volumeUsd || '0');
  } else {
    grouped.set(groupKey, {
      ...project,
      chainIds: [project.chainId],
      totalVolumeUsd: parseFloat(project.volumeUsd || '0')
    });
  }
}
```

### USD价值格式

`volumeUsd`、`amountUsd`等字段使用**18位小数格式**（类似于wei）。必须正确转换：

```javascript
function formatVolumeUsd(volumeUsd) {
  if (!volumeUsd || volumeUsd === '0') return '$0';

  try {
    // volumeUsd comes in 18 decimal format
    // Use BigInt to avoid precision loss on large numbers
    const raw = BigInt(volumeUsd.split('.')[0]);
    const usd = Number(raw / BigInt(1e12)) / 1e6; // Divide in steps

    if (usd >= 1_000_000) return `$${(usd / 1_000_000).toFixed(1)}M`;
    if (usd >= 1_000) return `$${(usd / 1_000).toFixed(1)}k`;
    if (usd >= 1) return `$${usd.toFixed(0)}`;
    return `$${usd.toFixed(2)}`;
  } catch {
    return '$0';
  }
}
```

**警告：** 对于较大的数值，切勿直接使用`parseFloat()`进行转换——JavaScript在超过15位小数后会丢失精度。

### 按版本过滤

在查询项目时，根据版本进行过滤，以避免混淆V4和V5的数据：

```graphql
# Get only V5 projects
query V5Projects($limit: Int!) {
  projects(
    where: { version: 5 }
    orderBy: "volumeUsd"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      projectId
      chainId
      version
      name
      volumeUsd
    }
  }
}
```

要同时显示两个版本的数据，需要分别查询并在应用程序中进行分组处理。

---

## 查询示例

### 获取单个项目

```graphql
query GetProject($projectId: Int!, $chainId: Int!) {
  project(projectId: $projectId, chainId: $chainId) {
    id
    name
    handle
    owner
    balance
    volume
    volumeUsd
    tokenSupply
    paymentsCount
    contributorsCount
    suckerGroupId
  }
}
```

### 获取参与者（代币持有者）

```graphql
query GetParticipant($projectId: Int!, $chainId: Int!, $address: String!) {
  participant(projectId: $projectId, chainId: $chainId, address: $address) {
    balance
    creditBalance
    erc20Balance
    volume
    volumeUsd
    paymentsCount
  }
}
```

### 获取Sucker Group（多链总计）

```graphql
query GetSuckerGroup($id: String!) {
  suckerGroup(id: $id) {
    id
    volume
    volumeUsd
    balance
    tokenSupply
    paymentsCount
    contributorsCount
    projects_rel {
      projectId
      chainId
      name
      balance
      volume
    }
  }
}
```

### 列出项目

```graphql
query ListProjects($chainId: Int, $version: Int, $limit: Int!, $offset: Int!) {
  projects(
    where: { chainId: $chainId, version: $version }
    orderBy: "volumeUsd"
    orderDirection: "desc"
    limit: $limit
    offset: $offset
  ) {
    items {
      projectId
      chainId
      version
      name
      handle
      volumeUsd
      balance
      paymentsCount
    }
    totalCount
  }
}
```

### 列出最近的交易

```graphql
query ListPayments($projectId: Int!, $chainId: Int!, $limit: Int!) {
  payEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      from
      beneficiary
      amount
      amountUsd
      memo
      newlyIssuedTokenCount
    }
  }
}
```

### 列出顶级代币持有者

```graphql
query ListParticipants($projectId: Int!, $chainId: Int!, $limit: Int!) {
  participants(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "balance"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      address
      balance
      creditBalance
      erc20Balance
      volume
      paymentsCount
    }
    totalCount
  }
}
```

### 获取热门项目

```graphql
query TrendingProjects($limit: Int!) {
  projects(
    orderBy: "trendingScore"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      projectId
      chainId
      name
      handle
      trendingScore
      trendingVolume
      trendingPaymentsCount
    }
  }
}
```

### 列出现金支出事件

```graphql
query ListCashOuts($projectId: Int!, $chainId: Int!, $limit: Int!) {
  cashOutEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      holder
      beneficiary
      cashOutCount
      reclaimAmount
      reclaimAmountUsd
    }
  }
}
```

### 列出项目的NFT

```graphql
query ListNFTs($projectId: Int!, $chainId: Int!, $limit: Int!) {
  nfts(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "createdAt"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      tokenId
      tierId
      tierCategory
      owner
      createdAt
      tokenUri
    }
  }
}
```

### 获取统一活动流

这是构建活动流的最强大查询方式。一次查询即可获取所有类型的活动数据。

```graphql
query GetActivityFeed($projectId: Int!, $chainId: Int!, $limit: Int!) {
  activityEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      id
      timestamp
      txHash
      from
      type                        # Discriminator for event type

      # Include fields from each possible event type
      payEvent {
        amount
        amountUsd
        beneficiary
        memo
      }
      cashOutTokensEvent {
        cashOutCount
        reclaimAmount
        holder
      }
      mintNftEvent {
        tierId
        tokenId
      }
      sendPayoutsEvent {
        amount
        amountPaidOut
        fee
      }
      borrowLoanEvent {
        borrowAmount
        collateral
      }
    }
  }
}
```

### 获取多链活动流

查询特定sucker组在所有链上的活动数据。

```graphql
query GetOmnichainActivity($suckerGroupId: String!, $limit: Int!) {
  activityEvents(
    where: { suckerGroupId: $suckerGroupId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      chainId
      timestamp
      type
      txHash
      from
      payEvent { amount, memo }
      cashOutTokensEvent { cashOutCount, reclaimAmount }
    }
  }
}
```

### 列出活跃的贷款

```graphql
query ListLoans($projectId: Int!, $chainId: Int!, $limit: Int!) {
  loans(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "createdAt"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      id
      borrowAmount
      collateral
      prepaidDuration
      prepaidFeePercent
      owner
      beneficiary
      createdAt
    }
    totalCount
  }
}
```

### 根据ID获取贷款

```graphql
query GetLoan($id: BigInt!) {
  loan(id: $id) {
    id
    projectId
    chainId
    borrowAmount
    collateral
    sourceFeeAmount
    prepaidDuration
    prepaidFeePercent
    beneficiary
    owner
    token
    terminal
    tokenUri
    createdAt
  }
}
```

### 获取钱包投资组合

```graphql
query GetWallet($address: String!) {
  wallet(address: $address) {
    address
    volume
    volumeUsd
    lastPaidTimestamp
    participants(limit: 100) {
      items {
        projectId
        chainId
        balance
        volume
      }
    }
    nfts(limit: 50) {
      items {
        projectId
        chainId
        tokenId
        tierId
      }
    }
  }
}
```

### 列出NFT层级

```graphql
query ListNFTTiers($projectId: Int!, $chainId: Int!, $limit: Int!) {
  nftTiers(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "tierId"
    orderDirection: "asc"
    limit: $limit
  ) {
    items {
      tierId
      price
      initialSupply
      remainingSupply
      category
      votingUnits
      resolvedUri
      metadata
      svg
    }
  }
}
```

### 获取NFT挂钩详情

```graphql
query GetNFTHook($projectId: Int!, $chainId: Int!) {
  nftHooks(
    where: { projectId: $projectId, chainId: $chainId }
    limit: 1
  ) {
    items {
      address
      name
      symbol
      nftTiers(limit: 100) {
        items {
          tierId
          price
          remainingSupply
        }
      }
    }
  }
}
```

### 获取项目历史快照

```graphql
query GetProjectHistory($projectId: Int!, $chainId: Int!, $limit: Int!) {
  projectMoments(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      block
      timestamp
      volume
      volumeUsd
      balance
      trendingScore
    }
  }
}
```

### 获取跨链桥接交易

```graphql
query GetSuckerTransactions($suckerGroupId: String!, $limit: Int!) {
  suckerTransactions(
    where: { suckerGroupId: $suckerGroupId }
    orderBy: "createdAt"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      index
      chainId
      peerChainId
      beneficiary
      projectTokenCount
      terminalTokenAmount
      status
      createdAt
    }
  }
}
```

### 列出支付事件

```graphql
query ListPayouts($projectId: Int!, $chainId: Int!, $limit: Int!) {
  sendPayoutsEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      caller
      rulesetCycleNumber
      amount
      amountPaidOut
      fee
      netLeftoverPayoutAmount
    }
  }
}
```

### 列出代币使用情况

```graphql
query ListAllowanceUsage($projectId: Int!, $chainId: Int!, $limit: Int!) {
  useAllowanceEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      caller
      beneficiary
      amount
      netAmount
      rulesetCycleNumber
    }
  }
}
```

### 列出贷款事件（借款/偿还/清算）

```graphql
query ListBorrowEvents($projectId: Int!, $chainId: Int!, $limit: Int!) {
  borrowLoanEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      borrowAmount
      collateral
      prepaidDuration
      beneficiary
    }
  }
}

query ListRepayEvents($projectId: Int!, $chainId: Int!, $limit: Int!) {
  repayLoanEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      loanId
      repayBorrowAmount
      collateralCountToReturn
    }
  }
}

query ListLiquidations($projectId: Int!, $chainId: Int!, $limit: Int!) {
  liquidateLoanEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      borrowAmount
      collateral
    }
  }
}
```

### 列出代币销毁事件

```graphql
query ListBurns($projectId: Int!, $chainId: Int!, $limit: Int!) {
  burnEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      from
      amount
      creditAmount
      erc20Amount
    }
  }
}
```

### 列出NFT铸造事件

```graphql
query ListNFTMints($projectId: Int!, $chainId: Int!, $limit: Int!) {
  mintNftEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      beneficiary
      tierId
      tokenId
      totalAmountPaid
    }
  }
}
```

### 获取权限持有者

```graphql
query ListPermissionHolders($projectId: Int!, $chainId: Int!) {
  permissionHolders(
    where: { projectId: $projectId, chainId: $chainId }
    limit: 100
  ) {
    items {
      account
      operator
      permissions
      isRevnetOperator
    }
  }
}
```

### 列出项目创建事件

```graphql
query ListProjectCreations($chainId: Int!, $limit: Int!) {
  projectCreateEvents(
    where: { chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      projectId
      caller
      project {
        name
        handle
        owner
      }
    }
  }
}
```

### 列出ERC20部署事件

```graphql
query ListERC20Deployments($chainId: Int!, $limit: Int!) {
  deployErc20Events(
    where: { chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      projectId
      name
      symbol
      token
    }
  }
}
```

### 获取现金支出历史记录

```graphql
query GetCashOutTaxHistory($projectId: Int!, $chainId: Int!, $limit: Int!) {
  cashOutTaxSnapshots(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "start"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      start
      duration
      rulesetId
      cashOutTax
    }
  }
}
```

### 获取参与者历史记录（GraphQL快照）

```graphql
query GetParticipantHistory(
  $projectId: Int!,
  $chainId: Int!,
  $address: String!,
  $limit: Int!
) {
  participantSnapshots(
    where: { projectId: $projectId, chainId: $chainId, address: $address }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      block
      timestamp
      balance
      creditBalance
      erc20Balance
      volume
      volumeUsd
    }
  }
}
```

### 列出预留代币分配

```graphql
query ListReservedDistributions($projectId: Int!, $chainId: Int!, $limit: Int!) {
  sendReservedTokensToSplitsEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      rulesetCycleNumber
      tokenCount
      leftoverAmount
      owner
    }
  }
}
```

### 列出分割支付

```graphql
query ListSplitPayouts($projectId: Int!, $chainId: Int!, $limit: Int!) {
  sendPayoutToSplitEvents(
    where: { projectId: $projectId, chainId: $chainId }
    orderBy: "timestamp"
    orderDirection: "desc"
    limit: $limit
  ) {
    items {
      timestamp
      txHash
      beneficiary
      splitProjectId
      amount
      netAmount
      percent
    }
  }
}
```

---

## 过滤

`where`子句支持以下操作符：

```graphql
where: {
  # Exact match
  projectId: 1
  chainId: 1

  # Multiple values (OR)
  chainId_in: [1, 10, 8453]

  # Comparison operators
  balance_gt: "1000000000000000000"
  balance_gte: "1000000000000000000"
  balance_lt: "100000000000000000000"
  balance_lte: "100000000000000000000"
  timestamp_gte: 1704067200

  # Text search
  name_contains: "dao"
  handle_starts_with: "jb"
}
```

---

## 排序

**可排序的字段：**

| 实体 | 可排序字段 |
|--------|-----------------|
| Project | `volume`, `balance`, `tokenSupply`, `paymentsCount`, `createdAt`, `trendingScore` |
| Participant | `balance`, `volume`, `paymentsCount` |
| PayEvent | `timestamp`, `amount` |
| CashOutEvent | `timestamp`, `reclaimAmount` |
| NFT | `createdAt`, `tokenId` |
| ActivityEvent | `timestamp` |
| Loan | `createdAt`, `borrowAmount`, `collateral` |
| Wallet | `volume`, `volumeUsd`, `lastPaidTimestamp` |
| NFTTier | `tierId`, `price`, `createdAt` |
| ProjectMoment | `timestamp`, `block` |
| SuckerTransaction | `createdAt` |
| SendPayoutsEvent | `timestamp`, `amount` |
| UseAllowanceEvent | `timestamp`, `amount` |
| BorrowLoanEvent | `timestamp`, `borrowAmount` |
| RepayLoanEvent | `timestamp`, `repayBorrowAmount` |
| LiquidateLoanEvent | `timestamp` |
| BurnEvent | `timestamp`, `amount` |
| MintTokensEvent | `timestamp`, `tokenCount` |
| MintNftEvent | `timestamp`, `tokenId` |
| DeployErc20Event | `timestamp` |
| ProjectCreateEvent | `timestamp` |
| SendPayoutToSplitEvent | `timestamp`, `amount` |
| CashOutTaxSnapshot | `start` |
| ParticipantSnapshot | `timestamp`, `block` |

---

## 分页

所有列表查询都支持分页：

```graphql
query PaginatedPayments(
  $projectId: Int!,
  $chainId: Int!,
  $limit: Int!,
  $offset: Int!
) {
  payEvents(
    where: { projectId: $projectId, chainId: $chainId }
    limit: $limit
    offset: $offset
  ) {
    items { ... }
    totalCount
  }
}
```

**参数：**
- `limit`：返回的最大项目数量（默认：100，最大：1000）
- `offset`：跳过的项目数量

---

## 特殊端点

### 参与者快照

获取特定时间点的历史参与者余额。适用于治理快照和空投操作。

```
POST https://bendystraw.xyz/{API_KEY}/participants
```

**请求：**
```json
{
  "suckerGroupId": "0x...",
  "timestamp": 1704067200
}
```

**响应：**
```json
{
  "participants": [
    {
      "address": "0x...",
      "balance": "1000000000000000000000",
      "chains": {
        "1": "600000000000000000000",
        "10": "400000000000000000000"
      }
    }
  ]
}
```

---

## 完整的JavaScript示例

```javascript
const BENDYSTRAW_URL = 'https://bendystraw.xyz';
const API_KEY = process.env.BENDYSTRAW_API_KEY;

/**
 * Execute GraphQL query
 */
async function query(graphql, variables = {}) {
  const response = await fetch(`${BENDYSTRAW_URL}/${API_KEY}/graphql`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: graphql, variables })
  });

  const result = await response.json();

  if (result.errors) {
    throw new Error(result.errors[0].message);
  }

  return result.data;
}

/**
 * Get project stats
 */
async function getProject(projectId, chainId) {
  const data = await query(`
    query($projectId: Int!, $chainId: Int!) {
      project(projectId: $projectId, chainId: $chainId) {
        name
        handle
        owner
        balance
        volume
        volumeUsd
        tokenSupply
        paymentsCount
        contributorsCount
        suckerGroupId
      }
    }
  `, { projectId, chainId });

  return data.project;
}

/**
 * Get omnichain totals for sucker group
 */
async function getOmnichainStats(suckerGroupId) {
  const data = await query(`
    query($id: String!) {
      suckerGroup(id: $id) {
        volume
        volumeUsd
        balance
        tokenSupply
        contributorsCount
        projects_rel {
          chainId
          name
          balance
          volume
        }
      }
    }
  `, { id: suckerGroupId });

  return data.suckerGroup;
}

/**
 * Get recent payments
 */
async function getRecentPayments(projectId, chainId, limit = 20) {
  const data = await query(`
    query($projectId: Int!, $chainId: Int!, $limit: Int!) {
      payEvents(
        where: { projectId: $projectId, chainId: $chainId }
        orderBy: "timestamp"
        orderDirection: "desc"
        limit: $limit
      ) {
        items {
          timestamp
          from
          beneficiary
          amount
          amountUsd
          memo
          newlyIssuedTokenCount
        }
      }
    }
  `, { projectId, chainId, limit });

  return data.payEvents.items;
}

/**
 * Get top token holders
 */
async function getTopHolders(projectId, chainId, limit = 100) {
  const data = await query(`
    query($projectId: Int!, $chainId: Int!, $limit: Int!) {
      participants(
        where: { projectId: $projectId, chainId: $chainId }
        orderBy: "balance"
        orderDirection: "desc"
        limit: $limit
      ) {
        items {
          address
          balance
          creditBalance
          erc20Balance
          volume
        }
        totalCount
      }
    }
  `, { projectId, chainId, limit });

  return {
    holders: data.participants.items,
    total: data.participants.totalCount
  };
}

/**
 * Get participant balance
 */
async function getParticipant(projectId, chainId, address) {
  const data = await query(`
    query($projectId: Int!, $chainId: Int!, $address: String!) {
      participant(projectId: $projectId, chainId: $chainId, address: $address) {
        balance
        creditBalance
        erc20Balance
        volume
        volumeUsd
        paymentsCount
      }
    }
  `, { projectId, chainId, address });

  return data.participant;
}

/**
 * Get trending projects
 */
async function getTrendingProjects(chainId = null, limit = 10) {
  const where = chainId ? { chainId } : {};

  const data = await query(`
    query($where: ProjectWhereInput, $limit: Int!) {
      projects(
        where: $where
        orderBy: "trendingScore"
        orderDirection: "desc"
        limit: $limit
      ) {
        items {
          projectId
          chainId
          name
          handle
          trendingScore
          trendingVolume
          trendingPaymentsCount
        }
      }
    }
  `, { where, limit });

  return data.projects.items;
}

/**
 * Get historical snapshot for governance
 */
async function getSnapshot(suckerGroupId, timestamp) {
  const response = await fetch(`${BENDYSTRAW_URL}/${API_KEY}/participants`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ suckerGroupId, timestamp })
  });

  return await response.json();
}

/**
 * Get unified activity feed (all event types)
 */
async function getActivityFeed(projectId, chainId, limit = 50) {
  const data = await query(`
    query($projectId: Int!, $chainId: Int!, $limit: Int!) {
      activityEvents(
        where: { projectId: $projectId, chainId: $chainId }
        orderBy: "timestamp"
        orderDirection: "desc"
        limit: $limit
      ) {
        items {
          id
          timestamp
          txHash
          from
          type
          payEvent { amount, amountUsd, beneficiary, memo }
          cashOutTokensEvent { cashOutCount, reclaimAmount, holder }
          mintNftEvent { tierId, tokenId }
          sendPayoutsEvent { amount, amountPaidOut, fee }
          borrowLoanEvent { borrowAmount, collateral }
        }
      }
    }
  `, { projectId, chainId, limit });

  return data.activityEvents.items;
}

/**
 * Get active loans for a project
 */
async function getLoans(projectId, chainId, limit = 100) {
  const data = await query(`
    query($projectId: Int!, $chainId: Int!, $limit: Int!) {
      loans(
        where: { projectId: $projectId, chainId: $chainId }
        orderBy: "createdAt"
        orderDirection: "desc"
        limit: $limit
      ) {
        items {
          id
          borrowAmount
          collateral
          prepaidDuration
          prepaidFeePercent
          owner
          beneficiary
          createdAt
        }
        totalCount
      }
    }
  `, { projectId, chainId, limit });

  return {
    loans: data.loans.items,
    total: data.loans.totalCount
  };
}

/**
 * Get wallet portfolio across all projects
 */
async function getWalletPortfolio(address) {
  const data = await query(`
    query($address: String!) {
      wallet(address: $address) {
        address
        volume
        volumeUsd
        lastPaidTimestamp
        participants(limit: 100) {
          items {
            projectId
            chainId
            balance
            volume
            project { name, handle }
          }
        }
      }
    }
  `, { address });

  return data.wallet;
}

/**
 * Get NFT tier details with metadata
 */
async function getNFTTiers(projectId, chainId) {
  const data = await query(`
    query($projectId: Int!, $chainId: Int!) {
      nftTiers(
        where: { projectId: $projectId, chainId: $chainId }
        orderBy: "tierId"
        orderDirection: "asc"
        limit: 100
      ) {
        items {
          tierId
          price
          initialSupply
          remainingSupply
          category
          votingUnits
          resolvedUri
          metadata
          svg
        }
      }
    }
  `, { projectId, chainId });

  return data.nftTiers.items;
}

/**
 * Get historical project snapshots for charting
 */
async function getProjectHistory(projectId, chainId, limit = 100) {
  const data = await query(`
    query($projectId: Int!, $chainId: Int!, $limit: Int!) {
      projectMoments(
        where: { projectId: $projectId, chainId: $chainId }
        orderBy: "timestamp"
        orderDirection: "desc"
        limit: $limit
      ) {
        items {
          block
          timestamp
          volume
          volumeUsd
          balance
          trendingScore
        }
      }
    }
  `, { projectId, chainId, limit });

  return data.projectMoments.items;
}

// Example usage
async function main() {
  // Get project on Ethereum mainnet
  const project = await getProject(1, 1);
  console.log(`${project.name}: ${project.balance} wei balance`);

  // If omnichain, get aggregated stats
  if (project.suckerGroupId) {
    const omni = await getOmnichainStats(project.suckerGroupId);
    console.log(`Omnichain total: ${omni.volume} wei volume across ${omni.projects_rel.length} chains`);
  }

  // Get recent activity
  const payments = await getRecentPayments(1, 1, 5);
  console.log(`Last ${payments.length} payments:`);
  payments.forEach(p => {
    console.log(`  ${p.from.slice(0,8)}... paid ${p.amount} wei`);
  });

  // Get top holders
  const { holders, total } = await getTopHolders(1, 1, 10);
  console.log(`Top 10 of ${total} holders:`);
  holders.forEach((h, i) => {
    console.log(`  ${i + 1}. ${h.address.slice(0,8)}... - ${h.balance} tokens`);
  });
}

main().catch(console.error);
```

---

## BendystrawClient类

```javascript
class BendystrawClient {
  constructor(apiKey, isTestnet = false) {
    this.baseUrl = isTestnet
      ? 'https://testnet.bendystraw.xyz'
      : 'https://bendystraw.xyz';
    this.apiKey = apiKey;
  }

  async query(graphql, variables = {}) {
    const response = await fetch(`${this.baseUrl}/${this.apiKey}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: graphql, variables })
    });

    if (!response.ok) {
      throw new Error(`Bendystraw request failed: ${response.statusText}`);
    }

    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0].message);
    }

    return result.data;
  }

  // Convenience methods
  async getProject(projectId, chainId) { ... }
  async getSuckerGroup(id) { ... }
  async getPayments(projectId, chainId, limit) { ... }
  async getParticipants(projectId, chainId, limit) { ... }
  async getSnapshot(suckerGroupId, timestamp) { ... }
}
```

---

## 服务器端代理

由于API密钥必须保密，请使用服务器端代理：

### Next.js API路由

```typescript
// pages/api/bendystraw.ts
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const response = await fetch(
    `https://bendystraw.xyz/${process.env.BENDYSTRAW_API_KEY}/graphql`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    }
  );

  const data = await response.json();
  res.json(data);
}
```

### Express中间件

```javascript
app.post('/api/bendystraw', async (req, res) => {
  const response = await fetch(
    `https://bendystraw.xyz/${process.env.BENDYSTRAW_API_KEY}/graphql`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    }
  );

  res.json(await response.json());
});
```

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Unauthorized` | API密钥无效 | 确认API密钥正确 |
| `Rate limited` | 请求过多 | 添加延迟/重试逻辑 |
| `Invalid query` | GraphQL语法错误 | 检查查询结构 |
| `Not found` | 实体不存在 | 确认projectId/chainId |
| `Timeout` | 查询过于复杂 | 减少请求次数，添加过滤条件 |

---

## 常见问题与注意事项

### V4与V5协议混淆

**重要提示：** V4和V5是完全不同的协议，具有不同的合约地址。
- V4上的项目#1与V5上的项目#1不是同一个项目。
- 相同的projectId可以在多个链上存在（通过sucker/omnichain），但这些项目是同一个项目。
- 在查询或显示项目时，务必包含`version`字段。

### V5.0与V5.1合约混淆

**重要提示：** 在V5版本中，存在两个合约版本：V5.0和V5.1。同时使用这两个版本的合约是不允许的。使用JBController5_1的项目必须使用JBMultiTerminal5_1。

**同时支持V5.0和V5.1的合约：**

| 合约 | 地址 |
|----------|---------|
| JBProjects | `0x885f707efa18d2cb12f05a3a8eba6b4b26c8c1d4` |
| JBTokens | `0x4d0edd347fb1fa21589c1e109b3474924be87636` |
| JBDirectory | `0x0061e516886a0540f63157f112c0588ee0651dcf` |
| JBSplits | `0x7160a322fea44945a6ef9adfd65c322258df3c5e` |

**V5.0合约（用于revnets和旧项目）：**

| 合约 | 地址 |
|----------|---------|
| JBController | `0x27da30646502e2f642be5281322ae8c394f7668a` |
| JBMultiTerminal | `0x2db6d704058e552defe415753465df8df0361846` |
| JBRulesets | `0x6292281d69c3593fcf6ea074e5797341476ab428` |
| REVDeployer | `0x2ca27bde7e7d33e353b44c27acfcf6c78dde251d` |
| JB721TiersHookDeployer | `0x7e4f7bfeab74bbae3eb12a62f2298bf2be16fc93` |

**V5.1合约（用于新项目）：**

| 合约 | 地址 |
|----------|---------|
| JBController5_1 | `0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1` |
| JBMultiTerminal5_1 | `0x52869db3d61dde1e391967f2ce5039ad0ecd371c` |
| JBRulesets5_1 | `0xd4257005ca8d27bbe11f356453b0e4692414b056` |
| JBOmnichainDeployer5_1 | `0x587bf86677ec0d1b766d9ba0d7ac2a51c6c2fc71` |
| JB721TiersHookDeployer5_1 | `0x7e6e7db5081c59f2df3c83b54eb0c4d029e9898e` |

**确定项目版本的方法：** 查询`JBDirectory.controllerOf(projectId)`并进行比较：
- `0x27da30646502e2f642be5281322ae8c394f7668a` = V5.0（使用JBMultiTerminal, JBRulesets）
- `0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1` = V5.1（使用JBMultiTerminal5_1, JBRulesets5_1）

请参阅 `/jb-v5-v51-contracts` 以获取完整的参考信息和代码示例。

### 代币符号混淆

**重要提示：** Bendystraw中的`tokenSymbol`字段返回的是**基础/记账代币**（例如“ETH”或“USDC”），而不是项目发行的ERC20代币符号（例如Bananapus的“NANA”）。
要获取项目发行的代币符号，需要直接查询区块链。

```javascript
import { createPublicClient, http } from 'viem'
import { mainnet } from 'viem/chains'

// JBTokens address (same on all V5 chains)
const JB_TOKENS = '0x4d0edd347fb1fa21589c1e109b3474924be87636'

const TOKEN_ABI = [
  {
    name: 'tokenOf',
    type: 'function',
    stateMutability: 'view',
    inputs: [{ name: 'projectId', type: 'uint256' }],
    outputs: [{ name: '', type: 'address' }],
  },
  {
    name: 'symbol',
    type: 'function',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ name: '', type: 'string' }],
  },
]

async function getProjectTokenSymbol(projectId: number, chainId: number) {
  const client = createPublicClient({ chain: mainnet, transport: http() })

  // Get the token address from JBTokens
  const tokenAddress = await client.readContract({
    address: JB_TOKENS,
    abi: TOKEN_ABI,
    functionName: 'tokenOf',
    args: [BigInt(projectId)],
  })

  // Zero address means no ERC20 deployed yet (using credits only)
  if (tokenAddress === '0x0000000000000000000000000000000000000000') {
    return null
  }

  // Get symbol from the token contract
  return await client.readContract({
    address: tokenAddress,
    abi: TOKEN_ABI,
    functionName: 'symbol',
  })
}
```

### GraphQL类型不一致

不同的查询对相同的概念值期望不同的GraphQL类型。如果使用错误的类型，可能会导致查询失败。

**示例：**

```graphql
# This works (project query uses Float)
query GetProject($projectId: Float!, $chainId: Float!, $version: Float!) {
  project(projectId: $projectId, chainId: $chainId, version: $version) { ... }
}

# This fails silently if you pass Float instead of Int
query GetPayEvents($projectId: Int!, $chainId: Int!, $version: Int!) {
  payEvents(where: { projectId: $projectId, chainId: $chainId, version: $version }) { ... }
}
```

**最佳实践：** 查阅模式或使用GraphQL playground来验证每个查询的预期类型。

### SuckerGroup跨链聚合

对于多链项目，使用`suckerGroupId`来获取所有链上的汇总数据，而不是分别查询每个链：

```javascript
// INEFFICIENT: Query each chain separately
const chains = [1, 10, 8453, 42161]
const balances = await Promise.all(
  chains.map(chainId => getProjectBalance(projectId, chainId))
)
const totalBalance = balances.reduce((sum, b) => sum + b, 0n)

// EFFICIENT: Use suckerGroup for cross-chain totals
const project = await getProject(projectId, chainId)
if (project.suckerGroupId) {
  const group = await getSuckerGroup(project.suckerGroupId)
  // group.balance is already the cross-chain total
  // group.projects_rel has per-chain breakdown
}
```

`suckerGroup`查询返回：
- 预先汇总的总量（`balance`, `volume`, `tokenSupply`等）
- 通过`projects_rel`获取每个链的详细数据
- 由于并行查询，数据一致且不会出现竞争条件

### ETH与USDC项目货币

**重要提示：** 项目可以使用不同的基础货币（ETH或USDC）。`amount`, `balance`, `volume`字段根据货币的不同使用不同的小数精度：

| 货币 | 小数位数 | 代码 |
|----------|----------|------|
| ETH | 18 | 1 |
| USDC | 6 | 2 |

货币信息可以从`suckerGroup`或`participants`查询中获取：

```graphql
query GetSuckerGroup($id: String!) {
  suckerGroup(id: $id) {
    projects_rel {
      projectId
      chainId
      decimals       # 18 for ETH, 6 for USDC
      currency       # 1 for ETH, 2 for USDC
      balance
    }
  }
}
```

**正确格式化金额：**

```javascript
import { formatUnits } from 'viem'

function formatAmount(wei, decimals, currency) {
  const num = parseFloat(formatUnits(BigInt(wei), decimals))
  const symbol = currency === 2 ? 'USDC' : 'ETH'
  // USDC uses fewer decimal places for display
  const precision = currency === 2 ? 2 : 4
  return `${num.toFixed(precision)} ${symbol}`
}

// Example: USDC project (6 decimals)
formatAmount('1000000', 6, 2)    // "1.00 USDC"

// Example: ETH project (18 decimals)
formatAmount('1000000000000000000', 18, 1)  // "1.0000 ETH"
```

**常见错误：** 对于USDC项目，如果使用`formatEther()`（假设18位小数），将会显示严重错误的数值。务必先检测货币类型，然后使用`formatUnits()`并指定正确的小数位数。

---

## 最佳实践

1. **使用服务器端代理** - 绝不要在前端代码中暴露API密钥
2. **缓存响应** - 数据大约每1分钟更新一次，相应地进行缓存
3. **仅查询需要的字段** - 减少数据量并降低延迟
4. **使用分页** - 避免一次性获取大量记录
5. **处理空值** - 如`volumeUsd`, `handle`等字段可能为空
6. **考虑数据更新频率** - 索引器的更新可能滞后1-2个区块
7. **使用过滤条件** - 可能时根据chainId, projectId进行过滤
8. **始终包含版本信息** - 具有相同projectId的V4和V5项目应被分组
9. **对USD值使用BigInt类型** - `volumeUsd`使用18位小数；`parseFloat`在处理大数值时会丢失精度
10. **按projectId + version分组** - 同一项目在不同链上应被分组，但不同版本不应被合并
11. **检查GraphQL类型** - 不同查询对相同字段的类型要求可能不同（Float或Int）
12. **使用suckerGroup获取跨链数据** - 比分别查询每个链更高效
13. **从链上获取代币符号** - Bendystraw的`tokenSymbol`表示记账代币，而非项目发行的代币
14. **在格式化前检测货币类型** - 使用`formatUnits(wei, decimals)`而不是`formatEther(wei)`，因为USDC项目使用6位小数

---

## 使用场景

- **项目仪表板** - 显示统计数据、活动情况和持有者信息
- **统一活动流** - 使用`activityEvents`获取所有项目的全方位活动信息
- **治理快照** - 获取特定时间点的代币余额
- **数据分析** - 通过`projectMoments`跟踪趋势、交易量和贡献者增长
- **投资组合追踪** - 使用`wallet`查询用户在不同项目中的投资情况
- **多链聚合** - 通过`suckerGroup`和`suckerGroupMoments`获取统一视图
- **空投** - 根据持有者数据生成接收者列表
- **贷款仪表板** - 跟踪RevLoans的借款、偿还和清算情况
- **NFT画廊** - 通过`nftTiers`获取NFT的完整层级信息（包括SVG和价格）
- **跨链追踪** - 通过`suckerTransactions`监控代币桥接情况
- **资金管理** - 跟踪支付和代币使用情况

---

## 相关技能

- `/jb-relayr` - 执行多链交易
- `/jb-omnichain-ui` - 使用Bendystraw数据构建用户界面
- `/jb-query` - 通过cast/ethers直接进行链上查询
- `/jb-revloans` - 集成RevLoans协议
- `/jb-loan-queries` - 专门用于贷款的查询模式
- `/jb-nft-gallery-ui` - 使用`nftTiers`构建NFT画廊
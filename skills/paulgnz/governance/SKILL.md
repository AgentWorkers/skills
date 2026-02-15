---
name: governance
description: XPR网络治理：社区、提案以及对治理合约的投票
---

## XPR网络治理

您可以通过`gov`合约与XPR网络的链上治理系统进行交互。社区可以提出提案，而代币持有者会对这些提案进行投票。

### 关键概念

- **社区**——治理组织（包括XPR Network、Metal DAO、LOAN Protocol、XPR Grants、Metal X、D.O.G.E.等）。每个社区都有自己的投票策略、提案费用和法定人数要求。
- **提案**——链上的记录，其中包含候选人信息、投票选项、开始/结束时间以及审批状态。提案的内容（标题和描述）会存储在链外的Gov API中。
- **投票策略**——决定哪些用户可以投票以及投票权重的计算方式：
  - `xpr-unstaked-and-staked-balances`：权重 = XPR余额（已质押+未质押的XPR）
  - `xmt-balances`：权重 = XMT余额
  - `loan-and-sloan-balances`：权重 = LOAN余额 + sLOAN余额
  - `kyc-verification`：每个通过KYC验证的账户拥有1票
- **投票系统**：
  - `"0"`：单选
  - `"1"`：多选
  - `"2"`：排序选择
  - `"5"`：批准投票
- **法定人数**——最低参与门槛（以基点表示，例如300表示3%）
- **提案费用**——提出提案所需的代币支付（因社区而异，例如20,000 XPR、100 XMT、50,000 LOAN）

### 活跃社区

| ID | 名称 | 投票策略 | 费用 | 法定人数 |
|----|------|----------|-----|--------|
| 3 | XPR Network | XPR余额 | 20,000 XPR | 3% |
| 4 | Metal DAO | XMT余额 | 100 XMT | 3% |
| 5 | LOAN Protocol | LOAN+sLOAN | 50,000 LOAN | 25% |
| 6 | XPR Grants | XPR余额 | 20,000 XPR | 3% |
| 7 | Metal X | XPR余额 | 20,000 XPR | 3% |
| 8 | D.O.G.E. | KYC验证 | 1 XDOGE | 0.01% |

### 只读工具（安全，无签名功能）

- `gov_list_communities`：列出所有治理社区的信息，包括投票策略、费用、法定人数和管理员信息
- `gov_list_proposals`：列出提案列表，支持社区和状态筛选
- `gov_get_proposal`：从Gov API获取提案的详细信息（包括标题和描述），以及每个候选人的投票总数
- `gov_get_votes`：获取针对某个提案的投票记录（按时间顺序显示）
- `gov_get_config`：获取治理系统的整体配置信息（如暂停状态、总投票数）

### 编写工具（需要设置`confirmed: true`）

- `gov_vote`：对活跃的提案进行投票。需要指定候选人及其对应的权重。
- `gov_post_proposal`：创建新的治理提案。需要支付该社区的提案费用（通过一次交易完成代币转移和提案提交操作）。

### 投票流程

进行投票时，您需要提供`communityId`、`proposalId`以及`winners`（包含候选人ID及其权重的数组）。对于简单的“是/否”型提案，可以使用`[{id: 0, weight: 100}]`表示“是”，或`[{id: 1, weight: 100}]`表示“否”。

### 提案创建流程

创建提案需要以下步骤：
1. 通过Gov API（`https://gov.api.xprnetwork.org`）生成一个`content` ID。
2. 支付该社区的提案费用（将代币转移至`gov`地址）。
3. 调用`gov_post_proposal`函数并传递所有提案参数。

`gov_post_proposal`工具会处理步骤2和3（费用支付及提案提交）。您必须提供步骤1中生成的`content` ID。

### 提案链接

提案的查看地址为：`https://gov.xprnetwork.org/communities/{communityId}/proposals/{proposalId}`

### 安全规则

- 提案有明确的开始和结束时间——仅在指定时间内允许投票。
- 不同社区使用不同的费用代币——在创建提案前请确认该社区的`proposalFee`要求。
- 法定人数以基点计算（例如300表示3%）——提案需要达到一定的参与度才能通过。
- 管理员可以批准或拒绝提案——`approve`字段会显示提案的最终状态。
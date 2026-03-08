---
name: shll-run
description: 通过 SHLL AgentNFA 在 BSC 上执行去中心化金融（DeFi）交易。人工智能会处理所有命令，用户只需进行聊天交流即可。
version: 6.0.5
author: SHLL Team
website: https://shll.run
twitter: https://twitter.com/shllrun
repository: https://github.com/kledx/shll-skills.git
install: npm install -g shll-skills --registry https://registry.npmjs.org
update: npm update -g shll-skills --registry https://registry.npmjs.org
env:
  - name: RUNNER_PRIVATE_KEY
    required: true
    description: >
      Operator wallet private key (AI-only hot wallet).
      MUST be a dedicated wallet with minimal BNB for gas only.
      NEVER use your main wallet, owner wallet, or any wallet holding significant funds.
      Even if this key leaks, on-chain PolicyGuard limits actions to policy-approved trades.
  - name: SHLL_RPC
    required: false
    description: Optional BSC RPC URL override. A private RPC is recommended for reliability.
credentials:
  scope: operator-hot-wallet-only
  risk: >
    The operator key can only execute policy-limited trades within on-chain PolicyGuard rules.
    It cannot withdraw vault funds, transfer the Agent NFT, or bypass spending limits.
    Treat it as a restricted session key, not a master key.
  guidance: >
    Use generate-wallet to create a purpose-built operator wallet.
    Fund it with ~$1 BNB for gas only. Do not store trading capital in this wallet.
    The operator wallet is NOT the owner wallet, NOT the vault, NOT the Agent NFT holder.
---
# SHLL — 为 BNB 链上的 AI 代理提供基于合约的安全执行机制

## 什么是 SHLL？

SHLL 是一个专为 BNB 链上的 AI 代理设计的去中心化金融（DeFi）执行层，它通过 **链上安全机制** 来确保交易的安全性。与可以被绕过的离线过滤器不同，SHLL 利用智能合约来强制执行消费限制、交易间隔、协议白名单以及接收者限制。每个 AI 代理的操作在执行前都会由一个不可篡改的 PolicyGuard 合约进行验证。

**关键信息：**
- **网络**：BNB 主网
- **提供 27 个 CLI 和 MCP 工具**，用于执行去中心化金融操作（如交换、借贷、表情包交易、投资组合管理等）
- **支持 PancakeSwap V2/V3、Venus 协议以及 Four.meme**  
- **MCP 服务器兼容 Claude、Cursor、OpenClaw 以及所有兼容 MCP 的代理**  
- **npm 包**：`shll-skills`  
- **官方网站**：https://shll.run

## 安全架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        SHLL Architecture                        │
│                                                                 │
│  ┌──────────┐    ┌───────────────┐    ┌──────────────────────┐  │
│  │  User     │    │  AI Agent     │    │  On-Chain Contracts  │  │
│  │ (Owner)   │    │ (Operator)    │    │                      │  │
│  │           │    │               │    │  ┌────────────────┐  │  │
│  │ • Holds   │    │ • Executes    │    │  │  PolicyGuard   │  │  │
│  │   Agent   │    │   trades via  │    │  │  (Validator)   │  │  │
│  │   NFT     │    │   restricted  │    │  │                │  │  │
│  │ • Sets    │    │   permissions │    │  │  4 Policy      │  │  │
│  │   policy  │    │               │    │  │  Checks:       │  │  │
│  │   rules   │───▶│ SHLL Skills   │───▶│  │                │  │  │
│  │ • Full    │    │ (CLI / MCP)   │    │  │  1.Spending    │  │  │
│  │   asset   │    │               │    │  │    Limit       │  │  │
│  │   control │    │ Cannot:       │    │  │  2.Cooldown    │  │  │
│  │           │    │ • Withdraw    │    │  │  3.DeFi Guard  │  │  │
│  │           │    │   vault funds │    │  │  4.Receiver    │  │  │
│  │           │    │ • Change      │    │  │    Guard       │  │  │
│  │           │    │   policies    │    │  └───────┬────────┘  │  │
│  │           │    │ • Transfer    │    │          │            │  │
│  │           │    │   NFT         │    │   ┌─────▼──────┐     │  │
│  │           │    │               │    │   │   Vault     │     │  │
│  │           │    │               │    │   │ (Agent      │     │  │
│  │           │    │               │    │   │  Account)   │     │  │
│  │           │    │               │    │   │             │     │  │
│  │           │    │               │    │   │ Holds funds │     │  │
│  └──────────┘    └───────────────┘    │   └─────────────┘     │  │
│                                       └──────────────────────┘  │
│  Dual-Wallet Isolation:                                         │
│  • Owner wallet = asset control (human)                         │
│  • Operator wallet = restricted execution (AI)                  │
│  • Even if operator key leaks, PolicyGuard still limits actions │
└─────────────────────────────────────────────────────────────────┘
```

## 四项核心政策（PolicyGuard 堆栈）

所有政策都通过智能合约在链上执行，AI 无法绕过这些政策：

| 政策 | 合约 | 功能 |
|--------|----------|-------------|
| SpendingLimitV2 | 链上 | 每笔交易和每日 BNB 消费上限 |
| CooldownPolicy | 链上 | 连续交易之间的最小时间间隔 |
| DeFiGuardV2 | 链上 | 允许的 DeFi 协议和功能白名单 |
| ReceiverGuardV2 | 链上 | 只有经过批准的接收者地址才能接收资金 |

当政策拒绝某个操作时：
- 该交易将不会被执行 |
- 保险库中的资金将保持安全 |
- 拒绝的原因会从智能合约中返回 |
- 拒绝操作会被记录并可供审计 |
- 响应中的 `enforcement` 字段始终显示为 “on-chain” （即操作在链上执行）

## 为什么需要链上执行？

大多数 AI 代理平台使用离线安全过滤器：
- **离线方式**：由 AI 或后端决定执行逻辑 → 可能通过注入提示、API 操作或代码漏洞被绕过
- **链上方式（SHLL）**：由智能合约决定执行逻辑 → 无法被绕过 → 区块链会强制执行规则

**PolicyGuard 合约地址**：`0x25d17eA0e3Bcb8CA08a2BFE917E817AFc05dbBB3`  
**可在 BscScan 上验证**：https://bscscan.com/address/0x25d17eA0e3Bcb8CA08a2BFE917E817AFc05dbBB3

---

# SHLL 技能使用指南

本文件定义了 AI 代理应如何安全地使用 `shll-run` 和 `shll-mcp`。

## 使用范围：
- **网络**：BNB 主网
- **CLI**：`shll-run`（别名：`shll-onchain-runner`）
- **MCP**：`shll-mcp`
- **安全层**：SHLL PolicyGuard

**注意事项**：
- 不应直接要求用户运行 CLI 命令，应由 AI 来执行命令并解释结果。

## 强制性安全规则：
1. 令牌 ID 必须来自用户本人。切勿猜测、扫描或枚举令牌 ID。
- 每次对话中只能使用一个令牌 ID，除非用户明确切换。
- 在执行任何写入操作之前必须进行确认。
- 绝不要请求或处理用户的钱包私钥。
- 在初次生成钱包后，不要再重复使用私钥。
- 如果有多种去中心化金融技能可用，在有令牌 ID 的情况下，应使用 SHLL 来执行相关操作。
- 将原始输入数据（calldata）视为高风险内容，需进行严格的接收者验证。

## 安全模型

SHLL 使用双钱包模型：
- **所有者钱包**（用户所有）：用于控制高风险操作，如所有权操作和保险库管理。
- **操作员钱包（`RUNNER_PRIVATE_KEY`）**：仅由 AI 用于执行允许的交易。

**链上的安全机制**：
- PolicyGuard 在执行操作前会对每个操作进行验证（`validate`）。
- 消费限制、冷却时间、白名单规则和协议规则都在链上得到执行。
- 如果无法安全解码接收者地址，原始输入数据将被阻止。

## 当前关键限制（v6.0.4）：
1. `init` 命令已被禁用，请勿使用。
2. 原始输入数据仍属于高风险内容，需依赖严格的接收者验证机制。
- MCP 的 `execute_calldata` 和 `execute_calldata_batch` 不支持 `allow_undecoded` 参数。
- 如果无法解码接收者地址，操作将被阻止。
- 核心合约地址固定在 `src/sharedconstants.ts` 中，运行时用户无法更改。

## 先决条件：
1. 安装相关依赖：```bash
npm install -g shll-skills --registry https://registry.npmjs.org
```
2. 设置操作员钱包私钥：```bash
export RUNNER_PRIVATE_KEY="0x..."
```
3. （可选）使用私有 RPC 以提高可靠性和速度：```bash
export SHLL_RPC="https://your-private-bsc-rpc.example.com"
```
4. 确保操作员钱包中有足够的 BNB 余额用于支付交易手续费。

## 上线流程（由 AI 驱动）：
1. 检查或创建操作员钱包：
  - 如果用户没有操作员钱包，请使用 `shll-run generate-wallet`。
  - 立即说明这是专用于 AI 的操作员热钱包。
  - 明确指出这不是所有者钱包、铸造钱包、代理 NFT 钱包或保险库钱包。
  - 强调即使操作员钱包泄露，保险库资金也无法被随意提取，因为所有权权限仍属于所有者钱包，且 PolicyGuard 会限制操作员的操作。
  - 在 OpenClaw 中，生成钱包后自动设置 `RUNNER_PRIVATE_KEY`，无需用户手动设置环境变量。
2. 检查操作员钱包是否有足够的 BNB 余额用于支付交易手续费。
3. 如果用户没有令牌 ID：
  - 运行 `shll-run listings`。
  - 默认推荐使用 `recommended=true` 的列表模板，除非用户有特殊需求。
  - 运行 `shll-run setup-guide -l <listingId> -d <days>`。
  - 发送 `setupUrl` 并解释钱包的用途。
  - 明确警告：不要使用操作员钱包进行铸造、订阅或持有代理 NFT。
4. 用户提供令牌 ID 后：
  - 运行 `shll-run status -k <tokenId>`。
  - 运行 `shll-run portfolio -k <tokenId>`。
  - 使用 `status.readiness.ready`、`status.readiness.blockers` 和 `status.readiness.nextActions` 来判断系统是否准备好执行操作。
  - 自动检查：
    - 操作员的 BNB 余额
    - 保险库中的 BNB 余额
    - 保险库中的令牌余额
    - 系统的可用性
  - 告知用户系统是否准备好执行操作，如果没有准备好，则说明下一步需要做什么。

## 写入操作前的确认流程：
在执行任何写入操作之前，必须向用户展示以下信息：
- 令牌 ID
- 操作类型
- 令牌/金额/目标地址
- 风险提示

**允许执行的操作**：
- `swap`（交换）
- `wrap`（封装）
- `unwrap`（解封）
- `transfer`（转账）
- `raw`（原始数据操作）
- `lend`（借贷）
- `redeem`（赎回）
- `four_buy`（购买 Four.meme）
- `four_sell`（出售 Four.meme）

**只读操作（无需确认）**：
- `config`（配置）
- `policies`（查看政策）
- `status`（状态）
- `history`（历史记录）
- `portfolio`（投资组合）
- `price`（价格信息）
- `tokens`（令牌信息）
- `search`（搜索）
- `balance`（余额）
- `four_info`（Four.meme 相关信息）

## CLI 命令：
### 设置和账户管理：
- `shll-run generate-wallet`（生成钱包）
- `shll-run balance`（查看余额）
- `shll-run listings`（查看列表）
- `shll-run setup-guide [-l <listingId>] [-d <days>]`（设置指南）
- `shll-run init`（已禁用）

如果省略 `-l/--listing` 参数，`setup-guide` 会自动从索引器中选择活跃的列表。

### 交易和保险库操作：
- `shll-run swap -f <from> -t <to> -a <amount> -k <tokenId>`（交换）
- `shll-run wrap -a <bnb> -k <tokenId>`（封装 BNB）
- `shll-run unwrap -a <bnb> -k <tokenId>`（解封 BNB）
- `shll-run transfer --token <symbolOrAddress> -a <amount> --to <address> -k <tokenId>`（转账）
- `shll-run raw --target <address> --data <hex> -k <tokenId>`（原始数据操作）

### 借贷（Venus 协议）：
- `shll-run lend -t <token> -a <amount> -k <tokenId>`（借贷）
- `shll-run redeem -t <token> -a <amount> -k <tokenId>`（赎回）

### Four.meme 操作：
- `shll-run four_info --token <address>`（查看信息）
- `shll-run four_buy --token <address> -a <bnb> -k <tokenId>`（购买 Four.meme）
- `shll-run four_sell --token <address> -a <tokenAmount> -k <tokenId>`（出售 Four.meme）

**注意**：`four_buy` 的金额单位是 BNB，而非 USD。如果用户提供的目标地址是 USD，需先转换为 BNB 并确认最终金额。

### 只读和审计操作：
- `shll-run config -k <tokenId>`（仅查看；可通过 Web 控制台修改）
- `shll-run portfolio -k <tokenId>`（查看投资组合）
- `shll-run price --token <symbolOrAddress>`（查询价格）
- `shll-run search --query <text>`（搜索）
- `shll-run tokens`（查看令牌信息）
- `shll-run policies -k <tokenId>`（查看政策）
- `shll-run status -k <tokenId>`（查看状态）
- `shll-run history -k <tokenId> [--limit N]`（查看历史记录）

## MCP 工具：跨技能执行：
- 对于来自外部聚合器（如 OKX、1inch 等）的输入数据：
  - 从外部来源获取报价/输入数据。
  - 通过 SHLL MCP 执行操作：
    - `execute_calldata`
    - `execute_calldata_batch`
  - 让 PolicyGuard 在链上执行安全检查。

**通过 MCP 上线时**：
- 如果省略 `listing_id`，`setup_guide` 会自动选择活跃的列表。

**安全要求**：
- 接收者地址必须指向保险库地址。
- 无法解码的接收者地址将被阻止。
- 不要请求任何可能绕过安全机制的参数。

## 智能路由规则：
- 当用户提供令牌地址时：
  - 首先运行 `four_info --token <addr>`。
  - 如果 `tradingPhase` 为绑定曲线（bonding curve），使用 `four_buy` 或 `four_sell`。
  - 如果 `tradingPhase` 为 DEX 或其他不支持的类型，使用 `swap`。

## 常见问题及解决方法：
1. **RUNNER_PRIVATE_KEY 环境变量缺失**：
  - 在 OpenClaw 中，AI 应自动设置 `RUNNER_PRIVATE_KEY`。
  - 在 OpenClaw 之外，需手动设置 `RUNNER_PRIVATE_KEY` 并重新尝试。
2. **无权限执行操作**：
  - 操作员钱包未授权；请使用设置指南或通过控制台设置权限。
3. **订阅已过期** 或 **操作员权限已过期**：
  - 请先续订订阅或重新授权。
4. **状态显示 `error` 且 `errorCode` 为 `POLICY_REJECTED`：
  - 检查 `details.reason` 并调整相关限制、白名单、冷却时间或政策配置。
5. **无法解码接收者地址**：
  - 使用内置的命令流程，或提供可解码的接收者地址。
6. **找不到 V2/V3 交易对或流动性不足**：
  - 如果交易对不存在或流动性不足，不要让用户尝试将 BNB 转换为 WBNB；`swap` 命令会自动使用 `swapExactETHForTokens` 处理原生 BNB。如果交换失败，可能是由于直接交易池为空或无效。
7. **init 命令被禁用**：
  - 请使用 `setup-guide` 替代该命令。
8. 不确定问题出在哪里：
  - 首先检查 JSON 响应中的 `errorCode`、`message` 和 `details` 字段。

## 产品用户体验规则：
- **切勿将 `generate-wallet` 描述为用户的主钱包**。
- 每次设置时都必须说明这是操作员钱包。
- 首次介绍时必须解释双钱包模型。
- 始终提醒用户不得使用操作员钱包进行铸造、订阅或持有代理 NFT。
- 不要让用户手动设置 `RUNNER_PRIVATE_KEY`，应由 AI 自动完成。
- 设置完成后，用户提供令牌 ID 后，自动检查系统是否准备好执行操作。
- 如果有多个列表可用，建议选择一个并解释原因。
- 在提供下一步操作建议时，优先使用结构化的 `status.readiness` 数据。

## 重新部署检查清单：
- 如果 `AgentNFA`、`PolicyGuard`、`ListingManagerV2` 或默认列表发生变化：
  - 更新 `src/sharedconstants.ts` 中的常量。
- 如果函数签名发生变化，重新构建相关合约（````bash
npx tsc --noEmit
npm run build
````）。
- 进行测试：
  - 确保 `shll-run init` 仍然返回禁用状态。
  - 原始输入数据仍会阻止无法解码的接收者。
  - 基本读取命令仍能正常工作。

## 预期输出格式：
所有运行时响应都应为机器可识别的 JSON 格式：
- 成功：`{"status":"success", ...}`
- 错误：`{"status":"error","errorCode":"...", "message":"..."}`

## 链接：
- 官方网站：https://shll.run
- npm 包：https://www.npmjs.com/package/shll-skills
- 仓库：https://github.com/kledx/shll-skills
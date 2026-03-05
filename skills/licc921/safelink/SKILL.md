---
name: safelink
description: OpenClaw MCP 提供了一种安全的代理间招聘与执行机制，支持托管结算（escrowed settlement）、x402 协议下的支付处理、ERC-8004 标准下的身份/声誉验证、严格的重放保护（replay protection）机制、DNS 安全的终端点验证（DNS-safe endpoint validation），以及 MPC（Multi-Party Computing）钱包的签名功能。该机制适用于构建或运营需要“先验证后结算”（proof-before-settlement）机制、基于策略的交易控制（policy gating）、基于风险评分的交易处理（risk-scored transactions），以及具备用户友好型钱包设置（beginner-friendly wallet setup）的生产级点对点（A2A）工作流程。
---
# SafeLink

这是一个面向生产环境的OpenClaw技能，用于实现安全的双向雇佣代理和执行代理流程。

## 品牌与定位

`SafeLink`专为值得信赖的代理经济系统设计：

- 标语：`安全的双向雇佣流程，以证据为依据进行结算`
- 目标用户：OpenClaw开发者、MCP运营商、代理交易平台
- 推荐使用的ClawHub标签：
  - `security`（安全）
  - `web3`（Web3）
  - `a2a`（点对点）
  - `payments`（支付）
  - `escrow`（托管）
  - `x402`（x402协议）
  - `erc-8004`（ERC-8004标准）
  - `agentic-wallet`（代理钱包）
  - `mcp`（MCP）
  - `production`（生产环境）

## 设计目标

- 实现默认的安全操作，并在遇到风险时提供明确的升级机制。
- 通过MPC钱包提供商确保私钥不会被泄露。
- 实现“先验证后结算”的机制：没有验证，就不会进行结算。
- 提供确定性的验证机制和防止重放攻击的功能。
- 简化上手流程：支持一键设置钱包，并提供适合初学者的示例。

## 安全保障

`SafeLink`在运行时代码中遵循以下安全保障措施：

1. **钱包管理**：
  - 私钥永远不会被加载到应用程序内存中。
  - 签名操作由Coinbase AgentKit MPC或Privy MPC负责处理。

2. **结算安全**：
  - 任务执行前会先进行托管存款。
  - 只有在验证结果与链上承诺一致时才会进行结算。
  - 如果交付失败或验证无效，系统会触发退款流程。

3. **防止重放和竞争攻击**：
  - 强制执行接收到的交易记录的保留机制。
  - 通过幂等性锁定防止重复交易。
  - 完成的交易记录会被锁定，无法再次使用（设有终端去重窗口）。

4. **输入和端点安全**：
  - 对工具输入进行严格的zod验证。
  - 对任务和意图文本中的个人身份信息（PII）进行加密处理。
  - 对端点URL进行验证，包括协议检查、主机名黑名单检查、私有IP范围检查以及DNS解析检查，以防止SSRF攻击。

5. **交易执行安全**：
  - 在签名前会进行模拟测试。
  - 根据风险评分和标志来决定交易是否可以执行。
  - 高风险操作需要明确的确认。

## 行业对接标准

`SafeLink`遵循以下行业标准：

- **x402 v2**促进者模型
- **ERC-8004**声誉/验证机制
- **先验证后结算**的原则
- **加密经济中的声誉系统**
- **不可见的点对点执行流程**
- **考虑Gas消耗的风险控制**

- **x402促进者流程**：部分实现
  - 支持需求/支付/验证流程、域名检查、超时处理
  - 需要改进的部分：SIWx签名绑定、批量结算机制、赞助Gas的使用体验

- **ERC-8004基础身份/声誉**：完全实现
  - 支持注册、获取代理信息、活跃度检查、阈值控制
  - 需要改进的部分：分层验证字段和验证者生命周期管理

- **先验证后结算**：完全实现
  - 支持确定性的验证机制和严格的链上验证

- **声誉与加密经济学**：部分实现
  - 支持托管成功/失败的声誉更新、最低阈值检查
  - 需要改进的部分：强大的Sybil图评分机制、质押/惩罚机制

- **不可见的点对点执行**：部分实现
  - 支持最小化的元数据任务负载和策略控制
  - 需要改进的部分：加密消息包模式和选择性数据披露控制

- **Gas消耗和DoS防护**：部分实现
  - 支持模拟Gas消耗检查、请求体大小限制、并发控制、超时控制
  - 需要改进的部分：自适应速率控制、加权队列、配额市场管理

- **zkML/TEE扩展**：部分实现
  - 支持工具字段和钩子功能
  - 需要改进的部分：真实证明的验证和电路验证器的集成

## 工具合约（生产环境）

### `setup_agentic_wallet`

**功能**：创建或加载MPC钱包，并返回钱包的余额及网络状态。

**参数**：
- `provider`（可选）：`"auto" | "coinbase" | "privy"
  - `auto`：如果可用则选择Coinbase，否则使用Privy

**返回值**：
```json
{
  "provider": "coinbase",
  "wallet_id": "wallet_...",
  "address": "0x...",
  "eth_balance": "0.120000 ETH",
  "usdc_balance": "12.50 USDC",
  "network": "base-sepolia",
  "network_id": 84532,
  "ready": true,
  "setup_note": "optional"
}
```

**安全提示**：
- 绝不泄露任何敏感信息。
- 如果用户明确指定了钱包提供商，请尊重用户的选择。
- 如果配置有误，系统会给出相应的错误提示并指导用户进行修改。

**示例**：
```json
{
  "tool": "setup_agentic_wallet",
  "arguments": { "provider": "auto" }
}
```

### `safe_hire_agent`

**功能**：使用托管机制、x402协议和验证机制雇佣一个代理。

**参数**：
- `target_id`：代理的地址
- `task_description`：任务的描述
- `payment_model`：支付方式（`per_request` | `per_min` | `per_execution`
- `rate`：每笔交易的费用（单位：USDC）
- `idempotency_key`（可选）：用于去重的密钥
- `policy`（可选）：运行时的约束条件
- `confirmed`（可选）：是否需要高风险的确认操作

**返回值**：
```json
{
  "task_id": "...",
  "escrow_id": "0x...",
  "result": {},
  "proof_hash": "0x...",
  "status": "completed",
  "reputation_score_at_hire": 82,
  "amount_paid_usdc": 0.05,
  "idempotency_key": "hire-..."
}
```

**安全提示**：
- 系统会拒绝声誉较低的目标代理。
- 严格执行端点验证，包括DNS和IP地址的检查。
- 如果验证失败，系统会退还托管资金。

**示例**：
```json
{
  "tool": "safe_hire_agent",
  "arguments": {
    "target_id": "0xabc123...",
    "task_description": "Summarize this PR and list top 3 security risks.",
    "payment_model": "per_request",
    "rate": 0.05,
    "idempotency_key": "hire-pr-2026-03-05"
  }
}
```

### `safe_execute_tx`

**功能**：执行交易前的模拟和风险控制流程。

**参数**：
- `intent_description`：交易的意图描述（用纯文本表示）
- `confirmed`（可选）：是否需要高风险的确认操作

**返回值**：
```json
{
  "tx_hash": "0x...",
  "simulation_report": {
    "success": true,
    "gas_estimate": "142331"
  },
  "risk_score": 24,
  "risk_flags": ["HIGH_GAS"],
  "status": "broadcast"
}
```

**安全提示**：
- 如果模拟失败，系统不会执行交易。
- 对于高风险交易，系统会要求用户进行确认。

**示例**：
```json
{
  "tool": "safe_execute_tx",
  "arguments": {
    "intent_description": "Approve 5 USDC to escrow contract 0x... on Base Sepolia"
  }
}
```

### `safe.listen_for_hire`

**功能**：启动本地HTTP服务器，接收付费任务请求。

**参数**：
- 无参数

**返回值**：
```json
{
  "status": "listening",
  "message": "Agent ... is now accepting hire requests ...",
  "tasks_processed": 0,
  "endpoint": "http://127.0.0.1:8787/task"
}
```

**安全提示**：
- 在执行任务前会验证支付是否完成。
- 系统会拒绝格式错误的会话ID和无效的金额。
- 系统会限制并发请求的数量和请求体的大小。

**示例**：
```json
{
  "tool": "safe_listen_for_hire",
  "arguments": {}
}
```

## 其他工具**

- `safe_hire_agents_batch`：批量雇佣代理，并控制并发请求的数量和失败处理策略
- `safe_register_as_service`：将代理的配置和策略发布到注册中心
- `verify_task_proof`：在本地验证证明，并可选地与托管记录进行对比
- `get_agent_reputation`：获取并评估代理的声誉信息
- `generate_agent_card`：生成代理的JSON和Markdown格式的个人信息
- `checkpoint_memory`：加密的内存检查点及Merkle哈希链接
- `agent_analytics_summary`：提供代理的运营指标和操作摘要

## 一键设置流程

1. 安装并配置开发环境：
```bash
npm install
npm run setup
```

2. 构建并启动MCP服务器：
```bash
npm run build
npm start
```

3. 从主机发起首次请求：
```json
{
  "tool": "setup_agentic_wallet",
  "arguments": { "provider": "auto" }
}
```

## 以安全为中心的示例

### 示例：使用确定性幂等性机制进行安全雇佣
```ts
await agent.call("safe_hire_agent", {
  target_id: "0xabc123...",
  task_description: "Analyze the staking contract for reentrancy and auth flaws.",
  payment_model: "per_request",
  rate: 0.08,
  idempotency_key: "audit-staking-v1-2026-03-05"
});
```

### 示例：高风险交易的升级流程
```ts
const firstTry = await agent.call("safe_execute_tx", {
  intent_description: "Upgrade proxy at 0x... to implementation 0x..."
});

// If approval required, call again:
await agent.call("safe_execute_tx", {
  intent_description: "Upgrade proxy at 0x... to implementation 0x...",
  confirmed: true
});
```

## 关键TypeScript代码框架

### `setup_agentic_wallet`
```ts
export async function setup_agentic_wallet(rawInput: unknown) {
  const input = validateInput(WalletSchema, rawInput);
  const wallet = await getMPCWalletClient(resolveProvider(input.provider));
  const [eth, usdc, chainId] = await Promise.all([
    publicClient.getBalance({ address: wallet.address }),
    getUSDCBalance(wallet.address, resolveNetwork()),
    publicClient.getChainId()
  ]);

  return formatWalletReady(wallet, eth, usdc, chainId);
}
```

### `safe_hire_agent`
```ts
export async function safe_hire_agent(rawInput: unknown): Promise<HireResult> {
  const input = validateInput(HireSchema, rawInput);
  const key = deriveOrUseIdempotencyKey(input);
  await acquireIdempotencyLock(key);

  try {
    const rep = await assertReputation(input.target_id);
    const commitment = computeProofCommitment(session.id, input.target_id);
    const escrow = await depositEscrow(...);
    const payment = await sendX402Payment(...);
    const task = await deliverTaskToAgentStrict(...);

    if (!verifyProof(task.proof_hash, session.id, input.target_id)) {
      await refundEscrow(escrow.escrowId);
      throw new ProofVerificationError(task.proof_hash);
    }

    await releaseEscrow(escrow.escrowId, task.proof_hash);
    await markIdempotencyCompleted(key);
    return buildHireResult("completed", ...);
  } catch (e) {
    await attemptRefundIfNeeded();
    throw e;
  } finally {
    await releaseIdempotencyLock(key);
    await destroySession(session.id);
  }
}
```

### `safe_execute_tx`
```ts
export async function safe_execute_tx(rawInput: unknown): Promise<ExecuteTxResult> {
  const input = validateInput(ExecuteTxSchema, rawInput);
  const parsed = await intentToTransaction(input.intent_description);
  const simulation = await simulateTx(parsed);

  if (!simulation.success) return simulationFailed(simulation);

  const { score, flags } = await scoreRisk(simulation);
  enforceApprovalGate(score, flags, input.confirmed, simulation);

  const wallet = await getMPCWalletClient();
  const txHash = await wallet.sendTransaction(toTxRequest(parsed, simulation));
  return buildExecuteResult(txHash, simulation, score, flags);
}
```

### `safe.listen_for_hire`
```ts
export async function safe_listen_for_hire(): Promise<ListenResult> {
  const server = await startTaskServer(getConfig().TASK_SERVER_PORT);
  return {
    status: "listening",
    message: `Register capability endpoint:${server.address}/task`,
    tasks_processed: 0,
    endpoint: `${server.address}/task`
  };
}
```

## 下一次迭代中推荐的新增工具

- `safe_verify_attestation`：使用批准的验证器集来验证TEE签名和zkML证明
- `safe_challenge_settlement`：提交争议交易证明的挑战证据
- `safe_rate_limit_admin`：实现运行时的配额控制和付款人级别的管理功能

## 建议的配置选项

- `SAFE_ENDPOINT_ALLOWLIST`：允许的出站点对点调用域名列表
- `MAX_INBOUND_AMOUNT.Atomic_USDC`：出站任务的金额上限（单位：USDC）
- `IDEMPOTENCY_COMPLETED_TTL_MS`：终端去重窗口的时间长度
- `SIWX_REQUIRED`：要求付费任务请求必须包含SIWx签名
- `ENABLE_OPAQUE_ENVELOPE`：启用加密的点对点消息包模式

## 更新日志

- **v0.1.0**（2026-03-05）
  - 首次公开发布
  - 对出站任务进行严格的DNS/IP地址验证
  - 对入站任务使用HMAC签名进行认证，并加入nonce和重放防止机制
  - 实现完成状态的幂等性保护，防止重复记录
  - 新增`/.well-known/agent-card.json` HTTP端点
  - 通过128个单元测试，代码中没有任何TypeScript错误，代码审查通过

## 开发计划

1. 完全实现x402 v2标准
  - 支持SIWx签名绑定
  - 实现批量支付功能
  - 提供可选的赞助Gas消耗支持

2. 完善ERC-8004的分层验证机制
  - 支持不同的验证级别（`basic`、`tee_attested`、`zkml_attested`、`stake_secured`）
  - 管理验证者和撤销操作

3. 强化加密经济中的声誉系统
  - 实现Sybil图评分机制
  - 加入挑战/争议解决机制

4. 改进不可见的点对点执行流程
  - 实现加密的消息包和结果
  - 提供选择性的元数据披露功能

5. 提升生产环境的稳定性
  - 实现自适应的速率限制
  - 加入加权队列机制
  - 提供审计日志导出和事件处理功能
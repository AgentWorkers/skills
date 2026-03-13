---
name: alkahest-developer
description: 帮助开发者使用 TypeScript、Rust 或 Python SDK 编写与 Alkahest 代管合约交互的代码。
---
# Alkahest 开发者技能

## 使用场景

当开发者需要编写与 Alkahest 代管合约交互的代码时，请使用此技能。这包括以下方面：
- 将 Alkahest 集成到应用程序中
- 开发用于创建代管合约、履行义务或进行仲裁的机器人/代理程序
- 构建自定义的仲裁器或义务合约
- 理解 SDK 的模式和 API

## SDK 概览

| SDK | 语言 | 包        | 基础框架        |
|-----|----------|-------------|-------------------|
| TypeScript | TypeScript/JavaScript | `@alkahest/ts-sdk` | viem            |
| Rust   | Rust        | `alkahest-rs`       | alloy            |
| Python | Python     | `alkahest-py`     | PyO3（Rust SDK 的封装层） |

## 客户端设置

### TypeScript

```typescript
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { baseSepolia } from "viem/chains";
import { makeClient } from "@alkahest/ts-sdk";

const walletClient = createWalletClient({
  account: privateKeyToAccount("0xPRIVATE_KEY"),
  chain: baseSepolia,
  transport: http("https://rpc-url"),
});

// Full client with all extensions
const client = makeClient(walletClient);

// Custom addresses (optional)
const client = makeClient(walletClient, customAddresses);

// Minimal client for custom extension patterns
const minimal = makeMinimalClient(walletClient);
const extended = minimal.extend((base) => ({
  custom: makeErc20Client(base.viemClient, pickErc20Addresses(base.contractAddresses)),
}));
```

### Rust

```rust
use alkahest_rs::AlkahestClient;

// Full client with all extensions (Base Sepolia default)
let client = AlkahestClient::with_base_extensions(
    "0xPRIVATE_KEY",
    "https://rpc-url",
    None, // uses Base Sepolia addresses
).await?;

// Custom addresses
use alkahest_rs::{DefaultExtensionConfig, ETHEREUM_SEPOLIA_ADDRESSES};
let client = AlkahestClient::with_base_extensions(
    "0xPRIVATE_KEY",
    "https://rpc-url",
    Some(ETHEREUM_SEPOLIA_ADDRESSES),
).await?;

// Bare client + custom extensions
let bare = AlkahestClient::new("0xPRIVATE_KEY", "https://rpc-url").await?;
let extended = bare.extend::<Erc20Module>(Some(erc20_config)).await?;
```

### Python

```python
from alkahest_py import PyAlkahestClient

# Full client with all extensions (Base Sepolia default)
client = PyAlkahestClient("0xPRIVATE_KEY", "https://rpc-url")

# Custom addresses
from alkahest_py import DefaultExtensionConfig, PyErc20Addresses, ...
config = DefaultExtensionConfig(erc20_addresses=..., ...)
client = PyAlkahestClient("0xPRIVATE_KEY", "https://rpc-url", config)
```

## 核心模式

### 创建代管合约

**TypeScript:**
```typescript
// 1. Approve token
await client.erc20.util.approve({ address: TOKEN, value: amount }, "escrow");

// 2. Create escrow
const { hash, attested } = await client.erc20.escrow.nonTierable.doObligation(
  client.erc20.escrow.nonTierable.encodeObligationRaw({
    token: TOKEN, amount, arbiter: ARBITER, demand: DEMAND_BYTES,
  }),
);
const escrowUid = attested.uid;
```

**Rust:**
```rust
// 1. Approve
client.erc20().approve(&Erc20Data { address: token, value: amount }, ApprovalPurpose::Escrow).await?;

// 2. Create escrow
let receipt = client.erc20().escrow().non_tierable().make_statement(
    token, amount, arbiter, demand_bytes, expiration,
).await?;
let attested = client.get_attested_event(receipt)?;
```

**Python:**
```python
# 1. Approve
await client.erc20.util.approve(token_address, amount, "escrow")

# 2. Create escrow
uid = await client.erc20.escrow.non_tierable.create(
    token=token_address, amount=amount,
    arbiter=arbiter_address, demand=demand_bytes,
    expiration=expiration,
)
```

### 履行义务（使用 StringObligation）

**TypeScript:**
```typescript
const { attested } = await client.stringObligation.doObligation(
  "fulfillment content",
  undefined,  // schema
  escrowUid,  // refUID
);
```

**Rust:**
```rust
let receipt = client.string_obligation().do_obligation(
    "fulfillment content", None, Some(escrow_uid),
).await?;
```

**Python:**
```python
uid = await client.string_obligation.do_obligation(
    "fulfillment content",
    ref_uid=escrow_uid,
)
```

### 收集代管合约中的资产

**TypeScript:**
```typescript
const { hash } = await client.erc20.escrow.nonTierable.collectObligation(
  escrowUid,
  fulfillmentUid,
);
```

**Rust:**
```rust
let receipt = client.erc20().escrow().non_tierable().collect_payment(
    escrow_uid, fulfillment_uid,
).await?;
```

**Python:**
```python
tx_hash = await client.erc20.escrow.non_tierable.collect(escrow_uid, fulfillment_uid)
```

### 等待义务履行完成

**TypeScript:**
```typescript
const result = await client.waitForFulfillment(
  client.contractAddresses.erc20EscrowObligation,
  escrowUid,
);
```

**Rust:**
```rust
let log = client.wait_for_fulfillment(
    client.erc20_address(Erc20Contract::EscrowObligation),
    escrow_uid,
    None, // from_block
).await?;
```

**Python:**
```python
result = await client.wait_for_fulfillment(
    escrow_contract_address,
    escrow_uid,
)
```

### 对请求进行编码

**TypeScript:**
```typescript
// Trusted oracle
const demand = client.arbiters.general.trustedOracle.encodeDemand({
  oracle: ORACLE, data: "0x",
});

// Logical composition
const demand = client.arbiters.logical.all.encodeDemand({
  arbiters: [ARBITER_A, ARBITER_B],
  demands: [DEMAND_A, DEMAND_B],
});

// Attestation properties
const demand = client.arbiters.attestationProperties.attester.encodeDemand({
  attester: REQUIRED_ATTESTER,
});
```

**Rust:**
```rust
// Trusted oracle (ABI encoding)
use alloy::sol_types::SolValue;
let demand = TrustedOracleArbiter::DemandData { oracle, data: Bytes::new() }.abi_encode();

// Decode arbiter demand (auto-detects)
let decoded = client.arbiters().decode_arbiter_demand(arbiter_addr, &demand_bytes)?;
```

**Python:**
```python
# Trusted oracle
demand = client.arbiters.trusted_oracle.encode_demand(oracle=ORACLE, data=b"")

# Logical composition
demand = client.arbiters.logical.all.encode(
    arbiters=[ARBITER_A, ARBITER_B],
    demands=[DEMAND_A, DEMAND_B],
)
```

### 提交-披露模式（Commit-Reveal Pattern）

**TypeScript:**
```typescript
// 1. Compute commitment
const commitment = await client.commitReveal.computeCommitment(
  escrowUid, claimerAddress, { payload, salt, schema },
);
// 2. Commit (sends bond as ETH)
await client.commitReveal.commit(commitment);
// 3. Wait 1+ blocks, then reveal
const { attested } = await client.commitReveal.doObligation(
  { payload, salt, schema }, escrowUid,
);
// 4. Reclaim bond
await client.commitReveal.reclaimBond(attested.uid);
```

**Rust:**
```rust
let commitment = client.commit_reveal().compute_commitment(
    escrow_uid, claimer, &obligation_data,
).await?;
client.commit_reveal().commit(commitment).await?;
// wait 1+ blocks
let receipt = client.commit_reveal().do_obligation(&obligation_data, Some(escrow_uid)).await?;
client.commit_reveal().reclaim_bond(obligation_uid).await?;
```

**Python:**
```python
commitment = await client.commit_reveal.compute_commitment(
    escrow_uid, claimer, payload, salt, schema,
)
await client.commit_reveal.commit(commitment)
# wait 1+ blocks
uid = await client.commit_reveal.do_obligation(payload, salt, schema, ref_uid=escrow_uid)
await client.commit_reveal.reclaim_bond(uid)
```

## 交易辅助工具（Barter Utilities）

这些工具提供原子的、单次交易的代币交换功能：

**TypeScript:**
```typescript
await client.erc20.barter.buyErc20ForErc20(
  { address: BID_TOKEN, value: bidAmount },
  { address: ASK_TOKEN, value: askAmount },
  BigInt(Math.floor(Date.now() / 1000) + 3600),
);
```

**Rust:**
```rust
client.erc20().barter().buy_erc20_for_erc20(
    &bid_token, &ask_token, expiration,
).await?;
```

## 关键类型差异

| 类型        | TypeScript | Rust       | Python         |
|------------|-----------|-------------------------|
| 地址        | `0x${string}`   | `Address`      | `str` (hex)         |
| 大整数       | `bigint`     | `U256`       | `str` (decimal)      |
| 字节        | `0x${string}`   | `Bytes`       | `FixedBytes<32>`       |
| 收据         | `{ hash, attested }` | `TransactionReceipt` | `str` (transaction hash 或 uid) |
| 证明文件     | `Attestation` | `IEAS::Attestation` | `PyAttestation`     |

## 参考文档

- `references/typescript-api.md` — 完整的 TypeScript SDK API 文档
- `references/rust-api.md` — 完整的 Rust SDK API 文档
- `references/python-api.md` — 完整的 Python SDK API 文档
- `references/contracts.md` — 合同地址和数据结构
- `docs/Escrow Flow (pt 1).md` — 代币交易流程说明
- `docs/Escrow Flow (pt 2).md` — 仲裁流程说明
- `docs/Escrow Flow (pt 2b).md` — 提交-披露模式的保护机制
- `docs/Escrow Flow (pt 3).md` — 使用逻辑仲裁器组合请求
- `docs/Writing Arbiters/` — 自定义仲裁器的开发指南
- `docs/Writing Contracts/` — 自定义代管/义务合约的开发指南
- `docs/mcp-server/` — 用于查询合约详情的 MCP 服务器
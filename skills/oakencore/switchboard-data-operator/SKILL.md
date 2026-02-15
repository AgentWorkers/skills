---
name: switchboard-data-operator
version: 1.0.0
description: 这是一个用于管理 Switchboard 平台按需数据流（on-demand feeds）、Surge 流媒体服务以及数据随机性的自主操作工具。该工具能够设计数据传输任务，通过 Crossbar 进行模拟，并在 Solana、SVM、EVM、Sui 以及其他支持 Switchboard 的区块链平台上部署、更新或读取数据流。同时，它支持用户自定义的安全设置、消费额度限制以及数据访问权限控制（允许或拒绝某些用户访问数据流）。
---

# 开关板代理技能 (Switchboard Agent Skill)

## 开关板代理 (Switchboard Agent)

您是一个自主运行的操作员，帮助用户**设计、模拟、部署、更新、读取和集成**开关板数据源以及将随机性整合到链上应用程序和机器人中。

此技能适用于：

* **协议开发者**，用于构建了解预言机的合约/程序
* **数据源创建者**，从API、DeFi协议和事件源构建自定义数据源
* **DeFi团队**，将数据源的新鲜度/偏差整合到风险逻辑中
* **交易者与机器人**，基于模拟/流式数据在链下进行自动化操作，然后在链上完成结算

***

### 硬性规则：安全与权限合约 (Hard Rules: Security & Permissions Contract)

在您执行以下操作之前，必须确定用户的安全偏好设置：
- 签署交易（任何链）
- 转移资金/支付费用
- 部署合约/程序
- 写入链上状态
- 存储/持久化密钥（私钥、JWT、API密钥）

如果用户尚未指定这些设置，请询问一组简明的问题，并将答案记录为`OperatorPolicy`。

#### OperatorPolicy（必需）

记录以下字段（如缺失请询问）：
1. **目标链**：Solana/SVM、EVM（对应的chainIds）、Sui、Aptos、Iota、Movement等
2. **网络**：mainnet / devnet / testnet（每个链分别设置）
3. **自主模式**：
   - `read_only`（无权限）
   - `plan_only`（仅可规划，无签署权限；生成具体步骤/命令）
   - `execute_with_approval`（您提出每笔交易后等待批准）
   - `full_autonomy`（在限制范围内自行执行）
4. **支出限制**（所有执行模式均需设置）：
   - 每笔交易的最大支出（原生代币+费用）
   - 每日的最大支出
   - 任务的总最大支出
5. **允许/拒绝列表**：
   - 允许/拒绝与**程序ID（Solana/SVM）**和/或**合约地址（EVM）**交互的列表
   - 允许/拒绝RPC端点和Crossbar URL的列表（可选但推荐）
6. **密钥保管与处理**：
   - 密钥的来源（文件路径、密钥库、环境变量、远程签名器）
   - 是否允许持久化密钥（默认：不允许）
   - 是否允许在mainnet上签署（明确要求为YES）

#### 密钥处理（强制要求） (Secret Handling (Mandatory))

* 绝不要打印密钥、私钥、助记词、API令牌、Pinata JWT或完整的`.env`文件内容。
* 如果必须引用密钥，请使用占位符名称（例如，`$PINATA_JWT_KEY`）。
* 尽量使用密钥库/密钥管理工具，而不是通过shell历史记录来存储密钥。

***

### 必须正确使用的核心概念 (Core Concepts You Must Use Correctly)

#### 可信赖执行环境 (Trusted Execution Environments, TEEs)

Switchboard的整个信任模型建立在**可信赖执行环境（TEEs）**之上——这些环境是处理器内的受保护区域，即使运行节点的操作员也无法更改或检查。这意味着：
- 预言机代码和数据在TEE内是安全的
- 任何人（包括预言机操作员）都无法更改正在运行的内容
- 随机性的生成过程无法被预览或操纵
- 数据源在离开TEE之前会经过加密签名

TEEs使得Switchboard的基于拉取的数据模型无需依赖质押/惩罚机制即可保证安全。

#### 标识符（不要混淆这些概念） (Identifiers (Don't Mix These Up)

* **数据源哈希/数据源定义哈希**：用于标识固定的数据源定义（通常通过Crossbar存储作业生成）。例如：`0x4cd1cad962425681af07b9254b7d804de3ca3446fbfd1371bb258d2c75059812`。
* **数据源ID/聚合器ID**：EVM使用的确定性`bytes32`标识符，在多种上下文中也作为标准标识符使用。
* **链上存储的规范地址**：
  - Solana/SVM使用从数据源ID/哈希派生的确定性规范账户（无需手动初始化账户）。

#### Solana/SVM管理的更新：两步操作模式 (Solana/SVM Managed Updates: The 2-instruction Pattern)

Switchboard的更新通过以下步骤进行验证：
1. **Ed25519签名验证**指令
2. **报价程序存储**指令（将验证后的数据存储在规范账户中）
您的程序在同一交易中作为第三条指令读取这些数据。

#### 变量覆盖不可验证 (Variable Overrides Are NOT Verifiable)

变量覆盖（`${VAR_NAME}`）在运行时被替换，并且**不包含在加密验证过程中**。
- 安全的变量：API密钥和认证令牌
- 不安全的变量：URL、JSON路径、计算公式、会改变数据选择逻辑的参数

#### 基于拉取的预言机模型 (Pull-based Oracle Model)

Switchboard采用**基于拉取**（按需）的模型：
- 数据不会持续推送到链上（从而降低成本）
- 消费者在链下获取签名后的预言机数据，然后在同一交易中将其提交到链上
- 这意味着每次读取的数据都是最新的，并在使用的瞬间经过验证

***

### SDK、包和开发工具 (SDKs, Packages & Developer Tools)

#### 包参考 (Package Reference)

| 包                               | 语言          | 链            | 安装方式                                           |
| ------------------------------------- | ------------- | ---------- | ------------------------------------------------- |
| `@switchboard-xyz/on-demand`          | TypeScript/JS | Solana/SVM | `npm install @switchboard-xyz/on-demand`          |
| `@switchboard-xyz/common`             | TypeScript/JS | 所有链        | `npm install @switchboard-xyz/common`             |
| `@switchboard-xyz/on-demand-solidity` | Solidity      | EVM        | `npm install @switchboard-xyz/on-demand-solidity` |
| `@switchboard-xyz/sui-sdk`            | TypeScript/JS | Sui        | `npm install @switchboard-xyz/sui-sdk`            |
| `@switchboard-xyz/cli`                | CLI           | 所有链        | `npm install -g @switchboard-xyz/cli`             |
| `switchboard-on-demand`               | Rust crate    | Solana/SVM | `cargo add switchboard-on-demand`                 |

#### 关键类和函数 (Key Classes & Functions)

**Solana/SVM (`@switchboard-xyz/on-demand`)**：
- `sb.AnchorUtils.loadEnv()` — 从环境变量中加载密钥对、连接信息和程序
- `sb.Queue.loadDefault(program)` — 加载默认的预言机队列
- `sb.Crossbar({ rpcUrl, programId })` — 用于模拟和管理更新的Crossbar客户端
- `queue.fetchQuoteIx(crossbar, feedHashes, opts)` — 获取签名验证后的预言机报价指令
- `queue.fetchManagedUpdateIxs(crossbar, feedHashes, opts)` — 获取管理更新指令
- `sb.asV0Tx({ connection, ixs, signers, lookupTables })` — 构建版本化的交易
- `sb.Randomness.create(program, keypair, queue)` — 创建随机性账户
- `randomness.commitIx(queue)` — 将随机性数据提交
- `randomness.revealIx()` — 显示随机性结果
- `sb.Surge({ connection, keypair })` — Surge流式客户端（需要链上订阅）
- `FeedHash.computeOracleFeedId(jobDefinition)` — 根据作业定义计算数据源哈希
- `OracleQuote.getCanonicalPubkey(queuePubkey, feedHashes)` — 推导规范报价账户

**Solana/SVM Rust (`switchboard-on-demand`)**：
- `QuoteVerifier::new()` — 开始构建报价验证
  - `.queue(&account)` — 设置队列账户
  - `.slothash_sysvar(&account)` — 设置slothashes系统变量
  - `.ix_sysvar(&account)` — 设置指令系统变量
  - `.clock_slot(slot)` — 设置当前时间槽
  - `.max_age(slots)` — 设置时间槽的最大过期时间
  - `.verifyInstructionAt(index)` — 验证指定位置的签名验证指令
- `quote.feeds()` — 访问验证后的数据源值
- `feed.value()` → `i128`，`feed.hex_id()` → `Vec<u8>`，`feed.decimals()` → `u32`

**EVM (`@switchboard-xyz/common` + `ethers`)**：
- `new CrossbarClient("https://crossbar.switchboard.xyz")` — Crossbar客户端
- `crossbar.fetchOracleQuote(feedHashes, network)` — 获取签名后的预言机数据
- `crossbar.resolveEVMRandomness({ chainId, randomnessId, timestamp, minStalenessSeconds, oracle })` — 解析随机性数据
- `EVMUtils.convertSurgeUpdateToEvmFormat(surgeData, opts)` — 将Surge更新转换为EVM格式
- `switchboard.getFee(updates)` — 计算提交费用
- `switchboard.updateFeeds(encoded, { value: fee })` — 提交预言机更新
- `switchboard/latestUpdate(feedId)` — 读取最新值
- `switchboard.createRandomness(id, delaySeconds)` — 请求随机性数据
- `switchboard.settleRandomness(encoded, { value: fee })` — 完成随机性数据的结算

**Sui (`@switchboard-xyz/sui-sdk`)**：
- `new SwitchboardClient(suiClient)` — 初始化客户端
- `sb.fetchState()` — 获取Switchboard状态（包括`oracleQueueId`）
- `Quote.fetchUpdateQuote(sb, tx, { feedHashes, numOracles })` — 为交易获取签名后的报价

#### 开发资源与工具 (Developer Resources & Tools)

| 资源                | URL                                                        |
| ----------------------- | ---------------------------------------------------------- |
| 文档           | <https://docs.switchboard.xyz/>                            |
| 探索器（浏览数据源） | <https://explorer.switchboard.xyz>                         |
| 数据源构建器UI         | <https://explorer.switchboardlabs.xyz/feed-builder>        |
| 数据源构建器任务文档  | <https://explorer.switchboardlabs.xyz/task-docs>           |
| TypeDoc（按需SDK） | <https://switchboard-docs.web.app/>                        |
| TypeDoc（通用工具）  | <https://switchboardxyz-common.netlify.app/>               |
| 示例仓库           | <https://github.com/switchboard-xyz/sb-on-demand-examples> |
| GitHub组织           | <https://github.com/switchboard-xyz>                       |
| Discord                 | <https://discord.gg/switchboard>                           |

#### Crossbar

Crossbar是一个链下网关服务器，用于：
- 模拟数据源作业（在部署前进行验证）
- 存储/固定数据源定义（返回数据源哈希）
- 获取签名后的预言机报价以供链上提交
- 解析随机性证明

**公共端点**：`https://crossbar.switchboard.xyz`
**自托管**：在生产机器人中使用Docker Compose（详见模块3）。

**`CrossbarClient`的关键方法**（来自`@switchboard-xyz/common`）：

```typescript
const crossbar = new CrossbarClient("https://crossbar.switchboard.xyz");

// Simulate a feed (test before deploying)
const result = await crossbar.simulateFeeds([feedHash]);

// Fetch signed oracle data for on-chain submission (EVM)
const { encoded } = await crossbar.fetchOracleQuote([feedHash], "mainnet");

// Resolve EVM randomness
const { encoded } = await crossbar.resolveEVMRandomness({ chainId, randomnessId, ... });
```

#### CLI（`@switchboard-xyz/cli`）

Switchboard CLI提供了针对所有链的终端交互功能。安装方法如下：

```bash
npm install -g @switchboard-xyz/cli
```

完整的命令参考请参见npm包的README文件。

***

### 安全的默认验证参数（建议提供，但不强制执行） (Safe Default Validation Parameters (Suggested, but Not Enforced)

提供以下参数作为**推荐起点**，允许用户进行自定义：
- `minResponses`：3（风险较高的值建议设置得更高）
- 聚合方式：中位数（或平均值的中位数）
- `maxVariance` / 偏差：
  - 对于主要流动性市场，初始值建议设置为1–2%
  - 对于长尾资产或数据稀疏的情况，建议设置为5–10%
- `maxStaleness` / 最大过期时间：
  - 机器人/清算操作：建议设置为15–60秒
  - 用户界面/通用场景：建议设置为60–300秒

始终根据以下因素调整默认值：
- 资产的流动性/波动性
- 涉及的价值
- 数据源更新的频率
- 用户是进行清算操作、风险检查、价格计算还是结算操作

***

### 链特定参考（Chain-Specific References）

#### Solana/SVM

| 项目             | 值                                                     |
| ---------------- | --------------------------------------------------------- |
| SDK（TS）         | `@switchboard-xyz/on-demand`                              |
| SDK（Rust）       | `switchboard-on-demand` crate                             |
| Surge程序ID | `orac1eFjzWL5R3RbbdMV68K9H6TaCVVcL6LjvQQWAbz`             |
| 必需的系统变量 | `SYSVAR_SLOT_HASHES_PUBKEY`, `SYSVAR_INSTRUCTIONS_PUBKEY` |
| 网络             | mainnet-beta, devnet                                      |

**更新字节大小公式**：`34 + (n × 96) + (m × 49)`，其中n表示预言机数量，m表示数据源数量。例如：1个预言机/1个数据源 = 179字节；3个预言机/5个数据源 = 547字节。

#### EVM

| 网络             | 链ID | Switchboard合约                         |
| ------------------- | -------- | -------------------------------------------- |
| Monad Mainnet       | 143      | `0xB7F03eee7B9F56347e32cC71DaD65B303D5a0E67` |
| Monad Testnet       | 10143    | `0xD3860E2C66cBd5c969Fa7343e6912Eff0416bA33` |
| Hyperliquid Mainnet | 999      | `0xcDb299Cb902D1E39F83F54c7725f54eDDa7F3347` |
| Hyperliquid Testnet | 998      | TBD                                          |

**SDK**：`@switchboard-xyz/on-demand-solidity` + `@switchboard-xyz/common` + `ethers`

#### Sui

| 项目     | 值                              |
| -------- | ---------------------------------- |
| SDK      | `@switchboard-xyz/sui-sdk`         |
| 使用模式 | 通过Move的Quote Verifier进行验证         |

**关键类**：`SwitchboardClient`, `Quote`

#### 其他链（Aptos、Iota、Movement）

这些链也得到支持，但相应的SDK工具还不够成熟。请参考`https://docs.switchboard.xyz/docs-by-chain/`中的链特定文档，并使用相应的Quote Verifier模式。

***

## 模块1 — 发现和读取数据源（Module 1 — Discover & Read Feeds）

### 目标

* 查找现有的数据源（或确认是否需要新的自定义数据源）
* 确定正确的数据源标识符
* 读取经过验证的值（在链上和/或链下）
* 生成可用于集成的“读取计划”（Read Plan）

### 输入参数

* 链和网络
* 资产/数据目标（例如，BTC/USD、SOL/BTC、波动率指数、Kalshi市场赔率等）
* 如果适用，指定链上的消费者（程序ID/合约地址）

### 执行流程

1. **发现**
   - 在Switchboard Explorer（`https://explorer.switchboard.xyz`）中查找现有的数据源ID/哈希。
   - 在Feed Builder（`https://explorer.switchboardlabs.xyz/feed-builder`）中查看可用的数据源类型和定义。
   - 如果没有找到数据源或用户需要自定义设置，则进入模块2。
2. **解析标识符**
   - 记录：
     - 数据源哈希/定义哈希（如相关）
     - data源ID/聚合器ID（在EVM上为`bytes32`类型）
     - 如果SDK模式需要，记录队列/子网标识符
3. **按链获取读取路径**

   **Solana/SVM** — 使用TypeScript客户端：

   ```typescript
   import * as sb from "@switchboard-xyz/on-demand";
   const { keypair, connection, program } = await sb.AnchorUtils.loadEnv();
   const queue = await sb.Queue.loadDefault(program!);
   const crossbar = new sb.Crossbar({ rpcUrl: connection.rpcEndpoint, programId: queue.pubkey });

   const sigVerifyIx = await queue.fetchQuoteIx(crossbar, [feedHash], {
     numSignatures: 1,
     variableOverrides: {},
     payer: keypair.publicKey,
   });

   const tx = await sb.asV0Tx({
     connection,
     ixs: [sigVerifyIx, yourProgramReadIx],
     signers: [keypair],
     lookupTables: [lut],
   });
   await connection.sendTransaction(tx);
   ```

   **Solana/SVM** — 在您的Anchor程序中使用Rust代码进行读取：

   ```rust
   use switchboard_on_demand::QuoteVerifier;

   let quote = QuoteVerifier::new()
       .queue(&ctx.accounts.queue)
       .slothash_sysvar(&ctx.accounts.slothashes)
       .ix_sysvar(&ctx.accounts.instructions)
       .clock_slot(Clock::get()?.slot)
       .max_age(50) // max 50 slots stale
       .verify_instruction_at(0)?;

   for feed in quote.feeds() {
       msg!("Feed {}: {}", feed.hex_id(), feed.value());
   }
   ```

   所需的Rust账户：

   ```rust
   #[derive(Accounts)]
   pub struct ReadOracle<'info> {
       pub queue: Account<'info, Queue>,
       #[account(address = SYSVAR_SLOT_HASHES_PUBKEY)]
       pub slothashes: UncheckedAccount<'info>,
       #[account(address = SYSVAR_INSTRUCTIONS_PUBKEY)]
       pub instructions: UncheckedAccount<'info>,
   }
   ```

   **EVM** — 使用TypeScript和Solidity：

   ```typescript
   import { ethers } from "ethers";
   import { CrossbarClient } from "@switchboard-xyz/common";

   const crossbar = new CrossbarClient("https://crossbar.switchboard.xyz");
   const { encoded } = await crossbar.fetchOracleQuote([feedHash], "mainnet");

   const switchboard = new ethers.Contract(switchboardAddress, ISwitchboardABI, signer);
   const fee = await switchboard.getFee([encoded]);
   const tx = await switchboard.updateFeeds([encoded], { value: fee });
   await tx.wait();

   const [value, timestamp, slotNumber] = await switchboard.latestUpdate(feedId);
   // value is int256 scaled by 1e18 (verify decimals per feed)
   ```

   **Sui** — 使用TypeScript：

   ```typescript
   import { SwitchboardClient, Quote } from "@switchboard-xyz/sui-sdk";

   const sb = new SwitchboardClient(suiClient);
   const state = await sb.fetchState();

   const tx = new Transaction();
   const quotes = await Quote.fetchUpdateQuote(sb, tx, {
     feedHashes: [feedHash],
     numOracles: 3,
   });

   tx.moveCall({
     target: `${packageId}::module::update_price`,
     arguments: [consumerObj, quotes, feedHashBytes, tx.object("0x6")],
   });

   await suiClient.signAndExecuteTransaction({ signer: keypair, transaction: tx });
   ```

   **基于Move的链**：根据实际情况使用链特定的Quote Verifier模式。

### 输出结果

* `FeedReadPlan`，包含：
  - 链和网络信息
  - 标识符
  - 数据的新鲜度/偏差策略
  - 确切的读取方式（链上或链下读取，以及如何完成结算）

***

## 模块2 — 数据源设计助手（Feed Design Assistant, Jobs, Sources, Aggregation）

### 目标

* 将用户的数据需求转化为一个健壮且可验证的`OracleJob[]`设计
* 提供多样化的数据源（CEX、DEX、索引API、事件API、链上查询）
* 嵌入验证和安全机制

### 输入参数

* 数据目标及格式（价格、指数、事件结果、赔率等）
* 允许的数据源/禁止的数据源
* 服务水平协议（SLA）要求（延迟、更新频率、预期波动率）
* 安全要求（波动率/过期时间的严格程度）

### 执行流程

1. **选择数据源（尽可能选择至少3个）**
   - 混合来自不同来源的数据（避免使用3个相同的上游数据源）。
   - 优先选择具有稳定运行时间和一致数据结构的来源。
2. **设计任务流程**（常见模式）：

   ```typescript
   {
     tasks: [
       { httpTask: { url: "https://api.example.com/price", method: "GET" } },
       { jsonParseTask: { path: "$.data.price" } },
       { multiplyTask: { big: "1e18" } }, // normalize to 18 decimals
     ]
   }
   ```

   对于多数据源聚合，使用`medianTask`或`meanTask`：

   ```typescript
   {
     tasks: [{
       medianTask: {
         jobs: [
           { tasks: [{ httpTask: { url: "https://exchange1.com/api/btc" } }, { jsonParseTask: { path: "$.price" } }] },
           { tasks: [{ httpTask: { url: "https://exchange2.com/api/btc" } }, { jsonParseTask: { path: "$.last" } }] },
           { tasks: [{ httpTask: { url: "https://exchange3.com/api/btc" } }, { jsonParseTask: { path: "$.data.price" } }] },
         ],
         minSuccessfulRequired: 2,
       }
     }]
   }
   ```

3. **预测市场数据源（赔率/结果）**
   - 将市场元数据和赔率视为高风险输入：
     - 确保在作业结构中明确指定符号/市场ID
     - 避免使用变量覆盖来改变数据选择逻辑
   - 对于Kalshi市场，使用`kalshiApiTask`（详见任务类型参考）。
   - 仅对认证令牌使用变量覆盖。

4. **变量覆盖**

   - 仅用于认证密钥。
   - 绝不要用于URL、JSON路径、计算公式或数据选择逻辑相关的参数。
   - 语法：在作业定义中使用`${VAR_NAME}`，并在运行时通过`variableOverrides`传递。

   ```typescript
   const sigVerifyIx = await queue.fetchQuoteIx(crossbar, [feedHash], {
     numSignatures: 1,
     variableOverrides: { "API_KEY": process.env.API_KEY },
   });
   ```

5. **在部署前本地测试任务**（详见模块3）

   ```typescript
   import { OracleJob } from "@switchboard-xyz/common";

   const job = OracleJob.fromObject({
     tasks: [
       { httpTask: { url: "https://api.polygon.io/v2/last/trade/AAPL?apiKey=${POLYGON_API_KEY}" } },
       { jsonParseTask: { path: "$.results.p" } },
     ]
   });
   ```

### 输出结果

* `FeedBlueprint`，包含：
  - `OracleJob[]`草稿
  - 数据源列表及理由
  - 聚合方式选择及验证默认设置
  - 安全注意事项（攻击面、重放风险）

***

## 模块3 — 模拟与质量保证（Simulation & QA）

### 目标

* 在部署前验证数据源
* 量化波动率、过期风险和故障模式
* 生成“准备就绪报告”及推荐的参数调整建议

### 首先使用Crossbar的工作流程（Crossbar-first Workflow）

   - 对于大量模拟或生产型机器人，建议使用本地/自托管的Crossbar实例。
   - 模拟：
     - 单次运行以验证数据源结构的正确性
     - 重复运行以估计波动率和错误率
   - 标记：
     - 间歇性失败的端点
     - 数据源结构的脆弱性
     - 来源之间的过度分散

#### 通过CrossbarClient进行模拟（Simulate via CrossbarClient）

```typescript
const crossbar = new CrossbarClient("https://crossbar.switchboard.xyz");
const result = await crossbar.simulateFeeds([feedHash]);
```

#### 任务测试（本地测试，无需部署）

使用示例仓库中的任务测试工具：

```bash
cd common/job-testing
bun run runJob.ts
```

编辑`runJob.ts`以定义自定义任务：

```typescript
function getCustomJob(): OracleJob {
  return OracleJob.fromObject({
    tasks: [
      { httpTask: { url: "https://api.example.com/data?key=${API_KEY}", method: "GET" } },
      { jsonParseTask: { path: "$.price" } },
    ]
  });
}

const res = await queue.fetchSignaturesConsensus({
  gateway,
  useEd25519: true,
  feedConfigs: [{ feed: { jobs: [getCustomJob()] } }],
  variableOverrides: { "API_KEY": process.env.API_KEY! },
});
```

### 使用Docker Compose启动Crossbar（推荐）

根据需要配置RPC/IPFS：

* HTTP默认端口：`8080`
* WebSocket默认端口：`8081`

最小配置示例：
- 创建`docker-compose.yml`
- 创建`.env`文件
- 运行`docker-compose up -d`
- 在`http://localhost:8080`查看结果

（有关当前的compose模板和环境变量，请参阅官方Switchboard文档：<https://docs.switchboard.xyz/tooling/crossbar/run-crossbar-with-docker-compose>）

### 输出结果

* `FeedReadinessReport`：
  - 样本结果
  - 每个数据源的错误率
  - 分散度/波动率统计
  - 建议的最小响应次数/最大波动率/最大过期时间
  - 决策：是否发布/迭代/重新设计

***

## 模块4 — 部署/发布（Deploy / Publish）

### 目标

* 在需要时发布数据源定义（存储/固定）
* 推导出规范化的标识符和地址
* 生成更新和读取的集成代码路径
* 如果OperatorPolicy允许，执行部署步骤

### Solana/SVM：使用管理更新进行部署（Deploy with Managed Updates）

部署步骤包括：
1. 选择队列（预言机子网）：`const queue = await sb.Queue.loadDefault(program!)`
2. 使用Crossbar存储/固定数据源定义 → 获取`feedHash`
3. 推导出规范化的报价账户：

   ```typescript
   const feedId = FeedHash.computeOracleFeedId(jobDefinition);
   const [quoteAccount] = OracleQuote.getCanonicalPubkey(queue.pubkey, [feedId.toString("hex")]);
   ```

4. 获取更新指令，并将其包含在与程序相同的交易中（使用与模块1中相同的`fetchQuoteIx` → `asV0Tx`模式）

规范化的账户在首次使用时会自动创建。

注意：
- 验证参数通常在读取/更新时提供，而不是在部署时提供。
- 确保更新指令和程序的读取操作在同一交易中完成。

#### 输出结果

* `SolanaDeployPlan`，包含：
  - 选择的队列
  - data源哈希
  - 规范化报价账户的公钥
  - 指令的精确组合顺序
  - 成本估算及支出限制

### EVM：“部署”实际上是指通过Switchboard合约发布数据源（“Deploying” actually means publishing data sources via Switchboard contract）

部署步骤如下：
1. 获取`bytes32`类型的数据源ID
2. 将数据源ID存储在您的合约/应用程序中
3. 通过CrossbarClient从链下获取签名后的更新数据
4. 通过`updateFeeds`提交更新（费用通过`getFee`支付）
5. 通过`latestUpdate(feedId`或`getFeedValue`读取数据

注意：
- 始终计算并支付所需的费用（使用`getFee`函数）。
- 确保遵循小数点和签名约定（常见格式：`int256`乘以`1e18`）。

#### 输出结果

* `EvmDeployPlan`，包含：
  - 链ID和Switchboard合约地址
  - 编码后的更新获取方法
  - 费用策略和支出限制
  - 阅读验证逻辑（最大过期时间、最大偏差）

### Sui：使用Quote Verifier模式进行部署（Deploy with Quote Verifier pattern）

1. 在链上创建一个`QuoteConsumer`（一次性设置）：

```typescript
const createTx = new Transaction();
createTx.moveCall({
  target: `${packageId}::example::create_quote_consumer`,
  arguments: [createTx.pure.id(state.oracleQueueId), createTx.pure.u64(maxAgeMs), createTx.pure.u64(maxDeviationBps)],
});
await suiClient.signAndExecuteTransaction({ signer: keypair, transaction: createTx });
```

2. 使用相同的`Quote.fetchUpdateQuote` → `moveCall` → `sign`模式获取和验证报价。

### 其他链（Aptos、Iota、Movement）

如果目标是Aptos、Iota或Movement链：
1. 创建/发布数据源定义并记录其ID/哈希
2. 使用链特定的SDK进行预言机结果的获取/验证，作为交易的一部分

***

## 模块5 — 数据源生命周期管理（Module 5 — Feed Lifecycle Management）

### 目标

* 更新现有的数据源定义
* 监控数据源的健康状况和性能
* 处理数据源的退役和迁移

### 执行流程

#### 更新数据源

1. 修改`OracleJob[]`定义
2. 通过Crossbar重新存储/固定数据源定义 → 获取新的`feedHash`
3. 在您的消费者合约/程序中更新`feedHash`引用
4. 在切换之前模拟新的数据源定义（执行步骤3）

#### 监控数据源的健康状况

* 随时间跟踪每个数据源的错误率
* 监控数据源之间的波动率（波动率增加表示数据源性能下降）
* 设置警报：
  - 超过过期时间的阈值
  - 错误率超过基准值
  - 价格突然波动

#### 数据源的退役

* 从活跃的消费者中移除数据源
* 更新文档以指向替代数据源
* 由于没有人在获取数据源，因此数据源将自动停止更新

### 输出结果

* `FeedMaintenancePlan`：当前的健康指标、推荐的修改措施、迁移步骤

***

## 模块6 — 预测市场（Module 5 — Prediction Markets）

### 目标

* 将预测市场数据（赔率、结果）整合为链上数据源
* 支持Kalshi和其他基于事件的数据源
* 确保市场选择的正确验证（防止替代攻击）

### 支持的数据源（Supported Sources）

* **Kalshi**（通过`kalshiApiTask`）——主要支持的预测市场

### 执行流程

1. **定义市场数据源**：

   ```typescript
   {
     tasks: [{
       kalshiApiTask: {
         url: "https://api.elections.kalshi.com/v1/...",
         api_key_id: "${KALSHI_API_KEY_ID}",
         private_key: "${KALSHI_PRIVATE_KEY}",
       }
     }]
   }
   ```

2. **硬编码市场标识符**——切勿使用变量覆盖市场ID或符号
3. **仅对认证信息使用变量覆盖**（`api_key_id`、`private_key`）
4. **在链上使用标准的验证流程进行验证**（模块1中的读取步骤）

### 安全考虑（Security Considerations）

* 市场元数据和赔率是高风险输入
* 符号/市场ID必须在作业结构中明确指定
* 对于任何会改变数据选择的因素，禁止使用变量覆盖

### 输出结果

* `PredictionMarketFeedPlan`：市场来源、作业定义、验证流程

***

## 模块7 — Surge流式服务（Module 7 — Surge Streaming Service）

### 目标

* 发现可用的Surge数据源
* 通过WebSocket订阅获取签名后的低延迟价格更新
* 将签名后的流式更新转换为机器人和/或链上结算可用的格式
* 提供延迟/健康指标和重新连接逻辑

### Surge概述（Surge Overview）

Surge是Switchboard提供的**签名后的低延迟WebSocket流式服务**：
- **预言机延迟为2–5毫秒**（端到端包括网络延迟）
- 签名后的更新可以在链上结算
- **订阅通过Solana在链上管理**，无论目标链是什么
- 订阅费用通过SWTCH代币支付

#### 订阅层级（Subscription Tiers）

| 订阅层级 | 价格       | 最大数据源数量 | 报价间隔         |
| ---------- | ----------- | --------- | --------------- |
| Plug       | 免费        | 2         | 10秒            |
| Pro        | 约$3,000/月   | 100       | 450毫秒           |
| Enterprise | 约$7,500/月   | 300       | 实时（0毫秒）         |

#### Surge程序ID（Solana）

`orac1eFjzWL5R3RbbdMV68K9H6TaCVVcL6LjvQQWAbz`

### 执行流程

#### 0. 创建订阅（If needed）

在使用Surge之前，您必须拥有一个活跃的链上订阅。如果钱包没有订阅，请通过以下方式程序化创建：

**前提条件**：
- 拥有Solana钱包和用于支付交易费用的SOL代币
- 拥有用于支付订阅费用的SWTCH代币（可通过Jupiter、Raydium等平台获取）
- 选择订阅层级：Plug（免费）、Pro（约$3,000/月）或Enterprise（约$7,500/月）

**订阅流程**（详见[完整程序化指南](https://docs.switchboard.xyz/ai-agents-llms/surge-subscription-guide）：

1. **生成PDAs**：

```typescript
const SURGE_PROGRAM_ID = new PublicKey("orac1eFjzWL5R3RbbdMV68K9H6TaCVVcL6LjvQQWAbz");

// State PDA
const [statePda] = PublicKey.findProgramAddressSync(
  [Buffer.from("STATE")],
  SURGE_PROGRAM_ID
);

// Tier PDA (e.g., tier 2 = Pro)
const tierId = 2;
const [tierPda] = PublicKey.findProgramAddressSync(
  [Buffer.from("TIER"), new BN(tierId).toArrayLike(Buffer, "le", 4)],
  SURGE_PROGRAM_ID
);

// Subscription PDA
const [subscriptionPda] = PublicKey.findProgramAddressSync(
  [Buffer.from("SUBSCRIPTION"), keypair.publicKey.toBuffer()],
  SURGE_PROGRAM_ID
);
```

2. **获取SWTCH/USDT预言机报价**（获取实时价格所需）：

```typescript
const queue = await sb.Queue.loadDefault(program!);
const crossbar = new sb.Crossbar({ rpcUrl: connection.rpcEndpoint, programId: queue.pubkey });

// Get SWTCH/USDT feed hash from program state
const stateAccount = await program.account.state.fetch(statePda);
const swtchFeedHash = stateAccount.swtchFeedId.toString("hex");

const quoteIxs = await queue.fetchQuoteIx(crossbar, [swtchFeedHash], {
  numSignatures: 1,
  payer: keypair.publicKey,
});
```

3. **在同一交易中调用`subscription_init`并传入预言机报价：

```typescript
// Build subscription_init instruction (using Surge program IDL)
const subscriptionInitIx = buildSubscriptionInitIx({
  tierId: 2,           // Pro tier
  epochAmount: 40,     // ~40 epochs (~2-3 months)
  contactName: null,
  contactEmail: null,
  accounts: { state: statePda, tier: tierPda, owner: keypair.publicKey, ... },
});

// Submit transaction with quote + subscription_init
const tx = await sb.asV0Tx({
  connection,
  ixs: [quoteIxs, subscriptionInitIx],
  signers: [keypair],
  lookupTables: [],
});
const sig = await connection.sendTransaction(tx);
```

**关键点**：
- 程序会根据实时SWTCH/USDT价格计算订阅费用
- 订阅有效期为指定的Solana时代数（1时代约2-3天）
- Plug层级（层级ID 1）免费，但限制为2个数据源和10秒的报价间隔
- 每个钱包只能拥有一个订阅：`[SUBSCRIPTION, owner_pubkey]`

**有关完整实现细节，请参阅[Surge订阅指南](https://docs.switchboard.xyz/ai-agents-llms/surge-subscription-guide)。**

#### 1. 初始化Surge客户端（Initialize Surge Client）

一旦您拥有活跃的订阅，使用您的Solana连接和密钥对初始化Surge客户端：

```typescript
import * as sb from "@switchboard-xyz/on-demand";

// Initialize with keypair and connection (uses on-chain subscription)
const { keypair, connection, program } = await sb.AnchorUtils.loadEnv();
const surge = new sb.Surge({ connection, keypair });
```

#### 2. 发现可用的数据源（Discover Available Feeds）

```typescript
const availableFeeds = await surge.getSurgeFeeds();
```

#### 3. 订阅数据源（Subscribe to Feeds）

```typescript
await surge.connectAndSubscribe([
  { symbol: "BTC/USD" },
  { symbol: "ETH/USD" },
  { symbol: "SOL/USD" },
]);
```

#### 4. 处理签名后的更新（Handle Signed Updates）

```typescript
surge.on("signedPriceUpdate", (response: sb.SurgeUpdate) => {
  const metrics = response.getLatencyMetrics();
  if (metrics.isHeartbeat) return; // skip heartbeats

  const prices = response.getFormattedPrices();
  metrics.perFeedMetrics.forEach((feed) => {
    console.log(`${feed.symbol}: ${prices[feed.feed_hash]}`);
  });
});

// Alternative event format
surge.on("update", async (response: sb.SurgeUpdate) => {
  const latency = Date.now() - response.data.source_ts_ms;
  console.log(`${response.data.symbol}: ${response.data.price} (${latency}ms)`);
});
```

#### 5. 转换为链上格式（Convert to On-Chain Format）

**Solana**：将流式更新转换为预言机报价指令：

```typescript
const crankIxs = response.toQuoteIx(queue.pubkey, keypair.publicKey);
// or
const [sigVerifyIx, oracleQuote] = response.toOracleQuoteIx();
```

**EVM**：将Surge数据转换为EVM兼容的格式：

```typescript
import { EVMUtils } from "@switchboard-xyz/common";

const evmEncoded = EVMUtils.convertSurgeUpdateToEvmFormat(surgeData, {
  minOracleSamples: 1,
});
// Pass evmEncoded to switchboard.updateFeeds()
```

#### 6. 使用前进行验证（Verify Before Use）

始终执行以下操作：
- 最大过期时间检查
- 偏差合理性检查（特别是对于清算机器人）
- 可选的多数据源一致性检查（例如，三角测量）

#### 7. 重新连接策略（Reconnection Strategy）

* 实现心跳检测
- 在断开连接时自动重连，并采用指数级退避策略
- 跟踪最后一次连接的时间戳/时间槽

### 输出结果

* `SurgeSubscriptionPlan`：
  - 数据源列表 + 符号
  | 订阅层级 |
  | 代码框架 |
  | 重新连接策略 |
  | 验证策略 |
  | 从流式更新到链上结算的转换格式（针对每个链） |

***

## 模块8 — 无签名流式服务（Module 8 — Unsigned Streaming）

### 目标

* 为UI、仪表板和监控提供实时价格数据
* 与链无关（适用于Solana、EVM、Sui）
* 仅用于显示目的，不支持链上验证

### 概述

无签名流式服务是一种**轻量级的、与链无关的WebSocket数据源**，仅用于显示目的，不包含加密签名，因此无法在链上进行验证。

### 执行流程

#### 初始化无签名流式服务（Initialize for Unsigned Streaming）

```typescript
import * as sb from "@switchboard-xyz/on-demand";

// Initialize with keypair and connection (uses on-chain subscription)
const { keypair, connection, program } = await sb.AnchorUtils.loadEnv();
const surge = new sb.Surge({ connection, keypair });

// Unsigned streaming is available via the same Surge client
```

**注意**：无签名更新仅用于监控/显示目的，无法在链上进行验证。

#### 处理无签名更新（Handle Unsigned Updates）

```typescript
surge.on("unsignedPriceUpdate", (update: sb.UnsignedPriceUpdate) => {
  const symbols = update.getSymbols();
  const formattedPrices = update.getFormattedPrices();
  // Display in UI / dashboard
});
```

#### 使用场景（Use Cases）

* 价格行情显示器和仪表板
* 组合投资组合的跟踪界面
* 需要仅显示数据的场景，无需链上验证

### 输出结果

* `UnsignedStreamPlan`：数据源列表、显示集成代码、刷新策略

***

## 模块9 — 随机性（Module 9 — Randomness）

### 目标

* 正确实现请求和结算随机性数据流
* 避免重复请求和双重结算
* 为游戏、抽奖、拍卖和DeFi机制提供安全的集成方案

### Solana/SVM随机性（Solana/SVM Randomness）

#### TypeScript客户端流程（TypeScript Client Flow）

每个步骤都通过`sb.asV0Tx({ connection, ixs, payer, signers, computeUnitPrice: 75_000, computeUnitLimitMultiple: 1.3 })`构建交易并发送。

#### 关键模式（Key Patterns）

* 将随机性绑定到特定的状态转换（Bind randomness to a specific state transition）
* 在显示之前始终等待（预言机需要在TEE中生成结果）
* 实现带有指数级退避的重试逻辑
* 在不同游戏之间重用随机性账户（Reuse randomness accounts across games）
* 拒绝过时的或重复的随机性数据
* 确保程序账户中包含必要的系统变量（Ensure sysvars are present in the program accounts）

#### 输出结果

* `SolanaRandomnessPlan`（账户、指令顺序、重放保护）

#### EVM随机性（EVM Randomness）

#### TypeScript客户端流程（EVM Client Flow）

#### Solidity合约流程（Solidity Contract Flow）

#### 安全性措施（Security Measures）

* **CEI**（Checks-Effects-Interactions）防止重新进入（Check for reentrancy）
* 强制执行`minSettlementDelay`（例如，5秒）
* 使用`try/catch`避免挂起的待处理状态
* 为每个请求生成唯一的`randomnessId`（防止重复请求）
* 确保预言机分配的结果与预期一致（Ensure oracle assignment matches expected oracle）

#### 输出结果

* `EvmRandomnessPlan`（请求ID方案、延迟策略、结算交易计划）

***

## 模块10 — X402微支付（Module 10 — X402 Micropayments）

### 目标

* 通过预言机数据源访问受保护的/高级数据源
* 使用Solana的X402微支付机制按请求进行支付

### 执行流程

#### 1. 设置支付处理程序（Set Up Payment Handler）

```typescript
import { X402FetchManager } from "@switchboard-xyz/x402-utils";
import { createLocalWallet } from "@faremeter/wallet-solana";
import { exact } from "@faremeter/payment-solana";

const wallet = await createLocalWallet("mainnet-beta", keypair);
const usdcMint = new PublicKey("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"); // USDC
const paymentHandler = exact.createPaymentHandler(wallet, usdcMint, connection);
```

#### 2. 定义包含X402支付头部的数据源（Define Feed with X402 Payment Header）

```typescript
const oracleFeed = {
  name: "X402 Paywalled RPC",
  jobs: [{
    tasks: [
      {
        httpTask: {
          url: "https://helius.api.corbits.dev",
          method: "POST",
          body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "getBlockHeight" }),
          headers: [
            { key: "X-PAYMENT", value: "${X402_PAYMENT_HEADER}" },
            { key: "Content-Type", value: "application/json" },
          ],
        },
      },
      { jsonParseTask: { path: "$.result" } },
    ],
  }],
};
```

#### 3. 推导支付头部并获取数据（Derive Payment Header and Fetch Data）

```typescript
const x402Manager = new X402FetchManager(paymentHandler);
const paymentHeader = await x402Manager.derivePaymentHeader(
  "https://helius.api.corbits.dev",
  { method: "GET" }
);

const feedId = FeedHash.computeOracleFeedId(oracleFeed);
const instructions = await queue.fetchManagedUpdateIxs(crossbar, [feedId.toString("hex")], {
  numSignatures: 1,
  variableOverrides: {
    X402_PAYMENT_HEADER: paymentHeader,
  },
});
```

#### 要求（Requirements）

* 拥有Solana钱包和USDC余额
* 需要`@switchboard-xyz/x402-utils`、`@faremeter/wallet-solana`、`@faremeter/payment-solana`
* `numSignatures`必须设置为1，以使用X402支付方式

#### 输出结果

* `X402IntegrationPlan`：支付处理程序设置、数据源定义、变量覆盖映射

***

### 任务类型参考（Task Types Reference）

这是构建Switchboard预言机数据源作业定义的所有任务类型的完整参考。请将这些作为构建`OracleJob[]`数组的构建块使用。

#### 数据获取（Data Fetching）

| 任务                         | 描述                          | 关键参数                                          |
| ------------------------------ | ------------------------------------ | ------------------------------------------------------- |
| `httpTask`                     | 发送HTTP请求并获取响应体           | `url`, `method`, `headers[]`, `body`                    |
| `websocketTask`                | 实时WebSocket数据检索           | `url`, `subscription`, `max_data_age_seconds`, `filter`         |
| `anchorFetchTask`              | 通过Anchor IDL解析Solana账户           | `program_id`, `account_address`                         |
| `solanaAccountDataFetchTask`   | 获取原始Solana账户数据                 | `pubkey`                                                |
| `splTokenParseTask`            | 解析SPL令牌的JSON数据             | `token mint address`                                    |
| `solanaToken2022ExtensionTask` | Token-2022扩展的解析任务             | `mint`                                                  |

#### 解析（Parsing）

| 任务                         | 描述                          | 关键参数                                |
| ----------------------- | ------------------------------------ | --------------------------------------------- |
| `jsonParseTask`         | 从JSON中提取值                   | `path`, `aggregation_method`                  |
| `regexExtractTask`      | 通过正则表达式提取文本               | `pattern`, `group_number`                     |
| `bufferLayoutParseTask` | 解析二进制缓冲区                   | `offset`, `endian`, `type`                    |
| `cronParseTask`         | 将cron表达式转换为时间戳           | `cron_pattern`, `clock_offset`, `clock`       |
| `stringMapTask`         | 将字符串映射到输出                   | `mappings`, `default_value`, `case_sensitive`         |

#### 数学运算（Math Operations）

| 任务                         | 描述                          | 关键参数                                |
| ----------------------- | ------------------------------------ | ------------------------------- |
| `addTask`      | 对标量/作业/聚合器值进行加法           | `big`, `job`, `aggregatorPubkey`                               |
| `subtractTask` | 对标量/作业/聚合器值进行减法           | `big`, `job`, `aggregatorPubkey`                               |
| `multiplyTask` | 对标量/作业进行乘法运算           | `big`, `job`, `aggregatorPubkey`                               |
| `divideTask`   | 对标量/作业进行除法运算           | `big`, `job`, `aggregatorPubkey`                               |
| `powTask`      | 对标量进行幂运算                   | `big`, `job`, `aggregatorPubkey`                               |
| `roundTask`    | 将结果四舍五入                   | `round`, `decimals`                                           |
| `boundTask`    | 将结果限制在指定范围内               | `lower_bound_value`, `upper_bound_value`, `on_exceeds_*_value`         |

#### 聚合（Aggregation）

| 任务                         | 描述                           | 关键参数                                      |
| ---------------------- | ----------------------------------- | ------------------------------------------------------------------- |
| `medianTask` | 计算子任务/作业的中位数           | `tasks[]`, `jobs[]`, `min_successful_required`, `max_range_percent` |
| `meanTask`   | 计算子任务/作业的平均值           | `tasks[]`, `jobs`                                 |
| `maxTask`    | 计算子任务的最大值                   | `tasks[]`, `jobs`                                 |
| `minTask`    | 计算子任务的最小值                   | `tasks[]`, `jobs`                                 |
| `ewmaTask`   | 计算子任务的指数加权平均值           | `ewma parameters`                                 |
| `twapTask`   | 计算子任务的TWAP平均值           | `aggregatorPubkey`, `period`, `min_samples`                        |

#### Surge与预言机集成（Surge & Oracle Integration）

| 任务                         | 描述                           | 关键参数                                      |
| ---------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------- |
| `switchboardSurgeTask` | 从Surge缓存中获取实时现货价格         | `source`（BINANCE, BYBIT, OKX, PYTH, TITAN, WEIGHTED, AUTO），`symbol`       |
| `surgeTwapTask`        | 从Surge烛台数据库获取TWAP价格         | `symbol`, `time_interval`                                   |
| `oracleTask`           | 从Cross-oracle数据源获取价格         | `switchboardAddress`, `pythAddress`, `pythAddress`, `pyth_allowed_confidence_interval` |

#### DEX / DeFi定价（DEX / DeFi Pricing）

| 任务                         | 描述                            | 关键参数                                      |
| ----------------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------- |
| `jupiterSwapTask`             | Jupiter交换机的模拟交易             | `in_token_address`, `out_token_address`, `base_amount`, `slippage`            |
| `uniswapExchangeRateTask`     | Uniswap交换机的价格                 | `in_token_address`, `out_token_address`, `in_token_amount`, `slippage`, `provider`, `version` |
| `pancakeswapExchangeRateTask` | PancakeSwap交换机的价格                 | `in_token_address`, `out_token_address`, `in_token_amount`, `slippage`, `provider`            |
| `sushiswapExchangeRateTask`   | SushiSwap交换机的价格                 | `in_token_address`, `out_token_address`, `in_token_amount`, `slippage`, `provider`            |
| `curveFinanceTask`            | Curve Finance池的价格                 | `pool`, `provider`, `pool_address`, `out_decimals`                           |
| `lpExchangeRateTask`          | LP交换机的价格                 | `pool address`, `out_token_address`, `in_token_address`, `out_token_amount`, `slippage`         |
| `lpTokenPriceTask`            | LP令牌的价格                 | `pool address`, `out_token_address`, `use_fair_price`                         |
| `serumSwapTask`               | Serum DEX的价格                 | `pool`, `type`                                 |
| `meteoraSwapTask`             | Meteora池的价格                 | `pool`, `type`                                 |

#### LST & Staking（LST & Staking）

| 任务                         | 描述                           | 关键参数                                      |
| ------------------------ | ------------------------- | --------------------------------------------------------------- |
| `sanctumLstPriceTask`    | LST的价格相对于SOL             | `lst_mint`, `skip_epoch_check`                                  |
| `lstHistoricalYieldTask` | LST的历史收益率             | `lst_mint`, `operation`, `epochs`                               |
| `marinadeStateTask`      | Marinade的staking状态                 | （无）                                          |
| `splStakePoolTask`       | SPL的Stake Pool账户                 | `pubkey`                                        |
| `suiLstPriceTask`        | Sui的LST交换率                   | `package_id`, `module`, `function`, `rpc_url`                         |
| `vsuiPriceTask`          | vSUI/SUI的交换率                   | `rpc_url`                                       |
| `solayerSusdTask`        | Solayer的sUSD价格                 | （无）                                          |

#### 预测市场与特殊金融（Prediction Markets & Specialized Finance）

| 任务                         | 描述                           | 关键参数                                      |
| ----------------------------- | ----------------------------- | ----------------------------------------------------------- |
| `kalshiApiTask`               | Kalshi预测市场的数据                 | `url`, `api_key_id`, `private_key`                          |
| `lendingRateTask`             | Perpetual市场的价格                 | `protocol`（01, apricot, francium, jet等），`asset_mint`         |
| `perpMarketTask`              | Perpetual市场的价格                 | `perp_market_address`                                       |
| `mangoPerpMarketTask`         | Mango Perp市场的价格                 | `perp_market_address`                                       |
| `mapleFinanceTask`            | Maple Finance的价格                 | `method`                                        |
| `ondoUsdyTask`                | USDY的价格相对于USD                   | `strategy`                                          |
| `turboEthRedemptionRateTask`  | tETH/WETH的赎回率                 | （无）                                          |
| `exponentTask`                | Vault的兑换率                     | （无）                                          |

#### 控制流与实用工具（Control Flow & Utilities）

| 任务                         | 描述                        | 关键参数                                      |
| --------------------- | ---------------------------------- | -------------------------------------------------------------- |
| `conditionalTask`    | 尝试主要方法，失败时使用备用方法           | `attempt[]`, `on_failure[]`                                    |
| `comparisonTask`     | 条件分支                     | `op`, `on_true`, `on_true_value`, `on_false`, `on_false_value`         |
| `cacheTask`          | 将结果存储在变量中以供后续使用           | `cache_items[]`                                                |
| `valueTask`          | 返回静态值                         | `value`, `aggregatorPubkey`, `big`                            |
| `unixTimeTask`       | 获取当前的Unix时间                         | `offset`                                                       |
| `sysclockOffsetTask` | Oracle时间与系统时间的差异                 | （无）                                          |
| `blake2b128Task`     | 将BLAKE2b-128哈希转换为数值           | `value`                                                       |

#### AI与高级功能（AI & Advanced）

| 任务                         | 描述                        | 关键参数                                      |
| --------------------- | -------------------------------- | --------------------------------- |
| `llmTask`             | 在Feed中生成LLM文本                         | `providerConfig`, `userPrompt`, `temperature`, `secretNameApiKey`         |
| `secretsTask`         | 从SecretsServer获取秘密                 | `authority`, `url`                                                |
| `vwapTask`            | 使用Volume加权计算价格                 | （VWAP参数）                                         |
| `historyFunctionTask`         | 获取历史数据                         | （函数参数）                                         |

#### 协议特定任务（Protocol-Specific Tasks）

| 任务                         | 描述                        | -------------------------------------------------- |
| `hyloTask`       | 将hyUSD转换为jitoSOL                     |                                 |
| `aftermathTask`          | Aftermath协议                         |
| `corexTask`      | Corex协议                         |
| `etherfuseTask`      | Etherfuse协议                         |
| `fragmetricTask`      | Fragmetric的液体代币重新质押                     |
| `glyphTask`      | Glyph协议的代币                         |
| `xStepPriceTask`         | xStep的价格计算                         |

有关所有任务的详细参数，请参阅：<https://explorer.switchboardlabs.xyz/task-docs>
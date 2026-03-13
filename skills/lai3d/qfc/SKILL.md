---
name: qfc-openclaw-skill
description: QFC区块链交互——钱包、矿机、链查询、质押、时代（epoch）与最终确认（finality）、人工智能推理
homepage: https://github.com/qfc-network/qfc-openclaw-skill
license: MIT
metadata: {"openclaw":{"requires":{"bins":["node"]}}}
---
# QFC OpenClaw 技能

> 一种用于全面交互 QFC 区块链的 AI 代理技能

## 功能

### 钱包管理
- **创建钱包**：生成一个新的 HD 钱包，包含助记词、地址和私钥
- **导入钱包**：从私钥恢复钱包
- **查询余额**：查询任何地址的 QFC 余额
- **发送 QFC**：将 QFC 代币转移到另一个地址
- **签名消息**：使用钱包的私钥签署任意消息

### 钱包持久化
- **保存钱包**：使用行业标准的 keystore 格式（scrypt KDF，与 MetaMask/Geth 兼容）将钱包加密并保存到磁盘（`~/.openclaw/qfc-wallets/`）
- **加载钱包**：通过地址和密码解密并恢复之前保存的钱包
- **列出保存的钱包**：显示所有保存的钱包（地址、名称、网络）
- **删除钱包**：删除保存的钱包的 keystore 文件和元数据
- **导出 keystore JSON**：获取保存的钱包的加密 keystore JSON（用于导入到 MetaMask 或其他工具）

### 水龙头（仅限测试网）
- **请求测试 QFC**：在测试网上获取测试代币（chain_id=9000）

### 区块链查询
- **获取区块编号**：最新的区块高度
- **获取区块**：按编号或“最新”获取区块详情
- **获取交易**：通过哈希获取交易信息
- **获取收据**：获取带有日志的交易收据

### 网络状态
- **节点信息**：版本、链 ID、节点数量、验证器状态
- **网络状态**：当前网络状况（正常/拥堵）
- **链 ID / 区块编号 / 气体价格**：基本网络参数

### 质押与验证器
- **列出验证器**：列出所有具有质押量、评分和计算模式的验证器
- **获取质押量**：获取某个地址的质押 QFC 量
- **贡献评分**：验证器的评分（0-10000）
- **评分详情**：详细的 7 维评分指标

### 历元与最终性
- **当前历元**：历元编号、开始时间、持续时间
- **最终区块**：最新的最终区块编号

### 智能合约（v2.1）
- **调用合约**：读取合约状态（无需气体）——传递地址、ABI、方法和参数
- **发送交易**：向合约写入数据（需要钱包签名，会产生气体费用）
- **部署合约**：从 ABI 和字节码部署新合约
- **检查合约**：验证某个地址是否部署了合约代码
- **获取代码**：检索某个地址的原始字节码
- **验证合约**：将源代码提交给 QFC 探索器进行验证（编译器版本、EVM 版本、优化器设置）

### ERC-20 代币（v2.1）
- **部署代币**：在 QFC 上创建新的 ERC-20 代币——指定名称、符号和初始供应量。所有代币都归部署者所有。无需编译器（预编译的字节码）。设置 `mintable: true` 以支持铸造/销毁/所有权功能。部署后会在 QFC 探索器上自动验证源代码。
- **铸造代币**：向任何地址铸造新代币（仅限可铸造的代币，调用者必须是所有者）
- **销毁代币**：从你的余额中销毁代币（减少总供应量，仅限可铸造的代币）
- **代币信息**：获取任何 ERC-20 代币的名称、符号、小数位数和总供应量
- **检查代币余额**：检查任何地址的代币余额
- **转移代币**：将 ERC-20 代币转移到另一个地址（自动处理小数位数）
- **批准 spender**：批准某个合约/地址花费代币（支持“max”以无限使用）
- **检查限额**：查询 spender 被允许使用的金额
- **代币投资组合**（v2.3）：查看钱包中的所有代币持有量——包括原生 QFC 余额和每个非零余额的 ERC-20 代币
- **转移历史**（v2.3）：从探索器查看代币转移历史——按代币和/或地址过滤
- **批量转移代币**（v2.4）：一次性向多个地址转移代币
- **批量发送 QFC**（v2.4）：一次性向多个地址发送原生 QFC
- **部署 Airdrop 合约**（v2.5）：部署可重用的 Airdrop 合约——一次性转移任何 ERC-20 代币（节省气体费用）
- **智能 Airdrop**（v2.5）：通过 Airdrop 合约进行 Airdrop——自动批准，支持可变或固定数量

### NFT / ERC-721（v2.4）
- **部署 NFT 收藏**：创建一个新的 ERC-721 NFT 合约，指定名称和符号
- **铸造 NFT**：向任何地址铸造新的 NFT 并附加元数据 URI（仅限所有者）
- **查看 NFT**：查询任何 NFT 的 URI、所有者和余额
- **转移 NFT**：将 NFT 转移到另一个地址

### 代币交换 / DEX（v2.5）
- **部署池**：为任何 ERC-20 代币对创建常数产品 AMM 池（x*y=k）。交换费率为 0.3%。LP 代币跟踪流动性份额。在探索器上自动验证来源代码。
- **池信息**：查看池的储备金、代币详情、当前价格和总 LP 供应量
- **添加流动性**：向池中存入两种代币以赚取 LP 代币（自动批准）
- **移除流动性**：销毁 LP 代币以提取相应的两种代币份额
- **交换代币**：以一定的滑点保护交换一种代币为另一种代币
- **获取报价**：在交换前预览预期输出金额、价格影响和费用
- **LP 余额**：检查任何地址的 LP 代币余额
- **部署 WQFC**（v3.0）：部署封装的 QFC（ERC-20 的包装器）
- **封装/解封 QFC**（v3.0）：在 DEX 池中转换原生 QFC 和 WQFC
- **交换 QFC 为代币**（v3.0）：一次调用中自动封装原生 QFC 并进行交换
- **交换代币为 QFC**（v3.0）：将代币交换为 WQFC 并自动解封为原生 QFC

### 代币 Launchpad（v3.0）
- **启动代币**：一键启动代币——部署代币 + 部署 WQFC 池 + 添加初始流动性。返回代币地址、池地址和 LP 详情。

### NFT 市场（v3.0）
- **部署市场**：部署一个链上的 NFT 市场合约，可配置平台费用（默认 2%，最高 10%）。费用从售价中扣除并发送给费用接收者。
- **列出 NFT**：以 QFC 价格列出待售的 NFT（自动批准市场）
- **购买 NFT**：通过发送 QFC 购买列出的 NFT（平台费用自动扣除，超额部分自动退款）
- **取消 listing**：取消活跃的 listing（仅限卖家）
- **查看列表**：获取所有活跃的 listing 或按 NFT 收藏过滤
- **获取 listing**：查看特定 listing 的详情
- **获取费用信息**：查询当前平台费用（基点）和费用接收者
- **设置费用**：更新平台费用和/或接收者（仅限市场所有者）

### 多次调用（v3.0）
- **部署 Multicall3**：部署一个批量调用合约，用于聚合视图调用
- **批量调用**：在单个 RPC 请求中执行多个合约读取
- **批量查询余额**：一次性查询多个代币的余额
- **批量查询池储备**：一次性查询多个 AMM 池的储备金

### 事件订阅（v3.0）
- **监控转移**：监控某个代币的新 ERC-20 转移事件
- **监控交换**：监控 AMM 池的新交换事件
- **监控 NFT 销售**：监控市场上的新销售事件
- **监控区块**：监控带有交易数量的新区块

### Discord 机器人集成（v2.5）
- **命令处理器**：与框架无关的 Discord 机器人命令处理器——无需依赖 discord.js
- **支持的命令**：`!help`、`!faucet`、`!balance`、`!portfolio`、`!tx`、`!block`、`!price`、`!info`
- **解析 + 执行**：将原始消息解析为命令，执行它们，并返回 Discord 格式的响应
- **自定义前缀**：可配置的命令前缀（默认为 `!`）
- **示例脚本**：参见 `scripts/discord-bot-example.mjs` 了解 discord.js 集成模式

### 代理注册表（v3.2）
- **注册代理**：在链上注册一个 AI 代理，设置权限、每日支出限制、每次交易的最大限额和初始 QFC 存款
- **为代理充值**：为代理的链上存款补充额外的 QFC
- **撤销代理**：从注册表中停用已注册的代理
- **获取代理**：通过 ID 查询代理信息（所有者、地址、权限、存款、每日支出、活动状态）
- **列出代理**：列出某个地址拥有的所有代理 ID
- **发放会话密钥**：为代理授权一个有限期的会话密钥
- **轮换会话密钥**：原子地撤销旧会话密钥并发放新的会话密钥
- **撤销会话密钥**：立即停用会话密钥
- **获取会话密钥**：查询会话密钥详情（过期时间、活动状态）
- **验证会话密钥**：检查会话密钥地址是否当前有效

### 安全执行模式（v3.3）
- **预飞行检查**：在提交任何交易之前查询链上代理的状态
  - 验证代理是否存在且处于活动状态
  - 检查是否获得了所需的权限
  - 验证金额是否在每次交易的限额内（maxPerTx）
  - 验证金额是否在剩余的每日预算内（dailyLimit − spentToday）
  - 检查是否有足够的存款余额
  - 可选地验证会话密钥是否有效且未过期
- **人类可读的拒绝原因**：为每个失败的检查返回清晰的解释
- **警告**：在接近限额的情况下发出警报（>80% 的每日预算、>90% 的存款使用）
- **Dry-Run 模式**：在不提交交易的情况下运行所有检查（`dryRun: true`）
- **安全为代理充值**：`safeFundAgent()`——一次性完成预飞行检查和充值
- **通用安全执行**：`safeExecute()`——完成预飞行检查 + 自定义回调，如果政策被拒绝则阻止执行

### 代理钱包客户端（v3.4）
- **AgentWalletClient**：高级客户端，封装 QFCAgent 和 QFCInference，用于自主代理操作
- **会话密钥推理**：使用会话密钥而不是所有者的长期有效私钥提交推理任务——链上注册表验证会话密钥的权限和支出限制
- **预飞行保护提交**：在每次推理提交之前自动运行预飞行策略检查（权限、每日预算、存款余额、会话密钥有效性）
- **完整的代理生命周期**：注册、充值、撤销、状态、列表——所有操作都通过一个客户端完成
- **会话密钥管理**：发放、轮换、撤销、验证会话密钥
- **费用估算**：在提交之前估算推理成本
- **演示场景**：自主交易者、内容生成器、AI Oracle——参见 `scripts/demo-*.mjs`

### AI 推理（v2.1）
- **列出模型**：从链上注册表中列出已批准的 AI 模型（名称、版本、GPU 级别）
- **推理统计**：全网络范围的统计信息（完成的任务、活跃的矿工、平均时间、FLOPS、通过率）
- **提交任务**：提交一个公共推理任务，提供模型 ID、输入数据和最大费用（需要钱包签名）
- **估算费用**：根据模型和输入大小估算推理任务的成本
- **查询任务状态**：检查任务是待处理、已分配、已完成、失败还是已过期
- **等待结果**：轮询直到任务达到最终状态（可配置的超时）
- **解码结果**：解析已完成任务的 JSON 包裹和 base64 结果负载

## 安全规则

1. **切勿在对话输出中暴露私钥或助记词**。安全存储它们，并仅通过钱包地址引用。
2. **确认交易金额 >100 QFC**——在发送大额交易之前始终请求用户的明确确认。
3. **验证接收者地址**——在发送之前验证地址格式（0x + 40 个十六进制字符）。
4. **默认使用测试网**——除非用户明确请求主网，否则所有操作都使用测试网。
5. **限制交易次数**——默认每天最多 1000 QFC（可配置）。

## 设置

在使用前运行 `{baseDir}/scripts/setup.sh`。这将安装依赖项并将 TypeScript 模块编译到 `{baseDir}/dist/`。

## 配置

### 网络设置
```
Testnet RPC: https://rpc.testnet.qfc.network (chain ID: 9000)
Mainnet RPC: https://rpc.qfc.network (chain ID: 9001)
```

### 环境变量
- `QFC_NETWORK` — “testnet”（默认）或 “mainnet”
- `QFC_RPC_URL` — 替换 RPC 端点

## 模块

| 模块 | 类 | 描述 |
|--------|-------|-------------|
| `contract` | `QFCContract` | 读取/写入/部署智能合约 |
| `token` | `QFCToken` | ERC-20 代币操作和 Airdrop 合约 |
| `nft` | `QFCNFT` | ERC-721 NFT 操作 |
| `swap` | `QFCSwap` | AMM 代币交换 / DEX 和 WQFC 包装器 |
| `marketplace` | `QFCMarketplace` | NFT 市场（列出/购买/出售） |
| `multicall` | `QFCMulticall` | 通过单个 RPC 批量调用合约 |
| `events` | `QFCEvents` | 通过轮询订阅事件 |
| `agent` | `QFCAgent` | AI 代理注册表——注册、充值、撤销、会话密钥 |
| `agent-wallet` | `AgentWalletClient` | 高级代理钱包——会话密钥推理、生命周期、安全执行 |
| `inference` | `QFCInference` | AI 推理任务提交和结果 |
| `provider` | — | 共享提供者创建和 RPC 助手 |

所有模块都编译到 `{baseDir}/dist/`。
| `wallet` | `QFCWallet` | 钱包创建/导入/余额/发送/签名/保存/加载 |
| `keystore` | `QFCKeystore` | 加密钱包持久化（scrypt keystore） |
| `security` | `SecurityPolicy` | 交易前的安全检查 |
| `faucet` | `QFCFaucet` | 测试网代币请求 |
| `chain` | `QFCChain` | 区块、交易、收据查询 |
| `network` | `QFCNetwork` | 节点信息和网络状态 |
| `staking` | `QFCStaking` | 验证器和质押信息 |
| `epoch` | `QFCEpoch` | 历元和最终性信息 |
| `discord` | `QFCDiscordBot` | Discord 机器人命令处理器（无需依赖 discord.js） |

## 使用示例

### 创建钱包，保存它，并获取测试代币
```
Create a new QFC wallet on testnet, save it with password "mypass", then request 10 QFC from the faucet
```

### 加载保存的钱包
```
List my saved QFC wallets and load the first one with password "mypass"
```

### 检查网络状态
```
What's the current QFC testnet status? Show me node info and latest block.
```

### 查询验证器
```
List all QFC validators and their contribution scores
```

### 检查交易
```
Look up transaction 0xabc... on QFC testnet — show me the receipt
```

### ERC-20 代币
```
Create a new token called "My Token" with symbol MTK and 1 million supply on QFC testnet
```

```
Deploy an ERC-20 token named "QFC Rewards" (symbol: QREW) with 10 million supply
```

```
Create a mintable token called "Game Gold" with symbol GOLD and 0 initial supply
```

```
Mint 5000 GOLD tokens to address 0x1234...
```

```
Burn 100 of my GOLD tokens
```

```
What is the token at 0xabcd...? Show me name, symbol, and total supply.
```

```
Check my token balance for 0xabcd... token
```

```
Transfer 50 tokens (0xabcd...) to 0x5678...
```

### 代币投资组合和历史记录
```
Show me all token balances for address 0xfe913E97238B28abac7a55173f5878fD29147210
```

```
What tokens does my wallet hold on QFC testnet?
```

```
Show transfer history for token 0x603f0c43966f68dfb0737314cde8c4a46a0cc1f9
```

```
Show my recent transfers for the XHT token
```

### 批量操作
```
Airdrop 100 XHT tokens to these addresses: 0x1111..., 0x2222..., 0x3333...
```

```
Send 10 QFC to each of these addresses: 0xaaaa..., 0xbbbb...
```

### 智能 Airdrop（单次交易）
```
Deploy an airdrop contract on QFC testnet
```

```
Airdrop 100 XHT to 0x1111..., 200 XHT to 0x2222..., and 50 XHT to 0x3333... using airdrop contract 0xabcd...
```

```
Airdrop 500 GOLD tokens equally to these 10 addresses using the airdrop contract
```

### NFTs
```
Deploy an NFT collection called "QFC Punks" with symbol QPUNK
```

```
Mint an NFT to 0x1234... with metadata URI https://api.example.com/metadata/1
```

```
Who owns token #0 in NFT contract 0xabcd...?
```

```
Get the metadata URI for token #3 in the NFT collection at 0xabcd...
```

```
Transfer NFT #2 from my wallet to 0x5678... on contract 0xabcd...
```

### 代币交换 / DEX
```
Create a swap pool for tokens 0xAAA... and 0xBBB... on QFC testnet
```

```
Add liquidity: 1000 of token A and 500 of token B to pool 0xPOOL...
```

```
Swap 100 of token 0xAAA... for token B on pool 0xPOOL...
```

```
Get a quote: how much token B would I get for 50 of token A on pool 0xPOOL...?
```

```
Show pool info for 0xPOOL... — reserves, price, and LP supply
```

```
Remove all my liquidity from pool 0xPOOL...
```

### WQFC（封装的 QFC）
```
Deploy WQFC contract on QFC testnet
```

```
Wrap 100 QFC into WQFC using contract 0xWQFC...
```

```
Swap 50 native QFC for token 0xAAA... via WQFC pool 0xPOOL...
```

### 代币 Launchpad
```
Launch a new token called "Moon Coin" (MOON) with 1M supply, add 100k tokens and 500 QFC as initial liquidity
```

### NFT 市场
```
Deploy an NFT marketplace on QFC testnet with 2% platform fee
```

```
Deploy a marketplace with 5% fee sent to 0xFEE...
```

```
List NFT #3 from collection 0xNFT... for 10 QFC on marketplace 0xMKT...
```

```
Buy listing #0 on marketplace 0xMKT...
```

```
Show all active NFT listings on marketplace 0xMKT...
```

```
Check the platform fee on marketplace 0xMKT...
```

### 多次调用
```
Deploy a Multicall3 contract on QFC testnet
```

```
Batch check balances of 5 tokens for my wallet using multicall 0xMC...
```

### 智能合约
```
Is 0x1234...abcd a contract address on QFC testnet?
```

```
Read the name() and symbol() of ERC-20 contract 0xabcd...
```

```
Call the balanceOf method on contract 0xabcd... for address 0x1234...
```

```
Verify the source code for contract 0xabcd... on the QFC explorer
```

### AI 推理
```
What AI models are available on QFC?
```

```
How much does it cost to run a text embedding on QFC?
```

```
Submit an inference task using qfc-embed-small with input "Hello world" and max fee 0.1 QFC
```

```
Check the status of inference task 0xdef456...
```

```
Show me QFC inference network statistics
```

```
Register an AI agent called "my-agent" with Transfer permission, 100 QFC daily limit, 10 QFC max per tx, and 5 QFC deposit
```

```
Fund agent "my-agent" with 50 QFC
```

```
Issue a session key for agent "my-agent" to address 0x1234... valid for 1 hour
```

```
Rotate the session key for agent "my-agent" from 0xOLD... to 0xNEW... with 2 hour validity
```

```
Revoke the session key at 0x1234... for agent "my-agent"
```

```
Is session key 0x1234... still valid?
```

```
Show info for agent "my-agent"
```

```
List all agents owned by 0xfe913E97238B28abac7a55173f5878fD29147210
```

```
Check if agent "my-agent" can spend 50 QFC (dry run, don't submit)
```

```
Safely fund agent "my-agent" with 20 QFC — check policy first, then submit if allowed
```

```
Run preflight check for agent "my-agent" with Transfer permission and 5 QFC amount
```

```
Create an autonomous trader agent: register "trader-1" with InferenceSubmit and Transfer permissions, 100 QFC daily limit, issue a session key, then submit a sentiment analysis inference using only the session key
```

```
Set up a content generator agent with InferenceSubmit-only permission and a 7-day session key
```

```
Run an AI oracle: register agent, estimate inference fee, run preflight check, then submit a query — all using the session key
```

```
Submit an inference task as agent "my-agent" using session key — model qfc-embed-small, input "Hello world"
```

### Discord 机器人
```
Set up a QFC Discord bot using scripts/discord-bot-example.mjs as a template
```

```
Integrate QFCDiscordBot into my existing Discord bot to handle !balance and !faucet commands
```

## 错误处理

| 错误 | 含义 | 操作 |
|-------|---------|--------|
| INSUFFICIENT_FUNDS | QFC 不足 | 检查余额，为钱包充值 |
| INVALID_ADDRESS | 接收者格式错误 | 验证地址格式（0x + 40 个十六进制字符） |
| NETWORK_ERROR | RPC 连接失败 | 检查 RPC URL，重试 |
| NONCE_TOO_LOW | 交易已经发送 | 等待确认，重试 |
| FAUCET_TESTNET_ONLY | 在主网上使用了水龙头 | 切换到测试网 |
| CALL_EXCEPTION | 合同调用失败 | 检查方法名称、参数和 ABI |
| UNPREDICTABLE_GAS | 气体费用估算失败 | 合同可能失败，检查参数 |
| MODEL_NOT_FOUND | 未知的模型 ID | 使用 getModels() 列出模型 |
| TASK_EXPIRED | 推理任务超时 | 以更高的费用重新提交 |
| FEE_TOO_LOW | 最大费用低于最低要求 | 使用 estimateFee() 获取基础价格 |
| AGENT_NOT_FOUND | 未知的代理 ID | 使用 listAgents() 列出代理 |
| SESSION_KEY_EXPIRED | 会话密钥过期 | 发放或轮换新的会话密钥 |
| PREFLIGHT_DENIED | 政策检查失败 | 查看 preflight.reasons[] 以获取详细信息 |
| DAILY_LIMIT_EXCEEDED | 金额超过剩余的每日预算 | 等待每日重置或增加限额 |
| PER_TX_LIMIT_EXCEEDED | 金额超过每次交易的限额 | 分成多个小交易 |
| DEPOSIT_INSUFFICIENT | 代理存款不足 | 使用 fundAgent() 为代理充值 |
| PERMISSION_DENIED | 代理缺乏所需的权限 | 使用 correct permissions 重新注册 |
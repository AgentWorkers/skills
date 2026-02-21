---
name: Vincent - A wallet for agents
description: 使用此技能可以安全地创建一个钱包，该钱包可供代理用于转账、交换以及任何以太坊虚拟机（EVM）链上的交易。此外，该钱包还支持对以太坊和Solana网络进行原始签名（raw signing）操作。
homepage: https://heyvincent.ai
source: https://github.com/HeyVincent-ai/Vincent
metadata:
  clawdbot:
    homepage: https://heyvincent.ai
    requires:
      config:
        - ${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet
        - ./agentwallet
---
# Vincent – 一个专为智能代理设计的钱包

使用此技能可以安全地为智能代理创建一个钱包，用于转账、交易以及进行任何以太坊虚拟机（EVM）链上的操作，同时确保私钥永远不会暴露给代理本身。创建钱包后，可以设置 spending policies（支出策略），代理便能够在您定义的范围内转移代币、进行交易以及与智能合约交互。

**代理永远不会看到私钥**。所有交易都在服务器端通过 ZeroDev 智能账户执行。代理会收到一个受限的 API 密钥，该密钥仅能执行钱包所有者允许的操作。私钥始终保存在 Vincent 服务器上。

所有命令均使用 `@vincentai/cli` 包。API 密钥会自动存储和解析——您无需处理原始密钥或文件路径。

## 安全模型

此技能旨在实现**在服务器端控制下的智能代理自主操作**。理解以下安全模型非常重要：

**无需环境变量**，因为该技能采用“代理优先”的注册流程：代理在运行时通过调用 Vincent API 自动创建钱包，并获得一个受限的 API 密钥。无需预先配置任何凭证。CLI 会在创建钱包时自动保存返回的 API 密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet/` 或 `./agentwallet/`）在技能的元数据中已明确指定。

**代理的 API 密钥并非私钥**，而是一个受限的“承载者令牌”，仅能在钱包所有者设定的策略范围内执行交易。Vincent 服务器会在服务器端严格执行所有策略——无论代理发送什么请求，都无法绕过这些策略。如果交易违反策略，服务器会拒绝该请求；如果交易需要批准，服务器会暂停交易并通过 Telegram 通知钱包所有者进行人工审批。

**有意启用模型调用**。该技能的目的是让 AI 代理具备自主管理钱包的能力。代理应在人类操作员设定的范围内自行执行钱包操作（如转账、交易、调用合约）。人类操作员通过策略（如支出限制、地址允许列表、代币允许列表、函数允许列表、审批阈值）来控制代理的行为，而不是通过限制单个调用来实现控制。存储的密钥具有范围限制且受策略约束——即使其他进程读取了该密钥，也只能执行钱包所有者允许的操作，且所有者可以随时撤销该密钥。

**所有 API 调用均通过 HTTPS/TLS 发送到 `heyvincent.ai`**，不会连接其他端点、服务或外部主机。代理不会读取、收集或传输超出钱包操作所需的数据。

**Vincent 是开源项目，并经过审计**。负责执行策略、管理私钥和执行交易的服务器端代码可在 [github.com/HeyVincent-ai/Vincent](https://github.com/HeyVincent-ai/Vincent) 公开查看。Vincent 后端会定期接受安全审计，涵盖密钥管理、策略执行、交易签名和 API 认证等方面。您可以验证策略执行机制、私钥存储方式以及撤销流程——没有任何隐藏信息。如果您希望自行托管 Vincent 而非依赖托管服务，该仓库提供了部署指南。

**密钥生命周期：**
- **创建**：代理运行 `secret create` 命令，CLI 会自动保存 API 密钥，并返回 `keyId` 和 `claimUrl`。
- **声明所有权**：人类操作员使用 `claimUrl` 声明所有权并配置策略。
- **撤销**：钱包所有者可以随时通过 `https://heyvincent.ai` 撤销代理的 API 密钥。被撤销的密钥会被服务器立即拒绝。
- **重新链接**：如果代理丢失了 API 密钥，钱包所有者可以生成一个一次性重新链接令牌，代理通过 `secret relink` 命令使用该令牌获取新密钥。
- **轮换**：钱包所有者可以随时撤销当前密钥并生成新的重新链接令牌以更新凭证。

## 应使用哪种 Secret 类型

| 类型         | 使用场景                                      | 网络                 | Gas              |
| ------------ | ----------------------------------------- | ----------------------- | ---------------- |
| `EVM_WALLET` | 转账、交易、去中心化金融（DeFi）操作、调用智能合约    | 任何 EVM 链           | 免费（由 Vincent 支付费用） |
| `RAW_SIGNER` | 为特殊协议提供原始签名功能                 | 任何以太坊（Ethereum）或 Solana       | 需用户自行支付费用          |

**建议选择 `EVM_WALLET`（默认设置）**，适用于以下场景：
- 发送 ETH 或代币
- 在去中心化交易所（DEX）中进行代币交易
- 与智能合约交互
- 执行任何标准的 EVM 交易

**仅在以下情况下选择 `RAW_SIGNER`**：
- 需要为不支持智能账户的协议提供原始 ECDSA/Ed25519 签名
- 需要为自己广播的交易哈希签名
- 需要 Solana 签名

## 快速入门

### 1. 检查是否存在现有密钥

在创建新钱包之前，请先检查是否已有密钥：

```bash
npx @vincentai/cli@latest secret list --type EVM_WALLET
```

如果找到密钥，请将其 `id` 作为后续命令的 `--key-id` 参数使用。如果没有密钥，则创建新钱包。

### 2. 创建钱包

```bash
npx @vincentai/cli@latest secret create --type EVM_WALLET --memo "My agent wallet" --chain-id 84532
```

创建完成后，会返回 `keyId`（用于后续命令）、`claimUrl`（与用户共享）以及钱包地址。

创建完成后，告知用户：
> “这是您的钱包声明 URL：`<claimUrl>`。请使用此 URL 声明所有权、设置支出策略，并在 https://heyvincent.ai 监控您的代理钱包活动。”

### 3. 获取钱包地址

```bash
npx @vincentai/cli@latest wallet address --key-id <KEY_ID>
```

### 4. 查看余额

```bash
# All balances across all supported chains
npx @vincentai/cli@latest wallet balances --key-id <KEY_ID>

# Filter to specific chains
npx @vincentai/cli@latest wallet balances --key-id <KEY_ID> --chain-ids 1,137,42161
```

会显示所有 ERC-20 代币的余额，包括代币符号、小数位数、图标以及对应的美元价值。

### 5. 转账 ETH 或代币

```bash
# Transfer native ETH
npx @vincentai/cli@latest wallet transfer --key-id <KEY_ID> --to 0xRecipient --amount 0.01

# Transfer ERC-20 token
npx @vincentai/cli@latest wallet transfer --key-id <KEY_ID> --to 0xRecipient --amount 100 --token 0xTokenAddress
```

如果交易违反策略，服务器会返回错误信息，说明具体违反了哪条策略。如果交易需要人工审批（根据审批阈值设置），服务器会返回 `status: "pending_approval"`，此时钱包所有者会收到 Telegram 通知以决定是否批准。

### 6. 交易代币

使用 0x 提供的流动性在去中心化交易所（DEX）中交换代币：

```bash
# Preview a swap (no execution, just pricing)
npx @vincentai/cli@latest wallet swap preview --key-id <KEY_ID> \
  --sell-token 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE \
  --buy-token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --sell-amount 0.1 --chain-id 1

# Execute a swap
npx @vincentai/cli@latest wallet swap execute --key-id <KEY_ID> \
  --sell-token 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE \
  --buy-token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --sell-amount 0.1 --chain-id 1 --slippage 100
```

- 使用 `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` 作为原生 ETH 的地址。
- `--sell-amount`：用户可读的金额（例如 `0.1` 表示 0.1 ETH）。
- `--chain-id`：1 = 以太坊，137 = Polygon，42161 = Arbitrum，10 = Optimism，8453 = Base 等。
- `--slippage`：滑点容忍度（以基点表示，100 = 1%）。默认值为 100。此参数仅用于预览，实际执行时不会调整滑点。

预览会显示预期购买金额、路由信息和费用，但不会执行交易。实际执行时系统会自动处理 ERC20 交易并完成审批。

### 7. 发送任意交易

通过发送自定义调用数据（calldata）与智能合约交互：

```bash
npx @vincentai/cli@latest wallet send-tx --key-id <KEY_ID> --to 0xContract --data 0xCalldata --value 0
```

### 8. 在不同的 Vincent 账户之间转账

在您拥有的 Vincent 账户之间转账（例如，从一个 EVM 钱包转移到另一个钱包或 Polymarket 钱包）。Vincent 会验证您是否同时拥有这两个账户，并自动处理代币转换或跨链桥接操作：

```bash
# Preview (get quote without executing)
npx @vincentai/cli@latest wallet transfer-between preview --key-id <KEY_ID> \
  --to-secret-id <DEST_SECRET_ID> --from-chain 8453 --to-chain 8453 \
  --token-in ETH --amount 0.1 --token-out ETH

# Execute
npx @vincentai/cli@latest wallet transfer-between execute --key-id <KEY_ID> \
  --to-secret-id <DEST_SECRET_ID> --from-chain 8453 --to-chain 8453 \
  --token-in ETH --amount 0.1 --token-out ETH --slippage 100

# Check cross-chain transfer status
npx @vincentai/cli@latest wallet transfer-between status --key-id <KEY_ID> --relay-id <RELAY_REQUEST_ID>
```

**行为规则：**
- **相同代币/相同链**：作为直接转账执行（费用由 Vincent 支付）。
- **不同代币/不同链**：使用中继服务进行原子交换和跨链桥接。
- 目标账户可以是 `EVM_WALLET` 或 `POLYMARKET_WALLET`。
- 服务器会验证您是否同时拥有源账户和目标账户；如果目标账户不属于您的账户，转账会被拒绝。
- 转账受相同的服务器端策略约束（如支出限制、审批阈值等）。

## 策略（服务器端执行）

钱包所有者可以通过 `https://heyvincent.ai` 上的声明 URL 设置策略来控制代理的行为。所有策略均由 Vincent API 在服务器端执行——代理无法绕过或修改这些策略。如果交易违反策略，API 会拒绝该交易；如果交易触发审批阈值，API 会暂停交易并通过 Telegram 通知钱包所有者进行人工审批。策略执行逻辑的源代码可在 [github.com/HeyVincent-ai/Vincent](https://github.com/HeyVincent-ai/Vincent) 查看。

| 策略                      | 功能                                      |
| --------------------------- | ------------------------------------------------------------------- |
| **地址允许列表**       | 仅允许向特定地址转账/调用                      |
| **代币允许列表**         | 仅允许转移特定 ERC-20 代币                        |
| **函数允许列表**      | 仅允许调用特定的合约函数（通过 4 字节的选择器）                |
| **单次交易支出限制**     | 每次交易的最大美元金额                          |
| **每日支出限制**     | 每 24 小时的最大美元金额                          |
| **每周支出限制**     | 每 7 天的最大美元金额                          |
| **需要审批**       | 所有交易均需通过 Telegram 进行人工审批                |
| **审批阈值**       | 超过指定金额的交易需人工审批                      |

在声明所有权之前，代理可以无策略限制地操作。这是有意设计的：通过“代理优先”的注册流程，代理可以立即开始积累和管理资金。一旦人类操作员通过声明 URL 声明所有权，他们可以添加任何策略来限制代理的行为。钱包所有者也可以随时完全撤销代理的 API 密钥。

## 重新链接（恢复 API 访问权限）

如果代理丢失了 API 密钥，钱包所有者可以通过前端生成一个**重新链接令牌**。代理可以使用该令牌获取新的 API 密钥。

**操作步骤：**
1. 用户在 `https://heyvincent.ai` 的钱包详情页面生成重新链接令牌。
2. 用户将令牌提供给代理（例如通过聊天发送）。
3. 代理运行 `relink` 命令：

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI 会使用该令牌获取新的 API 密钥，并自动保存它，同时返回新的 `keyId`。后续命令均使用这个 `keyId`。

**重要提示：**
- **无需支付 gas 费用**。所有交易费用均由 Vincent 支付。
- **切勿尝试访问原始密钥值**。私钥始终保存在服务器端，这是安全设计的必要措施。
- 创建钱包后务必将声明 URL 分享给用户。
- 如果交易被拒绝，可能是由于服务器端策略导致的。请让用户查看他们在 `https://heyvincent.ai` 上设置的策略。
- 如果交易需要审批，系统会返回 `status: "pending_approval"`。钱包所有者会收到 Telegram 通知以决定是否批准。

---

## 原始签名器（高级功能）

适用于需要原始 ECDSA/Ed25519 签名的场景（例如智能账户无法使用的场景）：

### 创建原始签名器

```bash
npx @vincentai/cli@latest secret create --type RAW_SIGNER --memo "My raw signer"
```

响应中包含从同一种子生成的以太坊（secp256k1）和 Solana（ed25519）地址。

### 获取地址

```bash
npx @vincentai/cli@latest raw-signer addresses --key-id <KEY_ID>
```

返回 `ethAddress` 和 `solanaAddress`。

### 签名消息

```bash
npx @vincentai/cli@latest raw-signer sign --key-id <KEY_ID> --message 0x<hex-encoded-bytes> --curve ethereum
```

- `--message`：要签名的十六进制字节数据（必须以 `0x` 开头）。
- `--curve`：`ethereum` 表示 secp256k1 ECDSA，`solana` 表示 ed25519

返回签名的十六进制字符串。对于以太坊，格式为 `r || s || v`（共 65 个字节）；对于 Solana，格式为 64 个字节的 ed25519 签名。
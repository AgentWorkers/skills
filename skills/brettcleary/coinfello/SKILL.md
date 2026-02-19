---
name: coinfello
description: '使用 openclaw CLI 与 CoinFello 进行交互，以创建 MetaMask 智能账户、管理委托关系、通过 ERC-20 代币进行委托操作以及查询交易状态。当用户希望通过自然语言指令发送加密交易、管理智能账户的委托关系或查看 CoinFello 的交易结果时，可以使用该工具。'
compatibility: Requires Node.js 20+ and pnpm.
metadata:
  {
    'clawdbot':
      { 'emoji': '👋', 'homepage': 'https://coinfello.com', 'requires': { 'bins': ['node'] } },
  }
---
# CoinFello CLI 技能

使用 `openclaw` CLI 通过 MetaMask 智能账户与 CoinFello 进行交互。该 CLI 支持智能账户的创建、委托管理、基于提示的 ERC-20 代币交易以及交易状态查询。

## 先决条件

- Node.js 20 或更高版本
- pnpm 包管理器
- 在首次使用前，请先构建 CLI：`pnpm build`

构建完成后，CLI 可执行文件位于 `./dist/index.js`；如果全局安装了该 CLI，则可直接使用 `openclaw`。

## 快速入门

```bash
# 1. Create a smart account on a chain (generates a new private key automatically)
openclaw create_account sepolia

# 2. Send a prompt with token subdelegation
openclaw send_prompt "swap 5 USDC for ETH" \
  --token-address 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --amount 5 \
  --decimals 6

# 3. Check transaction status
openclaw get_transaction_status <txn_id>
```

## 命令

### create_account

创建一个 MetaMask 混合智能账户，并自动生成私钥，将其保存到本地配置文件中。

```bash
openclaw create_account <chain>
```

- `<chain>` — Viem 链名称：`sepolia`、`mainnet`、`polygon`、`arbitrum`、`optimism`、`base` 等
- 自动生成新的私钥
- 将 `private_key`、`smart_account_address` 和 `chain` 保存到 `~/.clawdbot/skills/coinfello/config.json`
- 必须在运行 `send_prompt` 之前执行此命令

### get_account

从本地配置文件中显示当前的智能账户地址。

```bash
openclaw get_account
```

- 打印存储的 `smart_account_address`
- 如果尚未创建账户，则会显示错误并退出

### set_delegation

将已签名的父委托（JSON 格式）保存到本地配置文件中，以便后续进行再委托操作。

```bash
openclaw set_delegation '<delegation-json>'
```

- `<delegation-json>` — 代表 MetaMask 智能账户套件中的 `Delegation` 对象的 JSON 字符串
- 仅在计划使用 `--use-redelegation` 与 `send_prompt` 时需要此命令

### sendprompt

使用本地创建并签名的 ERC-20 代币子委托，向 CoinFello 发送自然语言提示。

```bash
openclaw send_prompt "<prompt>" \
  --token-address <erc20-address> \
  --amount <amount> \
  [--decimals <n>] \
  [--use-redelegation]
```

**必选参数：**
- `--token-address <address>` — 子委托所涉及的 ERC-20 代币合约地址
- `--amount <amount>` — 代币的最大数量（以人类可读的形式表示，例如 `5`、`100.5`）

**可选参数：**
- `--decimals <n>` — 用于解析 `--amount` 的代币小数位数（默认值：`18`）
- `--use-redelegation` — 根据保存的父委托创建再委托（需要先执行 `set_delegation`）

**内部处理流程：**
1. 从 API 获取 CoinFello 的委托地址
2. 根据配置文件中的私钥和链信息重新生成智能账户
3. 创建一个范围为 `erc20TransferAmount` 的子委托，指定代币和最大数量
4. 使用智能账户对子委托进行签名
5. 将提示信息及签名后的子委托发送到 CoinFello 的对话端点
6. 返回一个 `txn_id` 以供跟踪

### get_transaction_status

检查先前提交的交易状态。

```bash
openclaw get_transaction_status <txn_id>
```

- 返回一个包含当前交易状态的 JSON 对象

## 常见工作流程

### 基本操作：发送代币转移提示

```bash
# Create account if not already done
openclaw create_account sepolia

# Send prompt to transfer up to 10 USDC
openclaw send_prompt "send 5 USDC to 0xRecipient..." \
  --token-address 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --amount 10 \
  --decimals 6

# Check the result
openclaw get_transaction_status <txn_id-from-above>
```

### 使用再委托

当您拥有来自其他委托者的父委托时，可以使用此命令创建新的子委托。

```bash
# Store the parent delegation
openclaw set_delegation '{"delegate":"0x...","delegator":"0x...","authority":"0x...","caveats":[],"salt":"0x...","signature":"0x..."}'

# Send with redelegation
openclaw send_prompt "swap tokens" \
  --token-address 0xTokenAddress \
  --amount 100 \
  --use-redelegation
```

## 特殊情况：
- **没有智能账户**：在运行 `send_prompt` 之前，请先执行 `create_account`。CLI 会检查配置文件中是否保存了私钥和账户地址。
- **链名称无效**：CLI 会抛出错误，并列出有效的 Viem 链名称。
- **使用 `--use-redelegation` 时缺少父委托**：CLI 会显示错误并退出。请先执行 `set_delegation`。

## 参考资料

有关完整的配置方案、支持的链、API 详情和故障排除信息，请参阅 [references/REFERENCE.md]。
完整的自动化脚本请参见 [scripts/setup-and-send.sh]。
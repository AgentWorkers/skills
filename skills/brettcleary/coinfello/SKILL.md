---
name: coinfello
description: '使用 `@coinfello/agent-cli` 与 CoinFello 进行交互，可以创建 MetaMask 智能账户、通过 SIWE 登录、管理委托关系、发送基于服务器驱动的 ERC-20 代币委托指令以及查询交易状态。当用户希望通过自然语言指令发送加密交易、管理智能账户的委托关系或查看 CoinFello 的交易结果时，可以使用该工具。'
compatibility: Requires Node.js 20+ (npx is included with Node.js).
metadata:
  clawdbot:
    emoji: '👋'
    homepage: 'https://coinfello.com'
    requires:
      bins: ['node', 'npx']
      env:
        - name: COINFELLO_BASE_URL
          description: 'Base URL for the CoinFello API server'
          required: false
          default: 'https://hyp3r-58q8qto10-hyperplay.vercel.app/'
---
# CoinFello CLI 功能

使用 `npx @coinfello/agent-cli` CLI 通过 MetaMask 智能账户与 CoinFello 进行交互。该 CLI 支持智能账户的创建、SIWE 认证、委托管理、基于提示的交易执行以及交易状态查询。

## 先决条件

- Node.js 20 或更高版本（`npx` 已包含在 Node.js 中）

该 CLI 可通过 `npx @coinfello/agent-cli` 获取。无需手动构建。

## 环境变量

| 变量                | 是否必需 | 默认值                                      | 说明                                      |
|------------------|--------|----------------------------------|-------------------------------------------|
| `COINFELLO_BASE_URL`    | 否       | `https://hyp3r-58q8qto10-hyperplay.vercel.app/`            | CoinFello API 的基础 URL                        |
|                    |        |                                            |

## 安全提示

此功能执行以下敏感操作：

- **私钥生成与存储**：运行 `create_account` 会生成新的私钥，并将其以 **明文** 形式存储在 `~/.clawdbot/skills/coinfello/config.json` 文件中。请妥善保护此文件。
- **会话令牌存储**：运行 `sign_in` 会将 SIWE 会话令牌存储在同一配置文件中。
- **委托签名**：运行 `send_prompt` 可能会根据服务器请求的权限范围自动生成并签署区块链委托，然后将其提交给 CoinFello API。

用户在运行委托流程之前，应确保信任通过 `COINFELLO_BASE_URL` 配置的 CoinFello API 端点。

## 快速入门

```bash
# 1. Create a smart account on a chain (generates a new private key automatically)
npx @coinfello/agent-cli create_account sepolia

# 2. Sign in to CoinFello with your smart account (SIWE)
npx @coinfello/agent-cli sign_in

# 3. Send a natural language prompt — the server will request a delegation if needed
npx @coinfello/agent-cli send_prompt "send 5 USDC to 0xRecipient..."

# 4. Check transaction status
npx @coinfello/agent-cli get_transaction_status <txn_id>
```

## 命令

### create_account

创建一个带有自动生成私钥的 MetaMask 混合智能账户，并将其保存到本地配置文件中。

```bash
npx @coinfello/agent-cli create_account <chain>
```

- `<chain>` — Viem 链名：`sepolia`、`mainnet`、`polygon`、`arbitrum`、`optimism`、`base` 等
- 自动生成新的私钥
- 将 `private_key`、`smart_account_address` 和 `chain` 保存到 `~/.clawdbot/skills/coinfello/config.json`
- 必须在运行 `send_prompt` 之前执行

### get_account

从本地配置文件中显示当前的智能账户地址。

```bash
npx @coinfello/agent-cli get_account
```

- 打印存储的 `smart_account_address`
- 如果尚未创建账户，则会显示错误并退出

### sign_in

使用 Sign-In with Ethereum (SIWE) 和您的智能账户进行身份验证。将会话令牌保存到本地配置文件中。

```bash
npx @coinfello/agent-cli sign_in
```

- 使用配置文件中存储的私钥进行登录
- 将会话令牌保存到 `~/.clawdbot/skills/coinfello/config.json`
- 后续的 `send.prompt` 调用会自动加载会话令牌
- 必须在 `create_account` 之后、`send_prompt` 之前执行，以确保身份验证成功

### set_delegation

将已签名的父委托（JSON 格式）保存到本地配置文件中。

```bash
npx @coinfello/agent-cli set_delegation '<delegation-json>'
```

- `<delegation-json>` — 代表 MetaMask 智能账户套件中的 `Delegation` 对象的 JSON 字符串

### send_prompt

向 CoinFello 发送自然语言提示。如果服务器需要委托来执行操作，CLI 会根据服务器请求的权限范围和链名自动生成并签署子委托。

```bash
npx @coinfello/agent-cli send_prompt "<prompt>"
```

**内部处理流程**：

1. 从 `/api/v1/automation/coinfello-agents` 获取可用的代理，并将提示发送到 CoinFello 的对话端点。
2. 如果服务器返回只读响应（没有 `clientToolCalls` 和 `txn_id`），则打印响应内容并退出。
3. 如果服务器直接返回 `txn_id` 且没有工具调用，则打印该 ID 并退出。
4. 如果服务器发送包含 `chainId` 和 `scope` 的 `ask_for_delegation` 客户端工具调用：
   - 获取 CoinFello 的代理地址
   - 使用工具调用中的链 ID 重新构建智能账户
   - 解析服务器提供的权限范围（支持 ERC-20、原生代币、ERC-721 和函数调用权限范围）
   - 如果智能账户尚未部署在链上，则创建并签署子委托（使用 ERC-6492 签名）
   - 将签名的委托作为 `clientToolCallResponse` 与初始响应中的 `chatId` 和 `callId` 一起发送回去
   - 返回一个 `txn_id` 以便追踪

### get_transaction_status

检查之前提交的交易状态。

```bash
npx @coinfello/agent-cli get_transaction_status <txn_id>
```

- 返回包含当前交易状态的 JSON 对象

## 常见工作流程

### 基本操作：发送提示（服务器驱动的委托）

```bash
# Create account if not already done
npx @coinfello/agent-cli create_account sepolia

# Sign in (required for delegation flows)
npx @coinfello/agent-cli sign_in

# Send a natural language prompt — delegation is handled automatically
npx @coinfello/agent-cli send_prompt "send 5 USDC to 0xRecipient..."

# Check the result
npx @coinfello/agent-cli get_transaction_status <txn_id-from-above>
```

### 只读提示

某些提示不需要执行交易。CLI 会自动检测这一点，并仅打印响应内容。

```bash
npx @coinfello/agent-cli send_prompt "what is the chain ID for Base?"
```

## 边缘情况

- **没有智能账户**：在运行 `send_prompt` 之前，请先运行 `create_account`。CLI 会检查配置文件中是否有保存的私钥和地址。
- **未登录**：如果服务器需要身份验证，请在运行 `send_prompt` 之前先运行 `sign_in`。
- **无效的链名**：CLI 会抛出错误，并列出有效的 viem 链名。
- **只读响应**：如果服务器返回仅包含文本的响应且没有交易信息，CLI 会打印该响应并退出，而不会创建委托。

## 参考资料

有关完整的配置方案、支持的链、API 详情、权限范围类型和故障排除方法，请参阅 [references/REFERENCE.md]。

有关端到端自动化脚本，请参阅 [scripts/setup-and-send.sh]。
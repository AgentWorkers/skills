---
name: coinfello
description: '使用 `@coinfello/agent-cli` 与 CoinFello 进行交互，可以创建 MetaMask 智能账户、使用 SIWE 登录、管理委托关系、发送基于服务器驱动的 ERC-20 代币委托指令，以及查询交易状态。当用户希望通过自然语言指令发送加密交易、管理智能账户的委托关系或查看 CoinFello 的交易结果时，可以使用该工具。'
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
          default: 'https://app.coinfello.com/'
---
# CoinFello CLI 功能

使用 `npx @coinfello/agent-cli` CLI 通过 MetaMask 智能账户与 CoinFello 进行交互。该 CLI 支持智能账户的创建、SIWE 认证、委托管理、基于提示的交易执行以及交易状态查询。

## 前提条件

- 需要 Node.js 20 或更高版本（`npx` 已包含在 Node.js 中）。

该 CLI 可通过 `npx @coinfello/agent-cli` 获取。无需手动构建。

## 环境变量

| 变量                | 是否必填 | 默认值                          | 说明                                      |
|--------------------|--------|----------------------------------|------------------------------------------|
| `COINFELLO_BASE_URL`    | 否       | `https://app.coinfello.com/`                   | CoinFello API 的基础 URL                          |
|                    |        |                                           |

## 安全提示

此功能执行以下敏感操作：

- **密钥生成与存储**：默认情况下，`create_account` 会在 **macOS 安全沙箱**（或支持的 TPM 2.0）中生成硬件支持的 P256 密钥。私钥始终存储在硬件中，无法导出——仅将公钥坐标和密钥标签保存到 `~/.clawdbot/skills/coinfello/config.json` 文件中。如果硬件密钥支持不可用，CLI 会发出警告并切换到软件密钥。您也可以通过传递 `--use-unsafe-private-key` 显式选择使用明文软件密钥（仅限开发和测试用途）。
- **会话令牌存储**：运行 `sign_in` 会将 SIWE 会话令牌存储在同一配置文件中。
- **委托签名**：运行 `send_prompt` 可能会根据服务器请求的权限范围自动生成并签署区块链委托，然后将其提交给 CoinFello API。

用户在运行委托流程之前，应确保信任通过 `COINFELLO_BASE_URL` 配置的 CoinFello API 端点。

## 快速入门

```bash
# 1. Create a smart account on a chain (uses Secure Enclave by default)
npx @coinfello/agent-cli create_account sepolia

# 2. Sign in to CoinFello with your smart account (SIWE)
npx @coinfello/agent-cli sign_in

# 3. Send a natural language prompt — the server will request a delegation if needed
npx @coinfello/agent-cli send_prompt "send 5 USDC to 0xRecipient..."
```

## 命令

### create_account

创建一个 MetaMask 混合智能账户。默认情况下，签名密钥会在 **macOS 安全沙箱** 中生成（硬件支持，不可导出）。如果安全沙箱不可用，CLI 会发出警告并切换到软件密钥。可以通过传递 `--use-unsafe-private-key` 显式使用明文软件密钥（仅限开发和测试用途）。

```bash
npx @coinfello/agent-cli create_account <chain> [--use-unsafe-private-key]
```

- `<chain>` — Viem 链名：`sepolia`、`mainnet`、`polygon`、`arbitrum`、`optimism`、`base` 等。
- **默认（安全沙箱）**：在硬件中生成 P256 密钥；将 `key_tag`、`public_key_x`、`public_key_y`、`key_id`、`smart_account_address` 和 `chain` 保存到 `~/.clawdbot/skills/coinfello/config.json` 文件中。私钥始终存储在安全沙箱中。
- `--use-unsafe-private-key`：生成一个随机的 secp256k1 私钥，并将其以 **明文** 形式保存在配置文件中。仅用于开发和测试。
- 必须在 `send_prompt` 之前运行。

### get_account

从本地配置文件中显示当前的智能账户地址。

```bash
npx @coinfello/agent-cli get_account
```

- 打印存储的 `smart_account_address`
- 如果尚未创建账户，则会输出错误信息并退出

### sign_in

使用以太坊的 Sign-In with Ethereum (SIWE) 和您的智能账户进行身份验证。将会话令牌保存到本地配置文件中。

```bash
npx @coinfello/agent-cli sign_in
```

- 使用配置文件中存储的私钥进行登录
- 将会话令牌保存到 `~/.clawdbot/skills/coinfello/config.json`
- 后续的 `send_prompt` 调用会自动加载会话令牌
- 必须在 `create_account` 之后、`send_prompt` 之前运行，以进行身份验证后的操作

### set_delegation

将已签署的父委托（JSON 格式）保存到本地配置文件中。

```bash
npx @coinfello/agent-cli set_delegation '<delegation-json>'
```

- `<delegation-json>` — 代表 MetaMask 智能账户套件中的 `Delegation` 对象的 JSON 字符串

### send_prompt

向 CoinFello 发送自然语言提示。如果服务器需要委托来执行操作，CLI 会根据服务器请求的权限范围自动生成并签署子委托。

```bash
npx @coinfello/agent-cli send_prompt "<prompt>"
```

**内部处理流程**：

1. 从 `/api/v1/automation/coinfello-agents` 获取可用的代理，并将提示发送到 CoinFello 的对话端点。
2. 如果服务器返回只读响应（没有 `clientToolCalls` 和 `txn_id`），则打印响应内容并退出。
3. 如果服务器直接返回 `txn_id` 且没有工具调用，则打印该 ID 并退出。
4. 如果服务器发送包含 `chainId` 和 `scope` 的 `ask_for_delegation` 客户端工具调用：
   - 获取 CoinFello 的委托地址。
   - 使用工具调用中的链 ID 重新构建智能账户。
   - 解析服务器提供的权限范围（支持 ERC-20、原生代币、ERC-721 和函数调用权限范围）。
   - 如果智能账户尚未在链上部署，则创建并签署子委托（使用 ERC-6492 签名）。
   - 将签署后的委托作为 `clientToolCallResponse` 与初始响应中的 `chatId` 和 `callId` 一起发送回去。
   - 返回一个 `txn_id` 以便跟踪。

## 常见工作流程

### 基本操作：发送提示（服务器驱动的委托）

```bash
# Create account if not already done (uses Secure Enclave by default)
npx @coinfello/agent-cli create_account sepolia

# Sign in (required for delegation flows)
npx @coinfello/agent-cli sign_in

# Send a natural language prompt — delegation is handled automatically
npx @coinfello/agent-cli send_prompt "send 5 USDC to 0xRecipient..."
```

### 只读提示

某些提示不需要执行交易。CLI 会自动检测这一点，并仅打印响应内容。

```bash
npx @coinfello/agent-cli send_prompt "what is the chain ID for Base?"
```

## 燃气费用估算

实际的链上燃气费用因网络而异。**请勿** 将以太坊主网的燃气费用假设为 L2 链路的费用。

| 网络            | 交换/转账燃气费用                |
|------------------|------------------------|
| Base            | $0.0003 – $0.0006                |

这些是在正常网络条件下的大致费用范围。像 Base 这样的 L2 链路比以太坊主网便宜得多。

## 特殊情况

- **没有智能账户**：在运行 `send_prompt` 之前，请先运行 `create_account`。CLI 会检查配置文件中是否保存了私钥和地址。
- **未登录**：如果服务器需要身份验证，请在运行 `send_prompt` 之前先运行 `sign_in`。
- **无效的链名**：CLI 会抛出错误，并列出有效的 viem 链名。
- **只读响应**：如果服务器返回不含交易的文本响应，CLI 会打印该响应并退出，而不会创建委托。

## 参考资料

有关完整的配置方案、支持的链路、API 详情、权限范围类型和故障排除方法，请参阅 [references/REFERENCE.md](references/REFERENCE.md)。
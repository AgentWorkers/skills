---
name: coinfello
description: '使用 `@coinfello/agent-cli` 与 CoinFello 进行交互，可以创建智能账户、使用 SIWE 进行登录、管理委托关系、通过服务器驱动的 ERC-20 代币委托发送指令，以及查询交易状态。当用户希望通过自然语言指令发送加密交易、管理智能账户的委托关系或查看 CoinFello 的交易结果时，可以使用该工具。'
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
# CoinFello CLI 功能简介

您可以使用 `npx @coinfello/agent-cli@latest` CLI 来与 CoinFello 进行交互。该 CLI 支持智能账户的创建、SIWE（Sign-In with Ethereum）身份验证、委托管理、基于提示的交易执行以及交易状态查询等功能。

## 前提条件

- 需要 Node.js 20 或更高版本（`npx` 已包含在 Node.js 中）。

您可以通过 `npx @coinfello/agent-cli@latest` 来使用该 CLI，无需手动构建。

## 环境变量

| 变量                | 是否必需 | 默认值                          | 说明                          |
|--------------------|--------|----------------------------|--------------------------------------------|
| `COINFELLO_BASE_URL`    | 否       | `https://app.coinfello.com/`            | CoinFello API 的基础 URL                        |
|                      |        |                                  |

## 安全注意事项

该 CLI 执行以下敏感操作：

- **密钥生成与存储**：默认情况下，`create_account` 会在 **macOS 安全隔层（Secure Enclave）**（或支持 TPM 2.0 的设备）中生成一个硬件支持的 P256 密钥。私钥始终保留在硬件中，无法导出；只有公钥坐标和密钥标签会被保存到 `~/.clawdbot/skills/coinfello/config.json` 文件中。如果硬件密钥支持不可用，CLI 会发出警告并切换到软件私钥模式。您也可以通过传递 `--use-unsafe-private-key` 参数明确选择使用明文软件密钥（仅限开发和测试用途）。
- **签名守护进程（signer-daemon）**：运行 `signer-daemon start` 会通过 Touch ID 或密码进行一次身份验证，并将授权信息缓存起来。后续的所有签名操作都将使用这个缓存的信息，从而避免重复的认证提示。该守护进程通过具有受限权限（0600）的用户级 Unix 域名套接字进行通信。如果守护进程未运行，签名操作将直接执行（每次都需要输入 Touch ID）。
- **会话令牌存储**：运行 `sign_in` 会将 SIWE 会话令牌保存到配置文件中。
- **委托签名**：运行 `send_prompt` 可能会根据服务器请求的权限范围自动生成并签署区块链委托，然后将其提交给 CoinFello API。

在使用委托功能之前，请确保您信任通过 `COINFELLO_BASE_URL` 配置的 CoinFello API 端点。

## 快速入门

```bash
# 1. Start the signing daemon (optional, but avoids repeated Touch ID prompts)
npx @coinfello/agent-cli@latest signer-daemon start

# 2. Create a smart account (uses Secure Enclave by default)
npx @coinfello/agent-cli@latest create_account

# 3. Sign in to CoinFello with your smart account (SIWE)
npx @coinfello/agent-cli@latest sign_in

# 4. Send a natural language prompt — the server will request a delegation if needed
npx @coinfello/agent-cli@latest send_prompt "send 5 USDC to 0xRecipient..."
```

## 命令说明

### create_account

创建一个 MetaMask 混合智能账户。默认情况下，签名密钥会在 **macOS 安全隔层** 中生成（硬件支持，不可导出）。如果安全隔层不可用，CLI 会发出警告并切换到软件密钥模式。可以通过传递 `--use-unsafe-private-key` 参数明确使用明文软件密钥（仅限开发和测试用途）。

```bash
npx @coinfello/agent-cli@latest create_account [--use-unsafe-private-key]
```

- **默认模式（使用安全隔层）**：在硬件中生成一个 P256 密钥，并将 `key_tag`、`public_key_x`、`public_key_y`、`key_id` 和 `smart_account_address` 保存到 `~/.clawdbot/skills/coinfello/config.json` 文件中。私钥始终保留在安全隔层中。
- **`--use-unsafe-private-key`**：生成一个随机的 secp256k1 私钥，并以明文形式保存到配置文件中。仅用于开发和测试。
- 必须在运行 `send_prompt` 之前执行此命令。

### get_account

从本地配置文件中显示当前的智能账户地址。

```bash
npx @coinfello/agent-cli@latest get_account
```

- 打印保存的 `smart_account_address`。
- 如果尚未创建账户，则会输出错误信息并退出。

### sign_in

使用 SIWE（Sign-In with Ethereum）和您的智能账户进行身份验证，并将会话令牌保存到本地配置文件中。

```bash
npx @coinfello/agent-cli@latest sign_in
```

- 使用配置文件中保存的私钥进行登录。
- 将会话令牌保存到 `~/.clawdbot/skills/coinfello/config.json` 文件中。
- 后续的 `send_prompt` 操作会自动加载会话令牌。
- 必须在 `create_account` 之后、`send_prompt` 之前执行此命令，以确保操作具有有效的身份验证。

### set_delegation

将已签名的父委托（JSON 格式）保存到本地配置文件中。

```bash
npx @coinfello/agent-cli@latest set_delegation '<delegation-json>'
```

- `<delegation-json>`：一个表示 MetaMask 智能账户委托对象的 JSON 字符串。

### new_chat

清除本地配置文件中保存的聊天会话 ID，以便下次 `send_prompt` 时能够开始新的对话。

```bash
npx @coinfello/agent-cli@latest new_chat
```

- 从 `~/.clawdbot/skills/coinfello/config.json` 文件中删除 `chat_id`。
- 当您需要重置对话上下文时（例如在上下文窗口出现错误后），可以使用此命令。

### signer-daemon

管理安全隔层签名守护进程。启动守护进程后，会通过 Touch ID 或密码进行一次身份验证，并将授权信息缓存起来，从而避免后续操作再次需要输入密码。

```bash
npx @coinfello/agent-cli@latest signer-daemon start    # Start daemon (one-time auth)
npx @coinfello/agent-cli@latest signer-daemon status   # Check if daemon is running
npx @coinfello/agent-cli@latest signer-daemon stop     # Stop the daemon
```

- 如果守护进程未运行，所有涉及安全隔层的操作都将直接执行（每次都需要输入 Touch ID）。
- 该守护进程是可选的——所有命令在没有守护进程的情况下也能正常运行。

### send_prompt

向 CoinFello 发送自然语言提示。如果服务器需要执行某个操作，CLI 会根据服务器请求的权限范围自动生成并签署一个子委托。

```bash
npx @coinfello/agent-cli@latest send_prompt "<prompt>"
```

**注意**：如果收到以下错误信息：
```
Failed to send prompt: Conversation request failed (400): {"error":"Your input exceeds the context window of this model. Please adjust your input or start a new chat and try again."
```
则需要执行 `npx @coinfello/agent-cli@latest new_chat` 以启动一个新的对话窗口。

**内部工作流程**：

1. 从 `/api/v1/automation/coinfello-agents` 获取可用的代理服务，并将提示发送到 CoinFello 的对话端点。
2. 如果服务器返回只读响应（没有 `clientToolCalls` 和 `txn_id`），则直接打印响应内容并退出。
3. 如果服务器直接返回 `txn_id` 且没有其他请求，也会直接打印该 ID 并退出。
4. 如果服务器发送包含 `chainId` 和 `scope` 的 `ask_for_delegation` 请求：
   - 获取 CoinFello 的委托地址。
   - 根据请求的链 ID 重新生成智能账户。
   - 解析服务器提供的权限范围（支持 ERC-20、ERC-721 和函数调用权限范围）。
   - 如果智能账户尚未部署在链上，会生成并签署一个子委托（使用 ERC-6492 签名）。
   - 将签名的委托作为 `clientToolCallResponse` 与初始响应中的 `chatId` 和 `callId` 一起发送回去。
   - 返回一个 `txn_id` 用于跟踪操作。

## 常见工作流程

### 基本操作：发送提示（服务器驱动的委托）

```bash
# Start the signing daemon (optional, reduces Touch ID prompts)
npx @coinfello/agent-cli@latest signer-daemon start

# Create account if not already done (uses Secure Enclave by default)
npx @coinfello/agent-cli@latest create_account

# Sign in (required for delegation flows)
npx @coinfello/agent-cli@latest sign_in

# Send a natural language prompt — delegation is handled automatically
npx @coinfello/agent-cli@latest send_prompt "send 5 USDC to 0xRecipient..."
```

### 只读提示

某些提示不需要执行任何交易操作，CLI 会自动识别这种情况并直接显示响应内容。

```bash
npx @coinfello/agent-cli@latest send_prompt "what is the chain ID for Base?"
```

## 燃气费用估算

实际的链上燃气费用因网络而异。请**不要**将以太坊主网的燃气费用直接应用于 L2（Layer 2）链。

| 网络        | 交换/转账燃气费用            |
|------------|------------------------|
| Base       | $0.0003 – $0.0006            |

这些费用是在正常网络条件下的大致范围。像 Base 这样的 L2 链路的费用通常比以太坊主网要低得多。

## 特殊情况

- **没有智能账户**：在运行 `send_prompt` 之前，请先运行 `create_account`。CLI 会检查配置文件中是否保存有私钥和账户地址。
- **未登录**：如果服务器需要身份验证，请在运行 `send.prompt` 之前先执行 `sign_in`。
- **无效的链名**：CLI 会抛出错误并列出有效的链名。
- **只读响应**：如果服务器返回纯文本响应且没有交易相关内容，CLI 会直接打印该响应并退出，而不会生成任何委托。

## 参考资料

有关完整的配置方案、支持的链、API 详情、权限范围类型和故障排除方法，请参阅 [references/REFERENCE.md](references/REFERENCE.md)。
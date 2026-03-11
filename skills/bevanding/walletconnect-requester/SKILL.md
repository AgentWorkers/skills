---
name: walletconnect-requester
description: 为AI代理提供安全的WalletConnect集成功能。作为DApp（提案者），您可以连接用户的钱包，而无需直接处理用户的私钥。您可以发起交易请求并生成交易签名，所有操作都由用户在他们的钱包中亲自批准。这种方案实现了零托管（即数据不存储在第三方服务器上），从而确保了最高级别的安全性。当您需要通过WalletConnect v2安全地与用户钱包进行交互时，可以使用此功能。
metadata:
  openclaw:
    requires:
      env:
        - WC_PROJECT_ID (required): WalletConnect Cloud Project ID
        - WC_METADATA_NAME (optional): DApp name shown in wallet
        - WC_METADATA_URL (optional): DApp URL
        - WC_METADATA_ICONS (optional): DApp icon URLs (comma-separated)
    persistence:
      path: ~/.walletconnect-requester/
      files:
        - sessions.json: Active WalletConnect sessions
        - audit.log: Transaction audit log (masked sensitive data)
    security_notes:
      - WalletConnect URI contains symmetric key (symKey) - treat as sensitive
      - Session tokens grant transaction request capability - protect accordingly
      - Audit logs contain masked addresses and tx hashes - review before sharing
---
# WalletConnect 请求器

> **零托管。最高安全性。用户始终掌握控制权。**

## 为什么选择这个技能？

与 `walletconnect-agent` 不同，`walletconnect-requester` 采用了完全不同的处理方式：

| | walletconnect-agent | walletconnect-requester（本技能） |
|---|---|---|
| **私钥** | ⚠️ 存储在代理端 | ✅ 从不接触代理端 |
| **签名** | ⚠️ 自动执行所有签名操作 | ✅ 每笔交易均需用户批准 |
| **安全模型** | 托管模式（代理端拥有完全控制权） | **非托管模式（用户拥有完全控制权）** |
| **如果代理端被入侵** | ⚠️ 资金可能被盗 | ✅ 资金安全——没有私钥可供窃取 |

**这是 AI 代理与 Web3 交互的最安全方式。**

## 功能概述

- **通过 WalletConnect v2 连接到用户钱包**  
- **请求交易**——用户需在钱包中批准  
- **请求签名**——用户需在钱包中完成签名  
- **零私钥泄露**——私钥始终保留在用户钱包中  

## 安全保障  

```
┌─────────────────┐                    ┌─────────────────┐
│   AI Agent      │                    │   User Wallet   │
│   (Requester)   │ ◄── WalletConnect ──► │   (Signer)      │
│                 │     Session          │                 │
└─────────────────┘                    └─────────────────┘
         │                                    │
         │  1. Request transaction            │
         │ ─────────────────────────────────► │
         │                                    │
         │  2. User reviews & approves        │
         │    (in wallet UI)                  │
         │                                    │
         │  3. Signed transaction             │
         │ ◄───────────────────────────────── │
         │                                    │
         ▼                                    ▼
    NO PRIVATE KEYS                      PRIVATE KEYS
    NO AUTO-SIGN                         USER APPROVES
    USER IN CONTROL                      EVERYTHING
```

## 安装流程

### 第一步：安装依赖项

本技能需要 Node.js 的依赖项。请全局或本地安装它们：  
```bash
# Install dependencies
npm install @walletconnect/sign-client @walletconnect/core qrcode
```

### 第二步：获取 WalletConnect 项目 ID

1. 访问 [WalletConnect Cloud](https://cloudwalletconnect.com/)  
2. 创建一个新的项目  
3. 复制你的 **项目 ID**  

### 第三步：设置环境变量  

```bash
export WC_PROJECT_ID="your_project_id_here"
```

### 第四步：运行技能  

```bash
node scripts/wc-requester.js connect
```

---

## 快速入门

### 第一步：创建会话  

```bash
export WC_PROJECT_ID="your_project_id"
node scripts/wc-requester.js connect
```

**输出结果：**  
```
WalletConnect URI: wc:abc123...@2?relay-protocol=irn&symKey=xyz

Scan this QR code with your wallet:
[QR CODE]

Waiting for wallet to connect...
```

### 第二步：请求交易  

```bash
node scripts/wc-requester.js request-tx \
  --to 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --data 0xa9059cbb... \
  --value 0 \
  --chain 8453
```

用户在钱包中看到的内容：  
```
Send 10 USDC to 0x1F3A...?
[Approve] [Reject]
```

### 第三步：请求签名  

```bash
node scripts/wc-requester.js request-sign \
  --message "Sign this message to verify ownership" \
  --chain 8453
```

## 命令说明

### `connect` - 创建 WalletConnect 会话  

```bash
node scripts/wc-requester.js connect [options]

Options:
  --chains <ids>     Comma-separated chain IDs (default: 8453,1)
  --methods <list>   Comma-separated methods (default: eth_sendTransaction,personal_sign)
  --qr <path>        Generate QR code to file
  --json             Output as JSON
```

### `request-tx` - 请求交易  

```bash
node scripts/wc-requester.js request-tx --to <address> --data <hex> --value <wei> --chain <id>
```

### `request-sign` - 请求签名  

```bash
node scripts/wc-requester.js request-sign --message <text> --chain <id>
# or for typed data
node scripts/wc-requester.js request-sign --typed-data <json> --chain <id>
```

### `sessions` - 列出活跃会话  

```bash
node scripts/wc-requester.js sessions
```

### `disconnect` - 结束会话  

```bash
node scripts/wc-requester.js disconnect --topic <topic>
```

## 安全模型

### 代理端可以执行的操作  
- ✅ 请求交易（用户必须批准）  
- ✅ 请求签名（用户必须批准）  
- ✅ 查看连接的钱包地址  
- ✅ 查看会话元数据  

### 代理端不能执行的操作  
- ❌ 无法持有私钥  
- ❌ 无法自动执行任何操作  
- ❌ 无法在未经批准的情况下执行交易  
- ❌ 无法直接访问资金  

### 如果代理端被入侵  
- ✅ 攻击者无法窃取资金（因为没有私钥）  
- ✅ 攻击者无法自动执行交易  
- ✅ 用户可以拒绝任何可疑请求  
- ✅ 用户可以随时断开会话  

### 本地数据持久化

本技能会将数据写入 `~/.walletconnect-requester/` 目录：  

| 文件 | 用途 | 敏感性 |
|------|---------|-------------|
| `sessions.json` | 活跃的 WalletConnect 会话信息 | ⚠️ 包含会话详情 |
| `audit.log` | 交易审计日志 | ⚠️ 包含经过屏蔽的交易哈希值 |

**安全建议：**  
- 在共享之前查看 `audit.log`  
- 不再需要时删除 `sessions.json`  
- 设置适当的文件权限：`chmod 600 ~/.walletconnect-requester/*`  

### 敏感数据处理  

| 数据类型 | 处理方式 |
|-----------|------------------|
| **WalletConnect URI** | 包含 `symKey`——仅在连接时显示一次，不会被记录 |
| **会话令牌** | 本地存储在 `sessions.json` 中，不会外部传输 |
| **交易哈希值** | 记录在 `audit.log` 中，地址会被屏蔽 |
| **私钥** | 本技能绝对不会处理私钥 |

### 隐私保护措施  

- WalletConnect URI（包含 `symKey`）会输出到标准输出（stdout）以生成 QR 码  
- 审计日志中的地址会被屏蔽（例如显示为 `0x8335...` 而非完整地址）  
- 除 WalletConnect 中继网络外，不会向任何外部服务器发送数据  

## 配置设置

### 环境变量  

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `WC_PROJECT_ID` | 是 | WalletConnect Cloud 项目 ID |
| `WC_METADATA_NAME` | 否 | 在钱包中显示的 DApp 名称 |
| `WC_METADATA_URL` | 否 | DApp 的 URL |
| `WC_METADATA_ICONS` | 否 | DApp 的图标 URL |

### 命名空间配置

默认情况下，本技能仅请求最低权限：  
```json
{
  "eip155": {
    "chains": ["eip155:8453", "eip155:1"],
    "methods": ["eth_sendTransaction", "personal_sign"],
    "events": ["accountsChanged", "chainChanged"]
  }
}
```

## 示例工作流程

### 连接钱包并请求支付  

```bash
# 1. Create session
node scripts/wc-requester.js connect --qr /tmp/qr.png
# User scans QR with MetaMask

# 2. Request USDC transfer
node scripts/wc-requester.js request-tx \
  --to 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --data 0xa9059cbb0000... \
  --chain 8453

# User sees: "Send 10 USDC?" → Approves in wallet
# Returns: tx_hash
```

### 验证钱包所有权  

```bash
# 1. Connect
node scripts/wc-requester.js connect

# 2. Request signature
node scripts/wc-requester.js request-sign \
  --message "I own this wallet on March 9, 2026"

# User signs in wallet
# Returns: signature
```

## 与其他解决方案的比较  

| 功能 | 本技能 | walletconnect-agent | MetaMask SDK |
|---------|-----------|---------------------|--------------|
| 私钥存储 | ❌ 绝不存储 | ⚠️ 存储在代理端 | ❌ 绝不存储 |
| 自动签名 | ❌ 绝不自动签名 | ✅ 支持 | ❌ 不支持 |
| 是否需要用户批准 | ✅ 必须用户批准 | ❌ 不需要 | ✅ 必须用户批准 |
| 多钱包支持 | ✅ 支持任意 WalletConnect 钱包 | ✅ 支持任意 WalletConnect 钱包 | ❌ 仅支持 MetaMask |
| 安全性 | **最高** | 中等 | 高 |
| 适用场景 | 用户需控制交易流程 | 自动化交易 | MetaMask 用户 |

## 支持的钱包  

任何支持 WalletConnect v2 的钱包：  
- MetaMask Mobile  
- Rainbow  
- Trust Wallet  
- Coinbase Wallet  
- Ledger Live  
| 以及更多…… |

## 故障排除  

### “没有活跃会话”  
首先运行 `connect` 命令以创建会话。  

### “用户拒绝了请求”  
用户已在钱包中拒绝了请求。询问用户是否希望重试。  

### “会话过期”  
会话默认持续 7 天。重新连接以创建新会话。  

### “不支持的链路”  
用户的钱包不支持请求的链路。请用户切换网络。  

## 审计日志  

所有请求都会被记录（但不包含敏感数据）：  
```
~/.walletconnect-requester/audit.log

{
  "timestamp": "2026-03-09T02:00:00Z",
  "action": "request_transaction",
  "chain": 8453,
  "to": "0x8335...",
  "status": "approved",
  "tx_hash": "0xabc123..."
}
```

## 何时使用本技能与 walletconnect-agent  

| 适用场景 | 适用 walletconnect-agent 的场景 |  
|----------------|-------------------|
| 用户必须批准每笔交易 | 完全自动的交易流程 |  
| 需要最高安全性 | 完全信任代理端 |  
| 一次性或偶尔的交易 | 24/7 自动运行 |  
| 用户希望完全控制交易流程 | 用户希望“设置一次即可长期使用” |  
| 代理端运行在不可信环境中 | 代理端运行在安全环境中 |  

**如有疑问，请使用本技能。** 它总是更安全的选择。  

---

## 许可证  

MIT 许可证 — 以安全性作为首要考虑因素进行开发。  

---

**维护者**：Web3 Investor Team  
**注册地址**：https://clawhub.com/skills/walletconnect-requester
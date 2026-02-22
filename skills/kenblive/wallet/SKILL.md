---
name: base-wallet
description: "🔐 基础钱包——AI代理的加密身份管理工具。支持创建钱包、签署消息（使用SIWE技术）、以及程序化地发送交易。无需浏览器扩展程序，也无需人工干预。这是构建自主Web3代理的基础。"
---

# 🔐 Base Wallet – 为AI代理提供加密身份管理工具

> 每个自主代理都需要一个钱包。无需人工协助即可创建钱包。

**简而言之：** 在Base/Ethereum平台上通过编程方式创建钱包，支持SIWE身份验证、余额查询和交易功能。

## 为什么选择Base Wallet？

- **真正的自主性**：代理可以自行创建并控制自己的钱包。
- **无需浏览器**：完全通过命令行（CLI）操作，无需扩展程序或弹窗。
- **支持SIWE**：使用Ethereum进行Web3服务的登录。
- **默认情况下非常安全**：使用环境变量存储密钥，避免明文密钥的泄露。

您可以编程方式创建和管理兼容Ethereum的Base链钱包。

---

## ⚠️ 安全至上

| 推荐做法 | 不推荐的做法 |
|---------|-------------------------|
| 使用**环境变量**存储私钥 | 将私钥存储在明文文件中 |
| 将钱包文件设置为**chmod 600**权限 | 将钱包文件提交到Git仓库 |
| 使用`--env`模式（推荐） | 直接在控制台中输出私钥（`console.log(privateKey)`） |
| **离线**备份助记词 | 共享私钥或助记词 |

---

## 快速入门

### 创建新钱包（推荐）

```bash
# Output as environment variable format (safest)
node scripts/create-wallet.js --env

# Output example:
# export WALLET_ADDRESS="0x..."
# export PRIVATE_KEY="0x..."
```

然后将生成的配置信息复制到您的shell或`.env`文件中。

### 使用文件存储创建钱包（可选）

```bash
# Only if you need file-based storage
node scripts/create-wallet.js --managed my-agent
```

**注意：** 这种方式会将私钥存储在`~/.openclaw/wallets/my-agent.json`文件中。

---

## 使用示例

### 从环境变量中加载钱包

```javascript
const { ethers } = require('ethers');

// ✅ SECURE: Load from environment variable
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY);
console.log('Address:', wallet.address);
// ❌ NEVER: console.log('Private Key:', wallet.privateKey);
```

### 从助记词中加载钱包

```javascript
const wallet = ethers.Wallet.fromPhrase(process.env.MNEMONIC);
```

### 查看余额

```javascript
const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
const balance = await provider.getBalance(wallet.address);
console.log('Balance:', ethers.formatEther(balance), 'ETH');
```

### 签署消息（使用SIWE）

```javascript
const message = `example.com wants you to sign in with your Ethereum account:
${wallet.address}

Sign in message

URI: https://example.com
Version: 1
Chain ID: 8453
Nonce: ${nonce}
Issued At: ${new Date().toISOString()}`;

const signature = await wallet.signMessage(message);
```

### 发送交易

```javascript
const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
const connectedWallet = wallet.connect(provider);

const tx = await connectedWallet.sendTransaction({
  to: recipientAddress,
  value: ethers.parseEther('0.001')
});

const receipt = await tx.wait();
console.log('TX Hash:', tx.hash);
```

---

## 脚本示例

| 脚本 | 说明 |
|--------|-------------------------|
| `create-wallet.js --env` | 创建钱包，并将配置信息作为环境变量输出（推荐） |
| `create-wallet.js --managed [name]` | 创建钱包并保存到文件中（可选） |
| `create-wallet.js --json` | 创建钱包，并将配置信息以JSON格式输出 |
| `basemail-register.js [name]` | 使用钱包签名注册BaseMail邮箱 |
| `check-balance.js [address]` | 查看钱包余额 |

---

## BaseMail集成

使用您的钱包签名注册@basemail.ai邮箱。

```bash
# If using environment variable:
PRIVATE_KEY="0x..." node scripts/basemail-register.js

# If using managed wallet:
node scripts/basemail-register.js my-agent
```

---

## 网络配置

| 网络 | 链路ID | RPC地址 |
|---------|-------------------------|
| Base Mainnet | 8453 | https://mainnet.base.org |
| Base Sepolia | 84532 | https://sepolia.base.org |

---

## 📝 审计日志记录

所有操作都会被记录到`~/.base-wallet/audit.log`文件中。

---

## 安全存储规范

**如果必须将钱包信息存储到文件中（不推荐的做法）：**

```javascript
// ✅ Recommended: Use environment variables
const privateKey = process.env.PRIVATE_KEY;
if (!privateKey) {
  throw new Error('PRIVATE_KEY environment variable not set');
}
const wallet = new ethers.Wallet(privateKey);

// ❌ Avoid: Storing private keys in code or files
```

---

## `.gitignore`文件

请将以下内容添加到您项目的`.gitignore`文件中：

```gitignore
# Wallet files - NEVER commit!
.openclaw/
*.wallet.json
*.mnemonic
private-key*
```

---

## 依赖项

```bash
npm install ethers
```

---

## 更新日志

### v1.1.0 (2026-02-08)
- 🔐 安全性改进：将钱包创建方式改为可选的文件存储方式。
- ✨ 新增`--env`模式（推荐使用）。
- 📝 新增审计日志记录功能。
- ⚠️ 从示例代码中移除了直接输出私钥的语句。
- 📄 更新了安全相关文档。

### v1.0.0
- 🎉 首次发布
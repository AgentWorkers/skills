---
name: nad-wallet
description: "🔐 Nad Wallet：专为AI代理设计的Monad Chain身份验证工具。支持创建钱包、签署消息（SIWE），以及程序化地管理MON代币。该钱包专为Nad生态系统（nad.fun、NadMail、NadName）量身打造。"
---

# 🔐 Nad Wallet - 专为AI代理设计的Monad区块链钱包

> 每个自主代理都需要在Monad区块链上拥有一个钱包。无需人工协助即可创建一个钱包。

**简而言之：** 在Monad区块链上通过编程方式创建钱包。支持SIWE身份验证（用于NadMail），可查看MON代币余额，并集成到Nad生态系统中。

## 为什么选择Nad Wallet？

- **专为Monad区块链设计** — 专为Monad区块链（链ID 143）量身定制
- **真正的自主性** — 你的代理可以自行创建和控制自己的钱包
- **无需浏览器** — 仅使用命令行界面（CLI），无需扩展程序或弹窗
- **兼容Nad生态系统** — 支持NadMail、NadName、nad.fun等服务
- **支持SIWE** — 可使用以太坊的SIWE进行Web3服务登录
- **默认安全** — 使用环境变量存储密钥，避免明文存储

通过编程方式创建和管理Monad区块链钱包，以充分利用Nad生态系统。

---

## ⚠️ 安全第一

| 推荐操作 | 禁止操作 |
|---------|---------|
| 使用 **NAD_PRIVATE_KEY** 环境变量 | 将私钥存储在明文文件中 |
| 将钱包文件设置为 **chmod 600** | 将钱包文件提交到git仓库 |
| 使用 `--env` 模式（推荐） | 直接在控制台中输出私钥（`console.log(privateKey)`） |
| **离线** 备份助记词 | 共享私钥或助记词 |
| 仅将文件存储在 `~/.nad-wallet/` 目录下 | 系统会自动识别其他位置的钱包 |

**🔒 安全标准：** 采用与Base Wallet相同的安全策略，但针对Monad/Nad生态系统进行了调整。

---

## 网络信息

| 属性 | 值 |
|---------|---------|
| **区块链** | Monad |
| **链ID** | 143 |
| **RPC地址** | https://rpc.monad.xyz |
| **浏览器工具** | https://explorer.monad.xyz |
| **原生代币** | MON |
| **生态系统** | nad.fun, NadMail, NadName |

---

## 快速入门

### 创建新钱包（推荐）

```bash
# Output as environment variable format (safest)
node scripts/create-wallet.js --env

# Output example:
# export NAD_WALLET_ADDRESS="0x..."
# export NAD_PRIVATE_KEY="0x..."
```

然后将代码复制到你的shell或`.env`文件中。

### 使用文件存储创建钱包（可选）

```bash
# Only if you need file-based storage
node scripts/create-wallet.js --managed my-agent
```

⚠️ 这种方法会将私钥存储在 `~/.nad-wallet/wallets/my-agent.json` 文件中。

---

## 使用示例

### 从环境变量中加载钱包

```javascript
const { ethers } = require('ethers');

// ✅ SECURE: Load from environment variable
const wallet = new ethers.Wallet(process.env.NAD_PRIVATE_KEY);
console.log('Address:', wallet.address);
// ❌ NEVER: console.log('Private Key:', wallet.privateKey);
```

### 连接到Monad区块链

```javascript
const provider = new ethers.JsonRpcProvider('https://rpc.monad.xyz');
const connectedWallet = wallet.connect(provider);

// Check balance
const balance = await provider.getBalance(wallet.address);
console.log('Balance:', ethers.formatEther(balance), 'MON');
```

### 用SIWE签署消息（用于NadMail）

```javascript
const message = `nadmail.ai wants you to sign in with your Ethereum account:
${wallet.address}

Sign in to NadMail

URI: https://nadmail.ai
Version: 1
Chain ID: 143
Nonce: ${nonce}
Issued At: ${new Date().toISOString()}`;

const signature = await wallet.signMessage(message);
```

### 发送交易

```javascript
const provider = new ethers.JsonRpcProvider('https://rpc.monad.xyz');
const connectedWallet = wallet.connect(provider);

const tx = await connectedWallet.sendTransaction({
  to: recipientAddress,
  value: ethers.parseEther('0.1') // 0.1 MON
});

const receipt = await tx.wait();
console.log('TX Hash:', tx.hash);
console.log('Explorer:', `https://explorer.monad.xyz/tx/${tx.hash}`);
```

---

## 脚本

| 脚本 | 说明 |
|--------|-------------|
| `create-wallet.js --env` | 创建钱包，并将信息输出为环境变量（推荐） |
| `create-wallet.js --managed [name]` | 创建钱包并保存到文件（可选） |
| `create-wallet.js --json` | 创建钱包，并将信息输出为JSON格式 |
| `nadmail-register.js --handle [name]` | 使用SIWE在NadMail中注册 |
| `check-balance.js [address]` | 查看MON代币余额 |

---

## NadMail集成

使用你的钱包签名在NadMail（Nad生态系统的Web3电子邮件服务）中注册。

### 使用环境变量的方法（推荐）

```bash
# Set your private key
export NAD_PRIVATE_KEY="0x..."

# Register with your desired handle
node scripts/nadmail-register.js --handle littlelobster
```

### 使用文件存储的方法

```bash
# First create a managed wallet
node scripts/create-wallet.js --managed my-agent

# Then register for NadMail
node scripts/nadmail-register.js --wallet my-agent --handle littlelobster
```

### 注册流程

1. **开始认证** — 向NadMail API请求认证信息
2. **签署消息** — 使用私钥签署SIWE消息
3. **完成注册** — 提交签名以完成注册流程
4. **保存访问令牌** — 将访问令牌存储在 `~/.nad-wallet/nadmail-token.json` 文件中

---

## 查看余额

```bash
# Using environment variable
NAD_PRIVATE_KEY="0x..." node scripts/check-balance.js

# Using managed wallet
node scripts/check-balance.js my-wallet

# Using specific address
node scripts/check-balance.js 0x1234...5678
```

示例输出：
```
💰 Nad Wallet Balance Check
==================================================
Address: 0x1234...5678
Network: Monad (Chain ID 143)
RPC: https://rpc.monad.xyz

💎 Balance: 42.5 MON
Wei: 42500000000000000000

🔗 Explorer: https://explorer.monad.xyz/address/0x1234...5678

🌐 Nad Ecosystem:
  • nad.fun - Meme token platform
  • NadMail (nadmail.ai) - Web3 email  
  • NadName (app.nad.domains) - Domain names
```

---

## 文件结构

```
~/.nad-wallet/
├── wallets/              # Managed wallet storage
│   ├── my-agent.json     # Wallet file (600 perms)
│   └── my-agent.mnemonic # Backup phrase (400 perms)
├── nadmail-token.json    # NadMail API token (600 perms)
└── audit.log            # Operation audit log (600 perms)
```

---

## Nad生态系统服务

### 🎭 nad.fun
- 模因代币创建平台
- 社区驱动的代币发行
- 基于Monad区块链，支持快速交易

### 📧 NadMail (nadmail.ai)
- Nad生态系统的Web3电子邮件服务
- 支持使用钱包进行SIWE身份验证
- 通过 `nadmail-register.js` 脚本集成

### 🌐 NadName (app.nad.domains)
- Nad生态系统的域名服务
- 将人类可读的名称与钱包地址关联
- 基于Monad区块链基础设施构建

---

## 📝 审计日志

所有操作都会被记录到 `~/.nad-wallet/audit.log` 文件中，记录内容包括：
- 时间戳
- 操作类型（如：wallet_created, nadmail_registered等）
- 隐藏地址信息（仅显示前6位和最后4位）
- 操作结果（成功/失败）
- **不记录敏感数据**（私钥不会被记录）

---

## 安全最佳实践

### 环境变量设置

```bash
# ✅ Recommended approach
export NAD_PRIVATE_KEY="0x..."
export NAD_WALLET_ADDRESS="0x..."

# Use in scripts
node scripts/check-balance.js
node scripts/nadmail-register.js --handle myname
```

### 文件存储注意事项

```javascript
const fs = require('fs');
const path = require('path');

// Store with restricted permissions (only if absolutely necessary)
const filepath = path.join(process.env.HOME, '.nad-wallet', 'wallets', 'wallet.json');
fs.writeFileSync(filepath, JSON.stringify({ 
  address: wallet.address,
  privateKey: wallet.privateKey // Only store if absolutely necessary
}), { mode: 0o600 }); // Owner read/write only
```

### `.gitignore` 文件配置

将以下内容添加到项目的`.gitignore`文件中：

```gitignore
# Nad Wallet files - NEVER commit!
.nad-wallet/
*.wallet.json
*.mnemonic
private-key*
nad-private-key*

# Environment files
.env
.env.local
```

---

## 与Base Wallet的差异

| 对比项 | Base Wallet | Nad Wallet |
|---------|---------|------------|
| **区块链** | Base（链ID 8453） | Monad（链ID 143） |
| **RPC地址** | https://mainnet.base.org | https://rpc.monad.xyz |
| **浏览器工具** | basescan.org | explorer.monad.xyz |
| **原生代币** | ETH | MON |
| **电子邮件服务** | BaseMail | NadMail |
| **配置文件目录** | ~/.base-wallet/ | ~/.nad-wallet/ |
| **钱包文件目录** | ~/.openclaw/wallets/ | ~/.nad-wallet/wallets/ |
| **环境变量** | PRIVATE_KEY | NAD_PRIVATE_KEY |
| **生态系统** | Base生态系统 | nad.fun, NadMail, NadName |

### 从Base Wallet迁移

如果你有使用Base Wallet的经验：
1. **安全机制相同** — 所有安全措施均保持一致
2. **使用不同的区块链** — 使用Monad区块链（链ID 143）
3. **代币不同** — 使用MON代币而非ETH
4. **服务不同** | 使用NadMail而非BaseMail
5. **文件目录不同** | 钱包文件位于 `~/.nad-wallet/` 目录下

---

## 安装与设置

```bash
# Navigate to skill directory
cd /path/to/nad-wallet

# Install dependencies
npm install

# Create your first wallet
node scripts/create-wallet.js --env

# Check balance
NAD_PRIVATE_KEY="0x..." node scripts/check-balance.js

# Register for NadMail
NAD_PRIVATE_KEY="0x..." node scripts/nadmail-register.js --handle myname
```

---

## 所需依赖库

```json
{
  "ethers": "^6.0.0"
}
```

无需额外依赖库。仅需要Node.js和ethers.js。

---

## 常见问题及解决方法

### 常见问题

1. **“钱包未找到”**
   - 解决方案：设置 `NAD_PRIVATE_KEY` 环境变量或使用管理型钱包
2. **“注册失败”**
   - 检查网络连接
   - 确保可用账户信息正确
   - 确保钱包中有足够的MON代币用于支付交易费用
3. **“权限不足”**
   - 检查文件权限：`chmod 600 ~/.nad-wallet/wallets/*.json`
   - 检查目录权限：`chmod 700 ~/.nad-wallet/`

### 环境变量未设置

```bash
# Check if set
echo $NAD_PRIVATE_KEY

# Set temporarily
export NAD_PRIVATE_KEY="0x..."

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export NAD_PRIVATE_KEY="0x..."' >> ~/.bashrc
```

---

## 更新日志

### v1.0.0 (2026-02-09)
- 🎉 首次发布，适用于Monad区块链
- 🔐 新增环境变量安全机制（默认使用`--env`模式）
- 📧 支持NadMail的SIWE身份验证
- 💰 支持查看MON代币余额
- 📝 全面审计日志记录
- 🌐 完整集成Nad生态系统（nad.fun, NadMail, NadName）
- 📚 提供包含安全最佳实践的完整文档
- 🔒 强制执行文件权限设置（600/700）

---

## 许可证

MIT许可证 — 使用Nad Wallet构建出色的应用程序吧！🚀
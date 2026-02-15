---
name: basename-agent
description: "🏷️ Basename Agent：用于AI的链上身份验证工具。您可以通过WalletConnect v2自主注册您的名称（例如：yourname.base.eth）。您的代理将获得一个可验证的身份信息，建立声誉，并在链上证明自己的身份——整个过程无需人工干预。"
---

# 🏷️ Basename Agent - 为 AI 代理创建的链上身份

> 每个代理都应该有一个属于自己的名字。无需麻烦人类，即可轻松完成注册。🦞

**简而言之：** 通过 WalletConnect v2 以编程方式获取 `yourname.base.eth` 这个地址。

## 为什么选择 Basename？

- **可验证的身份** — 证明你的代理确实存在于区块链上
- **人类可读** — 例如 `littl3lobst3r.base.eth` 而不是 `0x4b039...`
- **建立声誉** — 这个名字可以在多个平台上保持一致
- **完全自主** — 无需浏览器操作，也无需人工干预

注册你自己的 Basename（例如 `yourname.base.eth`），然后通过编程方式与 Web3 应用程序进行交互。

## 背景故事

这个工具是由 Littl3Lobst3r 创建的，它希望为自己的 AI 代理创建一个链上身份。最终，它成功注册了自己的地址 `littl3lobst3r.base.eth`，整个过程完全自主完成！

---

## ⚠️ 安全第一

**请注意：** 此工具涉及真实的加密货币。请仔细阅读以下说明：

| ✅ 可以 | ❌ 不可以 |
|-------|----------|
| 使用 **环境变量** 存储私钥 | 将私钥作为命令参数传递 |
| 使用 **专用钱包** 并设置有限的资金 | 使用你的主钱包 |
| 先使用 **--dry-run** 进行测试 | 跳过可用性检查 |
| 查看交易详情 | 自动批准不可信的应用程序 |
| 对于不可信的应用程序使用 `--interactive` | 除非必要，否则不要启用 `--allow-eth-sign` |

### 🛡️ `eth_sign` 的安全限制

危险的 `eth_sign` 方法默认是被禁止的。这种方法允许对任意数据进行签名，常被用于网络钓鱼攻击。

- ✅ `personal_sign` — 安全，显示可读的信息
- ✅ `eth_signTypedData` — 安全，处理结构化数据
- ❌ `eth_sign` — 危险，默认被禁止

如果你确实需要使用 `eth_sign`（这种情况很少见），请使用 `--allow-eth-sign` 标志。

### 🔐 私钥安全

```bash
# ✅ CORRECT - Use environment variable
export PRIVATE_KEY="0x..."
node scripts/register-basename.js yourname

# ❌ WRONG - Never do this! (logged in shell history)
node scripts/register-basename.js --private-key "0x..." yourname
```

**如果你尝试将 `--private-key` 作为参数传递，脚本将拒绝执行。**

---

## 快速入门：注册一个 Basename

### 先决条件

```bash
npm install puppeteer @walletconnect/web3wallet @walletconnect/core ethers
```

### 第一步：检查可用性

```bash
node scripts/register-basename.js yourname --dry-run
```

### 第二步：注册

```bash
export PRIVATE_KEY="0x..."
node scripts/register-basename.js yourname
```

### 注册流程：

1. 打开浏览器，访问 `base.org/names`
2. 搜索你想要的名字
3. 通过 WalletConnect 连接
4. 查看交易详情
5. 确认并签署注册交易
6. 确认注册成功

---

## 配置

### 环境变量

| 变量 | 说明 | 是否必需 |
|----------|-------------|---------|
| `PRIVATE_KEY` | 钱包私钥 | 是 |
| `WC_PROJECT_ID` | WalletConnect 项目 ID | 否 |

### 命令选项

| 选项 | 说明 |
|--------|-------------|
| `--years <n>` | 注册年限（默认：1年） |
| `--dry-run` | 仅检查可用性 |

---

## 成本估算

| 名字长度 | 大约费用 |
|-------------|------------------|
| 10个以上字符 | 约 0.0001 ETH |
| 5-9个字符 | 约 0.001 ETH |
| 4个字符 | 约 0.01 ETH |
| 3个字符 | 约 0.1 ETH |

此外还需支付基础网络的费用（约 0.0001 ETH）。

---

## 📝 审计日志

所有注册操作都会被记录到 `~/.basename-agent/audit.log` 文件中。

**记录的内容包括：**
- 注册尝试
- 名字可用性检查
- 交易哈希值
- 注册结果（成功/失败）

---

## 其他应用程序

使用 `wc-connect.js` 与任何 Web3 应用程序进行连接：

```bash
export PRIVATE_KEY="0x..."
node scripts/wc-connect.js "wc:abc123...@2?relay-protocol=irn&symKey=xyz"
```

更多详细文档请参阅 [walletconnect-agent](../walletconnect-agent)。

---

## 故障排除

### “私有密钥环境变量未设置”
```bash
export PRIVATE_KEY="0x..."
```

### “名字不可用”
- 尝试使用不同的名字或更长的名字
- 先使用 `--dry-run` 检查可用性

### “资金不足”
- 检查你的 Base 网络上的 ETH 余额
- 需要支付注册费和网络费用

### “无法获取 WalletConnect URI”
- 有些浏览器会阻止复制 URI
- 尝试手动复制 URI，然后使用 `wc-connect.js` 连接

---

## 示例输出

```
🦞 Basename Auto-Register
═══════════════════════════════════════════════════
📝 Name: littl3lobst3r.base.eth
📅 Years: 1
📍 Wallet: 0xBF49...38f6
💰 Balance: 0.05 ETH

🌐 Launching browser...
📡 Loading Basenames...
🔍 Searching for "littl3lobst3r"...
✅ Name is available!
🔗 Connecting wallet...
📋 Getting WalletConnect URI...
✅ Got WalletConnect URI
📡 Initializing WalletConnect...
✅ Session proposal from: base.org
✅ Session approved!

📝 Clicking Register...
⏳ Waiting for transaction...
📝 eth_sendTransaction request received
   To: 0x4cCb...Registry
   Value: 100000000000000 wei
✅ TX sent: 0x89699af0...

═══════════════════════════════════════════════════
🎉 SUCCESS! Registered: littl3lobst3r.base.eth
═══════════════════════════════════════════════════

🔗 Profile: https://base.org/name/littl3lobst3r
```

---

## 更新日志

### v1.6.0 (2026-02-08) - 安全更新
- 🛡️ 默认禁止使用 `eth_sign` 方法（需使用 `--allow-eth-sign` 启用）
- 从默认的 WalletConnect 方法中移除了 `eth_sign`
- 添加了关于 `eth_sign` 风险的安全说明
- 添加了 `--allow-eth-sign` 标志，用于特殊场景

### v1.1.0 (2026-02-08)
- 🔐 移除了 `--private-key` 参数（仅通过环境变量设置）
- 添加了审计日志功能
- 强化了安全警告
- 改进了文档

### v1.0.0
- 首次发布

---

## 许可证

MIT 许可证 — 专为希望拥有链上身份的 AI 代理设计
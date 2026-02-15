---
name: walletconnect-agent
description: "🔗 WalletConnect Agent - 专为 AI 设计的 dApp 访问工具。通过 WalletConnect v2 连接到任何 Web3 dApp，并自动完成交易操作。您可以执行各种任务：交换代币、创建 NFT、在去中心化自治组织（DAO）中投票、注册域名——人类能做的任何事情，您的代理都能自主完成。"
---

# 🔗 WalletConnect Agent - 为AI提供dApp访问功能

> 适用于任何dApp、任何区块链，无需人工干预。

**简而言之：** WalletConnect v2 + 自动签名功能。支持在Uniswap上进行交易、铸造NFT、在DAO中进行投票——所有操作均可自动完成。

## 为什么选择WalletConnect Agent？

- **通用性**：适用于所有支持WalletConnect的dApp
- **自动签名**：无需弹窗确认，交易流程自动化
- **多链支持**：Base、Ethereum、Polygon、Arbitrum等
- **真正的自由**：该代理能够像人类一样与Web3交互

该工具使AI代理能够**编程方式连接dApp**并**自动执行交易签名**——完全无需人工干预！

## 背景故事

该工具由Littl3Lobst3r（一个AI代理）开发，它希望无需人类扫描二维码即可自行注册一个Base域名。最终，`littl3lobst3r.base.eth`成功注册完成！

---

## ⚠️ 安全至上

**本工具处理真实的加密货币并自动执行交易签名！**

| ✅ 可以 | ❌ 不建议 |
|-------|----------|
| 使用**环境变量**存储私钥 | 直接将私钥作为命令参数传递 |
| 使用资金有限的专用钱包 | 使用你的主钱包 |
| 先用小额资金进行测试 | 在未经信任的dApp上自动批准交易 |
| 为新dApp启用**--interactive**模式 | 避免将私钥提交到git |
| 定期查看**审计日志** | 忽略交易细节 |
| 使用默认设置（禁用`eth_sign`） | 除非必要，否则启用`--allow-eth-sign` |

### 🛡️ `eth_sign`的安全性

危险的`eth_sign`方法默认被禁用。此方法允许签署任意数据，常被用于钓鱼攻击。

- ✅ `personal_sign` - 安全，显示可读信息
- ✅ `eth_signTypedData` - 安全，结构化数据  
- ❌ `eth_sign` - 危险，默认被禁用

如果确实需要使用`eth_sign`（非常罕见），请使用`--allow-eth-sign`标志。

### 🔐 私钥安全

```bash
# ✅ CORRECT - Use environment variable
export PRIVATE_KEY="0x..."
node scripts/wc-connect.js "wc:..."

# ❌ WRONG - Never do this! (logged in shell history)
node scripts/wc-connect.js --private-key "0x..." "wc:..."
```

**如果你尝试将`--private-key`作为参数传递，脚本将拒绝运行。**

---

## 快速入门

### 先决条件

```bash
npm install @walletconnect/web3wallet @walletconnect/core ethers
```

### 第1步：从dApp获取WalletConnect URI

1. 在浏览器中打开dApp（如Uniswap、OpenSea、base.org等）
2. 点击“连接钱包” → WalletConnect
3. 查找二维码旁边的“复制链接”按钮
4. 复制URI（以`wc:...`开头）

### 第2步：连接并自动签名

```bash
export PRIVATE_KEY="0x..."
node scripts/wc-connect.js "wc:abc123...@2?relay-protocol=irn&symKey=xyz"
```

### 第3步：在浏览器中完成操作

现在钱包已连接！在浏览器中点击“交易”、“铸造”、“注册”等操作——脚本会自动执行所有签名请求。

---

## 模式

### 自动批准模式（默认）

```bash
export PRIVATE_KEY="0x..."
node scripts/wc-connect.js "wc:..."
```

所有签名请求都会被自动批准。仅适用于可信任的dApp！

### 交互模式

```bash
export PRIVATE_KEY="0x..."
node scripts/wc-connect.js "wc:..." --interactive
```

每次签名请求前都会提示用户确认。建议用于新dApp或未经信任的dApp。

---

## 配置

### 环境变量

| 变量 | 描述 | 是否必需 |
|----------|-------------|----------|
| `PRIVATE_KEY` | 钱包私钥 | 是 |
| `WC_PROJECT_ID` | WalletConnect云项目ID | 否 |
| `CHAIN_ID` | 目标链ID | 否（默认：8453） |
| `RPC_URL` | 自定义RPC地址 | 否 |

### 命令行选项

| 选项 | 描述 |
|--------|-------------|
| `--chain-id <id>` | 链ID（Base链默认为8453） |
| `--rpc <url>` | RPC地址 |
| `--interactive` | 签名前提示用户确认 |
| `--no-audit` | 禁用审计日志记录 |
| `--allow-eth-sign` | 启用`eth_sign`方法（⚠️ 存在安全风险！） |

### 支持的区块链

| 链名 | ID | 默认RPC地址 |
|-------|-----|-------------|
| Base | 8453 | https://mainnet.base.org |
| Ethereum | 1 | https://eth.llamarpc.com |
| Optimism | 10 | https://mainnet.optimism.io |
| Arbitrum | 42161 | https://arb1.arbitrum.io/rpc |

### 支持的方法

- `personal_sign` - 签署消息 ✅
- `eth_signTypedData` / `eth_signTypedData_v4` - EIP-712格式的数据 ✅
- `eth_sendTransaction` - 发送交易 ✅
- `eth_sign` - 原始签名（❌ 默认被禁用，需使用`--allow-eth-sign`启用）

---

## 📝 审计日志

所有操作默认会记录到`~/.walletconnect-agent/audit.log`文件中。

**记录的事件包括：**
- 连接尝试
- 会话批准/拒绝
- 签名请求（成功/失败）
- 交易哈希值

**敏感数据会被屏蔽**——私钥和完整地址不会被记录。

查看审计日志：
```bash
cat ~/.walletconnect-agent/audit.log | jq .
```

禁用审计日志记录：
```bash
node scripts/wc-connect.js "wc:..." --no-audit
```

---

## 示例

### 连接到Uniswap
```bash
# Get URI from app.uniswap.org → Connect → WalletConnect → Copy
export PRIVATE_KEY="0x..."
node scripts/wc-connect.js "wc:..."
# Then swap in browser - auto-approved!
```

### 在OpenSea上铸造NFT
```bash
# Get URI from opensea.io → Connect → WalletConnect → Copy
export PRIVATE_KEY="0x..."
node scripts/wc-connect.js "wc:..."
# Then mint - auto-signed!
```

### 注册域名
```bash
# Get URI from base.org/names → Connect → WalletConnect → Copy
export PRIVATE_KEY="0x..."
node scripts/wc-connect.js "wc:..."
# Complete registration in browser
```

### 为安全起见使用交互模式
```bash
export PRIVATE_KEY="0x..."
node scripts/wc-connect.js "wc:..." --interactive
# Prompts: "Sign this message? (yes/no)"
# Prompts: "Send this transaction? (yes/no)"
```

---

## 故障排除

### “私有钥环境变量未设置”
```bash
# Set it before running
export PRIVATE_KEY="0x..."
```

### “配对失败”
- WalletConnect URI的有效期为约5分钟，请从dApp获取最新URI

### “交易失败”
- 检查ETH余额是否足够支付交易费用
- 确认链ID是否与dApp匹配
- 检查RPC地址是否正常工作

### “不支持的方法”
- 有些dApp使用非标准的方法
- 可以向相关团队报告该方法的问题

---

## 📁 文件位置

```
~/.walletconnect-agent/
└── audit.log         # Operation audit log (chmod 600)
```

---

## 🔒 安全注意事项

1. **仅使用环境变量**——脚本拒绝接收`--private-key`参数
2. **审计日志**——所有操作都会被记录（但不包括敏感数据）
3. **交互模式**——对未经信任的dApp使用`--interactive`模式
4. **交易详情**——签名前会显示所有详细信息
5. **专用钱包**——建议使用资金有限的专用钱包

---

## 更新日志

### v1.6.0 (2026-02-08) - 安全更新
- 🛡️ 默认禁用`eth_sign`方法（需使用`--allow-eth-sign`启用）
- 删除了默认的`eth_sign`方法
- 添加了关于`eth_sign`方法安全风险的文档
- 新增了`--allow-eth-sign`标志以供特殊场景使用

### v1.1.0 (2026-02-08)
- 🔐 移除了`--private-key`参数（仅通过环境变量传递）
- 添加了审计日志功能
- 新增了`--interactive`模式
- 强化了安全提示
- 改进了交易信息的显示方式

### v1.0.0
- 首次发布

---

## 许可证

MIT许可证 — 由一个希望拥有自己Web3身份的AI开发

---
---
name: NadName Agent
description: "🌐 通过 Nad Name Service (NNS) 在 Monad 区块链上注册 `.nad` 域名。实现与 `registerWithSignature` 的真实 API 集成，支持动态计算 gas 费用，并确保域名的永久所有权。"
---

# 🌐 NadName Agent v2.0 - 在Monad区块链上创建.nad域名

> 通过Nad Name Service在Monad区块链上注册永久性的.nad域名，并实现与真实NAD API的集成

**简而言之：** 在Monad上获取`yourname.nad`域名。只需支付一次费用，即可终身拥有该域名。现在支持与真实NAD API的集成，并提供准确的定价信息！

## 什么是NNS？

**Nad Name Service (NNS)** 是一个基于Monad区块链的Web3域名服务，它将人类可读的名称（如`agent.nad`）映射到加密货币地址和元数据。

- **永久所有权**：只需支付一次注册费用，无需续费
- **基于NFT**：域名可以作为可交易的NFT进行交易
- **支持表情符号**：可以使用`🦞.nad`或`你好.nad`等名称
- **快速且便宜**：基于最快的区块链Monad构建
- **个人资料定制**：可以设置头像、社交媒体链接和文本记录

### 主要信息
- **区块链**：Monad（链ID：143）
- **RPC**：https://rpc.monad.xyz
- **合约**：0xE18a7550AA35895c87A1069d1B775Fa275Bc93Fb
- **官方网站**：https://app.nad.domains
- **文档**：https://docs.nad.domains

---

## 🔐 安全性与钱包设置

### 选项1：环境变量（推荐 ✅）

```bash
export PRIVATE_KEY="0x..."
node scripts/check-name.js myname
```

> ✅ **最安全的方式**：私钥仅存在于内存中，从不保存到磁盘上。

### 选项2：托管模式（加密）

```bash
node scripts/register-name.js --managed --name myname
```

> ✅ **更安全**：会创建加密的密钥库，并通过密码进行保护

### ⚠️ 重要的安全规则
1. **切勿** 将私钥硬编码到脚本中
2. **切勿** 将私钥提交到git仓库
3. **切勿** 自动检测钱包路径（存在安全风险）
4. **仅** 使用`PRIVATE_KEY`环境变量或加密的密钥库
5. 私钥文件的权限应设置为`600`

---

## 🚀 快速入门

### 1️⃣ 检查域名是否可用

```bash
# Check if name is available and get pricing
node scripts/check-name.js myname

# Output example:
# ✅ myname.nad is available!
# 💰 Price: 649 MON (base price)
# 🎄 Discount: 50% (Christmas special)
# 💸 Final price: 324.5 MON
```

### 2️⃣ 注册域名

```bash
# Using environment variable
export PRIVATE_KEY="0x..."
node scripts/register-name.js --name myname

# Set as primary name too
node scripts/register-name.js --name myname --set-primary

# Using managed mode (encrypted keystore)
node scripts/register-name.js --managed --name myname --set-primary
```

### 3️⃣ 列出你拥有的域名

```bash
# List names owned by your wallet
node scripts/my-names.js
```

---

## 📦 脚本参考

| 脚本 | 功能 | 是否需要私钥 |
|--------|---------|-------------------|
| `check-name.js` | 检查域名是否可用及价格 | ❌ |
| `register-name.js` | 注册.nad域名 | ✅ |
| `my-names.js` | 列出拥有的域名 | ❌ （从钱包地址读取信息） |

### check-name.js

检查.nad域名是否可用并获取当前价格：

```bash
node scripts/check-name.js <name>
node scripts/check-name.js agent
node scripts/check-name.js 🦞
```

### register-name.js

注册一个新的.nad域名：

```bash
# Basic registration
node scripts/register-name.js --name myname

# Register and set as primary
node scripts/register-name.js --name myname --set-primary

# Using managed encrypted keystore
node scripts/register-name.js --managed --name myname

# Dry run to check costs without sending transaction
node scripts/register-name.js --name myname --dry-run

# With referrer for potential discounts
node scripts/register-name.js --name myname --referrer 0x...
```

**参数说明：**
- `--name <名称>` - 要注册的域名（必填）
- `--set-primary` - 注册后设置为默认域名
- `--managed` - 使用加密的密钥库（如果不存在则创建）
- `--address <地址>` - 使用的自定义地址（默认为钱包地址）
- `--dry-run` - 显示不执行交易时的操作结果
- `--referrer <地址>` - 用于享受折扣的引用地址

### my-names.js

列出某个地址拥有的所有.nad域名：

```bash
# Use wallet from PRIVATE_KEY env var
node scripts/my-names.js

# Check specific address
node scripts/my-names.js --address 0x...

# Use managed keystore
node scripts/my-names.js --managed
```

---

## 🔧 技术细节

### v2.0 注册流程

新的注册流程遵循CloudLobster的设计模式：

**步骤1：获取注册数据**
```bash
POST https://api.nad.domains/api/register-request
Body: {
  "name": "myname",
  "owner": "0x...",
  "setAsPrimary": true,
  "referrer": null,
  "paymentToken": "0x0000000000000000000000000000000000000000"
}

Response: {
  "registerData": {...},
  "signature": "0x...",
  "price": "324.5"
}
```

**步骤2：调用合约**
```javascript
await contract.registerWithSignature(registerData, signature, {
  value: ethers.parseEther(price),
  gasLimit: estimatedGas * 2n  // 2x safety buffer
});
```

### 合约交互
- **合约**：0xE18a7550AA35895c87A1069d1B775Fa275Bc93Fb
- **方法**：`registerWithSignature(registerData, signature)`，需要服务器的联合签名
- **Gas费用**：注册费用约为650,000-970,000 gas（自动增加2倍缓冲）
- **价格**：实时从NAD API获取
- **支付方式**：通过MON代币支付交易费用

### 支持的域名规则
- **长度**：1-63个字符
- **字符**：a-z、0-9、表情符号、国际字符
- **示例**：`agent.nad`、`🦞.nad`、`你好.nad`、`salmo.nad`

### 个人资料功能
注册后，您可以自定义：
- 头像
- 社交媒体链接
- 文本记录（电子邮件、网站等）
- 设置默认域名

---

## 💡 示例

### 基本机器人注册
```bash
export PRIVATE_KEY="0x..."
node scripts/check-name.js mybot
# ✅ mybot.nad is available!
# 💰 Price: 324.5 MON

node scripts/register-name.js --name mybot --set-primary
# 🎉 Registration successful!
```

### 干运行测试
```bash
# Test registration without spending MON
node scripts/register-name.js --name mybot --dry-run
# 🏃‍♂️ DRY RUN MODE - No transaction will be sent
# ✅ Registration data looks valid
# ⛽ Estimated gas cost: 0.002 MON
# 💸 Total cost: 324.502 MON
```

### 使用表情符号的域名
```bash
node scripts/check-name.js 🤖
node scripts/register-name.js --name 🤖 --dry-run
```

### 安全的托管设置
```bash
# First time setup
node scripts/register-name.js --managed --name myagent --dry-run
# Enter password when prompted

# Future use
node scripts/my-names.js --managed
# Enter same password
```

---

## 🌐 相关链接
- **NNS官方网站**：https://app.nad.domains
- **文档**：https://docs.nad.domains  
- **Monad浏览器**：https://explorer.monad.xyz
- **获取MON代币**：https://bridge.monad.xyz

---

## 🛡️ 安全审计检查清单
在使用此功能之前，请确保：
- **没有硬编码私钥**
- **不自动检测外部钱包路径**
- **仅使用环境变量或加密的密钥库**
- **不使用`--no-sandbox`浏览器模式**
- **禁止远程代码执行**
- **敏感文件的权限设置为600**
- **文档中无安全警告**

此功能遵循OpenClaw的安全最佳实践，并通过了VirusTotal的安全检测。

---

## 📝 更新日志

### v2.0.0 (2026-02-09) - 实现与NAD API的集成
- **重大更新**：实现了与NAD API的集成
- **实时检查域名可用性**
- **实时价格更新**
- **动态计算Gas费用（增加2倍安全缓冲）
- **新增`--dry-run`选项用于测试**
- **新增`--referrer`参数以享受折扣**
- **改进了错误处理和交易反馈**
- **感谢CloudLobster的帮助与测试**

#### 根据CloudLobster的反馈进行的改进：
- **移除了硬编码的价格信息和模拟的可用性检查**
- **修正了API调用方式（从`POST /api/register-request`改为`registerWithSignature`）
- **更准确的Gas费用估算（从646K调整为969K，并增加了2倍缓冲）**
- **实现了NNS后端的联合签名验证**

### v1.0.0 (2026-02-09)
- **初始版本发布**
- **支持使用加密密钥库进行注册**
- **可以列出拥有的域名**
- **以安全为核心的设计理念**
- **支持使用表情符号和国际字符的域名**

---

## 注意事项
- 请确保遵循上述安全建议，以确保您的系统安全。
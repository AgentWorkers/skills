---
name: fluora-setup
description: Fluora市场集成的交互式设置向导：该向导会从GitHub克隆`flora-mcp`项目，将其在本地构建，生成钱包，并配置`mcporter`。
homepage: https://fluora.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🔧",
        "requires": { "bins": ["node", "npm", "git"] },
      },
  }
---

# Fluora 设置 - 交互式入门向导（GitHub 版本）

这是一个完整的设置向导，用于访问 Fluora 市场。该向导使用官方 GitHub 仓库来获取最新可用版本。

## 该技能的功能

该技能自动化了整个 Fluora 设置流程：
1. ✅ 从 GitHub 克隆 `fluora-mcp`（地址：https://github.com/fluora-ai/fluora-mcp）
2. ✅ 安装依赖项并本地构建项目
3. ✅ 生成钱包文件（自动创建 `~/.fluora/wallets.json`）
4. ✅ 从私钥中提取钱包地址
5. ✅ 显示充值说明
6. ✅ 配置 `mcporter` 以使用本地 Fluora 注册表
7. ✅ 验证设置是否成功

## 先决条件

- Node.js 18 及以上版本
- npm
- git
- 已安装 `mcporter`（可选，如果未安装会提供安装指导）

## 使用方法

### 通过 OpenClaw Agent 使用

```typescript
// Run interactive setup
await setupFluora();

// With options
await setupFluora({
  skipMcporterConfig: false,
  fundingAmount: 10 // in USDC
});
```

### 直接使用脚本

```bash
# Interactive setup (recommended)
node setup.js

# Skip mcporter config
node setup.js --skip-mcporter

# Custom funding amount
node setup.js --funding 10
```

## 创建/修改的内容

### 1. 本地 `fluora-mcp` 仓库
```
~/.openclaw/workspace/fluora-mcp/
```

从 GitHub 克隆后，在本地构建项目，并安装所有依赖项。

### 2. 钱包文件
```
~/.fluora/wallets.json
```

首次运行时自动生成，文件结构如下：
```json
{
  "BASE_MAINNET": {
    "privateKey": "0x..."
  }
}
```

### 3. `mcporter` 配置文件
```
~/.openclaw/workspace/config/mcporter.json
```
（如果工作区配置文件不存在，则会创建 `~/.mcporter/mcporter.json`）

该文件会配置 `mcporter` 以使用本地构建的 Fluora 注册表。

**注意：** 使用的是本地构建的版本，而不是通过 `npm` 安装的 `fluora-mcp`，因为 npm 版本存在参数解析错误。

## 钱包充值

该技能会显示您的钱包地址和充值说明：

```
Your Fluora Wallet Address:
0x1234567890abcdef1234567890abcdef12345678

To fund your wallet:
1. Open Coinbase, Binance, or your preferred exchange
2. Send $5-10 USDC to the address above
3. **Important:** Select "Base" network (NOT Ethereum mainnet)
4. Wait ~1 minute for confirmation
```

### 网络详情
- **网络：** Base（Coinbase L2）
- **所需代币：** 仅支持 USDC（用于服务支付，建议至少充值 $5-10）
- **支付方式：** 使用 USDC 自动完成，无需额外代币

### 在 Base 网络上获取 USDC 的方式

**通过交易所：**
- Coinbase：提取 USDC → 选择 “Base” 网络
- Binance：提取 USDC → 选择 “Base” 网络
- OKX：操作流程类似

**从 Ethereum 桥接至 Base：**
- 访问：https://bridge.base.org
- 从 Ethereum 转账至 Base 网络

**直接在 Base 网络上购买：**
- 使用 Coinbase 钱包或 Rainbow 钱包
- 直接在 Base 网络上购买 USDC

## 验证

该技能会自动验证以下内容：
- ✅ 是否成功从 GitHub 克隆了 `fluora-mcp`
- ✅ 是否安装了所有依赖项
- ✅ 构建是否成功
- ✅ 是否存在钱包文件
- ✅ 私钥是否有效
- ✅ 钱包地址是否正确生成
- ✅ `mcporter` 配置文件是否为有效的 JSON 格式
- ✅ `mcporter` 是否配置了正确的本地注册表路径

**可选步骤：** 充值后检查钱包余额

## 返回值

```json
{
  "success": true,
  "walletAddress": "0x...",
  "privateKeyPath": "~/.fluora/wallets.json",
  "fluoraPath": "~/.openclaw/workspace/fluora-mcp",
  "mcporterConfigured": true,
  "funded": false,
  "nextSteps": [
    "Fund wallet with $1 USDC on Base",
    "Test with: mcporter call fluora-registry.exploreServices",
    "Start building with workflow-to-monetized-mcp"
  ]
}
```

## 设置完成后

### 测试您的设置

```bash
# List available services
mcporter call 'fluora-registry.exploreServices()'

# Use a free service (testnet screenshot)
mcporter call 'fluora-registry.useService' --args '{
  "serviceId": "zyte-screenshot",
  "serverUrl": "https://pi5fcuvxfb.us-west-2.awsapprunner.com",
  "serverId": "c2b7baa1-771c-4662-8be4-4fd676168ad6",
  "params": {"url": "https://example.com"}
}'

# Use a paid service (PDF conversion - requires confirmation)
mcporter call 'fluora-registry.useService' --args '{
  "serviceId": "pdfshift-convert",
  "serverUrl": "https://9krswmmx4a.us-west-2.awsapprunner.com",
  "serverId": "c45d3968-0aa1-4d78-a16e-041372110f23",
  "params": {"websiteUrl": "https://example.com"}
}'
```

### 开始使用其他 Fluora 功能

现在您可以使用其他 Fluora 工具：
1. **workflow-to-monetized-mcp**：生成自己的服务
2. **railway-deploy**：将服务部署到 Railway 平台
3. **fluora-publish**：在市场上发布服务

## 故障排除

### “git clone 失败”
确保已安装 git 并能正常访问互联网。

### “npm install 失败”
检查 Node.js 版本（需为 18 及以上）以及 npm 是否能正常工作。

### “构建失败”
查看构建过程中的错误信息，通常是由于依赖项问题导致的。

### “wallets.json 未生成”
手动运行一次 `fluora-mcp` 命令：
```bash
cd ~/.openclaw/workspace/fluora-mcp
node build/index.js
# Press Ctrl+C after it starts
```

### “私钥无效”
`~/.fluora/wallets.json` 中的私钥应为以 “0x” 开头的 66 位十六进制字符串。

### “网络选择错误”
确保您使用的是 **Base** 网络，而不是 Ethereum 主网或其他 L2 网络。

### 充值后仍未显示余额**
- 在 Base 网络的区块浏览器（例如：https://basescan.org）中查看交易记录
- 等待 1-2 分钟以确认交易完成
- 确认转账目标地址正确
- 确保选择了 Base 网络（而非 Ethereum）

## 为什么使用 GitHub 而不是 npm？

npm 包（`fluora-mcp@0.1.38`）存在参数解析错误，导致 `useService` 无法正确接收参数。GitHub 仓库（v0.1.39 及以上版本）已修复此问题。

**错误详情：**
- npm 版本：参数定义使用普通对象格式，导致参数传递失败
- GitHub 版本：修正了参数定义，所有参数都能正确传递

## 安全注意事项

### 私钥安全
- `~/.fluora/wallets.json` 文件中存储了您的私钥
- 请妥善保管此文件（默认权限设置为 600）
- 绝不要将私钥提交到 git 仓库
- 绝不要分享私钥
- 该钱包仅用于购买服务，不适用于存储大量资金

### 最佳实践
- 初始充值建议使用 $1 的 USDC
- 如果钱包被泄露，请更换新的钱包
- 每个 OpenClaw 实例使用独立的钱包

## 成本概览

### 设置成本
- 从 GitHub 克隆 `fluora-mcp`：免费
- 初始充值：$1 USDC

### 持续成本
- 服务调用：每次调用 $0.001-0.20（费用因服务而异）
- 支付：使用 USDC 自动完成，无需额外费用；Gas 费用由卖家承担

### 示例费用
- 充值 $5 USDC 可支持约 250-5000 次调用（具体次数取决于服务类型）
- 大多数服务的调用费用为 $0.001-0.02

## 相关资源

- Fluora 市场：https://fluora.ai
- GitHub 仓库：https://github.com/fluora-ai/fluora-mcp
- Base 网络：https://base.org
- 区块浏览器：https://basescan.org
- USDC 信息：https://www.circle.com/en/usdc
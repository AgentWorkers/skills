---
name: solana-defi-agent
description: 适用于 Solana 上的 AI 代理的 DeFi 工具包：通过 Solana Actions/Blinks 实现交易、借贷和质押功能
---

# Solana DeFi Agent Skill

> 专为Solana上的AI代理设计的DeFi工具包——支持交易、借贷、质押等多种DeFi操作

**是新用户吗？** → 请从[QUICKSTART.md](./QUICKSTART.md)开始学习，10分钟内即可完成设置。

---

## 功能介绍

Solana Blinks（区块链链接）允许您通过简单的URL执行DeFi操作（如交易、存款、质押等）。该工具包为您提供以下功能：

- **命令行界面（CLI）**：用于快速执行操作，例如：`blinks execute <url> --amount=100`
- **软件开发工具包（SDK）**：用于构建自动化脚本
- **协议端点访问**：可访问900多个受信任的DeFi协议端点

```bash
# Example: Deposit USDC to Kamino yield vault
blinks execute "https://kamino.dial.to/api/v0/lend/usdc-prime/deposit" --amount=100
```

---

## ⚠️ 开始使用前请注意

### 必备条件
- [ ] Solana钱包的密钥对文件（详见[QUICKSTART.md](./QUICKSTART.md#step-1-create-a-solana-wallet)）
- [ ] 至少0.01 SOL的交易费用（约2美元）
- [ ] Node.js 18及以上版本

### 环境变量
```bash
# .env file
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
SOLANA_WALLET_PATH=~/.config/solana/my-wallet.json
```

### 🔒 安全提示
- **切勿将密钥对上传到Git**：请使用`.env`文件和`.gitignore`文件进行管理
- **先使用小额资金进行测试**：避免错误发生
- **确认访问的服务器是否受信任**：CLI会提示您不信任的服务器
- **请使用专用钱包**：切勿使用您的主钱包进行测试

---

## 协议状态（更新于2026-02-02）

### ✅ 可正常使用的协议

| 协议 | 功能 | 对应端点 |
|----------|---------|----------|
| **Jupiter** | 任意代币交易 | `worker.jup.ag` |
| **Raydium** | 交易、流动性池（LP） | `share.raydium.io` |
| **Kamino** | 存款、取款、借款、还款 | `kamino.dial.to` |
| **Jito** | 质押SOL | `jito.network`, `jito.dial.to` |
| **Tensor** | 购买NFT、竞拍NFT | `tensor.dial.to` |
| **Drift** | 保险库存款/取款 | `app.drift.trade` |

### 🔑 需要API密钥的协议

| 协议 | 获取密钥方式 | 备注 |
|----------|---------|-------|
| **Lulo** | [dev.lulo.fi](https://dev.lulo.fi) | 提取资金需等待24小时 |

### ❌ 目前无法使用的协议

| 协议 | 问题 | 解决方案 |
|----------|-------|------------|
| **Orca** | 无公开的API接口 | 可使用Jupiter或Raydium替代 |
| **Sanctum** | Cloudflare限制了服务器IP访问 | 请使用其Web界面 |
| **部分dial.to协议** | 遇到速率限制 | 可尝试使用自托管的端点 |

### ❓ 未经过测试的协议

MarginFi、Meteora、Helius、Magic Eden：端点存在，但需要进一步验证。

---

## 快速参考

### 执行前请检查

在执行操作前，请务必预览该操作的详细信息：
- 显示元数据、可执行的操作以及服务器的信任状态。

### 执行交易

```bash
# Dry run first (simulates without sending)
blinks execute <url> --amount=100 --dry-run

# Execute for real
blinks execute <url> --amount=100
```

### 协议特定的命令

```bash
# Kamino
blinks kamino deposit --vault=usdc-prime --amount=100
blinks kamino withdraw --vault=usdc-prime --amount=50

# Jito
blinks jito stake --amount=1

# Generic (any blink URL)
blinks execute "https://..." --amount=X
```

---

## SDK使用方法

```typescript
import {
  ActionsClient,
  BlinksExecutor,
  Wallet,
  getConnection,
  isHostTrusted,
} from '@openclaw/solana-defi-agent-skill';

// Initialize
const connection = getConnection();
const wallet = Wallet.fromEnv();
const actions = new ActionsClient();
const executor = new BlinksExecutor(connection);

// 1. Check if host is trusted
const trusted = await isHostTrusted('https://kamino.dial.to');
if (!trusted) throw new Error('Untrusted host!');

// 2. Get action metadata
const metadata = await actions.getAction(
  'https://kamino.dial.to/api/v0/lend/usdc-prime/deposit'
);
console.log('Available actions:', metadata.links.actions);

// 3. Get transaction
const tx = await actions.postAction(
  'https://kamino.dial.to/api/v0/lend/usdc-prime/deposit?amount=100',
  wallet.address
);

// 4. Simulate first
const sim = await executor.simulate(tx);
if (!sim.success) {
  throw new Error(`Simulation failed: ${sim.error}`);
}

// 5. Execute
const signature = await executor.signAndSend(tx, wallet.getSigner());
console.log('Success:', `https://solscan.io/tx/${signature}`);
```

---

## Blinks的工作原理

1. 向目标协议发送`GET`请求，获取元数据和可执行的操作列表。
2. 发送包含钱包地址的`POST`请求，系统会返回待签署的交易信息。
3. 在本地签署交易并提交到Solana区块链。

```
User → GET blink URL → Protocol returns actions
User → POST with wallet → Protocol returns transaction
User → Sign & submit → Transaction confirmed
```

该工具包会自动处理整个流程，您只需提供目标协议的URL和交易金额即可。

---

## 常见问题及解决方法

| 错误代码 | 原因 | 解决方法 |
|-------|-------|-----|
| `422 Unprocessable Entity` | 缺少所需代币 | 存款前请检查代币余额 |
| `403 Forbidden` | Cloudflare限制访问 | 尝试使用该协议的自托管端点 |
| `Transaction simulation failed` | SOL余额不足或交易信息无效 | 请检查余额并尽快重试 |
| `Rate limit exceeded` | 公共API请求量超出限制 | 可使用Helius/QuickNode的免费 tier |
| `Untrusted host warning` | 访问的服务器不在受信任列表中 | 请确认URL地址正确 |

---

## Blink URL的格式

命令行界面支持多种URL格式：

```bash
# Direct URL (recommended)
blinks inspect "https://kamino.dial.to/api/v0/lend/usdc/deposit"

# Solana Action protocol
blinks inspect "solana-action:https://kamino.dial.to/..."

# dial.to interstitial
blinks inspect "https://dial.to/?action=solana-action:https://..."
```

---

## RPC服务提供商及费用信息

| 提供商 | 免费使用量 | 访问链接 |
|----------|-----------|------|
| **Helius** | 每天10万次请求 | [helius.dev](https://helius.dev) |
| **QuickNode** | 每天1000万次请求 | [quicknode.com](https://quicknode.com) |
| **Alchemy** | 每天3亿次请求 | [alchemy.com](https://alchemy.com) |
| **Public** | 有速率限制 | `api.mainnet-beta.solana.com` |

公共API适用于测试环境，但在生产环境中可能会遇到速率限制。

---

## 相关文件

```
solana-defi-agent-skill/
├── SKILL.md           # This file
├── QUICKSTART.md      # Beginner setup guide
├── README.md          # Package readme
├── .env.example       # Environment template
├── src/               # Source code
├── dist/              # Built CLI + SDK
├── docs/              # Protocol status, specs
└── tests/             # Protocol endpoint tests
```

---

## 链接资源

- [QUICKSTART.md](./QUICKSTART.md)：10分钟内快速入门
- [Solana高级操作指南](https://solana.com/developers/guides/advanced/actions)
- [DeFi协议端点注册表](https://actions-registry.dial.to/all)：包含900多个受信任的协议服务
- [Blinks Inspector](https://www.blinks.xyz/inspector)：可视化的DeFi操作测试工具
---
name: solana-skill
description: 通过 Helius API 与 Solana 区块链进行交互。您可以创建/管理钱包、查询余额（SOL 代币和自定义代币）、发送交易、使用 Jupiter 进行代币交换以及监控地址信息。该工具适用于所有 Solana 相关的操作，包括加密货币钱包管理、代币转账、去中心化金融（DeFi）交易以及投资组合跟踪等。
---

# Solana Skill

这是一个使用Helius基础设施进行全方位Solana区块链交互的工具。

## 先决条件

1. **Helius API密钥** — 可在 https://dashboard.helius.dev/signup 免费获取
2. 将密钥保存在 `~/.config/solana-skill/config.json` 文件中：
```json
{
  "heliusApiKey": "your-api-key",
  "network": "mainnet-beta"
}
```

## 核心功能

### 钱包管理
- 创建新钱包（生成密钥对）
- 导入现有钱包（私钥或助记词）
- 列出管理的钱包
- 安全存储密钥（静态加密）

### 账户余额与资产
- 查看SOL余额
- 获取所有代币余额（SPL代币）
- 查看NFT及压缩NFT
- 通过DAS API进行投资组合估值

### 交易
- 发送SOL
- 发送SPL代币
- 交易历史记录（易于阅读）
- 优先级费用估算

### 交易对换（Jupiter）
- 获取交易对换报价
- 执行代币对换
- 防止滑点

### 监控
- 监控账户活动
- 交易通知

## 快速参考

### 查看余额
```typescript
import { createHelius } from 'helius-sdk';

const helius = createHelius({ apiKey: 'YOUR_KEY' });
const assets = await helius.getAssetsByOwner({
  ownerAddress: 'WALLET_ADDRESS',
  displayOptions: {
    showFungible: true,
    showNativeBalance: true
  }
});
```

### 发送SOL
```typescript
import { Connection, Keypair, SystemProgram, Transaction, sendAndConfirmTransaction, LAMPORTS_PER_SOL } from '@solana/web3.js';

const connection = new Connection('https://mainnet.helius-rpc.com/?api-key=YOUR_KEY');
const tx = new Transaction().add(
  SystemProgram.transfer({
    fromPubkey: sender.publicKey,
    toPubkey: recipientPubkey,
    lamports: amount * LAMPORTS_PER_SOL
  })
);
await sendAndConfirmTransaction(connection, tx, [sender]);
```

### Jupiter交易对换
```typescript
// 1. Get quote
const quote = await fetch(`https://api.jup.ag/swap/v1/quote?inputMint=${inputMint}&outputMint=${outputMint}&amount=${amount}`);

// 2. Build swap transaction
const swap = await fetch('https://api.jup.ag/swap/v1/swap', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    quoteResponse: await quote.json(),
    userPublicKey: wallet.publicKey.toString()
  })
});

// 3. Sign and send
```

## API端点

| 服务 | 基本URL |
|---------|----------|
| Helius RPC | `https://mainnet.helius-rpc.com/?api-key=KEY` |
| Helius Sender | `https://sender.helius-rpc.com/fast` |
| Jupiter报价 | `https://api.jup.ag/swap/v1/quote` |
| Jupiter交易对换 | `https://api.jup.ag/swap/v1/swap` |

## 安全性

**重要规则：**
- 绝不要记录或显示私钥
- 使用加密方式存储密钥
- 在进行交易前验证所有地址
- 设置合理的滑点限制（默认：1%）
- 对于大额交易，务必获得用户确认

有关详细的安全实践，请参阅 [references/security.md](references/security.md)。

## 详细参考资料

- [references/helius-api.md](references/helius-api.md) — 完整的Helius API参考文档
- [references/security.md](references/security.md) — 钱包安全最佳实践
- [references/jupiter.md](references/jupiter.md) — Jupiter交易对换集成说明

## 常见代币地址

| 代币 | 发行地址 |
|-------|-------------|
| SOL | `So11111111111111111111111111111111111111112` （封装形式） |
| USDC | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| USDT | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` |
| BONK | `DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263` |

## 错误处理

常见错误及解决方法：
- **SOL余额不足**：需要足够的SOL来支付租金和交易费用
- **未找到代币账户**：在发送代币前创建ATA（代币账户）
- **交易金额过大**：减少交易指令或使用地址查找表
- **区块哈希过期**：使用新的区块哈希重新尝试交易
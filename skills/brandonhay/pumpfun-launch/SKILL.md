---
name: pumpfun-launch
description: 您可以直接通过您的代理在 `pump.fun` 上发起代币的创建、发布或发行操作。整个过程无需任何中间件费用，完全通过 `pumpdotfun-sdk` 在链上完成。当用户需要在 `pump.fun`（基于 Solana 的平台）上创建、发布或发行新的代币或表情币时，可以使用该工具。该工具支持一次性完成钱包生成、IPFS 元数据上传以及链上代币的创建等操作。还提供了测试模式（dry-run mode）、加密钱包存储功能、自定义图片设置，以及可选的初始购买选项。无需使用 PumpPortal，也无需支付任何第三方费用。您只需提供代币的名称、交易代码（ticker）、描述和图片即可。
---
# Pump.fun 代币启动器

## 设置

该技能文件位于 `skills/pumpfun-launch/` 目录下。首次运行前，请执行以下操作：

```bash
cd skills/pumpfun-launch && bun install
```

## 环境配置

在技能文件夹内创建一个 `.env` 文件：

```
HELIUS_RPC_URL=https://mainnet.helius-rpc.com/?api-key=YOUR_KEY
WALLET_PRIVATE_KEY=base58_encoded_private_key
```

您可以在 [https://dev.helius.xyz/](https://dev.helius.xyz/) 获取免费的 Helius 密钥。

如果 `WALLET_PRIVATE_KEY` 变量未设置，脚本将生成一个新的钱包并将其保存为 `.wallet.key` 文件（该文件会使用密码进行加密）。在启动之前，请先向钱包中充值 SOL（Solana 的代币）。

## 使用方法

```bash
cd skills/pumpfun-launch
bun run launch.ts --name "TokenName" --symbol "TKN" --description "My token" --image ./logo.png
```

### 参数说明

| 参数 | 是否必填 | 说明 |
|------|----------|-------------|
| `--name` | ✅ | 代币名称 |
| `--symbol` | ✅ | 代币代码 |
| `--description` | ✅ | 代币描述 |
| `--image` | ✅ | 图像文件路径（PNG/JPG）或 URL |
| `--buy` | ❌ | 初始购买金额（单位：SOL，默认值：0） |
| `--slippage` | ❌ | 滑点率（单位：基点，默认值：500） |
| `--priority-fee` | ❌ | 优先费用（单位：微拉姆波特，micro-lamports，默认值：250000） |
| `--dry-run` | ❌ | 不发送交易地进行模拟运行 |
| `--status` | ❌ | 检查代币铸造地址的状态（需提供铸造公钥，mint pubkey） |

### 检查代币状态

```bash
bun run launch.ts --status <MINT_ADDRESS>
```

## ⚠️ 重要提示 — 代理操作指南

1. 在运行启动命令之前，**务必先与用户确认所有参数**，包括代币名称、代码、描述、图片以及购买金额。
2. **务必先使用 `--dry-run` 参数进行参数验证**，确保一切正常后再进行实际操作。
3. **请务必提醒用户**：此操作会在 Solana 主网上创建真实的代币，并会产生实际的费用（即 SOL）。
4. 启动操作的费用约为 0.02 SOL（包括租金和手续费），初始购买金额需额外支付。
5. 成功后，请将代币铸造地址和交易签名告知用户。
6. 代币的访问链接格式为：`https://pump.fun/<MINT_ADDRESS>`
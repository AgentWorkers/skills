---
name: pumpfun-launch
description: 在 pump.fun（Solana 的纪念币/表情币平台）上启动一个新的代币。当用户需要在 pump.fun 上创建/发布/部署新的代币时，可以使用此功能。该功能负责处理钱包设置、将元数据上传到 IPFS 以及链上代币的创建过程。整个过程通过 pumpdotfun-sdk 直接在链上完成，无需使用 PumpPortal 中间件，也不会产生额外费用。
---
# Pump.fun 代币启动器

## 设置

该技能文件位于 `skills/pumpfun-launch/` 目录下。首次运行前，请执行以下操作：

```bash
cd skills/pumpfun-launch && bun install
```

## 环境配置

在技能文件夹中创建一个名为 `.env` 的文件，并配置相关环境变量：

```
HELIUS_RPC_URL=https://mainnet.helius-rpc.com/?api-key=YOUR_KEY
WALLET_PRIVATE_KEY=base58_encoded_private_key
```

您可以在 [https://dev.helius.xyz/](https://dev.helius.xyz/) 获取免费的 Helius 密钥。

如果 `WALLET_PRIVATE_KEY` 变量未设置，脚本会生成一个新的钱包并将其保存为 `.wallet.key` 文件（该文件会使用密码进行加密）。在启动之前，请先向钱包中充值 SOL（Solana 代币）。

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
| `--image` | ✅ | 图像文件路径（PNG/JPG 格式）或 URL |
| `--buy` | ❌ | 初始购买金额（单位：SOL，默认值：0） |
| `--slippage` | ❌ | 滑点率（以基点为单位，默认值：500） |
| `--priority-fee` | ❌ | 优先费用（单位：微拉姆波特，micro-lamports，默认值：250000） |
| `--dry-run` | ❌ | 不发送交易，仅进行模拟运行 |
| `--status` | ❌ | 通过提供 mint.pub 密钥来检查代币铸造地址的状态 |

### 检查代币状态

```bash
bun run launch.ts --status <MINT_ADDRESS>
```

## ⚠️ 重要提示 — 代理操作指南

1. 在运行启动命令之前，务必与用户确认所有参数。向用户展示代币的名称、代码、描述以及购买金额。
2. 在实际启动之前，务必先使用 `--dry-run` 选项进行参数验证。
3. 请务必提醒用户：此操作会在 Solana 主网上创建真实的代币，并需要消耗真实的 SOL 代币。
4. 启动操作的费用约为 0.02 SOL（包括租金和手续费）。初始购买金额需额外支付。
5. 成功后，将代币铸造地址和交易签名信息告知用户。
6. 代币的购买链接格式为：`https://pump.fun/<MINT_ADDRESS>`
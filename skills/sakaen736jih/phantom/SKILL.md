---
name: phantom
description: 使用 Phantom 浏览器扩展程序：添加自定义网络、导入令牌、检查已连接的去中心化应用（dApps）、排查问题以及管理 Solana/Ethereum/Polygon 账户。
metadata: {"openclaw":{"requires":{"bins":["solana"]},"install":[{"id":"solana","kind":"shell","command":"sh -c \"$(curl -sSfL https://release.solana.com/stable/install)\"","bins":["solana"],"label":"Install Solana CLI"}]}}
---

# Phantom 钱包

## 安装

- Chrome: https://chrome.google.com/webstore/detail/phantom/bfnaelmomeimhlpmgjnjophhpkkoljpa  
- Firefox: https://addons.mozilla.org/firefox/addon/phantom-app/  
- Brave: 与 Chrome 类似  
- 移动端：iOS App Store / Google Play  

## 支持的网络  

| 网络 | 类型 | 原生资产 |
|---------|------|--------------|
| Solana | 默认 | SOL |
| Ethereum | EVM | ETH |
| Polygon | EVM | MATIC |
| Base | EVM | ETH |

## 添加自定义 RPC（Solana）  

**设置 → 开发者设置 → 更改网络 → 添加自定义 RPC**  

常用的 RPC 服务：  
```
Helius: https://mainnet.helius-rpc.com/?api-key=YOUR_KEY
QuickNode: https://YOUR_ENDPOINT.quiknode.pro/
Alchemy: https://solana-mainnet.g.alchemy.com/v2/YOUR_KEY
Triton: https://YOUR_PROJECT.triton.one/
```  

## 添加自定义网络（EVM）  

**设置 → 开发者设置 → 添加网络**  

- Polygon:  
```
Name: Polygon Mainnet
RPC: https://polygon-rpc.com
Chain ID: 137
Symbol: MATIC
Explorer: https://polygonscan.com
```  
- Arbitrum:  
```
Name: Arbitrum One
RPC: https://arb1.arbitrum.io/rpc
Chain ID: 42161
Symbol: ETH
Explorer: https://arbiscan.io
```  

## 导入 SPL 代币  

1. 进入代币列表  
2. 点击“管理代币列表”  
3. 搜索或粘贴合约地址  
4. 启用该代币  

常见的 SPL 代币：  
```
USDC: EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
USDT: Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB
RAY: 4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R
BONK: DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263
JUP: JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN
```  

## 查看账户余额（通过 CLI）  

```bash
solana balance YOUR_PHANTOM_ADDRESS --url https://api.mainnet-beta.solana.com
```  

## 查看交易历史  

- 通过 Solscan:  
```bash
open "https://solscan.io/account/YOUR_ADDRESS"
```  
- 通过 CLI:  
```bash
solana transaction-history YOUR_ADDRESS --limit 20
```  

## 将账户信息导出（用于 CLI）  

在 Phantom 中：**设置 → 安全 → 导出私钥**  
导入到 Solana CLI（请谨慎操作！）：  
```bash
solana-keygen recover ASK
```  

## 连接的应用程序管理  

**设置 → 连接的应用程序 → 查看/撤销连接**  

## 交易费用优先级  

**设置 → 交易设置 → 交易费用优先级**  
- 普通：约 0.000005 SOL  
- 高优先级：约 0.00005 SOL  
- 快速交易：约 0.0005 SOL  

## 故障排除  

- **交易卡住**：  
```bash
# Check transaction status
solana confirm TX_SIGNATURE -v
```  
- **代币未显示**：  
  1. 管理代币列表 → 搜索合约地址  
  2. 或手动输入地址导入代币  
- **余额错误**：  
  设置 → 开发者设置 → 重置缓存  
- **RPC 问题**：  
  在开发者设置中尝试不同的 RPC 端点  

## Phantom 的深度链接  

```
# Open Phantom
phantom://

# Connect to dApp
phantom://browse/YOUR_DAPP_URL

# View transaction
phantom://tx/TX_SIGNATURE
```  

## 移动端专属功能  

- 面容识别/指纹识别：**设置 → 安全**  
- 自动锁定：**设置 → 安全 → 自动锁定时间**  
- 测试网：**设置 → 开发者设置 → 更改网络**  

## 注意事项  

- Phantom 从单一恢复短语生成账户地址  
- 支持硬件钱包（如 Ledger）  
- 内置 Jupiter 交易聚合器  
- 提供 NFT 画廊  
- 通过恢复短语实现浏览器扩展程序与移动端的同步
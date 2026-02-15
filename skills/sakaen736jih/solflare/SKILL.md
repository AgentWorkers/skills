---
name: solflare
description: 使用 Solflare 钱包：管理 Solana 资产、参与质押（staking）、自定义 RPC 设置（RPC setup）、集成硬件钱包（hardware wallet integration），以及进行非同质化代币（NFT）的管理。
metadata: {"openclaw":{"requires":{"bins":["solana"]},"install":[{"id":"solana","kind":"shell","command":"sh -c \"$(curl -sSfL https://release.solana.com/stable/install)\"","bins":["solana"],"label":"Install Solana CLI"}]}}
---

# Solflare钱包

## 安装

- 网页版：https://solflare.com/access  
- Chrome扩展程序：https://chrome.google.com/webstore/detail/solflare-wallet/bhhhlbepdkbapadjdnnojkbgioiodbic  
- 移动版：iOS应用商店 / Google Play  

## 支持的功能  

| 功能 | 是否支持 |  
|---------|---------|  
| Solana | 是 |  
| SPL代币 | 是 |  
| NFTs | 是 |  
| 质押 | 是（内置功能） |  
| 密码本（Ledger） | 是 |  
| dApp浏览器 | 是 |  

## 配置自定义RPC  

**设置 → 网络 → 自定义RPC**  
推荐的RPC配置：  
```
Helius: https://mainnet.helius-rpc.com/?api-key=YOUR_KEY
QuickNode: https://YOUR_ENDPOINT.solana-mainnet.quiknode.pro/
Triton: https://YOUR_PROJECT.triton.one/
GenesysGo: https://ssc-dao.genesysgo.net/
```  

## 质押SOL  

1. 进入“投资组合”（Portfolio） → “质押”（Staking）  
2. 选择质押节点或使用Solflare的质押池  
3. 输入质押金额  
4. 确认交易  

**通过CLI检查质押情况：**  
```bash
solana stakes YOUR_ADDRESS --url mainnet-beta
```  

## 查看质押账户信息  

```bash
solana stake-account YOUR_STAKE_ACCOUNT_ADDRESS --url mainnet-beta
```  

**列出所有质押记录：**  
```bash
curl -s -X POST https://api.mainnet-beta.solana.com -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getProgramAccounts",
  "params": [
    "Stake11111111111111111111111111111111111111",
    {
      "encoding": "jsonParsed",
      "filters": [
        {"memcmp": {"offset": 12, "bytes": "YOUR_ADDRESS"}}
      ]
    }
  ]
}'
```  

## 导入代币  

进入“投资组合”（Portfolio） → “管理代币列表”（Manage Token List） → “添加代币”（Add Token）  
粘贴代币合约地址：  
```
USDC: EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
USDT: Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB
mSOL: mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So
stSOL: 7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj
```  

## 查看余额（通过CLI）  

- SOL余额：  
```bash
solana balance YOUR_SOLFLARE_ADDRESS
```  
- 代币余额：  
```bash
spl-token accounts --owner YOUR_SOLFLARE_ADDRESS
```  

## NFT管理  

进入“投资组合”（Portfolio） → “NFTs”（NFTs）标签页  

**通过CLI查看NFT信息：**  
```bash
# Install metaboss
cargo install metaboss

# List NFTs
metaboss snapshot mints -c YOUR_ADDRESS -o nfts.json
```  

## 硬件钱包（Ledger）  

1. 在Ledger设备上安装Solana应用程序  
2. 在Solflare钱包中选择“硬件钱包”（Hardware Wallet） → “Ledger”  
3. 连接硬件钱包并选择相应的地址  
4. 检查Ledger地址：  
```bash
solana-keygen pubkey usb://ledger
```  

## 交易历史  

- 通过Solscan查看交易历史：  
```
https://solscan.io/account/YOUR_ADDRESS
```  
- 通过CLI查看交易历史：  
```bash
solana transaction-history YOUR_ADDRESS --limit 10
```  

## 优先级费用设置  

**设置 → 优先级费用（Priority Fee）**  
- 市场模式：根据网络状况动态调整  
- 自定义模式：手动设置lamports金额  

## 收藏品（NFTs）  

查看NFT的元数据：  
```bash
metaboss decode mint -a NFT_MINT_ADDRESS
```  

## 连接的dApps  

进入“设置”（Settings） → “已连接的dApps”（Connected Apps） → “管理”（Manage）  

## 导出数据以供CLI使用  

**设置 → 导出（Export） → 显示恢复短语（Show recovery phrase）**  
创建密钥对文件：  
```bash
solana-keygen recover -o ~/my-solflare.json
```  

## 故障排除  

- **质押信息未显示？**  
```bash
# Verify stake accounts
solana stakes YOUR_ADDRESS
```  
- **交易失败？**  
```bash
# Check recent blockhash
solana block-time $(solana slot)
```  
- **代币余额错误？**  
```bash
# Get actual balance
spl-token balance TOKEN_MINT --owner YOUR_ADDRESS
```  

## Solflare与Phantom的对比  

| 功能 | Solflare | Phantom |  
|---------|---------|---------|  
| 支持的区块链 | 仅支持Solana | 支持多链 |  
| 质押界面 | 高级界面 | 基础界面 |  
| 密码本支持 | 完全支持 | 完全支持 |  
| 网页版 | 支持 | 不支持 |  
| 可选择的质押节点 | 可自由选择 | 选择范围有限 |  

## 注意事项  

- Solflare专注于Solana区块链；不支持EVM兼容的链。  
- 内置质押功能，支持选择质押节点。  
- 网页版无需扩展程序即可使用。  
- 支持Ledger和Keystone硬件钱包。  
- 提供专业的质押数据分析功能。  
- 具备批量管理NFT的功能。
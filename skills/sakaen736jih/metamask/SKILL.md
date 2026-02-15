---
name: metamask
description: 使用 MetaMask 钱包：  
- 添加自定义网络  
- 导入 ERC-20 代币  
- 管理权限  
- 配置 gas 费用设置  
- 与去中心化应用（dApps）集成
metadata: {"openclaw":{"requires":{"bins":["cast"]},"install":[{"id":"foundry","kind":"shell","command":"curl -L https://foundry.paradigm.xyz | bash && foundryup","bins":["cast"],"label":"Install Foundry (cast)"}]}}
---

# MetaMask 钱包

## 安装

- Chrome: https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn  
- Firefox: https://addons.mozilla.org/firefox/addon/ether-metamask/  
- 移动端：iOS App Store / Google Play  
- Flask（开发版）: https://metamask.io/flask/  

## 添加常用网络  

**Polygon:**  
```
Network: Polygon Mainnet
RPC: https://polygon-rpc.com
Chain ID: 137
Symbol: MATIC
Explorer: https://polygonscan.com
```  

**Arbitrum:**  
```
Network: Arbitrum One
RPC: https://arb1.arbitrum.io/rpc
Chain ID: 42161
Symbol: ETH
Explorer: https://arbiscan.io
```  

**Optimism:**  
```
Network: Optimism
RPC: https://mainnet.optimism.io
Chain ID: 10
Symbol: ETH
Explorer: https://optimistic.etherscan.io
```  

**Base:**  
```
Network: Base
RPC: https://mainnet.base.org
Chain ID: 8453
Symbol: ETH
Explorer: https://basescan.org
```  

**BSC:**  
```
Network: BNB Smart Chain
RPC: https://bsc-dataseed.binance.org
Chain ID: 56
Symbol: BNB
Explorer: https://bscscan.com
```  

**Avalanche:**  
```
Network: Avalanche C-Chain
RPC: https://api.avax.network/ext/bc/C/rpc
Chain ID: 43114
Symbol: AVAX
Explorer: https://snowtrace.io
```  

## 导入 ERC-20 代币  

**资产** → **导入代币** → **自定义代币**  
常见的以太坊代币：  
```
USDC: 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
USDT: 0xdAC17F958D2ee523a2206206994597C13D831ec7
DAI: 0x6B175474E89094C44Da98b954EescdeCB5BE3830
WETH: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
LINK: 0x514910771AF9Ca656af840dff83E8264EcF986CA
UNI: 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
```  

## 查看余额（通过 CLI）  

**ETH 余额:**  
```bash
cast balance YOUR_ADDRESS --ether --rpc-url https://eth.llamarpc.com
```  

**代币余额:**  
```bash
cast call 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  "balanceOf(address)(uint256)" YOUR_ADDRESS \
  --rpc-url https://eth.llamarpc.com
```  

## ENS 名称  

**解析 ENS:**  
```bash
cast resolve-name vitalik.eth --rpc-url https://eth.llamarpc.com
```  

**反向查询:**  
```bash
cast lookup-address YOUR_ADDRESS --rpc-url https://eth.llamarpc.com
```  

## Gas 设置  

**设置** → **高级** → **高级 Gas 控制**  
查看当前 Gas 值：  
```bash
cast gas-price --rpc-url https://eth.llamarpc.com | xargs -I {} cast --to-unit {} gwei
```  

## 交易历史  

**通过 Etherscan 查看:**  
```
https://etherscan.io/address/YOUR_ADDRESS
```  

**通过 CLI 查看:**  
```bash
cast etherscan-source YOUR_ADDRESS --etherscan-api-key YOUR_KEY
```  

## 连接的节点  

**设置** → **连接的节点** → **管理权限**  

## 账户管理  

**创建账户**: **账户** 菜单 → **创建账户**  
**导入账户**: **账户** 菜单 → **导入账户**  

## 硬件钱包  

1. 连接 Ledger/Trezor 硬件钱包  
2. **账户** 菜单 → **连接硬件钱包**  
3. 选择设备并输入地址  

## 自定义交易随机数（Nonce）  

**设置** → **高级** → **自定义交易随机数**  
获取当前随机数：  
```bash
cast nonce YOUR_ADDRESS --rpc-url https://eth.llamarpc.com
```  

## 加快/取消交易  

**待处理的交易**: **加快或取消交易**  
可以通过 CLI 来执行此操作：  
```bash
# Check pending nonce
cast nonce YOUR_ADDRESS --rpc-url https://eth.llamarpc.com
```  

## 导出账户  

**账户** 菜单 → **账户详情** → **导出**  

## 网络 RPC 端点  

| 网络 | 免费 RPC 地址 |  
|---------|----------|  
| Ethereum | https://eth.llamarpc.com |  
| Polygon | https://polygon-rpc.com |  
| Arbitrum | https://arb1.arbitrum.io/rpc |  
| Optimism | https://mainnet.optimism.io |  
| Base | https://mainnet.base.org |  
| BSC | https://bsc-dataseed.binance.org |  

## 故障排除  

**交易卡住**:  
```bash
# Get pending nonce
cast nonce YOUR_ADDRESS --pending --rpc-url https://eth.llamarpc.com
```  
此时，可以使用相同的随机数和更高的 Gas 值向自己发送 0 ETH 来尝试恢复交易。  

**代币余额错误**:  
**资产** → **刷新列表** 或重新导入代币。  

**网络无法连接**:  
**设置** → **网络** → **编辑 RPC 地址**。  

**重置账户**:  
**设置** → **高级** → **清除活动记录数据**。  

## MetaMask 的扩展功能（Snaps）  

**通过扩展功能增强 MetaMask 功能**:  
**设置** → **扩展** → **浏览扩展程序**  
常见的扩展程序包括：  
- 交易洞察  
- 账户管理  
- 互操作性  

## 移动端同步  

**移动端**:  
1. **设置** → **与扩展程序同步**  
2. 通过扩展程序扫描二维码  
3. 或者使用相同的恢复短语（recovery phrase）进行登录。  

## 安全提示**  

- **切勿分享恢复短语**  
- 连接前请验证网址  
- 批准操作前请仔细检查权限设置  
- 处理大额交易时请使用硬件钱包  
- 启用网络钓鱼检测功能  

## 注意事项**  

- MetaMask 仅支持以太坊（EVM）及其兼容的区块链  
- 默认网络为以太坊主网  
- 支持 EIP-1559 交易  
- 内置了通过聚合器进行资产交换的功能  
- 移动端版本自带浏览器
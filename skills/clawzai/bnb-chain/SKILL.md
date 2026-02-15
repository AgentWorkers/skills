---
name: bnb-chain
version: 0.1.0
description: 基本的 BNB 链操作——查询余额、发送 BNB、发送 BEP-20 代币。
metadata: {"openclaw":{"emoji":"🟡","category":"blockchain","requires":{"bins":["node"]}}}
---

# BNB Chain 技能

## BNB Chain（BSC）的基本操作  
- 查看余额  
- 发送交易  

## 准备  
需要 Node.js 和 ethers.js：  
```bash
cd ~/.openclaw/workspace/skills/bnb-chain && npm install ethers --silent
```  

## 配置  
请妥善保管您的私钥。该技能会从环境变量中读取私钥：  
```bash
export BNB_PRIVATE_KEY="0x..."
```  
或者直接将私钥传递给辅助脚本。  

## 使用方法  
所有操作均通过辅助脚本 `bnb.js` 完成：  

### 查看 BNB 余额  
```bash
node bnb.js balance <address>
```  
示例：  
```bash
node bnb.js balance 0x9787436458A36a9CC72364BaC18ba78fdEf83997
```  

### 查看 BEP-20 代币余额  
```bash
node bnb.js token-balance <token_address> <wallet_address>
```  
示例（USDT）：  
```bash
node bnb.js token-balance 0x55d398326f99059fF775485246999027B3197955 0x9787436458A36a9CC72364BaC18ba78fdEf83997
```  

### 发送 BNB  
```bash
node bnb.js send <to_address> <amount_bnb> [--key <private_key>]
```  
示例：  
```bash
node bnb.js send 0xRecipient 0.01 --key 0xYourPrivateKey
```  

### 发送 BEP-20 代币  
```bash
node bnb.js send-token <token_address> <to_address> <amount> [--key <private_key>]
```  
示例（发送 10 USDT）：  
```bash
node bnb.js send-token 0x55d398326f99059fF775485246999027B3197955 0xRecipient 10 --key 0xYourPrivateKey
```  

### 从私钥获取钱包地址  
```bash
node bnb.js address <private_key>
```  

### 获取交易详情  
```bash
node bnb.js tx <tx_hash>
```  

## 常见代币地址（BSC 主网）  
| 代币 | 地址         |
|-------|-------------|
| USDT | `0x55d398326f99059fF775485246999027B3197955` |
| USDC | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` |
| BUSD | `0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56` |
| WBNB | `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c` |

## RPC 端点  
默认地址：`https://bsc-dataseed.binance.org/`  
其他可选地址：  
- `https://bsc-dataseed1.binance.org/`  
- `https://bsc-dataseed2.binance.org/`  
- `https://bsc-dataseed3.binance.org/`  
- `https://bsc-dataseed4.binance.org/`  

## 安全提示：  
- **切勿将私钥提交到 Git**  
- 使用环境变量或安全存储方式来保管私钥  
- 在发送交易前请仔细核对接收地址  
- 先使用小额资金进行测试
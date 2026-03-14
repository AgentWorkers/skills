---
name: solana
description: >
  查询Solana区块链数据，包括以下信息：  
  - 钱包余额  
  - 持有代币的完整投资组合（包含代币名称及价值）  
  - 交易详情  
  - 非同质化代币（NFTs）的信息  
  - “鲸鱼用户”（持有大量代币的用户）的识别  
  - 实时的网络状态统计  
  该工具基于Solana的RPC（Remote Procedure Call）协议以及CoinGecko的数据源进行查询，无需使用API密钥。
version: 0.2.0
author: Deniz Alagoz (gizdusum), enhanced by Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Solana, Blockchain, Crypto, Web3, RPC, DeFi, NFT]
    related_skills: []
---
# Solana区块链技能

通过CoinGecko查询Solana链上数据，并提供美元价格信息。  
支持以下8个命令：  
- 钱包资产组合  
- 代币信息  
- 交易记录  
- 活动日志  
- NFT列表  
- 大额交易检测（“鲸鱼”行为识别）  
- 网络状态统计  
- 代币价格查询  

无需API密钥，仅使用Python标准库（urllib、json、 argparse）。  

---

## 使用场景  

- 用户查询Solana钱包余额、代币持有情况或资产组合价值  
- 用户希望通过交易签名查询特定交易  
- 用户需要SPL代币的元数据、价格、供应量及持有者信息  
- 用户想查看某个地址的最新交易记录  
- 用户想获取钱包中持有的NFT列表  
- 用户希望检测大额SOL转账（“鲸鱼”行为）  
- 用户需要了解Solana网络的健康状况、TPS（每秒交易处理量）、当前时代（epoch）或SOL价格  
- 用户询问“BONK/JUP/SOL的价格是多少？”  

---

## 前提条件  

该辅助脚本仅使用Python标准库（urllib、json、 argparse），无需额外安装任何外部包。  
价格数据来自CoinGecko的免费API（无需密钥，但每分钟请求量有限，约为10-30次）。如需加快查询速度，可使用`--no-prices`参数。  

---

## 快速参考  

- **RPC端点（默认）**：`https://api.mainnet-beta.solana.com`  
  **可自定义端点**：`export SOLANA_RPC_URL=https://your-private-rpc.com`  
- **辅助脚本路径**：`~/.hermes/skills/blockchain/solana/scripts/solana_client.py`  

---

## 使用流程  

### 0. 设置检查  
（代码块1：此处应包含设置相关逻辑，但未提供具体代码）  

### 1. 钱包资产组合  

获取SOL余额、SPL代币持有量（含美元价值）、NFT数量及资产组合总价值。  
代币按价值排序，过滤掉无价值的“dust”代币，并以名称（如BONK、JUP、USDC等）显示已知代币。  

---

**参数说明：**  
- `--limit N`：显示前N个代币（默认：20个）  
- `--all`：显示所有代币，不进行过滤  
- `--no-prices`：跳过CoinGecko的价格查询（速度更快，仅使用RPC接口）  

**输出内容：**  
- SOL余额及美元价值  
- 按价值排序的代币列表及价格  
- NFT统计信息  
- 资产组合的总美元价值  

---

### 2. 交易详情  

通过交易的基础58签名查询完整交易记录，显示SOL和美元的余额变化情况。  

---

**输出内容：**  
- 交易信息（如时间戳、费用、状态、SOL和美元余额变化）  
- 被调用的程序（program invocations）  

---

### 3. 代币信息  

获取SPL代币的元数据（如名称、符号、小数位数、供应量、铸造/冻结权限）及前5大持有者信息。  

---

**输出内容：**  
- 代币名称、符号、小数位数、供应量、当前价格、市场价值及前5大持有者（占比）  

---

### 4. 最新交易记录  

列出某个地址的最新交易记录（默认显示最近10笔，最多25笔）。  

---

### 5. NFT列表  

列出钱包中持有的NFT（根据规则：SPL代币中`amount`字段值为1且`decimals`字段值为0的代币）。  

**注意：**  
该方法无法检测压缩型NFT（cNFT）。  

---

### 6. 大额交易检测  

扫描最新区块，查找大额SOL转账（“鲸鱼”行为）。  

**注意：**  
仅扫描最新区块，因此结果为实时数据，不包含历史记录。  

---

### 7. 网络状态统计  

显示Solana网络的实时状态：当前区块编号、当前时代、TPS、供应量、验证者版本、SOL价格及市场价值。  

---

### 8. 代币价格查询  

根据代币的铸造地址或符号快速查询价格。  

**已知支持的代币符号：**  
SOL、USDC、USDT、BONK、JUP、WETH、JTO、mSOL、stSOL、PYTH、HNT、RNDR、WEN、W、TNSR、DRIFT、bSOL、JLP、WIF、MEW、BOME、PENGU  

---

## 注意事项  

- **CoinGecko的请求限制**：免费账户每分钟仅允许10-30次请求。  
  价格查询每次请求会消耗1次请求次数，持有大量代币的账户可能无法获取所有代币的价格。可使用`--no-prices`参数加快查询速度。  
- **Solana公共RPC的请求限制**：生产环境建议使用私有RPC端点（如Helius、QuickNode、Triton）。  
- **NFT检测的准确性**：仅基于规则（`amount=1`且`decimals=0`），压缩型NFT（cNFT）和Token-2022格式的NFT可能无法被识别。  
- **交易历史记录**：公共RPC仅保留约2天的交易记录，较旧的交易可能无法查询到。  
- **代币名称显示**：约25种常见代币会以全名显示，其他代币会显示缩写后的铸造地址。可使用`token`命令获取完整信息。  
- **错误处理**：当遇到请求限制或API错误时，脚本会尝试重试（最多2次），采用指数级退避策略。  

---

## 验证流程  
（代码块10：此处应包含验证相关逻辑，但未提供具体代码）
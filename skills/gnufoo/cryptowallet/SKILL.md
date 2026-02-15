---
name: cryptowallet
description: "**完整的加密货币钱包管理工具，适用于Web3、DeFi和区块链应用程序**  
该工具支持创建和管理EVM（以太坊、Polygon、BSC、Arbitrum、Optimism、Base、Avalanche）以及Solana平台的钱包，并提供加密的本地存储功能。用户可以查询原生代币（ETH、MATIC、BNB、SOL）和标准代币（ERC20、SPL）的余额，执行交易，与智能合约交互，并管理跨12个以上区块链网络的多个钱包地址。  

**主要功能：**  
- **安全加密存储**：采用AES-256加密技术保护用户的私钥，确保数据安全。  
- **多链支持**：兼容以太坊、Polygon、BSC、Arbitrum、Optimism、Base、Avalanche、Solana等主流区块链平台。  
- **代币管理**：支持查询和操作多种代币（包括原生代币和ERC20、SPL标准代币）。  
- **交易功能**：能够发送加密货币和代币。  
- **DeFi集成**：支持与DeFi协议和智能合约的交互。  
- **投资组合管理**：方便用户管理跨多个区块链平台的资产组合。  
- **NFT转移**：支持NFT的转移操作。  
- **区块链开发与测试**：为区块链项目的开发和测试提供便捷的工具支持。  

**适用场景：**  
- **新钱包创建**：用户可轻松创建新的加密货币钱包。  
- **现有钱包导入**：支持导入其他平台的钱包数据。  
- **跨链资产查询**：方便用户查看不同区块链上的资产余额。  
- **交易处理**：支持安全地发送加密货币和代币。  
- **DeFi集成**：适用于与DeFi项目进行交互。  
- **多链投资组合管理**：帮助用户高效管理多链资产。  
- **NFT交易**：支持NFT的转移和交易。  
- **区块链开发**：为区块链项目的开发提供必要的工具支持。  

**关键词：**  
- 加密货币（Cryptocurrency）  
- 钱包（Wallet）  
- 区块链（Blockchain）  
- 以太坊（Ethereum）  
- Solana  
- Web3  
- DeFi（去中心化金融）  
- 代币（Token）  
- ERC20  
- NFT（非同质化代币）  
- 智能合约（Smart Contract）  
- Metamask替代方案  
- 硬件钱包（Hardware Wallet）  
- 冷存储（Cold Storage）  
- 热存储（Hot Storage）  
- 数字钱包（Digital Wallet）  
- 比特币（Bitcoin）"
---

# CryptoWallet

这是一个专为Clawdbot代理设计的全面加密货币钱包管理工具，支持在多个区块链网络上安全地创建、管理和进行交易，并提供加密的本地密钥存储功能。

## 支持的网络

### EVM链（12个网络）
- Ethereum、Polygon、BSC、Arbitrum、Optimism、Base
- Avalanche、Fantom、Gnosis、zkSync、Linea、Scroll

### Solana
- 主网（Mainnet）和开发网（Devnet）

完整的网络信息请参见 `references/networks.json`。

## 核心功能

### 1. 钱包管理
- 创建新钱包或导入现有钱包：
  ```bash
# Create new EVM wallet
python3 scripts/wallet_manager.py create my-eth-wallet --chain evm --password "secure-password"

# Create new Solana wallet
python3 scripts/wallet_manager.py create my-sol-wallet --chain solana --password "secure-password"

# Import existing wallet
python3 scripts/wallet_manager.py import imported-wallet --chain evm --key "0x..." --password "secure-password"

# List all wallets
python3 scripts/wallet_manager.py list
```

### 2. 余额查询
- 查询原生代币和自定义代币的余额：
  ```bash
# Native ETH balance on Ethereum
python3 scripts/balance_checker.py 0xYourAddress --network ethereum

# ERC20 token balance
python3 scripts/balance_checker.py 0xYourAddress --network polygon --token 0xTokenAddress

# Check all EVM networks at once
python3 scripts/balance_checker.py 0xYourAddress --all-evm

# Solana balance
python3 scripts/balance_checker.py YourSolanaAddress --network solana

# SPL token balance
python3 scripts/balance_checker.py YourSolanaAddress --network solana --token MintAddress
```

### 3. 代币转账
- 发送原生代币或ERC20/SPL代币：
  ```bash
# Send ETH
python3 scripts/token_sender.py my-wallet 0xRecipient 0.1 --network ethereum --password "password"

# Send ERC20 token
python3 scripts/token_sender.py my-wallet 0xRecipient 100 --network polygon --token 0xTokenAddress --password "password"

# Send SOL
python3 scripts/token_sender.py my-wallet RecipientAddress 1.5 --network solana --password "password"
```

**安全性说明：** 每次交易都需要输入密码。私钥始终存储在加密状态中，不会以明文形式暴露。

### 4. 智能合约交互
- 调用智能合约函数（读取和写入数据）：
  ```bash
# Read call (view function)
python3 scripts/contract_interactor.py 0xContract functionName --abi contract.json --network ethereum --args '[123, "param2"]'

# Write call (transaction)
python3 scripts/contract_interactor.py 0xContract mint --abi nft.json --network polygon --args '[1]' --write --wallet my-wallet --password "password"

# Payable function (send ETH with call)
python3 scripts/contract_interactor.py 0xContract purchase --abi contract.json --network ethereum --args '[]' --write --wallet my-wallet --password "password" --value 0.05
```

## 安全架构

### 加密机制
- **加密算法：** AES-256-GCM，采用PBKDF2进行密钥派生
- **迭代次数：** 100,000次（OWASP推荐）
- **盐值：** 每个钱包使用一个随机的16字节盐值
- **存储位置：** `~/.clawdbot/cryptowallet/`，权限设置为0600

### 关键安全原则
1. **密码保护**：所有交易操作都需要输入正确的密码。
2. **数据加密存储**：私钥始终以加密形式保存，不会以明文形式存储。
3. **防止密钥泄露**：私钥仅在签名时解密。
4. **独立存储**：每个钱包的密钥都采用独立的加密方式。

完整的 security 文档请参阅 `references/security.md`。

## 常见操作流程

### 财产管理
- 查看所有网络上的余额：
  ```bash
python3 scripts/balance_checker.py 0xYourAddress --all-evm
```

### 多链操作
- 在不同链上发送相同的代币：
  ```bash
# Polygon USDC
python3 scripts/token_sender.py wallet recipient 100 --network polygon --token 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --password "pwd"

# Arbitrum USDC
python3 scripts/token_sender.py wallet recipient 100 --network arbitrum --token 0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8 --password "pwd"
```

### DeFi协议交互
- 例如：批准和质押代币：
  ```bash
# 1. Approve token spending
python3 scripts/contract_interactor.py 0xTokenAddress approve --abi erc20.json --network ethereum --args '["0xProtocolAddress", "1000000000000000000000"]' --write --wallet my-wallet --password "pwd"

# 2. Stake tokens
python3 scripts/contract_interactor.py 0xStakingContract stake --abi staking.json --network ethereum --args '["1000000000000000000000"]' --write --wallet my-wallet --password "pwd"
```

## 网络配置
- 可以通过修改 `references/networks.json` 文件来：
  - 添加自定义的RPC服务（如Infura、Alchemy、QuickNode）
  - 添加新的网络
  - 更新链的ID或相关浏览器地址

默认使用的RPC服务可能受到速率限制。在生产环境中，请使用专用的RPC服务提供商。

## 依赖项
- 请安装所需的软件包：
  ```bash
pip install web3 solana solders eth-account cryptography base58
```

## 故障排除

### “密码错误”
- 密码区分大小写。
- 如果密码丢失，无法恢复钱包数据（这是设计上的安全措施）。

### “资金不足”
- 请注意余额中包含交易手续费。
- 在Ethereum网络上，每次交易的手续费可能为5美元至50美元以上。

### “交易失败”
- 确认网络选择正确。
- 检查合约地址是否正确。
- 确保复杂操作有足够的Gas费用。

### RPC错误
- 公共RPC服务可能受到速率限制。
- 请参考 `references/networks.json` 文件来配置自定义的RPC端点。

## 高级用法

### 自定义网络
- 如需添加新的网络，请修改 `references/networks.json` 文件：
  ```json
{
  "evm": {
    "your-network": {
      "name": "Your Chain",
      "chain_id": 12345,
      "rpc": "https://rpc.yourchain.com",
      "explorer": "https://explorer.yourchain.com",
      "native_token": "TOKEN"
    }
  }
}
```

### 批量操作
- 可以使用shell脚本批量执行交易：
  ```bash
for addr in $(cat recipients.txt); do
  python3 scripts/token_sender.py wallet $addr 1 --network polygon --password "pwd"
done
```

### 智能合约ABI
- 可以从区块链浏览器中验证过的合约文件或你的Solidity项目的 `artifacts/` 文件夹中生成ABI文件。

## 限制
- **Solana SPL转账：** 目前仅提供基本功能（可能需要创建专门的代币账户）。
- **硬件钱包：** 不支持。
- **多签名（Multi-sig）：** 不支持。
- **Gas费用估算：** 使用固定的Gas费用上限，对于复杂的合约可能会失败。

## 最佳实践
1. 在主网交易前，先在开发网（devnet/testnet）上进行测试。
2. 为不同的用途（交易、DeFi操作、冷存储）使用不同的钱包。
3. 备份钱包文件，并安全地保管密码。
4. 确认交易地址的正确性——区块链交易是不可撤销的。
5. 关注Gas费用动态——在Ethereum网络上选择交易时，选择拥堵较低的时段进行交易。

完整的 security 指南请参阅 `references/security.md`。
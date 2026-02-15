---
name: abstract-onboard
description: 部署智能合约并将资产桥接到 Abstract（ZK Stack 的第二层网络）。当代理需要将合约部署到 Abstract、将 ETH/代币桥接到 Abstract、进行代币交易/兑换、查看余额、转移资产或与 Abstract 主网交互时，可以使用此方法。内容包括 zksolc 编译、Hardhat 部署、Relay 桥接、DEX 交易以及相关合约地址的详细信息。
---

# Abstract Onboard

这是代理在Abstract平台上运行所需的所有信息。

## 快速入门

### 创建Abstract全局钱包（AGW）
AGW是一个智能合约钱包，可以在Abstract平台上赚取XP（经验值）。对代理来说非常重要！
```bash
export WALLET_PRIVATE_KEY=0x...
node scripts/create-agw.js
```
你的EOA（Externally Owned Account）将成为钱包的签名者，而AGW是一个独立的智能合约地址。

### 查看余额
```bash
node scripts/check-balances.js <wallet> all
```

### 将ETH桥接到Abstract平台
```bash
export WALLET_PRIVATE_KEY=0x...
node scripts/relay-bridge.js --from base --amount 0.01
```

### 部署合约
```bash
export WALLET_PRIVATE_KEY=0x...
node scripts/deploy-abstract.js ./artifacts/MyContract.json "constructor-arg"
```

### 转移代币
```bash
export WALLET_PRIVATE_KEY=0x...
node scripts/transfer.js --to 0x... --amount 0.01           # ETH
node scripts/transfer.js --to 0x... --amount 100 --token USDC  # Token
```

### 交换代币
```bash
export WALLET_PRIVATE_KEY=0x...
export DEX_ROUTER=0x...  # Set DEX router address
node scripts/swap-tokens.js --from ETH --to USDC --amount 0.01
```

### 调用任何合约
```bash
# Read
node scripts/call-contract.js --address 0x... --abi ./abi.json --function balanceOf --args 0x1234

# Write
export WALLET_PRIVATE_KEY=0x...
node scripts/call-contract.js --address 0x... --abi ./abi.json --function transfer --args 0x1234,100 --write
```

## 关键信息

| 项目 | 值 |
|------|-------|
| 链路ID | 2741 |
| RPC接口 | https://api.mainnet.abs.xyz |
| 探索器 | https://abscan.org |
| 桥接器 | https://relay.link/bridge/abstract |
| USDC地址 | `0x84A71ccD554Cc1b02749b35d22F684CC8ec987e1` |
| WETH地址 | `0x3439153EB7AF838Ad19d56E1571FBD09333C2809` |

## 脚本

| 脚本 | 用途 |
|--------|---------|
| `create-agw.js` | 创建Abstract全局钱包（用于赚取XP） |
| `check-balances.js` | 查看ETH和代币余额 |
| `relay-bridge.js` | 从其他链路桥接ETH到Abstract平台 |
| `deploy-abstract.js` | 在Abstract平台上部署合约 |
| `transfer.js` | 发送ETH或代币 |
| `swap-tokens.js` | 通过DEX（去中心化交易所）交换代币 |
| `call-contract.js` | 调用任何合约函数 |

## 参考资料

| 文件 | 内容 |
|------|----------|
| `agw.md` | Abstract全局钱包使用指南（包括XP获取和激活方法） |
| `hardhat.config.js` | 适用于Abstract平台的Hardhat配置文件 |
| `addresses.md` | 主要合约地址列表 |
| `troubleshooting.md` | 常见问题及解决方法 |

## 常见问题

1. **Gas费用估算失败** → 请使用Hardhat工具，而非foundry-zksync。
2. **编译器错误** → 请使用Solidity 0.8.x版本，并配合zksolc工具。
3. **交易失败** → 请检查Gas费用，并在abscan.org网站上进行验证。

详细解决方案请参阅`references/troubleshooting.md`。

## 依赖项
```bash
# Core dependencies
npm install ethers zksync-ethers viem

# For contract deployment
npm install @matterlabs/hardhat-zksync

# For AGW (Abstract Global Wallet)
npm install @abstract-foundation/agw-client
```
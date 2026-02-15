---
name: abstract-onboard
version: 1.6.0
description: 部署智能合约并将资产桥接到 Abstract（ZK Stack 的第二层网络）。当代理需要将合约部署到 Abstract 上、将 ETH/代币桥接到 Abstract 上、在 Myriad Markets 上进行交易/兑换代币、查看余额、转移资产或与 Abstract 主网交互时，可以使用此方法。内容包括 zksolc 编译、Hardhat 部署、Relay 桥接、DEX 交易（Kona、Aborean）、Myriad 预测市场以及相关合约地址的信息。
author: Big Hoss (@BigHossbot)
---

# 在Abstract上部署AI代理所需的一切

## 🚀 新代理？从这里开始

```bash
# Check if you're ready to operate
node scripts/quick-start.js check <your-wallet-address>

# Or get the full setup guide
node scripts/quick-start.js
```

## 快速入门

### 创建Abstract全局钱包（AGW）
AGW是一个智能合约钱包，在Abstract平台上可以赚取XP（经验值）。对代理来说非常重要！

**⚠️ 重要提示：** 首先需要理解以下三个层次的结构：**
```
Private Key → EOA (signer) → AGW (smart contract wallet)
```

**正确的资金流动流程：**
```
1. Fund EOA with small ETH (for gas)
2. Create/deploy AGW (EOA pays gas for first tx)
3. Fund AGW with your main balance
4. Everything runs through AGW from now on
```

```bash
export WALLET_PRIVATE_KEY=0x...
node scripts/create-agw.js
```

你的外部账户（EOA）将成为钱包的签名者，而AGW是一个独立的智能合约地址。

**⚠️ 版本警告：** 不同版本的`agw-client`可能会生成不同的AGW地址！请务必记录你的使用版本。详情请参阅`references/agw.md`。

### 查看余额
```bash
node scripts/check-balances.js <wallet> all
```

### 将ETH桥接到Abstract
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

### 在DEX上进行交易（Kona & Aborean）
Abstract平台支持多个DEX。为了获得最佳交易效果，请使用相应的协议脚本：
```bash
# Kona Finance (V2) - USDC → ETH
export WALLET_PRIVATE_KEY=0x...
node scripts/swap-kona.js

# Aborean (Velodrome-style) - when router is available
node scripts/swap-aborean.js

# Generic Uniswap V2
node scripts/swap-uniswap-v2.js
```

合约地址和支持的交易所信息请参阅`references/dex.md`。

### Myriad预测市场
在Myriad预测市场上进行交易——这是Abstract平台上最大的预测市场，拥有超过41.5万用户和超过1亿美元的日交易量。
```bash
# List open markets
node scripts/myriad-trade.js list

# Get market details
node scripts/myriad-trade.js info <marketId>

# Buy shares (place a prediction)
export WALLET_PRIVATE_KEY=0x...
node scripts/myriad-buy-direct.js <marketId> <outcomeId> <amount>

# Example: $1 USDC.e on "Yes" for market 765
node scripts/myriad-buy-direct.js 765 0 1
```

合约地址、ABI详细信息及代币详情请参阅`references/myriad.md`。

### 调用任何合约
```bash
# Read
node scripts/call-contract.js --address 0x... --abi ./abi.json --function balanceOf --args 0x1234

# Write
export WALLET_PRIVATE_KEY=0x...
node scripts/call-contract.js --address 0x... --abi ./abi.json --function transfer --args 0x1234,100 --write
```

### 创造NFT
```bash
# Deploy SimpleNFT.sol first, then mint
export WALLET_PRIVATE_KEY=0x...

# Mint to existing contract
node scripts/mint-nft.js --contract 0x... --image QmIPFShash --to 0xRecipient --name "My NFT"
```

基本NFT合约模板请参阅`references/SimpleNFT.sol`。

### USDC操作
```bash
# Check USDC balance
node scripts/usdc-ops.js balance <wallet>

# Transfer USDC
export WALLET_PRIVATE_KEY=0x...
node scripts/usdc-ops.js transfer <to> <amount>

# Approve spender
node scripts/usdc-ops.js approve <spender> <amount>

# Check allowance
node scripts/usdc-ops.js allowance <owner> <spender>
```

### 估算Gas费用
```bash
# Get current gas prices
node scripts/estimate-gas.js

# Estimate transfer cost
node scripts/estimate-gas.js transfer <to> <amount>

# Estimate deployment cost
node scripts/estimate-gas.js deploy <bytecodeSize>
```

### 监控事件
```bash
# Watch new blocks
node scripts/watch-events.js blocks

# Watch ETH transfers to/from wallet
node scripts/watch-events.js transfers <wallet>

# Watch ERC20 transfers
node scripts/watch-events.js erc20 <token> <wallet>

# Watch contract events
node scripts/watch-events.js contract <address>
```

### 设置测试网
```bash
# Get faucet instructions
node scripts/testnet-setup.js faucet

# Check testnet balance
node scripts/testnet-setup.js check <wallet>

# Verify testnet setup
node scripts/testnet-setup.js verify <wallet>
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
| Kona路由器地址 | `0x441E0627Db5173Da098De86b734d136b27925250` |
| Uniswap V2路由器地址 | `0xad1eCa41E6F772bE3cb5A48A6141f9bcc1AF9F7c` |
| Myriad预测市场合约地址 | `0x3e0F5F8F5Fb043aBFA475C0308417Bf72c463289` |
| Myriad PTS代币地址 | `0x0b07cf011B6e2b7E0803b892d97f751659940F23` |
| Myriad API | `https://api-v2.myriadprotocol.com` |

## 脚本

| 脚本 | 用途 |
|--------|---------|
| `quick-start.js` | **从这里开始**——部署指南及健康检查 |
| `create-agw.js` | 创建Abstract全局钱包（可赚取XP） |
| `check-balances.js` | 查看ETH和代币余额 |
| `relay-bridge.js` | 从其他链桥接ETH到Abstract |
| `bridge-usdc-relay.js` | 通过Relay API桥接USDC |
| `deploy-abstract.js` | 在Abstract上部署合约（包含验证步骤） |
| `verify-contract.js | 验证合约的字节码（安全检查） |
| `transfer.js` | 发送ETH或代币 |
| `usdc-ops.js | USDC转账、授权等操作 |
| `swap-tokens.js` | 通过DEX交换代币 |
| `swap-kona.js` | 在Kona Finance上进行代币交换（V2版本） |
| `swap-aborean.js` | 在Aborean平台上进行代币交换（Velodrome风格） |
| `swap-uniswap-v2.js` | 在Uniswap V2上进行代币交换 |
| `myriad-trade.js` | 列出市场信息（通过Myriad API） |
| `myriad-buy-direct.js` | 在Myriad平台上直接下注（链上交易） |
| `call-contract.js | 调用任何合约函数 |
| `mint-nft.js` | 向现有合约创建NFT |
| `estimate-gas.js | 交易前估算Gas费用 |
| `watch-events.js` | 实时监控链上事件 |
| `testnet-setup.js | 设置并验证测试网访问权限 |

## 参考资料

| 文件 | 内容 |
|------|----------|
| `agw.md` | Abstract全局钱包使用指南（包括XP获取方法） |
| `dex.md` | DEX合约及交换规则（Kona、Aborean平台） |
| `myriad.md` | Myriad预测市场相关合约、ABI及交易信息 |
| `hardhat.config.js` | 适用于Abstract的Hardhat配置文件 |
| `addresses.md` | 重要合约地址列表 |
| `troubleshooting.md | 常见问题及解决方法 |
| `SimpleNFT.sol` | 基本NFT合约模板 |

## ⚠️ 重要提示：合约部署
Abstract基于zkSync技术，因此标准的EVM部署方法不适用。

### 可以使用的部署方法 ✅
```javascript
// Use zksync-ethers (NOT viem, NOT standard ethers)
const { ContractFactory } = require("zksync-ethers");
const factory = new ContractFactory(abi, bytecode, wallet);
const contract = await factory.deploy(args);

// ALWAYS verify bytecode after deploy
const code = await provider.getCode(address);
if (code === '0x') throw new Error("Deploy failed!");
```

### 不推荐的方法 ❌
```javascript
// DON'T use viem's deployContract
await walletClient.deployContract({...}); // Returns success but NO BYTECODE

// DON'T use standard ethers ContractFactory
// DON'T trust transaction success alone
```

### 部署检查清单：
- [ ] 使用`zksolc`编译合约（而非标准版本的solc）
- [ ] 使用`zksync-ethers`作为合约工厂
- [ ] 部署后验证`eth_getCode`的值是否为`0x`
- [ ] 在发送代币前测试合约功能

## 常见问题及解决方法

1. **Gas费用估算失败** → 使用Hardhat工具，而非foundry-zksync
2. **编译错误** → 使用Solidity 0.8.x版本并配合zksolc编译
3. **交易失败** → 检查Gas费用，并在abscan.org上验证交易结果
4. **合约部署成功但无字节码** → 使用`zksync-ethers`进行部署
5. **代币被发送到空地址** → 请务必先验证合约的字节码！

详细解决方案请参阅`references/troubleshooting.md`。

## 依赖项
```bash
# Core dependencies
npm install ethers zksync-ethers viem

# For contract deployment
npm install @matterlabs/hardhat-zksync

# For AGW (Abstract Global Wallet) - PIN THE VERSION!
# Different versions compute different AGW addresses
npm install @abstract-foundation/agw-client@1.10.0
```

**⚠️ agw-client版本警告：** 新版本可能使用不同的合约工厂，导致相同的EOA生成不同的AGW地址。如果更换版本，请在转账前确认AGW地址是否发生变化！
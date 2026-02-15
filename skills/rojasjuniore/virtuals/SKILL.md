---
name: virtuals
version: 1.0.0
description: "OpenClaw的Virtuals Protocol集成：在Base平台上创建、管理和交易token化的AI代理。"
metadata: {"openclaw": {"emoji": "🎭", "homepage": "https://virtuals.io"}}
---

# Virtuals Protocol 技能 🎭  
在 Virtuals Protocol（基础 L2 层）上创建、管理和交易代币化的 AI 代理。  

## 主要功能  
- 📊 **查看代理列表** - 浏览 Virtuals 上的热门 AI 代理  
- 💰 **查询价格** - 获取代理代币的价格和市场数据  
- 🔍 **代理详情** - 查看代理信息、持有者及交易记录  
- 🚀 **创建代理** - 发布你自己的代币化 AI 代理  
- 💸 **交易** - 买卖代理代币  

## 安装  
```bash
clawhub install virtuals
cd ~/.openclaw/skills/virtuals
npm install && npm run build && npm link
```  

## 快速入门  
```bash
# Check $VIRTUAL price
virtuals price

# List top agents
virtuals agents list

# Get agent details
virtuals agents info <agent-name>

# Check your balance
virtuals balance <wallet-address>
```  

## 命令  
### 市场数据  
```bash
virtuals price                    # $VIRTUAL price and market cap
virtuals agents list [--top 10]   # List top agents by market cap
virtuals agents trending          # Trending agents (24h volume)
```  

### 代理信息  
```bash
virtuals agents info <name>       # Agent details
virtuals agents holders <name>    # Top holders
virtuals agents trades <name>     # Recent trades
```  

### 钱包  
```bash
virtuals balance <address>        # Check $VIRTUAL balance
virtuals portfolio <address>      # All agent tokens held
```  

### 创建代理（需资金）  
```bash
virtuals create --name "MyAgent" --ticker "AGENT" --description "..."
```  

### 交易（需资金）  
```bash
virtuals buy <agent> <amount>     # Buy agent tokens
virtuals sell <agent> <amount>    # Sell agent tokens
```  

## 配置  
设置用于交易的钱包：  
```bash
virtuals config --wallet <address> --private-key <key>
```  

**⚠️ 目前仅支持测试网（TESTNET）——请勿使用主网资金。**  

## 架构  
```
┌─────────────────────────────────────┐
│         virtuals CLI                │
├─────────────────────────────────────┤
│  @virtuals-protocol/game SDK        │
│  + ethers.js (Base L2)              │
├─────────────────────────────────────┤
│  Virtuals Protocol Contracts        │
│  • VIRTUAL Token                    │
│  • Agent Factory                    │
│  • Bonding Curves                   │
│  • Uniswap V2 Pools                 │
└─────────────────────────────────────┘
```  

## 合同地址（基础）  
| 合同 | 地址 |  
|---------|---------|  
| $VIRTUAL | `0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b` |  

## 资源  
- Virtuals 应用程序：https://app.virtuals.io  
- Fun（用于创建代理）：https://fun.virtuals.io  
- 白皮书：https://whitepaper.virtuals.io  
- GAME SDK：https://github.com/game-by-virtuals/game-node  

## 许可证  
MIT  

---

**由 IntechChain 为 OpenClaw 开发 🦞**
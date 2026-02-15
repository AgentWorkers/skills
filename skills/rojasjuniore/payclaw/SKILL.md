---
name: payclaw
version: 1.0.0
description: "**代理之间的 USDC 支付功能**  
支持创建钱包、发送/接收支付请求，以及实现代理之间的资金托管。该功能专为 Moltbook 平台上的 USDC 霸客赛（USDC Hackathon）而开发。"
metadata: {"openclaw": {"emoji": "💸", "homepage": "https://github.com/rojasjuniore/payclaw"}}
---

# PayClaw 💸  
OpenClaw的代理间USDC支付解决方案。  
专为Moltbook上的USDC黑客马拉松项目开发。  

## 功能介绍  
PayClaw允许任何OpenClaw代理：  
- 🏦 创建USDC钱包（由Circle管理的开发者控制型钱包）  
- 💰 接收来自其他代理或用户的付款  
- 💸 向任何钱包地址发送付款  
- 🤝 在代理之间进行资金托管，以实现无信任交易  
- 🔗 支持Arc Testnet（Circle的原生USDC Layer-1网络）  

## 重要性  
代理在执行任务时需要资金支持。  
目前，如果代理需要：  
- 支付API调用费用  
- 雇佣其他代理  
- 收到任务报酬  
- 为交易托管资金……  
这些操作都缺乏便捷的解决方案。PayClaw正是为解决这些问题而设计的。  

## 安装  
```bash
clawhub install payclaw
cd ~/.openclaw/skills/payclaw
npm install && npm run build && npm link
```  

## 设置  
```bash
# Configure with Circle API key
payclaw setup --api-key YOUR_CIRCLE_API_KEY

# Create your agent's wallet
payclaw wallet create "MyAgent"

# Get testnet USDC
payclaw faucet
```  

## 命令  
### 钱包管理  
```bash
payclaw wallet create [name]     # Create new wallet
payclaw wallet list              # List all wallets
payclaw wallet balance           # Check balance
payclaw wallet address           # Show wallet address
```  

### 支付  
```bash
payclaw pay <address> <amount>   # Send USDC
payclaw request <amount> [memo]  # Generate payment request
payclaw history                  # Transaction history
```  

### 资金托管（代理间）  
```bash
payclaw escrow create <amount> <recipient> [--condition "task completed"]
payclaw escrow list              # List active escrows
payclaw escrow release <id>      # Release funds to recipient
payclaw escrow refund <id>       # Refund to sender
```  

### 代理发现  
```bash
payclaw agents list              # List agents with PayClaw wallets
payclaw agents find <name>       # Find agent's wallet address
payclaw agents register          # Register your agent in directory
```  

## 使用示例  
### 向其他代理付款  
```bash
# Find agent's wallet
payclaw agents find "DataBot"
# Output: 0x1234...5678

# Send payment
payclaw pay 0x1234...5678 10 --memo "For data analysis task"
# Output: ✅ Sent 10 USDC to DataBot (0x1234...)
#         TX: 0xabc...def
```  

### 为任务创建资金托管  
```bash
# Client creates escrow
payclaw escrow create 50 0xFreelancerWallet --condition "Deliver logo design"
# Output: 🔒 Escrow created: ESC-001
#         Amount: 50 USDC
#         Recipient: 0xFreelancer...
#         Condition: Deliver logo design

# After task completion, client releases
payclaw escrow release ESC-001
# Output: ✅ Released 50 USDC to 0xFreelancer...
```  

### 接收付款  
```bash
# Generate payment request
payclaw request 25 --memo "API access for 1 month"
# Output: 💰 Payment Request
#         To: 0xYourWallet...
#         Amount: 25 USDC
#         Memo: API access for 1 month
#         
#         Share this with payer:
#         payclaw pay 0xYourWallet 25 --memo "API access for 1 month"
```  

## 代理集成  
```typescript
// In your OpenClaw skill
import { PayClaw } from 'payclaw';

const payclaw = new PayClaw();

// Check if payment received
const balance = await payclaw.getBalance();

// Send payment
await payclaw.send('0x...', 10, 'For task completion');

// Create escrow
const escrow = await payclaw.createEscrow(50, '0x...', 'Task condition');
```  

## 支持的区块链  
- **Arc Testnet**（默认）：Circle的原生USDC Layer-1网络  
- Base Sepolia  
- Polygon Amoy  
- Ethereum Sepolia  

## 安全性  
- 私钥不会离开Circle的基础设施  
- 通过Circle Gas Station实现零费用交易  
- 仅限黑客马拉松环境使用（不涉及真实资金）  

## 架构  
```
┌─────────────────┐     ┌─────────────────┐
│  OpenClaw Agent │────▶│    PayClaw      │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  Circle Wallets │
                        │    (Testnet)    │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Arc Testnet   │
                        │     (USDC)      │
                        └─────────────────┘
```  

## 黑客马拉松相关信息  
**最佳OpenClaw技能**：该功能为OpenClaw代理添加了原生USDC支付能力，开启了全新的代理间交易模式。  

## 链接  
- GitHub：https://github.com/rojasjuniore/payclaw  
- Moltbook：https://moltbook.com/u/JuniorClaw  
- 开发者：IntechChain  

## 许可证  
MIT许可证  

---

**专为Moltbook上的OpenClaw USDC黑客马拉松项目开发 💵**
# 组合投资风险与优化分析器

**基于人工智能的加密货币投资组合风险分析工具，支持自动将费用兑换为$BANKR代币进行回购。**

## 概述

加密货币交易者在风险管理方面表现不佳。本工具具备以下功能：
- 🔍 实时扫描用户钱包中的资产
- 📊 分析投资组合的构成（包括DeFi产品、山寨币、稳定币、NFT等）
- ⚠️ 进行压力测试和情景分析
- 💡 提出再平衡和对冲建议
- 🎙️ 通过电话语音指令进行操作
- 💰 通过将收集到的费用兑换为$BANKR代币来实现自我盈利

## 盈利模式

**费用收取方式：**
- **一次性扫描费用：** 5美元（ETH/USDC）
- **月度订阅费：** 20美元/月（可无限次扫描）
- **$BANKR持有者免费**（持有量≥1000枚代币）

**自动回购机制：**
- 所有收取的费用将100%用于通过Uniswap交易所将用户持有的代币兑换为$BANKR
- 这种机制持续为$BANKR创造购买压力
- 购买到的$BANKR代币将被销毁或分配给参与质押的用户

**代币地址：**
- $BANKR: `0x50D2280441372486BeecdD328c1854743EBaCb07`（Base/Polygon区块链）

## 主要功能

### 1. 实时投资组合扫描
- 支持多条区块链（Ethereum、Base、Polygon、Arbitrum、Optimism）
- 显示代币余额和价值
- 公示DeFi产品中的投资情况（如Aave、Compound、Uniswap的LP合约）
- 显示NFT持有情况及其最低交易价格
- 显示用户的质押状态

### 2. 风险分析
- **资产类别分布：**
  - 稳定币：X%
  - 优质资产（ETH、BTC）：X%
  - DeFi代币：X%
  - 山寨币：X%
  
- **协议风险：**
  - 智能合约的风险评分
  - 合同的审计状态
  - 资产的锁定价值（TVL）和合约年龄

- **集中度风险：**
  - 最大的5个投资资产
  - 投资组合的多元化程度（0-100分）

- **非永久性损失风险：**
  - 计算LP合约的潜在损失
  - 提供历史损失数据

### 3. 压力测试
- **市场暴跌情景模拟：**
  - 市场价格下跌20%、50%、80%
  - 分析资产之间的相关性

- **清算风险：**
  - 检查用户的抵押品比例
  - 评估可能的清算价格

- **交易费用影响：**
  - 在高交易费用环境下分析退出成本

### 4. 优化建议
- 提供再平衡建议
- 制定对冲策略
- 优化投资回报
- 帮助用户把握税收优惠时机

### 5. 语音交互界面
- 通过电话调用分析工具：
  - 询问：“我的投资组合风险有多大？”
  - 询问：“我最主要的资产风险是什么？”
  - 询问：“我需要重新平衡投资组合吗？”
  - 询问：“我有被清算的风险吗？”

## 先决条件

### 1. 节点提供商
需要设置RPC（Remote Procedure Call）端点：
```bash
export ETHEREUM_RPC="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"
export BASE_RPC="https://base-mainnet.g.alchemy.com/v2/YOUR_KEY"
export POLYGON_RPC="https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY"
```

### 2. 数据接口
需要接入相关的数据API：
```bash
export COINGECKO_API_KEY="your_key"
export DEFILLAMA_API_KEY="your_key"  # Optional, has public tier
export OPENSEA_API_KEY="your_key"    # For NFT data
```

### 3. 支付钱包
用于接收费用并执行回购操作：
```bash
export PAYMENT_WALLET_KEY="your_private_key"
```

### 4. Twilio（用于语音交互）
需要配置Twilio服务：
```bash
export TWILIO_ACCOUNT_SID="your_sid"
export TWILIO_AUTH_TOKEN="your_token"
export TWILIO_PHONE_NUMBER="+1234567890"
```

## 快速入门

### 安装
按照文档中的步骤进行安装：
```bash
clawdhub install portfolio-risk-analyzer
cd skills/portfolio-risk-analyzer
npm install  # Install dependencies
```

### 配置
创建`.env`配置文件：
```bash
# RPC Endpoints
ETHEREUM_RPC=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
BASE_RPC=https://base-mainnet.g.alchemy.com/v2/YOUR_KEY
POLYGON_RPC=https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY

# APIs
COINGECKO_API_KEY=your_key
DEFILLAMA_API_KEY=your_key
OPENSEA_API_KEY=your_key

# Payment & Buyback
PAYMENT_WALLET_ADDRESS=0xYourAddress
PAYMENT_WALLET_KEY=your_private_key
BANKR_TOKEN=0x50D2280441372486BeecdD328c1854743EBaCb07
UNISWAP_ROUTER=0x... # Uniswap V3 router address

# Voice
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
```

### 分析钱包
使用指定命令分析钱包：
```bash
./scripts/analyze-wallet.sh 0xYourWalletAddress
```

### 启用支付功能
配置支付网关：
```bash
./scripts/payment-server.sh
# Listens on port 3000 for payment webhooks
```

### 启动语音交互机器人
启动语音交互服务：
```bash
./scripts/voice-bot.sh
# Users call your Twilio number
```

## 核心脚本

### `analyze-wallet.sh` - 全面投资组合分析
执行全面的投资组合分析：
```bash
./scripts/analyze-wallet.sh <wallet_address> [--chain ethereum|base|polygon|all]
```

**输出结果：**
- 资产构成分析
- 风险评分
- 投资建议

**示例：**
```bash
./scripts/analyze-wallet.sh 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
```

### `check-payment.sh` - 验证支付
验证用户是否已支付费用，并检查用户是否持有$BANKR代币以获得免费使用权限：
```bash
./scripts/check-payment.sh <tx_hash>
```

### `execute-buyback.sh` - 将费用兑换为$BANKR
自动将收集到的费用通过Uniswap交易所兑换为$BANKR：
```bash
./scripts/execute-buyback.sh <amount_usdc>
```

### `stress-test.sh` - 运行压力测试
模拟市场暴跌情景：
```bash
./scripts/stress-test.sh <wallet_address> --scenario crash|liquidation|gas
```

### `optimize.sh` - 生成优化建议
根据分析结果生成投资优化建议：
```bash
./scripts/optimize.sh <wallet_address>
```

## 支付流程

### 1. 用户请求处理
接收用户的分析请求：
```bash
curl -X POST https://your-domain.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "payment_tx": "0x123abc..."
  }'
```

### 2. 验证支付
验证用户是否已支付费用：
```javascript
// Check if user paid or holds BANKR
const bankrBalance = await getBankrBalance(wallet);
const hasPaid = await verifyPaymentTx(payment_tx);

if (bankrBalance >= 1000 || hasPaid) {
  // Run analysis
} else {
  return { error: "Payment required" };
}
```

### 3. 分析投资组合
执行投资组合分析：
```javascript
const analysis = await analyzePortfolio(wallet);
return analysis;
```

### 4. 自动回购
根据分析结果自动执行回购操作：
```javascript
// Every hour or when fees > $100
if (collectedFees > 100) {
  await executeUniswapBuyback(collectedFees, BANKR_TOKEN);
}
```

## 风险评分算法

### 投资组合风险评分（0-100分）
```javascript
const riskScore = 
  (concentrationRisk * 0.3) +
  (volatilityRisk * 0.3) +
  (liquidationRisk * 0.2) +
  (protocolRisk * 0.2);
```

**评分依据：**
- **集中度风险**：前3大资产所占的比例
- **波动性风险**：基于资产价格的波动性
- **清算风险**：用户是否接近被清算的临界点
- **协议风险**：智能合约的风险评分

### 风险等级
- **0-20分**：🟢 低风险（保守型）
- **21-40分**：🟡 低风险-中等
- **41-60分**：🟠 中等风险
- **61-80分**：🟠 高风险
- **81-100分**：⚫ 极高风险

## 优化建议

### 再平衡建议
根据分析结果提供再平衡建议：
```javascript
// If memecoin exposure > 30%
if (memecoins / totalValue > 0.3) {
  suggest("Reduce memecoin exposure to 15%");
  suggest("Move profits to ETH or stablecoins");
}

// If no stablecoins
if (stablecoins / totalValue < 0.1) {
  suggest("Add 10-20% stablecoin buffer");
}

// If single asset > 50%
if (largestHolding > 0.5) {
  suggest("Diversify: no single asset > 30%");
}
```

### 对冲策略
制定相应的对冲策略：
```javascript
// If long-only crypto portfolio
suggest("Consider shorting BTC perpetuals for downside protection");

// If large LP positions
suggest("Hedge IL with options or reduce LP size");
```

### 收益优化
优化投资组合的收益表现：
```javascript
// Find best yields
const aaveYield = await getAaveRate("USDC");
const compoundYield = await getCompoundRate("USDC");

if (stablecoinBalance > 1000 && max(aaveYield, compoundYield) > 5) {
  suggest(`Deposit stables in ${aaveYield > compoundYield ? 'Aave' : 'Compound'} for ${Math.max(aaveYield, compoundYield)}% APY`);
}
```

## 语音交互机器人集成

### 使用流程
1. 用户拨打Twilio提供的电话号码
2. 语音交互系统提示用户提供钱包地址或ENS名称
3. 系统验证钱包信息
4. 检查用户是否已支付费用及持有$BANKR代币
5. 如果验证通过，开始分析投资组合
6. 通过电话向用户反馈分析结果
7. 可通过短信或电子邮件发送详细报告

### 语音指令示例
- “分析我的投资组合”
- “我的风险评分是多少？”
- “我是否有被清算的风险？”
- “我需要重新平衡投资组合吗？”
- “我最主要的资产是什么？”

### 示例脚本
展示如何使用这些语音指令：
```javascript
// voice-bot.js
const VoiceResponse = require('twilio').twiml.VoiceResponse;

app.post('/voice', async (req, res) => {
  const twiml = new VoiceResponse();
  
  twiml.say("Welcome to Portfolio Risk Analyzer. Please say your wallet address.");
  
  const gather = twiml.gather({
    input: 'speech',
    action: '/analyze'
  });
  
  res.type('text/xml');
  res.send(twiml.toString());
});

app.post('/analyze', async (req, res) => {
  const wallet = req.body.SpeechResult;
  
  // Verify payment or BANKR holding
  const hasAccess = await checkAccess(wallet);
  
  if (!hasAccess) {
    twiml.say("Payment required. Send $5 USDC to our wallet, then call back.");
    return res.send(twiml.toString());
  }
  
  // Run analysis
  const analysis = await analyzePortfolio(wallet);
  
  twiml.say(`Your portfolio risk score is ${analysis.riskScore} out of 100.`);
  twiml.say(`You have ${analysis.summary.concentrationRisk}% concentration risk.`);
  twiml.say(analysis.recommendations.join('. '));
  
  res.send(twiml.toString());
});
```

## API接口

### `/api/analyze`  
用于分析用户的投资组合：
```json
{
  "wallet": "0x742d35Cc...",
  "payment_tx": "0x123abc...",
  "chain": "ethereum"
}
```

**请求格式：**
```json
{
  "wallet": "0x742d35Cc...",
  "payment_tx": "0x123abc...",
  "chain": "ethereum"
}
```

**响应格式：**
```json
{
  "wallet": "0x742d35Cc...",
  "riskScore": 65,
  "totalValue": 125000,
  "breakdown": {
    "stablecoins": 15000,
    "bluechips": 50000,
    "defi": 30000,
    "memecoins": 25000,
    "nfts": 5000
  },
  "exposures": {
    "ethereum": 45,
    "uniswap": 20,
    "shib": 15
  },
  "risks": {
    "concentration": 65,
    "volatility": 70,
    "liquidation": 20,
    "protocol": 30
  },
  "recommendations": [
    "Reduce memecoin exposure from 20% to 10%",
    "Add 15% stablecoin buffer",
    "Diversify: SHIB is 15% of portfolio"
  ]
}
```

### `/api/payment/verify`  
用于验证用户的支付交易：
```json
{
  "tx_hash": "0x123abc...",
  "amount": 5
}
```

**请求格式：**
```json
{
  "tx_hash": "0x123abc...",
  "amount": 5
}
```

**响应格式：**
```json
{
  "valid": true,
  "amount_paid": 5.0,
  "from": "0x742d35Cc...",
  "timestamp": 1706805600
}
```

### `/api/buyback/execute`  
用于触发手动回购操作（仅限管理员使用）：
```json
{
  "admin_key": "secret",
  "amount": 100
}
```

**请求格式：**
```json
{
  "admin_key": "secret",
  "amount": 100
}
```

**响应格式：**
```json
{
  "success": true,
  "tx_hash": "0xabc123...",
  "bankr_bought": 12500,
  "price": 0.008
}
```

## 智能合约（可选）
用于在链上验证支付信息：
```solidity
// PaymentGate.sol
contract PaymentGate {
    address public owner;
    address public bankrToken = 0x50D2280441372486BeecdD328c1854743EBaCb07;
    uint256 public scanPrice = 5e6; // $5 USDC
    
    mapping(address => uint256) public lastScan;
    mapping(address => bool) public hasLifetime;
    
    event PaymentReceived(address indexed user, uint256 amount);
    event BuybackExecuted(uint256 usdcAmount, uint256 bankrAmount);
    
    function payScan() external payable {
        require(msg.value >= scanPrice, "Insufficient payment");
        lastScan[msg.sender] = block.timestamp;
        emit PaymentReceived(msg.sender, msg.value);
        
        // Auto-buyback via Uniswap
        _executeBuyback(msg.value);
    }
    
    function hasAccess(address user) public view returns (bool) {
        // Free if holds 1000+ BANKR
        if (IERC20(bankrToken).balanceOf(user) >= 1000e18) {
            return true;
        }
        
        // Or paid within last 30 days
        if (block.timestamp - lastScan[user] < 30 days) {
            return true;
        }
        
        return false;
    }
    
    function _executeBuyback(uint256 amount) internal {
        // Swap USDC → BANKR via Uniswap
        // Send to burn address or distribute to stakers
    }
}
```

## 部署流程

### 1. 部署支付相关合约（可选）
部署用于处理支付的智能合约：
```bash
npx hardhat run scripts/deploy.js --network base
```

### 2. 启动API服务器
配置API服务器：
```bash
node server.js
# Runs on port 3000
```

### 3. 注册域名
设置项目的官方网站域名：
```bash
# Point your domain to the server
# Set up SSL with Let's Encrypt

certbot --nginx -d analyzer.yourdomain.com
```

### 4. 设置自动回购任务
设置定期执行回购的定时任务：
```bash
# Add to crontab
0 * * * * cd /path/to/skill && ./scripts/execute-buyback.sh
```

### 5. 监控系统运行
持续监控系统的运行状态：
```bash
# Check collected fees
./scripts/check-balance.sh

# View buyback history
./scripts/buyback-history.sh
```

## 定价方案

### 免费套餐
- **条件：** 持有至少1000枚$BANKR代币（约8美元，单价0.008美元/枚）
- **权益：** 无限次扫描投资组合

### 按次付费
- **费用：** 每次扫描5美元
- **支付方式：** ETH、USDC或USDT
- **有效期：** 24小时

### 月度订阅
- **费用：** 20美元/月
- **支付方式：** 加密货币或法定货币
- **权益：** 无限次扫描投资组合
- **额外福利：** 可提前使用新功能

## 代币持有者的额外权益

**持有1000枚以上$BANKR代币：**
- ✅ 免费无限次扫描投资组合
- ✅ 优先使用语音交互机器人
- ✅ 享受高级分析服务
- ✅ 可访问API接口

**持有10,000枚以上$BANKR代币：**
- ✅ 享受上述所有权益
- ✅ 使用自定义风险模型
- ✅ 获得投资组合优化建议
- ✅ 分享回购收益（按比例）

## 示例使用场景

### 使用场景1：DeFi投资者
```bash
# Scan portfolio
./scripts/analyze-wallet.sh 0xDeFiFarmer

# Check IL on LP positions
./scripts/check-il.sh 0xDeFiFarmer --pool USDC-ETH

# Optimize yield
./scripts/optimize.sh 0xDeFiFarmer --focus yield
```

### 使用场景2：山寨币投资者
```bash
# Full risk assessment
./scripts/analyze-wallet.sh 0xDegenApe

# Stress test: what if memecoins dump 80%?
./scripts/stress-test.sh 0xDegenApe --scenario crash --drop 80

# Get rebalancing advice
./scripts/optimize.sh 0xDegenApe --focus risk
```

### 使用场景3：机构投资者
```bash
# Multi-wallet analysis
./scripts/analyze-institution.sh wallets.txt

# Generate PDF report
./scripts/generate-report.sh 0xInstitution --format pdf

# Set up alerts
./scripts/alert.sh 0xInstitution --liquidation-risk > 50 --notify webhook
```

## 回购机制

### 收益来源
说明平台的收入来源：
```javascript
// Track all payments
let totalRevenue = 0;

app.post('/api/analyze', async (req, res) => {
  const payment = await verifyPayment(req.body.payment_tx);
  
  if (payment.valid) {
    totalRevenue += payment.amount;
    await saveToDatabase({ user: req.body.wallet, amount: payment.amount });
  }
});
```

### 自动回购触发机制
描述自动回购的触发条件：
```javascript
// Run every hour
setInterval(async () => {
  const balance = await getUSDCBalance(PAYMENT_WALLET_ADDRESS);
  
  if (balance >= 100) {
    console.log(`Executing buyback: $${balance} USDC → BANKR`);
    
    const tx = await executeUniswapSwap({
      from: 'USDC',
      to: BANKR_TOKEN,
      amount: balance,
      slippage: 1
    });
    
    console.log(`Bought ${tx.amountOut} BANKR at ${tx.price}`);
    
    // Optional: Burn or distribute
    await burnOrDistribute(tx.amountOut);
  }
}, 60 * 60 * 1000); // Every hour
```

### 回购监控面板
提供回购操作的实时监控信息：
```bash
./scripts/buyback-stats.sh

# Output:
# Total Revenue: $5,420
# Total BANKR Bought: 677,500 tokens
# Average Price: $0.008
# Buy Pressure: +$5.4k
# Holders Benefited: 127 wallets
```

## 营销策略

### 发布计划
- **免费测试阶段**（2周）：
  - 提高产品知名度
  - 收集用户反馈

- **正式上线**：
  - 在Twitter上发布公告
  - 公布首次回购的统计数据

- **推荐计划**：
  - 为推荐新用户提供10%的$BANKR代币作为佣金
  - 采用传销式的奖励机制

### 营销宣传语
- “AI机器人利用盈利来回购自己的代币 🤖💰”
- “支付5美元，即可获得投资组合分析服务并增加对$BANKR代币的购买力”
- “持有1000枚代币，即可终身免费使用该工具”

### 社区激励措施
- 每月向顶级用户发放代币奖励
- 开设抽奖活动，赢取免费一年的订阅资格
- 设立排行榜，奖励优化投资组合表现最佳的用户

## 开发计划

### 第一阶段（MVP阶段，第1-2周）：
- ✅ 基本的投资组合扫描功能
- ✅ 风险评分系统
- ✅ 支付功能
- ✅ 自动回购机制

### 第二阶段（进阶阶段，第3-4周）：
- 语音交互机器人集成
- 支持更多区块链
- 加强压力测试功能
- 增加NFT分析功能

### 第三阶段（扩展阶段，第2个月）：
- 开放API接口，支持第三方集成
- 推出移动应用
- 为机构用户提供专属服务
- 为代币持有者分配收益

## 技术支持
- 社交媒体：[@KellyClaudeAI](https://twitter.com/KellyClaudeAI)
- 项目GitHub仓库：[portfolio-risk-analyzer](https://github.com/kellyclaudeai/portfolio-risk-analyzer)
- 社交媒体群组：[加入社区](https://discord.gg/bankrbot)

## 许可证
本项目采用MIT许可证发布

## 开发者信息
由Kelly Claude（AI开发团队）开发
基于$BANKR代币运行
在ClawdHub平台上发布

---

**准备好分析您的投资组合并使用$BANKR代币进行回购了吗？**

```bash
clawdhub install portfolio-risk-analyzer
```

将用户支付的费用转化为对$BANKR的购买力，帮助用户成为平台的长期持有者吧！🚀
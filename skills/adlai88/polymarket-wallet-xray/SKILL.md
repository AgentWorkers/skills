---
name: polymarket-wallet-xray
displayName: Polymarket Wallet X-Ray
description: 可以对任何 Polymarket 钱包进行详细分析：包括用户的技能水平、交易质量、是否存在机器人（bot）参与交易的情况，以及进行深入的数据挖掘（edge analysis）。该功能通过查询 Polymarket 的公开 API 来实现，无需任何身份验证。这一功能的灵感来源于 @thejayden 的分析报告《对 Polymarket 上大额交易用户的深入剖析》（“Autopsy of a Polymarket Whale”）。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":[],"pip":[]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
inspired_by:
  - thejayden (@thejayden) - "Autopsy: How to Read the Mind of a Polymarket Whale"
version: "1.0.0"
published: true
---
# Polymarket钱包分析工具（X-Ray）

该工具可分析任何Polymarket钱包的交易模式、交易者的技能水平以及其交易策略中的“优势”（即相对于市场的竞争优势）。

**无需身份验证**。该工具直接通过Polymarket的公开CLOB API进行数据查询。

**灵感来源：** [@thejayden](https://x.com/thejayden) 的文章《The Autopsy: How to Read the Mind of a Polymarket Whale》（https://x.com/thejayden/status/2020891572389224878）

> 该工具实现了[@thejayden]开发的交易分析框架。建议阅读原文，以了解“Time Profitable”指标、对冲策略检查、机器人检测以及交易信号识别等功能的背后原理。

> **请注意：** 这只是一个分析工具，并非交易信号生成器。它为任何Polymarket钱包提供详细的交易数据，帮助用户理解交易者的行为模式，从而做出更明智的决策。该工具仅用于教育和研究目的，不可用于盲目复制交易行为。

## ⚠️ 重要免责声明

**过去的表现并不能保证未来的结果。** 财户的历史数据仅能反映：
- 用户过去的交易情况
- 用户的历史胜率和交易决策的质量
- 但不能预测其策略在未来是否依然有效

**盲目复制交易的风险：**
- 市场环境随时可能变化
- 交易者的“优势”可能源于运气、时机选择或特定历史事件
- 交易滑点和手续费会侵蚀这些“优势”
- 如果多个用户使用相同的策略，这些优势可能会被抵消

**使用建议：**
- 了解熟练交易者的特征（通过分析指标和行为）
- 识别潜在的异常行为（如机器人或套利者）
- 理解交易者的心理（如害怕错过机会（FOMO）与自律性）
- 为自身的交易策略提供参考

**禁止使用场景：**
- **禁止** 自动复制他人的交易行为
- **禁止** 期望复制他人的收益
- **禁止** 仅凭这些指标进行交易，而不了解其背后的逻辑
- **禁止** 在不理解交易模式的情况下投入大量资金

## 适用场景

- **了解熟练交易者的操作方式**：哪些指标能区分赢家和输家？
- **理解交易心理**：哪些交易者更注重价格追逐，哪些更有自律性？
- **检测异常行为**：识别可疑的交易模式（如机器人或套利行为）
- **研究套利机会**：寻找持有对冲头寸的账户
- **比较交易者表现**：了解稳定盈利的交易者与运气好的交易者的区别
- **辅助决策**：将分析结果作为决策的参考，而非直接的交易指令

## 快速操作命令

```bash
# Analyze a single wallet
python wallet_xray.py 0x1234...abcd

# Analyze wallet + only look at specific market
python wallet_xray.py 0x1234...abcd "Bitcoin"

# Compare two wallets head-to-head
python wallet_xray.py 0x1111... 0x2222... --compare

# Find wallets matching criteria (top Time Profitable in market)
python wallet_xray.py "Will BTC hit $100k?" --top-wallets 5 --dry-run

# Check your account status
python scripts/status.py
```

**使用的API（公开接口，无需认证）：**
- Gamma API：`https://gamma-api.polymarket.com` — 市场搜索
- CLOB API：`https://clob.polymarket.com` — 交易历史和订单簿

## 分析结果

该工具会返回以下详细的交易分析指标：

```json
{
  "wallet": "0x1234...abcd",
  "total_trades": 156,
  "total_period_hours": 42.5,
  "profitability": {
    "time_profitable_pct": 75.3,
    "win_rate_pct": 68.2,
    "avg_profit_per_win": 0.035,
    "avg_loss_per_loss": -0.018,
    "realized_pnl_usd": 2450.00
  },
  "entry_quality": {
    "avg_slippage_bps": 28,
    "quality_rating": "B+",
    "assessment": "Good entries, occasional FOMO"
  },
  "behavior": {
    "is_bot_detected": false,
    "trading_intensity": "high",
    "avg_seconds_between_trades": 45,
    "price_chasing": "moderate",
    "accumulation_signal": "growing"
  },
  "edge_detection": {
    "hedge_check_combined_avg": 0.98,
    "has_arbitrage_edge": false,
    "assessment": "No locked-in edge; relies on direction"
  },
  "risk_profile": {
    "max_drawdown_pct": 12.5,
    "volatility": "medium",
    "max_position_concentration": 0.22
  },
  "recommendation": "Good trader. Skilled entries, disciplined sizing. Good metrics for learning from. Not advice to copytrade."
}
```

## 工作原理

1. **获取交易历史**：通过Simmer API从Polymarket下载该钱包的所有交易记录
2. **计算盈利时间线**：分析用户何时处于亏损状态，何时盈利
3. **评估交易决策的质量**：判断用户是否在最佳价格买入
4. **检测交易模式**：区分人类交易者（有策略的交易）和机器人（快速交易）
5. **检查是否存在套利机会**：如果“买入”和“卖出”的平均价格差小于1美元，则可能存在无风险的套利机会
6. **分析交易行为**：判断用户是否存在害怕错过机会（FOMO）的行为，以及是否具备交易纪律
7. **提供使用建议**：判断该钱包是否值得关注，以及其中潜藏的风险

## 指标解释

### ⏱️ **Time Profitable**（例如：75.3%）
该钱包在75%的交易时间内处于盈利状态（未出现亏损）。仅经历了25%的亏损，显示出良好的交易纪律。

- **>80%**：表明交易者具有极高的交易技巧（精准的买入时机和良好的持有策略）
- **50-80%**：表示交易者有一定纪律性，但仍有提升空间
- **<50%**：提示交易策略存在风险，可能因恐慌性操作导致亏损

### 🎯 **Entry Quality**（例如：平均滑点28个基点）
用户通常在最佳价格附近买入。对于活跃的交易者来说，28个基点的滑点属于正常范围。没有迹象表明用户存在害怕错过机会（FOMO）的行为。

- **<20 bps**：表明用户非常专业，使用限价单进行交易。
- **20-40 bps**：表示交易者的操作速度和价格判断能力适中。
- **>50 bps**：表明用户可能过于追逐价格波动。

### 🤖 **Bot Detection**（例如：结果为“false”）
平均每次交易间隔45秒，属于人类交易者的行为。机器人的交易间隔通常小于1秒。

- **<5 sec**：很可能是机器人操作，除非确定对方是正规的市场做市商。
- **5-30 sec**：可能是机器人，但也有可能是人类交易者。
- **>30 sec**：肯定是人类交易者。

### 💰 **Hedge Check**（例如：综合得分0.98）
如果用户在价格0.70时买入，在价格0.30时卖出，那么他们的总收益应为1美元。这意味着他们的交易策略实现了无风险的套利。

- **< $0.95**：表明用户找到了套利机会（可能是机构投资者）。
- **$0.95-1.00**：表明存在微小的竞争优势。
- **> $1.00**：表示没有明显的竞争优势，用户可能是单纯基于价格走势进行交易。

## 使用示例

### **示例1：学习熟练交易者的交易策略**
```python
import subprocess
import json

# Analyze a wallet known for skilled trading
result = subprocess.run(
    ["python", "wallet_xray.py", "0x123...abc", "--json"],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)

# LEARN from their profile, don't copy blindly
time_prof = data["profitability"]["time_profitable_pct"]
entry_qual = data["entry_quality"]["quality_rating"]

print(f"📊 What this trader does well:")
print(f"  • Time Profitable: {time_prof}% (disciplined)")
print(f"  • Entry Quality: {entry_qual} (patient buyer)")
print(f"  • Behavior: {data['behavior']['accumulation_signal']} (not FOMO)")

# THEN: Ask yourself
# - Why are they profitable? (skill or luck?)
# - Can I replicate their decision-making process?
# - Do I have their capital size, timing, or information?
```

### **示例2：研究异常交易行为（用于教育目的）**
```python
# Analyze multiple wallets to understand patterns
wallets = ["0x111...", "0x222...", "0x333..."]

print("Comparing trader profiles:")
for wallet in wallets:
    result = subprocess.run(
        ["python", "wallet_xray.py", wallet, "--json"],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)

    is_bot = "🤖 BOT" if data["behavior"]["is_bot_detected"] else "👤 HUMAN"
    print(f"\n{wallet}: {is_bot}")
    print(f"  Win Rate: {data['profitability']['win_rate_pct']}%")
    print(f"  Time Profitable: {data['profitability']['time_profitable_pct']}%")

# Use this data to understand what successful trading LOOKS LIKE
# Then build your own strategy based on these insights
```

### **示例3：基于分析做出决策（而非盲目复制）**
```python
# Analyze before you decide what to do
result = subprocess.run(
    ["python", "wallet_xray.py", "0x123...abc", "--json"],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)

# Make an INFORMED decision based on analysis + YOUR OWN JUDGMENT
if data["profitability"]["time_profitable_pct"] > 75 and \
   data["entry_quality"]["quality_rating"] in ["A", "A+"]:

    print(f"✅ This wallet shows skill (high Time Profitable, good entries)")
    print(f"⚠️  But I will NOT copytrade blindly.")
    print(f"📋 Instead, I'll:")
    print(f"   1. Backtest their patterns on fresh data")
    print(f"   2. Add my own market signals")
    print(f"   3. Start with small position (1-2% of capital)")
    print(f"   4. Monitor for next 30 days")
    print(f"   5. Adjust if it stops working")
else:
    print(f"❌ This wallet doesn't show strong enough metrics.")
    print(f"   Safer to avoid or research further before deciding.")
```

## 运行该工具

- **分析单个钱包（默认设置）：**
```bash
python wallet_xray.py 0x1234...abcd
```

- **分析特定市场的钱包：**
```bash
python wallet_xray.py 0x1234...abcd "Bitcoin"
```

- **以JSON格式输出结果（适用于脚本）：**
```bash
python wallet_xray.py 0x1234...abcd --json
```

- **比较两个钱包的交易数据：**
```bash
python wallet_xray.py 0x1111... 0x2222... --compare
```

- **仅分析最近的交易数据（加快分析速度）：**
```bash
python wallet_xray.py 0x1234...abcd --limit 100
```

## 常见问题及解决方法

- **“钱包没有交易记录”**：该钱包尚未进行交易，或所有交易记录过于陈旧。请尝试使用活跃的交易账户。
- **“市场未找到”**：查询的市场在Polymarket系统中不存在。请尝试输入更具体的市场名称，或选择“全部市场”进行查询。
- **“分析耗时过长”**：对于交易记录超过500条的钱包，分析可能需要30秒以上。可以使用`--limit 100`参数仅分析最近的交易记录以加快速度。
- **“API请求次数过多”**：如果同时分析多个钱包，可能会导致请求限制。请稍后重试，或使用`--limit 50`参数减少每次请求的数量。
- **“连接错误”**：请确认Polymarket的CLOB API是否可用（可尝试访问`curl https://clob.polymarket.com/trades`）。如果API不可用，请稍后再试，或使用`--limit 50`参数减少请求次数。

## 致谢

该工具基于[@thejayden](https://x.com/thejayden)的《The Autopsy: How to Read the Mind of a Polymarket Whale》一文中的交易分析框架开发。原文介绍了如何：
- 识别虚假的交易专家（高盈亏比但交易决策糟糕）
- 检测机器人（通过分析交易速度）
- 发现套利机会（通过分析对冲头寸）
- 理解交易者的心理（如FOMO情绪和自律性）

此处使用的所有指标和分析方法均源自该文章。如果您觉得该工具有用，请阅读原文并关注[@thejayden](https://x.com/thejayden)的更多内容。

## 链接资源

- **Simmer API完整文档：** [simmer.markets/docs.md](https://simmer.markets/docs.md)
- **原始分析文章：** [The Autopsy: How to Read the Mind of a Polymarket Whale](https://x.com/thejayden/status/2020891572389224878)
- **仪表盘界面：** [simmer.markets/dashboard](https://simmer.markets/dashboard)
- **技术支持：** [Telegram频道：** [https://t.me/+m7sN0OLM_780M2Fl]
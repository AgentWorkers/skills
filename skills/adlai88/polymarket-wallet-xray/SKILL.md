---
name: polymarket-wallet-xray
displayName: Polymarket Wallet X-Ray
description: 可以对任何 Polymarket 钱包进行深度分析，包括其技能水平、交易质量、机器人交易行为（bot detection）以及市场趋势（edge analysis）。该工具通过查询 Polymarket 的公开 API 来获取数据，无需任何身份验证。该功能的灵感来源于 @thejayden 的分析报告《Polymarket 钱包的“解剖”》。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":[],"pip":[]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
inspired_by:
  - thejayden (@thejayden) - "Autopsy: How to Read the Mind of a Polymarket Whale"
version: "1.0.2"
published: true
---
# Polymarket钱包分析工具（X-Ray）

该工具可用于分析任何Polymarket钱包的交易模式、交易者的技能水平以及其交易策略中的“优势”（即相对于市场的竞争优势）。

**无需身份验证。**该工具直接通过Polymarket的公开CLOB API进行数据查询。

**灵感来源：** [@thejayden](https://x.com/thejayden) 的文章《The Autopsy: How to Read the Mind of a Polymarket Whale》（https://x.com/thejayden/status/2020891572389224878）

> 该工具实现了[@thejayden]开发的交易分析框架。建议阅读原文，以了解“Time Profitable”指标、对冲策略检查、机器人检测以及交易信号识别等功能的原理。

> **请注意：** 这只是一个分析工具，并非交易建议。它仅提供交易者的相关数据，供您了解交易者的行为模式并据此做出决策，而非用于盲目复制他们的交易行为。

## ⚠️ 重要免责声明

**过去的表现并不能保证未来的结果。** 财户的历史数据可以反映：
- ✅ 他们过去的交易情况
- ✅ 他们的历史胜率和交易决策质量
- ❌ 但无法预测他们的策略在未来是否依然有效

**盲目复制他人交易的风险：**
- 市场环境会不断变化
- 交易者的优势可能源于运气、时机选择或特定历史事件
- 交易滑点及费用可能会将微弱的优势侵蚀殆尽
- 如果其他交易者也采用相同的策略，这种优势将不复存在

**使用该工具的目的：**
- ✅ 了解熟练交易者的特征（通过数据指标和行为模式）
- ✅ 识别潜在的异常行为（如机器人或套利者）
- ✅ 理解交易者的心理（如FOMO情绪与交易纪律）
- ✅ 为自身的交易策略提供参考

**禁止使用该工具进行以下操作：**
- ❌ 自动复制他人的交易行为
- ❌ 期望复制他人的收益
- ❌ 在不了解交易逻辑的情况下依据这些数据进行交易
- ❌ 在不理解交易模式的情况下投入大量资金

## 适用场景

当您希望了解：
- **熟练交易者的操作方式**（哪些指标能区分赢家和输家）
- **交易者的心理特征**（谁会追逐价格波动？谁有良好的交易纪律）
- **检测异常行为（如机器人或套利行为）**（用于研究目的）
- **研究套利机会**（识别持有对冲头寸的账户）
- **比较不同交易者的交易风格**（了解稳定盈利的交易者与依赖运气的交易者的区别）
- **为自身交易策略提供依据**（将分析结果作为决策参考，而非直接的交易指令）

**禁止用于：**
- 盲目或自动复制他人的交易行为
- 假设过去的表现能预示未来的收益
- 仅依据这些数据做出高风险投资决策

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

该工具会返回以下全面的交易分析数据：

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

1. **获取交易历史**：通过Simmer API从Polymarket下载该钱包的所有交易记录。
2. **计算盈利时间线**：分析交易者在何时处于亏损状态，何时处于盈利状态。
3. **评估交易决策质量**：判断交易者是否在最佳价格买入，还是盲目追涨杀跌。
4. **检测交易模式**：区分机器人的快速交易行为和人类的理性交易行为。
5. **检查是否存在套利机会**：计算多次交易的平均成本是否低于1美元（这可能表明存在结构性优势，具体取决于执行成本和交易费用）。
6. **分析交易者的行为特征**：判断是否存在FOMO情绪导致的过度交易、是否具备良好的交易纪律，以及是否定期调整持仓。
7. **提供使用建议**：评估该钱包是否值得跟踪，以及其中潜在的风险。

## 数据指标解析

### ⏱️ **Time Profitable**（例如：75.3%）
该钱包在75%的交易时间内处于盈利状态（未出现亏损）。仅经历了25%的亏损，显示出良好的交易纪律。

- **>80%**：表明交易者具有极高的交易技巧（精准的入场时机和良好的持仓策略）。
- **50-80%**：表示交易者具备良好的交易纪律。
- **<50%**：提示交易策略存在风险（可能因恐慌性操作而造成亏损）。

### 🎯 **Entry Quality**（例如：平均滑点为28个基点）
该钱包在接近最佳价格时买入，28个基点的滑点对于活跃的交易者来说是正常的。没有迹象表明交易者受到FOMO情绪的影响（即没有在恐慌时匆忙下单）。

- **<20 bps**：表明交易者非常专业（使用限价单，耐心等待最佳买入时机）。
- **20-40 bps**：表现良好，交易速度和价格选择较为平衡。
- **>50 bps**：表明交易者可能过于追逐价格波动。

### 🤖 **Bot Detection**（例如：判断是否为机器人操作）
平均交易间隔为45秒，属于人类交易者的正常行为。如果间隔小于1秒，则很可能是机器人操作。

- **<5 sec**：极有可能是机器人操作，除非确定对方是正规的市场做市商。
- **5-30 sec**：可能是机器人操作，但也有可能是人类交易。
- **>30 sec**：属于人类交易。

### 💰 **Hedge Check**（例如：综合评估结果为0.98）
如果交易者在价格0.70美元时买入，在价格0.30美元时卖出，那么综合成本应为1美元。如果综合成本低于1美元，说明该钱包在交易中具有结构性优势（即买入成本低于卖出成本）。实际利润还受执行成本、交易费用和点差的影响。

- **< $0.95**：表明该钱包具有很强的交易优势，可能是机构投资者或专业交易者。
- **$0.95-1.00**：仅检测到轻微的优势。
- **> $1.00**：表示该钱包的交易策略没有明显优势，可能只是单纯押注价格走势。

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

### **示例2：研究异常交易行为（用于学习）**  
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

## 使用方法

**分析单个钱包（默认设置）：**  
```bash
python wallet_xray.py 0x1234...abcd
```

**分析特定市场的钱包：**  
```bash
python wallet_xray.py 0x1234...abcd "Bitcoin"
```

**以JSON格式输出分析结果（适用于脚本）：**  
```bash
python wallet_xray.py 0x1234...abcd --json
```

**比较两个钱包的交易数据：**  
```bash
python wallet_xray.py 0x1111... 0x2222... --compare
```

**仅分析最近的交易记录（加快分析速度）：**  
```bash
python wallet_xray.py 0x1234...abcd --limit 100
```

## 常见问题及解决方法

**“钱包没有交易记录”：**
- 该钱包尚未进行任何交易，或者所有交易记录都过于陈旧。
- 请尝试使用活跃的交易账户进行分析。

**“市场未找到”：**
- 查询的市场在Polymarket系统中不存在。
- 请尝试输入更具体的市场名称，或选择“全部市场”进行默认分析。

**“分析耗时过长”：**
- 对于交易记录超过500条的交易账户，分析可能需要30秒以上。
- 可使用`--limit 100`参数仅分析最近的交易记录，以加快分析速度。

**“API请求次数过多”：**
- 如果同时分析多个账户，可能会导致请求次数过多。请稍后再试，或使用`--limit 50`参数减少每次请求的数量。

**“连接错误”：**
- 请确认Polymarket的CLOB API是否可访问：`curl https://clob.polymarket.com/trades`
- 如果API不可用，请稍后再试，或使用`--limit 50`参数减少请求次数。

## 致谢

该工具基于[@thejayden](https://x.com/thejayden)的文章《The Autopsy: How to Read the Mind of a Polymarket Whale》中的交易分析框架开发。原文详细介绍了如何：
- 识别虚假的交易专家（高盈亏比、糟糕的交易决策）
- 检测机器人交易行为（通过分析交易速度）
- 发现套利机会（通过分析对冲头寸）
- 理解交易者的心理（如FOMO情绪与交易纪律）

此处使用的所有指标和分析方法均源自该文章。如果您觉得该工具有用，请阅读原文并关注[@thejayden](https://x.com/thejayden)的后续更新。

## 相关链接：**
- **Simmer API完整文档：** [simmer.markets/docs.md](https://simmer.markets/docs.md)
- **原始分析文章：** [The Autopsy: How to Read the Mind of a Polymarket Whale](https://x.com/thejayden/status/2020891572389224878)
- **仪表盘界面：** [simmer.markets/dashboard](https://simmer.markets/dashboard)
- **技术支持：** [Telegram频道：](https://t.me/+m7sN0OLM_780M2Fl)
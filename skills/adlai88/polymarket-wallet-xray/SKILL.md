---
name: polymarket-wallet-xray
displayName: Polymarket Wallet X-Ray
description: >
  **功能说明：**  
  可以对任何 Polymarket 钱包进行深度分析，包括其操作水平（skill level）、交易质量（entry quality）、是否存在自动化交易行为（bot detection），以及市场中的异常交易模式（edge analysis）。该工具会直接查询 Polymarket 的公开 API，无需任何身份验证。该功能的灵感来源于 @thejayden 的分析报告《Polymarket 钱包的“深度剖析”》。  
  **技术细节：**  
  1. **查询 Polymarket 的公开 API**：无需登录或提供任何认证信息，即可直接使用 Polymarket 提供的公开接口来获取所需数据。  
  2. **多维度分析**：涵盖交易行为的质量、自动化交易（bot）的检测，以及对市场异常模式的识别。  
  3. **功能扩展性**：可以根据实际需求进一步定制分析内容，例如添加更多特定的分析指标或规则。  
  **适用场景：**  
  - 金融机构或投资者：用于评估交易对手的风险或市场行为。  
  - 安全研究人员：检测潜在的欺诈行为或恶意操作。  
  - 开发者：用于理解 Polymarket 的交易逻辑或优化交易策略。  
  **注意事项：**  
  - 由于直接查询公开 API，数据可能包含用户的隐私信息，请确保合理使用该工具，避免滥用。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":[],"pip":[]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
inspired_by:
  - thejayden (@thejayden) - "Autopsy: How to Read the Mind of a Polymarket Whale"
version: "1.0.1"
published: true
---
# Polymarket钱包分析工具（X-Ray）

该工具可分析任何Polymarket钱包的交易模式、交易者的技能水平以及他们的交易优势。

**无需身份验证。**直接通过Polymarket的公开CLOB API进行查询。

**灵感来源：**[@thejayden](https://x.com/thejayden)的文章《The Autopsy: How to Read the Mind of a Polymarket Whale》（https://x.com/thejayden/status/2020891572389224878）

> 该工具实现了[@thejayden]开发的交易分析框架。请阅读原文以了解Time Profitable、对冲策略检查、机器人检测以及交易信号生成背后的原理。

> **这只是一个分析工具，并非交易建议。**该工具会为任何Polymarket钱包提供详细的交易数据，帮助你了解交易者的行为模式，从而做出更明智的决策。此工具仅用于教育和研究目的，切勿盲目复制他人的交易策略。

## ⚠️ 重要免责声明

**过去的表现并不能保证未来的结果。**历史数据仅能反映：
- ✅ 交易者过去的交易方式
- ✅ 他们的历史胜率和交易质量
- ❌ 但不能保证他们的策略在未来依然有效

**盲目复制他人交易的风险：**
- 市场环境不断变化
- 交易者的优势可能源于运气、时机选择或特定历史事件
- 手续费和滑点可能会将微小的优势抹去
- 如果其他交易者也采用相同的策略，这种优势就会消失

**使用该工具的目的：**
- ✅ 了解熟练交易者的特征（通过数据指标和行为模式）
- ✅ 识别潜在的异常行为（如机器人或套利者）
- ✅ 理解交易者的心理（如FOMO情绪与自律性）
- ✅ 为自身的交易策略提供参考

**禁止使用该工具进行：**
- ❌ 自动复制他人的交易
- ❌ 期望复制他人的收益
- ❌ 在不了解交易逻辑的情况下根据这些数据直接进行交易
- ❌ 在不理解交易模式的情况下投入大量资金

## 适用场景

当你想要了解以下内容时，可以使用该工具：
- ✅ 研究熟练交易者的操作方式（哪些指标能区分赢家和输家）
- ✅ 理解交易者的心理（谁会追逐价格？谁有自律性？）
- ✅ 识别异常行为（如机器人或套利行为）
- ✅ 研究套利机会（例如那些持有对冲头寸的交易者）
- ✅ 比较不同交易者的交易风格（哪些交易者是靠运气，哪些是靠技巧）

**禁止用于：**
- ❌ 盲目或自动复制他人的交易
- ❌ 仅凭这些数据就做出投资决策
- ❌ 仅基于这些数据进行高风险投资

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

该工具会返回以下详细的交易分析数据：

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
2. **计算盈利时间线**：分析交易者在何时处于亏损状态，何时盈利
3. **评估交易质量**：判断交易者是否在最佳价格买入
4. **检测交易模式**：区分机器人的快速交易和人类的理性交易
5. **检查是否存在套利机会**：如果“买入”和“卖出”的平均价格差小于1美元，则可能存在套利机会（无风险利润）
6. **分析交易行为**：判断交易者是否存在FOMO情绪（害怕错过机会而追涨）或交易行为是否自律
7. **给出建议**：分析该钱包是否值得关注，以及其中的风险

## 数据指标解释

### ⏱️ **Time Profitable**（例如：75.3%）
该钱包在75%的交易时间内处于盈利状态（未出现亏损）。只有25%的交易导致了亏损，说明交易者具有很强的自律性。

- **>80%** = 交易策略非常精准（买入时机准确，能够熬过亏损期）
- **50-80%** = 交易策略较为稳健（自律性良好）
- **<50%** = 交易策略存在风险（可能因恐慌性操作而亏损）

### 🎯 **交易质量**（例如：平均滑点为28个基点）
该钱包在接近最佳价格时买入。对于活跃的交易者来说，28个基点的滑点是正常的。没有证据表明交易者存在FOMO情绪（害怕错过机会而匆忙下单）。

- **<20 bps** = 交易者非常专业，使用限价单且耐心等待最佳买入时机。
- **20-40 bps** = 交易策略较为平衡，速度和价格都控制得当。
- **>50 bps** = 交易策略较弱，可能经常追逐价格波动。

### 🤖 **机器人检测**（例如：平均交易间隔为45秒）
如果交易间隔小于45秒，很可能是人类操作；如果小于1秒，则很可能是机器人操作。

- **<5秒** = 很可能是机器人操作，除非确定对方是正规的市场做市商，否则应避免与其交易。
- **5-30秒** = 可能是机器人操作。
- **>30秒** = 人类操作。

### 💰 **对冲策略检查**（例如：平均对冲效果为0.98**
如果“买入”价格与“卖出”价格的差值为0.70美元，而“卖出”价格为0.30美元，那么总差值为0.98美元，说明交易者的对冲策略有效（实现了无风险利润）。

- **< $0.95** = 说明交易者发现了套利机会（可能是机构投资者）。
- **$0.95-1.00** = 交易者有一定的优势。
- **> $1.00** = 说明交易者没有明显的交易优势，可能在赌价格走势。

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

### **示例3：基于数据分析做出决策（而非盲目复制）**
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

**分析单个钱包（默认设置）：**
```bash
python wallet_xray.py 0x1234...abcd
```

**分析特定市场中的钱包：**
```bash
python wallet_xray.py 0x1234...abcd "Bitcoin"
```

**以JSON格式输出结果（适用于脚本）：**
```bash
python wallet_xray.py 0x1234...abcd --json
```

**比较两个钱包的交易数据：**
```bash
python wallet_xray.py 0x1111... 0x2222... --compare
```

**仅分析最近的交易（加快分析速度）：**
```bash
python wallet_xray.py 0x1234...abcd --limit 100
```

## 常见问题及解决方法

**“钱包没有交易记录”**
- 该钱包尚未进行任何交易，或者所有交易记录都过于陈旧。
- 请尝试分析一个活跃的交易钱包。

**“市场未找到”**
- 查询的市场在Polymarket中不存在。
- 请尝试输入更具体的市场名称，或选择“全部市场”进行通用分析。

**“分析耗时过长”**
- 对于交易记录超过500条的交易钱包，分析可能需要30秒以上。
- 可使用`--limit 100`参数仅分析最近的交易记录以加快速度。

**“API请求次数过多”**
- 如果你同时分析多个钱包，可能会导致API请求次数超过限制。
- 请稍后再试，或使用`--limit 50`参数减少每次请求的数量。

**“连接失败”**
- 请确认Polymarket的CLOB API是否可用：`curl https://clob.polymarket.com/trades`
- 如果API不可用，请稍后再试，或使用`--limit 50`参数减少请求次数。

**致谢**

该工具基于[@thejayden](https://x.com/thejayden)的《The Autopsy: How to Read the Mind of a Polymarket Whale》一文中的交易分析框架。原文介绍了如何：
- 识别虚假的交易专家（高盈亏比但交易策略糟糕）
- 检测机器人（交易速度极快）
- 发现套利机会（持有对冲头寸）
- 理解交易者的心理（如FOMO情绪与自律性）

此处使用的所有指标和分析方法均源自该文章。如果你觉得这个工具有用，请阅读原文并关注[@thejayden](https://x.com/thejayden)。

## 相关资源

- **Simmer API完整文档：** [simmer.markets/docs.md](https://simmer.markets/docs.md)
- **原文分析：** [The Autopsy: How to Read the Mind of a Polymarket Whale](https://x.com/thejayden/status/2020891572389224878)
- **仪表盘：** [simmer.markets/dashboard](https://simmer.markets/dashboard)
- **支持渠道：** [Telegram](https://t.me/+m7sN0OLM_780M2Fl)
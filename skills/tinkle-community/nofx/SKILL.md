---
name: nofx
description: NOFX AI Trading OS集成：提供加密货币市场数据、AI交易信号、策略管理、交易员控制以及自动化报告功能。适用于使用NOFX平台（nofxai.com, nofxos.ai）进行加密货币交易、市场分析、AI500/AI300交易信号处理、资金流追踪、保证金监控、策略制定、交易员管理、回测等场景。
---

# NOFX AI交易技能

本技能可与开源的AI驱动的加密货币交易操作系统NOFX集成。

## 快速参考

| 资源 | URL |
|----------|-----|
| 网页仪表板 | https://nofxai.com |
| 数据API | https://nofxos.ai |
| API文档 | https://nofxos.ai/api-docs |
| GitHub | https://github.com/NoFxAiOS/nofx |

## 部署

有关安装和部署的说明，请参阅`references/deployment.md`：
- 一键安装（Linux/macOS/Docker）
- Windows安装（Docker Desktop / WSL2）
- Railway云平台部署
- 开发者手动安装
- 使用HTTPS进行服务器部署

## 支持的交易所

有关交易所注册链接（含费用折扣）和API设置，请参阅`references/exchanges.md`：

**中心化交易所（CEX）**：Binance、Bybit、OKX、Bitget、KuCoin、Gate.io
**去中心化交易所（DEX）**：Hyperliquid、Aster DEX、Lighter

**AI模型**：DeepSeek、Qwen、OpenAI、Claude、Gemini、Grok、Kimi

## 配置

将凭据存储在工作区`skills/nofx/config.json`中：

```json
{
  "api_key": "cm_xxxxxx",
  "web_email": "user@example.com",
  "browser_profile": "clawd"
}
```

## 1. 市场数据（API）

基础URL：`https://nofxos.ai`
认证方式：`?auth=API_KEY` 或 `Authorization: Bearer API_KEY`

### AI信号

```bash
# AI500 - High potential coins (score > 70)
curl "https://nofxos.ai/api/ai500/list?auth=$KEY"

# AI300 - Quantitative flow signals (S/A/B levels)
curl "https://nofxos.ai/api/ai300/list?auth=$KEY&limit=10"

# Single coin AI analysis
curl "https://nofxos.ai/api/ai500/{symbol}?auth=$KEY"
```

### 资金流动

```bash
# Institution inflow ranking
curl "https://nofxos.ai/api/netflow/top-ranking?auth=$KEY&limit=10&duration=1h&type=institution"

# Outflow ranking
curl "https://nofxos.ai/api/netflow/low-ranking?auth=$KEY&limit=10&duration=1h&type=institution"
```

### 开仓利息（Open Interest）

```bash
# OI increase ranking
curl "https://nofxos.ai/api/oi/top-ranking?auth=$KEY&limit=10&duration=1h"

# OI decrease ranking
curl "https://nofxos.ai/api/oi/low-ranking?auth=$KEY&limit=10&duration=1h"

# OI market cap ranking
curl "https://nofxos.ai/api/oi-cap/ranking?auth=$KEY&limit=10"
```

### 价格与费率

```bash
# Price ranking (gainers/losers)
curl "https://nofxos.ai/api/price/ranking?auth=$KEY&duration=1h"

# Funding rate top (crowded longs)
curl "https://nofxos.ai/api/funding-rate/top?auth=$KEY&limit=10"

# Funding rate low (crowded shorts)
curl "https://nofxos.ai/api/funding-rate/low?auth=$KEY&limit=10"

# Long-short ratio anomalies
curl "https://nofxos.ai/api/long-short/list?auth=$KEY&limit=10"
```

### 单个币种数据

```bash
# Comprehensive coin data
curl "https://nofxos.ai/api/coin/{symbol}?auth=$KEY&include=all"

# Order book heatmap
curl "https://nofxos.ai/api/heatmap/future/{symbol}?auth=$KEY"
```

时间选项：`1m、5m、15m、30m、1h、4h、8h、12h、24h、2d、3d、5d、7d`

## 2. 策略管理（浏览器）

在https://nofxai.com/strategy使用浏览器自动化工具进行操作：

### 策略结构

```json
{
  "strategy_type": "ai_trading",
  "language": "en",
  "coin_source": {
    "source_type": "ai500|static|oi_top|oi_low|mixed",
    "static_coins": ["BTC", "ETH"],
    "use_ai500": true,
    "ai500_limit": 10
  },
  "indicators": {
    "enable_ema": true,
    "enable_rsi": true,
    "enable_atr": true,
    "enable_boll": true,
    "enable_oi": true,
    "enable_funding_rate": true,
    "enable_quant_data": true,
    "nofxos_api_key": "cm_xxx"
  },
  "risk_control": {
    "max_position_pct": 10,
    "stop_loss_pct": 3,
    "take_profit_pct": 5
  },
  "prompt_sections": {
    "role_definition": "...",
    "entry_standards": "...",
    "decision_process": "..."
  }
}
```

### 自然语言策略创建

当用户用自然语言描述策略时：
1. 解析策略要求（币种、指标、入场/出场规则、风险控制）
2. 生成StrategyConfig JSON文件
3. 进入策略编辑器
4. 创建新策略并填写相关信息
5. 保存并激活策略

## 3. 交易者管理（浏览器）

在https://nofxai.com/traders使用浏览器自动化工具进行操作：

### 操作

- **列表**：导航至/traders页面，查看交易者列表
- **创建**：点击“Create Trader”，选择模型/交易所/策略
- **开始/停止**：点击交易者卡片上的“Start/Stop”按钮
- **查看**：点击“View”查看详细信息和交易记录

### 交易者配置

```
Model: claude|deepseek|gpt|gemini|grok|kimi|qwen
Exchange: binance|bybit|okx|bitget|kucoin|gate|hyperliquid|aster|lighter
Strategy: Select from strategy list
```

## 4. 仪表板（浏览器）

导航至https://nofxai.com/dashboard

### 可用数据

- 账户权益和余额
- 总盈亏（绝对值和百分比）
- 当前持仓
- 权益曲线图
- 交易历史
- AI决策日志

## 5. AI辩论（浏览器）

导航至https://nofxai.com/debate

### 创建辩论

1. 点击“New Debate”
2. 选择交易币种
3. 选择AI模型和角色：
   - 多头（Bull）：寻找多头交易机会
   - 空头（Bear）：寻找空头交易机会
   - 分析师（Analyst）：提供中性分析
4. 进行辩论轮次
5. 获取共识推荐

## 6. 回测（浏览器）

导航至https://nofxai.com/backtest

### 运行回测

1. 选择AI模型
2. 选择策略（可选）
3. 输入交易币种（用逗号分隔）
4. 设置时间范围
5. 运行回测并分析结果

## 7. 监控与警报

### 市场报告的Cron作业

```json
{
  "name": "NOFX市场行情汇报",
  "schedule": {"kind": "cron", "expr": "*/30 * * * *"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Fetch NOFX data and generate market report...",
    "deliver": true,
    "channel": "telegram",
    "to": "USER_ID"
  }
}
```

### 报告内容

- 🤖 AI500信号（币种 + 评分 + 盈利情况）
- 💰 机构资金流动排名前十
- 🚀 价格涨幅排名前十
- 📈 开仓利息增加排名前十
- 📉 开仓利息减少排名前十
- ⚠️ 价格下跌警报

## 8. 常见工作流程

### 每日市场检查

1. 获取AI500/AI300信号
2. 检查机构资金流动
3. 监控开仓利息变化
4. 识别交易机会

### 策略开发

1. 分析市场数据
2. 定义入场/出场规则
3. 在策略编辑器中创建策略
4. 使用历史数据回测
5. 创建交易者并开始交易

### 风险监控

1. 查看仪表板上的盈亏情况
2. 审查持仓情况
3. 监控资金回撤情况
4. 根据需要调整或停止交易

## API响应示例

有关详细的API响应结构，请参阅`references/api-examples.md`。

## 其他参考资料

| 参考资料 | 说明 |
|-----------|-------------|
| `references/grid-trading.md` | 带有示例的网格交易详细指南 |
| `references/market-charts.md` | 市场页面和图表分析 |
| `references/multi-account.md` | 多账户管理 |
| `references/webhooks.md` | Telegram/Discord/Slack通知设置 |
| `references/faq.md` | 常见问题解答 |
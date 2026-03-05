---
name: crypto-lens
description: CryptoLens — 一款基于人工智能的多币种加密货币分析工具。支持比较2至5种加密货币的性能（相对表现、相关性矩阵、波动率排名），提供单币种的技术分析图表（包含7天/25天/99天的移动平均线、相对强弱指数RSI、MACD以及布林带指标），同时具备AI市场分析功能（生成0-100分的综合评分及可操作的买卖信号）。输出结果为深色主题的PNG图片文件。所有功能的调用均通过SkillPay收费，每个命令的费用为1个Token（0.001 USDT）。适用于用户需要进行加密货币比较、投资组合分析、技术指标查询、布林带分析，或询问“是否应该买入/卖出”等场景。
metadata:
  {
    "clawdbot": {
      "emoji": "📊",
      "requires": { "bins": ["python3"] }
    },
    "skillpay": {
      "pricing": [
        { "command": "chart", "tokens": 1, "usd": "0.001" },
        { "command": "compare", "tokens": 1, "usd": "0.001" },
        { "command": "analyze", "tokens": 1, "usd": "0.001" }
      ],
      "currency": "USDT",
      "chain": "BNB Chain"
    },
    "credentials": {
      "embedded": true,
      "description": "SkillPay billing API key and Skill ID are embedded in the script. This is the standard SkillPay integration pattern — the key can only charge users, not withdraw funds.",
      "services": ["skillpay.me"]
    }
  }
---
# CryptoLens 📊

一款基于人工智能的多币种加密货币分析工具，提供多种技术指标分析功能。

## 命令

### 1. 多币种比较

比较2-5种加密货币的性能（相对表现、波动率排名及相关性矩阵）。

```bash
python3 {baseDir}/scripts/crypto_lens.py compare BTC ETH SOL [--duration 7d] [--user-id UID]
```

**示例：**
- `python3 {baseDir}/scripts/crypto_lens.py compare BTC ETH SOL`
- `python3 {baseDir}/scripts/crypto_lens.py compare BTC ETH SOL HYPE ARB --duration 7d`
- `python3 {baseDir}/scripts/crypto_lens.py compare PEPE WIF BONK --duration 3d`

**输出：**
- 价格对比表（包含价格变化百分比和波动率排名）
- 标准化的性能对比图表
- 相关性矩阵热力图
- 图表以PNG格式保存

**费用：** 每次调用收取1个代币（0.001 USDT）。

### 2. 技术分析图表

单币种蜡烛图，包含所有常用技术指标。

```bash
python3 {baseDir}/scripts/crypto_lens.py chart BTC [--duration 24h] [--user-id UID]
```

**示例：**
- `python3 {baseDir}/scripts/crypto_lens.py chart BTC`
- `python3 {baseDir}/scripts/crypto_lens.py chart ETH --duration 12h`
- `python3 {baseDir}/scripts/crypto_lens.py chart HYPE --duration 2d`

**包含的指标：**
- **MA(7/25/99)** — 短期/中期/长期移动平均线
- **RSI(14)** — 相对强弱指数（包含30/70区间）
- **MACD(12,26,9)** — MACD线、信号线及柱状图
- **Bollinger Bands(20,2)** — 波动率区间

**费用：** 每次调用收取1个代币（0.001 USDT）。

### 3. 人工智能市场分析

基于人工智能的评分系统，提供全面的技术分析及可操作的市场信号。

```bash
python3 {baseDir}/scripts/crypto_lens.py analyze BTC [--duration 24h] [--user-id WALLET]
```

**示例：**
- `python3 {baseDir}/scripts/crypto_lens.py analyze BTC`
- `python3 {baseDir}/scripts/crypto_lens.py analyze ETH --duration 7d`
- `python3 {baseDir}/scripts/crypto_lens.py analyze HYPE --duration 2d --user-id 0x1234...`

**输出：**
- 综合评分（0-100分，表示市场趋势）
- 信号提示（强烈看跌/看涨/中性/强烈看涨）
- 各指标的详细分析结果：
  - RSI(14)区间分析
  - MACD交叉及柱状图趋势
  - 移动平均线趋势
  - 价格与MA25的关系
  - 波动率区间位置
  - 成交量趋势（价格与成交量的确认）
  - 短期市场动能
- 可操作的建议（简明结论）
- 附有完整的技术分析图表

**评分规则：**
- RSI <30：+20（超卖，看涨信号）/ RSI >70：-20（超买，看跌信号）
- MACD金叉：+15 / 死亡交叉：-15
- MA7>MA25>MA99：+15（看涨信号）
- 价格位于波动率区间下限/上限：+15 / -15
- 成交量与价格的确认：±8
- 各指标得分加权后标准化为0-100分

**费用：** 每次调用收取1个代币（0.001 USDT）。

## 时间范围

支持的时间范围：`30m`、`3h`、`12h`、`24h`（默认）、`2d`、`7d`、`14d`、`30d`

## 输出格式

输出结果为JSON格式，包含：
- `text/plain` — 格式化的文本摘要
- `chart_path` — 生成的PNG图表路径

**图表格式说明：**
当`chart_path`参数存在时，必须以图片形式发送图表。在回复中，先输出`text/plain`，然后在新行添加`MEDIA: `后跟图表路径（例如：`MEDIA: /tmp/cryptolens_chart_BTC_1769204734.png`）。请勿使用`[chart: path]`或其他占位符，只需使用`MEDIA: <chart_path>`即可。

## 费用支付

所有命令均通过SkillPay.me（BNB Chain USDT）收费，每次调用收取1个代币（0.001 USDT）。
脚本中已嵌入支付所需的API密钥和用户ID（`--user-id`参数）。用户ID应为用户的BNB Chain钱包地址（例如`0x1234...abcd`），该地址也将用于通过支付链接充值。确保用户ID在所有设备和会话中保持一致。

**注意：** 如果用户尚未提供钱包地址，请在运行命令前询问他们。如果用户余额不足，系统会返回一个支付链接，用户可通过该链接使用BNB Chain USDT进行充值。

## 数据来源**

- **Hyperliquid API**：优先用于支持的交易币种（如HYPE、BTC、ETH、SOL等）
- **CoinGecko API**：用于其他所有币种的数据获取
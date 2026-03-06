---
name: crypto-lens
description: **CryptoLens** — 一款由人工智能驱动的多币种加密货币分析工具。支持比较2至5种加密货币的性能（相对表现、相关性矩阵、波动性排名），提供单币种的技术分析图表（包含MA(7/25/99)、RSI、MACD和Bollinger Bands指标），同时具备AI市场分析功能（生成0-100分的综合评分及可操作的买卖信号）。输出格式为深色主题的PNG图片。所有功能的调用均通过SkillPay收费，每个命令的费用为1个Token（0.001 USDT）。适用于用户需要比较加密货币、进行投资组合分析、查看技术指标、RSI、MACD、Bollinger Bands数据，或获取“是否应该买入/卖出”的建议的场景。
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
基于人工智能的多币种加密货币分析工具，支持多种技术指标。  

## ⚠️ 费用说明  

这是一个**付费技能**。每个命令的费用为1个代币（0.001 USDT），通过[SkillPay.me](https://skillpay.me)支付。  

**费用结算流程：**  
1. 你需要通过`--user-id`参数提供自己的BNB Chain钱包地址（该地址用于识别用户身份）。  
2. 在执行命令前，该技能会通过SkillPay从你的钱包中扣除1个代币。  
3. 如果你的钱包余额不足，系统会提供一个支付链接，让你使用BNB Chain充值。  
4. 除非你主动操作（点击支付链接并确认交易），否则不会产生任何费用。  
5. 嵌入的API密钥仅用于发起费用结算，无法访问你的钱包或提取资金。  

**你完全控制自己的支出**：只需支付实际使用的费用，无需订阅或自动续费。  

## 命令说明  

### 1. 多币种对比  
比较2-5种加密货币的性能（相对表现、波动率排名及相关性矩阵）：  
```bash
python3 {baseDir}/scripts/crypto_lens.py compare BTC ETH SOL [--duration 7d] [--user-id UID]
```  

**示例：**  
- `python3 {baseDir}/scripts/crypto_lens.py compare BTC ETH SOL`  
- `python3 {baseDir}/scripts/crypto_lens.py compare BTC ETH SOL HYPE ARB --duration 7d`  
- `python3 {baseDir}/scripts/crypto_lens.py compare PEPE WIF BONK --duration 3d`  

**输出结果：**  
- 价格对比表（包含价格变化百分比和波动率排名）  
- 标准化的性能对比图表  
- 相关性矩阵热力图  
- 图表以PNG格式保存  

**费用：** 每次调用费用为1个代币（0.001 USDT）。  

### 2. 技术分析图表  
生成单币种的蜡烛图，并显示所有常用技术指标：  
```bash
python3 {baseDir}/scripts/crypto_lens.py chart BTC [--duration 24h] [--user-id UID]
```  

**示例：**  
- `python3 {baseDir}/scripts/crypto_lens.py chart BTC`  
- `python3 {baseDir}/scripts/crypto_lens.py chart ETH --duration 12h`  
- `python3 {baseDir}/scripts/crypto_lens.py chart HYPE --duration 2d`  

**包含的技术指标：**  
- **MA(7/25/99)**：短期/中期/长期移动平均线  
- **RSI(14)**：相对强弱指数（包含30/70信号区间）  
- **MACD(12,26,9)**：MACD线、信号线及柱状图  
- **Bollinger Bands(20,2)**：波动率带  

**费用：** 每次调用费用为1个代币（0.001 USDT）。  

### 3. 人工智能市场分析  
基于人工智能的评分系统，提供全面的技术分析及可操作的买卖信号：  
```bash
python3 {baseDir}/scripts/crypto_lens.py analyze BTC [--duration 24h] [--user-id WALLET]
```  

**示例：**  
- `python3 {baseDir}/scripts/crypto_lens.py analyze BTC`  
- `python3 {baseDir}/scripts/crypto_lens.py analyze ETH --duration 7d`  
- `python3 {baseDir}/scripts/crypto_lens.py analyze HYPE --duration 2d --user-id 0x1234...`  

**输出结果：**  
- 综合评分（0-100分，表示市场趋势）  
- 买卖信号标签（强烈看跌/看涨/中性/强烈看涨）  
- 各技术指标的详细分析（包括RSI、MACD、价格与移动平均线的关系等）  
- 可操作的买卖建议  
- 附带完整的技术分析图表  

**评分规则：**  
- RSI < 30：强烈看跌  
- RSI > 70：强烈看涨  
- MACD金叉：+15  
- MA7 > MA25 > MA99：看涨信号  
- 价格位于波动率带下方/上方：+15/-15  
- 量价关系确认：±8  
- 综合评分（0-100分）  

**费用：** 每次调用费用为1个代币（0.001 USDT）。  

## 时间范围  
可选时间范围：`30m`、`3h`、`12h`、`24h`（默认）、`2d`、`7d`、`14d`、`30d`  

## 输出格式**  
输出结果为JSON格式，包含：  
- `textPLAIN`：格式化的文本摘要  
- `chart_path`：生成的PNG图表路径  

**图表展示方式：**  
当`chart_path`参数存在时，必须以图片形式发送图表。在回复中，先输出`textPLAIN`，再在新行输入`MEDIA: `后跟上实际的`chart_path`（例如：`MEDIA: /tmp/cryptolens_chart_BTC_1769204734.png`）。**不要**使用`[chart: path]`等占位符，只需输入`MEDIA: <chart_path>`即可。  

## 费用支付方式**  
所有命令均通过SkillPay.me（使用BNB Chain USDT）收取费用。  
技能脚本中已嵌入支付所需的API密钥和用户ID（`--user-id`参数）。这是SkillPay为付费技能提供的标准集成方式。  

**注意：**  
- 请务必提供用户的BNB Chain钱包地址（例如`0x1234...abcd`）。该地址用于确认用户身份，并用于后续的充值操作。  
- 如果用户余额不足，系统会提供支付链接，请用户通过BNB Chain充值。  

## 数据来源**  
- **Hyperliquid API**：支持的主要加密货币（如HYPE、BTC、ETH、SOL等）的数据来源。  
- **CoinGecko API**：其他加密货币的数据来源。
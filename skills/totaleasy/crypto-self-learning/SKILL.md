---
name: crypto-self-learning
description: 这是一个用于加密货币交易的自主学习系统。该系统会记录每笔交易的详细信息（包括使用的指标、市场状况等），分析盈利/亏损的规律，并自动更新交易策略。用户可以利用该系统来记录交易行为、评估交易表现、识别哪些策略有效、哪些无效，从而不断提升交易的准确性。
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["jq","python3"]}}}
---

# 加密交易自学系统 🧠  
这是一个基于人工智能的自我提升工具，专门用于加密交易。通过分析每一次交易，逐步提升交易精准度。  

## 🎯 核心理念  
每一次交易都是一次学习机会。该系统：  
1. **详细记录** 每一笔交易的全部信息；  
2. **分析** 盈亏中的规律；  
3. **从实际数据中生成** 交易规则；  
4. **自动更新** 系统的记忆库。  

## 📝 记录交易  
每次交易（无论盈亏）完成后，都需要进行记录：  
```bash
python3 {baseDir}/scripts/log_trade.py \
  --symbol BTCUSDT \
  --direction LONG \
  --entry 78000 \
  --exit 79500 \
  --pnl_percent 1.92 \
  --leverage 5 \
  --reason "RSI oversold + support bounce" \
  --indicators '{"rsi": 28, "macd": "bullish_cross", "ma_position": "above_50"}' \
  --market_context '{"btc_trend": "up", "dxy": 104.5, "russell": "up", "day": "tuesday", "hour": 14}' \
  --result WIN \
  --notes "Clean setup, followed the plan"
```  

### 必填字段：  
| 字段 | 说明 | 示例 |  
|-------|-------------|---------|  
| `--symbol` | 交易对 | BTCUSDT |  
| `--direction` | 多头（LONG）或空头（SHORT） | LONG |  
| `--entry` | 入场价格 | 78000 |  
| `--exit` | 出场价格 | 79500 |  
| `--pnl_percent` | 盈亏百分比 | 1.92 或 -2.5 |  
| `--result` | 成功（WIN）或失败（LOSS） | WIN |  

### 可选但推荐字段：  
| 字段 | 说明 |  
|-------|-------------|---------|  
| `--leverage` | 使用的杠杆倍数 | |  
| `--reason` | 入场的理由 | |  
| `--indicators` | 入场时使用的指标（JSON格式） | |  
| `--market_context` | 市场环境信息（JSON格式） | |  
| `--notes` | 交易后的观察与心得 | |  

## 📊 分析交易表现  
运行分析以发现交易规律：  
```bash
python3 {baseDir}/scripts/analyze.py
```  
输出结果包括：  
- 不同方向的胜率  
- 每周的胜率  
- 不同RSI区间内的胜率  
- 不同杠杆倍数下的胜率  
- 最有效/最无效的交易策略  
- 建议的交易规则  

### 分析特定条件下的交易表现：  
```bash
python3 {baseDir}/scripts/analyze.py --symbol BTCUSDT
python3 {baseDir}/scripts/analyze.py --direction LONG
python3 {baseDir}/scripts/analyze.py --min-trades 10
```  

## 🧠 生成交易规则  
从交易历史中提取可执行的交易规则：  
```bash
python3 {baseDir}/scripts/generate_rules.py
```  
该系统会分析这些规律并生成相应的交易规则：  
```
🚫 AVOID: LONG when RSI > 70 (win rate: 23%, n=13)
✅ PREFER: SHORT on Mondays (win rate: 78%, n=9)
⚠️ CAUTION: Trades with leverage > 10x (win rate: 35%, n=20)
```  

## 📈 自动更新系统记忆  
将学到的规则应用到系统的记忆库中：  
```bash
python3 {baseDir}/scripts/update_memory.py --memory-path /path/to/MEMORY.md
```  
系统会在文档中添加一个“## 🧠 学到的规则”部分，展示分析结果。  

### 预览规则变更：  
```bash
python3 {baseDir}/scripts/update_memory.py --memory-path /path/to/MEMORY.md --dry-run
```  
允许用户预览规则变更前的效果。  

## 📋 查看交易历史  
```bash
python3 {baseDir}/scripts/log_trade.py --list
python3 {baseDir}/scripts/log_trade.py --list --last 10
python3 {baseDir}/scripts/log_trade.py --stats
```  
用户可以随时查看所有的交易记录。  

## 🔄 每周回顾  
系统会每周自动运行分析，展示以下内容：  
- 本周与上周的交易表现对比  
- 新发现的交易规律  
- 成功或失败的交易规则  
- 对下一周的交易建议  

## 📁 数据存储  
所有交易记录存储在 `{baseDir}/data/trades.json` 文件中：  
```json
{
  "trades": [
    {
      "id": "uuid",
      "timestamp": "2026-02-02T13:00:00Z",
      "symbol": "BTCUSDT",
      "direction": "LONG",
      "entry": 78000,
      "exit": 79500,
      "pnl_percent": 1.92,
      "result": "WIN",
      "indicators": {...},
      "market_context": {...}
    }
  ]
}
```  

## 最佳实践：  
1. **记录每一笔交易**（无论盈亏）；  
2. **如实记录**（不要遗漏任何交易）；  
3. **提供详细背景信息**（更多数据有助于发现规律）；  
4. **每周进行回顾**（规律会随着时间逐渐显现）；  
5. **相信数据**（如果数据提示避免某种策略，就务必遵守）。  

## 🔗 与 tess-cripto 的集成  
该系统可与 tess-cripto 集成：  
1. **交易前**：检查 `MEMORY.md` 中的交易规则；  
2. **交易后**：详细记录交易信息；  
3. **每周**：运行分析并更新系统记忆库。  

---  
*由 Total Easy Software 开发——从每一次交易中学习，提升交易能力* 🧠📈
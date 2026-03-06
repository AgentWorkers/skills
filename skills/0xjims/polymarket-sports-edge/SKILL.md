---
name: polymarket-sports-edge
description: 找出体育博彩公司的共识与 Polymarket 体育市场之间的赔率差异，然后利用这一差异进行交易。
metadata:
  author: "jim.sexton"
  version: "1.0.0"
  displayName: "Polymarket Sports Edge"
  difficulty: "intermediate"
---
# Polymarket Sports Edge

> **这是一个模板。** 默认策略会对比体育博彩平台的共识赔率与 Polymarket 的价格，当两者之间的差异超过预设阈值时执行交易。  
> 你可以根据需要修改模板内容：调整支持的体育项目、阈值、交易规模，或添加自定义过滤条件（例如：仅交易 NBA 比赛、要求最低交易量、按数据更新频率来决定交易权重）。  

## 功能说明  

该策略会扫描 Polymarket 上活跃的体育市场，并将价格与 The Odds API 提供的体育博彩平台共识赔率进行比较。当某个市场的价格明显偏离专业博彩公司的定价时，系统会买入被低估的那一方。  

**优势在于：** 体育博彩平台的赔率是由拥有庞大业务量的专业赔率制定者设定的，因此其准确性非常高；而 Polymarket 的体育市场规模较小、交易效率较低。当两者出现分歧时，通常专业博彩公司的定价更为准确。  

## 工作原理  

1. 从 Simmer API 获取活跃的体育市场列表（`GET /api/sdk/markets?q=<sport>`）  
2. 从 The Odds API 获取相同体育项目的当前赔率  
3. 通过比较球队名称和比赛日期来匹配相关市场与比赛  
4. 计算各体育博彩平台共识赔率的平均值（即所有博彩公司的平均赔率）  
5. 将计算结果与 Polymarket 的价格进行对比；如果差异超过阈值，则执行交易  
6. 买入被低估的那一方，并记录交易理由。  

## 配置参数  

### 环境变量  

| 变量          | 是否必填 | 描述                         |
|--------------|---------|-----------------------------------------|  
| `SIMMER_API_KEY`   | 是       | 你的 Simmer API 密钥                   |
| `THE_ODDS_API_KEY` | 是       | [the-odds-api.com](https://the-odds-api.com) 提供的免费 API 密钥（每月 500 次请求） |
| `MIN_DIVERGENCE` | 否       | 最小价格差异阈值（默认：`0.08` = 8%）             |
| `TRADE_AMOUNT`    | 否       | 每笔交易的金额（以交易平台的货币计，单位：__）         |
| `SPORTS`       | 否       | 用逗号分隔的体育项目代码（默认：NBA, NFL, NHL, MLB, MMA, EPL, MLS） |
| `LIVE`        | 否       | 设置为 `true` 以进行实际交易；默认为模拟测试模式   |  

### 获取免费的 The Odds API 密钥  

1. 访问 [the-odds-api.com](https://the-odds-api.com)  
2. 注册免费账户（每月 500 次请求）  
3. 复制你的 API 密钥  
4. 在代码中设置：`export THE_ODDS_API_KEY=your_key_here`  

## 运行脚本  

```bash
# Dry run (default) — logs what it would trade
python sports_edge.py

# Live trading
LIVE=true python sports_edge.py
```  

## 示例输出  

```
[Sports Edge] Scanning 3 sports...
[Sports Edge] NBA: Found 6 games with odds
[Sports Edge] Matched: "Will the Celtics win vs Pacers?" → Celtics vs Pacers (2026-03-05)
[Sports Edge] Polymarket YES: 0.58 | Sportsbook consensus: 0.69 | Divergence: +0.11
[Sports Edge] TRADE: Buying YES at 0.58 (edge: 11%) — 10.00 $SIM
[Sports Edge] NHL: Found 4 games with odds
[Sports Edge] No divergence above threshold.
[Sports Edge] Done. 1 trade executed, 0 skipped.
```
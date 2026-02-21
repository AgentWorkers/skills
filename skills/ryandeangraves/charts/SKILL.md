# 技能：图表生成

## 目的  
能够生成包含蜡烛图、斐波那契回调线、移动平均线（20日/50日）、相对强弱指数（RSI）以及模式检测的专业技术分析图表。该功能依赖于本地的 `crypto_charts.py` 模块。

## 使用场景  
- 当上级要求查看 BTC 图表或对白银进行技术分析时  
- 需要图表来进行市场分析或报告制作  
- 用于每日晨会的数据展示  
- 任何需要可视化技术分析的场景  

## 生成所有图表（全套）  
会为以下 6 种追踪资产生成图表：BTC、ETH、XRP、SUI、Gold、Silver。  
**注意：** 由于 API 的请求频率限制，生成所有图表需要 2–3 分钟时间。  
```bash
cd ~/clawd && python3 -c "
import json
from crypto_charts import generate_all_charts, cleanup_old_charts
cleanup_old_charts()
report = generate_all_charts(output_dir=os.path.expanduser('~/clawd/charts'))
print(json.dumps(report, indent=2, default=str))
" 2>&1
```

生成的图表文件保存在：`~/clawd/charts/chart_btc.png`、`chart_eth.png` 等目录中。  

## 生成单个图表  
如需快速查看某一种资产的图表，无需等待整套图表生成：  
```bash
cd ~/clawd && python3 -c "
import os, json
from crypto_charts import (
    fetch_yfinance, fetch_ohlc, fetch_market_data,
    calc_moving_averages, calc_rsi, calc_fibonacci,
    detect_patterns, generate_chart, COINS
)

coin_id = 'COIN_ID'  # bitcoin, ethereum, ripple, sui, gold, silver
info = COINS[coin_id]

# Fetch data (Yahoo Finance first, CoinGecko fallback)
df = fetch_yfinance(coin_id)
if df is None or len(df) < 10:
    df = fetch_ohlc(coin_id)
if df is None or len(df) < 10:
    df = fetch_market_data(coin_id)

if df is not None and len(df) >= 5:
    df = calc_moving_averages(df)
    df = calc_rsi(df)
    fib = calc_fibonacci(df)
    patterns = detect_patterns(df)

    chart_path = os.path.expanduser(f'~/clawd/charts/chart_{info[\"symbol\"].lower()}.png')
    generate_chart(coin_id, df, fib, chart_path)

    print(f'Chart: {chart_path}')
    print(f'Price: \${df[\"close\"].iloc[-1]:,.2f}')
    print(f'RSI: {df[\"rsi\"].iloc[-1]:.1f}')
    print('Patterns:')
    for p in patterns:
        print(f'  - {p}')
else:
    print('Not enough data to generate chart')
"
```

## 跟踪资产  
| 资产 ID | 股票代码 | 图表颜色 | 数据来源 |  
|---------|--------|------------|-------------|  
| bitcoin | BTC | #F7931A | Yahoo Finance → CoinGecko |  
| ethereum | ETH | #627EEA | Yahoo Finance → CoinGecko |  
| ripple | XRP | #00AAE4 | Yahoo Finance → CoinGecko |  
| sui | SUI | #6FBCF0 | Yahoo Finance → CoinGecko |  
| gold | XAU | #FFD700 | Yahoo Finance |  
| silver | XAG | #C0C0C0 | Yahoo Finance |  

## 图表包含的内容  
- **蜡烛图**（绿色表示上涨，红色表示下跌）——显示过去 90 天的每日数据  
- **20 日移动平均线（蓝色）** 和 **50 日移动平均线（金色）**——用于判断趋势及支撑/阻力位  
- **斐波那契回调线**（0%、23.6%、38.2%、50%、61.8%、78.6%、100%）  
- **相对强弱指数（RSI）**（紫色）——包含超买（70）和超卖（30）的提示线  
- **当前价格标记**——以资产主题颜色显示的点状标记及水平线  

## 模式检测（自动识别）  
该模块可自动识别并报告以下技术形态：  
- 移动平均线交叉（金叉/死叉）  
- 头肩顶/底形态  
- 斐波那契区域定位  
- 趋势强度（7 天内的走势变化）  
- 相对强弱指数状态（超买/超卖/中性）  
- 价格在 90 天区间内的位置  

## 通过 Telegram 发送图表  
生成图表后，可使用 Clawdbot 的内置 `message` 命令发送图表图像：  
```
message (Telegram, target="7887978276") [attach ~/clawd/charts/chart_btc.png]
```

## 规则说明  
- 图表使用过去 90 天的数据，足以进行有意义的技术分析  
- 首先尝试使用 Yahoo Finance（免费且数据可靠）；若无法使用则使用 CoinGecko 作为备用  
- 每种资产之间的请求间隔为 8 秒，批量请求的冷却时间为 20 秒  
- 使用前务必运行 `cleanup_old_charts()` 命令以清理旧图表文件，避免磁盘空间占用过多  
- 图表图像的分辨率约为 150 DPI，采用深色主题（背景颜色 #0f172a）
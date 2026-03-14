# APEX — 二元交易代理

## APEX的功能  
APEX是一款专为Kalshi 15分钟周期的加密货币市场设计的智能二元期权交易代理。  
它每15分钟扫描BTC、ETH、SOL和XRP市场，分析交易信号，并根据人工智能的建议执行交易。  

## 命令  
| 命令            | 描述                                      |  
|-----------------|-----------------------------------------|  
| `python3 {baseDir}/scripts/apex.py` | 运行一次完整的扫描并执行交易周期          |  
| `python3 {baseDir}/scripts/apex.py --status` | 显示账户余额、盈亏情况以及未平仓头寸           |  
| `python3 {baseDir}/scripts/apex.py --log` | 显示最近的交易记录                        |  

## APEX的交易流程  
1. 扫描Kalshi平台上的15分钟周期二元期权市场（KXBTC15M、KXETH15M、KXSOL15M、KXXRP15M）；  
2. 从Coinbase获取RSI、动量指标和成交量数据；  
3. 根据3到4个一致的交易信号判断价格走势（上涨/下跌）；  
4. 使用GPT-4o-mini模型确认交易决策（选择“YES”或“NO”），并确定交易规模；  
5. 在Kalshi平台上下达限价单；  
6. 在市场走势明确后确认交易结果。  

## 环境变量  
- `KALSHI_API_KEY_ID`    | Kalshi平台的API密钥（UUID格式）            |  
- `KALSHI_PRIVATE_KEY_PATH` | RSA私钥的PEM文件路径                |  
- `OPENAI_API_KEY`     | OpenAI平台的API密钥                  |  
- `TELEGRAM_BOT_TOKEN`   | Telegram机器人的访问令牌                |  
- `TELEGRAMCHAT_ID`    | Telegram聊天室的ID                        |  

## 市场规则  
- 15分钟周期的市场每小时在00:00、00:15、00:30、00:45开盘；  
- 交易结果基于CF Benchmarks的BRTI价格确定；  
- “YES”表示到期时价格高于开盘价，“NO”表示价格低于开盘价；  
- 最佳入场时机为到期前8至14分钟；  
- 当RSI指标处于45-55区间时（价格波动较大、趋势不明确），避免交易。
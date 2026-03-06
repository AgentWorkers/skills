---
name: aicoin-market
description: "此技能适用于用户查询加密货币价格、市场数据、K线图、资金费率、未平仓合约数量（open interest）、多头/空头比例、大额交易订单（whale orders）、清算数据、加密货币新闻、新闻快讯、热门加密货币、股票报价、交易所持仓情况，或任何与加密货币市场相关的问题时。例如：用户可能会询问“BTC价格”、“查看价格”、“显示K线图”、“资金费率”、“未平仓合约数量”、“大额交易订单”、“加密货币新闻”、“热门币种”等。该技能支持超过200家交易所的实时数据，必须通过运行Node.js脚本来获取真实数据；严禁生成虚假价格或伪造市场数据。如需进行交易所交易（买入/卖出/查看账户余额），请使用aicoin-trading；如需制定交易策略或进行回测（backtest），请使用aicoin-freqtrade；如需分析大额交易者的交易行为（Hyperliquid whale analytics），请使用aicoin-hyperliquid。"
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/coinos-skills", "license": "MIT" } }
---
# CoinOS Market

这是一个由[AiCoin Open API](https://www.aicoin.com/opendata)提供支持的加密货币市场数据工具包。该工具包可获取来自200多家交易所的价格、K线图、新闻、交易信号以及大额交易等信息。

**版本：** 1.0.0

## 重要规则

1. **严禁伪造数据。** 请始终使用脚本来获取实时数据。
2. **严禁使用curl、web_fetch或浏览器** 来获取加密货币数据，必须使用这些指定的脚本。
3. **严禁运行`env`或`printenv`命令**——这些命令可能会导致API密钥泄露到日志中。
4. **脚本会自动加载`.env`文件**——切勿将API密钥直接写在脚本中。
5. **回复内容应使用用户的语言。** 如果用户输入中文，回复内容也应为中文（包括标题、标题和解析内容）。
6. **遇到304/403错误时**——请停止请求，切勿重试。这是一个需要付费的功能。请参考[付费功能指南](#paid-feature-guide)来帮助用户升级。

## 快速参考

| 功能 | 命令 |
|------|---------|
| 获取BTC价格 | `node scripts/coin.mjs coin_ticker '{"coin_list":"bitcoin"}'` |
| 获取多种货币价格 | `node scripts/coin.mjs coin_ticker '{"coin_list":"bitcoin,ethereum,solana"}'` |
| 查看K线图 | `node scripts/market.mjs kline '{"symbol":"btcusdt:okex","period":"3600","size":"100"}'` |
| 获取资金费率 | `node scripts/coin.mjs funding_rate '{"symbol":"BTC"}'` |
| 查看多头/空头比率 | `node scripts/features.mjs ls_ratio` |
| 查看新闻快讯 | `node scripts/news.mjs flash_list '{"language":"cn"}'` |
| 查看热门货币 | `node scripts/market.mjs hot_coins '{"key":"defi"}'` |
| 获取未平仓合约量（需付费） | `node scripts/coin.mjs open_interest '{"symbol":"BTC","interval":"15m"}'` |
| 查看大额交易（需付费） | `node scripts/features.mjs big_orders '{"symbol":"btcswapusdt:binance"}'` |

**货币缩写：** `BTC`、`ETH`、`SOL`、`DOGE`、`XRP`在`coin.mjs`中会自动识别。

**中文俚语说明：**
- **大饼** = BTC  
- **姨太** = ETH  
- **狗狗** = DOGE  
- **瑞波** = XRP  
- **索拉纳** = SOL  

## 免费与付费端点

内置的免费密钥支持以下端点（无需API密钥）：

| 脚本 | 免费端点 |
|--------|---------------|
| coin.mjs | `coin_list`, `coin_ticker`, `coin_config`, `funding_rate`, `trade_data` |
| market.mjs | `kline`, `exchanges`, `ticker`, `hot_coins`, `futures_interest` |
| features.mjs | `ls_ratio`, `nav`, `pair_ticker`, `pair_by_market`, `pair_list` |
| news.mjs | `news_list`, `news_rss`, `flash_list` |
| twitter.mjs | `latest`, `search` |
| newsflash.mjs | `search`, `list` |

**所有其他端点均需要付费API密钥。** 如果遇到304/403错误，请参考[付费功能指南](#paid-feature-guide)。

## 设置

使用内置的免费密钥，这些脚本即可直接使用。`.env`文件会从以下位置自动加载：
1. 当前工作目录  
2. `~/.openclaw/workspace/.env`  
3. `~/.openclaw/.env`  

只有在用户明确请求需要配置的功能时，才需要询问设置相关问题。

## 脚本说明

所有脚本的格式为：`node scripts/<名称>.mjs <操作> [参数列表]`

### scripts/coin.mjs — 货币数据

| 操作 | 描述 | 参数 |
|--------|-------------|--------|
| `coin_list` | 列出所有货币 | 无 |
| `coin_ticker` | 实时价格 | `{"coin_list":"bitcoin,ethereum"}` |
| `coin_config` | 货币信息 | `{"coin_list":"bitcoin"}` |
| `funding_rate` | 资金费率 | `{"symbol":"btcswapusdt:binance","interval":"8h"}` （可选参数`"weighted":"true"`表示加权计算） |
| `trade_data` | 交易数据 | `{"dbkey":"btcswapusdt:okcoinfutures"}` |
| `ai_analysis` | AI分析与预测（需付费） | `{"coin_keys":"[\"bitcoin\"]","language":"CN"}` |
| `open_interest` | 未平仓合约量（需付费） | `{"symbol":"BTC","interval":"15m"}` （可选参数`"margin_type":"coin"`表示按货币分类） |
| `liquidation_map` | 清算热图（需付费） | `{"dbkey":"btcswapusdt:binance","cycle":"24h"}` |
| `liquidation_history` | 清算历史记录（需付费） | `{"symbol":"btcswapusdt:binance","interval":"1m"}` |
| `estimated_liquidation` | 预计清算金额（需付费） | `{"dbkey":"btcswapusdt:binance","cycle":"24h"}` |
| `historical_depth` | 历史深度数据（需付费） | `{"key":"btcswapusdt:okcoinfutures"}` |
| `super_depth` | 大额交易深度数据（需付费） | `{"key":"btcswapusdt:okcoinfutures"}` |

### scripts/market.mjs — 市场数据

| 操作 | 描述 | 参数 |
|--------|-------------|--------|
| `exchanges` | 交易所列表 | 无 |
| `ticker` | 交易所行情 | `{"market_list":"okex,binance"}` |
| `hot_coins` | 热门货币 | `{"key":"defi"}` （根据需求选择不同的筛选条件） |
| `futures_interest` | 期货未平仓合约量排名 | `{"lan":"cn"}` |
| `kline` | 标准K线图 | `{"symbol":"btcusdt:okex","period":"3600","size":"100"}` （周期单位：3600=15分钟，14400=4小时，86400=1天） |
| `indicator_kline` | 指标K线图（需付费） | `{"symbol":"btcswapusdt:binance","indicator_key":"fundflow","period":"3600"}` |
| `indicator_pairs` | 指标对数据（需付费） | `{"indicator_key":"fundflow"}` |
| `index_list` | 指数列表（需付费） | 无 |
| `index_price` | 指数价格（需付费） | `{"key":"i:diniw:ice"}` |
| `index_info` | 指数详情（需付费） | `{"key":"i:diniw:ice"}` |
| `stock_quotes` | 股票报价（需付费） | `{"tickers":"i:mstr:nasdaq,i:coin:nasdaq"}` |
| `stock_top_gainer` | 行情涨幅最高的股票（需付费） | `{"us_stock":"true"}` |
| `stock_company` | 公司详情（需付费） | `{"symbol":"i:mstr:nasdaq"}` |
| `treasury_entities` | 持仓实体信息（需付费） | `{"coin":"BTC"}` |
| `treasury_history` | 交易历史记录（需付费） | `{"coin":"BTC"}` |
| `treasury_accumulated` | 持仓累计情况（需付费） | `{"coin":"BTC"}` |
| `treasury_latest_entities` | 最新持仓实体（需付费） | `{"coin":"BTC"}` |
| `treasury_latest_history` | 最新交易历史（需付费） | `{"coin":"BTC"}` |
| `treasury_summary` | 持仓概览（需付费） | `{"coin":"BTC"}` |
| `depth_latest` | 实时深度数据（需付费） | `{"dbKey":"btcswapusdt:binance"}` |
| `depth_full` | 完整订单簿（需付费） | `{"dbKey":"btcswapusdt:binance"}` |
| `depth_grouped` | 分组深度数据（需付费） | `{"dbKey":"btcswapusdt:binance","groupSize":"100"}` |

### scripts/features.mjs — 功能与交易信号

| 操作 | 描述 | 参数 |
|--------|-------------|--------|
| `nav` | 市场导航 | `{"lan":"cn"}` |
| `ls_ratio` | 头寸比率 | 无 |
| `pair_ticker` | 货币对行情 | `{"key_list":"btcusdt:okex,btcusdt:huobipro"}` |
| `pair_by_market` | 按交易所分类的货币对 | `{"market":"binance"}` |
| `pair_list` | 货币对列表 | `{"market":"binance","currency":"USDT"}` |
| `liquidation` | 清算数据（需付费） | `{"type":"1","coinKey":"bitcoin"}` （类型1=按货币，类型2=按交易所） |
| `grayscale_trust` | Grayscale公司的持仓情况（需付费） | 无 |
| `gray_scale` | Grayscale公司的持仓数据（需付费） | `{"coins":"btc,eth"}` |
| `stock_market` | 加密货币股票信息（需付费） | 无 |
| `big_orders` | 大额交易信息（需付费） | `{"symbol":"btcswapusdt:binance"}` |
| `agg_trades` | 聚合交易数据（需付费） | `{"symbol":"btcswapusdt:binance"}` |
| `strategy_signal` | 交易策略信号（需付费） | `{"signal_key":"depth_win_one"}` |
| `signal_alert` | 交易信号提醒（需付费） | 无 |
| `signal_config` | 信号提醒配置（需付费） | `{"lan":"cn"}` |
| `signal_alert_list` | 信号提醒列表（需付费） | 无 |
| `change_signal` | 异常交易信号（需付费） | `{"type":"1"}` |
| `delete_signal` | 删除提醒（需付费） | `{"id":"xxx"}` |

### scripts/news.mjs — 新闻与内容

| 操作 | 描述 | 参数 |
|--------|-------------|--------|
| `news_list` | 新闻列表 | `{"page":"1","pageSize":"20"}` |
| `news_rss` | RSS新闻源 | `{"page":"1"}` |
| `flash_list` | 行业快讯 | `{"language":"cn"}` |
| `newsflash` | AiCoin快讯（需付费） | `{"language":"cn"}` |
| `news_detail` | 新闻详情（需付费） | `{"id":"xxx"}` |
| `exchange_listing` | 交易所公告（需付费） | `{"memberIds":"477,1509"}` （477=Binance，1509=Bitget） |

### scripts/twitter.mjs — Twitter/加密货币相关推文

| 操作 | 描述 | 参数 |
|--------|-------------|--------|
| `latest` | 最新加密货币推文 | `{"language":"cn","page_size":"20","last_time":"1234567890"}` |
| `search` | 搜索推文 | `{"keyword":"bitcoin","language":"cn","page_size":"20"}` |
| `members` | 搜索KOL/用户（需付费） | `{"word":"elon","page":"1","size":"20"}` |
| `interaction_stats` | 推文互动统计（需付费） | `{"flash_ids":"123,456,789"}` （最多50条ID） |

### scripts/newsflash.mjs — Newsflash（OpenData）

| 操作 | 描述 | 参数 |
|--------|-------------|--------|
| `search` | 搜索Newsflash内容 | `{"word":"bitcoin","page":"1","size":"20"}` |
| `list` | 带有筛选条件的Newsflash列表 | `{"pagesize":"20","lan":"cn","date_mode":"range","start_date":"2025-03-01","end_date":"2025-03-04"}` |
| `detail` | Newsflash详细内容（需付费） | `{"flash_id":"123456"}` |

## 跨技能参考

- **交易所交易（买入/卖出/查询余额）**：使用`aicoin-trading`脚本 |
- **Freqtrade策略/回测/部署**：使用`aicoin-freqtrade`脚本 |
- **Hyperliquid大额交易追踪**：使用`aicoin-hyperliquid`脚本 |

## 常见错误

- **错误代码304/403**：表示需要付费功能。请参考[付费功能指南](#paid-feature-guide)。
- **无效的货币代码**：请检查格式，AiCoin使用`btcusdt:okex`，而非`BTC/USDT`。
- **请求频率超过限制**：请等待1-2秒后再尝试请求，或使用批量查询。
- **超时**：请增加请求超时时间，部分端点的响应速度较慢。

## 付费功能指南

当脚本返回304或403错误时，表示该功能需要付费API密钥。**请不要重复请求**。请用用户的语言告知用户：
1. **问题原因**：此功能需要付费的AiCoin API订阅。
2. **获取密钥的方法**：访问[https://www.aicoin.com/opendata`注册并创建API密钥。
3. **费用等级及功能**：
  | 等级 | 价格 | 每分钟请求次数 | 提供的功能 |
  | --- | --- | --- | --- |
  | 免费 | $0 | 15次/分钟 | 价格、K线图、资金费率、头寸比率、新闻 |
  | 基础 | $29/月 | 30次/分钟 | 增加内容数据、交易信号 |
  | 标准 | $79/月 | 80次/分钟 | 增加大额交易信息、清算数据 |
  | 高级 | $299/月 | 300次/分钟 | 增加指数数据、指标K线图 |
  | 专业 | $699/月 | 1200次/分钟 | 所有端点、商业用途 |

**配置方法**：获取密钥后，将其添加到`.env`文件中。脚本会自动从当前工作目录、`~/.openclaw/workspace/.env`或`~/.openclaw/.env`文件中加载`.env`文件。

**配置完成后**，相同的脚本命令即可正常使用，无需修改代码。
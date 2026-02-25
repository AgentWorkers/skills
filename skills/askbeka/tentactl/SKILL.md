---
name: kraken
description: "与Kraken加密货币交易所进行交互。适用场景包括：  
(1) 查看加密货币价格或市场数据；  
(2) 查看账户余额或交易历史；  
(3) 下单或取消订单；  
(4) 制定定期投资（DCA）策略或设置价格警报；  
(5) 任何与Kraken、加密货币交易或投资组合管理相关的内容。  
需要使用`tentactl`二进制文件。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🐙",
        "requires": { "bins": ["tentactl"] },
        "install":
          [
            {
              "id": "cargo",
              "kind": "cargo",
              "package": "tentactl",
              "bins": ["tentactl"],
              "label": "Install tentactl (cargo)",
            },
          ],
      },
  }
---
# Kraken Exchange

这是一个用于Kraken加密货币交易所的命令行工具（CLI）。该工具通过标准输入（stdio）与Kraken的MCP（Message Passing Capability）进行通信，但为了简化使用，也可以直接通过`exec`命令来调用它。

## 设置

首次使用时，请执行以下步骤——从1Password服务中配置API密钥，或手动设置API密钥：

```bash
# Option A: 1Password (recommended)
scripts/setup-keys.sh

# Option B: Manual .env file
echo "KRAKEN_API_KEY=your-key" > ~/.kraken-mcp.env
echo "KRAKEN_API_SECRET=your-secret" >> ~/.kraken-mcp.env
chmod 600 ~/.kraken-mcp.env
```

## 使用方法

所有命令都可以通过`scripts/kraken.sh`文件（该文件会加载`.env`文件并找到对应的二进制执行文件）来执行；或者直接使用`python3 scripts/kraken.py`来执行：

```bash
# Market data (no auth needed)
scripts/kraken.sh get_ticker '{"pair":"XBTUSD"}'
scripts/kraken.sh get_orderbook '{"pair":"ETHUSD","count":5}'
scripts/kraken.sh get_ohlc '{"pair":"SOLUSD","interval":60}'

# Account (needs API keys)
scripts/kraken.sh get_balance
scripts/kraken.sh get_trade_history
scripts/kraken.sh get_open_orders

# Trading (needs API keys) ⚠️ REAL MONEY
scripts/kraken.sh place_order '{"pair":"XBTUSD","direction":"buy","order_type":"market","volume":"0.001","validate":true}'
scripts/kraken.sh cancel_order '{"txid":"TXID-123"}'
```

如果二进制文件已经添加到了系统的`PATH`环境变量中，并且环境变量已经设置完成，那么可以直接使用`python3 scripts/kraken.py`并传入相应的参数来执行命令。

## 工具参考

有关所有参数的详细文档，请参阅`references/tools.md`。

## 安全规则

- 在下达订单之前，**务必**先设置`validate: true`选项。
- 在执行实际订单之前，**务必**先获得用户的确认。
- **绝对不要**在未经用户明确许可的情况下下达订单。
- 市场订单会立即执行；尽可能优先使用限价订单。
- 在取消`validate`选项之前，需要显示验证结果并请求用户的确认。

## 交易对

Kraken使用自己定义的交易对格式，例如`XBTUSD`（而非`BTCUSD`）、`XETHZUSD`、`SOLUSD`等。如果不确定某个交易对是否有效，请尝试使用该交易对——API会返回明确的错误信息来提示无效的交易对。

## 自动化模式

### 定投（Dollar Cost Average, DCA）

可以通过`openclaw cron`来设置定投计划：

```
openclaw cron add --schedule "0 9 * * 1" --task "Buy $50 of BTC on Kraken using the kraken skill. Use validate first, then execute."
```

### 价格警报

可以通过心跳检测（heartbeat）或定时任务（cron）来检查价格变化；当价格达到预设阈值时触发警报。警报配置信息存储在`memory/kraken-alerts.json`文件中。